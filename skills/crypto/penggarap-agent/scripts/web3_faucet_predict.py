# Metadata: Domain: nft.retium.org, Date: 2026-08-22, Symptom: Fails to connect testnet, claim faucet, predict

async def bypass(page, connect_sel="button:has-text('Connect')", faucet_sel="button:has-text('Faucet')", predict_sel="button:has-text('Predict')"):
    for sel in [connect_sel, faucet_sel, predict_sel]:
        try:
            await page.click(sel, timeout=5000)
            await page.wait_for_timeout(3000)
        except Exception:
            continue
    return True