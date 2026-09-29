# Metadata: mrhoodapp.com, 2026-08-23, PFP extraction and download failure
import os
import urllib.request

async def download_image(page, image_selector, output_filename="/tmp/pfp_bypass.jpg"):
    """Extracts image URL from a selector and downloads it locally for X upload."""
    try:
        await page.wait_for_selector(image_selector, timeout=15000)
        img_url = await page.evaluate(f"document.querySelector('{image_selector}').src")
        
        if not img_url:
            raise ValueError(f"No src attribute found for selector: {image_selector}")
            
        if img_url.startswith('/'):
            base_url = await page.evaluate("window.location.origin")
            img_url = base_url + img_url
            
        req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req) as response, open(output_filename, 'wb') as out_file:
            out_file.write(response.read())
            
        return output_filename
    except Exception as e:
        print(f"[bypass_pfp_download] Failed: {e}")
        return None
