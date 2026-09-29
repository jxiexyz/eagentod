# Metadata: Origin: mossuri.xyz, Date: 2026-09-25, Symptom: Unknown registration block / No DOM
import asyncio
from playwright.async_api import Page

async def bypass_registration(page: Page, code: str, input_sel: str = "input[type='text']", btn_sel: str = "button[type='submit']"):
    await page.wait_for_selector(input_sel, state="visible", timeout=5000)
    await page.fill(input_sel, code)
    await page.click(btn_sel)
    await page.wait_for_load_state("networkidle")