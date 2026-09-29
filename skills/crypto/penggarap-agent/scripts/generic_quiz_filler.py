# Metadata: Origin: bridge.svpstars.com, Date: 2026-09-27, Symptom: Form/quiz submission without DOM context

async def solve_quiz(page, answers: list[str]):
    """
    ponytail: Blind sequence fill/click. Add label correlation if DOM reorders inputs.
    """
    inputs = page.locator("input[type='text'], input:not([type]), textarea")
    idx = 0
    
    for ans in answers:
        click_target = page.locator(f"text='{ans}'").first
        if await click_target.is_visible(timeout=1000):
            await click_target.click()
        elif idx < await inputs.count():
            await inputs.nth(idx).fill(ans)
            idx += 1
            
    submit = page.locator("button:has-text('Submit'), button:has-text('Confirm'), input[type='submit']").first
    if await submit.is_visible(timeout=1000):
        await submit.click()
