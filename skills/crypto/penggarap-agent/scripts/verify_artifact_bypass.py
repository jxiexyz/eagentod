# Metadata: app.rally.fun, 2026-08-18, Worker claimed success but provided NO valid VERIFICATION artifact

async def get_verification_artifact(page, selectors=["text='Claimed'", "text='Success'", ".Toastify__toast--success", ".toast-success"]):
    for s in selectors:
        try:
            el = await page.wait_for_selector(s, timeout=5000)
            return {"verified": True, "artifact": await el.inner_text()}
        except:
            pass
    return {"verified": False, "artifact": page.url}