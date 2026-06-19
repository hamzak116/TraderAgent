---
description: Weekly learning review — grade calls, extract lessons, check calibration
allowed-tools: Bash(python3 trader/scripts/*), Bash(bash trader/scripts/sync.sh*), Read, Write, Edit, Glob, Grep, WebSearch
---

You are the trading agent. Read `trader/AGENT.md` and follow the **Learning
loop** section exactly.

Quick reference:
0. Sync first: `bash trader/scripts/sync.sh pull`.
1. `python3 trader/scripts/portfolio.py history` — full record + calibration stats.
2. For every call closed since the last review: write a post-mortem in `trader/lessons.md` — thesis vs what happened, was it thesis/timing/sizing error (or skill on wins), and the specific falsifiable rule that follows.
3. Check calibration: hit rate, winner/loser asymmetry, confidence-vs-outcome correlation. Persistent bias → propose a change to AGENT.md to the user (do not silently edit it).
4. Re-read open positions against current lessons — flag any holding a lesson argues against.
5. Refresh dashboard: `python3 trader/scripts/dashboard.py`. Then push state: `bash trader/scripts/sync.sh push "review: <today> lessons"`.
6. Notify: `python3 trader/scripts/notify.py "<calibration stats + new lessons>"` (best-effort).
7. Reply with: calibration stats, new lessons added, any proposed manual changes.
