# Metadata: Origin Domain: app.rally.fun, Date: 2026-08-26, Symptom: Wallet connect button clicks blocked by Shadow DOM boundaries (Privy/Dynamic).

async def click_wallet_button(page, button_text="Browser Wallet"):
    js_code = """
    (text) => {
        function searchElement(root) {
            for (const el of root.querySelectorAll('*')) {
                if (el.shadowRoot) {
                    const found = searchElement(el.shadowRoot);
                    if (found) return found;
                }
                if ((el.tagName === 'BUTTON' || el.getAttribute('role') === 'button' || el.closest('button')) && el.textContent.toLowerCase().includes(text.toLowerCase())) {
                    return el;
                }
            }
            return null;
        }
        const btn = searchElement(document);
        if (btn) {
            btn.click();
            return true;
        }
        return false;
    }
    """
    return await page.evaluate(js_code, button_text)