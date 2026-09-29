# Metadata: Origin Domain: titanshod.xyz, justbanners.art, otterink.xyz, Date: 2026-08-25, Symptom: Form submission blocked/UI intercepted or React state locked, requiring direct API fetch injection
import json

async def bypass(page, endpoint: str, payload: dict, method: str = "POST"):
    """
    Bypasses UI form blocks by directly submitting the payload to the site's API.
    """
    js_code = f"""async () => {{
        try {{
            const res = await fetch('{endpoint}', {{
                method: '{method}',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({json.dumps(payload)})
            }});
            const data = await res.json().catch(() => ({{}}));
            return {{ status: res.status, ok: res.ok, data }};
        }} catch (e) {{
            return {{ error: e.toString() }};
        }}
    }}"""
    
    try:
        response = await page.evaluate(js_code)
        print(f"[+] API response: {response}")
        return response
    except Exception as e:
        print(f"[-] API Bypass Failed: {e}")
        return None
