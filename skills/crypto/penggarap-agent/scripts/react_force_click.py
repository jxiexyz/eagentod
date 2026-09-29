# Metadata: memebitcoin.org, 2026-08-24, Playwright click intercepted by UI overlays/React event traps.

async def force_click(page, selector: str):
    """Forces a click using standard DOM events to bypass React synthetic event traps and z-index overlays."""
    await page.wait_for_selector(selector, state='attached', timeout=10000)
    await page.evaluate('''
        (selector) => {
            const element = document.querySelector(selector);
            if (!element) throw new Error("Element not found: " + selector);
            
            // Bypass potential blocking overlays (common in Web3 modals/particle backgrounds)
            document.querySelectorAll('div').forEach(div => {
                const style = window.getComputedStyle(div);
                if ((style.position === 'fixed' || style.position === 'absolute') && parseInt(style.zIndex || 0) > 50) {
                    if (!div.contains(element)) div.style.pointerEvents = 'none';
                }
            });

            element.scrollIntoView({block: 'center', behavior: 'instant'});
            ['mouseover', 'mousedown', 'mouseup', 'click'].forEach(evt => 
                element.dispatchEvent(new MouseEvent(evt, {bubbles: true, cancelable: true, view: window}))
            );
        }
    ''', selector)