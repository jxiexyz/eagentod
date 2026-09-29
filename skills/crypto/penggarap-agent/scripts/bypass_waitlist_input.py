# Metadata: Domain: ink-ape.xyz, Date: 2026-08-25, Symptom: React synthetic event blocking EVM address input
import asyncio

async def bypass_waitlist_input(page, address_selector: str, submit_selector: str, evm_address: str):
    try:
        await page.wait_for_selector(address_selector, state='visible', timeout=5000)
        await page.evaluate('''([selector, value]) => {
            const input = document.querySelector(selector);
            if (input) {
                const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                setter.call(input, value);
                input.dispatchEvent(new Event('input', { bubbles: true }));
                input.dispatchEvent(new Event('change', { bubbles: true }));
            }
        }''', [address_selector, evm_address])
        await asyncio.sleep(1)
        await page.click(submit_selector, force=True)
        return True
    except Exception as e:
        return False
