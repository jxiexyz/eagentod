# Metadata: Origin Domain: docs.google.com | Date: 2026-08-24 | Symptom: Playwright strict actionability checks failing on obscured or custom elements (e.g. div radios)

async def force_interact(page, selector: str, action: str = 'click', value: str = None):
    element = await page.wait_for_selector(selector, state='attached', timeout=10000)
    if not element:
        raise Exception(f"Selector {selector} not found")
    
    if action == 'click':
        await element.evaluate("el => el.click()")
    elif action == 'mouse_event':
        await element.evaluate("el => el.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true, view: window}))")
    elif action == 'fill' and value is not None:
        await element.evaluate("(el, val) => { el.value = val; el.dispatchEvent(new Event('input', {bubbles: true})); el.dispatchEvent(new Event('change', {bubbles: true})); }", arg=value)
    return True
