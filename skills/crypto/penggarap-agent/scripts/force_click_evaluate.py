# Metadata: Generic, Date, Symptom
async def force_click_evaluate(page, selector):
    await page.evaluate(f'''(selector) => {{
        const el = document.querySelector(selector);
        if (el) {{
            const ev1 = new MouseEvent('mousedown', {{bubbles: true, cancelable: true, view: window}});
            const ev2 = new MouseEvent('mouseup', {{bubbles: true, cancelable: true, view: window}});
            const ev3 = new MouseEvent('click', {{bubbles: true, cancelable: true, view: window}});
            el.dispatchEvent(ev1);
            el.dispatchEvent(ev2);
            el.dispatchEvent(ev3);
        }}
    }}''', selector)
