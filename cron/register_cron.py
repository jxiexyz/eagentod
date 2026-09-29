#!/usr/bin/env python3
"""
register_cron.py
Registers eagent-scanner cron job into Hermes Agent jobs.json.
Can be executed directly on the VPS.
"""
import json
import os
import sys
import uuid
from datetime import datetime

HERMES_DIR = os.path.expanduser("~/.hermes")
CRON_FILE = os.path.join(HERMES_DIR, "cron", "jobs.json")
SPEC_FILE = os.path.join(os.path.dirname(__file__), "eagent_scanner_cron.json")

def register():
    if not os.path.exists(HERMES_DIR):
        print(f"[!] Hermes directory not found at {HERMES_DIR}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(os.path.dirname(CRON_FILE), exist_ok=True)

    with open(SPEC_FILE, "r") as f:
        spec = json.load(f)

    jobs_data = {"jobs": []}
    if os.path.exists(CRON_FILE):
        try:
            with open(CRON_FILE, "r") as f:
                jobs_data = json.load(f)
        except Exception:
            jobs_data = {"jobs": []}

    jobs = jobs_data.get("jobs", []) if isinstance(jobs_data, dict) else jobs_data

    # Check if already exists
    existing = [j for j in jobs if j.get("name") == spec["name"]]
    if existing:
        print(f"[*] Job '{spec['name']}' already registered (ID: {existing[0].get('id')}). Updating spec...")
        for k, v in spec.items():
            existing[0][k] = v
        existing[0]["enabled"] = True
        existing[0]["state"] = "scheduled"
    else:
        new_job = dict(spec)
        new_job["id"] = uuid.uuid4().hex[:12]
        new_job["enabled"] = True
        new_job["state"] = "scheduled"
        new_job["created_at"] = datetime.now().isoformat()
        jobs.append(new_job)
        print(f"[+] Registered job '{spec['name']}' with ID: {new_job['id']}")

    if isinstance(jobs_data, dict):
        jobs_data["jobs"] = jobs
        jobs_data["updated_at"] = datetime.now().isoformat()
        to_save = jobs_data
    else:
        to_save = jobs

    with open(CRON_FILE, "w") as f:
        json.dump(to_save, f, indent=2)

    print(f"[✓] Cron job successfully saved to {CRON_FILE}")

if __name__ == "__main__":
    register()
