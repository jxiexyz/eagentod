# Metadata: 
# Origin Domain: register.divvy.bet (Generic X & SOL Wallet Auth)
# Date: 2026-08-23
# Symptom: Blocked at dual-step registration requiring X account binding and SOL wallet connection.

import asyncio

async def handle_x_oauth(page, context, x_btn_selector):
    async with context.expect_page() as new_page_info:
        await page.click(x_btn_selector)
    oauth_page = await new_page_info.value
    await oauth_page.wait_for_load_state('networkidle')
    
    # Click 'Authorize app' if presented (assumes persistent session already logged in)
    auth_btn = oauth_page.locator("button[data-testid='OAuth_Consent_Button']")
    if await auth_btn.is_visible():
        await auth_btn.click()
    
    # Wait for the OAuth popup to close and return control
    await oauth_page.wait_for_event('close')

async def inject_sol_wallet(page, address):
    # Mock Phantom wallet injection for headless Solana dApp connections
    await page.evaluate(f'''
        window.solana = {{
            isPhantom: true,
            publicKey: {{
                toString: () => "{address}",
                toBase58: () => "{address}"
            }},
            isConnected: true,
            connect: async () => ({{ publicKey: {{ toString: () => "{address}" }} }}),
            signMessage: async (msg) => ({{ signature: new Uint8Array(64) }}),
            on: () => {{}},
        }};
    ''')

async def execute_bypass(page, context, x_btn_selector, wallet_btn_selector, sol_address):
    # 1. Prepare environment
    await inject_sol_wallet(page, sol_address)
    
    # 2. Handle X OAuth popup flow
    if x_btn_selector:
        await handle_x_oauth(page, context, x_btn_selector)
        await page.wait_for_timeout(2000)

    # 3. Handle Wallet connection
    if wallet_btn_selector:
        await page.click(wallet_btn_selector)
        await page.wait_for_timeout(2000)
