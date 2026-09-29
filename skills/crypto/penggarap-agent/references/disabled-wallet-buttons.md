# Disabled Wallet Buttons in Modals

When dealing with Web3 connection modals (e.g., RainbowKit, Web3Modal, custom UI) where the "MetaMask" or target wallet button is greyed out or explicitly marked `disabled` in the DOM snapshot (e.g., `button "MetaMask" [disabled, ref=e23]`):

## Cause
The frontend state (e.g., React Wagmi hook) checked for `window.ethereum` or EIP-6963 providers before the mock injection completed, or the site actively clears the mock upon detecting headless/automation context.

## Bypass Tactics

### 1. HTML Attribute Brute-Force (DOM Override)
Remove the disabled attribute directly and trigger the click. Often the event listener is still attached to the button even if visually disabled by React props.
```javascript
// Execute via node CDP script or page.evaluate
const mmBtn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('MetaMask'));
if (mmBtn) {
    mmBtn.removeAttribute('disabled');
    mmBtn.click();
}
```

### 2. Wagmi LocalStorage Fallback
If unlocking the button doesn't trigger the connection, the site is likely relying on Wagmi's internal state machine rather than standard provider requests.
- Read `references/wagmi-localstorage-bypass.md` (from `crypto-airdrop-wallet-connect` skill).
- **Tip:** Wagmi v2 often requires both `wagmi.store` and `wagmi.recentConnectorId` to be set manually via JS, followed by a forced page reload (`window.location.reload()`).

### 3. Manual Provider Trigger
If standard UI clicks fail, attempt to manually fire the wallet request in the isolated context:
```javascript
window.ethereum.request({ method: 'eth_requestAccounts' }).catch(console.error);
```
If `window.ethereum` returns `undefined`, the injection script failed or was overwritten by the site. Run `wallet_connect.py --mock-only` again and retry immediately.