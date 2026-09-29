# Agentic — Autonomous Eagent Airdrop Scanner & Executor

Fully autonomous LLM-driven airdrop hunter, waitlist scanner, and execution engine designed for **Hermes Agent**.

Monitors **PureAlpha.app** (hot & new windows) and **985monitor.xyz** (smart follower live events) with **Frontrun Pro** trust verification (anti-rebrand check, min 5 smart followers, wallet detection) for high-signal opportunities:
- Web waitlist & registration forms (Google Forms, Typeform, Tally, Premint, Alphabot)
- Verified whitelist (WL) & Guaranteed (GTD) NFT minting
- Direct creator/founder wallet-drop replies
- Anti-scam, anti-farming keyword & reputation filters

---

## 🏛 Architecture

```
┌───────────────────────────────────────────────────────────┐
│              Hermes Cron Trigger (every 15m)              │
└─────────────────────────────┬─────────────────────────────┘
                              ▼
        ┌───────────────────────────────────────────┐
        │  scripts/purealpha_eagent_feeder.py       │
        │  - Acquire browser lock                   │
        │  - Check pending queue                    │
        │  - Scrape PureAlpha + 985monitor API      │
        │  - Pre-filter keywords, deduplicate state │
        └─────────────────────┬─────────────────────┘
                              ▼
                [TASKS_FOUND / NO_TASKS]
                              ▼
        ┌───────────────────────────────────────────┐
        │  Hermes Autonomous LLM Turn               │
        │  Skills: eagent-scanner + penggarap-agent │
        │  - Evaluate legitimacy vs scam/farming    │
        │  - Browser automation over local CDP 9222 │
        │  - Fill forms using ~/airdrop_identity.py │
        │  - Post report to Telegram Topic          │
        │  - Cleanup tabs & release browser lock    │
        └───────────────────────────────────────────┘
```

---

## 📁 Repository Structure

```
agentic/
├── README.md                      # Documentation & setup guide
├── setup.sh                       # 1-click installer for Hermes on Linux
├── requirements.txt               # Python package dependencies
├── .env.example                   # Environment variable template
├── config/
│   ├── airdrop_identity.py.example # Schema for EVM/SOL/social identities
│   ├── purealpha_cookies.json.example # PureAlpha auth session template
│   ├── eagent_state.json.example  # Initial dedup state file
│   └── eagent_queue.json.example  # Initial queue file
├── cron/
│   ├── eagent_scanner_cron.json   # Hermes cronjob spec
│   └── register_cron.py           # Auto-registers cron in ~/.hermes/cron/jobs.json
├── scripts/
│   ├── purealpha_eagent_feeder.py # Main feeder scanner script
│   ├── purealpha_client.py        # Next.js RSC parser for purealpha.app
│   ├── eagent_precheck.py         # State manager (mark done / skip)
│   ├── post_eagent_report.py      # Telegram HTML reporter
│   ├── nft_watchlist_register.py  # Idempotent NFT watchlist tracker
│   ├── browser_lock.py            # Chromium concurrency lock
│   ├── cleanup_tabs.py            # Auto tab hygiene / RAM saver
│   └── x_native.py                # Twitter GraphQL actions (HTTP, no browser)
├── skills/
│   └── crypto/
│       ├── eagent-scanner/        # LLM Autonomous SOP
│       └── penggarap-agent/       # Web3 form & DOM bypass SOP + references
└── tests/
    ├── test_purealpha_eagent_feeder.py
    ├── test_eagent_precheck.py
    └── test_post_eagent_report.py
```

---

## ⚡ Prerequisites

1. **Linux VPS** (Ubuntu 22.04+ recommended, min 2GB RAM).
2. **Python 3.10+**.
3. **Hermes Agent** installed (`hermes`).
4. **Google Chrome / Chromium** running with remote debugging port `9222`:
   ```bash
   google-chrome --remote-debugging-port=9222 --headless=new &
   ```
5. Verified Telegram bot for status reports.

---

## 🚀 Quick Start (New VPS / Agent)

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/jxiexyz/agentic.git
cd agentic
pip install -r requirements.txt
```

### 2. Run Setup Script

```bash
./setup.sh
```

This will automatically:
- Copy scripts to `~/.hermes/scripts/`
- Install skills into `~/.hermes/skills/crypto/`
- Initialize state and queue files
- Register the `eagent-scanner` cronjob in Hermes

### 3. Configure Credentials

#### A. Telegram Reporting (`~/.hermes/.env`)
Edit `~/.hermes/.env`:
```env
EAGENT_BOT_TOKEN="your_telegram_bot_token"
EAGENT_CHAT_ID="-100xxxxxxxxxx"
EAGENT_TOPIC_ID=3602
```

#### B. Airdrop Identity (`~/airdrop_identity.py`)
Edit `~/airdrop_identity.py` and populate your EVM wallet, Solana wallet, and social handles:
```python
IDENTITY = {
    "main": {
        "evm_wallet": "0xYourWalletAddress...",
        "sol_wallet": "YourSolAddress...",
        "x_handle": "YourTwitterHandle",
        "email": "your_email@domain.com",
        ...
    }
}
```

#### C. PureAlpha Session Cookies (`~/.hermes/purealpha_cookies.json`)
Export your session cookies from purealpha.app and save them to `~/.hermes/purealpha_cookies.json`.

#### D. Frontrun Pro Session Cookies (`~/.hermes/frontrun_cookies.json`)
Export your session cookies from frontrun.pro (`__Secure-frontrun.session_token`) and save to `~/.hermes/frontrun_cookies.json`.

---

## 🧪 Testing & Verification

Run the test suite:
```bash
pytest tests/
```

Test the feeder manually:
```bash
python3 ~/.hermes/scripts/purealpha_eagent_feeder.py
```

Check state:
```bash
python3 ~/.hermes/scripts/eagent_precheck.py
```

---

## 🛡 Concurrency & Safety Rules

- **Browser Lock (`browser_lock.py`)**: Ensures only one worker or LLM agent touches the Chrome instance at any given time.
- **Tab Cleanup (`cleanup_tabs.py`)**: Tabs are automatically killed after execution to prevent memory leaks on 2GB VPS nodes.
- **Anti-Duplication**: All processed usernames, tweet IDs, and form links are recorded in `eagent_state.json`. If a target is already followed or completed, it is immediately skipped.
