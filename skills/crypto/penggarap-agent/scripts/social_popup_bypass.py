# Metadata: Generic Airdrop Sites, 2026-08-21, Social task popups causing timeouts or blocking main page context, React state not updating on EVM input

async def bypass_social_popups(page):
    """
    Stubs window.open to bypass actual Twitter/Telegram popup navigation.
    Fools the site into thinking the task window was opened and allows verification steps to proceed.
    """
    await page.evaluate('''() => {
        window.originalOpen = window.open;
        window.open = function(url, name, specs) {
            console.log('Intercepted popup for:', url);
            // Trigger a focus event shortly after to simulate returning to the window
            setTimeout(() => { window.dispatchEvent(new Event('focus')); }, 500);
            return { closed: false, close: function() { this.closed = true; }, focus: function() {} };
        };
    }''')

async def force_react_fill(page, selector, text_value):
    """
    Force fills React input fields when standard page.fill() fails to trigger state updates.
    """
    await page.evaluate('''([sel, val]) => {
        const el = document.querySelector(sel);
        if (!el) throw new Error('Element not found: ' + sel);
        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        nativeInputValueSetter.call(el, val);
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }''', [selector, text_value])