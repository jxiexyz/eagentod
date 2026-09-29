# Bypassing Lazy Intent Links (Window.Open Override)

Some sites verify social tasks (like Twitter intent links) purely on the frontend by checking if the `<a>` tag was clicked. Clicking them normally spawns new popup tabs which can clutter the CDP session, trigger anti-bot blocks, or hang the script.

**Tactic:** Override `window.open` in the page context to return `null`, then programmatically click all intent links. This satisfies the frontend's click listener and triggers the UI's "DONE" state without actually opening any tabs.

```javascript
// 1. Disable popups globally in the page
await page.evaluate(() => {
    window.open = function() { return null; };
});

// 2. Click all intent links to trigger frontend verification
await page.evaluate(() => {
    const links = Array.from(document.querySelectorAll('a'))
                       .filter(a => a.href && a.href.includes('intent'));
    links.forEach(l => l.click());
});
```