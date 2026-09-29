# Origin Domain: docs.google.com
# Date: 2026-08-26
# Specific Symptom: Playwright native fill/click fails on custom ARIA div inputs and buttons

async def fill_google_form_input(page, label_text, fill_text):
    js_script = '''([label, val]) => {
        const items = Array.from(document.querySelectorAll('div[role="listitem"]'));
        for (const item of items) {
            if (item.innerText.includes(label)) {
                const input = item.querySelector('input[type="text"], textarea');
                if (input) {
                    input.value = val;
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                    input.dispatchEvent(new Event('change', { bubbles: true }));
                    return true;
                }
            }
        }
        return false;
    }'''
    return await page.evaluate(js_script, [label_text, fill_text])

async def bypass_google_form_submit(page):
    js_script = '''() => {
        const buttons = Array.from(document.querySelectorAll('div[role="button"]'));
        for (const btn of buttons) {
            const text = btn.innerText ? btn.innerText.toLowerCase() : '';
            if (text.includes('submit') || text.includes('kirim') || text.includes('next') || text.includes('berikutnya')) {
                btn.click();
                return true;
            }
        }
        return false;
    }'''
    await page.wait_for_selector('form', timeout=10000)
    result = await page.evaluate(js_script)
    if result:
        await page.wait_for_timeout(3000)
    return result
