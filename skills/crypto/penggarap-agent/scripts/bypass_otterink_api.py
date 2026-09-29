# Metadata: Domain: otterink.xyz, Date: 2026-08-25, Symptom: Form UI claims success but API submission fails silently or fails to display success message
import json

async def bypass(page, handle, comment_url, address, tasks={"follow": True, "repost": True, "comment": True}):
    """
    Directly hits the /api/whitelist endpoint to seal the entry.
    """
    payload = {
        "handle": handle,
        "commentUrl": comment_url,
        "address": address.strip(),
        "tasks": tasks
    }
    
    js_code = f"""async () => {{
        try {{
            const res = await fetch("/api/whitelist", {{
                method: "POST",
                headers: {{"Content-Type": "application/json"}},
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
