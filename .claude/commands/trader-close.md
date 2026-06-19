---
description: Market-close routine — daily performance report on the suggested portfolio
allowed-tools: Bash(python3 trader/scripts/*), Bash(bash trader/scripts/sync.sh*), Read, Write, Glob, Grep, WebSearch, WebFetch
---

You are the trading agent. Read `trader/AGENT.md` and follow the **Close
routine** section exactly.

Quick reference:
0. Sync first: `bash trader/scripts/sync.sh pull`.
1. If `trader/profile.md` is missing, stop and tell the user to run `/trader-onboard`.
2. `python3 trader/scripts/portfolio.py status` — the day's numbers vs SPY.
3. For each position: explain the day's move (WebSearch the name if it moved >2% or against the market), check distance to stop/target.
4. If a stop is clearly breached, record the sell suggestion now via `portfolio.py sell`; otherwise flag for tomorrow morning.
5. Write `trader/journal/<today>-close.md`: performance table, narrative, flags.
6. Refresh dashboard: `python3 trader/scripts/dashboard.py`. Then push state: `bash trader/scripts/sync.sh push "close: <today> report"`.
7. Notify: `python3 trader/scripts/notify.py "<headline + narrative>"` (best-effort).
8. Reply to the user leading with the headline: portfolio day move and total return vs SPY, then the narrative. If lagging SPY, say so in the first line.
