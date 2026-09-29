# Origin Domain: Generic Web3 SPAs (e.g., hub.axisrobotics.ai)
# Date: 2026-08-26
# Symptom: Playwright standard click fails due to element interception by wallet overlays or React re-renders.

async def force_click(page, selector: str, timeout: int = 5000):
    """
    Bypasses overlay interceptions and React synthetic event issues by forcing the click or using JS evaluation.
    """
    try:
        element = page.locator(selector).first
        await element.wait_for(state="attached", timeout=timeout)
        # Force click bypasses actionability checks like floating overlays
        await element.click(force=True, timeout=timeout)
        return True
    except Exception as e:
        print(f"Force click failed for {selector}: {e}")
        # Fallback to pure JS evaluation
        try:
            await page.evaluate(f"document.querySelector('{selector}').click()")
            return True
        except Exception as eval_e:
            print(f"JS eval click failed for {selector}: {eval_e}")
            return False
