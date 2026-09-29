# Hidden Form CSS Bypass (Display/Opacity/Visibility)

When a form is in the DOM but hidden from Playwright/Puppeteer (e.g., zero opacity, `display: none` on a parent container), the inputs might exist but `.is_visible()` returns `False`. Normal `page.fill()` will fail with a TimeoutError waiting for the element to be visible.

## Identification
- `page.query_selector_all('input')` finds inputs, but `.is_visible()` is `False`.
- HTML snapshot shows the inputs exist (e.g., `<input class="refinput">` or other input tags).

## Solution: Walk the DOM Tree
Inject JavaScript to walk up the parent tree of the hidden inputs and force them to be visible by overriding the CSS styles:

```javascript
page.evaluate('''() => {
    // Target inputs or specific classes (e.g., '.refinput')
    document.querySelectorAll('input, .refinput').forEach(el => {
        let parent = el.parentElement;
        while(parent && parent.tagName !== 'BODY') {
            parent.style.display = 'block';
            parent.style.opacity = '1';
            parent.style.visibility = 'visible';
            parent = parent.parentElement;
        }
    });
}''')
```

After forcing visibility, `page.fill()` and `page.locator(...).click(force=True)` will work natively.