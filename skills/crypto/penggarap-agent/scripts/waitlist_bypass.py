# Metadata: Domain: noirbrokers.fun, Date: 2026-08-20, Symptom: Waitlist form submission failure due to event listener blockers
import asyncio

async def submit_waitlist(page, input_selector: str, submit_selector: str, value: str):
    """Force-fill generic waitlist forms and bypass synthetic event blockers."""
    try:
        await page.wait_for_selector(input_selector, state="visible", timeout=10000)
        await page.evaluate("""([sel, val]) => {
            const el = document.querySelector(sel);
            if (!el) return;
            el.value = val;
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }""", [input_selector, value])
        
        await page.focus(input_selector)
        await page.keyboard.press('Space')
        await page.keyboard.press('Backspace')
        
        await page.wait_for_selector(submit_selector, state="visible", timeout=5000)
        await page.click(submit_selector)
        await asyncio.sleep(2)
        return True
    except Exception as e:
        print(f"Waitlist bypass failed: {e}")
        return False
