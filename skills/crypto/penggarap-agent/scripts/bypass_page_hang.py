# Metadata: Origin Domain: zygofuture.com, Date: 2026-08-17, Symptom: hermes -z no final response was produced (infinite hang/timeout)

def safe_navigate_and_stop(page, url, timeout_ms=30000, block_heavy_resources=True):
    """Prevents agent timeout by intercepting heavy resources and forcing domcontentloaded."""
    if block_heavy_resources:
        def intercept_route(route):
            if route.request.resource_type in ["image", "media", "font", "eventsource", "websocket"]:
                route.abort()
            else:
                route.continue_()
        page.route("**/*", intercept_route)
    
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
    except Exception:
        # Force stop hanging scripts/trackers that prevent network idle
        page.evaluate("window.stop()")
    
    return page
