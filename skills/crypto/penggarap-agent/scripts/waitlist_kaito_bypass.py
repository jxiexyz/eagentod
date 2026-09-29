# Origin Domain: waitlist.gte.xyz (Kaito)
# Date: 2026-08-21
# Symptom: Failure to intercept X (Twitter) popup during Kaito waitlist "Post about Axis" action due to React synthetic event blocking or shadow DOM.

import asyncio

async def bypass_kaito_action(page, selector):
    """Forces native DOM click to bypass React event traps and captures the resulting popup."""
    try:
        # Start waiting for popup before clicking
        async with page.expect_popup(timeout=15000) as popup_info:
            # Evaluate native click to bypass standard Playwright actionability checks
            await page.evaluate(f'''(sel) => {{
                const el = document.querySelector(sel);
                if (el) {{ el.click(); }}
            }}''', selector)
        
        popup = await popup_info.value
        await popup.wait_for_load_state('domcontentloaded')
        return popup
    except Exception as e:
        print(f"Popup interception bypass failed for {selector}: {e}")
        return None
