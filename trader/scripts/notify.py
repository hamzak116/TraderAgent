#!/usr/bin/env python3
"""Send a message to the user's Telegram via a bot. Stdlib only.

Credentials are read from environment variables, falling back to a
`trader/.env` file (which is gitignored — never commit the token):

    TELEGRAM_BOT_TOKEN=123456:ABC-...
    TELEGRAM_CHAT_ID=987654321

Usage:
    python3 notify.py "Your message here"     # message as argument
    echo "Your message" | python3 notify.py   # message on stdin
    python3 notify.py --check                  # verify credentials work

Designed to never crash a routine: if credentials are missing or the send
fails, it prints a warning to stderr and exits non-zero, but the caller
(sync/routine) treats notification as best-effort.
"""
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
TELEGRAM_MAX = 4096


def load_env():
    """Populate os.environ from trader/.env for any keys not already set."""
    if not ENV_FILE.exists():
        return
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key, val = key.strip(), val.strip().strip('"').strip("'")
        os.environ.setdefault(key, val)


def creds():
    load_env()
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        sys.exit(
            "notify: missing TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID "
            f"(set them in env or {ENV_FILE}). See trader/.env.example."
        )
    return token, chat_id


def send(text: str) -> dict:
    token, chat_id = creds()
    if len(text) > TELEGRAM_MAX:
        text = text[: TELEGRAM_MAX - 40].rstrip() + "\n…(truncated — see full report on GitHub)"
    data = urllib.parse.urlencode(
        {"chat_id": chat_id, "text": text, "parse_mode": "Markdown",
         "disable_web_page_preview": "true"}
    ).encode()
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.load(resp)


def check():
    token, chat_id = creds()
    url = f"https://api.telegram.org/bot{token}/getMe"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            me = json.load(resp)
        bot = me.get("result", {}).get("username", "?")
        print(f"notify: token OK (bot @{bot}), chat_id={chat_id}. Sending test message…")
        send("✅ trading-agent notifications are wired up. You'll get daily briefs here.")
        print("notify: test message sent — check your Telegram.")
    except Exception as e:  # noqa: BLE001
        sys.exit(f"notify: credential check failed: {e}")


def main(argv):
    if argv and argv[0] == "--check":
        return check()
    text = " ".join(argv) if argv else sys.stdin.read()
    text = text.strip()
    if not text:
        sys.exit("notify: empty message")
    try:
        result = send(text)
        if not result.get("ok"):
            sys.exit(f"notify: Telegram API error: {result}")
        print("notify: sent.")
    except Exception as e:  # noqa: BLE001
        sys.exit(f"notify: send failed: {e}")


if __name__ == "__main__":
    main(sys.argv[1:])
