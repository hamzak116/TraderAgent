#!/usr/bin/env python3
"""Paper-portfolio bookkeeping for the trading agent. Stdlib only.

This is the system of record for every suggestion the agent makes.
The agent NEVER trades real money; this ledger simulates what would
happen if every suggestion were followed.

Usage:
    portfolio.py init --cash 10000 [--force]
    portfolio.py import TICKER --shares N --avg-cost P [--opened YYYY-MM-DD]
    portfolio.py rebase            # reset performance baseline to today (after imports)
    portfolio.py buy TICKER --dollars 1500 --thesis "..." [--price P]
                 [--confidence high|medium|low] [--stop P] [--target P] [--horizon-days N]
    portfolio.py sell TICKER --reason "..." [--pct 100] [--price P]
    portfolio.py note TICKER --action hold|watch|avoid --thesis "..."
    portfolio.py status            # markdown valuation report w/ live prices
    portfolio.py history [--open]  # all suggestions + calibration stats

`import` adds a pre-existing real-life holding: cash is untouched, no buy
suggestion is recorded (it was the user's call, not the agent's), and the
user's true cost basis is preserved for P&L display. Run `rebase` once after
importing so the agent's vs-SPY track record starts from the takeover date.
"""
import argparse
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from quotes import quote  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PORTFOLIO = ROOT / "portfolio.json"
SUGGESTIONS = ROOT / "suggestions.json"
BENCHMARK = "SPY"


def load(path: Path, default):
    if path.exists():
        return json.loads(path.read_text())
    return default


def save(path: Path, data):
    path.write_text(json.dumps(data, indent=2) + "\n")


def load_state():
    pf = load(PORTFOLIO, None)
    if pf is None:
        sys.exit("No portfolio. Run: portfolio.py init --cash N")
    sg = load(SUGGESTIONS, {"next_id": 1, "suggestions": []})
    return pf, sg


def today() -> str:
    return date.today().isoformat()


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def get_price(ticker: str, override) -> float:
    if override is not None:
        return float(override)
    return float(quote(ticker)["price"])


def find_position(pf, ticker):
    for pos in pf["positions"]:
        if pos["ticker"] == ticker:
            return pos
    return None


# ---------------------------------------------------------------- commands

def cmd_init(args):
    if PORTFOLIO.exists() and not args.force:
        sys.exit(f"{PORTFOLIO} exists. Use --force to reinitialize (wipes paper history).")
    spy = quote(BENCHMARK)
    pf = {
        "created": today(),
        "starting_cash": round(args.cash, 2),
        "cash": round(args.cash, 2),
        "positions": [],
        "benchmark": {"ticker": BENCHMARK, "start_price": spy["price"], "start_date": today()},
    }
    save(PORTFOLIO, pf)
    if not SUGGESTIONS.exists() or args.force:
        save(SUGGESTIONS, {"next_id": 1, "suggestions": []})
    print(f"Initialized paper portfolio: ${args.cash:,.2f} cash. "
          f"Benchmark {BENCHMARK} @ {spy['price']}.")


def cmd_import(args):
    pf, sg = load_state()
    ticker = args.ticker.upper()
    if find_position(pf, ticker):
        sys.exit(f"{ticker} already in portfolio. Use `buy` to add to it.")
    market = get_price(ticker, None)
    spy_now = quote(BENCHMARK)["price"]
    pos = {
        "ticker": ticker, "shares": round(args.shares, 4), "avg_cost": round(args.avg_cost, 4),
        "opened": args.opened or today(),
        "lots": [{"date": args.opened or today(), "shares": round(args.shares, 4),
                  "price": round(args.avg_cost, 4), "imported": True}],
        "stop": None, "target": None,
        "imported": True, "import_date": today(), "import_price": market,
    }
    pf["positions"].append(pos)
    record_suggestion(
        sg, action="import", ticker=ticker, price=market, shares=round(args.shares, 4),
        dollars=round(args.shares * market, 2),
        thesis=f"User-imported pre-existing holding (cost basis ${args.avg_cost:,.2f}/sh). "
               f"Not an agent call; agent decisions on it are measured from import price.",
        confidence=None, stop=None, target=None, horizon_days=None,
        spy_at_suggestion=spy_now, status="standalone", outcome=None,
    )
    save(PORTFOLIO, pf)
    save(SUGGESTIONS, sg)
    unreal = 100 * (market / args.avg_cost - 1)
    print(f"Imported {args.shares} {ticker} @ cost ${args.avg_cost:,.2f} "
          f"(now ${market:,.2f}, {unreal:+.2f}% for you). Cash untouched. "
          f"Run `rebase` after the last import.")


def cmd_rebase(args):
    pf, _ = load_state()
    total = pf["cash"]
    for pos in pf["positions"]:
        total += pos["shares"] * quote(pos["ticker"])["price"]
    spy = quote(BENCHMARK)
    pf["starting_cash"] = round(total, 2)
    pf["created"] = today()
    pf["benchmark"] = {"ticker": BENCHMARK, "start_price": spy["price"], "start_date": today()}
    save(PORTFOLIO, pf)
    print(f"Baseline rebased: agent performance measured from {today()} "
          f"with equity ${total:,.2f}, {BENCHMARK} @ {spy['price']}.")


def record_suggestion(sg, **fields) -> int:
    sid = sg["next_id"]
    sg["next_id"] += 1
    entry = {"id": sid, "recorded_at": now_iso(), "date": today(), **fields}
    sg["suggestions"].append(entry)
    return sid


def cmd_buy(args):
    pf, sg = load_state()
    ticker = args.ticker.upper()
    price = get_price(ticker, args.price)
    dollars = float(args.dollars)
    if dollars > pf["cash"] + 0.01:
        sys.exit(f"Insufficient paper cash: ${pf['cash']:,.2f} available, ${dollars:,.2f} requested.")
    shares = round(dollars / price, 4)
    spy_now = quote(BENCHMARK)["price"]

    pos = find_position(pf, ticker)
    if pos:
        total_cost = pos["shares"] * pos["avg_cost"] + dollars
        pos["shares"] = round(pos["shares"] + shares, 4)
        pos["avg_cost"] = round(total_cost / pos["shares"], 4)
        pos["lots"].append({"date": today(), "shares": shares, "price": price})
    else:
        pos = {
            "ticker": ticker, "shares": shares, "avg_cost": price,
            "opened": today(), "lots": [{"date": today(), "shares": shares, "price": price}],
            "stop": args.stop, "target": args.target,
        }
        pf["positions"].append(pos)
    if args.stop is not None:
        pos["stop"] = args.stop
    if args.target is not None:
        pos["target"] = args.target
    pf["cash"] = round(pf["cash"] - dollars, 2)

    sid = record_suggestion(
        sg, action="buy", ticker=ticker, price=price, shares=shares,
        dollars=round(dollars, 2), thesis=args.thesis, confidence=args.confidence,
        stop=args.stop, target=args.target, horizon_days=args.horizon_days,
        spy_at_suggestion=spy_now, status="open", outcome=None,
    )
    save(PORTFOLIO, pf)
    save(SUGGESTIONS, sg)
    print(f"#{sid} BUY {shares} {ticker} @ ${price:,.2f} (${dollars:,.2f}). "
          f"Cash left: ${pf['cash']:,.2f}.")


def cmd_sell(args):
    pf, sg = load_state()
    ticker = args.ticker.upper()
    pos = find_position(pf, ticker)
    if not pos:
        sys.exit(f"No open position in {ticker}.")
    price = get_price(ticker, args.price)
    pct = float(args.pct)
    shares_sold = round(pos["shares"] * pct / 100, 4)
    proceeds = round(shares_sold * price, 2)
    ret_pct = round(100 * (price / pos["avg_cost"] - 1), 2)
    spy_now = quote(BENCHMARK)["price"]

    pf["cash"] = round(pf["cash"] + proceeds, 2)
    full_exit = pct >= 99.99
    if full_exit:
        pf["positions"] = [p for p in pf["positions"] if p["ticker"] != ticker]
    else:
        pos["shares"] = round(pos["shares"] - shares_sold, 4)

    # close out the open buy suggestions for this ticker, grading each lot vs SPY
    graded = []
    for s in sg["suggestions"]:
        if s["ticker"] == ticker and s["action"] == "buy" and s["status"] == "open" and full_exit:
            stock_ret = round(100 * (price / s["price"] - 1), 2)
            spy_ret = round(100 * (spy_now / s["spy_at_suggestion"] - 1), 2)
            alpha = round(stock_ret - spy_ret, 2)
            s["status"] = "closed"
            s["outcome"] = {
                "closed_date": today(), "close_price": price,
                "return_pct": stock_ret, "spy_return_pct": spy_ret, "alpha_pct": alpha,
                "grade": "win" if alpha > 0 else ("loss" if alpha < 0 else "flat"),
                "exit_reason": args.reason, "lesson": None,
            }
            graded.append(s)

    sid = record_suggestion(
        sg, action="sell", ticker=ticker, price=price, shares=shares_sold,
        dollars=proceeds, thesis=args.reason, confidence=None, stop=None,
        target=None, horizon_days=None, spy_at_suggestion=spy_now,
        status="closed", outcome={"return_pct": ret_pct, "vs_avg_cost": pos.get("avg_cost")},
    )
    save(PORTFOLIO, pf)
    save(SUGGESTIONS, sg)
    print(f"#{sid} SELL {shares_sold} {ticker} @ ${price:,.2f} → ${proceeds:,.2f} "
          f"({ret_pct:+.2f}% vs avg cost). Cash: ${pf['cash']:,.2f}.")
    for s in graded:
        o = s["outcome"]
        print(f"  graded buy #{s['id']}: {o['return_pct']:+.2f}% vs SPY {o['spy_return_pct']:+.2f}% "
              f"→ alpha {o['alpha_pct']:+.2f}% ({o['grade']})")


def cmd_note(args):
    _, sg = load_state()
    sid = record_suggestion(
        sg, action=args.action, ticker=args.ticker.upper(),
        price=get_price(args.ticker, args.price), shares=None, dollars=None,
        thesis=args.thesis, confidence=args.confidence, stop=None, target=None,
        horizon_days=None, spy_at_suggestion=quote(BENCHMARK)["price"],
        status="standalone", outcome=None,
    )
    save(SUGGESTIONS, sg)
    print(f"#{sid} {args.action.upper()} note recorded for {args.ticker.upper()}.")


def cmd_status(args):
    pf, _ = load_state()
    rows, total_value, total_cost = [], 0.0, 0.0
    for pos in pf["positions"]:
        q = quote(pos["ticker"])
        value = pos["shares"] * q["price"]
        cost = pos["shares"] * pos["avg_cost"]
        total_value += value
        total_cost += cost
        rows.append({
            "ticker": pos["ticker"] + ("\\*" if pos.get("imported") else ""),
            "shares": pos["shares"], "avg_cost": pos["avg_cost"],
            "price": q["price"], "day_pct": q["day_change_pct"], "value": value,
            "unreal_pct": 100 * (q["price"] / pos["avg_cost"] - 1),
            "stop": pos.get("stop"), "target": pos.get("target"), "opened": pos["opened"],
        })
    equity = pf["cash"] + total_value
    total_ret = 100 * (equity / pf["starting_cash"] - 1)
    spy = quote(pf["benchmark"]["ticker"])
    spy_ret = 100 * (spy["price"] / pf["benchmark"]["start_price"] - 1)

    print(f"# Portfolio status — {today()}\n")
    print(f"| Ticker | Shares | Avg cost | Price | Day % | Value | Unreal. % | Stop | Target |")
    print(f"|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        print(f"| {r['ticker']} | {r['shares']} | ${r['avg_cost']:,.2f} | ${r['price']:,.2f} "
              f"| {r['day_pct']:+.2f}% | ${r['value']:,.2f} | {r['unreal_pct']:+.2f}% "
              f"| {r['stop'] or '—'} | {r['target'] or '—'} |")
    if not rows:
        print("| (no positions) | | | | | | | | |")
    if any(p.get("imported") for p in pf["positions"]):
        print("\n\\* imported pre-existing holding; Unreal. % is vs the user's own cost basis")
    print(f"\n- Cash: ${pf['cash']:,.2f}")
    print(f"- Equity (cash + positions): ${equity:,.2f}")
    print(f"- Total return since {pf['created']}: {total_ret:+.2f}%")
    print(f"- {pf['benchmark']['ticker']} over same period: {spy_ret:+.2f}% "
          f"(started @ {pf['benchmark']['start_price']})")
    print(f"- Alpha vs benchmark: {total_ret - spy_ret:+.2f}%")


def cmd_history(args):
    _, sg = load_state()
    items = sg["suggestions"]
    if args.open:
        items = [s for s in items if s["status"] == "open"]
    print(f"# Suggestion history ({len(items)} records)\n")
    for s in items:
        line = (f"- #{s['id']} {s['date']} **{s['action'].upper()} {s['ticker']}** "
                f"@ ${s['price']:,.2f}")
        if s.get("confidence"):
            line += f" (conf: {s['confidence']})"
        line += f" — {s['thesis']}"
        print(line)
        if s.get("outcome") and s["action"] == "buy":
            o = s["outcome"]
            print(f"    → closed {o['closed_date']} @ ${o['close_price']:,.2f}: "
                  f"{o['return_pct']:+.2f}% vs SPY {o['spy_return_pct']:+.2f}% "
                  f"= alpha {o['alpha_pct']:+.2f}% ({o['grade']}) — {o['exit_reason']}")
            if o.get("lesson"):
                print(f"    → lesson: {o['lesson']}")
    closed = [s for s in sg["suggestions"]
              if s["action"] == "buy" and s["status"] == "closed" and s.get("outcome")]
    if closed:
        wins = [s for s in closed if s["outcome"]["grade"] == "win"]
        losses = [s for s in closed if s["outcome"]["grade"] == "loss"]
        avg_alpha = sum(s["outcome"]["alpha_pct"] for s in closed) / len(closed)
        print(f"\n## Calibration")
        print(f"- Closed buy calls: {len(closed)} | wins (beat SPY): {len(wins)} "
              f"| losses: {len(losses)} | hit rate: {100 * len(wins) / len(closed):.0f}%")
        print(f"- Average alpha per closed call: {avg_alpha:+.2f}%")
        if wins:
            print(f"- Avg winner alpha: {sum(s['outcome']['alpha_pct'] for s in wins) / len(wins):+.2f}%")
        if losses:
            print(f"- Avg loser alpha: {sum(s['outcome']['alpha_pct'] for s in losses) / len(losses):+.2f}%")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init")
    s.add_argument("--cash", type=float, required=True)
    s.add_argument("--force", action="store_true")
    s.set_defaults(fn=cmd_init)

    s = sub.add_parser("import")
    s.add_argument("ticker")
    s.add_argument("--shares", type=float, required=True)
    s.add_argument("--avg-cost", type=float, required=True)
    s.add_argument("--opened", help="YYYY-MM-DD the real position was opened, if known")
    s.set_defaults(fn=cmd_import)

    s = sub.add_parser("rebase")
    s.set_defaults(fn=cmd_rebase)

    s = sub.add_parser("buy")
    s.add_argument("ticker")
    s.add_argument("--dollars", type=float, required=True)
    s.add_argument("--thesis", required=True)
    s.add_argument("--price", type=float)
    s.add_argument("--confidence", choices=["high", "medium", "low"], default="medium")
    s.add_argument("--stop", type=float)
    s.add_argument("--target", type=float)
    s.add_argument("--horizon-days", type=int)
    s.set_defaults(fn=cmd_buy)

    s = sub.add_parser("sell")
    s.add_argument("ticker")
    s.add_argument("--reason", required=True)
    s.add_argument("--pct", type=float, default=100)
    s.add_argument("--price", type=float)
    s.set_defaults(fn=cmd_sell)

    s = sub.add_parser("note")
    s.add_argument("ticker")
    s.add_argument("--action", choices=["hold", "watch", "avoid"], required=True)
    s.add_argument("--thesis", required=True)
    s.add_argument("--price", type=float)
    s.add_argument("--confidence", choices=["high", "medium", "low"], default="medium")
    s.set_defaults(fn=cmd_note)

    s = sub.add_parser("status")
    s.set_defaults(fn=cmd_status)

    s = sub.add_parser("history")
    s.add_argument("--open", action="store_true")
    s.set_defaults(fn=cmd_history)

    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
