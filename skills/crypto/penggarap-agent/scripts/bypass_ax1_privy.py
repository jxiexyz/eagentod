# Metadata: ax1.vc, 2026-08-22, Bypass Privy popups for agent creation
async def run(page, **kwargs):
    print("Bypassing Privy Create Agent popup...")
    
    # 1. Wait for Privy iframe to appear
    iframe_locator = page.locator('iframe#privy-dialog-iframe')
    try:
        await iframe_locator.wait_for(state='attached', timeout=10000)
        print("Found Privy iframe.")
    except Exception as e:
        print(f"Privy iframe not found: {e}")
        return False
        
    frame = iframe_locator.content_frame
    if not frame:
        print("Could not access Privy frame.")
        return False
        
    # 2. Find and click the 'Create a wallet' button inside
    create_btn = frame.locator('button:has-text("Create a wallet")')
    try:
        await create_btn.wait_for(state='visible', timeout=5000)
        await create_btn.click()
        print("Clicked Create a wallet inside Privy iframe.")
    except Exception as e:
        print(f"Create a wallet button not found: {e}")
        # Try alternate text
        create_btn = frame.locator('button:has-text("Create")')
        try:
            await create_btn.click()
            print("Clicked Create inside Privy iframe.")
        except Exception as e2:
            print(f"Create button not found: {e2}")
            return False
            
    # 3. Wait for success
    try:
        await page.wait_for_timeout(3000)
        print("Agent created.")
        return True
    except Exception as e:
        print(f"Wait failed: {e}")
        return False
