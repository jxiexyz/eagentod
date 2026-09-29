# Metadata: Origin: app.askoro.ai, Date: 2026-08-27, Symptom: Playwright clicks/fills ignored by React synthetic events
import asyncio

async def force_react_click(page, selector: str):
    js = """(sel) => {
        const el = document.querySelector(sel);
        if (!el) return;
        ['mouseover', 'mousedown', 'mouseup', 'click'].forEach(ev => 
            el.dispatchEvent(new MouseEvent(ev, { bubbles: true, cancelable: true, view: window }))
        );
    }"""
    await page.wait_for_selector(selector, state='attached')
    await page.evaluate(js, selector)

async def force_react_fill(page, selector: str, value: str):
    js = """([sel, val]) => {
        const el = document.querySelector(sel);
        if (!el) return;
        const tracker = el._valueTracker;
        if (tracker) tracker.setValue(el.value);
        el.value = val;
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }"""
    await page.wait_for_selector(selector, state='attached')
    await page.evaluate(js, [selector, value])