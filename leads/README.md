# Overnight Craigslist lead harvester

Read-only. Watches Austin Craigslist "housing wanted" (hsw), "rooms and shares" (roo), and "sublets" (sub) overnight, qualifies each renter post with agents, drafts a reply in Sophia's locked voice, and emails one ranked digest at 6am CT. It never logs into Craigslist, never posts, never replies.

## Pieces
- `harvest.py` Playwright scraper. New posts only (dedupe in `state.json`, 30 day memory). Appends to `nightly/<date>.json`.
- `qualify_rules.md` scoring rubric (A >= 70, B 40..69, C dropped).
- `reply_rules.md` reply copy spec (no em dashes, <= 3 emoji, fixed signature).
- `../.claude/workflows/leads-qualify.js` multi-agent workflow: chunks of 8 leads per agent, then one merge/rank agent writes `nightly/<date>.ranked.json`.
- `digest.py` renders subject/text/html from the ranked file.

## Schedule
Routine "CL Night Harvest" (claude.ai/code -> Routines) fires a fresh cloud session hourly, 10pm to 6am CT (`0 3-11 * * *` UTC while on CDT; change to `0 4-12 * * *` after the November DST switch). Each fire harvests + qualifies + commits. The 6am fire also sends the Gmail digest to sophia.reddehase@gmail.com.

Pause: disable the Routine. Change hours: edit its cron. Change scoring or voice: edit the two rules files, no code change needed.

## Requirements
- Cloud environment network access must allow `craigslist.org` (Full access, or allowlist). Otherwise harvest returns 0 rows with "no result rows rendered".
- Gmail connector attached to the Routine.
- `pip install playwright` (browser already in the image at `/opt/pw-browsers/chromium`).

## Manual run
```
pip install -q playwright
python3 leads/harvest.py --dry-run --max 10     # look before writing
python3 leads/harvest.py                        # writes nightly + state
# then in Claude: Workflow scriptPath=.claude/workflows/leads-qualify.js args={"nightFile":"leads/nightly/<date>.json","pids":[...]}
python3 leads/digest.py --night <date>
```
