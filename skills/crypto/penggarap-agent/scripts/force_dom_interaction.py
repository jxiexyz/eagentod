# Metadata: Domain: inkvikings.xyz, Date: 2026-08-24, Symptom: Element not interactable / Waitlist button blocked by overlay

async def force_interact(page, selector, action='click', value=''):
    """
    Bypass strict visibility/interactability checks in Playwright/Puppeteer
    by executing actions directly via client-side JavaScript.
    """
    if action == 'click':
        await page.evaluate('''([sel]) => {
            const el = document.querySelector(sel);
            if (el) {
                el.scrollIntoView({block: 'center', behavior: 'instant'});
                el.click();
            }
        }''', [selector])
    elif action == 'fill':
        await page.evaluate('''([sel, val]) => {
            const el = document.querySelector(sel);
            if (el) {
                el.focus();
                el.value = val;
                el.dispatchEvent(new Event('input', { bubbles: true }));
                el.dispatchEvent(new Event('change', { bubbles: true }));
            }
        }''', [selector, value])