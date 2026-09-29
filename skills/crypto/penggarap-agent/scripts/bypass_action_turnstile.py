# Metadata: app.gyndore.com, 2026-08-26, Action-Gated Turnstile HTTP 400/403 on API (Unable to verify you are human)
import asyncio
from playwright.async_api import Page
import traceback
import sys

async def bypass(page: Page, **kwargs) -> bool:
    try:
        print("[*] Checking for Action-Gated Turnstile blocks...")
        toasts = await page.locator('[role="status"], [role="alert"], .toast, [class*="toast"]').all_text_contents()
        toast_text = " ".join(toasts).lower()
        
        if "unable to verify you are human" in toast_text or "cloudflare" in toast_text:
            print("[-] Action-gated Turnstile block detected via UI toast (403 on API).")
            print("[-] FUTILITY RULE: Headless CDP cannot solve invisible/post-action Turnstile challenges.")
            print("[-] Aborting to save cycles and prevent infinite retries.")
            return False
            
        for f in page.frames:
            if "challenges.cloudflare.com" in f.url:
                print("[-] Cloudflare challenge frame detected post-action. Aborting.")
                return False
                
        print("[+] No hard WAF block detected.")
        return True
    except Exception as e:
        print(f"[-] Bypass Error: {str(e)}")
        traceback.print_exc(file=sys.stderr)
        return False
