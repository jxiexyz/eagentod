#!/usr/bin/env python3
"""
post_eagent_report.py
Delivers Eagent execution reports to Telegram Topic via Bot API.
Configurable via environment variables or .env file.
"""
import os
import sys
import requests

def _load_env():
    for p in [os.path.expanduser("~/.hermes/.env"), ".env", os.path.join(os.path.dirname(__file__), "..", ".env")]:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip("'\"")
                        if k not in os.environ:
                            os.environ[k] = v

_load_env()

BOT_TOKEN = os.environ.get("EAGENT_BOT_TOKEN") or os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.environ.get("EAGENT_CHAT_ID") or os.environ.get("TELEGRAM_CHAT_ID", "")
TOPIC_ID = int(os.environ.get("EAGENT_TOPIC_ID") or os.environ.get("TELEGRAM_TOPIC_ID", "3602"))


def post_eagent(text: str) -> bool:
    if not BOT_TOKEN or not CHAT_ID:
        print("[!] EAGENT_BOT_TOKEN or EAGENT_CHAT_ID not configured. Skipping TG delivery.", file=sys.stderr)
        return False

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "message_thread_id": TOPIC_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    try:
        res = requests.post(url, json=payload, timeout=15)
        data = res.json()
        if res.status_code == 200 and data.get("ok"):
            print(f"[+] Eagent report delivered to Topic {TOPIC_ID} (msg_id: {data['result']['message_id']})")
            return True
        print(f"[-] Bot API error ({res.status_code}): {res.text}")
        return False
    except Exception as e:
        print(f"[-] Bot API exception: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        post_eagent(sys.argv[1])
    else:
        print("Usage: python3 post_eagent_report.py '<html_message>'")
