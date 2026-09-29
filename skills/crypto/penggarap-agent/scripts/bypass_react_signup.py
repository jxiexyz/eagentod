# Metadata: thor.savethelife.io, 2026-08-24, Form submission blocked by React state or timeout during signup
import asyncio
from playwright.async_api import Page

async def bypass_react_signup(page: Page, email: str, password: str):
    print(f"Attempting to fill signup form for {email}")
    await page.wait_for_selector('input[type="email"]', state="visible", timeout=15000)
    
    email_inputs = await page.query_selector_all('input[type="email"]')
    if email_inputs:
        await email_inputs[0].fill(email)
        await page.evaluate('(el) => el.dispatchEvent(new Event("input", { bubbles: true }))', email_inputs[0])
        await page.evaluate('(el) => el.dispatchEvent(new Event("change", { bubbles: true }))', email_inputs[0])

    password_inputs = await page.query_selector_all('input[type="password"]')
    if password_inputs:
        await password_inputs[0].fill(password)
        await page.evaluate('(el) => el.dispatchEvent(new Event("input", { bubbles: true }))', password_inputs[0])
        await page.evaluate('(el) => el.dispatchEvent(new Event("change", { bubbles: true }))', password_inputs[0])
        
        if len(password_inputs) > 1:
            await password_inputs[1].fill(password)
            await page.evaluate('(el) => el.dispatchEvent(new Event("input", { bubbles: true }))', password_inputs[1])
            await page.evaluate('(el) => el.dispatchEvent(new Event("change", { bubbles: true }))', password_inputs[1])

    checkboxes = await page.query_selector_all('input[type="checkbox"]')
    for checkbox in checkboxes:
        if not await checkbox.is_checked():
            await checkbox.click(force=True)
            await page.evaluate('(el) => el.dispatchEvent(new Event("change", { bubbles: true }))', checkbox)
            await page.wait_for_timeout(500)

    submit_buttons = await page.query_selector_all('button[type="submit"]')
    if submit_buttons:
        print("Clicking submit button...")
        await submit_buttons[0].click(force=True)
    else:
        await page.evaluate('() => { const btns = Array.from(document.querySelectorAll("button")); const btn = btns.find(b => b.innerText.includes("Sign Up") || b.innerText.includes("Register") || b.innerText.includes("Create Account")); if(btn) btn.click(); }')

    await page.wait_for_timeout(3000)
    return True
