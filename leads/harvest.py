#!/usr/bin/env python3
"""Craigslist Austin "housing wanted" harvester.

Read-only. Pulls new posts from the sections in --sections, dedupes against
leads/state.json, and appends raw leads to leads/nightly/<date>.json.
Never logs in, never posts, never replies.

Usage:
  python3 leads/harvest.py                   # normal nightly run
  python3 leads/harvest.py --dry-run --max 10  # print, write nothing
"""
import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

from playwright.sync_api import TimeoutError as PWTimeout
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
STATE_PATH = ROOT / "state.json"
NIGHTLY_DIR = ROOT / "nightly"
SITE = "https://austin.craigslist.org"
CHROMIUM = os.environ.get("PW_CHROMIUM", "/opt/pw-browsers/chromium")
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
DELAY_S = 2.0  # polite pacing between page loads
SEEN_TTL_DAYS = 30

SECTIONS = {
    "hsw": "housing wanted",
    "roo": "rooms and shares",
    "sub": "sublets and temporary",
}

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_RE = re.compile(r"(?:\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}")
BUDGET_RE = re.compile(r"\$\s?(\d{1,2}[,.]?\d{3}|\d{3,4})(?:\s*(?:/|per|a)\s*(?:mo|month))?", re.I)
PID_RE = re.compile(r"/(\d{9,11})\.html")


def log(msg):
    print(f"[harvest {datetime.now(timezone.utc).strftime('%H:%M:%S')}] {msg}", file=sys.stderr, flush=True)


def load_state():
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return {"seen": {}, "last_run": None}


def save_state(state):
    cutoff = (datetime.now(timezone.utc) - timedelta(days=SEEN_TTL_DAYS)).isoformat()
    state["seen"] = {k: v for k, v in state["seen"].items() if v >= cutoff}
    state["last_run"] = datetime.now(timezone.utc).isoformat()
    STATE_PATH.write_text(json.dumps(state, indent=1, sort_keys=True) + "\n")


def nightly_path(now_utc):
    # A "night" is keyed by the Central date the digest goes out on (morning).
    central = now_utc - timedelta(hours=5)
    if central.hour >= 20:  # 8pm CT or later belongs to tomorrow's digest
        central += timedelta(days=1)
    return NIGHTLY_DIR / f"{central.strftime('%Y-%m-%d')}.json"


def list_section(page, sec, max_posts):
    """Return [{pid,url,title,price,hood,posted}] from a section search page, newest first."""
    url = f"{SITE}/search/{sec}?sort=date"
    log(f"list {sec}: {url}")
    page.goto(url, wait_until="domcontentloaded", timeout=45000)
    try:
        page.wait_for_selector(".cl-search-result, li.cl-static-search-result, .result-row", timeout=20000)
    except PWTimeout:
        log(f"list {sec}: no result rows rendered (blocked or layout change)")
        return []
    rows = page.evaluate(
        """() => {
          const out = [];
          const nodes = document.querySelectorAll('.cl-search-result, li.cl-static-search-result, .result-row');
          for (const n of nodes) {
            const a = n.querySelector('a.posting-title, a.cl-app-anchor, a.result-title, a[href*=".html"]');
            if (!a) continue;
            const t = n.querySelector('.label, .title, .result-title, .posting-title');
            const price = n.querySelector('.priceinfo, .price, .result-price');
            const hood = n.querySelector('.meta .supertitle, .location, .result-hood, .meta span[title]');
            const time = n.querySelector('.meta span[title], time');
            out.push({
              url: a.href,
              title: (t ? t.textContent : a.textContent).trim(),
              price: price ? price.textContent.trim() : '',
              hood: hood ? hood.textContent.trim() : '',
              posted: time ? (time.getAttribute('datetime') || time.getAttribute('title') || time.textContent) : '',
            });
          }
          return out;
        }"""
    )
    items = []
    for r in rows:
        m = PID_RE.search(r["url"])
        if not m:
            continue
        r["pid"] = m.group(1)
        r["section"] = sec
        items.append(r)
        if len(items) >= max_posts:
            break
    log(f"list {sec}: {len(items)} rows")
    return items


def fetch_post(page, item):
    """Open the post, pull body/attrs/contact. Adds keys in place."""
    page.goto(item["url"], wait_until="domcontentloaded", timeout=45000)
    try:
        page.wait_for_selector("#postingbody, .removed", timeout=15000)
    except PWTimeout:
        item["error"] = "post body not rendered"
        return item
    if page.query_selector(".removed"):
        item["error"] = "removed"
        return item
    data = page.evaluate(
        """() => {
          const q = s => document.querySelector(s);
          const body = q('#postingbody');
          if (body) { const qr = body.querySelector('.print-qrcode-container'); if (qr) qr.remove(); }
          const t = q('time.date.timeago, .postinginfo time');
          const attrs = [...document.querySelectorAll('.attrgroup span, .attrgroup .attr')].map(e => e.textContent.trim()).filter(Boolean);
          return {
            title: (q('#titletextonly') || {textContent: ''}).textContent.trim(),
            body: body ? body.innerText.trim() : '',
            posted: t ? (t.getAttribute('datetime') || t.textContent) : '',
            map: (q('.mapaddress') || {textContent: ''}).textContent.trim(),
            attrs,
            updated: [...document.querySelectorAll('.postinginfo')].map(e => e.textContent.trim()).join(' | '),
          };
        }"""
    )
    item.update({k: v for k, v in data.items() if v})
    text = f"{item.get('title','')}\n{item.get('body','')}"
    item["emails_in_post"] = sorted(set(EMAIL_RE.findall(text)))
    item["phones_in_post"] = sorted(set(m.strip() for m in PHONE_RE.findall(text)))
    item["budgets_in_post"] = sorted(set(BUDGET_RE.findall(text)))
    item["reply_email"] = fetch_reply_email(page, item)
    return item


def fetch_reply_email(page, item):
    """Craigslist relay address (xxxx@reply.craigslist.org). Two strategies, both best-effort."""
    # 1. JSON endpoint the reply button calls
    try:
        r = page.request.get(f"{SITE}/reply/aus/{item['section']}/{item['pid']}", timeout=15000)
        if r.ok:
            txt = r.text()
            m = re.search(r"[\w.+-]+@reply\.craigslist\.org", txt)
            if m:
                return m.group(0)
            try:
                j = r.json()
                for k in ("replyEmail", "reply_email", "email"):
                    if j.get(k):
                        return j[k]
            except Exception:
                pass
    except Exception as e:
        log(f"reply json {item['pid']}: {str(e)[:80]}")
    # 2. Click the reply button and read the revealed address
    try:
        btn = page.query_selector("button.reply-button, .reply-button, a.reply-button")
        if btn:
            btn.click()
            page.wait_for_timeout(2500)
            m = re.search(r"[\w.+-]+@reply\.craigslist\.org", page.content())
            if m:
                return m.group(0)
    except Exception as e:
        log(f"reply click {item['pid']}: {str(e)[:80]}")
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sections", default="hsw,roo,sub")
    ap.add_argument("--max", type=int, default=60, help="max NEW posts to open per run (all sections)")
    ap.add_argument("--list-max", type=int, default=120, help="max rows to read per section list")
    ap.add_argument("--dry-run", action="store_true", help="print leads, do not touch state/nightly")
    ap.add_argument("--headed", action="store_true")
    args = ap.parse_args()

    now = datetime.now(timezone.utc)
    state = load_state()
    seen = state["seen"]
    out_path = nightly_path(now)
    NIGHTLY_DIR.mkdir(exist_ok=True)
    existing = json.loads(out_path.read_text()) if out_path.exists() else {"night": out_path.stem, "runs": [], "leads": []}

    new_leads, scanned = [], 0
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not args.headed, executable_path=CHROMIUM)
        ctx = browser.new_context(user_agent=UA, locale="en-US", viewport={"width": 1280, "height": 900})
        page = ctx.new_page()
        candidates = []
        for sec in [s.strip() for s in args.sections.split(",") if s.strip()]:
            try:
                rows = list_section(page, sec, args.list_max)
            except Exception as e:
                log(f"list {sec} failed: {str(e)[:200]}")
                rows = []
            scanned += len(rows)
            candidates += [r for r in rows if r["pid"] not in seen]
            time.sleep(DELAY_S)
        log(f"{scanned} scanned, {len(candidates)} unseen, opening up to {args.max}")
        for item in candidates[: args.max]:
            try:
                fetch_post(page, item)
            except Exception as e:
                item["error"] = str(e)[:200]
            item["harvested_at"] = now.isoformat()
            new_leads.append(item)
            seen[item["pid"]] = now.isoformat()
            time.sleep(DELAY_S)
        browser.close()

    if args.dry_run:
        print(json.dumps(new_leads, indent=1))
        log(f"dry run: {len(new_leads)} new leads, nothing written")
        return

    existing["runs"].append({"at": now.isoformat(), "scanned": scanned, "new": len(new_leads)})
    existing["leads"] += new_leads
    out_path.write_text(json.dumps(existing, indent=1) + "\n")
    save_state(state)
    print(json.dumps({"night_file": str(out_path.relative_to(ROOT.parent)), "scanned": scanned, "new": len(new_leads)}))


if __name__ == "__main__":
    main()
