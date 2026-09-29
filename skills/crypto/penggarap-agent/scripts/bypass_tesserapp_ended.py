# Metadata: tesserapp.org, 2026-08-21, Raffle already ended missing ENTER RAFFLE button
async def bypass_tesserapp_ended(page, **kwargs):
    """
    Checks if a Tesserapp raffle has ended and gracefully aborts.
    """
    is_ended = await page.evaluate("""() => {
        const text = document.body.innerText;
        return text.includes('This raffle has ended') || text.includes('ENDED');
    }""")
    
    if is_ended:
        print("VERIFICATION: Bypass triggered - Raffle has already ended. Cannot submit entry.")
        return True
    
    return False
