# Metadata: app.rally.fun, 2026-08-26, Skip task if payment required

async def bypass(page, url=None, **kwargs):
    '''
    Skip campaign if it requires on-chain payment.
    '''
    content = await page.content()
    if 'Pay with ETH' in content or 'Pay with RLP' in content or 'Choose payment method' in content:
        print('butuh transaksi on-chain, skip')
        return True
    return False
