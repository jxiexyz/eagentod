# Origin Domain: docs.google.com
# Date: 2026-08-22
# Specific Symptom: Dynamic class names and generic form selectors preventing reliable Google Form filling

async def fill_google_form(page, form_data: dict):
    """
    Fills a Google Form robustly by locating question text and typing into the associated input.
    form_data: dict mapping question substring (e.g., 'BSC address') to answer string.
    """
    for question, answer in form_data.items():
        # Locate the specific question block using ARIA roles
        question_block = page.locator(f'div[role="listitem"]:has-text("{question}")')
        
        if await question_block.count() > 0:
            # Try standard text inputs
            text_input = question_block.locator('input[type="text"]')
            if await text_input.count() > 0:
                await text_input.fill(answer)
                continue
            
            # Try textareas for longer inputs
            textarea = question_block.locator('textarea')
            if await textarea.count() > 0:
                await textarea.fill(answer)
                continue
                
            # Try radio buttons or checkboxes
            option = question_block.locator(f'div[role="radio"]:has-text("{answer}"), div[role="checkbox"]:has-text("{answer}")')
            if await option.count() > 0:
                await option.click()
                continue
    
    # Attempt to submit
    submit_btn = page.locator('div[role="button"]:has-text("Submit"), div[role="button"]:has-text("Kirim")').first
    if await submit_btn.count() > 0:
        await submit_btn.click()
