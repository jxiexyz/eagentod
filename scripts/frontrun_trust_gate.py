#!/usr/bin/env python3
"""
frontrun_trust_gate.py
Frontrun Pro trust validation layer for eagent-scanner candidates.
Validates:
- Project (<1k followers): min 3 smart followers, 0 username changes
- Project (>=1k followers): min 5 smart followers, 0 username changes
- CT Giveaway (KOL/person/giveaway tweet): min 100 smart followers, max 1 username change
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

MIN_SMART_FOLLOWERS_PROJECT_LOW_FOL = 3
MIN_SMART_FOLLOWERS_PROJECT = 5
MAX_USERNAME_CHANGES_PROJECT = 0

MIN_SMART_FOLLOWERS_CT_GIVEAWAY = 100
MAX_USERNAME_CHANGES_CT_GIVEAWAY = 1

# Backward-compat defaults
MIN_SMART_FOLLOWERS = MIN_SMART_FOLLOWERS_PROJECT
MAX_USERNAME_CHANGES = MAX_USERNAME_CHANGES_PROJECT


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


def resolve_thresholds(
    min_smart_followers: int = None,
    max_username_changes: int = None,
    followers: int = 0,
    is_project: bool = True,
    is_ct_giveaway: bool = False,
) -> tuple:
    """Resolve (min_smart_followers, max_username_changes) based on account type."""
    if is_ct_giveaway:
        target_sf = MIN_SMART_FOLLOWERS_CT_GIVEAWAY if min_smart_followers is None else min_smart_followers
        target_changes = MAX_USERNAME_CHANGES_CT_GIVEAWAY if max_username_changes is None else max_username_changes
    elif is_project:
        if 0 < followers < 1000:
            target_sf = MIN_SMART_FOLLOWERS_PROJECT_LOW_FOL if min_smart_followers is None else min_smart_followers
        else:
            target_sf = MIN_SMART_FOLLOWERS_PROJECT if min_smart_followers is None else min_smart_followers
        target_changes = MAX_USERNAME_CHANGES_PROJECT if max_username_changes is None else max_username_changes
    else:
        target_sf = MIN_SMART_FOLLOWERS if min_smart_followers is None else min_smart_followers
        target_changes = MAX_USERNAME_CHANGES if max_username_changes is None else max_username_changes

    return target_sf, target_changes


def validate_handle(
    handle: str,
    min_smart_followers: int = None,
    max_username_changes: int = None,
    followers: int = 0,
    is_project: bool = True,
    is_ct_giveaway: bool = False,
) -> dict:
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

    target_min_sf, target_max_changes = resolve_thresholds(
        min_smart_followers=min_smart_followers,
        max_username_changes=max_username_changes,
        followers=followers,
        is_project=is_project,
        is_ct_giveaway=is_ct_giveaway,
    )

    # Check cache first
    cache = _load_cache()
    cached = cache.get(clean)
    if cached and time.time() - cached.get("ts", 0) < CACHE_TTL:
        raw_res = cached.get("result", {})
        sf_count = raw_res.get("smart_follower_count", 0)
        history_len = raw_res.get("username_changes", 0)
        old_names = raw_res.get("old_usernames", [])

        trusted = True
        reject_reason = None
        if history_len > target_max_changes:
            old_str = ", ".join(old_names[:3])
            reject_reason = f"rebrand:{old_str}"
            trusted = False
        elif sf_count < target_min_sf:
            reject_reason = f"low_smart_followers:{sf_count}/{target_min_sf}"
            trusted = False

        return {
            **raw_res,
            "trusted": trusted,
            "reject_reason": reject_reason,
            "cached": True,
        }

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
    except Exception as e:
        print(f"WARN: username_history failed for @{clean}: {e}", file=sys.stderr)

    # 2. Smart follower check
    sf_error = None
    try:
        sf = frontrun_client.get_smart_followers(clean)
        result["smart_follower_count"] = len(sf)
        result["smart_followers"] = [
            s.get("twitter", s.get("name", "")) for s in sf[:10]
        ]
    except Exception as e:
        print(f"WARN: smart_followers failed for @{clean}: {e}", file=sys.stderr)
        sf_error = e

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

    # Evaluate thresholds
    if sf_error is not None:
        result["reject_reason"] = f"smart_followers_error:{sf_error}"
        result["trusted"] = False
    elif result["username_changes"] > target_max_changes:
        old_names = ", ".join(result["old_usernames"][:3])
        result["reject_reason"] = f"rebrand:{old_names}"
        result["trusted"] = False
    elif result["smart_follower_count"] < target_min_sf:
        result["reject_reason"] = f"low_smart_followers:{result['smart_follower_count']}/{target_min_sf}"
        result["trusted"] = False
    else:
        result["trusted"] = True
        result["reject_reason"] = None

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


def batch_validate(handles: list, **kwargs) -> dict:
    """Validate multiple handles. Returns {handle: result}."""
    results = {}
    for h in handles:
        results[h] = validate_handle(h, **kwargs)
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
