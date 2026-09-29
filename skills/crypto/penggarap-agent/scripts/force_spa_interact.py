# Metadata: Origin Domain: takeapeak.ai, Date: 2026-08-25, Symptom: Element intercepted / Not interactable during SPA routing

async def force_click(page, selector: str, timeout: int = 5000):
    """
    Bypasses transparent overlays and React event listener issues by dispatching 
    a native click event directly on the DOM element.
    """
    await page.wait_for_selector(selector, state="attached", timeout=timeout)
    await page.evaluate('''(sel) => {
        const el = document.querySelector(sel);
        if (!el) throw new Error("Element not found");
        el.scrollIntoView({behavior: 'smooth', block: 'center'});
        const event = new MouseEvent('click', {
            view: window,
            bubbles: true,
            cancelable: true
        });
        el.dispatchEvent(event);
    }''', selector)

async def force_fill(page, selector: str, text: str, timeout: int = 5000):
    """
    Forces input values and triggers React's synthetic event system.
    """
    await page.wait_for_selector(selector, state="attached", timeout=timeout)
    await page.evaluate('''({sel, text}) => {
        const el = document.querySelector(sel);
        if (!el) throw new Error("Element not found");
        el.value = text;
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }''', {'sel': selector, 'text': text})