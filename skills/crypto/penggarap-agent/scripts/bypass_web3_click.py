# Origin Domain: app.meridian.xyz
# Date: 2026-08-22
# Symptom: Faucet/Predict buttons intercepted or obscured by Web3 modal overlays and React state.

async def bypass_web3_click(page, text_content: str, timeout: int = 5000):
    """Bypasses standard playwright clicks for nested React/Web3 buttons."""
    try:
        # Attempt forced click ignoring interception
        await page.get_by_text(text_content, exact=False).first.click(force=True, timeout=timeout)
        return True
    except Exception:
        pass
        
    try:
        # Fallback to pure JS DOM traversal to bypass shadow/event listeners
        await page.evaluate('''text => {
            const elements = [...document.querySelectorAll('button, div[role="button"], span')];
            const target = elements.find(el => el.textContent && el.textContent.includes(text));
            if (target) {
                target.click();
            }
        }''', text_content)
        return True
    except Exception as e:
        print(f'Bypass click failed for "{text_content}": {e}')
        return False
