# eagentod — Autonomous Airdrop Scanner & On-Chain Execution Agent

**eagentod** is an autonomous intelligence engine and execution pipeline designed for crypto hunters, automated waitlist farming, and high-signal alpha discovery.

It continuously tracks early projects, influencer movements, and curated giveaways across decentralized feeds, filters out scams and rebrands using real-time social trust metrics, and prepares actionable tasks for automated execution.

---

## ⚡ Key Features

- **Multi-Source Social Radar**: Scans real-time feeds from PureAlpha, 985monitor live streams, and KOL activity for new project arrivals and alpha opportunities.
- **Moni Intelligence & Trust Gate**: Automated zero-auth reputation verification — tracks verified smart followers, scores, and rebrand history to eliminate bot farms and scam accounts before execution.
- **Dynamic Tiered Thresholds**: Adaptive filtering criteria tailored for early projects vs. high-velocity CT giveaways (anti-rebrand detection + tiered smart follower requirements).
- **Autonomous Task Extraction**: Intelligent detection of actionable opportunities including Google Forms, Typeform, Tally, Premint, Whitelist (WL) / Guaranteed (GTD) allocations, and wallet drop requests.
- **Resource-Efficient & VPS-Optimized**: Ultra-lightweight footprint (~20MB RAM during scanning cycles) engineered to run seamlessly on resource-constrained environments (Linux 2GB RAM / low-spec VPS).
- **Concurrency & Browser Isolation**: Built-in process guard and browser locking mechanisms to ensure zero race conditions across concurrent automated jobs.
- **Automated Web3 Form & Social Workflows**: Form automation, wallet injection, and contextual interaction handling over local CDP.

---

## 🛠 Prerequisites

- Linux environment (Ubuntu 22.04+ recommended)
- Python 3.10+
- Google Chrome / Chromium (with remote debugging port enabled)
- Active identity profile (`airdrop_identity.py`)

---

## 🚀 Quick Setup

1. **Clone repository**:
   ```bash
   git clone https://github.com/jxiexyz/eagentod.git
   cd eagentod
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**:
   - Set up your social accounts and target wallet identities.
   - Configure reporting webhooks or Telegram bot credentials.

4. **Run Test Suite**:
   ```bash
   pytest tests/
   ```

---

*Explore the codebase to discover the automation mechanics, browser execution strategies, and custom pipeline workflows.*
