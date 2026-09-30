#!/usr/bin/env python3
"""
frontrun_client.py
Direct REST client for Frontrun Pro API using dumped session cookies.
Provides Twitter intelligence & trending smart-follower accounts without browser.
"""

import json
import os
import sys
import urllib.request
import urllib.parse
from typing import Any, Dict, List, Optional

COOKIE_PATH = os.path.expanduser("~/.hermes/frontrun_cookies.json")
BASE_URL = "https://loadbalance.frontrun.pro"


def load_cookie_header() -> str:
    if not os.path.exists(COOKIE_PATH):
        return ""
    try:
        with open(COOKIE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return "; ".join([f"{c['name']}={c['value']}" for c in data])
    except Exception:
        return ""


def req(endpoint: str, timeout: int = 15) -> Dict[str, Any]:
    url = f"{BASE_URL}{endpoint}"
    cookie_str = load_cookie_header()
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "X-Copilot-Client-Version": "0.0.415",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    if cookie_str:
        headers["Cookie"] = cookie_str

    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")
        return {"error": f"HTTP {e.code}", "detail": body}
    except Exception as e:
        return {"error": str(e)}


def get_trending_accounts(window: str = "24h") -> List[Dict[str, Any]]:
    res = req(f"/api/v1/openbits/trending-accounts?window={window}")
    return res.get("data", {}).get("accounts", [])


def get_twitter_info(handle: str) -> Dict[str, Any]:
    clean_handle = handle.lstrip("@").strip()
    res = req(f"/api/v4/twitter/{clean_handle}/info")
    return res.get("data", {})


def get_smart_followers(handle: str) -> List[Dict[str, Any]]:
    clean_handle = handle.lstrip("@").strip()
    res = req(f"/api/v1/twitter/{clean_handle}/smart-followers")
    if "error" in res:
        raise RuntimeError(f"Frontrun API error: {res.get('error')} - {res.get('detail')}")
    return res.get("data", {}).get("smartFollowers", [])


def get_username_history(handle: str) -> List[Dict[str, Any]]:
    clean_handle = handle.lstrip("@").strip()
    res = req(f"/api/v1/twitter/{clean_handle}/username-history")
    if "error" in res:
        raise RuntimeError(f"Frontrun API error: {res.get('error')} - {res.get('detail')}")
    return res.get("data", {}).get("usernameHistory", [])


def get_wallets(handle: str) -> List[Dict[str, Any]]:
    clean_handle = handle.lstrip("@").strip()
    res = req(f"/api/v4/twitter/{clean_handle}/wallets")
    if "error" in res:
        raise RuntimeError(f"Frontrun API error: {res.get('error')} - {res.get('detail')}")
    return res.get("data", {}).get("wallets", [])


def get_credit_status() -> Dict[str, Any]:
    res = req("/api/v1/user/credit-status")
    return res.get("data", {})


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 frontrun_client.py [trending|info|smart|history|wallets|credit] [handle]")
        sys.exit(0)

    cmd = sys.argv[1].lower()
    if cmd == "trending":
        win = sys.argv[2] if len(sys.argv) > 2 else "24h"
        accs = get_trending_accounts(win)
        print(f"Top {len(accs)} Trending Accounts ({win}):")
        for a in accs[:10]:
            print(f"- @{a.get('handle')}: +{a.get('smartFollowerGainCount')} smart followers | {a.get('officialLabel') or a.get('category')} | {a.get('displayName')}")
    elif cmd == "info" and len(sys.argv) > 2:
        print(json.dumps(get_twitter_info(sys.argv[2]), indent=2))
    elif cmd == "smart" and len(sys.argv) > 2:
        print(json.dumps(get_smart_followers(sys.argv[2]), indent=2))
    elif cmd == "history" and len(sys.argv) > 2:
        print(json.dumps(get_username_history(sys.argv[2]), indent=2))
    elif cmd == "wallets" and len(sys.argv) > 2:
        print(json.dumps(get_wallets(sys.argv[2]), indent=2))
    elif cmd == "credit":
        print(json.dumps(get_credit_status(), indent=2))
    else:
        print("Unknown command or missing handle argument.")
