# trading-agent

A **research-only** stock trading agent built on the LLM Wiki pattern. It
suggests buys/sells daily, tracks every suggestion in a paper portfolio
benchmarked against the S&P 500, and learns from graded outcomes.

> **It never executes trades and has no access to money or a brokerage.**
> Every suggestion is simulated in a paper ledger so the track record is
> honest whether or not the human acts on it. Not financial advice.

## Layout

| Path | What |
|---|---|
| `trader/AGENT.md` | Operating manual — guardrails, routines, risk tiers, learning loop |
| `trader/profile.md` | User's risk profile, goals, constraints |
| `trader/scripts/` | `quotes.py` (live prices), `portfolio.py` (paper ledger + alpha-vs-SPY grading) |
| `trader/portfolio.json`, `suggestions.json` | Ledger state — the source of truth |
| `trader/lessons.md` | Post-mortems from graded calls; read before every morning run |
| `trader/journal/` | Daily morning briefs and close reports |
| `DASHBOARD.md` / `dashboard.html` | Auto-generated portfolio dashboard (markdown for the GitHub mobile app; HTML to open locally). Regenerated each routine by `trader/scripts/dashboard.py`. |
| `trader/REMOTE-PLAN.md` | Plan for laptop-independent (cloud) execution + phone delivery |
| `wiki/` | Knowledge base (index, log, agent docs) |
| `raw/` | Methodology source material (immutable) |

## Routines

Run via slash commands or on a schedule:

- `/trader-onboard` — first-run interview; initializes profile + ledger
- `/trader-morning` — pre-open: regime scan, research, buy/sell suggestions
- `/trader-close` — post-close: performance vs SPY, move explanations
- `/trader-review` — weekly: grade calls, extract lessons, check calibration

## Guardrails

Never trades · equities long-only (no options/futures/crypto/shorting) ·
every suggestion carries thesis/confidence/stop/target/horizon · suggestions
respect the user's profile constraints · performance numbers come only from
the ledger scripts.
