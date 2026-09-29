# Puppeteer & DOM querySelector Pitfalls

When using `page.evaluate()` or standard `document.querySelector` in Puppeteer/Node scripts:

**DO NOT** use Playwright-specific pseudo-classes like `:has-text("Submit")`. It will throw a `DOMException: SyntaxError`. Puppeteer's native DOM queries do not support it.

**WORKAROUND:** Use standard CSS to select all elements, then filter via standard JS array methods.

```javascript
// ❌ WRONG (Playwright only syntax):
const btn = document.querySelector('button:has-text("SUBMIT")');

// ✅ CORRECT (Standard DOM/Puppeteer evaluate):
const btns = Array.from(document.querySelectorAll('button'));
const btn = btns.find(b => b.innerText.includes('SUBMIT'));
if (btn) btn.click();
```