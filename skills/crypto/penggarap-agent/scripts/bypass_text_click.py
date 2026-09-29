# Metadata: Domain: testnet.x1ecochain.com, Date: 2026-08-25, Symptom: Playwright Page.click Timeout on generic text selectors due to strict visibility/intercept checks.

async def bypass_text_click(page, text: str):
    """
    Bypass Playwright's strict visibility/intercept checks for text-based clicks.
    Finds the element containing the text and forces a click via JS.
    """
    await page.evaluate("""(textToFind) => {
        const elements = Array.from(document.querySelectorAll('*'));
        const el = elements.find(e => 
            e.children.length === 0 && 
            e.textContent.trim() === textToFind
        );
        if (el) {
            el.click();
        } else {
            // Fallback: look for partial match if exact fails
            const partial = elements.find(e => 
                e.children.length === 0 && 
                e.textContent.includes(textToFind)
            );
            if (partial) partial.click();
        }
    }""", text)