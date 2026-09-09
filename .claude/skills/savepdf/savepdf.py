#!/usr/bin/env python3
"""Turn a Markdown file into a clean PDF using the pre-installed Chromium.

Usage:
    python3 .claude/skills/savepdf/savepdf.py <input.md> [output.pdf]

If output is omitted, the PDF lands in daily-log/pdf/<input-stem>.pdf.
No third-party Python packages needed. Chromium is looked up under
/opt/pw-browsers, then PATH.
"""
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]

CSS = """
@page { size: Letter; margin: 0.75in 0.8in; }
body { font-family: Helvetica, Arial, sans-serif; font-size: 11pt; line-height: 1.45; color: #1a1a1a; }
h1 { font-size: 22pt; margin: 0 0 4pt; }
h2 { font-size: 15pt; margin: 20pt 0 6pt; border-bottom: 1px solid #bbb; padding-bottom: 3pt; }
h3 { font-size: 12.5pt; margin: 14pt 0 4pt; }
p { margin: 4pt 0 8pt; }
ul, ol { margin: 2pt 0 8pt; padding-left: 20pt; }
li { margin: 2pt 0; }
table { border-collapse: collapse; margin: 6pt 0 10pt; width: 100%; font-size: 10pt; }
th, td { border: 1px solid #ccc; padding: 4pt 6pt; vertical-align: top; text-align: left; }
th { background: #f0f0f0; }
hr { border: 0; border-top: 1px solid #bbb; margin: 14pt 0; }
code { font-family: Menlo, Consolas, monospace; font-size: 9.5pt; background: #f3f3f3; padding: 0 3pt; }
.meta { color: #666; font-size: 10pt; margin-bottom: 14pt; }
"""


def inline(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def md_to_html(md: str) -> str:
    out = []
    lines = md.splitlines()
    i = 0
    list_stack = []  # each entry: "ul" or "ol"

    def close_lists(to_depth=0):
        while len(list_stack) > to_depth:
            out.append(f"</{list_stack.pop()}>")

    para = []

    def flush_para():
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para.clear()

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            flush_para()
            close_lists()
            i += 1
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            flush_para(); close_lists()
            level = len(m.group(1))
            out.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            i += 1
            continue

        if re.match(r"^(-{3,}|\*{3,}|_{3,})$", stripped):
            flush_para(); close_lists()
            out.append("<hr>")
            i += 1
            continue

        if stripped.startswith("|") and i + 1 < len(lines) and re.match(r"^\|?\s*:?-{2,}", lines[i + 1].strip()):
            flush_para(); close_lists()
            header = [c.strip() for c in stripped.strip("|").split("|")]
            out.append("<table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in header) + "</tr></thead><tbody>")
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells) + "</tr>")
                i += 1
            out.append("</tbody></table>")
            continue

        m = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", line)
        if m:
            flush_para()
            indent = len(m.group(1).replace("\t", "    "))
            depth = indent // 2 + 1
            kind = "ol" if m.group(2)[0].isdigit() else "ul"
            while len(list_stack) > depth:
                out.append(f"</{list_stack.pop()}>")
            while len(list_stack) < depth:
                list_stack.append(kind)
                out.append(f"<{kind}>")
            if list_stack[-1] != kind and len(list_stack) == depth:
                out.append(f"</{list_stack.pop()}>")
                list_stack.append(kind)
                out.append(f"<{kind}>")
            body = m.group(3)
            body = re.sub(r"^\[ \]\s*", "☐ ", body)
            body = re.sub(r"^\[x\]\s*", "☑ ", body, flags=re.I)
            out.append(f"<li>{inline(body)}</li>")
            i += 1
            continue

        para.append(stripped)
        i += 1

    flush_para(); close_lists()
    return "\n".join(out)


def find_chromium() -> str:
    for c in [
        "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
        "/opt/pw-browsers/chromium/chrome-linux/chrome",
    ]:
        if os.path.exists(c):
            return c
    for root in Path("/opt/pw-browsers").glob("chromium*/chrome-linux/chrome"):
        return str(root)
    for name in ("chromium", "chromium-browser", "google-chrome", "chrome"):
        p = shutil.which(name)
        if p:
            return p
    sys.exit("No Chromium found. Install chromium or set PLAYWRIGHT_BROWSERS_PATH.")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1]).resolve()
    if len(sys.argv) > 2:
        dst = Path(sys.argv[2]).resolve()
    else:
        dst = REPO / "daily-log" / "pdf" / (src.stem + ".pdf")
    dst.parent.mkdir(parents=True, exist_ok=True)

    md = src.read_text(encoding="utf-8")
    title_m = re.search(r"^#\s+(.*)$", md, re.M)
    title = html.escape(title_m.group(1)) if title_m else src.stem
    doc = f"<!doctype html><html><head><meta charset='utf-8'><title>{title}</title><style>{CSS}</style></head><body>{md_to_html(md)}</body></html>"

    with tempfile.TemporaryDirectory() as td:
        h = Path(td) / "doc.html"
        h.write_text(doc, encoding="utf-8")
        cmd = [
            find_chromium(), "--headless=new", "--no-sandbox", "--disable-gpu",
            "--no-pdf-header-footer", f"--print-to-pdf={dst}", f"file://{h}",
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if not dst.exists():
            sys.exit(f"Chromium failed:\n{r.stderr[-2000:]}")
    print(dst)


if __name__ == "__main__":
    main()
