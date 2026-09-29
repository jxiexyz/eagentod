# Origin Domain: join.actionmodel.com
# Date: 2026-08-26
# Symptom: Campaign requires a browser extension to be installed to proceed.

async def mock_extension_presence(page, window_vars=None, mock_post_messages=None):
    """
    Bypass extension checks by injecting mock window variables and intercepting postMessages.
    """
    script = ""
    if window_vars:
        import json
        for key, val in window_vars.items():
            val_str = json.dumps(val)
            script += f"window['{key}'] = {val_str};\n"
    
    if mock_post_messages:
        import json
        mocks_str = json.dumps(mock_post_messages)
        script += f"""
        const mockResponses = {mocks_str};
        window.addEventListener('message', (event) => {{
            const msgKey = event.data && (event.data.type || event.data.action);
            if (msgKey && mockResponses[msgKey]) {{
                window.postMessage(mockResponses[msgKey], '*');
            }}
        }});
        """
    
    if script:
        await page.add_init_script(script)
    
    return True
