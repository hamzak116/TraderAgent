# Trading Agent

**Summary**: A research-only trading agent that suggests stock buys/sells daily, tracks every suggestion in a paper portfolio benchmarked against the S&P 500, and learns from graded outcomes. It never executes trades and has no access to money.

**Sources**: docs/superpowers/specs/2026-04-23-stock-research-agent-p1-knowledge-base-design.md, minervini-sepa-vcp.md, alpha-architect-quant-momentum.txt, dalio-economic-machine-transcript.md, howard-marks-memos-index.md

**Last updated**: 2026-06-09

---

## What it is

The agent implements phases P2–P4 of the project roadmap (source:
docs/superpowers/specs/2026-04-23-stock-research-agent-p1-knowledge-base-design.md):
a scheduled research agent with portfolio state tracking. It produces
recommendations only — the human decides whether to act. Whether or not the
human follows a suggestion, the paper portfolio simulates it, so the track
record is honest.

## Components

| Piece | Location | Purpose |
|---|---|---|
| Operating manual | `trader/AGENT.md` | Guardrails, routines, risk tiers, learning loop |
| Ledger scripts | `trader/scripts/portfolio.py`, `quotes.py` | Paper trades, live quotes, P&L vs SPY, call grading |
| User profile | `trader/profile.md` | Risk tier, goals, constraints from onboarding interview |
| Suggestion record | `trader/suggestions.json` | Every call with graded outcome (alpha vs SPY) |
| Lessons | `trader/lessons.md` | Distilled post-mortems; read before every morning run |
| Daily journal | `trader/journal/` | Morning briefs and close reports |

## Daily cycle

1. **Pre-open** (`/trader-morning`, scheduled weekdays before 9:30 ET) —
   regime scan, holdings review, sentiment/news research, 0–3 suggestions
   executed in the paper portfolio with thesis/stop/target/horizon.
2. **Post-close** (`/trader-close`, scheduled weekdays after 16:00 ET) —
   day P&L vs SPY, move explanations, stop/target flags.
3. **Weekly** (`/trader-review`) — grade closed calls, write falsifiable
   lessons, check calibration (hit rate, win/loss asymmetry,
   confidence-vs-outcome).

## Methodology

Drawn from the sources in `raw/`: Minervini SEPA/VCP momentum entries and exit
discipline (source: minervini-sepa-vcp.md), quantitative momentum screening
(source: alpha-architect-quant-momentum.txt), CAN SLIM growth criteria
(source: macroops-can-slim-deep-dive.md), Dalio regime framework (source:
dalio-economic-machine-transcript.md), and Marks-style risk honesty (source:
howard-marks-memos-index.md). The risk-tier table and 11-step research
workflow come from the design spec.

## Guardrails

- Never trades; no brokerage or money access, ever.
- Equities long-only; no options, futures, crypto, shorting.
- Every suggestion carries thesis, confidence, stop, target, horizon.
- Performance numbers only from the ledger scripts, never recalled from memory.
- Not financial advice; the human decides.

## Related pages

- [[index]]
