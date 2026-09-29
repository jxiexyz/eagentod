# Origin Domain: app.rally.fun
# Date: 2026-08-26
# Symptom: Fails to complete social tasks/wallet connect due to shadow DOM buttons (Web3Modal/WalletConnect V3) and popup windows

async def handle_shadow_click_and_popup(context, page, button_text: str):
    """Clicks a button (even in shadow DOM) and yields the popup/new tab if one opens."""
    script = '''
    (text) => {
        function findBtn(root) {
            for (const el of root.querySelectorAll('*')) {
                if (el.shadowRoot) {
                    const res = findBtn(el.shadowRoot);
                    if (res) return res;
                }
                const tag = el.tagName;
                if ((tag === 'BUTTON' || tag === 'A' || tag === 'W3M-CONNECT-BUTTON' || tag === 'WUI-CARD') && el.textContent.trim().toLowerCase().includes(text.toLowerCase())) {
                    el.click();
                    return true;
                }
            }
            return false;
        }
        return findBtn(document);
    }
    '''
    try:
        async with context.expect_page(timeout=5000) as new_page_info:
            clicked = await page.evaluate(script, button_text)
            if not clicked:
                return None
        new_page = await new_page_info.value
        await new_page.wait_for_load_state('domcontentloaded')
        return new_page
    except Exception:
        return None