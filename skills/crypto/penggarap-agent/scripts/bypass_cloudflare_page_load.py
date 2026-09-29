# Metadata: ayo.coca-cola.co.id | 2026-09-27 | Initial page load fails - Cloudflare challenge or resource blocking

import asyncio

async def bypass_cloudflare_page_load(page, timeout=30):
    """Wait for Cloudflare challenge resolution and critical resources to load.
    
    Args:
        page: Playwright page object
        timeout: Max seconds to wait (default 30)
    
    Returns:
        bool: True if page loaded successfully, False if blocked/timeout
    """
    try:
        # Wait for Cloudflare challenge iframe or bypass
        await page.wait_for_load_state('domcontentloaded', timeout=timeout * 1000)
        
        # Check for Cloudflare challenge indicators
        cf_indicators = [
            'cf-challenge-running',
            'cf-browser-verification',
            '#challenge-running',
            'iframe[src*="challenges.cloudflare.com"]'
        ]
        
        # Wait up to timeout for challenge to clear
        end_time = asyncio.get_event_loop().time() + timeout
        while asyncio.get_event_loop().time() < end_time:
            # Check if any challenge indicator present
            has_challenge = False
            for selector in cf_indicators:
                try:
                    elem = await page.query_selector(selector)
                    if elem:
                        has_challenge = True
                        break
                except:
                    pass
            
            if not has_challenge:
                break
            
            await asyncio.sleep(1)
        
        # Wait for network idle (resources loaded)
        await page.wait_for_load_state('networkidle', timeout=10000)
        
        # Check if page accessible (not blocked)
        title = await page.title()
        if 'cloudflare' in title.lower() or 'just a moment' in title.lower():
            return False
        
        return True
        
    except Exception as e:
        print(f"Cloudflare page load bypass failed: {e}")
        return False