# Metadata: app.rally.fun, 2026-08-21, Button unclickable or ignores native Playwright clicks during tweet submission
async def bypass_waitlist_submit(page, selector='button:has-text("Submit tweet")'):
    await page.evaluate(f'''(selector) => {{
        const el = document.querySelector(selector);
        if (el) {{
            el.removeAttribute('disabled');
            const ev = new MouseEvent('click', {{bubbles: true, cancelable: true, view: window}});
            el.dispatchEvent(ev);
        }}
    }}''', selector)