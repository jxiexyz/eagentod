# Metadata: Origin Domain: octra.fun, Date: 2026-08-26, Symptom: External social links and Telegram bot redirects hanging the VPS browser

async def intercept_external_redirects(page, target_domains=None):
    """
    Intercepts navigation and popups to external domains to prevent headless browser hangs.
    Returns a list of intercepted URLs for alternative CLI processing (e.g., telegram-cli).
    """
    if target_domains is None:
        target_domains = ["t.me", "telegram.me", "tg://", "twitter.com", "x.com", "discord.gg"]
        
    intercepted_urls = []
    
    async def route_handler(route):
        url = route.request.url
        if any(domain in url for domain in target_domains):
            intercepted_urls.append(url)
            await route.abort()
        else:
            await route.fallback()

    await page.route("**/*", route_handler)
    
    # Neutralize window.open to stop new tabs
    await page.add_init_script('''
        window.open = (url) => {
            console.log("INTERCEPTED_POPUP: " + url);
            return null;
        };
    ''')
    
    page.on("console", lambda msg: intercepted_urls.append(msg.text.replace("INTERCEPTED_POPUP: ", "")) if "INTERCEPTED_POPUP: " in msg.text else None)
    
    return intercepted_urls
