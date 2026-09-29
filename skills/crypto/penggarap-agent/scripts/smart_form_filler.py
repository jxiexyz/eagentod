# Metadata: teogiwa.com, 2026-08-24, Dynamic registration/OAuth form element resolution failure

async def fill_and_submit(page, target_texts, ref_code=None):
    """Bypass for dynamic or shadow DOM forms. Locates inputs by loose heuristics and clicks target buttons."""
    try:
        await page.wait_for_load_state('domcontentloaded', timeout=10000)
        if ref_code:
            for selector in ['input[name*="ref" i]', 'input[name*="code" i]', 'input[placeholder*="code" i]']:
                elements = await page.locator(selector).all()
                if elements:
                    await elements[0].fill(ref_code)
                    break
        
        for text in target_texts:
            btn = page.locator(f'button:has-text("{text}"), a:has-text("{text}"), div[role="button"]:has-text("{text}")').first
            if await btn.is_visible():
                await btn.click()
                return True
        return False
    except Exception as e:
        print(f"Smart fill failed: {e}")
        return False
