# Origin Domain: inkarians.xyz (Embedded Google Forms)
# Date: 2026-08-25
# Symptom: Cannot interact with form elements because they are trapped inside a cross-origin iframe.

import asyncio

async def fill_iframe_form(page, iframe_selector: str, form_data: dict, submit_selector: str = None):
    """
    Bypasses iframe boundaries to fill a form (e.g., Google Forms) embedded in a page.
    form_data: dict mapping selectors to input values.
    """
    print(f"Waiting for iframe: {iframe_selector}")
    iframe_element = await page.wait_for_selector(iframe_selector, state="attached")
    frame = await iframe_element.content_frame()
    
    if not frame:
        raise Exception(f"Could not resolve frame for selector: {iframe_selector}")

    print("Frame resolved. Filling data...")
    for selector, value in form_data.items():
        await frame.wait_for_selector(selector, state="visible")
        await frame.fill(selector, value)
        await asyncio.sleep(0.5)

    if submit_selector:
        print(f"Clicking submit: {submit_selector}")
        await frame.click(submit_selector)
        await asyncio.sleep(2)
        
    return True
