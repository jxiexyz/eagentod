# Metadata: Domain: inkarians.xyz, Date: 2026-08-25, Symptom: Cross-origin embedded iframe interaction failure for waitlist forms.

async def bypass_iframe_isolation(page, iframe_selector='iframe[src*="docs.google.com"], iframe[src*="forms."]'):
    """Extracts embedded form URL and navigates main frame to it, bypassing cross-origin iframe interaction blocks."""
    await page.wait_for_selector(iframe_selector, state='attached', timeout=10000)
    form_url = await page.get_attribute(iframe_selector, 'src')
    
    if not form_url:
        raise Exception(f'Could not find src attribute on {iframe_selector}')
        
    await page.goto(form_url, wait_until='networkidle')
    return form_url
