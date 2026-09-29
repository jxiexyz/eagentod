# Origin Domain: docs.google.com
# Date: 2026-08-26
# Symptom: Event interception by ARIA overlays blocks standard Playwright clicks/fills.

async def bypass_aria_overlay(page, selector: str, action: str, value: str = ""):
    el = page.locator(selector).first
    await el.wait_for(state="attached", timeout=5000)
    if action == "click":
        await el.evaluate("e => e.click()")
    elif action == "fill":
        await el.fill(value, force=True)
        await el.evaluate("e => { e.dispatchEvent(new Event('input', {bubbles: true})); e.dispatchEvent(new Event('change', {bubbles: true})); }")
