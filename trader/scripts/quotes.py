#!/usr/bin/env python3
"""Fetch stock quotes. Stdlib only.

Two providers, auto-selected:
  - Finnhub   (if FINNHUB_API_KEY is set) — works from datacenter IPs, so it's
    the cloud-routine source. Read from env or trader/.env.
  - Yahoo     (no key) — default for local runs; Yahoo 403s datacenter IPs.

`quote()` tries the preferred provider first and falls back to the other, so
the same script works locally (Yahoo) and in the cloud (Finnhub) unchanged.

Usage:
    python3 quotes.py AAPL MSFT SPY            # current/latest prices as JSON
    python3 quotes.py --history 30 AAPL        # last N daily closes for one ticker
"""
import json
import os
import sys
import urllib.request
from pathlib import Path

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
_ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


def _finnhub_key():
    key = os.environ.get("FINNHUB_API_KEY")
    if not key and _ENV_FILE.exists():
        for line in _ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line.startswith("FINNHUB_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
                break
    return key or None


def _get_json(url: str, headers=None) -> dict:
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.load(resp)


# ---- Yahoo ----------------------------------------------------------------

def fetch_chart(ticker: str, range_: str = "5d", interval: str = "1d") -> dict:
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        f"?range={range_}&interval={interval}"
    )
    return _get_json(url, UA)


def _quote_yahoo(ticker: str) -> dict:
    data = fetch_chart(ticker)
    result = data["chart"]["result"][0]
    meta = result["meta"]
    price = meta["regularMarketPrice"]
    prev = meta.get("regularMarketPreviousClose") or meta.get("previousClose")
    if not prev:
        closes = [c for c in result["indicators"]["quote"][0].get("close", []) if c is not None]
        if len(closes) >= 2:
            prev = closes[-2] if abs(closes[-1] - price) < 0.01 else closes[-1]
    return {
        "ticker": ticker.upper(),
        "price": round(price, 4),
        "previous_close": round(prev, 4) if prev else None,
        "currency": meta.get("currency"),
        "market_state": meta.get("marketState", "UNKNOWN"),
        "day_change_pct": round(100 * (price / prev - 1), 2) if prev else None,
        "52wk_high": meta.get("fiftyTwoWeekHigh"),
        "52wk_low": meta.get("fiftyTwoWeekLow"),
        "volume": meta.get("regularMarketVolume"),
        "source": "yahoo",
    }


# ---- Finnhub --------------------------------------------------------------

def _quote_finnhub(ticker: str, key: str) -> dict:
    # https://finnhub.io/docs/api/quote — c=current, pc=previous close, dp=% change
    d = _get_json(f"https://finnhub.io/api/v1/quote?symbol={ticker.upper()}&token={key}")
    price = d.get("c")
    if not price:  # unknown symbol or rate-limited returns zeros
        raise ValueError(f"finnhub returned no price for {ticker} ({d})")
    prev = d.get("pc")
    return {
        "ticker": ticker.upper(),
        "price": round(price, 4),
        "previous_close": round(prev, 4) if prev else None,
        "currency": "USD",
        "market_state": "UNKNOWN",
        "day_change_pct": round(d["dp"], 2) if d.get("dp") is not None
        else (round(100 * (price / prev - 1), 2) if prev else None),
        "52wk_high": d.get("h"),   # session high (Finnhub free has no 52wk in /quote)
        "52wk_low": d.get("l"),
        "volume": None,
        "source": "finnhub",
    }


def quote(ticker: str) -> dict:
    """Preferred provider first, the other as fallback."""
    key = _finnhub_key()
    providers = []
    if key:
        providers = [lambda t: _quote_finnhub(t, key), _quote_yahoo]
    else:
        providers = [_quote_yahoo, lambda t: _quote_finnhub(t, key) if key else (_ for _ in ()).throw(RuntimeError("no finnhub key"))]
    last_err = None
    for fn in providers:
        try:
            return fn(ticker)
        except Exception as e:  # noqa: BLE001 - try next provider
            last_err = e
    raise RuntimeError(f"all quote providers failed for {ticker}: {last_err}")


def history(ticker: str, days: int) -> dict:
    """Daily closes via Yahoo. Finnhub's free tier has no candles, so when
    Yahoo is unreachable (e.g. the cloud sandbox) this degrades to an empty
    series with a note rather than crashing the routine."""
    try:
        data = fetch_chart(ticker, range_=f"{days}d")
        result = data["chart"]["result"][0]
        timestamps = result.get("timestamp", [])
        closes = result["indicators"]["quote"][0].get("close", [])
        from datetime import datetime, timezone

        rows = [
            {"date": datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d"), "close": round(c, 4)}
            for ts, c in zip(timestamps, closes)
            if c is not None
        ]
        return {"ticker": ticker.upper(), "history": rows, "source": "yahoo"}
    except Exception as e:  # noqa: BLE001 - history is non-critical; degrade
        return {"ticker": ticker.upper(), "history": [], "unavailable": str(e),
                "note": "history feed unavailable (Yahoo blocked); use live quotes for trend"}


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__, file=sys.stderr)
        return 1
    if argv[0] == "--history":
        days, ticker = int(argv[1]), argv[2]
        print(json.dumps(history(ticker, days), indent=2))
        return 0
    out = []
    errors = []
    for t in argv:
        try:
            out.append(quote(t))
        except Exception as e:  # noqa: BLE001 - report per-ticker failures
            errors.append({"ticker": t.upper(), "error": str(e)})
    print(json.dumps({"quotes": out, "errors": errors}, indent=2))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
