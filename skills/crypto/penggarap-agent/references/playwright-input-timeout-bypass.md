# Playwright Input Fill Timeout Bypass

When automating stubborn React forms via Playwright over a CDP connection, standard selectors like `page.fill('input:has-text("...")')` or `page.fill('input:nth-child(n)')` often fail with `Timeout 30000ms exceeded`. This happens because Playwright's actionability checks (waiting for the element to be stable/visible) get confused by React's Virtual DOM or Shadow DOM implementations.

## The Fix: Native Query Indexing

Instead of relying on Playwright's pseudo-selectors to find and fill in one step, query all inputs natively, check the array length, and index them directly.

```python
inputs = await page.query_selector_all('input')
if len(inputs) >= 2:
    # Bypass selector timeouts by indexing the array directly
    await inputs[0].fill('value1')
    await inputs[1].fill('value2')
    
    # Force enable and click the submit button via evaluate
    await page.evaluate('''() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Continue'));
        if (btn) {
            btn.removeAttribute('disabled');
            btn.click();
        }
    }''')
else:
    print('Inputs not found')
```