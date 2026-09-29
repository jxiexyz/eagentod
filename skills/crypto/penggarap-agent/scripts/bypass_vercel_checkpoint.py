# Metadata: Domain app.meridian.xyz, Date 2026-08-22, Symptom Vercel Security Checkpoint block

async def bypass_vercel_checkpoint(page):
    """
    Injects standard stealth evasions to bypass Vercel Security Checkpoint 429 blocks.
    Must be called before page.goto().
    """
    await page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
        Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
        window.chrome = { runtime: {} };
    """)
    return page
