# Metadata: Domain: otterink.xyz, Date: 2026-08-25, Symptom: Quest buttons intercepted or hidden in shadow DOM causing standard click failures
import asyncio

async def bypass(page, selector, timeout=10000):
    """
    Pierces shadow DOMs and uses JS click to bypass pointer events interception.
    """
    try:
        await page.wait_for_selector(selector, state="attached", timeout=timeout)
        await page.evaluate('''(sel) => {
            function findElement(root, s) {
                if (!root) return null;
                let el = root.querySelector(s);
                if (el) return el;
                let els = root.querySelectorAll('*');
                for (let e of els) {
                    if (e.shadowRoot) {
                        let found = findElement(e.shadowRoot, s);
                        if (found) return found;
                    }
                }
                return null;
            }
            let target = findElement(document, sel);
            if (target) {
                target.scrollIntoView({block: 'center', inline: 'center'});
                target.click();
                return true;
            }
            throw new Error("Selector not found in main or shadow DOM");
        }''', selector)
        await page.wait_for_timeout(1000)
        return True
    except Exception as e:
        print(f"Bypass failed: {e}")
        return False
