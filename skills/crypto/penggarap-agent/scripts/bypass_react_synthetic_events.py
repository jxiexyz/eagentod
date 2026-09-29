# Metadata: Origin Domain: rewards.svpstars.com | Date: 2026-09-25 | Symptom: Unable to interact with task buttons or read hidden launch code due to React/synthetic event blocking or invisible DOM elements.
import asyncio

async def force_click_and_extract(page, click_selector: str, extract_selector: str = None):
    """
    Forcefully clicks an element bypassing React synthetic event blocks,
    and optionally extracts text from another element.
    """
    try:
        # Force click using JS to bypass Playwright's actionability checks
        await page.evaluate(f'''(selector) => {{
            const el = document.querySelector(selector);
            if (el) {{
                ['mousedown', 'mouseup', 'click'].forEach(eventType => {{
                    const event = new MouseEvent(eventType, {{
                        view: window,
                        bubbles: true,
                        cancelable: true,
                        buttons: 1
                    }});
                    el.dispatchEvent(event);
                }});
            }}
        }}''', click_selector)
        
        await page.wait_for_timeout(2000)

        if extract_selector:
            try:
                text = await page.locator(extract_selector).text_content(timeout=2000)
                return text.strip() if text else None
            except Exception:
                text = await page.evaluate(f'''(selector) => {{
                    const el = document.querySelector(selector);
                    return el ? (el.innerText || el.textContent) : null;
                }}''', extract_selector)
                return text.strip() if text else None
        return True
    except Exception as e:
        print(f"Bypass failed: {e}")
        return False
