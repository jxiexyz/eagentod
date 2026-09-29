# Metadata: testnet.x1ecochain.com, 2026-08-25, Sim teleoperation environment bot detection

import random
import asyncio

async def human_teleoperate_action(page, selector: str, action_type: str = 'click'):
    """Perform human-like teleoperated mouse movements to bypass sim detection."""
    element = await page.wait_for_selector(selector, state='visible', timeout=10000)
    box = await element.bounding_box()
    if not box:
        raise ValueError(f"Element {selector} not visible or no bounding box")
    
    target_x = box['x'] + (box['width'] / 2)
    target_y = box['y'] + (box['height'] / 2)
    
    # Emulate human jitter and approach
    start_x = target_x + random.uniform(-200, 200)
    start_y = target_y + random.uniform(-200, 200)
    await page.mouse.move(start_x, start_y)
    await asyncio.sleep(random.uniform(0.1, 0.3))
    
    steps = random.randint(5, 10)
    for i in range(1, steps + 1):
        progress = i / steps
        curve_x = target_x if i == steps else start_x + (target_x - start_x) * progress + random.uniform(-10, 10)
        curve_y = target_y if i == steps else start_y + (target_y - start_y) * progress + random.uniform(-10, 10)
        await page.mouse.move(curve_x, curve_y)
        await asyncio.sleep(random.uniform(0.01, 0.05))
        
    await asyncio.sleep(random.uniform(0.1, 0.4))
    if action_type == 'click':
        await page.mouse.down()
        await asyncio.sleep(random.uniform(0.05, 0.15))
        await page.mouse.up()
    return True
