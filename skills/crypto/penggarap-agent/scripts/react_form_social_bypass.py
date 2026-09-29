# Metadata: spinelab.fun, 2026-08-25, React form state not updating on standard fill and social link clicks hanging
import asyncio

async def robust_react_fill(page, selector: str, text: str):
    """Fills an input bypassing standard React state blockers."""
    await page.wait_for_selector(selector, state='visible', timeout=10000)
    await page.evaluate(f'''(sel, val) => {{
        const el = document.querySelector(sel);
        if (!el) return;
        el.value = val;
        el.dispatchEvent(new Event('input', {{ bubbles: true }}));
        el.dispatchEvent(new Event('change', {{ bubbles: true }}));
    }}''', selector, text)
    await page.type(selector, text, delay=50)

async def handle_social_click(page, context, selector: str):
    """Clicks a social link and closes the resulting tab immediately to bypass auth hangs."""
    await page.wait_for_selector(selector, state='visible', timeout=10000)
    async with context.expect_page() as new_page_info:
        await page.click(selector, force=True)
    new_page = await new_page_info.value
    await new_page.wait_for_load_state('domcontentloaded')
    await asyncio.sleep(2)
    await new_page.close()
