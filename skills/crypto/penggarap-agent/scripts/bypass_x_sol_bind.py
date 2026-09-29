# Origin Domain: register.divvy.bet
# Date: 2026-08-23
# Symptom: Fails to bind X account and connect SOL address due to popup blocking and wallet detection failure.

import asyncio
from playwright.async_api import Page, BrowserContext

async def inject_phantom_mock(page: Page, pubkey: str):
    script = f"""
        window.solana = {{
            isPhantom: true,
            publicKey: {{ toString: () => '{pubkey}' }},
            isConnected: true,
            connect: async () => ({{ publicKey: {{ toString: () => '{pubkey}' }} }}),
            signMessage: async () => ({{ signature: new Uint8Array(64) }}),
            on: () => {{}},
            request: async (req) => {{
                if (req.method === 'connect') return {{ publicKey: '{pubkey}' }};
                return null;
            }}
        }};
    """
    await page.add_init_script(script)

async def handle_x_oauth_popup(page: Page, context: BrowserContext, trigger_selector: str):
    async with context.expect_page() as popup_info:
        await page.click(trigger_selector)
    popup = await popup_info.value
    await popup.wait_for_load_state('domcontentloaded')
    
    auth_btn = popup.locator("[value='Authorize app'], button:has-text('Authorize')")
    if await auth_btn.count() > 0:
        await auth_btn.first.click()
        try:
            await popup.wait_for_event('close', timeout=10000)
        except Exception:
            pass

async def bypass_x_sol_bind(page: Page, context: BrowserContext, x_btn_sel: str, sol_btn_sel: str, sol_pubkey: str):
    await inject_phantom_mock(page, sol_pubkey)
    await page.reload()
    
    if sol_btn_sel:
        await page.click(sol_btn_sel)
        await asyncio.sleep(2)
        
    if x_btn_sel:
        await handle_x_oauth_popup(page, context, x_btn_sel)
