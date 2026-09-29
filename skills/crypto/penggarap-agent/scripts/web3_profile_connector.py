# Metadata: Origin Domain: app.stabilizer.finance | Date: 2026-08-23 | Symptom: Web3 wallet connection or profile linking buttons blocked by overlays or hidden inside Shadow DOMs (common Privy/Dynamic SDK behavior).

import asyncio

async def force_click_profile_button(page, target_text="Connect"):
    """
    Generic web3 button clicker. Pierces shadow roots and forces DOM-level clicks
    to bypass overlay interceptions and visibility checks.
    """
    js_pierce_and_click = f"""
    () => {{
        function findAndClick(node, text) {{
            if (node.shadowRoot) {{
                if (findAndClick(node.shadowRoot, text)) return true;
            }}
            if (node.nodeType === Node.TEXT_NODE && node.textContent.trim().toLowerCase().includes(text.toLowerCase())) {{
                let parent = node.parentElement;
                while(parent) {{
                    if(parent.tagName === 'BUTTON' || parent.getAttribute('role') === 'button' || parent.onclick) {{
                        parent.click();
                        return true;
                    }}
                    parent = parent.parentElement;
                }}
                // Fallback direct click on text parent
                node.parentElement.click();
                return true;
            }}
            for (let child of node.childNodes) {{
                if (findAndClick(child, text)) return true;
            }}
            return false;
        }}
        return findAndClick(document, "{target_text}");
    }}
    """
    try:
        # Attempt deep shadow piercing click
        clicked = await page.evaluate(js_pierce_and_click)
        
        # Fallback to Playwright force click if JS traversal fails
        if not clicked:
            locator = page.locator(f"text={target_text}").first
            await locator.click(force=True, timeout=5000)
        return True
    except Exception as e:
        print(f"Bypass force click failed for '{target_text}': {e}")
        return False
