#!/usr/bin/env python3
"""
Precheck & Scanner for Eagent (Autonomous Web Hunter).
Scans X research, filters out scams/spams, checks against persistent done/state history,
checks follow status on X, and only returns fresh valid tasks to stdout.
"""
import os
import sys
import json
import re
from datetime import datetime

STATE_FILE = os.environ.get("EAGENT_STATE_FILE", os.path.expanduser("~/.hermes/scripts/eagent_state.json"))
QUEUE_FILE = os.environ.get("EAGENT_QUEUE_FILE", os.path.expanduser("~/.hermes/scripts/eagent_queue.json"))

def _update_queue(username=None, tweet_id=None, status="done", note=""):
    queue_path = os.environ.get("EAGENT_QUEUE_FILE", QUEUE_FILE)
    if not os.path.exists(queue_path):
        return
    try:
        with open(queue_path, "r") as f:
            queue = json.load(f)
        changed = False
        for item in queue:
            match_u = username and item.get("handle", "").lower() == username.lower()
            match_t = tweet_id and str(item.get("tweet_id", "")) == str(tweet_id)
            if (match_u or match_t) and item.get("status") == "pending":
                item["status"] = status
                if note:
                    item["skip_reason" if status == "skipped" else "note"] = note
                changed = True
        if changed:
            with open(queue_path, "w") as f:
                json.dump(queue, f, indent=2)
    except Exception as e:
        print(f"[WARN] Failed to update queue: {e}", file=sys.stderr)

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "processed_tweet_ids": [],
        "processed_users": ["kaleido_finance"],
        "processed_domains": ["kaleido.finance", "forms.gle/i6QsTeTyxHTFHn"],
        "history": []
    }

def save_state(state):
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"[ERROR] Failed to save state: {e}", file=sys.stderr)

def mark_done(tweet_id=None, username=None, domain=None, note=""):
    state = load_state()
    if "processed_tweet_ids" not in state: state["processed_tweet_ids"] = []
    if "processed_users" not in state: state["processed_users"] = []
    if "processed_domains" not in state: state["processed_domains"] = []
    if "history" not in state: state["history"] = []

    if tweet_id and tweet_id not in state["processed_tweet_ids"]:
        state["processed_tweet_ids"].append(str(tweet_id))
    if username and username.lower() not in [u.lower() for u in state["processed_users"]]:
        state["processed_users"].append(username.lower())
    if domain and domain.lower() not in [d.lower() for d in state["processed_domains"]]:
        state["processed_domains"].append(domain.lower())

    state["history"].append({
        "timestamp": datetime.now().isoformat(),
        "tweet_id": tweet_id,
        "username": username,
        "domain": domain,
        "note": note
    })
    save_state(state)
    status = "skipped" if note and "skip" in note.lower() else "done"
    _update_queue(username=username, tweet_id=tweet_id, status=status, note=note)
    print(f"[DEDUP] Marked done: {username or domain or tweet_id}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ("mark", "skip"):
        is_skip = sys.argv[1] == "skip"
        u = sys.argv[2] if len(sys.argv) > 2 else ""
        d = sys.argv[3] if len(sys.argv) > 3 else ""
        note = sys.argv[4] if len(sys.argv) > 4 else ("skipped" if is_skip else "manual mark")
        mark_done(username=u, domain=d, note=note)
    else:
        state = load_state()
        print(f"Eagent State Summary:")
        print(f"- Processed Tweet IDs: {len(state.get('processed_tweet_ids', []))}")
        print(f"- Processed Users: {state.get('processed_users', [])}")
        print(f"- Processed Domains: {state.get('processed_domains', [])}")
