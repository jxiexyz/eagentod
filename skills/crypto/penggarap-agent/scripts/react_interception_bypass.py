# Metadata: Origin Domain: chatlee.io, Date: 2026-08-21, Symptom: Element click interception and React state fill failures
import asyncio
from playwright.async_api import Page

async def force_click(page: Page, selector: str, timeout: int = 10000) -> bool:
    try:
        await page.wait_for_selector(selector, state="attached", timeout=timeout)
        await page.evaluate("(sel) => document.querySelector(sel).click()", selector)
        return True
    except Exception:
        return False

async def react_fill(page: Page, selector: str, value: str, timeout: int = 10000) -> bool:
    try:
        await page.wait_for_selector(selector, state="attached", timeout=timeout)
        js_code = """(args) => {
            const el = document.querySelector(args.sel);
            const tracker = el._valueTracker;
            if (tracker) { tracker.setValue(el.value); }
            el.value = args.val;
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }"""
        await page.evaluate(js_code, {"sel": selector, "val": value})
        return True
    except Exception:
        return False
