# Metadata: commonsmade.com, 2026-08-24, React form submission button stays disabled on programmatic fill
import asyncio

async def bypass_fill(page, input_sel: str, btn_sel: str, text: str):
    await page.wait_for_selector(input_sel, state="visible")
    await page.click(input_sel)
    await page.fill(input_sel, "")
    await page.type(input_sel, text, delay=200)
    
    # Force synthetic event dispatch for stubborn framework state
    await page.evaluate(f"""
        const el = document.querySelector('{input_sel}');
        if (el) {{
            el.dispatchEvent(new Event('input', {{ bubbles: true }}));
            el.dispatchEvent(new Event('change', {{ bubbles: true }}));
        }}
    """)
    
    await asyncio.sleep(1)
    await page.wait_for_selector(btn_sel, state="visible")
    await page.click(btn_sel)
    await asyncio.sleep(2)
    return True
