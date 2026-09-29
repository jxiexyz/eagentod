# Metadata: Domain: sohonft.site (generic waitlist), Date: 2026-08-21, Symptom: React form submit intercepted / success modal text extraction fails

import asyncio
from playwright.async_api import Page, TimeoutError

async def submit_and_extract_modal(page: Page, submit_selector: str = 'button', submit_text: str = 'SUBMIT', modal_selector: str = '.modal.is-open', timeout: int = 15000):
    """
    Forces click on a submit button using JS evaluation to bypass overlays and React pointer-events locks,
    then waits for a success modal to appear and extracts its text/properties for verification.
    """
    print(f"[Bypass] Forcing click on submit button matching '{submit_text}' or selector '{submit_selector}'")
    
    clicked = await page.evaluate("""(args) => {
        const sel = args.selector;
        const txt = args.text;
        const elements = Array.from(document.querySelectorAll(sel));
        const el = elements.find(b => b.textContent.includes(txt)) || document.querySelector(sel);
        if (el) {
            el.removeAttribute('disabled');
            el.click();
            return true;
        }
        return false;
    }""", {"selector": submit_selector, "text": submit_text})
    
    if not clicked:
        print("[Bypass] Submit button not found!")
        return None

    print(f"[Bypass] Waiting for modal overlay: {modal_selector}")
    try:
        await page.wait_for_selector(modal_selector, state="attached", timeout=timeout)
        await asyncio.sleep(1) # Allow animation
        
        result = await page.evaluate("""(sel) => {
            const el = document.querySelector(sel);
            if (!el) return null;
            return {
                className: el.className,
                innerText: el.innerText,
                title: el.querySelector('h1, h2, h3, .title') ? el.querySelector('h1, h2, h3, .title').innerText : '',
                desc: el.querySelector('p, .desc, .description') ? el.querySelector('p, .desc, .description').innerText : ''
            };
        }""", modal_selector)
        
        print("[Bypass] Modal extracted successfully")
        return result
    except TimeoutError:
        print("[Bypass] Modal wait timed out. Attempting fallback fuzzy extraction...")
        fallback = await page.evaluate("""() => {
            const modals = Array.from(document.querySelectorAll('[class*="modal"], [class*="overlay"], dialog'));
            const visible = modals.find(m => window.getComputedStyle(m).display !== 'none' && window.getComputedStyle(m).visibility !== 'hidden');
            if (visible) {
                return {
                    className: visible.className,
                    innerText: visible.innerText
                };
            }
            return null;
        }""")
        return fallback
