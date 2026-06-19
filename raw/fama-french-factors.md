# Kenneth French Data Library — Fama-French Factors (descriptions)

**Source URL**: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_factors.html
**Publisher**: Kenneth R. French, Tuck School of Business at Dartmouth
**Retrieved**: 2026-04-23
**License / use**: Freely available data and methodology. Standard academic attribution.

---

## Factors described on this page

### Rm-Rf (Market excess return)
Value-weighted return of all eligible CRSP firms incorporated in the US and trading on NYSE, AMEX, or NASDAQ, **minus** the risk-free rate (one-month Treasury bill).

### SMB (Small Minus Big) — the size factor
Formula:
```
SMB = 1/3 × (Small Value + Small Neutral + Small Growth)
    − 1/3 × (Big Value + Big Neutral + Big Growth)
```
Captures the return differential between smaller and larger companies.

### HML (High Minus Low) — the value factor
Formula:
```
HML = 1/2 × (Small Value + Big Value)
    − 1/2 × (Small Growth + Big Growth)
```
Measures value versus growth stock performance.

## Data availability

Multiple frequencies:
- **Daily**: July 1926 – February 2026
- **Weekly**: July 1926 – February 2026
- **Monthly**: July 1926 – February 2026
- **Annual**: 1927 – 2025

## Not described on this page (present in other library pages)

- **RMW (Robust Minus Weak)** — profitability factor (5-factor model)
- **CMA (Conservative Minus Aggressive)** — investment factor (5-factor model)
- **MOM (Momentum)** — Carhart 4-factor model

**For `quant-factors.md` wiki page**: Need to additionally fetch:
- `https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_5developed.html` (5-factor description)
- `https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_mom_factor.html` (momentum)
