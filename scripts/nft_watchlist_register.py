#!/usr/bin/env python3
"""
Register NFT project to nft_watchlist.json.
Usage:
  python3 nft_watchlist_register.py <x_handle> <project_name> <chain> [notes]

Idempotent — skip if handle already exists. Used by worker-agent and eagent-scanner
after successfully completing an NFT WL/mint task.
"""
import sys
import json
import os
from datetime import date

FILE = os.environ.get("NFT_WATCHLIST_FILE", os.path.expanduser("~/.hermes/scripts/nft_watchlist.json"))


def register(handle, project, chain, notes=""):
    handle = handle.strip().lstrip("@").lower()
    if not handle:
        return

    data = []
    if os.path.exists(FILE):
        with open(FILE) as f:
            data = json.load(f)

    if any(p["x_handle"] == handle for p in data):
        print(f"[NFT-WL] Already tracked: @{handle}")
        return

    data.append({
        "project": project,
        "x_handle": handle,
        "chain": chain,
        "type": "wl_nft",
        "notes": notes,
        "added": str(date.today()),
    })
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"[NFT-WL] Registered: {project} (@{handle}) on {chain}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: nft_watchlist_register.py <handle> <project> <chain> [notes]")
        sys.exit(1)
    register(sys.argv[1], sys.argv[2], sys.argv[3], " ".join(sys.argv[4:]) if len(sys.argv) > 4 else "")
