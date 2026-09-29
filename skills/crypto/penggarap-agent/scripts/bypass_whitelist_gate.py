# Metadata: Domain: fulelore.xyz, Date: 2026-08-21, Symptom: Blocked by generic overlay or Cloudflare Turnstile challenge during airdrop whitelist registration

async def bypass(page, **kwargs):
    import logging
    logging.info("Executing generic whitelist gate bypass...")
    try:
        await page.evaluate('''() => {
            document.querySelectorAll('[class*="overlay"], [class*="modal"], [id*="modal"]').forEach(el => {
                const z = parseInt(window.getComputedStyle(el).zIndex || '0');
                if (z > 50 || window.getComputedStyle(el).position === 'fixed') el.remove();
            });
        }''')
        cf = await page.query_selector('iframe[src*="cloudflare"]')
        if cf:
            box = await cf.bounding_box()
            if box:
                await page.mouse.click(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
            await page.wait_for_selector('iframe[src*="cloudflare"]', state='hidden', timeout=15000)
        return True
    except Exception as e:
        logging.error(f"Gate bypass error: {e}")
        return False
