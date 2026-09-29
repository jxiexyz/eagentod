# Metadata: ax1.vc, 2026-08-22, Bypass RPC failure on viem request to sepolia.base.org
async def run(page, **kwargs):
    print("Intercepting viem RPC requests to replace failed endpoint...")
    
    async def route_handler(route):
        if "sepolia.base.org" in route.request.url:
            await route.continue_(url="https://base-sepolia.gateway.tenderly.co")
        else:
            await route.continue_()
            
    await page.route("**/*", route_handler)
    return True