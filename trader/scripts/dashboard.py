#!/usr/bin/env python3
"""Generate the portfolio dashboard in two private formats. Stdlib only.

  - DASHBOARD.md   — committed to the repo; glanceable in the GitHub mobile app.
  - dashboard.html — self-contained styled page to open locally on a computer.

Both render the same numbers from portfolio.json + suggestions.json with live
prices (degrading gracefully to cost basis if the feed is unreachable). No
hosting, no secrets — read-only views of state already in the repo.

Usage:  python3 dashboard.py        # writes ../DASHBOARD.md and ../dashboard.html
"""
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from quotes import quote  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent          # trader/
REPO_ROOT = ROOT.parent                                # repo root
PORTFOLIO = ROOT / "portfolio.json"
SUGGESTIONS = ROOT / "suggestions.json"
MD_OUT = REPO_ROOT / "DASHBOARD.md"                    # top-level: glanceable in GitHub mobile app
HTML_OUT = REPO_ROOT / "dashboard.html"


def load(path, default):
    return json.loads(path.read_text()) if path.exists() else default


def safe_quote(ticker):
    try:
        q = quote(ticker)
        return q.get("price"), q.get("day_change_pct"), None
    except Exception as e:  # noqa: BLE001 - degrade to cost basis
        return None, None, str(e)


def compute():
    pf = load(PORTFOLIO, None)
    if pf is None:
        sys.exit("No portfolio.json — run portfolio.py init first.")
    sg = load(SUGGESTIONS, {"suggestions": []})

    rows, total_value, stale = [], 0.0, False
    for pos in pf["positions"]:
        price, day_pct, err = safe_quote(pos["ticker"])
        if price is None:
            price, stale = pos["avg_cost"], True
        value = pos["shares"] * price
        total_value += value
        rows.append({
            "ticker": pos["ticker"], "imported": pos.get("imported", False),
            "shares": pos["shares"], "avg_cost": pos["avg_cost"], "price": price,
            "day_pct": day_pct, "value": value,
            "unreal_pct": 100 * (price / pos["avg_cost"] - 1) if pos["avg_cost"] else 0,
            "stop": pos.get("stop"), "target": pos.get("target"),
            "price_stale": err is not None,
        })
    rows.sort(key=lambda r: r["value"], reverse=True)

    cash = pf["cash"]
    equity = cash + total_value
    total_ret = 100 * (equity / pf["starting_cash"] - 1) if pf["starting_cash"] else 0
    bench = pf["benchmark"]
    spy_price, _, spy_err = safe_quote(bench["ticker"])
    spy_ret = 100 * (spy_price / bench["start_price"] - 1) if spy_price else None
    alpha = (total_ret - spy_ret) if spy_ret is not None else None

    closed = [s for s in sg["suggestions"]
              if s.get("action") == "buy" and s.get("status") == "closed" and s.get("outcome")]
    wins = [s for s in closed if s["outcome"].get("grade") == "win"]
    losses = [s for s in closed if s["outcome"].get("grade") == "loss"]
    calib = {
        "n": len(closed), "wins": len(wins), "losses": len(losses),
        "hit_rate": (100 * len(wins) / len(closed)) if closed else None,
        "avg_alpha": (sum(s["outcome"]["alpha_pct"] for s in closed) / len(closed)) if closed else None,
    }
    open_calls = [s for s in sg["suggestions"]
                  if s.get("action") == "buy" and s.get("status") == "open"]

    return {
        "pf": pf, "rows": rows, "cash": cash, "equity": equity,
        "total_ret": total_ret, "bench": bench, "spy_ret": spy_ret, "alpha": alpha,
        "calib": calib, "open_calls": open_calls, "stale": stale,
        "closed_recent": sorted(closed, key=lambda s: s["outcome"].get("closed_date", ""), reverse=True)[:8],
    }


# ---------------------------------------------------------------- formatting

def money(x):
    return f"${x:,.2f}" if x is not None else "—"


def pct(x, plus=True):
    if x is None:
        return "—"
    return f"{x:+.2f}%" if plus else f"{x:.2f}%"


def sign_word(x):
    return "pos" if (x or 0) > 0 else ("neg" if (x or 0) < 0 else "flat")


# ---------------------------------------------------------------- markdown

def render_md(d):
    pf, bench = d["pf"], d["bench"]
    L = []
    L.append("# 📈 Portfolio Dashboard\n")
    L.append(f"_Research-only paper portfolio — the agent never trades. "
             f"Updated {datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC}._\n")
    if d["stale"]:
        L.append("> ⚠️ Live price feed unavailable for one or more names; "
                 "those rows show cost basis. Numbers regenerate next run.\n")
    a = d["alpha"]
    verdict = "—"
    if a is not None:
        verdict = f"**{'ahead of' if a > 0 else ('behind' if a < 0 else 'level with')} SPY by {abs(a):.2f}%**"
    L.append(f"## {money(d['equity'])}  ·  {pct(d['total_ret'])} total  ·  {verdict}\n")
    L.append(f"- Cash: {money(d['cash'])}  |  Invested: {money(d['equity'] - d['cash'])}")
    L.append(f"- Since {pf['created']}: portfolio {pct(d['total_ret'])} vs "
             f"{bench['ticker']} {pct(d['spy_ret'])}  →  alpha {pct(a)}\n")

    L.append("## Positions\n")
    L.append("| Ticker | Shares | Avg cost | Price | Day | Value | Unreal. | Stop | Target |")
    L.append("|---|--:|--:|--:|--:|--:|--:|--:|--:|")
    for r in d["rows"]:
        tk = r["ticker"] + ("\\*" if r["imported"] else "")
        L.append(f"| {tk} | {r['shares']:g} | {money(r['avg_cost'])} | {money(r['price'])} "
                 f"| {pct(r['day_pct'])} | {money(r['value'])} | {pct(r['unreal_pct'])} "
                 f"| {money(r['stop']) if r['stop'] else '—'} | {money(r['target']) if r['target'] else '—'} |")
    if not d["rows"]:
        L.append("| _(no positions)_ | | | | | | | | |")
    if any(r["imported"] for r in d["rows"]):
        L.append("\n\\* imported holding — Unreal. % is vs your own cost basis.")

    c = d["calib"]
    L.append("\n## Track record (graded calls)\n")
    if c["n"]:
        L.append(f"- Closed calls: **{c['n']}**  |  beat SPY: **{c['wins']}**  |  "
                 f"lagged: **{c['losses']}**  |  hit rate: **{c['hit_rate']:.0f}%**")
        L.append(f"- Average alpha per closed call: **{pct(c['avg_alpha'])}**")
    else:
        L.append("- No closed calls yet — stats appear once positions are sold.")

    if d["open_calls"]:
        L.append("\n## Open agent calls\n")
        for s in d["open_calls"]:
            L.append(f"- **{s['ticker']}** @ {money(s['price'])} "
                     f"(conf: {s.get('confidence', '—')}) — {s['thesis']}")

    L.append("\n---\n_Not financial advice. Generated by `trader/scripts/dashboard.py`._")
    MD_OUT.write_text("\n".join(L) + "\n")


# ---------------------------------------------------------------- html

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Portfolio · trading-agent</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,900&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<style>
  :root{
    --ink:#0a0c10; --ink2:#11141a; --line:#23272f;
    --paper:#ece4d3; --muted:#8b8676; --faint:#5b5d63;
    --gold:#c8a24a; --gain:#5fb87a; --loss:#d8604a; --flat:#8b8676;
    --serif:'Fraunces',Georgia,serif; --mono:'JetBrains Mono',ui-monospace,monospace;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  html{-webkit-text-size-adjust:100%}
  body{
    background:
      radial-gradient(1200px 600px at 80% -10%, rgba(200,162,74,.08), transparent 60%),
      radial-gradient(900px 500px at -10% 110%, rgba(95,184,122,.05), transparent 55%),
      var(--ink);
    color:var(--paper); font-family:var(--mono); line-height:1.5;
    min-height:100vh; padding:clamp(20px,5vw,64px);
  }
  body::before{
    content:""; position:fixed; inset:0; pointer-events:none; opacity:.035; z-index:0;
    background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  }
  .wrap{max-width:980px;margin:0 auto;position:relative;z-index:1}
  .masthead{
    display:flex;justify-content:space-between;align-items:baseline;
    border-bottom:1px solid var(--line);padding-bottom:14px;margin-bottom:34px;gap:16px;flex-wrap:wrap;
  }
  .brand{font-family:var(--serif);font-weight:900;font-size:clamp(20px,3vw,26px);letter-spacing:-.01em}
  .brand .dot{color:var(--gold)}
  .stamp{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.18em}
  .hero{margin-bottom:14px}
  .hero .label{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--muted)}
  .hero .equity{font-family:var(--serif);font-weight:600;font-size:clamp(48px,11vw,92px);line-height:.95;letter-spacing:-.02em;margin:6px 0 2px}
  .verdict{font-family:var(--serif);font-style:italic;font-size:clamp(17px,2.6vw,23px);color:var(--paper)}
  .verdict .em{font-style:normal;font-weight:600}
  .ribbon{display:flex;flex-wrap:wrap;gap:10px;margin:26px 0 40px}
  .chip{
    border:1px solid var(--line);border-radius:2px;padding:12px 16px;background:rgba(255,255,255,.012);
    min-width:150px;flex:1
  }
  .chip .k{font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--muted)}
  .chip .v{font-family:var(--serif);font-weight:600;font-size:clamp(20px,3.2vw,28px);margin-top:6px}
  h2{
    font-family:var(--serif);font-weight:500;font-size:13px;letter-spacing:.26em;text-transform:uppercase;
    color:var(--gold);margin:40px 0 16px;display:flex;align-items:center;gap:14px
  }
  h2::after{content:"";flex:1;height:1px;background:var(--line)}
  table{width:100%;border-collapse:collapse;font-size:13.5px}
  thead th{
    text-align:right;font-weight:500;color:var(--muted);font-size:10px;letter-spacing:.14em;
    text-transform:uppercase;padding:0 0 10px;border-bottom:1px solid var(--line)
  }
  thead th:first-child{text-align:left}
  tbody td{padding:13px 0;border-bottom:1px solid rgba(35,39,47,.55);text-align:right;font-variant-numeric:tabular-nums}
  tbody td:first-child{text-align:left;font-weight:700;letter-spacing:.02em}
  tbody tr:hover td{background:rgba(200,162,74,.03)}
  .tk-star{color:var(--gold);font-size:10px;vertical-align:super;margin-left:1px}
  .pos{color:var(--gain)} .neg{color:var(--loss)} .flat{color:var(--flat)}
  .stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:1px;background:var(--line);border:1px solid var(--line)}
  .stat{background:var(--ink);padding:18px 16px}
  .stat .k{font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
  .stat .v{font-family:var(--serif);font-weight:600;font-size:26px;margin-top:8px}
  .calls{list-style:none;display:flex;flex-direction:column;gap:1px;background:var(--line);border:1px solid var(--line)}
  .calls li{background:var(--ink);padding:14px 16px}
  .calls .h{display:flex;justify-content:space-between;align-items:baseline;gap:12px}
  .calls .name{font-weight:700;font-size:15px}
  .calls .conf{font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);border:1px solid var(--line);padding:2px 7px;border-radius:2px}
  .calls .th{color:var(--muted);font-size:12.5px;margin-top:7px;line-height:1.55}
  .warn{border-left:2px solid var(--loss);background:rgba(216,96,74,.06);padding:11px 15px;margin-bottom:24px;font-size:12.5px;color:var(--paper)}
  .foot{margin-top:46px;padding-top:18px;border-top:1px solid var(--line);font-size:11px;color:var(--faint);letter-spacing:.04em;line-height:1.7}
  .foot .guard{color:var(--gold)}
  .empty{color:var(--muted);font-style:italic;padding:14px 0}
</style>
</head>
<body>
<div class="wrap">
  <div class="masthead">
    <div class="brand">trading&middot;agent<span class="dot">.</span></div>
    <div class="stamp">__STAMP__ · paper portfolio</div>
  </div>

  __WARN__

  <div class="hero">
    <div class="label">Total equity</div>
    <div class="equity">__EQUITY__</div>
    <div class="verdict">__VERDICT__</div>
  </div>

  <div class="ribbon">
    <div class="chip"><div class="k">Total return</div><div class="v __TR_CLS__">__TR__</div></div>
    <div class="chip"><div class="k">__BENCH__ benchmark</div><div class="v __SPY_CLS__">__SPY__</div></div>
    <div class="chip"><div class="k">Alpha</div><div class="v __AL_CLS__">__AL__</div></div>
    <div class="chip"><div class="k">Cash</div><div class="v">__CASH__</div></div>
  </div>

  <h2>Positions</h2>
  <table>
    <thead><tr>
      <th>Ticker</th><th>Shares</th><th>Avg cost</th><th>Price</th><th>Day</th>
      <th>Value</th><th>Unreal.</th><th>Stop</th><th>Target</th>
    </tr></thead>
    <tbody>__ROWS__</tbody>
  </table>
  __IMPNOTE__

  <h2>Track record</h2>
  <div class="stats">__STATS__</div>

  <h2>Open calls</h2>
  __OPEN__

  <div class="foot">
    <span class="guard">The agent never executes trades and holds no money.</span>
    Every suggestion is simulated here and graded against the S&amp;P 500.
    Not financial advice. Generated __NOW__ by trader/scripts/dashboard.py.
  </div>
</div>
</body>
</html>
"""


def render_html(d):
    a = d["alpha"]
    if a is None:
        verdict = "Benchmark unavailable this run."
    else:
        word = "ahead of" if a > 0 else ("behind" if a < 0 else "level with")
        verdict = (f'<span class="em {sign_word(a)}">{word} {d["bench"]["ticker"]} '
                   f'by {abs(a):.2f}%</span> since {d["pf"]["created"]}')

    rows = []
    for r in d["rows"]:
        star = '<span class="tk-star">★</span>' if r["imported"] else ""
        rows.append(
            f"<tr><td>{r['ticker']}{star}</td>"
            f"<td>{r['shares']:g}</td><td>{money(r['avg_cost'])}</td><td>{money(r['price'])}</td>"
            f"<td class='{sign_word(r['day_pct'])}'>{pct(r['day_pct'])}</td>"
            f"<td>{money(r['value'])}</td>"
            f"<td class='{sign_word(r['unreal_pct'])}'>{pct(r['unreal_pct'])}</td>"
            f"<td>{money(r['stop']) if r['stop'] else '—'}</td>"
            f"<td>{money(r['target']) if r['target'] else '—'}</td></tr>")
    rows_html = "".join(rows) or '<tr><td colspan="9" class="empty">No positions yet.</td></tr>'

    c = d["calib"]
    if c["n"]:
        stats = (
            f'<div class="stat"><div class="k">Closed calls</div><div class="v">{c["n"]}</div></div>'
            f'<div class="stat"><div class="k">Beat SPY</div><div class="v pos">{c["wins"]}</div></div>'
            f'<div class="stat"><div class="k">Lagged</div><div class="v neg">{c["losses"]}</div></div>'
            f'<div class="stat"><div class="k">Hit rate</div><div class="v">{c["hit_rate"]:.0f}%</div></div>'
            f'<div class="stat"><div class="k">Avg alpha</div><div class="v {sign_word(c["avg_alpha"])}">{pct(c["avg_alpha"])}</div></div>')
    else:
        stats = '<div class="stat"><div class="k">Status</div><div class="v" style="font-size:15px">No closed calls yet</div></div>'

    if d["open_calls"]:
        items = []
        for s in d["open_calls"]:
            items.append(
                f'<li><div class="h"><span class="name">{s["ticker"]} '
                f'<span style="color:var(--muted);font-weight:400">@ {money(s["price"])}</span></span>'
                f'<span class="conf">{s.get("confidence","—")}</span></div>'
                f'<div class="th">{s["thesis"]}</div></li>')
        open_html = '<ul class="calls">' + "".join(items) + "</ul>"
    else:
        open_html = '<p class="empty">No open agent calls right now.</p>'

    warn = ('<div class="warn">⚠ Live price feed unavailable for one or more names; '
            'those rows show cost basis. Figures regenerate next run.</div>') if d["stale"] else ""
    impnote = ('<p style="color:var(--muted);font-size:11px;margin-top:10px">'
               '★ imported holding — Unreal. % is vs your own cost basis.</p>') \
              if any(r["imported"] for r in d["rows"]) else ""

    html = HTML_TEMPLATE
    repl = {
        "__STAMP__": date.today().isoformat(),
        "__WARN__": warn,
        "__EQUITY__": money(d["equity"]),
        "__VERDICT__": verdict,
        "__TR__": pct(d["total_ret"]), "__TR_CLS__": sign_word(d["total_ret"]),
        "__BENCH__": d["bench"]["ticker"],
        "__SPY__": pct(d["spy_ret"]), "__SPY_CLS__": sign_word(d["spy_ret"]),
        "__AL__": pct(a), "__AL_CLS__": sign_word(a),
        "__CASH__": money(d["cash"]),
        "__ROWS__": rows_html, "__IMPNOTE__": impnote,
        "__STATS__": stats, "__OPEN__": open_html,
        "__NOW__": f"{datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC}",
    }
    for k, v in repl.items():
        html = html.replace(k, str(v))
    HTML_OUT.write_text(html)


def main():
    d = compute()
    render_md(d)
    render_html(d)
    print(f"Wrote {MD_OUT.name} and {HTML_OUT.name} "
          f"(equity {money(d['equity'])}, {pct(d['total_ret'])} vs {d['bench']['ticker']} {pct(d['spy_ret'])}).")


if __name__ == "__main__":
    main()
