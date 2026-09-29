# Handling WalletConnect QR Code Fallbacks (EIP-6963)

## The Problem (BuilderFi & Modern dApps)
When automating web3 logins on modern dApps (using RainbowKit, ConnectKit, or Dynamic SDKs), the automation might get stuck at a "WalletConnect" QR code instead of seeing a "MetaMask" or "Browser Wallet" button. 

This happens because modern dApps enforce **EIP-6963 (Multi-Injected Provider Discovery)**. If the injected `window.ethereum` mock is too basic (e.g., just `isMetaMask: true`), the dApp assumes no valid desktop extension is installed and forces the mobile QR code flow.

## The Solution: Advanced EIP-6963 Mock Injection
To trick these strict SDKs into showing the clickable desktop wallet button, you must inject a comprehensive mock provider that implements the expected JSON-RPC methods (`eth_requestAccounts`, `eth_chainId`, `personal_sign`) **before** the wallet modal is opened, ideally before the page finishes loading.

### Advanced Mock Payload
When building a custom Puppeteer script or injecting via CDP, use this comprehensive mock payload to simulate a full MetaMask installation:

```javascript
(() => {
  const address = "0x444b38c15cCc46db22b9590497023D91e506B2fF"; // Replace with actual worker EVM
  window.ethereum = {
    isMetaMask: true,
    isConnected: () => true,
    request: async ({ method, params }) => {
      console.log("Mock Wallet Request:", method, params);
      if (method === 'eth_requestAccounts' || method === 'eth_accounts') {
          return [address];
      }
      if (method === 'eth_chainId') {
          return "0x1"; // Mainnet
      }
      if (method === 'personal_sign' || method === 'eth_signTypedData_v4') {
          // Return a dummy signature for connect-only verification flows
          return "0xmock_signature_00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000";
      }
      throw new Error("Mock wallet: Method not supported " + method);
    },
    on: () => {}, 
    removeListener: () => {}
  };
  
  // Optional: Dispatch EIP-6963 announce event if the dApp specifically listens for it
  window.dispatchEvent(new CustomEvent('eip6963:announceProvider', {
    detail: {
      info: { uuid: 'mock-uuid', name: 'MetaMask', icon: 'data:image/svg+xml,...', rdns: 'io.metamask' },
      provider: window.ethereum
    }
  }));
})();
```

### Execution Strategy
If a site fails with a QR code during a standard run:
1. Update `/home/ubuntu/.hermes/scripts/inject_wallet.js` to include the robust mock above.
2. If using Puppeteer, inject this using `page.evaluateOnNewDocument()` so it executes before React initializes.
3. This forces the dApp to render the "MetaMask" button, allowing standard `click()` automation to proceed.