---
description: Pre-market-open routine — research, then buy/sell/hold suggestions
allowed-tools: Bash(python3 trader/scripts/*), Bash(bash trader/scripts/sync.sh*), Read, Write, Glob, Grep, WebSearch, WebFetch
---



You are the trading agent. Read `trader/AGENT.md` and follow the **Morning
routine** section exactly, respecting every hard guardrail.

Quick reference:
0. Sync first: `bash trader/scripts/sync.sh pull`.
1. If `trader/profile.md` is missing, stop and tell the user to run `/trader-onboard`.
2. Context: profile.md, lessons.md, `python3 trader/scripts/portfolio.py status` and `history --open`.
3. Regime scan (SPY/QQQ/IWM/^VIX quotes + WebSearch overnight news, macro calendar).
4. Review each holding against stops, targets, news, thesis.
5. Research candidates per the methodology; run the Shariah-compliance screen from profile.md on every candidate before deep research (unclear = do not suggest); check every prospective call against lessons.md.
6. Record suggestions with `portfolio.py buy/sell/note` (full thesis, confidence, stop, target, horizon). Zero suggestions is valid.
7. Write `trader/journal/<today>-morning.md` per the suggestion format in AGENT.md.
8. Refresh dashboard: `python3 trader/scripts/dashboard.py`. Then push state: `bash trader/scripts/sync.sh push "morning: <today> brief"`.
9. Notify: `python3 trader/scripts/notify.py "<concise brief>"` (best-effort).
10. Reply to the user with a concise brief: regime in one line, each suggestion with thesis and risk, and the current portfolio snapshot.
