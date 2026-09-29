# Metadata: evoevo.ai, 2026-08-25, Sim teleoperation environment mission completion blocking worker
import asyncio
import logging

logger = logging.getLogger(__name__)

async def bypass_sim_mission(page, target_selector="canvas"):
    """
    Generic bypass for interacting with sim teleoperation environments (e.g., Real World missions).
    """
    logger.info(f"Attempting to bypass sim environment using selector: {target_selector}")
    try:
        await page.wait_for_selector(target_selector, state="visible", timeout=15000)
        element = await page.query_selector(target_selector)
        
        if not element:
            return False
            
        box = await element.bounding_box()
        if not box:
            return False

        # Default teleop action: Click center, drag slightly
        cx = box['x'] + box['width'] / 2
        cy = box['y'] + box['height'] / 2
        
        await page.mouse.move(cx, cy)
        await page.mouse.down()
        await page.mouse.move(cx + 50, cy + 50, steps=10)
        await page.mouse.up()
        await asyncio.sleep(2)
        
        return True
    except Exception as e:
        logger.error(f"Failed sim bypass: {str(e)}")
        return False
