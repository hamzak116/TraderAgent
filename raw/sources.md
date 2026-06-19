# raw/ Sources — Tracking Index

**Last updated**: 2026-04-23
**Purpose**: Tracks what has been ingested into `raw/`, what failed, and what the user needs to acquire manually.
**Spec reference**: `docs/superpowers/specs/2026-04-23-stock-research-agent-p1-knowledge-base-design.md` — Section 6 lists the full target list.

---

## ✅ Successfully ingested (22 readable files; 21 unique sources)

| File | Feeds wiki pages | Notes |
|---|---|---|
| `Free Stock Market API and Financial Statements API.md` ⭐ (user-added) | `data-sources`, `earnings-and-catalysts`, `financial-statements`, `technical-indicators`, `key-metrics-glossary` | **FMP full developer docs** — 2,348 lines, 28 sections (Statements, Earnings Transcript, News, Form 13F, Analyst, Technical Indicators, SEC Filings, Insider Trades, DCF, etc.). This is the richest single file in `raw/` — functionally a complete API reference. |
| `alpha-architect-quant-momentum.pdf` + `alpha-architect-quant-momentum.txt` (user-added, extracted via poppler) | `quant-factors`, `momentum-and-swing-trading` | **Jack Vogel (Alpha Architect) — Quantitative Momentum Investing Philosophy.** 798 lines of readable text. 5-step process: (1) universe = largest 1,500 liquid U.S. stocks, (2) remove outliers via academic red flags, (3) momentum screen → top 100, (4) momentum *quality* screen (frog-in-pan/FIP, smooth vs gap-driven returns) → top 50, (5) invest with conviction. |
| `chartschool-technical-analysis.md` | `technical-analysis`, `technical-indicators` | Overview-level. Canonical TA primer. |
| `chartschool-chart-analysis.md` | `technical-analysis` | Section outline — individual patterns need follow-up fetches. |
| `minervini-sepa-vcp.md` | `momentum-and-swing-trading`, `position-sizing`, `risk-management`, `selling-and-rotation` | Deep SEPA + VCP methodology with specific numbers. |
| `quantstrategy-sepa.md` | Same as above | Complementary SEPA source with slightly different VCP contraction numbers (20–30/10–15/5–8%). |
| `wikipedia-can-slim.md` | `growth-investing` | Standard reference. |
| `cfi-can-slim.md` | `growth-investing` | Corporate Finance Institute's framing. |
| `macroops-can-slim-deep-dive.md` | `growth-investing` | Quantitative specifics (20–50% quarterly EPS, 24% 5-yr CAGR, 11.8M avg shares). |
| `damodaran-valuation-class.md` | `value-investing`, `valuation-methods`, `financial-statements`, `key-metrics-glossary` | Full 25-session course structure; deep content requires watching webcasts. |
| `buffett-letters-index.md` | `value-investing`, `behavioral-finance`, `traders-and-thinkers` | Index of 48 letters 1977–2024. Individual letters = PDFs (manual download). |
| `dalio-economic-principles-site.md` | `macro-and-regime` | Site overview + 6 downloadable PDFs listed. |
| `dalio-economic-machine-transcript.md` | `macro-and-regime`, `strategy-selection`, `risk-tolerance-mapping` | Three forces framework, credit mechanics, four deleveraging paths. |
| `fama-french-factors.md` | `quant-factors` | SMB + HML formulas, market excess return definition. RMW/CMA need follow-up fetch. |
| `aqr-research-library.md` | `quant-factors`, `portfolio-construction`, `behavioral-finance` | Library structure + canonical paper names for follow-up. |
| `research-affiliates-value-quality-momentum.md` | `quant-factors`, `strategy-selection`, `portfolio-construction` | Integrated VQM thesis — excellent for `strategy-selection.md`. |
| `howard-marks-memos-index.md` | `risk-management`, `behavioral-finance`, `macro-and-regime` | Memos catalog 1990–2026; key memos identified. PDFs need manual download. |
| `alpaca-api-overview.md` | `data-sources` | API product lines; details need deeper fetches. |
| `finnhub-api-overview.md` | `data-sources` | Landing page only — thin; confirmed 60 calls/min free tier. |
| `polygon-massive-api-overview.md` | `data-sources` | Polygon rebranded to Massive; covers stocks/options/futures/indices/forex/crypto. |
| `sec-investor-basics.md` | `market-structure`, `risk-management` | SEC roadmap + fraud-prevention guidance + T+1/PDT callouts. |

## ⚠️ Couldn't fetch — need manual download or alternative

| Source                                                                                                  | Reason                                  | Workaround                                                                                                                                                                                                                                       |
| ------------------------------------------------------------------------------------------------------- | --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Damodaran homepage                                                                                      | Fetch error (`null` DOM)                | Skip — `damodaran-valuation-class.md` covers most of what's needed. Retry later.                                                                                                                                                                 |
| ~~Alpha Architect — *Quantitative Momentum Investing Philosophy* PDF~~ ✅ **RESOLVED** — user downloaded; extracted via `pdftotext -layout` (poppler installed 2026-04-23). Text file sits next to PDF. | 403 Forbidden | — |
| FRED (St. Louis Fed)                                                                                    | 403 Forbidden on main site              | Alternative: fetch `https://fred.stlouisfed.org/docs/api/fred/` (API docs page) — may be more bot-friendly.                                                                                                                                      |
| ~~Financial Modeling Prep~~ ✅ **RESOLVED** — user saved full developer docs as `Free Stock Market API and Financial Statements API.md`. | 403 Forbidden | — |
| Investopedia (fundamental analysis, Kelly criterion, glossary terms)                                    | Blocks Claude Code bot                  | Manual: user copy-paste relevant pages, OR we synthesize from cross-source coverage and skip Investopedia. Investopedia isn't essential — CFA Institute + SEC + Damodaran cover the same ground.                                                 |
| Ray Dalio PDFs (economic machine, Big Debt Crises, Changing World Order)                                | WebFetch can't parse PDFs               | Manual: download from https://economicprinciples.org/ and save to `raw/` as `dalio-economic-machine.pdf` etc. OR we proceed with the transcript summary already saved (`dalio-economic-machine-transcript.md`), which covers the core framework. |
| Buffett letters (2004–2024)                                                                             | PDFs                                    | Manual download from https://www.berkshirehathaway.com/letters/letters.html if deep letter content desired. For P1a we only need the index; letters themselves can be P1b extras.                                                                |
| Howard Marks' memo *The Indispensability of Risk* PDF                                                   | PDF binary, not parseable               | Manual download from `https://www.oaktreecapital.com/docs/default-source/memos/the-indispensability-of-risk.pdf`. OR we source Marks' risk framework from his memo titles + publicly-available summaries.                                        |
| AQR flagship papers (*Value and Momentum Everywhere*, *QMJ*, *Betting Against Beta*, *Buffett's Alpha*) | Mostly PDFs behind login or paper sites | Manual: several are on SSRN. Search by title; most are free. For P1b.                                                                                                                                                                            |

## 📌 Pending — not yet attempted, priority for P1b

These were in the spec's Section 6 shortlist but I stopped to report back; can continue if you want:

| Source | Spec # |
|---|---|
| Damodaran — Investment Philosophies class structure | #3 |
| Alpha Architect — Momentum research archive (top-level index) | #10 |
| Kenneth French — 5-factor description (RMW/CMA) | Follow-up to #7 |
| Kenneth French — Momentum factor detail | Follow-up to #7 |
| CFA Institute Research Foundation — free books page | #17 |
| SEC EDGAR — filings landing + full-text search overview | #18 |
| Investopedia — specific term pages (if we decide to workaround block) | #21 |

## 📊 Coverage summary

By target wiki page (P1 complete list):

| Wiki page | Coverage | Notes |
|---|---|---|
| `value-investing.md` | 🟡 Partial | Damodaran course + Buffett letter index. No Graham primary source yet. |
| `growth-investing.md` | 🟢 Good | 3 CAN SLIM sources (Wikipedia + CFI + Macro Ops). |
| `momentum-and-swing-trading.md` ⭐ P1a | 🟢 Good | 2 Minervini SEPA sources with overlapping & complementary details. |
| `technical-analysis.md` | 🟢 Good | 2 ChartSchool sources (overview + chart analysis structure). |
| `quant-factors.md` | 🟢 Good | Fama-French partial (HML + SMB), AQR structure, Research Affiliates VQM, **Alpha Architect Quant Momentum** (5-step process + FIP quality screen, fully readable). Still need Fama-French RMW/CMA/MOM primary details — currently the only gap on this page. |
| `macro-and-regime.md` | 🟢 Good | Dalio framework transcript + Economic Principles site. |
| `risk-management.md` ⭐ P1a | 🟡 Partial | Minervini 7–8% stop rule, Marks memo index. No primary Marks content yet. |
| `position-sizing.md` ⭐ P1a | 🟡 Partial | Minervini formula with worked example. No Kelly criterion primary source yet. |
| `portfolio-construction.md` | 🟡 Partial | Research Affiliates integration + AQR structure. Need Markowitz/MPT primary. |
| `valuation-methods.md` | 🟡 Partial | Damodaran course structure. Deep detail requires watching webcasts. |
| `technical-indicators.md` | 🟡 Partial | ChartSchool indicator list. Individual indicator pages need follow-up fetches. |
| `financial-statements.md` | 🔴 Thin | Damodaran has relevant sessions but no deep extract yet. SEC EDGAR not fetched. |
| `earnings-and-catalysts.md` | 🔴 Thin | Referenced in Minervini/CAN SLIM. Needs dedicated sources. |
| `news-and-sentiment.md` | 🔴 None | Needs dedicated fetch (AAII survey, VIX explainer, Finnhub sentiment API). |
| `selling-and-rotation.md` ⭐ P1a | 🟢 Good | Minervini exit strategies (3 types); CAN SLIM stop-loss. |
| `behavioral-finance.md` | 🟡 Partial | Marks memos + Buffett letters indexed. Need Kahneman primary. |
| `strategy-selection.md` ⭐ P1a | 🟢 Good | Research Affiliates VQM + Dalio regime framework feed this directly. |
| `risk-tolerance-mapping.md` ⭐ P1a | 🟢 Good | Minervini position sizing + Research Affiliates complementary factor framing. |
| `research-workflow.md` ⭐ P1a | 🟢 Good | SEPA workflow + CAN SLIM screening + VQM integration provide process detail. |
| `data-sources.md` ⭐ P1a | 🟢 **Excellent** | Alpaca + Finnhub + Polygon/Massive + **FMP full docs** (2,348 lines, 28 sections) + SEC callouts. FRED still pending but non-critical. |
| `key-metrics-glossary.md` | 🟡 Partial | Distributed across multiple files; needs glossary-specific pass. |
| `traders-and-thinkers.md` | 🟡 Partial | Bio material distributed across files; needs dedicated assembly. |
| `market-structure.md` | 🟢 Good | SEC Investor.gov basics. |

## Legend
- 🟢 Good — enough for the wiki page to be written well
- 🟡 Partial — wiki page can be written but with gaps; will note "needs further sources"
- 🔴 Thin — page will be shallow until more sources added
- ⭐ — P1a MVP enabler (must be green before the agent can run 2-week test case)

## Status per P1a enabler

All 8 P1a pages can now be written from `raw/` content — though a few (`risk-management`, `position-sizing`) will benefit from additional primary sources before being considered complete.
