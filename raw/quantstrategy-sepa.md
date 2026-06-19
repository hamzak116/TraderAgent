# QuantStrategy.io — SEPA Strategy Explained

**Source URL**: https://quantstrategy.io/blog/sepa-strategy-explained-mastering-trend-following-with-mark/
**Publisher**: QuantStrategy.io
**Retrieved**: 2026-04-23
**License / use**: Publicly accessible article.

---

## Trend template quantitative thresholds

### Moving average criteria
- Stock price above 150-day and 200-day MAs
- 150-day MA above 200-day MA
- 200-day MA trending upward for minimum 1 month (ideally 4–5 months)
- 50-day MA above both 150 and 200-day MAs
- Current price above 50-day MA

### Valuation / performance filters
- **At least 30% above 52-week low** (avoids depressed stocks)
- **Within 25% of 52-week high**
- Relative Strength ranking ≥ 70 (outperforms 70% of market)
- Quarterly EPS increased Q/Q
- Annual EPS increased Y/Y

## Volatility Contraction Pattern (VCP) — specific numbers

Multi-stage consolidation where volatility progressively tightens:

- **Contraction 1**: 20–30% pullback
- **Contraction 2**: 10–15% pullback
- **Contractions 3–4**: 5–8% pullbacks on declining volume

Entry trigger: "**one cent above**" the final pivot point with volume confirmation (ideally **300%+ of average**).

## Risk management rules

- **7–8% maximum stop loss** below entry — non-negotiable
- Permits surviving "**10 consecutive losses**" while preserving capital

## Exit strategies

1. **Profit-taking trailing stop** after 20% gain (move stop to breakeven)
2. **Parabolic exhaustion selling** during vertical spikes with volume divergence
3. **Moving average breaks** (10-day or 21-day EMA) on distribution volume

## What this source does NOT provide

- Backtesting results
- Historical performance metrics
- Win rates
- Portfolio-level allocation rules

## Cross-reference

This source complements `minervini-sepa-vcp.md` (finermarketpoints). The two together cover the SEPA methodology reasonably well for the `momentum-and-swing-trading.md` wiki page. Any deeper detail (win rates, backtests, specific examples) requires Minervini's book B5 (*Trade Like a Stock Market Wizard*).
