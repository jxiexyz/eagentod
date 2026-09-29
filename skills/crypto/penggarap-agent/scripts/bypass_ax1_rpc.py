# Metadata: ax1.vc, 2026-08-22, Bypass RPC failure on token deploy
async def run(page, **kwargs):
    print("Intercepting viem RPC requests to replace failed endpoint...")
    
    async def route_handler(route):
        request = route.request
        if "sepolia.base.org" in request.url:
            # Reroute to working Base Sepolia RPC
            print(f"Rerouting {request.url} to https://base-sepolia.gateway.tenderly.co")
            await route.continue_(url="https://base-sepolia.gateway.tenderly.co")
        else:
            await route.continue_()
            
    await page.route("**/*", route_handler)
    print("RPC interception active.")
    return True
