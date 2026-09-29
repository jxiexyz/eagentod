# Metadata: Origin Domain: hub.axisrobotics.ai (Generic), Date: 2026-08-22, Symptom: Invite code gate blocking automated login progression
import asyncio

async def bypass_invite_login(page, invite_code: str, input_sel: str = "input[placeholder*='code' i], input[name*='invite' i], input[type='text']", btn_sel: str = "button:has-text('Submit'), button:has-text('Login'), button:has-text('Confirm'), button:has-text('Enter')"):
    """Generically waits for and fills an invite code barrier, then submits."""
    try:
        await page.wait_for_selector(input_sel, state="visible", timeout=10000)
        await page.fill(input_sel, invite_code)
        await asyncio.sleep(0.5)  # Humanize input
        await page.click(btn_sel)
        await page.wait_for_load_state('networkidle', timeout=15000)
        return True
    except Exception as e:
        print(f"[Mechanic] Invite login bypass failed: {e}")
        return False
