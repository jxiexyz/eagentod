# Metadata: Origin: app.stabilizer.finance | Date: 2026-08-23 | Symptom: Profile connection modal automation failure
import asyncio
from playwright.async_api import Page

async def bypass_profile_connect(page: Page, connect_selector: str = "text='Connect'"):
    try:
        await page.wait_for_selector(connect_selector, state="visible", timeout=10000)
        await page.click(connect_selector)
        await page.wait_for_timeout(2000)
        
        wallet_selectors = [
            "text='MetaMask'", 
            "text='Injected'", 
            "text='Browser Wallet'",
            "[data-testid*='metaMask']",
            "button:has-text('MetaMask')"
        ]
        for sel in wallet_selectors:
            btn = await page.query_selector(sel)
            if btn:
                await btn.click()
                break
                
        await page.wait_for_timeout(3000)
        return True
    except Exception as e:
        print(f"Profile connection bypass failed: {e}")
        return False
