# Metadata: chatlee.io, 2026-08-21, Cloudflare Turnstile verification prevents form submission
import asyncio

async def bypass_turnstile(page, timeout=30000):
    """
    Reusable bypass script for Cloudflare Turnstile challenges.
    Locates the Turnstile widget iframe, clicks it to initiate the challenge if needed,
    and waits for the 'cf-turnstile-response' input to be populated with a valid token.
    """
    print("[*] Scanning for Cloudflare Turnstile widget...")
    try:
        # Check if the site uses Turnstile by looking for the token input
        turnstile_input = await page.query_selector('input[name="cf-turnstile-response"]')
        if not turnstile_input:
            print("[-] No Turnstile input found on this page.")
            return False

        # Wait for the Turnstile iframe to become visible
        iframe = await page.wait_for_selector('iframe[src*="challenges.cloudflare.com"]', timeout=10000)
        if iframe:
            print("[*] Turnstile iframe found. Attempting interaction...")
            # Attempt to click the center of the widget
            box = await iframe.bounding_box()
            if box:
                x = box['x'] + (box['width'] / 2)
                y = box['y'] + (box['height'] / 2)
                await page.mouse.click(x, y)
                print("[*] Clicked Turnstile widget bounding box.")
            else:
                await iframe.click(force=True)
                print("[*] Force clicked Turnstile iframe.")

        print("[*] Waiting for cf-turnstile-response token generation...")
        # Poll until the token is injected into the DOM
        await page.wait_for_function(
            '''() => {
                const tokenInput = document.querySelector('input[name="cf-turnstile-response"]');
                return tokenInput && tokenInput.value && tokenInput.value.length > 20;
            }''',
            timeout=timeout
        )
        
        token = await page.evaluate('document.querySelector(\'input[name="cf-turnstile-response"]\').value')
        print(f"[+] Turnstile solved successfully. Token length: {len(token)}")
        return True

    except Exception as e:
        print(f"[-] Turnstile bypass failed or timed out: {str(e)}")
        return False
