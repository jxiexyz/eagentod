# Metadata: Origin Domain: app.meridian.xyz, Date: 2026-08-22, Symptom: Web3 modal/faucet buttons (Connect, Claim) unresponsive due to Shadow DOM/React event traps.

async def force_click_web3_button(page, selector_or_text: str):
    """
    Generic Web3 button clicker for Connect/Faucet/Predict bypassing shadow DOM.
    """
    try:
        el = await page.wait_for_selector(selector_or_text, timeout=3000, state="attached")
        if el:
            await el.click(force=True)
            return True
    except Exception:
        pass

    script = """
    (target) => {
        const findAndClick = (root) => {
            for (const el of root.querySelectorAll('*')) {
                if ((el.matches && el.matches(target)) || (el.textContent && el.textContent.trim() === target)) {
                    el.click();
                    return true;
                }
                if (el.shadowRoot && findAndClick(el.shadowRoot)) {
                    return true;
                }
            }
            return false;
        };
        return findAndClick(document);
    }
    """
    return await page.evaluate(script, selector_or_text)