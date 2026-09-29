# Metadata: Origin Domain: siloprotocol.xyz, Date: 2026-08-22, Symptom: Unspecified interaction failure (likely shadow DOM or overlays)
import asyncio
from playwright.async_api import Page

async def robust_click(page: Page, selector: str, timeout: int = 5000):
    """Attempts to click an element, bypassing common blockers like overlays and shadow DOMs."""
    try:
        await page.wait_for_selector(selector, state="attached", timeout=timeout)
        await page.click(selector, timeout=timeout)
        return True
    except Exception:
        pass
    
    try:
        await page.click(selector, force=True, timeout=timeout)
        return True
    except Exception:
        pass
        
    try:
        # Deep shadow DOM pierce and JS click fallback
        js_script = f"""
        (() => {{
            function findElement(root, sel) {{
                let el = root.querySelector(sel);
                if (el) return el;
                for (let child of root.querySelectorAll('*')) {{
                    if (child.shadowRoot) {{
                        let found = findElement(child.shadowRoot, sel);
                        if (found) return found;
                    }}
                }}
                return null;
            }}
            let target = findElement(document, '{selector}');
            if (target) {{ target.click(); return true; }}
            return false;
        }})()
        """
        return await page.evaluate(js_script)
    except Exception:
        return False
