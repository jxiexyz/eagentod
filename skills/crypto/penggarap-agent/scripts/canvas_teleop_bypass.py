# Origin Domain: evoevo.ai
# Date: 2026-08-25
# Symptom: Fails to interact with sim teleoperation / Real World mission canvas

import asyncio

async def interact_with_canvas(page, selector="canvas", action_type="click", x=0, y=0, drag_to_x=None, drag_to_y=None):
    """
    Generic bypass for WebGL/Canvas based sim environments.
    Dispatches raw mouse events relative to the canvas bounding box to bypass DOM event blocking.
    """
    element = await page.wait_for_selector(selector, state="visible", timeout=10000)
    box = await element.bounding_box()
    
    if not box:
        raise ValueError(f"Bounding box not found for {selector}")
        
    # Default to center if coordinates are 0
    target_x = box['x'] + (box['width'] / 2 if x == 0 else x)
    target_y = box['y'] + (box['height'] / 2 if y == 0 else y)
    
    await page.mouse.move(target_x, target_y)
    
    if action_type == "click":
        await page.mouse.down()
        await asyncio.sleep(0.125)
        await page.mouse.up()
    elif action_type == "drag" and drag_to_x is not None and drag_to_y is not None:
        await page.mouse.down()
        await asyncio.sleep(0.1)
        end_x = box['x'] + drag_to_x
        end_y = box['y'] + drag_to_y
        await page.mouse.move(end_x, end_y, steps=15)
        await asyncio.sleep(0.125)
        await page.mouse.up()
    
    return True
