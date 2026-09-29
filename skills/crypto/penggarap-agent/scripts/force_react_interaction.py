# Metadata: Origin Domain: app.rally.fun, Date: 2026-08-26, Symptom: Element not clickable / Intercepted by React synthetic events or Shadow DOM boundaries

import asyncio

async def force_click(page, selector: str, timeout: int = 5000):
    """Forces a click using JavaScript to bypass React synthetic event blockers and shadow DOM boundaries."""
    try:
        await page.wait_for_selector(selector, state='attached', timeout=timeout)
        await page.evaluate('''(sel) => {
            const el = document.querySelector(sel);
            if (el) {
                el.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }));
                return;
            }
            // Fallback for Shadow DOM traversal
            const traverse = (root) => {
                const node = root.querySelector(sel);
                if (node) return node;
                const shadows = Array.from(root.querySelectorAll('*')).filter(n => n.shadowRoot);
                for (let s of shadows) {
                    const res = traverse(s.shadowRoot);
                    if (res) return res;
                }
                return null;
            };
            const shadowEl = traverse(document);
            if (shadowEl) shadowEl.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }));
        }''', selector)
        return True
    except Exception as e:
        print(f"Force click failed for {selector}: {e}")
        return False
