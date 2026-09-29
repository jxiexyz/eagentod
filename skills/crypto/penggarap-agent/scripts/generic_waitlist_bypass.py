# Metadata: Domain: sporefolks.fun, Date: 2026-08-25, Symptom: Waitlist quest interaction failure / element intercepted

async def bypass_waitlist_action(page, selector, text_to_fill=None):
    try:
        await page.wait_for_selector(selector, state='attached', timeout=5000)
        if text_to_fill:
            await page.evaluate('''([sel, txt]) => {
                const el = document.querySelector(sel);
                if(el) {
                    el.value = txt;
                    el.dispatchEvent(new Event('input', {bubbles: true}));
                    el.dispatchEvent(new Event('change', {bubbles: true}));
                }
            }''', [selector, text_to_fill])
        else:
            await page.evaluate('''([sel]) => {
                const el = document.querySelector(sel);
                if(el) el.click();
            }''', [selector])
        return True
    except Exception as e:
        print(f"Bypass error: {e}")
        return False
