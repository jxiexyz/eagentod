# Metadata: rewards.svpstars.com, 2026-09-25, Playwright text extraction failing due to visibility/hidden CSS

async def extract_hidden_text(page, selector: str) -> str:
    """Bypass visibility checks to extract text from hidden DOM elements."""
    try:
        await page.wait_for_selector(selector, state="attached", timeout=10000)
        return await page.evaluate(
            '(sel) => { const el = document.querySelector(sel); return el ? el.textContent.trim() : null; }',
            selector
        )
    except Exception as e:
        return f"Error: {e}"
