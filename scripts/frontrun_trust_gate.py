#!/usr/bin/env python3
"""
frontrun_trust_gate.py
Frontrun Pro trust validation layer for eagent-scanner candidates.
Validates: username history (no rebrands), smart follower count (min 5).
Returns enriched candidate data with wallet addresses for auto-reply.
"""

import sys
import os
import json
import time

sys.path.insert(0, "/home/ubuntu/.hermes/scripts")
import frontrun_client

# ponytail: cache TTL 1h per handle, upgrade to sqlite if >500 entries
CACHE_PATH = "/home/ubuntu/.hermes/scripts/frontrun_trust_cache.json"
CACHE_TTL = 3600  # 1 hour

MIN_SMART_FOLLOWERS = 5
MAX_USERNAME_CHANGES = 0  # zero tolerance for rebrands


def _load_cache():
    try:
        with open(CACHE_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_cache(cache):
    try:
        with open(CACHE_PATH, "w") as f:
            json.dump(cache, f, separators=(",", ":"))
    except Exception:
        pass


def validate_handle(handle: str) -> dict:
    """
    Validate a Twitter handle via Frontrun Pro.
    Returns:
        {
            "trusted": bool,
            "reject_reason": str or None,
            "smart_follower_count": int,
            "smart_followers": [str, ...],
            "username_changes": int,
            "old_usernames": [str, ...],
            "wallets": {"EVM": str, "SOL": str, ...},
            "cached": bool,
        }
    """
    clean = handle.lstrip("@").strip().lower()
    if not clean:
        return {"trusted": False, "reject_reason": "empty_handle"}

    # Check cache first
    cache = _load_cache()
    cached = cache.get(clean)
    if cached and time.time() - cached.get("ts", 0) < CACHE_TTL:
        return {**cached["result"], "cached": True}

    result = {
        "trusted": False,
        "reject_reason": None,
        "smart_follower_count": 0,
        "smart_followers": [],
        "username_changes": 0,
        "old_usernames": [],
        "wallets": {},
        "cached": False,
    }

    # 1. Username history check (rebrand detection)
    try:
        history = frontrun_client.get_username_history(clean)
        result["username_changes"] = len(history)
        result["old_usernames"] = [h.get("oldTwitterUsername", "") for h in history]
        if len(history) > MAX_USERNAME_CHANGES:
            old_names = ", ".join(result["old_usernames"][:3])
            result["reject_reason"] = f"rebrand:{old_names}"
            _cache_result(cache, clean, result)
            return result
    except Exception as e:
        # Non-fatal: proceed without history check
        print(f"WARN: username_history failed for @{clean}: {e}", file=sys.stderr)

    # 2. Smart follower check
    try:
        sf = frontrun_client.get_smart_followers(clean)
        result["smart_follower_count"] = len(sf)
        result["smart_followers"] = [
            s.get("twitter", s.get("name", "")) for s in sf[:10]
        ]
        if len(sf) < MIN_SMART_FOLLOWERS:
            result["reject_reason"] = f"low_smart_followers:{len(sf)}/{MIN_SMART_FOLLOWERS}"
            _cache_result(cache, clean, result)
            return result
    except Exception as e:
        print(f"WARN: smart_followers failed for @{clean}: {e}", file=sys.stderr)
        result["reject_reason"] = f"smart_followers_error:{e}"
        _cache_result(cache, clean, result)
        return result

    # 3. Wallet detection (bonus: auto-detect chain for reply drops)
    try:
        wallets = frontrun_client.get_wallets(clean)
        for w in wallets:
            chain = w.get("chain", "").upper()
            addr = w.get("address", "")
            if chain and addr and chain not in result["wallets"]:
                result["wallets"][chain] = addr
    except Exception:
        pass  # non-fatal

    # All checks passed
    result["trusted"] = True
    _cache_result(cache, clean, result)
    return result


def _cache_result(cache, handle, result):
    cache[handle] = {"ts": time.time(), "result": {k: v for k, v in result.items() if k != "cached"}}
    # Evict old entries
    if len(cache) > 500:
        sorted_keys = sorted(cache, key=lambda k: cache[k].get("ts", 0))
        for k in sorted_keys[:100]:
            del cache[k]
    _save_cache(cache)


def batch_validate(handles: list) -> dict:
    """Validate multiple handles. Returns {handle: result}."""
    results = {}
    for h in handles:
        results[h] = validate_handle(h)
        time.sleep(0.3)  # Rate limit courtesy
    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 frontrun_trust_gate.py <handle> [handle2 ...]")
        sys.exit(0)

    handles = sys.argv[1:]
    for h in handles:
        r = validate_handle(h)
        status = "✅ TRUSTED" if r["trusted"] else f"❌ REJECTED ({r['reject_reason']})"
        print(f"@{h.lstrip('@')}: {status}")
        print(f"  Smart followers: {r['smart_follower_count']} {r['smart_followers'][:5]}")
        if r["old_usernames"]:
            print(f"  Old usernames: {r['old_usernames']}")
        if r["wallets"]:
            print(f"  Wallets: {r['wallets']}")
        print()
