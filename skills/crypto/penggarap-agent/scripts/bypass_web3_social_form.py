# Metadata: bafoontown.wtf, 2026-08-25, Social link target=_blank tab proliferation and React input state mismatch
import asyncio

async def execute_bypass(page, social_selectors: list, address_selector: str, wallet_address: str):
    """
    Bypass social link redirects and fill React-controlled wallet inputs.
    """
    # Intercept window.open to prevent new tabs blocking the automation flow
    await page.add_init_script("""
        window.open = function() {
            return { closed: false, focus: function(){}, close: function(){} };
        };
    """)

    # Process social links: remove target="_blank", prevent navigation, and click
    for selector in social_selectors:
        locators = await page.locator(selector).all()
        for loc in locators:
            await loc.evaluate("""el => {
                el.removeAttribute('target');
                el.onclick = (e) => e.preventDefault();
            }""")
            await loc.click()
            await asyncio.sleep(0.5)

    # Force fill BSC address to bypass React synthetic event drops
    if address_selector and wallet_address:
        await page.evaluate("""([sel, val]) => {
            const el = document.querySelector(sel);
            if (!el) return;
            const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            if (nativeInputValueSetter) {
                nativeInputValueSetter.call(el, val);
            }
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }""", [address_selector, wallet_address])

    return True
