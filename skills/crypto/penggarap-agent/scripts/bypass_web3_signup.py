# Metadata: thor.savethelife.io, 2026-08-25, Generic Web3 signup form interception/blocking
import asyncio

async def bypass_web3_signup(page, address, twitter_handle=None, telegram_handle=None):
    """
    Bypasses standard Web3 signup forms by forcing value injection and JS clicks.
    Handles address inputs and common social fields when standard Playwright typing fails.
    """
    try:
        # Force inject address into any input likely to be a wallet address
        await page.evaluate(f'''(address) => {{
            const inputs = Array.from(document.querySelectorAll('input'));
            const walletInput = inputs.find(i => i.placeholder.toLowerCase().includes('bsc') || i.placeholder.toLowerCase().includes('address') || i.name.toLowerCase().includes('wallet'));
            if (walletInput) {{
                walletInput.value = address;
                walletInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                walletInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
        }}''', address)

        # Handle social handles if provided
        if twitter_handle or telegram_handle:
            await page.evaluate(f'''(xHandle, tgHandle) => {{
                const inputs = Array.from(document.querySelectorAll('input'));
                if (xHandle) {{
                    const xInput = inputs.find(i => i.placeholder.toLowerCase().includes('twitter') || i.name.toLowerCase().includes('twitter') || i.placeholder.toLowerCase().includes('x.com'));
                    if (xInput) {{ xInput.value = xHandle; xInput.dispatchEvent(new Event('input', {{ bubbles: true }})); }}
                }}
                if (tgHandle) {{
                    const tgInput = inputs.find(i => i.placeholder.toLowerCase().includes('telegram') || i.name.toLowerCase().includes('telegram'));
                    if (tgInput) {{ tgInput.value = tgHandle; tgInput.dispatchEvent(new Event('input', {{ bubbles: true }})); }}
                }}
            }}''', twitter_handle, telegram_handle)
        
        # Force click submit buttons (avoiding element interception)
        await page.evaluate('''() => {
            const buttons = Array.from(document.querySelectorAll('button, input[type="submit"]'));
            const submitBtn = buttons.find(b => b.innerText.toLowerCase().includes('submit') || b.innerText.toLowerCase().includes('sign up') || b.innerText.toLowerCase().includes('join') || b.value.toLowerCase().includes('submit'));
            if (submitBtn) submitBtn.click();
        }''')
        
        await asyncio.sleep(2)
        return True
    except Exception as e:
        print(f"Bypass failed: {e}")
        return False
