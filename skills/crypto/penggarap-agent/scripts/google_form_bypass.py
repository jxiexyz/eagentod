# Metadata: Origin docs.google.com, Date 2026-08-27, Symptom dynamic DOM input targeting failure

async def bypass_google_form(page, form_data: dict):
    for question, answer in form_data.items():
        container = page.locator(f'div[role="listitem"]:has-text("{question}")').first
        text_input = container.locator('input[type="text"], input[type="email"]').first
        if await text_input.count() > 0:
            await text_input.fill(str(answer))
            continue
        textarea = container.locator('textarea').first
        if await textarea.count() > 0:
            await textarea.fill(str(answer))
            continue
        choice = container.locator(f'[data-value="{answer}"]').first
        if await choice.count() > 0:
            await choice.click()
            continue

    submit_btn = page.locator('div[role="button"]:has-text("Submit"), div[role="button"]:has-text("Kirim")').first
    if await submit_btn.count() > 0:
        await submit_btn.click()
