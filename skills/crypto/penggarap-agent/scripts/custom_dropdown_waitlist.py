# Metadata: nft.retium.org, 2026-08-20, Custom country select and email form failure
import asyncio
from playwright.async_api import Page

async def bypass_waitlist(page: Page, email_sel: str, email_val: str, drop_sel: str, country_val: str, submit_sel: str):
    await page.evaluate('''([sel, val]) => {
        const el = document.querySelector(sel);
        if(el) {
            const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            setter.call(el, val);
            el.dispatchEvent(new Event('input', {bubbles: true}));
        }
    }''', [email_sel, email_val])
    await page.click(drop_sel, force=True)
    await asyncio.sleep(0.5)
    await page.evaluate('''([text]) => {
        const els = Array.from(document.querySelectorAll('*'));
        const el = els.find(e => e.textContent.trim() === text && e.children.length === 0);
        if(el) el.click();
    }''', [country_val])
    await asyncio.sleep(0.5)
    await page.click(submit_sel, force=True)
