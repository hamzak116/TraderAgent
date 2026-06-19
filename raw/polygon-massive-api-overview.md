# Polygon.io / Massive — API Overview

**Source URL**: https://massive.com/docs (redirected from polygon.io/docs — Polygon appears to have rebranded to Massive)
**Publisher**: Polygon.io / Massive
**Retrieved**: 2026-04-23
**License / use**: Public API documentation.

---

## Access methods

### REST API
"Request specific market data and analytics on demand" — historical records and ad-hoc queries integrated into applications.

### WebSocket API
Real-time streaming for live market updates — trading platforms, dashboards, monitoring tools.

### Flat Files
Bulk historical data downloads via CSV — designed for comprehensive analysis, backtesting, and machine learning.

## Supported asset classes

- Stocks
- Options
- Futures
- Indices
- Forex
- Cryptocurrency

## Gaps in this fetch

The landing page doesn't detail:
- Free vs paid tier specifics
- Rate limits per tier
- Authentication mechanism
- Exact historical data coverage per tier
- Python SDK status

**Known from prior web research**: Polygon's free tier is limited (delayed quotes, capped endpoints). It's optimized for low-latency and scale — tick-by-tick precision and WebSocket feeds. Paid tiers are more expensive than Alpaca's but offer institutional-quality data.

**For P2 / data-sources.md wiki page**: Fetch specific endpoint docs when choosing between Alpaca / Polygon / FMP for implementation.
