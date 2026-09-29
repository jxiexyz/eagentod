# Metadata: Origin Domain: mrhoodapp.com, Date: 2026-08-23, Symptom: Complex image download (CORS/auth blocks direct fetch).

def extract_visible_image(page, selector, output_path):
    """Captures a DOM element directly to an image file, bypassing CORS and src extraction."""
    element = page.locator(selector).first
    element.wait_for(state="visible", timeout=10000)
    element.screenshot(path=output_path)
    return True