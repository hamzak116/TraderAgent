# R2 — Cloud Routines Setup

How to run the daily routines on Anthropic's cloud (Claude Code Routines) so
the laptop can be off. Mechanism: claude.ai Code Routines, which clone the
GitHub repo and run on a schedule. Created via the `RemoteTrigger` API
(`/v1/code/triggers`) or the web UI at claude.ai/code/routines.

## Schema (confirmed 2026-06-15 by probing the API)

A trigger needs:
- `name`
- `cron_expression` — 5-field cron, **local timezone**
- `job_config.ccr.environment_id` — **the gating prerequisite** (see below)
- `job_config.ccr.session_context.allowed_tools` — defaults are fine (includes
  Bash, Read, Write, WebSearch, WebFetch, Skill, etc.)
- the routine prompt (set in the web UI, or via the API session config)

## One-time setup (browser — only the user can do this)

1. Go to **claude.ai/code** and connect the GitHub repo
   **`moodysamkary/trading-agent`**. This installs the **Claude GitHub App**
   on the repo (grants clone access) and creates a **Code environment** with
   an `environment_id`.
2. In that environment's settings, add two **secrets / env vars** (so the
   cloud run can send Telegram messages — `.env` is gitignored and is NOT in
   the repo):
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
   `notify.py` reads `os.environ` first, so this is all it needs.
3. Hand the `environment_id` to Claude here, OR create the three routines
   directly in the web UI by pasting the prompts below.

## The three routines (schedules in America/Chicago)

Same prompts as the local scheduled tasks — they read `trader/AGENT.md` and
bookend with `sync.sh` pull/push + `notify.py`. The repo is already cloned by
the environment, so the prompt just needs to run the routine.

| Routine | Cron (CT) | Prompt source |
|---|---|---|
| morning brief | `45 7 * * 1-5` | local task `trader-morning-brief` |
| close report | `10 15 * * 1-5` | local task `trader-close-report` |
| weekly review | `0 16 * * 5` | local task `trader-weekly-review` |

(The exact prompt text lives in `~/.claude/scheduled-tasks/<id>/SKILL.md` and
is reproduced when the routines are created.)

## Egress caveat (test on first run)

Cloud sandboxes may restrict outbound network. On the first cloud run, confirm
`quotes.py` can reach `query1.finance.yahoo.com`. If it's blocked, swap the
price source to FMP / Finnhub / Alpaca (docs already in `raw/`) — a contained
change to `quotes.py`, not a redesign.

## Cutover

Run cloud + local in parallel for a few days. Once cloud runs are reliably
producing briefs + Telegram messages, disable the local scheduled tasks
(`update_scheduled_task enabled=false`) but keep them as manual backups.

## Decisions (2026-06-15)

- Routines will be created by **Claude via the `RemoteTrigger` API** once the
  user provides the `environment_id` (not hand-built in the web UI).
- **Disable the local scheduled tasks once the cloud routines are confirmed
  live** (not run in parallel long-term).

## When the user provides `environment_id`, Claude does:

1. Create 3 triggers via `RemoteTrigger create` with
   `job_config.ccr.environment_id = <id>`, the crons above, and the routine
   prompts (reuse the local `~/.claude/scheduled-tasks/*/SKILL.md` text).
2. `RemoteTrigger run` the morning one once to smoke-test: confirm it clones
   the repo, reads market data (Yahoo egress!), pushes state, and sends the
   Telegram message.
3. If the smoke test is clean, disable the 3 local tasks
   (`update_scheduled_task enabled=false`).

## Live cloud routines (created 2026-06-15)

Environment: `env_01L8JC8YFuFWLeKGSQGT7pzi` ("Default" cloud env, repo
`moodysamkary/trading-agent`, Network access = Trusted, model claude-opus-4-8,
env vars `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` set). Cron is stored in
**UTC** (the web UI converts local→UTC; CT is UTC−5 in summer).

| Routine | Trigger ID | Cron (UTC) | = Central |
|---|---|---|---|
| trader-morning-brief (UI-created) | `trig_01QjzGHYUeQBABPnz5cRw8Le` | `45 12 * * 1-5` | 7:45 AM weekdays |
| trader-close-report | `trig_01GLgtmwM1SEZoVdhBzmVaiF` | `10 20 * * 1-5` | 3:10 PM weekdays |
| trader-weekly-review | `trig_019imt5erRS7CsaQBzrGzRXf` | `0 21 * * 5` | 4:00 PM Friday |

Create-body shape that works (via `RemoteTrigger create`): `name`,
`cron_expression`, `enabled`, `notifications.channel`, and
`job_config.ccr.{environment_id, events:[{data:{type:"user",
message:{role:"user", content:<prompt>}}}], session_context:{allowed_tools,
model, sources:[{git_repository:{url}}]}}`.

`sync.sh` pushes `HEAD:main` (not `main`) so it persists state from the cloud
sandbox's `claude/*` work branch — fixed 2026-06-15.

## ✅ R2 COMPLETE (2026-06-15)

Cloud routines are live and fully verified; **local scheduled tasks disabled**.
Resolution of the egress blocker: set the env's **Network access → Full**
(options were None / Trusted / Full / Custom; Custom has known allowlist
enforcement bugs, so Full is the reliable choice for this personal env). With
Full egress, **Yahoo serves the datacenter IP** — live prices AND candles work,
no API key needed. Telegram (`api.telegram.org`) also reachable → notifications
confirmed arriving. The Finnhub support in `quotes.py` stays as a dormant
fallback (no-op unless `FINNHUB_API_KEY` is set).

Verified end-to-end: clone → pull → Yahoo live prices → `portfolio.py status`
official numbers → push state to `main` → Telegram message delivered.

Leftover: probe trigger `trig_01Neqetwqgf…` (DISABLED, fake env, never runs) —
delete from claude.ai/code/routines if desired.

## Smoke test history (2026-06-15 close-report cloud runs)

✅ Clone, `sync.sh push HEAD:main` (state persisted to main), WebSearch, and
graceful degradation per AGENT.md honesty rules all worked.
❌ **Outbound egress blocked.** `quotes.py`→Yahoo returned 403, and so did a
plain `google.com` curl → the "Trusted" network level blocks general internet
(only github/Anthropic-routed WebSearch reachable). `portfolio.py status`
could not run; `api.telegram.org` almost certainly blocked too (Telegram
notify likely failed in the cloud).

### Remaining work to finish R2

1. **Widen the env's Network access** (env settings → Network access): allow
   the price-API host + `api.telegram.org`, or set fully open. Note: known
   enforcement bugs with custom additional-domain allowlists — "all domains"
   is the most reliable.
2. **Likely swap `quotes.py` off Yahoo.** Yahoo 403s datacenter IPs even when
   egress is allowed. Move to a keyed, datacenter-friendly API (Finnhub or FMP
   free tier — docs in `raw/`); store the key as an env var on the cloud env.
3. Re-run the close-report cloud test; confirm `quotes.py` returns a price and
   Telegram arrives. Only then disable the local scheduled tasks.

**Local scheduled tasks remain the reliable path and stay ENABLED** until the
cloud data feed is fixed. Probe `trig_01Neqetwqgf…` left disabled.
