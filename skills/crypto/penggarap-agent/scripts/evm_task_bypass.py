# Metadata: Domain: puffins.fun, Date: 2026-08-21, Symptom: Automated task completion and EVM address submission failure on unknown DOM structure
import asyncio
import re
from playwright.async_api import Page

async def bypass_tasks_and_submit_evm(page: Page, evm_address: str):
    """
    Bypasses task verifications by heuristically finding and clicking task-related elements,
    then locates an EVM input field by placeholder/attributes, fills it, and submits.
    """
    # 1. Click all potential task/verification buttons
    task_pattern = re.compile(r'verify|complete|follow|join|check|claim', re.I)
    elements = await page.locator('button, a').all()
    for el in elements:
        try:
            text = await el.text_content()
            if text and task_pattern.search(text) and await el.is_visible():
                await el.click(timeout=2000)
                await asyncio.sleep(1.5)
        except Exception:
            continue

    # 2. Find and fill EVM address input heuristically
    inputs = await page.locator('input').all()
    for inp in inputs:
        try:
            ph = await inp.get_attribute('placeholder') or ''
            name = await inp.get_attribute('name') or ''
            attrs = (ph + ' ' + name).lower()
            if any(k in attrs for k in ['0x', 'evm', 'wallet', 'address', 'eth', 'submit']):
                await inp.fill(evm_address)
                await asyncio.sleep(1)
                break
        except Exception:
            continue

    # 3. Submit the form
    submit_pattern = re.compile(r'submit|save|confirm|enter|kirim', re.I)
    submits = await page.locator('button').all()
    for sub in submits:
        try:
            text = await sub.text_content()
            if text and submit_pattern.search(text) and await sub.is_visible():
                await sub.click(timeout=2000)
                await asyncio.sleep(2)
                break
        except Exception:
            continue

    return True
