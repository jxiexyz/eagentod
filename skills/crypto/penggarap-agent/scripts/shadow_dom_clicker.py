# Metadata: Origin Domain: ax1.vc, Date: 2026-08-24, Symptom: Web3 wallet connection and deployment buttons blocked by Shadow DOM boundaries
import asyncio

async def deep_click(page, text_or_selector):
    """
    Recursively searches through Shadow DOMs to find and click an element by text or selector.
    """
    await page.evaluate(f'''(target) => {{
        function findAndClick(targetStr, root = document) {{
            let nodes = [...root.querySelectorAll('*')];
            
            try {{
                let el = root.querySelector(targetStr);
                if (el) {{ el.click(); return true; }}
            }} catch(e) {{}}
            
            for (let node of nodes) {{
                if (node.innerText && node.innerText.trim() === targetStr) {{
                    node.click();
                    return true;
                }}
                if (node.shadowRoot) {{
                    if (findAndClick(targetStr, node.shadowRoot)) return true;
                }}
            }}
            return false;
        }}
        findAndClick(target);
    }}''', text_or_selector)
    await asyncio.sleep(1)
    return True

async def execute_sequential_clicks(page, sequence):
    """
    Executes a sequence of deep clicks, useful for multi-step Web3 flows.
    sequence: list of strings (selectors or button text) e.g., ['Connect', 'MetaMask', 'Activate Agent', 'Deploy Token']
    """
    for step in sequence:
        await deep_click(page, step)
        await asyncio.sleep(2)
    return True
