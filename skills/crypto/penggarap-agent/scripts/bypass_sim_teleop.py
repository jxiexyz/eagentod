# Metadata:
# Origin Domain: testnet.x1ecochain.com, fortunefoes.com
# Date: 2026-08-25
# Symptom: Sim teleoperation environment / Paper trading mission blocking standard DOM clicks, requiring coordinate-based interactions. Missing mouse.up() causing interaction hangs.

import asyncio

async def bypass_sim_teleop(page, selector="canvas", x_offset=0, y_offset=0):
    """
    Bypasses standard DOM interaction blocks by clicking via raw mouse coordinates.
    Useful for canvas-based 'teleoperation', WebGL environments, or paper trading charts.
    """
    element = await page.wait_for_selector(selector, state="attached")
    box = await element.bounding_box()
    
    if not box:
        raise Exception(f"Could not get bounding box for {selector}")
        
    x = box["x"] + (box["width"] / 2) + x_offset
    y = box["y"] + (box["height"] / 2) + y_offset
    
    await page.mouse.move(x, y)
    await asyncio.sleep(0.1)
    await page.mouse.down()
    await asyncio.sleep(0.1)
    await page.mouse.up()
    return True
