# Origin Domain: intersticedigital.io
# Date: 2026-08-21
# Symptom: Email registration and OTP verification flow failure (likely SPA React/Vue event absorption)

from playwright.async_api import Page

async def submit_registration(page: Page, email_sel: str, email: str, user_sel: str, user: str, btn_sel: str):
    await page.locator(email_sel).click()
    await page.locator(email_sel).press_sequentially(email, delay=50)
    if user_sel:
        await page.locator(user_sel).click()
        await page.locator(user_sel).press_sequentially(user, delay=50)
    await page.locator(btn_sel).click()

async def fill_otp(page: Page, otp_sel: str, code: str):
    boxes = await page.locator(otp_sel).all()
    if len(boxes) > 1:
        for i, c in enumerate(code):
            await boxes[i].fill(c)
    else:
        await page.locator(otp_sel).click()
        await page.locator(otp_sel).press_sequentially(code, delay=100)
