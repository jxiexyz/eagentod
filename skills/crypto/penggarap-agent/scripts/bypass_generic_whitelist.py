# Metadata: Domain: justbanners.art, Date: 2026-08-22, Symptom: Automation blocked on whitelist signup page (session 20260822_083204_4c622d)

async def bypass(page, target_selectors=None):
    if target_selectors is None:
        target_selectors = ['button:has-text("Join")', 'button:has-text("Register")', 'button:has-text("Submit")', 'button:has-text("Connect")']
    
    try:
        await page.wait_for_load_state('networkidle', timeout=10000)
    except Exception:
        pass
    
    await page.wait_for_timeout(2000)
    
    for selector in target_selectors:
        try:
            elements = await page.query_selector_all(selector)
            for el in elements:
                if await el.is_visible():
                    await el.scroll_into_view_if_needed()
                    await el.click(force=True)
                    await page.wait_for_timeout(1000)
        except Exception:
            continue
            
    return True