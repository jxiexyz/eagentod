#!/usr/bin/env bash
set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HERMES_DIR="$HOME/.hermes"
HERMES_SCRIPTS="$HERMES_DIR/scripts"
HERMES_SKILLS="$HERMES_DIR/skills/crypto"

echo "=== Setting up Eagent Scanner ==="

# 1. Directories
echo "[*] Creating target directories in $HERMES_DIR..."
mkdir -p "$HERMES_SCRIPTS"
mkdir -p "$HERMES_SKILLS"

# 2. Copy scripts
echo "[*] Installing runner scripts to $HERMES_SCRIPTS..."
cp -v "$REPO_DIR/scripts/"*.py "$HERMES_SCRIPTS/"
chmod +x "$HERMES_SCRIPTS/"*.py

# 3. Copy skills
echo "[*] Installing skills to $HERMES_SKILLS..."
rm -rf "$HERMES_SKILLS/eagent-scanner" "$HERMES_SKILLS/penggarap-agent"
cp -r "$REPO_DIR/skills/crypto/eagent-scanner" "$HERMES_SKILLS/"
cp -r "$REPO_DIR/skills/crypto/penggarap-agent" "$HERMES_SKILLS/"

# 4. State & Queue files initialization
if [ ! -f "$HERMES_SCRIPTS/eagent_state.json" ]; then
    echo "[*] Initializing empty eagent_state.json..."
    cp "$REPO_DIR/config/eagent_state.json.example" "$HERMES_SCRIPTS/eagent_state.json"
fi

if [ ! -f "$HERMES_SCRIPTS/eagent_queue.json" ]; then
    echo "[*] Initializing empty eagent_queue.json..."
    cp "$REPO_DIR/config/eagent_queue.json.example" "$HERMES_SCRIPTS/eagent_queue.json"
fi

if [ ! -f "$HERMES_SCRIPTS/nft_watchlist.json" ]; then
    echo "[*] Initializing empty nft_watchlist.json..."
    echo "[]" > "$HERMES_SCRIPTS/nft_watchlist.json"
fi

# 5. Environment config (.env)
if [ ! -f "$HERMES_DIR/.env" ]; then
    if [ -f "$REPO_DIR/.env" ]; then
        cp "$REPO_DIR/.env" "$HERMES_DIR/.env"
    else
        echo "[!] No .env found. Copying .env.example to $HERMES_DIR/.env"
        cp "$REPO_DIR/.env.example" "$HERMES_DIR/.env"
    fi
fi

# 6. Check airdrop_identity.py
if [ ! -f "$HOME/airdrop_identity.py" ]; then
    echo "[!] ~/airdrop_identity.py not found!"
    echo "[*] Creating template at $HOME/airdrop_identity.py. PLEASE EDIT IT with your credentials."
    cp "$REPO_DIR/config/airdrop_identity.py.example" "$HOME/airdrop_identity.py"
fi

# 7. Check PureAlpha cookies
if [ ! -f "$HERMES_DIR/purealpha_cookies.json" ]; then
    echo "[!] $HERMES_DIR/purealpha_cookies.json not found."
    echo "[*] Creating placeholder from example..."
    cp "$REPO_DIR/config/purealpha_cookies.json.example" "$HERMES_DIR/purealpha_cookies.json"
fi

# 8. Register Cron Job
echo "[*] Registering cron job in Hermes..."
python3 "$REPO_DIR/cron/register_cron.py"

# 9. Verify CDP connection
echo "[*] Checking local Chrome CDP port 9222..."
if curl -s http://127.0.0.1:9222/json/version >/dev/null 2>&1; then
    echo "[✓] Chrome CDP port 9222 reachable."
else
    echo "[!] WARNING: Chrome CDP port 9222 is NOT reachable."
    echo "    Make sure Chrome is running with: google-chrome --remote-debugging-port=9222 --headless=new"
fi

echo "=== Setup complete! ==="
echo "Next steps:"
echo "1. Edit ~/.hermes/.env with your Telegram bot credentials (EAGENT_BOT_TOKEN, EAGENT_CHAT_ID, EAGENT_TOPIC_ID)"
echo "2. Edit ~/airdrop_identity.py with your EVM/SOL addresses and X/social handles"
echo "3. Add valid session cookies to ~/.hermes/purealpha_cookies.json"
echo "4. Test feeder manually: python3 ~/.hermes/scripts/purealpha_eagent_feeder.py"
