# Origin Domain: generic (triggered by bridge.svpstars.com)
# Date: 2026-09-27
# Symptom: Need robust quiz answer submission mechanism for mixed input types (buttons/radios/text)

async def submit_quiz_answers(page, answers, submit_button_selector="button[type='submit'], button:has-text('Submit'), button:has-text('Verify')"):
    """
    Generic quiz solver that clicks elements containing specific answer texts or fills inputs.
    """
    import asyncio

    for answer in answers:
        try:
            # If it's a URL or long string, try to fill empty text inputs first
            if answer.startswith('http') or len(answer) > 30:
                inputs = await page.locator("input[type='text'], input:not([type]), input[type='url'], textarea").all()
                filled = False
                for inp in inputs:
                    if await inp.is_visible() and await inp.is_editable() and not await inp.input_value():
                        await inp.fill(answer)
                        filled = True
                        break
                if filled:
                    await page.wait_for_timeout(500)
                    continue

            # Otherwise try clicking as a multiple choice option
            locator = page.get_by_text(answer, exact=False).first
            await locator.wait_for(state="visible", timeout=3000)
            await locator.click(force=True)
            await page.wait_for_timeout(500)
        except Exception as e:
            print(f"Playwright click failed for '{answer}': {e}")
            # JS fallback
            try:
                await page.evaluate(f'''(text) => {{
                    const elements = Array.from(document.querySelectorAll('div, span, button, p, a, label, li'));
                    const el = elements.find(e => e.textContent && e.textContent.includes(text));
                    if (el) el.click();
                }}''', answer)
                await page.wait_for_timeout(500)
            except Exception as e2:
                print(f"JS fallback failed for '{answer}': {e2}")

    if submit_button_selector:
        try:
            submit_btn = page.locator(submit_button_selector).first
            await submit_btn.wait_for(state="visible", timeout=3000)
            await submit_btn.click(force=True)
            await page.wait_for_load_state('networkidle', timeout=5000)
        except Exception as e:
            print(f"Submit button click failed: {e}")