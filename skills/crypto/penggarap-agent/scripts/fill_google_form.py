# Metadata: Origin Domain: inkarians.xyz | Date: 2026-08-25 | Symptom: Standard automation fails to locate or fill Google Form fields (iframed or direct)

async def execute(page, answers: list, iframe_selector: str = None):
    target = page
    if iframe_selector:
        frame_element = await page.wait_for_selector(iframe_selector, timeout=5000)
        if frame_element:
            target = await frame_element.content_frame()

    await target.wait_for_load_state('networkidle')
    
    inputs = await target.query_selectors('input[type="text"], input[type="email"], textarea')
    
    for i, answer in enumerate(answers):
        if i < len(inputs):
            await inputs[i].fill(str(answer))
    
    submit_btn = await target.query_selector('div[role="button"] span:has-text("Submit"), div[role="button"] span:has-text("Kirim")')
    if not submit_btn:
         buttons = await target.query_selectors('div[role="button"]')
         if buttons:
             submit_btn = buttons[-1]
             
    if submit_btn:
        await submit_btn.click()
        await target.wait_for_timeout(2000)
        return True
    return False