# Metadata: Domain: inklords.xyz, Date: 2026-08-25, Symptom: Social tasks and EVM address submission failing via standard clicks
import asyncio

async def bypass_social_evm_submit(page, evm_address):
    # Fake social clicks by intercepting links to prevent navigation loss
    await page.evaluate('''() => {
        document.querySelectorAll('a[href*="t.me"], a[href*="twitter.com"], a[href*="x.com"]').forEach(el => {
            el.removeAttribute('target');
            el.onclick = (e) => { e.preventDefault(); console.log('Intercepted social click'); };
            el.click();
        });
    }''')
    
    await asyncio.sleep(2)
    
    # Force React/Vue input event for EVM address
    await page.evaluate(f'''(evm_address) => {{
        const inputs = Array.from(document.querySelectorAll('input'));
        const evmInput = inputs.find(i => i.placeholder.toLowerCase().includes('0x') || i.placeholder.toLowerCase().includes('bsc') || i.placeholder.toLowerCase().includes('address') || i.placeholder.toLowerCase().includes('wallet'));
        if (evmInput) {{
            const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            nativeInputValueSetter.call(evmInput, evm_address);
            evmInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
            evmInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
        }}
    }}''', evm_address)
    
    await asyncio.sleep(1)
    
    # Trigger submit button
    await page.evaluate('''() => {
        const buttons = Array.from(document.querySelectorAll('button, div[role="button"]'));
        const submitBtn = buttons.find(b => b.innerText.toLowerCase().includes('submit') || b.innerText.toLowerCase().includes('join') || b.innerText.toLowerCase().includes('apply') || b.innerText.toLowerCase().includes('claim'));
        if (submitBtn) {
            submitBtn.click();
        }
    }''')
