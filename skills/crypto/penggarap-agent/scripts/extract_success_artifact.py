# Metadata: withspout.com, 2026-08-17, Worker claimed success but provided NO valid VERIFICATION artifact

async def extract_success_artifact(page, selectors=None, timeout=5000):
    if not selectors:
        selectors = ["[class*='success']", "[class*='toast']", "text='Thank'", "text='Success'", "text='verified'"]
    try:
        await page.wait_for_load_state('networkidle', timeout=timeout)
    except:
        pass
    for selector in selectors:
        try:
            el = await page.wait_for_selector(selector, timeout=2000, state='visible')
            if el:
                txt = await el.inner_text()
                if txt.strip():
                    return txt.strip()
        except:
            continue
    try:
        return await page.evaluate("document.body.innerText.substring(0, 500)")
    except Exception as e:
        return str(e)