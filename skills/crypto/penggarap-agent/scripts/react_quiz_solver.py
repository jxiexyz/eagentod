# Metadata
# Origin Domain: rewards.svpstars.com
# Date: 2026-09-20
# Symptom: Quiz elements blocked by React synthetic event interception or overlays.

import asyncio

async def force_react_click(page, selector: str):
    """Bypass intercepted clicks by dispatching native events directly via JS evaluation."""
    await page.evaluate('''
        (sel) => {
            const elements = document.querySelectorAll(sel);
            if (!elements || elements.length === 0) return;
            const el = elements[0];
            el.dispatchEvent(new MouseEvent('mousedown', {bubbles: true}));
            el.dispatchEvent(new MouseEvent('mouseup', {bubbles: true}));
            el.click();
        }
    ''', selector)

async def solve_quiz(page, option_selector: str, next_button_selector: str, max_iterations: int = 20):
    """Iterates through a quiz, bypassing click intercepts."""
    for _ in range(max_iterations):
        try:
            await page.wait_for_selector(option_selector, state='visible', timeout=3000)
            await force_react_click(page, option_selector)
            await asyncio.sleep(0.5)
            
            next_btn = await page.query_selector(next_button_selector)
            if next_btn:
                await force_react_click(page, next_button_selector)
                await asyncio.sleep(1)
        except Exception:
            break
