# Metadata: Domain: Generic, Date: 2026-08-22, Symptom: Element unclickable due to Shadow DOM isolation

async def click_shadow_dom(page, selectors):
    """
    Pierces Shadow DOM boundaries to click elements (e.g., Dynamic.xyz or Privy modals).
    :param page: Playwright page object
    :param selectors: List of CSS selectors pathing through shadow roots to the target.
    """
    script = """(selectors) => {
        let current = document;
        for (let i = 0; i < selectors.length; i++) {
            let el = current.querySelector(selectors[i]);
            if (!el) return false;
            if (i === selectors.length - 1) {
                el.click();
                return true;
            }
            current = el.shadowRoot || el;
        }
        return false;
    }"""
    return await page.evaluate(script, selectors)