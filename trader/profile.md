# Trader Profile

**Summary**: Personal risk profile, goals, and constraints that every trading routine reads first. Set during onboarding.

**Last updated**: 2026-06-19

---

## Risk tier: Moderate

Reaction to a 15% drawdown with no news: **hold and reassess** — re-check the
thesis before acting, neither panic-sell nor average down blindly.

Implied limits (from AGENT.md risk-tier table):

| Limit | Value |
|---|---|
| Max position size | 20% of equity |
| Stop distance | ~10% |
| Max portfolio drawdown | 15% |
| Target position count | 6–10 holdings |
| Risk per trade | (entry − stop) × shares ≤ 1–2% of equity |

At the current $2,000 paper capital, a 20% max position is ~$400; expect to
hold roughly 5–10 names rather than a few concentrated bets.

## Goal

**Beat the S&P 500 over the long term** with a disciplined, repeatable edge.
Every call is benchmarked against SPY in the paper ledger; the scoreboard is
alpha vs SPY, not raw return.

## Horizon

**Mixed / flexible** — holding period varies by setup, from short swings (days)
to position trades (weeks to months). The thesis and stop define the exit, not
a fixed calendar.

## Experience level: Beginner

Reports should **explain terms and reasoning in plain language**. Spell out why
a setup qualifies, what the catalyst is, and what would invalidate the trade.
Favor clarity over jargon and density.

## Constraints

- **No religious-compliance (Shariah) screen** — standard methodology/risk
  screening only.
- **Sector tilt: none** — broad universe; follow the methodology wherever the
  edge is, no thematic preference.
- **No avoid-list** at this time.
- **Imported real-life holdings**: the user holds existing positions to be
  tracked (import details pending — added via `portfolio.py import`, then
  `rebase` to set the agent's baseline from the takeover date).

## Notes

- Goal (beat S&P) is achievable within the Moderate tier; it does **not**
  require speculative-tier risk, so no elevated-variance warning applies.
- Capital and constraints can be revised any time by re-running
  `/trader-onboard`.

## Related pages

- [[AGENT]] — operating manual and hard guardrails
