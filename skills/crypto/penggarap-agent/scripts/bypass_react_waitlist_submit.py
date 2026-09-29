# Metadata: sporefolks.fun, 2026-08-25, Waitlist form React state/click interception
async def bypass(page, input_selector="input[type='email']", btn_selector="button[type='submit']", input_value=""):
    try:
        await page.wait_for_selector(input_selector, state="visible", timeout=5000)
        await page.evaluate(f'''(sel, val) => {{
            const el = document.querySelector(sel);
            if (el) {{
                const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                setter.call(el, val);
                el.dispatchEvent(new Event('input', { bubbles: true }));
                el.dispatchEvent(new Event('change', { bubbles: true }));
            }}
        }}''', input_selector, input_value)
        await page.evaluate(f'''(sel) => {{
            const btn = document.querySelector(sel);
            if (btn) btn.click();
        }}''', btn_selector)
        await page.wait_for_timeout(2000)
        return True
    except Exception as e:
        print(f"Bypass failed: {e}")
        return False