# Metadata: robillio.xyz, 2026-08-21, Skip execution if already whitelisted/registered

async def execute(page, success_text="You Are On The Whitelist"):
    try:
        content = await page.content()
        if success_text.lower() in content.lower():
            print(f"[+] Already registered. Found success text: {success_text}")
            return True
        return False
    except Exception as e:
        print(f"[-] Error checking registration status: {e}")
        return False
