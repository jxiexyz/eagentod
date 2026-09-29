# Metadata: etherbubu.com, 2026-08-21, FCFS Claim Interception / Overlay Blocking
import asyncio

async def execute_bypass(page, selector, retries=3):
    for attempt in range(retries):
        try:
            locator = page.locator(selector).first
            await locator.wait_for(state='attached', timeout=5000)
            
            # Purge common fixed overlays blocking interactions
            await page.evaluate('''() => {
                document.querySelectorAll('*').forEach(el => {
                    const style = window.getComputedStyle(el);
                    if ((style.position === 'fixed' || style.position === 'absolute') && parseInt(style.zIndex, 10) > 99) {
                        el.style.display = 'none';
                    }
                });
            }''')
            
            await locator.scroll_into_view_if_needed()
            # Force native DOM click to pierce React synthetic events
            await locator.evaluate('el => el.click()')
            return True
        except Exception as e:
            if attempt == retries - 1:
                return f"Failed after {retries} attempts: {str(e)}"
            await asyncio.sleep(1)
    return False