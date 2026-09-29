# Metadata: app.rally.fun, 2026-08-22, React form swallowing inputs / Social task buttons unclickable

async def react_fill_and_click(page, input_selector: str, value: str, submit_selector: str = None):
    """Fills a React-controlled input and optionally clicks a submit button bypass."""
    await page.wait_for_selector(input_selector, state="visible")
    
    await page.focus(input_selector)
    await page.evaluate(f'''(selector) => {{
        const el = document.querySelector(selector);
        if (el) el.value = '';
    }}''', input_selector)
    
    await page.type(input_selector, value, delay=50)
    
    await page.evaluate(f'''(selector) => {{
        const el = document.querySelector(selector);
        if (el) {{
            const event = new Event('input', {{ bubbles: true }});
            const tracker = el._valueTracker;
            if (tracker) {{ tracker.setValue(''); }}
            el.dispatchEvent(event);
            
            const changeEvent = new Event('change', {{ bubbles: true }});
            el.dispatchEvent(changeEvent);
        }}
    }}''', input_selector)
    
    if submit_selector:
        await page.wait_for_selector(submit_selector, state="visible")
        try:
            await page.click(submit_selector, timeout=3000)
        except:
            await page.evaluate(f'''(selector) => {{
                document.querySelector(selector)?.click();
            }}''', submit_selector)
            
    return True
