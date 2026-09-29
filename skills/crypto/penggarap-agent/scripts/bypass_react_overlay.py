# Origin Domain: app.meridian.xyz
# Date: 2026-08-22
# Symptom: Web automation click failure (session 20260822_030829_d80d45) - likely React synthetic event block or transparent overlay

async def force_click(page, selector: str):
    """
    Dispatches native mouse events directly to the element to bypass React/Vue event pooling
    and invisible CSS overlay blockers.
    """
    await page.wait_for_selector(selector, state="attached")
    await page.evaluate(
        "(sel) => {\n"
        "  const el = document.querySelector(sel);\n"
        "  if (!el) throw new Error('Element not found: ' + sel);\n"
        "  ['pointerdown', 'mousedown', 'pointerup', 'mouseup', 'click'].forEach(type => {\n"
        "    el.dispatchEvent(new MouseEvent(type, { bubbles: true, cancelable: true, view: window }));\n"
        "  });\n"
        "}",
        selector
    )