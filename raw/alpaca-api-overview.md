# Alpaca APIs — Overview

**Source URL**: https://docs.alpaca.markets/docs/
**Publisher**: Alpaca Markets
**Retrieved**: 2026-04-23
**License / use**: Public API documentation. For wiki ingest into `reference/data-sources.md`, cite specific endpoints from deeper docs when implementation decisions are made.

---

## Data coverage

Alpaca supports **stocks, options, and cryptocurrency** across multiple API products.

## API product lines

### Trading API
- Equities and crypto spot trading for individuals and businesses
- Real-time account management, orders, positions, assets
- Paper trading available
- Options trading with Level 3 support
- Crypto spot trading with dedicated order types

### Market Data API
- Historical and real-time pricing
- "up to 6+ years worth of historical data for stocks and crypto"
- WebSocket streaming for real-time quotes
- Historical bars, trades, and news data

### Broker API
- White-label solutions for building trading platforms
- Customer account opening/management
- Funding and ACH capabilities
- Crypto wallets and trading

### Connect API
- OAuth2 integration enabling third-party app connections

## Relevance to this project

Alpaca's Market Data API and paper-trading account are a natural fit for the research agent:

- **No live trades** (we're research-only). Paper account simulates executions.
- Market Data API is the primary use — historical bars and real-time quotes.
- Python SDK exists (referenced in docs footer); simplifies integration.
- News data endpoint is available.

## Gaps in this overview

The landing page doesn't specify:
- Exact free-tier rate limits (need to access individual endpoint docs)
- Exact historical data horizon per subscription tier
- Authentication token management specifics

**Next step during P2 planning**: Fetch `docs.alpaca.markets/docs/getting-started` and `docs.alpaca.markets/docs/historical-api` for specifics.
