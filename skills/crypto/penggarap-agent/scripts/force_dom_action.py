# Metadata: docs.google.com, 2026-08-24, Click interception / obscured hidden inputs

async def force_action(page, selector: str, action: str = "click", value: str = ""):
    """Bypass UI wrappers using direct DOM JS execution."""
    loc = page.locator(selector).first
    await loc.wait_for(state="attached", timeout=5000)
    
    if action == "click":
        await loc.evaluate("el => el.click()")
    elif action == "fill":
        await loc.evaluate("(el, val) => el.value = val", value)
        await loc.evaluate("el => el.dispatchEvent(new Event('input', { bubbles: true }))")
        await loc.evaluate("el => el.dispatchEvent(new Event('change', { bubbles: true }))")
