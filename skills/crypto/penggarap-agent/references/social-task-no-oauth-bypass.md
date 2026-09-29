# Social Task Validation Bypass (No OAuth)

Some modern airdrop campaigns (like `luckycall.lol/whitelist`) feature social tasks (Follow, Like, Retweet) but **do not use OAuth** to verify them. 

Instead, they rely purely on the frontend state (React state or LocalStorage) changing when the user clicks the action link.

### The Trap
If you attempt to complete the OAuth flow on these sites (assuming you need to authorize an app), you will get stuck in an infinite loop because there is no app to authorize — the link just opens twitter.com in a new tab.

### The Bypass (DOM Injection)
When a site explicitly states it doesn't verify the account, or when you notice the social action buttons are just plain links (`<a target="_blank" href="https://x.com/...">`), you can bypass the entire flow using Playwright DOM evaluation:

1. **Simulate the clicks on all required links simultaneously.**
   Remove the `target` attribute so it doesn't spawn unmanageable tabs, or just let it click and close the new tabs if the state is bound to the click event.

2. **Inject state overrides.**
   Many forms track completion via LocalStorage. Inject the state:
   ```javascript
   window.localStorage.setItem('x_followed', 'true');
   window.localStorage.setItem('x_liked', 'true');
   window.localStorage.setItem('x_reposted', 'true');
   window.localStorage.setItem('x_commented', 'true');
   ```

3. **Force the final submit.**
   Remove the `disabled` attribute from the final button and click it:
   ```javascript
   const btn = document.querySelector('button:last-of-type');
   if (btn) {
       btn.removeAttribute('disabled');
       btn.click();
   }
   ```

### Full Example Snippet (Playwright Async)

```python
await page.evaluate('''() => {
    // 1. Click all social links to trigger frontend state listeners
    const links = Array.from(document.querySelectorAll('a'));
    links.filter(a => a.textContent.includes('OPEN LINE') || a.href.includes('x.com')).forEach(a => {
        a.removeAttribute('target');
        a.click();
    });
    
    // 2. Inject LocalStorage overrides just in case
    window.localStorage.setItem('x_followed', 'true');
    window.localStorage.setItem('x_liked', 'true');
    window.localStorage.setItem('x_reposted', 'true');
}''')

await asyncio.sleep(3) # Wait for React state to settle

await page.evaluate('''() => {
    // 3. Force submit
    const btn = document.querySelector('button:last-of-type');
    if(btn) {
        btn.removeAttribute('disabled');
        btn.click();
    }
}''')
```