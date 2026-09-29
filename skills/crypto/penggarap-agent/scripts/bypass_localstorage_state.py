# Metadata: roarmads.xyz, 2026-08-20, React form timeout on inputs, state managed via localStorage

async def bypass_localstorage_state(page, storage_key: str, state_dict: dict, reload_page: bool = True):
    """
    Injects application state directly into localStorage and reloads the page.
    Useful for bypassing React/NextJS multi-step forms where native page.fill times out 
    or buttons are disabled due to state locking.
    """
    print(f"Injecting state into localStorage key: {storage_key}")
    
    # Playwright auto-serializes the Python dict to a JS object,
    # and then we stringify it in the browser context for localStorage.
    await page.evaluate(
        "([key, val]) => { localStorage.setItem(key, JSON.stringify(val)); }",
        [storage_key, state_dict]
    )
    
    if reload_page:
        print("Reloading page to apply state...")
        await page.reload(wait_until='domcontentloaded')
        await page.wait_for_timeout(2000)
    
    return True
