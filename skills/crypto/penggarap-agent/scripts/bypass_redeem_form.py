# Metadata:
# Origin Domain: commonsmade.com
# Date: 2026-08-23
# Specific Symptom: Automated redeem form submission failing or timing out without explicit DOM.

import asyncio

async def bypass_redeem_form(page, code_value: str, input_selector: str = 'input[type="text"], input[name*="code" i], input[placeholder*="code" i]', submit_selector: str = 'button[type="submit"], button:has-text("Redeem"), button:has-text("Submit"), button:has-text("Claim")'):
    """
    Generic bypass to locate a redeem code input field, fill it, and submit.
    """
    try:
        input_element = await page.wait_for_selector(input_selector, state='visible', timeout=15000)
        if not input_element:
            raise Exception(f"Input selector {input_selector} not found.")
        
        await input_element.scroll_into_view_if_needed()
        await input_element.click()
        await input_element.fill(code_value)
        
        submit_element = await page.wait_for_selector(submit_selector, state='visible', timeout=5000)
        if not submit_element:
            raise Exception(f"Submit selector {submit_selector} not found.")
            
        await submit_element.scroll_into_view_if_needed()
        await submit_element.click()
        
        try:
            await page.wait_for_load_state('networkidle', timeout=10000)
        except:
            pass # Ignore networkidle timeout if action succeeds
            
        return True
        
    except Exception as e:
        print(f"Bypass failed: {str(e)}")
        return False
