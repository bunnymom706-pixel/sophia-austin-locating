---
name: savepdf
description: Save a PDF of what happened in this session so Sophia can download it and remember it. Use when she types /savepdf or asks to save, export, or download a PDF of the session, the day, or the conversation.
---

# /savepdf

Make a downloadable PDF of this session. Everything that happened, with dates and times. Then hand it to her.

## Steps

1. **Write the summary** as Markdown at `daily-log/sessions/YYYY-MM-DD-<short-slug>.md`. Use today's date. If the session spans days, put the range in the title and say when it started and when it resumed. Sections, in this order:
   - Title: `# Session: <name or short description>`
   - One line under it: dates covered, and the current time in Austin (America/Chicago) when saved.
   - **What happened** as a timeline, one line each, with the time when known. Include anything she reported, anything logged, anything built, anything decided.
   - **What got logged** to `daily-log/2026-XX.md` (or whichever month), summarized.
   - **Exercises given** in this session, if any, as the same numbered lists she ran, with the result she reported.
   - **Decisions and rules** made or changed in the session.
   - **Dates coming up** that were mentioned. Always include what is already known: quarterly taxes Sept 15 and Jan 15, Oportun goal dates, the December target.
   - **Open items**: anything unfinished, blocked, or waiting on her.
   - **What she already did**: a short list of what got done. This is the part she reads when defeated. No lecture.
2. **Render it**:
   ```
   python3 .claude/skills/savepdf/savepdf.py daily-log/sessions/<file>.md
   ```
   The PDF lands at `daily-log/pdf/<file>.pdf`. No pip packages needed. Uses the pre-installed Chromium.
3. **Send it** with `SendUserFile`, display `attach`, so she can download it. Do this before anything else finishes. The PDF is the deliverable.
4. **Commit** the Markdown and the PDF to the current branch and push. If the push is denied by a permission check, say so plainly and tell her the file is still saved locally and was already sent to her.

## Style
- Her voice back to her. Plain words. Short lines. No scores unless she asked for them.
- Times as she gave them. `~` for approximate. "Time not given" when she didn't say.
- Streak language only: "day 1", "night 2". Never "you missed".
- Done beats good. Ship the PDF even if a section is thin.
