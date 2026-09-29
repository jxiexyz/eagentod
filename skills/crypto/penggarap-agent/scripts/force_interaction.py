# Metadata: app.meridian.xyz, 2026-08-22, Element not interactable / click intercepted

async def force_click(page, selector: str, timeout: int = 5000):
    await page.wait_for_selector(selector, state="attached", timeout=timeout)
    await page.evaluate("""(sel) => {
        const el = document.querySelector(sel);
        if (!el) throw new Error("Element not found: " + sel);
        el.scrollIntoView({behavior: "instant", block: "center"});
        el.dispatchEvent(new MouseEvent("click", {bubbles: true, cancelable: true, view: window}));
    }""", selector)

async def force_fill(page, selector: str, text: str, timeout: int = 5000):
    await page.wait_for_selector(selector, state="attached", timeout=timeout)
    await page.evaluate("""([sel, val]) => {
        const el = document.querySelector(sel);
        if (!el) throw new Error("Element not found: " + sel);
        el.scrollIntoView({behavior: "instant", block: "center"});
        el.focus();
        const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value")?.set;
        if (nativeSetter) nativeSetter.call(el, val);
        else el.value = val;
        el.dispatchEvent(new Event("input", { bubbles: true }));
        el.dispatchEvent(new Event("change", { bubbles: true }));
    }""", [selector, text])
