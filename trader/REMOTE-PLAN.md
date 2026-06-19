# Plan: Local → Remote Routines

**Status**: **R1 ✅ R1b ✅ R2 ✅ R3 ✅ — laptop-independent operation achieved
(2026-06-15).** Three cloud routines run on Anthropic infra against the GitHub
repo (Network access = Full so Yahoo + Telegram are reachable), state persists
to `main`, briefs deliver to Telegram. Local scheduled tasks disabled. Details: `trader/cloud-routines.md`.

**R4 ✅ (2026-06-15)** — `trader/scripts/dashboard.py` regenerates a private
`DASHBOARD.md` (GitHub mobile app) + `dashboard.html` (open locally) from
portfolio/suggestions each routine, before the state push. No public hosting
(repo stays private). All remote phases complete.
**Goal**: Daily routines run without the laptop being on; portfolio data
accessible from anywhere; reports delivered to the user's phone.

## Current state (and why it's laptop-bound)

The three routines (`trader-morning-brief`, `trader-close-report`,
`trader-weekly-review`) are desktop-app scheduled tasks. They run only while
the Claude app is open, and all state (`portfolio.json`, `suggestions.json`,
`journal/`, `lessons.md`) lives only on this machine.

## Phase R1 — Put the project on GitHub (prerequisite) ✅ DONE 2026-06-15

1. ✅ `git init` (main branch), `.gitignore` excludes secrets (`.env`,
   `*.key`), `.DS_Store`, `.obsidian/workspace.json`. Added `README.md`.
2. ✅ Private repo `moodysamkary/trading-agent` created via `gh`, pushed.
3. ✅ `trader/scripts/sync.sh` (pull / push helpers, never aborts a routine on
   git error). All routines (slash commands + scheduled-task prompts + the
   "State persistence" section of AGENT.md) now pull at start and push at end.

Payoff already live: full history/auditability of every ledger change, and
state readable from any device via the GitHub mobile app.

## Phase R2 — Move schedules to cloud routines

**Decision (2026-06-15): Claude cloud routines** (chosen over GitHub Actions).
Sequenced **after R3 token setup**. The Telegram token must be set as a cloud
secret/env var (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`) since `.env` is
gitignored and won't travel in the repo — `notify.py` reads `os.environ`
first, so this works once configured.

Path: **Claude Code cloud routines** via the `RemoteTrigger` API
(`/v1/code/triggers`) — runs on Anthropic infra, clones the GitHub repo.
Full setup steps, schema, and routine prompts: see `trader/cloud-routines.md`.

**Gating prerequisite (browser, user-only):** connect `moodysamkary/trading-agent`
at claude.ai/code to create a Code **environment** (`environment_id`) and add
`TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` as environment secrets. Claude can
create the three triggers via the API once the `environment_id` exists.

1. Recreate the three schedules as cloud routines with the same prompts,
   adding: pull latest state at start, commit + push state at end.
2. Mind the timezone: cloud cron may be UTC — 7:45 AM CT = 12:45 UTC (CDT) /
   13:45 UTC (CST); re-check at DST changes, or accept ET-anchored times.
3. **Verify before cutover** (cloud sandboxes restrict network egress):
   - Yahoo Finance endpoint (`query1.finance.yahoo.com`) reachable? If not,
     swap `quotes.py` to an allowlisted/free API — FMP, Finnhub, or Alpaca
     (full docs already in `raw/`, see `raw/sources.md`).
   - WebSearch available in routine runs (needed for sentiment/news).
4. Run local + cloud in parallel for a few days; disable local tasks once the
   cloud runs prove stable (`update_scheduled_task enabled=false`, keep as
   manual backups).

Fallback if cloud routines don't fit the plan/billing: **GitHub Actions cron**
running headless Claude Code (`claude -p "/trader-morning"`) with an
`ANTHROPIC_API_KEY` repo secret; the workflow commits state back and posts the
notification itself. More plumbing, fully controllable, billed per API token.

## Phase R3 — Phone delivery of reports

Recommendation: **Telegram bot** — easiest, free, good mobile UX:

1. Create a bot via @BotFather (2 minutes) → bot token; get your `chat_id`.
2. Add `trader/scripts/notify.py`: POST the routine's final summary to
   `https://api.telegram.org/bot<token>/sendMessage` (stdlib `urllib`, ~20 lines).
3. Each routine's last step: send the brief/report summary (with a link to
   the full journal entry on GitHub). Token lives in a secret (cloud routine
   env / Actions secret), **never committed to the repo**.

Alternatives, ranked by effort:
- **Slack**: incoming webhook — equally trivial if you live in Slack; also has
  a first-party Claude integration.
- **Email**: trivial fallback.
- **WhatsApp**: requires Meta Business API or Twilio — approval process,
  per-message costs, heaviest setup. Only worth it if WhatsApp is strongly
  preferred (this was flagged as open question OQ1 in the April spec).

## Phase R4 (optional) — Glanceable dashboard

A small static page (GitHub Pages) rendering `portfolio.json` +
`suggestions.json`: positions, P&L vs SPY, call history. Read-only, no
secrets. The GitHub mobile app + Telegram messages may make this unnecessary.

## Unchanged invariants

- The agent still never trades and never touches money — remote execution
  changes where research runs, not what it's allowed to do.
- Profile constraints, risk tiers, learning loop: identical (AGENT.md travels
  with the repo).
- Cost note: cloud routines consume plan usage; GitHub Actions consumes API
  tokens — worth a week of parallel running to gauge daily cost either way.

## Suggested order of execution

R1 (30 min) → R3 with local routines first (notifications are useful
immediately) → R2 (the actual decoupling from the laptop) → R4 if wanted.
