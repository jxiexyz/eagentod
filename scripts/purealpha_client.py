"""
purealpha_client.py
Helper module to scrape signals from purealpha.app using stored session cookies or CDP session.
"""

import json
import os
import re
import urllib.request
from typing import Any, Dict, List, Optional

COOKIE_PATH = os.path.expanduser("~/.hermes/purealpha_cookies.json")


def load_cookies() -> str:
    """Load cookie string from local json."""
    if not os.path.exists(COOKIE_PATH):
        return ""
    with open(COOKIE_PATH, "r", encoding="utf-8") as f:
        cookies = json.load(f)
    return "; ".join([f"{c['name']}={c['value']}" for c in cookies])


def fetch_feed(
    feed: str = "hot",
    window: str = "24h",
    acc_type: str = "projects",
    follower_cap: int = 25000,
) -> Dict[str, Any]:
    """
    Fetch and parse PureAlpha feed.
    
    Args:
        feed: 'hot' or 'new'
        window: '10m', '1h', '3h', '12h', '24h', '7d'
        acc_type: 'projects' or 'people'
        follower_cap: follower ceiling (e.g. 25000, 1000)
    """
    cookie_header = load_cookies()
    url = f"https://purealpha.app/?feed={feed}&window={window}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    if cookie_header:
        headers["Cookie"] = cookie_header

    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        html = resp.read().decode("utf-8")

    # Extract Next.js RSC chunks
    pushes = re.findall(r"self\.__next_f\.push\(\[1,\"(.*?)\"\]\)", html, re.DOTALL)
    full_rsc = "".join(pushes).encode("utf-8").decode("unicode-escape")

    # Parse identity
    identity = {}
    m_id = re.search(r"\"initialIdentity\":(\{.*?\})", full_rsc)
    if m_id:
        try:
            identity = json.loads(m_id.group(1))
        except Exception:
            pass

    # Parse rows
    rows: List[Dict[str, Any]] = []
    # If logged in, rows is in "rows": [...]
    m_rows = re.search(r"\"rows\":(\[.*?\]),\"available\"", full_rsc)
    if m_rows:
        try:
            rows = json.loads(m_rows.group(1))
        except Exception:
            pass
    
    # If guest or fallback, look for previewRows
    if not rows:
        m_prev = re.search(r"\"previewRows\":(\[.*?\]),\"view\"", full_rsc)
        if m_prev:
            try:
                rows = json.loads(m_prev.group(1))
            except Exception:
                pass

    return {
        "identity": identity,
        "feed": feed,
        "window": window,
        "count": len(rows),
        "data": rows,
    }


if __name__ == "__main__":
    result = fetch_feed(feed="hot", window="24h")
    print(f"Logged in as: {result['identity'].get('member', {}).get('xUsername', 'Guest')}")
    print(f"Total entries: {result['count']}")
    for i, item in enumerate(result["data"][:10], 1):
        handle = item.get("handle")
        name = item.get("name")
        followers = item.get("fol")
        hot_count = item.get("hotCount")
        print(f"{i}. @{handle} ({name}) - Followers: {followers} | Hot Signals: {hot_count}")
