# Metadata: Origin Domain: app.rally.fun, Date: 2026-08-26, Symptom: Auth/Login page hangs waiting for wallet interaction

async def handle_web3_auth(page, target_text="Browser Wallet"):
    """Clicks wallet auth buttons bypassing standard visibility checks."""
    try:
        await page.wait_for_load_state('domcontentloaded')
        await page.locator(f"button:has-text('{target_text}')").first.click(force=True, timeout=5000)
        return True
    except Exception:
        # Fallback to JS click for shadow DOM or overlapping elements
        return await page.evaluate('''(text) => {
            let clicked = false;
            document.querySelectorAll('button, div[role="button"]').forEach(el => {
                if (el.textContent && el.textContent.includes(text)) {
                    el.click();
                    clicked = true;
                }
            });
            return clicked;
        }''', target_text)