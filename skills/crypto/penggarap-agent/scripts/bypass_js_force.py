# Metadata: app.zen-o.xyz, 2026-08-23, Generic Element Interception/Unreachable
import asyncio

async def bypass_action(page, selector, action="click", text=None):
    """
    Bypass Playwright interception/visibility errors via direct DOM execution.
    """
    try:
        await page.wait_for_selector(selector, state="attached", timeout=10000)
        if action == "click":
            await page.evaluate(f"document.querySelector('{selector}').click()")
        elif action == "fill" and text:
            await page.evaluate(f"document.querySelector('{selector}').value = '{text}'")
            await page.evaluate(f"document.querySelector('{selector}').dispatchEvent(new Event('input', {{ bubbles: true }}))")
            await page.evaluate(f"document.querySelector('{selector}').dispatchEvent(new Event('change', {{ bubbles: true }}))")
        return True
    except Exception as e:
        print(f"[Mechanic] JS bypass failed for {selector}: {e}")
        return False
