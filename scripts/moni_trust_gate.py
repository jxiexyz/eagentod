#!/usr/bin/env python3
"""
moni_trust_gate.py
Moni API trust validation layer for eagent-scanner candidates.
Validates:
- Project (<1k followers): min 3 smart followers, 0 username changes
- Project (>=1k followers): min 5 smart followers, 0 username changes
- CT Giveaway (KOL/person/giveaway tweet): min 100 smart followers, max 1 username change
Returns enriched candidate data with smart followers.
"""

import sys
import os
import json
import time
from typing import Dict, Any, List, Optional, Tuple

sys.path.insert(0, "/home/ubuntu/.hermes/scripts")
import moni_client

CACHE_PATH = "/home/ubuntu/.hermes/scripts/moni_trust_cache.json"
CACHE_TTL = 3600  # 1 hour

MIN_SMART_FOLLOWERS_PROJECT_LOW_FOL = 3
MIN_SMART_FOLLOWERS_PROJECT = 5
MAX_USERNAME_CHANGES_PROJECT = 0

MIN_SMART_FOLLOWERS_CT_GIVEAWAY = 100
MAX_USERNAME_CHANGES_CT_GIVEAWAY = 1

# Backward-compat defaults
MIN_SMART_FOLLOWERS = MIN_SMART_FOLLOWERS_PROJECT
MAX_USERNAME_CHANGES = MAX_USERNAME_CHANGES_PROJECT


def _load_cache() -> Dict[str, Any]:
    try:
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_cache(cache: Dict[str, Any]) -> None:
    try:
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(cache, f, separators=(",", ":"))
    except Exception:
        pass


def _cache_result(cache: Dict[str, Any], handle: str, result: Dict[str, Any]) -> None:
    cache[handle] = {"ts": time.time(), "result": {k: v for k, v in result.items() if k != "cached"}}
    if len(cache) > 500:
        sorted_keys = sorted(cache, key=lambda k: cache[k].get("ts", 0))
        for k in sorted_keys[:100]:
            del cache[k]
    _save_cache(cache)


def resolve_thresholds(
    min_smart_followers: Optional[int] = None,
    max_username_changes: Optional[int] = None,
    followers: Optional[int] = None,
    is_project: bool = True,
    is_ct_giveaway: bool = False,
) -> Tuple[int, int]:
    """Resolve (min_smart_followers, max_username_changes) based on account type."""
    if is_ct_giveaway:
        target_sf = MIN_SMART_FOLLOWERS_CT_GIVEAWAY if min_smart_followers is None else min_smart_followers
        target_changes = MAX_USERNAME_CHANGES_CT_GIVEAWAY if max_username_changes is None else max_username_changes
    elif is_project:
        if followers is not None and 0 <= followers < 1000:
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
    min_smart_followers: Optional[int] = None,
    max_username_changes: Optional[int] = None,
    followers: Optional[int] = None,
    is_project: bool = True,
    is_ct_giveaway: bool = False,
) -> Dict[str, Any]:
    """
    Validate a Twitter handle via Moni API.
    Returns:
        {
            "trusted": bool,
            "reject_reason": str or None,
            "smart_follower_count": int,
            "smart_followers": [str, ...],
            "username_changes": int,
            "old_usernames": [str, ...],
            "wallets": {},
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
        raw_res = cached.get("result", {})
        cached_followers = raw_res.get("followers", followers)
        eff_followers = followers if followers is not None else cached_followers
        target_min_sf, target_max_changes = resolve_thresholds(
            min_smart_followers=min_smart_followers,
            max_username_changes=max_username_changes,
            followers=eff_followers,
            is_project=is_project,
            is_ct_giveaway=is_ct_giveaway,
        )

        sf_count = raw_res.get("smart_follower_count", 0)
        history_len = raw_res.get("username_changes", 0)
        old_names = raw_res.get("old_usernames", [])

        trusted = True
        reject_reason = None
        if history_len > target_max_changes:
            old_str = ", ".join(old_names[:3]) if old_names else "rebrand"
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

    # Fetch from Moni
    try:
        info = moni_client.get_account_info(clean)
        if "error" in info:
            raise RuntimeError(info.get("error"))
    except Exception as e:
        print(f"WARN: Moni get_account_info failed for @{clean}: {e}", file=sys.stderr)
        # Fail-open: allow candidate through on Moni errors
        return {
            "trusted": True,
            "reject_reason": f"moni_error:{e}",
            "smart_follower_count": 0,
            "smart_followers": [],
            "username_changes": 0,
            "old_usernames": [],
            "wallets": {},
            "cached": False,
        }

    # Follower count fallback from Moni if not provided
    moni_followers = info.get("followersCount")
    eff_followers = followers if followers is not None else moni_followers

    # Resolve thresholds
    target_min_sf, target_max_changes = resolve_thresholds(
        min_smart_followers=min_smart_followers,
        max_username_changes=max_username_changes,
        followers=eff_followers,
        is_project=is_project,
        is_ct_giveaway=is_ct_giveaway,
    )

    sf_count = info.get("smartFollowersCount", 0) or 0
    username_changes = info.get("usernameChangeCount", 0) or 0
    raw_changes = info.get("usernameChanges") or []
    old_usernames = [
        c.get("oldUsername") or c.get("newUsername") or ""
        for c in raw_changes
        if isinstance(c, dict) and (c.get("oldUsername") or c.get("newUsername"))
    ]

    trusted = True
    reject_reason = None

    if username_changes > target_max_changes:
        old_str = ", ".join(old_usernames[:3]) if old_usernames else "rebrand"
        reject_reason = f"rebrand:{old_str}"
        trusted = False
    elif sf_count < target_min_sf:
        reject_reason = f"low_smart_followers:{sf_count}/{target_min_sf}"
        trusted = False

    smart_followers = []
    # Only fetch smart followers list if trusted and observedId present
    if trusted and info.get("observedId"):
        try:
            sf_res = moni_client.get_smart_followers(info["observedId"], limit=10)
            items = sf_res.get("items", []) if isinstance(sf_res, dict) else []
            smart_followers = [
                item.get("username") for item in items if isinstance(item, dict) and item.get("username")
            ]
        except Exception as e:
            print(f"WARN: get_smart_followers failed for @{clean}: {e}", file=sys.stderr)

    result = {
        "trusted": trusted,
        "reject_reason": reject_reason,
        "smart_follower_count": sf_count,
        "smart_followers": smart_followers,
        "username_changes": username_changes,
        "old_usernames": old_usernames,
        "wallets": {},
        "cached": False,
        "followers": moni_followers,
    }

    _cache_result(cache, clean, result)
    return result


def batch_validate(handles: List[str], **kwargs) -> Dict[str, Dict[str, Any]]:
    """Validate multiple handles. Returns {handle: result}."""
    results = {}
    for h in handles:
        results[h] = validate_handle(h, **kwargs)
        time.sleep(0.3)
    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 moni_trust_gate.py <handle> [handle2 ...]")
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
