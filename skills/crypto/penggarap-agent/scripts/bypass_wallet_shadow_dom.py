# Metadata: Origin: rewards.svpstars.com | Date: 2026-09-22 | Symptom: Web3 wallet button not accessible due to shadow DOM or overlay

async def click_shadow_wallet(page, wallet_name="Xverse"):
    js = """(name) => {
        const scan = (root) => {
            for (const el of root.querySelectorAll('*')) {
                if (el.shadowRoot) {
                    if (scan(el.shadowRoot)) return true;
                }
                if (el.textContent?.toLowerCase().includes(name.toLowerCase()) && el.getBoundingClientRect().width > 0) {
                    el.click();
                    return true;
                }
            }
            return false;
        };
        return scan(document);
    }"""
    if not await page.evaluate(js, wallet_name):
        await page.get_by_text(wallet_name, exact=False).first.click(timeout=3000)
