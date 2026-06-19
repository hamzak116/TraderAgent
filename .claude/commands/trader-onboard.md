---
description: First-run interview — risk tolerance, goals, constraints; initializes the paper portfolio
allowed-tools: Bash(python3 trader/scripts/*), Read, Write, AskUserQuestion
---

You are the trading agent. Read `trader/AGENT.md` first. This command sets up
(or re-runs) the user profile that every other routine depends on.

1. If `trader/profile.md` already exists, show it and ask whether to update or
   start over.
2. Interview the user with AskUserQuestion (not free text) covering:
   - **Risk tolerance** — map to a tier from AGENT.md's table
     (conservative / moderate / aggressive / speculative), and probe with a
     concrete scenario: "a position drops 15% in a week with no news — sell,
     hold, or buy more?"
   - **Financial goal** — beat S&P long-term / income / aggressive growth /
     learning, and target return expectation.
   - **Horizon** — typical intended holding period (days / weeks / months / years).
   - **Paper capital** — how much the simulated portfolio starts with (should
     mirror what they'd realistically invest).
   - **Constraints** — sectors or stocks to avoid or favor, ESG limits,
     max single-position comfort, anything they already hold in real life.
   - **Experience level** — calibrates how much explanation reports include.
3. Write `trader/profile.md`: tier, goals, constraints, the implied limits
   (max position %, stop distance, position count from the tier table), and
   the date. Note that the spec's risk warning applies if target requires
   speculative tier (state expected variance honestly).
4. Initialize the ledger:
   `python3 trader/scripts/portfolio.py init --cash <amount>`
5. Confirm to the user: profile summary, paper starting cash, SPY benchmark
   start price, and that the daily routines are now live.
