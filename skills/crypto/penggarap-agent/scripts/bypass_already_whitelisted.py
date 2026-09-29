# Metadata: inklords.xyz, 2026-08-24, Already registered / Whitelist confirmed text found

def run_bypass(page):
    try:
        if page.locator("text=\"This username or wallet has already petitioned the Court.\"").count() > 0:
            return True
        if page.locator("text=\"You are already whitelisted.\"").count() > 0:
            return True
        if page.locator("text=\"This wallet is already on the list.\"").count() > 0:
            return True
        return False
    except Exception:
        return False