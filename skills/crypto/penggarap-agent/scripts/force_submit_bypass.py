# Metadata: Generic, Date, Symptom
async def force_submit_bypass(page, selector):
    await page.evaluate(f'''(selector) => {{
        const btn = document.querySelector(selector);
        if (btn) {{
            btn.removeAttribute('disabled');
            btn.classList.remove('disabled');
            btn.click();
        }}
    }}''', selector)
