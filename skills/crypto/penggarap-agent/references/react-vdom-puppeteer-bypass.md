# React VDOM Puppeteer Bypass

When standard CDP `browser_type` or `browser_click` fails to update the React state (e.g., the submit button remains disabled because React doesn't know the input changed), use this Node.js Puppeteer snippet. 

## The React 16+ Input Setter

React overrides native DOM input setters. To bypass this and force an update, you must call the prototype setter directly and dispatch a bubbling input event.

```javascript
const setNativeValue = (element, value) => {
    const valueSetter = Object.getOwnPropertyDescriptor(element, 'value').set;
    const prototype = Object.getPrototypeOf(element);
    const prototypeValueSetter = Object.getOwnPropertyDescriptor(prototype, 'value').set;
    
    if (valueSetter && valueSetter !== prototypeValueSetter) {
        prototypeValueSetter.call(element, value);
    } else {
        valueSetter.call(element, value);
    }
    
    element.dispatchEvent(new Event('input', { bubbles: true }));
};
```

## Full Usage Template (Node.js)

Save this template to a file (e.g., `/home/ubuntu/.hermes/scripts/bypass.js`) and run it via `node bypass.js`.

```javascript
const puppeteer = require('puppeteer-core');

(async () => {
    const browser = await puppeteer.connect({
        browserURL: 'http://localhost:9222',
        defaultViewport: null
    });
    
    const pages = await browser.pages();
    // Target the specific tab by URL
    const page = pages.find(p => p.url().includes('TARGET_DOMAIN_HERE')); 
    
    if (page) {
        await page.evaluate(() => {
            const setNativeValue = (element, value) => {
                const valueSetter = Object.getOwnPropertyDescriptor(element, 'value').set;
                const prototype = Object.getPrototypeOf(element);
                const prototypeValueSetter = Object.getOwnPropertyDescriptor(prototype, 'value').set;
                if (valueSetter && valueSetter !== prototypeValueSetter) {
                    prototypeValueSetter.call(element, value);
                } else {
                    valueSetter.call(element, value);
                }
                element.dispatchEvent(new Event('input', { bubbles: true }));
            };

            // Example 1: Find and fill a text input
            const inputs = document.querySelectorAll('input[type="text"]');
            const handleInput = Array.from(inputs).find(el => el.placeholder.toLowerCase().includes('handle') || el.name.toLowerCase().includes('handle'));
            if(handleInput) {
                setNativeValue(handleInput, '@chiquast');
            }

            // Example 2: Check all checkboxes
            const checkboxes = document.querySelectorAll('input[type="checkbox"]');
            checkboxes.forEach(cb => {
                if(!cb.checked) {
                   cb.click(); 
                }
            });

            // Example 3: Enable and click the submit button
            const submitBtn = document.querySelector('button[type="submit"]') || Array.from(document.querySelectorAll('button')).find(b => b.textContent.toLowerCase().includes('submit'));
            if(submitBtn) {
                submitBtn.removeAttribute('disabled');
                submitBtn.click();
            }
        });
        
        // Wait for network requests/transitions
        await new Promise(r => setTimeout(r, 4000));
        
        // Verify success
        const content = await page.evaluate(() => document.body.innerText);
        console.log(content.slice(0, 500));
        
        // IMPORTANT: Close the tab to free memory
        await new Promise(r => setTimeout(r, 2000));
        await page.close();
        console.log("CLOSED");
    } else {
        console.log("Page not found");
    }
    
    browser.disconnect();
})();
```

## Critical Pitfalls
- **Language**: **Never** use Python `pyppeteer` for custom DOM bypass scripts. It frequently throws `ModuleNotFoundError`. Always use Node.js and `puppeteer-core`.
- **Delays**: `page.waitForTimeout` is deprecated and will crash the script. Use `await new Promise(r => setTimeout(r, 2000));`.
- **Cleanup**: Always ensure you call `await page.close();` at the end to prevent the headless Chrome port from exhausting memory.