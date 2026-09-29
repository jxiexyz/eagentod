# React 6-Digit OTP Form Bypass

Forms requiring a 6-digit OTP often use 6 individual `<input>` elements. Native `browser_type` or standard Playwright `page.fill()` on the first input will usually fail to populate the subsequent boxes.

Use this Playwright CDP snippet to reliably inject the OTP code into all 6 inputs sequentially and trigger React's state update.

```python
import asyncio
from playwright.async_api import async_playwright
import time

async def type_otp(code, url_substring="allox.ai"):
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        context = browser.contexts[0]
        
        # Find the correct tab
        page = next((p_ for p_ in context.pages if url_substring in p_.url), None)
        if page:
            await page.bring_to_front()
            
            # Approach 1: Native Playwright (if inputs are reachable and interactable)
            inputs = await page.locator('div[role="dialog"] input').all()
            if len(inputs) == 6:
                for i in range(6):
                    await inputs[i].fill(code[i])
            else:
                # Approach 2: JS Event Dispatch Bypass (For stubborn React states)
                await page.evaluate(f'''() => {{
                    const inputs = document.querySelectorAll('div[role="dialog"] input'); // Adjust selector if needed
                    if(inputs.length >= 6) {{
                        const code = '{code}';
                        for(let i=0; i<6; i++) {{
                            inputs[i].value = code[i];
                            inputs[i].dispatchEvent(new Event('input', {{ bubbles: true }}));
                            inputs[i].dispatchEvent(new Event('change', {{ bubbles: true }}));
                        }}
                    }}
                }}''')
            time.sleep(3)
        else:
            print(f'Target page with {url_substring} not found')

# Example usage:
# asyncio.run(type_otp('476610', 'allox.ai'))
```
