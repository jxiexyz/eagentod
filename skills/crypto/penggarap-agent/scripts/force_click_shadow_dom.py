# Origin Domain: app.rally.fun
# Date: 2026-08-26
# Specific Symptom: Standard Playwright clicks fail on React/Shadow DOM campaign buttons

async def bypass_click(page, selector: str):
    await page.evaluate('''(sel) => {
        function findEl(root) {
            let el = root.querySelector(sel);
            if (el) return el;
            for (const child of root.querySelectorAll('*')) {
                if (child.shadowRoot) {
                    let res = findEl(child.shadowRoot);
                    if (res) return res;
                }
            }
            return null;
        }
        const target = findEl(document);
        if (target) {
            target.scrollIntoView({block: 'center', inline: 'center'});
            target.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }));
        } else {
            throw new Error('Element not found: ' + sel);
        }
    }''', selector)