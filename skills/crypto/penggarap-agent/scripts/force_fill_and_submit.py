# Origin Domain: di.xyz
# Date: 2026-08-27
# Symptom: Fails to complete social tasks and submit BSC address due to dynamic DOM or visibility checks.

async def force_fill_and_submit(page, input_text: str, input_selector: str, submit_selector: str):
    """
    Forces input fill and submit button click, bypassing standard visibility and shadow DOM boundaries.
    """
    try:
        input_loc = page.locator(input_selector).first
        await input_loc.wait_for(state="attached", timeout=10000)
        await input_loc.scroll_into_view_if_needed()
        await input_loc.fill(input_text, force=True)
        
        submit_loc = page.locator(submit_selector).first
        await submit_loc.wait_for(state="attached", timeout=5000)
        await submit_loc.click(force=True)
        
        return True
    except Exception as e:
        print(f"Bypass failed: {e}")
        return False
