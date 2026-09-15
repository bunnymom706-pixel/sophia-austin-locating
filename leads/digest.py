#!/usr/bin/env python3
"""Render the morning digest from leads/nightly/<date>.ranked.json.

  python3 leads/digest.py                # today's night file, prints JSON {subject, text, html}
  python3 leads/digest.py --night 2026-09-16
  python3 leads/digest.py --file path/to/x.ranked.json --out /tmp/digest.json
"""
import argparse
import html
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NIGHTLY = ROOT / "nightly"


def default_night():
    central = datetime.now(timezone.utc) - timedelta(hours=5)
    if central.hour >= 20:
        central += timedelta(days=1)
    return central.strftime("%Y-%m-%d")


def contact_line(lead):
    c = lead.get("contact") or {}
    parts = []
    if c.get("reply_email"):
        parts.append(f"CL relay: {c['reply_email']}")
    if c.get("emails_in_post"):
        parts.append("Email: " + ", ".join(c["emails_in_post"]))
    if c.get("phones_in_post"):
        parts.append("Phone: " + ", ".join(c["phones_in_post"]))
    return " | ".join(parts) or "Contact via CL post link"


def build(night, ranked, raw):
    leads = ranked.get("ranked", [])
    counts = ranked.get("counts") or {}
    a = [l for l in leads if l.get("tier") == "A"]
    b = [l for l in leads if l.get("tier") == "B"]
    runs = raw.get("runs", []) if raw else []
    scanned = sum(r.get("scanned", 0) for r in runs)
    new = sum(r.get("new", 0) for r in runs)
    subject = f"CL Leads {night}: {len(leads)} new (A: {len(a)}, B: {len(b)})"

    url_by_pid = {l["pid"]: l.get("url", "") for l in (raw.get("leads", []) if raw else [])}
    title_by_pid = {l["pid"]: l.get("title", "") for l in (raw.get("leads", []) if raw else [])}

    text, htm = [], []
    text.append(f"Good morning. Overnight: {scanned} posts scanned across {len(runs)} runs, {new} new, {len(leads)} worth a reply.")
    htm.append(f"<p style='font:15px/1.5 -apple-system,Segoe UI,Arial'>Good morning. Overnight: <b>{scanned}</b> posts scanned across {len(runs)} runs, <b>{new}</b> new, <b>{len(leads)}</b> worth a reply. Dropped as C tier: {counts.get('C', len(ranked.get('dropped', [])))}.</p>")

    for tier, group in (("A", a), ("B", b)):
        if not group:
            continue
        text.append(f"\n===== TIER {tier} ({len(group)}) =====")
        htm.append(f"<h2 style='font:600 18px -apple-system,Segoe UI,Arial;margin:24px 0 8px'>Tier {tier} ({len(group)})</h2>")
        for i, l in enumerate(group, 1):
            pid = l.get("pid", "")
            url = url_by_pid.get(pid, f"https://austin.craigslist.org/search/hsw?query={pid}")
            title = title_by_pid.get(pid, "") or l.get("why", "")
            meta = f"Budget {l.get('budget','?')} | {l.get('beds','?')} | {l.get('area','?')} | Move {l.get('timeline','?')} | Score {l.get('score')}"
            flags = ", ".join(l.get("red_flags") or [])
            text += [f"\n{i}. {title}", f"   {meta}", f"   Why: {l.get('why','')}"]
            if flags:
                text.append(f"   Flags: {flags}")
            text += [f"   Post: {url}", f"   {contact_line(l)}", "   --- reply draft ---", "   " + l.get("reply_draft", "").replace("\n", "\n   ")]
            htm.append(
                "<div style='border:1px solid #ddd;border-radius:10px;padding:12px 14px;margin:10px 0;font:14px/1.5 -apple-system,Segoe UI,Arial'>"
                f"<div style='font-weight:600'>{i}. {html.escape(title)}</div>"
                f"<div style='color:#555'>{html.escape(meta)}</div>"
                f"<div>Why: {html.escape(l.get('why',''))}</div>"
                + (f"<div style='color:#a00'>Flags: {html.escape(flags)}</div>" if flags else "")
                + f"<div><a href='{html.escape(url)}'>Open post</a> &nbsp; {html.escape(contact_line(l))}</div>"
                f"<pre style='white-space:pre-wrap;background:#f6f6f6;padding:10px;border-radius:8px;font:13px/1.45 -apple-system,Segoe UI,Arial;margin:8px 0 0'>{html.escape(l.get('reply_draft',''))}</pre>"
                "</div>"
            )
    if not leads:
        text.append("\nNo A or B leads tonight. Quiet night on the boards.")
        htm.append("<p>No A or B leads tonight. Quiet night on the boards.</p>")
    text.append("\nReply from the post link (CL relay) or the contact shown. Drafts follow your locked rules; edit freely.")
    htm.append("<p style='color:#777;font:13px -apple-system,Segoe UI,Arial'>Reply from the post link (CL relay) or the contact shown. Drafts follow your locked rules; edit freely.</p>")
    return {"subject": subject, "text": "\n".join(text), "html": "\n".join(htm), "counts": {"A": len(a), "B": len(b), "scanned": scanned, "new": new}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--night", default=default_night())
    ap.add_argument("--file", help="explicit .ranked.json path")
    ap.add_argument("--out", help="write JSON here instead of stdout")
    args = ap.parse_args()
    ranked_path = Path(args.file) if args.file else NIGHTLY / f"{args.night}.ranked.json"
    raw_path = Path(str(ranked_path).replace(".ranked.json", ".json"))
    ranked = json.loads(ranked_path.read_text()) if ranked_path.exists() else {"ranked": [], "dropped": [], "counts": {}}
    raw = json.loads(raw_path.read_text()) if raw_path.exists() else {}
    digest = build(args.night if not args.file else ranked_path.stem.replace(".ranked", ""), ranked, raw)
    out = json.dumps(digest, indent=1)
    if args.out:
        Path(args.out).write_text(out)
        print(digest["subject"])
    else:
        print(out)


if __name__ == "__main__":
    main()
