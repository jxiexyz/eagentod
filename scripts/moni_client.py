#!/usr/bin/env python3
"""
moni_client.py
Direct REST client for Moni API (api.moni.ai).
No authentication required. Public social intelligence, smart followers, and profile changes.
"""

import json
import sys
import time
import urllib.parse
import urllib.request
import urllib.error
from typing import Any, Dict, List, Optional

BASE_URL = "https://api.moni.ai/api/v1"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"


def req(endpoint: str, params: Optional[Dict[str, Any]] = None, timeout: int = 15) -> Dict[str, Any]:
    url = f"{BASE_URL}{endpoint}"
    if params:
        query_str = urllib.parse.urlencode(params)
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}{query_str}"

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    }
    request = urllib.request.Request(url, headers=headers)

    max_retries = 3
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as resp:
                raw_body = resp.read().decode("utf-8", errors="ignore")
                try:
                    return json.loads(raw_body)
                except Exception:
                    return {"error": "json_decode", "detail": raw_body[:200]}
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            body = e.read().decode("utf-8", errors="ignore")
            return {"error": f"HTTP {e.code}", "detail": body}
        except urllib.error.URLError as e:
            return {"error": str(e.reason)}
        except Exception as e:
            return {"error": str(e)}

    return {"error": "HTTP 429", "detail": "rate_limited"}


def get_account_info(handle: str, timeframe: str = "H24") -> Dict[str, Any]:
    clean = handle.lstrip("@").strip()
    if not clean:
        return {}
    res = req("/observed/", params={"twitterUsername": clean, "timeframe": timeframe})
    if "error" in res:
        return res
    soc = res.get("socialData")
    return soc if isinstance(soc, dict) else {}


def get_smart_followers(observed_id: int, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
    params = {
        "observedId": observed_id,
        "observedType": "twitter_account",
        "limit": limit,
        "offset": offset,
    }
    res = req("/observed/smart_followers/", params=params)
    if "error" in res:
        return res
    return res if isinstance(res, dict) else {}


def get_timeline(observed_id: int, limit: int = 20, types: Optional[str] = None) -> Dict[str, Any]:
    params: Dict[str, Any] = {
        "observedId": observed_id,
        "observedType": "twitter_account",
        "limit": limit,
    }
    if types:
        params["types"] = types
    res = req("/observed/timeline/", params=params)
    if "error" in res:
        return res
    return res if isinstance(res, dict) else {}


def resolve_username(handle: str) -> Dict[str, Any]:
    clean = handle.lstrip("@").strip()
    if not clean:
        return {}
    res = req(f"/observed/resolve/{clean}/")
    return res


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 moni_client.py [info|smart|timeline|resolve] <handle>")
        sys.exit(0)

    cmd = sys.argv[1].lower()
    target = sys.argv[2] if len(sys.argv) > 2 else ""

    if cmd == "info" and target:
        print(json.dumps(get_account_info(target), indent=2))
    elif cmd == "smart" and target:
        info = get_account_info(target)
        obs_id = info.get("observedId")
        if not obs_id:
            print(f"Error: Could not resolve observedId for @{target}")
            sys.exit(1)
        print(json.dumps(get_smart_followers(obs_id), indent=2))
    elif cmd == "timeline" and target:
        info = get_account_info(target)
        obs_id = info.get("observedId")
        if not obs_id:
            print(f"Error: Could not resolve observedId for @{target}")
            sys.exit(1)
        print(json.dumps(get_timeline(obs_id), indent=2))
    elif cmd == "resolve" and target:
        print(json.dumps(resolve_username(target), indent=2))
    else:
        print("Unknown command or missing target handle.")
