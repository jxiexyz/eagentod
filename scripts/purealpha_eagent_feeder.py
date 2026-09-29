#!/usr/bin/env python3
"""
purealpha_eagent_feeder.py
Pre-filter PureAlpha feed for eagent-scanner cron.
Outputs actionable tasks (WL/form/drop address/GTD/free) for LLM agent to execute.
"""

import sys
import os
import json
import re
import time
import subprocess
import urllib.request

sys.path.insert(0, "/home/ubuntu/purealpha")
sys.path.insert(0, "/home/ubuntu/.hermes/scripts")
from purealpha_client import fetch_feed

STATE_FILE = "/home/ubuntu/.hermes/scripts/eagent_state.json"
QUEUE_FILE = os.environ.get("EAGENT_QUEUE_FILE", "/home/ubuntu/.hermes/scripts/eagent_queue.json")
EAGENT_QUEUE_FILE = QUEUE_FILE  # alias
MAX_PER_CYCLE = 3
RETTIWT_ENV = os.path.expanduser("~/.hermes/.env_rettiwt")


def load_json(path, default=None):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return default if default is not None else []


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


# Actionable keywords — case insensitive match against bio + tweets
# HARAM: Cuma "testnet", "early access", "faucet", "sign up", "apply now" tanpa ada form/WL/GTD/mint/drop
ACTIONABLE_KEYWORDS = [
    "drop address", "drop your address", "drop wallet", "drop your wallet",
    "leave address", "leave your address", "leave wallet",
    "paste your", "paste address", "paste wallet",
    "comment your", "comment address", "comment wallet",
    "reply with your", "reply your address", "reply wallet",
    "whitelist", "wl open", "wl spot", "wl giveaway",
    "waitlist",
    "gtd", "guaranteed", "gtd wl", "gtd spot", "gtd spots", "gtd giveaway",
    "fcfs wl", "allowlist",
    "free mint", "freemint", "free to mint", "free drop", "free nft", "freemint nft",
    "gtd mint", "wl mint", "whitelist mint", "nft whitelist", "nft wl",
    "google form", "typeform", "tally", "forms.gle", "premint",
    "zec nft", "zcash nft", "zeckers", "zecfrogs", "zecbit",
    "arc whitelist", "arc nft",
]

# URL patterns that indicate actionable forms/portals
FORM_URL_PATTERNS = [
    r"forms\.gle/",
    r"docs\.google\.com/forms/",
    r"\.typeform\.com/",
    r"tally\.so/",
    r"subber\.xyz/",
    r"premint\.xyz/",
    r"alphabot\.app/",
    r"heyform\.net/",
    r"/whitelist",
    r"/waitlist",
    r"/register",
]


def load_eagent_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {"processed_users": [], "processed_domains": [], "processed_tweet_ids": []}


def is_already_processed(handle, state):
    return handle.lower() in [u.lower() for u in state.get("processed_users", [])]


def match_actionable(text):
    """Check if text contains actionable keywords. Returns list of matched keywords."""
    text_lower = text.lower()
    return [kw for kw in ACTIONABLE_KEYWORDS if kw in text_lower]


def has_form_url(text):
    """Check if text contains known form/portal URL patterns."""
    return any(re.search(pat, text, re.I) for pat in FORM_URL_PATTERNS)


def _get_rettiwt_key():
    key = os.environ.get("API_KEY", "") or os.environ.get("RETTIWT_API_KEY", "")
    if not key and os.path.exists(RETTIWT_ENV):
        with open(RETTIWT_ENV) as f:
            for line in f:
                if line.startswith("API_KEY=") or line.startswith("RETTIWT_API_KEY="):
                    key = line.strip().split("=", 1)[1]
                    break
    if not key:
        alt_key_path = "/home/ubuntu/hermesfull/scripts/.rettiwt_key"
        if os.path.exists(alt_key_path):
            with open(alt_key_path) as f:
                key = f.read().strip()
    return key


def fetch_recent_tweets(handle, user_id=None, count=5):
    """Fetch recent tweets from a user via x_native. Returns list of tweet texts."""
    try:
        import x_native
        res = x_native.user_timeline_tweets(user_id or handle, count=count)
        return [t.get("fullText", "") for t in res.get("list", []) if t.get("fullText")]
    except Exception:
        return []


def fetch_985_candidates():
    """Fetch raw candidate targets from 985monitor.xyz (new smart followers + new arrivals)."""
    candidates = []
    # 1. 985 twitter live stream
    try:
        req = urllib.request.Request(
            "https://985monitor.xyz/api/twitter-live-events?limit=500",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            for e in data.get("events", []):
                ev_type = e.get("eventType")
                if ev_type == "NEW_FOLLOWER":
                    c = e.get("content")
                    entries = c if isinstance(c, list) else (c.get("entries", []) if isinstance(c, dict) else [])
                    for entry in entries:
                        h = entry.get("twAccount")
                        if not h:
                            continue
                        fol = entry.get("followerCount") or 0
                        kols_raw = entry.get("kols") or "{}"
                        kol_count = 0
                        smart_followers = []
                        if e.get("twAccount"):
                            smart_followers.append(e.get("twAccount"))
                        try:
                            kols_data = json.loads(kols_raw) if isinstance(kols_raw, str) else kols_raw
                            kol_count = kols_data.get("total_count", 0)
                            for u in kols_data.get("users", []):
                                sn = u.get("screen_name")
                                if sn and sn not in smart_followers:
                                    smart_followers.append(sn)
                        except Exception:
                            pass
                        candidates.append({
                            "handle": h,
                            "name": entry.get("twUserName") or "",
                            "summary": entry.get("description") or "",
                            "why": entry.get("description") or "",
                            "fol": fol,
                            "kind": "project",
                            "signal": {"hotCount": max(2, kol_count)},
                            "smart_followers": smart_followers[:5],
                            "source_feed": "985_follow",
                        })
    except Exception as err:
        print(f"WARN: Failed to fetch 985 twitter live events: {err}", file=sys.stderr)

    # 2. 985 new arrivals
    try:
        req = urllib.request.Request(
            "https://985monitor.xyz/api/new-arrivals",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            for a in data.get("arrivals", []):
                h = a.get("h")
                if not h:
                    continue
                candidates.append({
                    "handle": h,
                    "name": a.get("n") or "",
                    "summary": a.get("d") or "",
                    "why": a.get("d") or "",
                    "fol": a.get("f") or 0,
                    "kind": "project",
                    "signal": {"hotCount": 2},
                    "source_feed": "985_arrival",
                })
    except Exception as err:
        print(f"WARN: Failed to fetch 985 new arrivals: {err}", file=sys.stderr)

    # 3. 985 live tweets from smart followers (giveaway, NFT WL, GTD, drop address)
    try:
        req = urllib.request.Request(
            "https://985monitor.xyz/api/twitter-live-events?limit=500",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            for e in data.get("events", []):
                ev_type = e.get("eventType")
                if ev_type in ("NEW_TWEET", "NEW_TWEET_QUOTE", "NEW_TWEET_REPLY"):
                    c = e.get("content")
                    if not isinstance(c, dict):
                        continue
                    full_text = c.get("fullText") or c.get("text") or ""
                    if not full_text:
                        continue
                    # Check actionable in smart follower tweet directly
                    matched_kw = match_actionable(full_text)
                    has_form = has_form_url(full_text)
                    if not matched_kw and not has_form:
                        continue
                    h = e.get("twAccount") or c.get("userScreenName")
                    if not h:
                        continue
                    tid = str(c.get("tweetId") or c.get("id") or "")
                    candidates.append({
                        "handle": h,
                        "name": c.get("userName") or h,
                        "summary": full_text[:200],
                        "why": full_text[:200],
                        "fol": (c.get("user", {}) or {}).get("followersCount") or 0,
                        "kind": "smart_follower_tweet",
                        "signal": {"hotCount": 3},
                        "smart_followers": [h],
                        "source_feed": "985_kol_tweet",
                        "direct_tweet": full_text[:300],
                        "tweet_id": tid,
                    })
    except Exception as err:
        print(f"WARN: Failed to fetch 985 smart follower tweets: {err}", file=sys.stderr)

    return candidates


def main():
    from browser_lock import acquire_browser_lock, release_browser_lock, acquire_job_guard

    # --- Guard anti-overlap: hanya 1 instance eagent-scanner ---
    _guard = acquire_job_guard("eagent-scanner")
    if _guard is None:
        print("NO_TASKS")
        return

    # === FASE 0: ANTREAN TERTUNDA DIDAHULUKAN ===
    state = load_eagent_state()
    queued = load_json(EAGENT_QUEUE_FILE, [])

    # Auto-resolve antrean yang sudah ada di processed state
    queue_changed = False
    for x in queued:
        if x.get("status") == "pending" and is_already_processed(x.get("handle", ""), state):
            x["status"] = "skipped"
            x["skip_reason"] = "already_processed_in_state"
            queue_changed = True
    if queue_changed:
        save_json(EAGENT_QUEUE_FILE, queued)

    pending_queued = [x for x in queued
                      if x.get("handle") and x.get("status") == "pending"]

    if not pending_queued:
        # === FASE 1: FETCH KANDIDAT BARU (hanya kalau antrean kosong) ===
        fetched = _scan_candidates()
        if fetched:
            existing = {x.get("handle", "").lower() for x in queued}
            for t in fetched:
                if t["handle"].lower() not in existing:
                    queued.append({
                        "handle": t["handle"],
                        "name": t.get("name", ""),
                        "followers": t.get("followers", 0),
                        "insiders": t.get("insiders", 0),
                        "smart_followers": t.get("smart_followers", []),
                        "fr_smart_count": t.get("fr_smart_count", 0),
                        "fr_wallets": t.get("fr_wallets", {}),
                        "summary": t.get("summary", ""),
                        "matched_keywords": t.get("matched_keywords", []),
                        "has_form_url": t.get("has_form_url", False),
                        "source": t.get("source", ""),
                        "source_feed": t.get("source_feed", ""),
                        "tweet_text": t.get("tweet_text", ""),
                        "tweet_id": t.get("tweet_id", ""),
                        "x_url": t.get("x_url", ""),
                        "status": "pending",
                        "added_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                    })
            save_json(EAGENT_QUEUE_FILE, queued)
            pending_queued = [x for x in queued if x.get("status") == "pending"]

    if not pending_queued:
        print("NO_TASKS")
        return

    pending_queued.sort(key=lambda x: x.get("added_at") or "")

    # --- Browser lock: cek cepat (Opsi A). Cron berikutnya yang retry. ---
    try:
        acquire_browser_lock(timeout=5, job_name='eagent-scanner')
    except RuntimeError:
        print("LOCKED")
        return

    _has_tasks = False
    try:
        tasks = pending_queued[:MAX_PER_CYCLE]
        if not tasks:
            print("NO_TASKS")
            return

        # Tasks found — agent turn berikutnya pakai browser.
        # JANGAN release lock di sini, biar agent yang garap.
        _has_tasks = True

        print(f"TASKS_FOUND: {len(tasks)}")
        print("---")
        for i, t in enumerate(tasks, 1):
            kw_str = ", ".join(t["matched_keywords"]) if t.get("matched_keywords") else "form_url_detected"
            feed_label = "985monitor" if "985" in t.get("source_feed", "") else "PureAlpha"
            print(f"[{i}] @{t['handle']} ({t.get('name','')}) [{feed_label}]")
            print(f"    Followers: {t.get('followers',0)} | Insiders: {t.get('insiders',0)} | FrontrunSF: {t.get('fr_smart_count', '?')}")
            if t.get("smart_followers"):
                sf_str = ", ".join(f"@{s}" for s in t["smart_followers"][:5])
                print(f"    SmartFollower: {sf_str}")
            if t.get("fr_wallets"):
                wl_str = ", ".join(f"{k}:{v[:10]}..." for k, v in t["fr_wallets"].items())
                print(f"    Wallets: {wl_str}")
            print(f"    Match ({t.get('source','')}): {kw_str}")
            print(f"    Summary: {t.get('summary','')}")
            if t.get("tweet_text"):
                print(f"    Tweet: {t['tweet_text']}")
            print(f"    X: {t.get('x_url','')}")
            if t.get("has_form_url"):
                print(f"    ⚠ Form URL detected")
            print()
    finally:
        # Release lock HANYA kalau tidak ada task.
        if not _has_tasks:
            release_browser_lock()


def _frontrun_validate(handle, followers=0, is_project=True, is_ct_giveaway=False):
    """Validate handle via Frontrun Pro trust gate. Returns (trusted, result_dict)."""
    try:
        from frontrun_trust_gate import validate_handle
        result = validate_handle(
            handle,
            followers=followers,
            is_project=is_project,
            is_ct_giveaway=is_ct_giveaway,
        )
        return result.get("trusted", False), result
    except Exception as e:
        print(f"WARN: Frontrun trust gate failed for @{handle}: {e}", file=sys.stderr)
        # Fail-open: allow candidate through if Frontrun is down
        return True, {"trusted": True, "reject_reason": f"gate_error:{e}",
                       "smart_follower_count": 0, "smart_followers": [],
                       "username_changes": 0, "old_usernames": [], "wallets": {}}


def _scan_candidates():
    """Scan PureAlpha + 985monitor, validate via Frontrun trust gate, return actionable tasks (max 5)."""
    state = load_eagent_state()
    seen_handles = set()
    items = []
    for window in ["10m", "1h", "3h", "24h"]:
        try:
            result = fetch_feed(feed="hot", window=window)
            for item in result.get("data", []):
                h = item.get("handle", "")
                if h and h not in seen_handles:
                    seen_handles.add(h)
                    item["source_feed"] = "purealpha"
                    flws = item.get("flws", [])
                    sf_list = [
                        f.get("handle") for f in flws
                        if f.get("handle") and not f.get("handle").startswith("•")
                    ]
                    item["smart_followers"] = sf_list
                    items.append(item)
        except Exception as e:
            print(f"WARN: Failed to fetch window={window}: {e}", file=sys.stderr)

    for item in fetch_985_candidates():
        h = item.get("handle", "")
        if h and h not in seen_handles:
            seen_handles.add(h)
            items.append(item)

    if not items:
        return []

    candidates = []
    for item in items:
        handle = item.get("handle", "")
        if not handle:
            continue
        if is_already_processed(handle, state):
            continue
        kind = item.get("kind", "project")
        if kind not in ("project", "person", "smart_follower_tweet"):
            continue
        fol = item.get("fol", 0) or 0
        if kind != "smart_follower_tweet" and fol > 25000:
            continue
        signal = item.get("signal", {})
        hot_count = signal.get("hotCount") or len(item.get("flws", [])) + (item.get("flwsMore") or 0)
        if kind != "smart_follower_tweet" and hot_count < 2:
            continue
        candidates.append((item, hot_count))

    if not candidates:
        return []

    tasks = []
    for item, hot_count in candidates:
        handle = item.get("handle", "")
        name = item.get("name") or ""
        summary = item.get("why") or item.get("summary") or ""
        fol = item.get("fol", 0) or 0
        kind = item.get("kind", "project")
        source_feed = item.get("source_feed", "")
        direct_tw = item.get("direct_tweet", "")

        # --- DETERMINE TARGET TYPE ---
        text_all = f"{name} {handle} {summary} {direct_tw}".lower()
        has_giveaway_kw = any(k in text_all for k in ("giveaway", "give away", "giving away", "raffle"))

        # CT Giveaway: from smart follower / KOL tweet, personal account, or non-project giveaway
        is_ct_giveaway = (
            kind in ("smart_follower_tweet", "person")
            or source_feed == "985_kol_tweet"
            or (has_giveaway_kw and kind != "project")
        )
        is_project = not is_ct_giveaway

        # --- FRONTRUN TRUST GATE ---
        trusted, fr_result = _frontrun_validate(
            handle,
            followers=fol,
            is_project=is_project,
            is_ct_giveaway=is_ct_giveaway,
        )
        if not trusted:
            reason = fr_result.get("reject_reason", "unknown")
            target_type = "CT giveaway" if is_ct_giveaway else f"project (fol={fol})"
            print(f"SKIP @{handle} [{target_type}]: Frontrun rejected ({reason})", file=sys.stderr)
            continue

        if item.get("direct_tweet"):
            direct_tw = item.get("direct_tweet", "")
            matched_kw = match_actionable(direct_tw)
            has_form = has_form_url(direct_tw)
            source = "smart_follower_tweet"
            tweet_text = direct_tw
        else:
            bio_text = f"{name} {handle} {summary}"
            matched_kw = match_actionable(bio_text)
            has_form = has_form_url(bio_text)
            source = "bio"
            tweet_text = ""

            if not matched_kw and not has_form:
                user_id = item.get("id")
                tweets = fetch_recent_tweets(handle, user_id=user_id, count=5)
                all_tweets = " ".join(tweets)
                matched_kw = match_actionable(all_tweets)
                has_form = has_form_url(all_tweets)
                if not matched_kw and not has_form:
                    continue
                source = "tweet"
                for tw in tweets:
                    tw_match = match_actionable(tw)
                    tw_form = has_form_url(tw)
                    if tw_match or tw_form:
                        tweet_text = tw[:200]
                        break

        # Enrich with Frontrun data
        fr_sf = fr_result.get("smart_followers", [])
        fr_wallets = fr_result.get("wallets", {})
        # Merge smart followers: feeder source + Frontrun source (dedupe)
        existing_sf = item.get("smart_followers", [])
        merged_sf = list(dict.fromkeys(existing_sf + fr_sf))[:10]

        tasks.append({
            "handle": handle,
            "name": name,
            "followers": fol,
            "insiders": hot_count,
            "smart_followers": merged_sf,
            "fr_smart_count": fr_result.get("smart_follower_count", 0),
            "fr_wallets": fr_wallets,
            "summary": summary[:200],
            "matched_keywords": matched_kw[:3],
            "has_form_url": has_form,
            "source": source,
            "source_feed": item.get("source_feed", "purealpha"),
            "tweet_text": tweet_text,
            "tweet_id": item.get("tweet_id", ""),
            "x_url": f"https://x.com/{handle}",
        })

        if len(tasks) >= 5:
            break

    return tasks



if __name__ == "__main__":
    main()
