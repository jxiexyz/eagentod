# Metadata: app.rally.fun, 2026-08-29, Wallet modal Shadow DOM block
# ponytail: naive text locator. add robust regex/role if fails.

async def click_shadow_text(page, text_selector):
    btn = page.locator(f"text='{text_selector}'").first
    await btn.wait_for(state="visible", timeout=5000)
    await btn.click()
