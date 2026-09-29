# Metadata: Origin Domain: siloprotocol.xyz, Date: 2026-08-22, Symptom: Element interception / generic interaction failure

async def bypass_overlays(page, selectors_to_hide=None):
    """Hides overlapping elements blocking clicks."""
    if not selectors_to_hide:
        selectors_to_hide = [
            '[id*="overlay"]',
            '[class*="overlay"]',
            '[class*="modal"]',
            'div[style*="z-index: 999"]'
        ]
        
    for selector in selectors_to_hide:
        try:
            await page.evaluate(f"""
                document.querySelectorAll('{selector}').forEach(el => {{
                    if(el) el.style.pointerEvents = 'none';
                }});
            """)
        except Exception:
            pass
            
    return True