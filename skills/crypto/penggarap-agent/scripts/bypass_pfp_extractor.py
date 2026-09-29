# Metadata: Origin Domain: teogiwa.com, Date: 2026-08-23, Symptom: Failure to download PFP due to DOM/Blob/CORS restrictions.
import base64
from playwright.async_api import Page

async def extract_and_save_image(page: Page, selector: str, output_path: str = "/tmp/pfp.png") -> str:
    """Extracts image via browser context fetch to bypass CORS and Blob URL blocks."""
    await page.wait_for_selector(selector, state="attached")
    src = await page.locator(selector).get_attribute("src")
    
    if not src:
        raise ValueError(f"No image src found for selector: {selector}")
        
    base64_data = await page.evaluate('''async (url) => {
        const response = await fetch(url);
        const blob = await response.blob();
        return new Promise((resolve) => {
            const reader = new FileReader();
            reader.onloadend = () => resolve(reader.result.split(',')[1]);
            reader.readAsDataURL(blob);
        });
    }''', src)

    if base64_data:
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(base64_data))
        return output_path
    
    raise Exception("Failed to extract base64 image data from page.")