# Origin Domain: hub.axisrobotics.ai
# Date: 2026-08-26
# Specific Symptom: Wallet and X connect buttons unresponsive (shadow DOM) or OAuth popup timeouts (session 20260826_181635_214483)

async def click_shadow_dom_element(page, selector: str):
    """Finds and clicks an element piercing shadow DOMs (common in Privy, Dynamic, Web3Modal)."""
    js_script = """
    (selector) => {
        function querySelectorAllShadows(selector, el = document.body) {
            const childShadows = Array.from(el.querySelectorAll('*')).map(e => e.shadowRoot).filter(Boolean);
            const childResults = childShadows.map(child => querySelectorAllShadows(selector, child));
            const result = Array.from(el.querySelectorAll(selector));
            return result.concat(...childResults);
        }
        const elements = querySelectorAllShadows(selector);
        if (elements.length > 0) {
            elements[0].click();
            return true;
        }
        return false;
    }
    """
    return await page.evaluate(js_script, selector)

async def handle_oauth_popup(page, trigger_selector: str):
    """Clicks an OAuth button (like X connect) and returns the popup page object."""
    async with page.expect_popup() as popup_info:
        try:
            await page.click(trigger_selector, timeout=3000)
        except Exception:
            await click_shadow_dom_element(page, trigger_selector)
    return await popup_info.value
