# Metadata: Domain: rpg.cash, Date: 2026-08-27, Symptom: Phaser canvas with DOM overlays blocking standard Playwright interaction

import asyncio

async def interact_with_dom_overlay(page, selector: str, action: str = "click", value: str = None):
    """
    Interact with DOM elements injected over a canvas (e.g., Phaser.DOM.GameObjectFactory).
    Playwright often fails to click these natively because they are layered above/below the canvas context.
    """
    try:
        if action == "click":
            await page.evaluate('''([sel]) => {
                const elements = document.querySelectorAll(sel);
                elements.forEach(el => {
                    if (!el.disabled) el.click();
                });
            }''', [selector])
        elif action == "fill" and value is not None:
            await page.evaluate('''([sel, val]) => {
                const el = document.querySelector(sel);
                if (el) {
                    el.value = val;
                    el.dispatchEvent(new Event('input', { bubbles: true }));
                    el.dispatchEvent(new Event('change', { bubbles: true }));
                }
            }''', [selector, value])
            
        await asyncio.sleep(1)
        return True
    except Exception as e:
        print(f"Error interacting with overlay: {e}")
        return False

async def claim_all_quests(page, claim_selector: str = "[data-quest]:not([disabled])"):
    """
    Finds and clicks all claimable quest buttons in the DOM overlay, iterating until exhausted.
    """
    try:
        while True:
            # Fetch clickable quests avoiding visually 'claimed' states if class differs
            has_clickable = await page.evaluate('''([sel]) => {
                const elements = Array.from(document.querySelectorAll(sel));
                const el = elements.find(e => !e.disabled && !e.classList.contains('is-claimed'));
                if (el) {
                    el.click();
                    return true;
                }
                return false;
            }''', [claim_selector])
            
            if not has_clickable:
                break
                
            await asyncio.sleep(3) # Wait for network request and claim animation
            
        return True
    except Exception as e:
        print(f"Error claiming quests: {e}")
        return False
