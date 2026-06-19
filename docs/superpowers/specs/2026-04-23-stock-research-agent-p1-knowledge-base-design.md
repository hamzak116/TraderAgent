# P1: Trading Research Knowledge Base — Design Spec

**Date**: 2026-04-23
**Author**: Claude (brainstorm with user)
**Status**: Draft for user review

---

## 1. Context & purpose

This is **Phase 1 of a larger project**: a research-only stock trading agent that runs on a schedule, produces buy/sell recommendations with position sizing, tracks a simulated portfolio, and notifies the user over Telegram/WhatsApp/Dispatch. The agent **does not execute trades**. The user acts on recommendations manually.

**Test case context** that shapes the agent's eventual behavior:
- Budget: $1,000
- Horizon: 2 weeks
- Target: ≥20% gain, at minimum beat the S&P 500 over the window
- Must generalize to arbitrary (budget, horizon, target) triples in future runs

Phase 1 — scope of **this** spec — produces **none of the agent**. It produces the knowledge base the agent will later read to be an "expert." The current repo is an LLM Wiki (per `CLAUDE.md`), structured for exactly this: user drops sources into `raw/`, Claude ingests them into interlinked pages in `wiki/`.

### Why a knowledge base first

The alternative — have Claude freestyle trading advice from general pretraining — is exactly what produces confident-sounding-but-mediocre recommendations. The knowledge base gives the agent:

- A **stable methodology** it applies consistently run-over-run, not a new approach each time.
- **Citable provenance** for every claim in the agent's output reports (traceable to `raw/`).
- A **decision framework** for mapping `(budget, horizon, target)` → strategy mix → specific stock-selection criteria.
- An artifact the user can **audit and correct** between runs, closing the loop.

### Full project roadmap (for context; not this spec's scope)

| Phase | Deliverable |
|---|---|
| **P1 (this spec)** | Wiki populated with multi-strategy trading methodology, ~26 pages, MVP milestone at ~8 pages |
| P2 | Research agent MVP — manual invocation, reads wiki + live market data, outputs daily markdown research report |
| P3 | Portfolio state tracker — positions, cost basis, P&L, rotation triggers |
| P4 | Scheduled execution (pre-market + post-market) + notification layer (Telegram/WhatsApp/Dispatch) |

Each later phase gets its own spec cycle.

---

## 2. Scope

### In scope

1. A fully-populated `wiki/` directory organized into `strategy-schools/`, `concepts/`, `meta/`, and `reference/` subdirectories (~26 pages).
2. All pages follow the format defined in `CLAUDE.md`: title, summary, sources, last-updated, body, related pages, `[[wiki-links]]` throughout.
3. `wiki/index.md` as the navigable entry point.
4. `wiki/log.md` as the append-only operations record.
5. A curated source shortlist embedded in this spec that the user can act on to populate `raw/`.
6. An explicit MVP milestone (P1a) that unlocks P2 before full P1b completion.

### Out of scope

- Any code, agent, scheduler, notification layer, portfolio tracker, market data integration.
- Execution of trades — **the system never trades**, only recommends.
- Options, futures, crypto, forex. **Equities long-only.** (User requirement.)
- Sector-specific deep dives (healthcare, energy, etc.) — general methodology only in P1.
- Backtesting infrastructure.
- Tax strategy pages.
- Anything requiring sources not on the curated shortlist (expand later).

---

## 3. Wiki structure

```
wiki/
├── index.md                              # TOC with 1-line descriptions per page
├── log.md                                # Append-only ingest log
│
├── strategy-schools/                     # Major research traditions
│   ├── value-investing.md                # Graham → Buffett → Damodaran lineage
│   ├── growth-investing.md               # Fisher, O'Neil (CAN SLIM)
│   ├── momentum-and-swing-trading.md     # Minervini SEPA/VCP, O'Neil swing
│   ├── technical-analysis.md             # Edwards/Magee, Murphy, chart patterns
│   ├── quant-factors.md                  # Fama-French, AQR (value/mom/quality/low-vol/size)
│   └── macro-and-regime.md               # Dalio economic machine, business cycle
│
├── concepts/                             # Cross-cutting, apply across strategies
│   ├── risk-management.md                # Max drawdown, stops, VaR basics
│   ├── position-sizing.md                # Kelly, fixed-fractional, Van Tharp R-multiples
│   ├── portfolio-construction.md         # Diversification, correlation, concentration
│   ├── valuation-methods.md              # DCF, multiples, relative valuation
│   ├── technical-indicators.md           # MACD, RSI, MAs, volume, Bollinger
│   ├── financial-statements.md           # Income/BS/CF primer, red flags
│   ├── earnings-and-catalysts.md         # Earnings plays, guidance, events, analyst actions
│   ├── news-and-sentiment.md             # Processing news flow, sentiment indicators
│   ├── selling-and-rotation.md           # Exit rules, when to cut, when to rotate
│   └── behavioral-finance.md             # Biases, pitfalls, discipline
│
├── meta/                                 # The agent's decision framework
│   ├── strategy-selection.md             # (budget, horizon, target) → strategy mix
│   ├── risk-tolerance-mapping.md         # Target % → implied risk tier → constraints
│   └── research-workflow.md              # Step-by-step daily research procedure
│
└── reference/
    ├── data-sources.md                   # APIs, feeds, when to use which
    ├── key-metrics-glossary.md           # P/E, ROE, FCF, EV/EBITDA, beta, ATR, etc.
    ├── traders-and-thinkers.md           # Short bios: Graham, Buffett, O'Neil, Minervini, Damodaran, Dalio, Asness, Marks
    └── market-structure.md               # Order types, liquidity, execution basics
```

**Total: 26 pages** (24 content pages + `index.md` + `log.md`).

---

## 4. MVP milestone — P1a vs P1b

**P1a (MVP, 8 content pages + index + log):** Sufficient for a swing-trading agent to run the 2-week test case. Enables starting P2 in parallel with P1b.

- `meta/strategy-selection.md`
- `meta/risk-tolerance-mapping.md`
- `meta/research-workflow.md`
- `concepts/risk-management.md`
- `concepts/position-sizing.md`
- `concepts/selling-and-rotation.md`
- `strategy-schools/momentum-and-swing-trading.md`
- `reference/data-sources.md`
- *(plus `index.md` + `log.md` scaffolding)*

**P1b (remaining ~18 pages):** Fills out the true multi-strategy framework. Required before the "accept any timeframe" capability is real.

- All other pages under `strategy-schools/`, `concepts/`, `reference/`.

P1a done ≠ P1 done. P2 may start once P1a is done, but both P1b and P2 continue.

---

## 5. Page-by-page content spec

Every page follows `CLAUDE.md` format exactly: H1 title, **Summary**, **Sources**, **Last updated**, `---`, body, `## Related pages`. Every factual claim has `(source: filename)` citation or is flagged `[needs verification]`.

### 5.1 `strategy-schools/`

**`value-investing.md`** — Graham's margin of safety, intrinsic value, Mr. Market; Buffett's evolution to quality-at-fair-price; Damodaran's valuation discipline. When the approach works (long horizons, patient capital, out-of-favor names) and when it fails (growth regimes, momentum-dominated markets). Typical holding periods: years. Compatibility with 2-week test: **low** — include but flag as low-weight for short horizons.

**`growth-investing.md`** — Fisher's scuttlebutt, O'Neil's CAN SLIM (Current earnings ≥25%, Annual earnings, New product, Supply/demand, Leader, Institutional, Market direction). Earnings acceleration focus. Overlap with momentum (below).

**`momentum-and-swing-trading.md`** ⭐ (P1a) — Minervini SEPA (Specific Entry Point Analysis): trend template (price above 150/200-day MA, MAs stacked correctly), VCP (Volatility Contraction Pattern — successive shallower pullbacks, ≤25% → ≤15% → ≤8%, declining volume), relative strength ≥70-80, fundamental fuel (EPS growth accelerating). Stage analysis (Weinstein/Minervini stages 1–4). Pivot points, pocket pivots. Typical holds: 2–10 weeks. **High relevance to 2-week test case.**

**`technical-analysis.md`** — Dow theory; chart patterns (cup-and-handle, flat base, double bottom, head-and-shoulders); support/resistance; trend identification; volume confirmation. Note: TA-as-sole-signal is weak; TA as timing overlay on fundamentally-screened candidates is strong.

**`quant-factors.md`** — The canonical factors: value (HML), size (SMB), momentum (MOM/UMD), quality (QMJ), low-volatility, profitability, investment. Fama-French 3/5-factor, Carhart 4-factor. AQR's integrated value-momentum-quality thesis (complementary, negatively-correlated payoff timing). Multi-factor beats single-factor. Cost of implementation (turnover) matters.

**`macro-and-regime.md`** — Dalio's "economic machine": productivity growth + short-term debt cycle (~5–10yr) + long-term debt cycle (~50–75yr). Rate regimes (rising/falling). Risk-on vs risk-off. Sector rotation through cycle (early cycle: consumer discretionary/tech; late cycle: staples/energy/utilities). Recession indicators (yield curve, LEI, credit spreads).

### 5.2 `concepts/`

**`risk-management.md`** ⭐ (P1a) — "Avoid large losses" as the prime directive. Position-level stops (% or ATR-based). Portfolio-level max drawdown tolerance. The math of loss recovery (50% loss requires 100% gain). Kelly-fraction upper bound on any single bet. Stop-loss placement: technical (below support / prior swing low) vs volatility (1.5–2× ATR). **This page drives every sell decision the agent will make.**

**`position-sizing.md`** ⭐ (P1a) — Fixed-fractional (bet X% of portfolio per position). Kelly criterion (optimal f given edge and odds) and why half-Kelly is used in practice. Van Tharp's R-multiples: define risk-per-trade (R) as the distance from entry to stop × shares, size so R = 1–2% of portfolio. Worked examples using $1,000 budget. Pyramiding rules.

**`portfolio-construction.md`** — Diversification vs concentration tradeoff. Correlation (sector, factor, beta). Rebalancing. For small accounts (~$1k), position count tradeoffs (3–5 concentrated vs 10–15 diversified; commissions now $0, so concentration decision is purely risk-driven).

**`valuation-methods.md`** — DCF mechanics (FCF projection, terminal value, WACC). Relative valuation (P/E, EV/EBITDA, P/B, P/S vs peers). When each applies. Damodaran's critique of precision theater in DCF — model transparency > output precision.

**`technical-indicators.md`** — Moving averages (SMA, EMA, stacking); MACD; RSI (overbought/oversold thresholds, divergence); Bollinger Bands; ATR; volume analysis (accumulation/distribution, OBV). What each measures, typical use, known failure modes.

**`financial-statements.md`** — Income statement (revenue, margins, EPS, quality of earnings — recurring vs one-time); balance sheet (asset quality, leverage, working capital); cash flow (OCF > net income = healthy; high CapEx intensity = low FCF). Red flags: receivables growing faster than revenue; inventory buildup; rising share count without revenue growth.

**`earnings-and-catalysts.md`** — Earnings report structure (beat/miss, guidance, call transcript). Typical post-earnings drift. Catalyst calendar items: earnings, guidance updates, analyst days, FDA/regulatory, product launches, macro data (FOMC, CPI, NFP). Pre-announce / post-announce trade setups.

**`news-and-sentiment.md`** — How to process news flow without overreacting. Primary sources vs aggregators. Sentiment indicators (VIX, AAII survey, put/call ratio, fund flows). Social sentiment (cautious use). Analyst action types (initiation, upgrade/downgrade, price target) and their typical market impact.

**`selling-and-rotation.md`** ⭐ (P1a) — The discipline most individual investors lack. Sell triggers: stop-loss hit, thesis invalidation (fundamental change), better opportunity (positive rotation), technical breakdown, time-stop (position not performing after X bars), target reached. Tax considerations (short-term vs long-term capital gains — out of scope for P1 but flag). Rotation logic: raise cash only, or replace immediately.

**`behavioral-finance.md`** — Loss aversion, sunk cost, confirmation bias, anchoring, recency bias, overconfidence, FOMO. Specific manifestations in trading: holding losers too long, selling winners too early, overtrading, revenge trading. The agent's job: serve as a consistent, bias-free checklist.

### 5.3 `meta/` — the decision framework

**`strategy-selection.md`** ⭐ (P1a) — **This is the page that makes the multi-strategy framework real.** A decision matrix:

| Horizon | Target return | Primary strategy | Secondary overlay |
|---|---|---|---|
| Days – 2 weeks | Aggressive (>10%) | Momentum/swing (SEPA/VCP) | Earnings catalyst, technical breakout |
| Weeks – months | Moderate (5–15%) | Growth (CAN SLIM) | Quality factor filter |
| Months – year | Market-beat (5–15% p.a.) | Multi-factor quant (VMQ) | Macro/regime awareness |
| 1+ year | Compound | Value + quality | Contrarian overlay |

Plus: how `budget` affects strategy (tiny budgets → concentration forced; commissions zero so no cost floor, but liquidity matters for cheap stocks). How `target` translates to required risk tier. Explicit warning text: "A 20%-in-2-weeks target implies high-risk concentrated momentum plays; expected variance is very high and probability of hitting target on any single run is modest. Long-run edge comes from process discipline, not individual-run outcome."

**`risk-tolerance-mapping.md`** ⭐ (P1a) — Four risk tiers with explicit constraints:

| Tier | Max position size | Stop distance | Max drawdown tolerance | Diversification |
|---|---|---|---|---|
| Conservative | 10% | 8% | 10% | ≥10 positions |
| Moderate | 20% | 10% | 15% | 6–10 positions |
| Aggressive | 33% | 12% | 25% | 3–5 positions |
| Speculative | 50% | 15% | 40% | 2–3 positions |

Target-to-tier mapping: <5% (conservative) / 5–15% (moderate) / 15–30% (aggressive) / >30% (speculative, with explicit risk disclaimer).

**`research-workflow.md`** ⭐ (P1a) — The procedure the agent follows each run:

1. **Context load** — read user config (budget, horizon, target), current portfolio state, prior run's theses
2. **Regime scan** — check macro indicators (SPY trend, VIX, yield curve, sector breadth) → bull/bear/sideways classification
3. **Strategy select** — given target + horizon + regime, select primary strategy from `strategy-selection.md`
4. **Universe filter** — screen for liquidity (avg volume, market cap floor), exclude penny stocks / low-float
5. **Candidate generation** — apply strategy-specific screens (e.g. SEPA trend template for momentum)
6. **Deep research per candidate** — fundamentals, technicals, catalysts, news/sentiment, each cited
7. **Thesis construction** — one page per candidate: why buy, at what price, expected target, stop, R-multiple, confidence
8. **Rank & select** — score candidates, choose top N given position-sizing rules
9. **Portfolio impact** — for existing holdings: reconfirm thesis or flag for sell/rotate; for new candidates: fit into available cash
10. **Report output** — structured markdown with buys, sells, holds, position sizes, rationale, risk notes, citations
11. **Log append** — record to wiki log

### 5.4 `reference/`

**`data-sources.md`** ⭐ (P1a) — API comparison and recommendation table (see Section 6 for sources used to populate this page). Recommended stack for P2:
- **Prices/intraday**: Alpaca (free, generous limits) or Polygon (paid, low-latency)
- **Fundamentals**: Financial Modeling Prep (FMP) or Tiingo
- **Filings**: SEC EDGAR (free, authoritative)
- **News/sentiment**: Finnhub (free tier) or NewsAPI
- **Macro**: FRED (St. Louis Fed — free)
- **Analyst data**: FMP or paid (Refinitiv/Bloomberg out of scope)

**`key-metrics-glossary.md`** — ~40 entries: P/E, PEG, P/B, P/S, EV/EBITDA, ROE, ROIC, FCF yield, operating margin, net margin, debt/equity, current ratio, EPS growth, revenue growth, beta, ATR, relative strength, IBD RS rating, short interest, float, avg volume, market cap tiers, etc.

**`traders-and-thinkers.md`** — ~1-paragraph bios with core ideas and key writings for: Benjamin Graham, Warren Buffett, Charlie Munger, Philip Fisher, William O'Neil, Mark Minervini, Jesse Livermore, Aswath Damodaran, Ray Dalio, Cliff Asness (AQR), Howard Marks, Seth Klarman, Peter Lynch, Stan Weinstein, Van Tharp, James O'Shaughnessy, Daniel Kahneman, James Montier.

**`market-structure.md`** — Exchanges (NYSE/NASDAQ); order types (market, limit, stop, stop-limit); liquidity (bid-ask spread, market impact for small vs large orders); trading hours (pre-market/regular/after-hours); circuit breakers; settlement (T+1); PDT rule (applies to margin accounts <$25k — flag as relevant to $1k test case).

---

## 6. Curated source shortlist

The user should download/bookmark these and drop copies (or links) into `raw/`. Claude will ingest from `raw/` into the wiki pages listed.

### Free web / open-access (recommend starting here)

| # | Source | Format | Feeds pages |
|---|---|---|---|
| 1 | [Damodaran Online — homepage](https://pages.stern.nyu.edu/~adamodar/) | Website + PDFs | `value-investing`, `valuation-methods`, `financial-statements`, `key-metrics-glossary`, `traders-and-thinkers` |
| 2 | [Damodaran — Free Valuation Online Class (25 webcasts)](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/webcastvalonline.htm) | Video + slides | Same as #1 |
| 3 | [Damodaran — Investment Philosophies (free online class)](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/webcastinvphil.htm) | Video + slides | `strategy-selection`, `value-investing`, `quant-factors` |
| 4 | [Ray Dalio — "How the Economic Machine Works" PDF](https://www.economicprinciples.org/downloads/ray_dalio__how_the_economic_machine_works__leveragings_and_deleveragings.pdf) | PDF | `macro-and-regime` |
| 5 | [Ray Dalio — Economic Principles site / 30-min animation](https://economicprinciples.org/) | Video + docs | `macro-and-regime` |
| 6 | [Kenneth French Data Library (Fama-French factors)](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html) | Data + descriptions | `quant-factors` |
| 7 | [Kenneth French — Factor descriptions](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_factors.html) | Web page | `quant-factors` |
| 8 | [AQR Research Library](https://www.aqr.com/Insights/Research) | Papers | `quant-factors`, `momentum-and-swing-trading`, `portfolio-construction` |
| 9 | [AQR — "20 for Twenty" paper collection](https://www.aqr.com/Insights/Research/Book/20-for-Twenty) | PDF book | `quant-factors` |
| 10 | [Alpha Architect — Momentum research archive](https://alphaarchitect.com/category/architect-academic-insights/factor-investing/momentum-investing/) | Blog + papers | `quant-factors`, `momentum-and-swing-trading` |
| 11 | [Alpha Architect — Quantitative Momentum Philosophy (free PDF)](https://alphaarchitect.com/wp-content/uploads/2021/08/The_Quantitative_Momentum_Investing_Philosophy.pdf) | PDF | `quant-factors`, `momentum-and-swing-trading` |
| 12 | [Research Affiliates — Value/Quality/Momentum integration](https://www.researchaffiliates.com/publications/articles/1110-why-value-quality-and-momentum-belong-together) | Article | `quant-factors`, `strategy-selection` |
| 13 | [StockCharts ChartSchool — Technical Analysis](https://chartschool.stockcharts.com/table-of-contents/overview/technical-analysis) | Free course | `technical-analysis`, `technical-indicators` |
| 14 | [StockCharts ChartSchool — Chart Analysis](https://chartschool.stockcharts.com/table-of-contents/chart-analysis) | Free course | `technical-analysis` |
| 15 | [Berkshire Hathaway — Buffett shareholder letters (1977–present)](https://www.berkshirehathaway.com/letters/letters.html) | PDFs | `value-investing`, `behavioral-finance`, `traders-and-thinkers` |
| 16 | [Howard Marks — Oaktree memos](https://www.oaktreecapital.com/insights/memos) | PDFs | `behavioral-finance`, `risk-management`, `market-regime` |
| 17 | [CFA Institute Research Foundation — free books](https://rpc.cfainstitute.org/research/foundation/publications) | PDFs | `portfolio-construction`, `valuation-methods`, `quant-factors` |
| 18 | [SEC EDGAR — company filings](https://www.sec.gov/edgar) | Filings | `financial-statements`, `earnings-and-catalysts` |
| 19 | [SEC Investor.gov — retail investor education](https://www.investor.gov/) | Reference | `market-structure`, `risk-management` |
| 20 | [FRED (St. Louis Fed)](https://fred.stlouisfed.org/) | Macro data | `macro-and-regime`, `data-sources` |
| 21 | [Investopedia](https://www.investopedia.com/) | Reference | `key-metrics-glossary`, most concept pages (supplementary) |
| 22 | [Corporate Finance Institute — CAN SLIM overview](https://corporatefinanceinstitute.com/resources/equities/can-slim/) | Article | `growth-investing` |
| 23 | [Wikipedia — CAN SLIM](https://en.wikipedia.org/wiki/CAN_SLIM) | Article | `growth-investing` |
| 24 | [Macro Ops — O'Neil CAN SLIM deep explainer](https://macro-ops.com/william-oneils-can-slim-trading-strategy-explained/) | Article | `growth-investing`, `momentum-and-swing-trading` |
| 25 | [finermarketpoints — Minervini SEPA/VCP full guide](https://www.finermarketpoints.com/post/what-is-mark-minervini-s-trading-strategy-the-complete-sepa-vcp-guide) | Article | `momentum-and-swing-trading` |
| 26 | [QuantStrategy.io — SEPA explainer](https://quantstrategy.io/blog/sepa-strategy-explained-mastering-trend-following-with-mark/) | Article | `momentum-and-swing-trading` |
| 27 | [Alpaca Markets — free market data API docs](https://alpaca.markets/docs/) | Docs | `data-sources` |
| 28 | [Polygon.io — market data API docs](https://polygon.io/docs) | Docs | `data-sources` |
| 29 | [Financial Modeling Prep — fundamentals API](https://site.financialmodelingprep.com/) | Docs | `data-sources` |
| 30 | [Finnhub — news + quotes API](https://finnhub.io/docs/api) | Docs | `data-sources` |

### Paid / book sources (recommend but optional)

These aren't freely available but are canonical enough that depth suffers without them. Add to `raw/` only if you acquire legitimate copies.

| # | Book | Feeds pages |
|---|---|---|
| B1 | *The Intelligent Investor* — Graham | `value-investing`, `behavioral-finance` |
| B2 | *Security Analysis* — Graham & Dodd | `value-investing`, `financial-statements` |
| B3 | *Common Stocks and Uncommon Profits* — Fisher | `growth-investing` |
| B4 | *How to Make Money in Stocks* — O'Neil | `growth-investing`, `momentum-and-swing-trading` |
| B5 | *Trade Like a Stock Market Wizard* — Minervini | `momentum-and-swing-trading` |
| B6 | *Technical Analysis of Stock Trends* — Edwards & Magee | `technical-analysis` |
| B7 | *Trading for a Living* — Elder | `technical-analysis`, `behavioral-finance` |
| B8 | *Damodaran on Valuation* — Damodaran | `valuation-methods` |
| B9 | *Reminiscences of a Stock Operator* — Lefèvre (Livermore) | `traders-and-thinkers`, `behavioral-finance` |
| B10 | *The Most Important Thing* — Howard Marks | `risk-management`, `behavioral-finance` |
| B11 | *Thinking, Fast and Slow* — Kahneman | `behavioral-finance` |
| B12 | *Expected Returns* — Antti Ilmanen | `quant-factors`, `portfolio-construction` |
| B13 | *Quantitative Momentum* — Gray & Vogel | `quant-factors`, `momentum-and-swing-trading` |
| B14 | *Principles* — Dalio | `macro-and-regime`, `behavioral-finance` |

**Workflow:** User adds available sources to `raw/` progressively. Claude ingests whatever's there and flags any page where coverage is thin pending additional sources.

---

## 7. Done criteria

### P1a (MVP) is done when:

1. All 8 listed P1a pages exist in `wiki/` with populated content, proper format per `CLAUDE.md`, and citations where claims are factual.
2. `wiki/index.md` exists and lists all P1a pages with 1-line descriptions.
3. `wiki/log.md` exists with an entry for each ingest operation.
4. At least sources #1, #4, #13, #15, #25, and #27 from Section 6 have been ingested and cited in the relevant pages. (User drops PDFs/downloads into `raw/`, OR saves a plain-text list of URLs into `raw/sources.md` that Claude re-fetches at ingest time. Either is fine; trade-off is offline-availability vs freshness.)
5. Each P1a page has ≥3 outgoing `[[wiki-links]]` to related pages (even if target doesn't exist yet — P1b fills in).
6. `meta/strategy-selection.md` has a concrete decision matrix the agent could read programmatically.

### P1b (Full) is done when:

1. All 24 content pages exist with populated content per above format.
2. Orphan check: no page has zero inbound links except `index.md` / `log.md`.
3. Concept-coverage check: every concept mentioned in any page either has its own page or is defined in `key-metrics-glossary.md`.
4. All Section 6 sources #1–#30 have been attempted for ingest. Sources that are paywalled or otherwise inaccessible are noted explicitly in `log.md`. User is prompted to supply books from the B-list based on which pages are weakest.
5. `wiki/index.md` lists all 24 pages with descriptions.
6. Contradiction check (Claude reviews all pages): any contradictions between pages are explicitly called out rather than silently glossed over.

---

## 8. Non-goals (reiterated)

- **No code.** No Python, no agent implementation, no scheduler, no notification layer. All of that is P2–P4.
- **No trades.** Ever. This is a research-only system.
- **No claims of market-beating edge.** The wiki documents methodology; it makes no performance promises. All statements about expected returns are explicitly framed as probability distributions with wide variance.
- **No options, futures, crypto.** Equities long-only.

---

## 9. Risks & open questions

### R1 — Source paywalls for canonical material

Much gold-standard content is in paid books. The curated web shortlist is strong but has gaps (Minervini's specific numeric thresholds, O'Neil's exact CAN SLIM thresholds beyond Wikipedia-level). **Mitigation:** flag these gaps explicitly in pages; recommend the user acquire B-list books progressively. Don't pretend we have full coverage when we don't.

### R2 — 20%-in-2-weeks target realism

The target is ~520% annualized. No methodology consistently delivers this. The agent's output must include **explicit expected-value and drawdown framing**, not just "buy these stocks." **Mitigation:** `meta/risk-tolerance-mapping.md` will contain prominent warning language for aggressive/speculative tier targets. The agent will never present a recommendation as high-confidence when the target requires speculative-tier risk.

### R3 — Recency / data staleness in web sources

Factor returns, sector rotations, valuation multiples, and macro regime change over time. Pages that cite specific historical numbers risk becoming outdated. **Mitigation:** Every page's `**Last updated**:` field is a real date. Lint pass in P1b flags pages with stale-looking specifics (e.g., "as of 2019…") for refresh.

### R4 — User's "no options" but 2-week/20% target may be inconsistent

Short-horizon aggressive targets traditionally use options for asymmetric payoffs. No-options constrains the agent to momentum/catalyst plays only. **Mitigation:** acknowledge in `strategy-selection.md` that no-options + 2-week + 20% = concentrated momentum/breakout plays only, with elevated single-stock risk.

### R5 — Wiki → agent integration not yet designed

P1 produces content. P2 designs how the agent reads it. There's risk that P2 will need wiki structure changes. **Mitigation:** Section 5.3 specifies `meta/research-workflow.md` and `meta/strategy-selection.md` as machine-readable-friendly (explicit decision matrix, stepwise procedure), so the agent can directly consume them. P2 spec will revisit if format tweaks are needed.

### OQ1 — Telegram/WhatsApp/Dispatch notification channel

User mentioned Anthropic "recently released" a Telegram/WhatsApp integration. I'm not confident this exists as a first-party feature. This is a **P4 question**, not P1. Defer to P4 spec — by then we can verify current state.

### OQ2 — Agent hosting platform (local vs Claude managed agents vs Claude Code scheduled tasks)

User mentioned "locally or hosted using claude managed agents." Claude Code's scheduled-tasks MCP (`mcp__scheduled-tasks__create_scheduled_task`) is confirmed available. "Claude managed agents" may refer to a different Anthropic product. **Defer to P4 spec** — by then we've built P2 and will know what the execution environment needs.

---

## 10. Handoff plan

**Next step after this spec is approved:**

1. Invoke the `superpowers:writing-plans` skill to produce an executable implementation plan for P1.
2. Plan will break P1a and P1b into specific ingest tasks keyed to sources in Section 6.
3. User adds sources to `raw/` progressively. Each ingest session produces:
   - Updates to 1–N wiki pages
   - An `wiki/log.md` entry
   - An `wiki/index.md` update
4. P1a completion triggers optional start of P2 (research agent MVP) in parallel with P1b.

---

## 11. Approval

Pending user review. If approved, transition to `writing-plans`.
