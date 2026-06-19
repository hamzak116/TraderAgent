# Setup — your personal trading agent

This is a clean copy of the trading-agent template: the engine, scripts,
slash-command skills, and methodology sources (`raw/`) are intact, but all
portfolio data, journals, lessons, and dashboards from the original owner
have been removed.

## 1. Put it on your own GitHub

```bash
cd trading-agent
git init
git add -A
git commit -m "Initial commit: personal trading agent from template"
# create an EMPTY repo on github.com (no README), then:
git remote add origin https://github.com/hamzak116/<your-repo-name>.git
git branch -M main
git push -u origin main
```

## 2. Add your API keys (private — never committed)

Edit `trader/.env` (a copy of `.env.example`, already git-ignored):
- `FINNHUB_API_KEY` — required for live quotes
- `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` — optional, for phone alerts

## 3. Onboard

Open the repo in Claude Code and run **`/trader-onboard`**. It interviews you
(risk tier, goals, constraints, horizon) and creates `trader/profile.md` plus a
fresh paper portfolio seeded with your holdings. Then use `/trader-morning`,
`/trader-close` daily and `/trader-review` weekly.

Note: the template's original profile had a Shariah-compliance screen and a
tech/quantum/nuclear/space tilt — onboarding replaces those with *your*
answers, so you're not locked into the previous owner's constraints.
