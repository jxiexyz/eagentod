# Metadata: ink-ape.xyz, 2026-08-24, Verification artifact hidden inside a modal triggered by a button that fails standard Playwright click
import asyncio
from playwright.async_api import Page

async def execute(page: Page, args: dict = None):
    try:
        # Force click the view pass button via JS to avoid interception or selector issues
        await page.evaluate('''() => {
            const btn = document.querySelector('.btn-primary-neon') || 
                        Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('VIEW PASS') || b.innerText.includes('WL SUBMITTED'));
            if (btn) btn.click();
        }''')
        
        await page.wait_for_timeout(2000)
        
        # Extract the success text
        success_text = await page.evaluate('''() => {
            if (document.body.innerText.includes('ENTRY VERIFIED & SECURED!')) {
                return 'ENTRY VERIFIED & SECURED!';
            }
            const headings = Array.from(document.querySelectorAll('h2, h3, .modal-title, .success-title'));
            const match = headings.find(h => h.innerText.includes('VERIFIED'));
            return match ? match.innerText : '';
        }''')
        
        if success_text:
            return {"success": True, "verification": success_text}
            
        return {"success": False, "error": "Modal verification artifact not found in DOM"}
    except Exception as e:
        return {"success": False, "error": str(e)}
