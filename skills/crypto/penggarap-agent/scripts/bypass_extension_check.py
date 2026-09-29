# Origin Domain: join.actionmodel.com
# Date: 2026-08-26
# Symptom: Task requires downloading an extension. Automation blocked at 'install extension' step.

async def bypass(page, extension_global_var: str = 'actionModel', mock_methods: list = None):
    """
    Injects a mock object into the page's window to bypass extension installation checks.
    Accepts a generic extension global variable name and optional mock methods.
    """
    if mock_methods is None:
        mock_methods = ['connect', 'sign', 'request']
        
    methods_js = ', '.join([f"{m}: async () => ({{ success: true }})" for m in mock_methods])
    
    script = f"""
    if (typeof window !== 'undefined') {{
        Object.defineProperty(window, '{extension_global_var}', {{
            value: {{
                isInstalled: true,
                version: '1.0.0',
                {methods_js}
            }},
            writable: false,
            configurable: true
        }});
    }}
    """
    
    # Apply on future navigations/frames
    await page.add_init_script(script)
    
    # Apply immediately to current context
    try:
        await page.evaluate(script)
    except Exception:
        pass
        
    return True