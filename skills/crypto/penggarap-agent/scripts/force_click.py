# Metadata: cloudquest.asia, 2026-08-27, Clicks intercepted or failing due to React/Shadow DOM overlays

async def force_click(page, selector: str, timeout: int = 5000):
    """Forces a click using multiple fallback strategies for stubborn social quest UIs."""
    try:
        await page.click(selector, timeout=timeout)
    except Exception:
        try:
            # JS native click bypasses overlays and pointer-events
            await page.evaluate(f"document.querySelector('{selector}').click()")
        except Exception:
            # Dispatch full MouseEvents for React synthetic event listeners
            await page.evaluate(f"""
                const el = document.querySelector('{selector}');
                if (el) {
                    ['pointerdown', 'mousedown', 'pointerup', 'mouseup', 'click'].forEach(type => {
                        el.dispatchEvent(new MouseEvent(type, { bubbles: true, cancelable: true, view: window }));
                    });
                }
            """)