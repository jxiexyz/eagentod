# Metadata: Origin Domain: tally.so, Date: 2026-08-26, Symptom: Form inputs unfillable due to custom React rendering or iframe encapsulation

import asyncio

async def bypass_form_fill(page, fields_dict, submit_text='Submit'):
    '''
    Fills custom forms by targeting iframes, placeholders, and labels dynamically.
    fields_dict: dict of { "label/placeholder substring": "value" }
    '''
    target_frame = page
    for frame in page.frames:
        if await frame.locator('input, textarea').count() > 0:
            target_frame = frame
            break

    await target_frame.wait_for_selector('input, textarea', state='visible', timeout=10000)

    for key, val in fields_dict.items():
        placeholder_loc = target_frame.locator(f'input[placeholder*="{key}" i], textarea[placeholder*="{key}" i]')
        if await placeholder_loc.count() > 0:
            await placeholder_loc.first.fill(str(val))
            continue

        label_loc = target_frame.locator(f'label:has-text("{key}")')
        if await label_loc.count() > 0:
            input_id = await label_loc.first.get_attribute('for')
            if input_id:
                await target_frame.locator(f'#{input_id}').fill(str(val))
                continue
            
            nested_input = label_loc.first.locator('input, textarea')
            if await nested_input.count() > 0:
                await nested_input.first.fill(str(val))
                continue

    submit_btn = target_frame.locator(f'button:has-text("{submit_text}"), button[type="submit"]')
    if await submit_btn.count() > 0:
        await submit_btn.first.click()
