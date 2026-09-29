# Origin Domain: nft.retium.org (General Web3 Testnets)
# Date: 2026-08-22
# Specific Symptom: Cannot click dynamic Web3 buttons (faucet/predict/wallet) due to shadow DOM encapsulation or React hydration re-renders.

async def bypass_web3_shadow_click(page, selector: str, timeout: int = 15000):
    """
    Bypasses React DOM detached errors and shadow DOM barriers to forcefully click elements.
    """
    from playwright.async_api import TimeoutError

    try:
        # Attempt standard Playwright interaction first
        element = page.locator(selector).first
        await element.wait_for(state="attached", timeout=timeout)
        await element.scroll_into_view_if_needed()
        await element.click(delay=150)
        return True
    except TimeoutError:
        pass

    # Fallback to forceful recursive JS evaluation for Shadow DOM traversal
    try:
        await page.evaluate(f'''(sel) => {{
            function findElement(root, s) {{
                if (!root) return null;
                let el = root.querySelector(s);
                if (el) return el;
                for (let child of root.querySelectorAll('*')) {{
                    if (child.shadowRoot) {{
                        let res = findElement(child.shadowRoot, s);
                        if (res) return res;
                    }}
                }}
                return null;
            }}
            let target = findElement(document, sel);
            if (target) {{
                target.scrollIntoView({{behavior: 'smooth', block: 'center'}});
                target.dispatchEvent(new MouseEvent('click', {{bubbles: true, cancelable: true, view: window}}));
            }} else {{
                throw new Error("Element " + sel + " not found in standard or shadow DOM");
            }}
        }}''', selector)
        return True
    except Exception as e:
        print(f"Shadow DOM JS click failed for {selector}: {e}")
        return False
