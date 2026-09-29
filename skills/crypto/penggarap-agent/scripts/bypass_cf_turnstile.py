# Metadata: Origin Domain: roarmads.xyz, Date: 2026-08-22, Symptom: Blocked on whitelist load (session 20260822_072307_27520f), suspected Cloudflare Turnstile or iframe challenge
import asyncio

async def bypass_challenge(page, challenge_selector="iframe[src*='turnstile'], iframe[src*='challenge']", timeout=10000):
    """Wait for and click Turnstile/Cloudflare challenge checkboxes within iframes."""
    try:
        await page.wait_for_selector(challenge_selector, state='attached', timeout=timeout)
        for frame in page.frames:
            if 'turnstile' in frame.url or 'challenge' in frame.url:
                checkbox = await frame.query_selector('.mark, input[type="checkbox"], #challenge-stage')
                if checkbox:
                    await checkbox.click()
                    await asyncio.sleep(3)
    except Exception:
        pass
    await page.wait_for_load_state('domcontentloaded')
    return True
