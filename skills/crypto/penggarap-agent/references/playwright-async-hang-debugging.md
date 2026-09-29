# Debugging Playwright Async Hangs in Standalone Workers

When a standalone Python worker script (using `playwright.async_api`) hangs indefinitely without throwing an error, the root cause is almost always an un-timeout-wrapped async operation.

## Common Hang Points & Fixes

### 1. The `page.evaluate` Deadlock
When executing JS on a page that is navigating, reloading, or blocked by a modal, `page.evaluate` can hang forever waiting for the execution context to settle.

**Fix:** Wrap every evaluation in `asyncio.wait_for`.
```python
# BAD
text = await page.evaluate("document.body.innerText")

# GOOD
try:
    text = await asyncio.wait_for(
        page.evaluate("document.body.innerText"),
        timeout=10.0
    )
except asyncio.TimeoutError:
    text = "[page evaluation timeout - page may be loading or blocked]"
```

### 2. The Missing Popup
When a script clicks a button expecting a popup (like an OAuth window), but the popup is blocked by the browser or doesn't fire, the `wait_for_event("popup")` promise hangs.

**Fix:** Use `page.expect_popup` inside an `asyncio.wait_for` wrapper, and handle the timeout gracefully so execution can continue.
```python
# GOOD
async def click_and_check_popup():
    try:
        async with page.expect_popup(timeout=3000) as popup_info:
            await page.click(selector, timeout=3000)
        popup = await popup_info.value
        await popup.wait_for_load_state(timeout=3000)
        url = popup.url
        await popup.close()
        return url
    except:
        return None

popup_url = await asyncio.wait_for(click_and_check_popup(), timeout=5.0)
```

### 3. LLM API Timeouts
The OpenAI/LiteLLM client can hang indefinitely if the backend drops the connection without closing the socket.

**Fix:** Always wrap completions in `asyncio.wait_for`.
```python
# GOOD
try:
    resp = await asyncio.wait_for(
        llm_client.chat.completions.create(...),
        timeout=30.0
    )
except asyncio.TimeoutError:
    return "DONE: FAILED - LLM timeout"
```

### 4. Hidden Output Buffering
Sometimes the script isn't hung; it's just printing output that is being buffered by Python and not flushed to the supervisor process.

**Fix:** Force unbuffered output globally or flush explicitly.
```python
# Force unbuffered file logging
import sys
sys.stdout = open('/tmp/worker.log', 'a', buffering=1)

# Or flush explicit prints
print(f"Action: {action}", flush=True)
```