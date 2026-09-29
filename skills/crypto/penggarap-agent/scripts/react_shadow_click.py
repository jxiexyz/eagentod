# Metadata: sporefolks.fun, 2026-08-25, Shadow DOM / React synthetic event click failure
import asyncio

async def force_click(page, selector: str):
    """
    Generic bypass for elements hidden in Shadow DOM or requiring React synthetic events.
    """
    js_code = """
    (selector) => {
        const findElement = (root, sel) => {
            let el = root.querySelector(sel);
            if (el) return el;
            for (let child of Array.from(root.querySelectorAll('*')).filter(e => e.shadowRoot)) {
                let res = findElement(child.shadowRoot, sel);
                if (res) return res;
            }
            return null;
        };
        const target = findElement(document, selector);
        if (!target) return false;
        ['pointerdown', 'mousedown', 'pointerup', 'mouseup', 'click'].forEach(t => {
            target.dispatchEvent(new MouseEvent(t, {view: window, bubbles: true, cancelable: true, buttons: 1}));
        });
        return true;
    }
    """
    return await page.evaluate(js_code, selector)
