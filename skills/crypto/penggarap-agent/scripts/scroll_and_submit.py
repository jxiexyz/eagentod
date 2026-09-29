# Origin Domain: app.bitrobot.ai
# Date: 2026-08-22
# Symptom: Email waitlist form requires scrolling down to become visible/interactable.

import asyncio

async def bypass(page, input_selector: str, submit_selector: str, input_value: str, scroll_delay: int = 2000):
    await page.evaluate('''
        async () => {
            await new Promise((resolve) => {
                let totalHeight = 0;
                const distance = 200;
                const timer = setInterval(() => {
                    const scrollHeight = document.body.scrollHeight;
                    window.scrollBy(0, distance);
                    totalHeight += distance;
                    if(totalHeight >= scrollHeight - window.innerHeight) {
                        clearInterval(timer);
                        resolve();
                    }
                }, 50);
            });
        }
    ''')
    await page.wait_for_timeout(scroll_delay)
    
    input_element = page.locator(input_selector).first
    await input_element.wait_for(state="visible", timeout=10000)
    await input_element.scroll_into_view_if_needed()
    await input_element.fill(input_value)
    
    submit_element = page.locator(submit_selector).first
    await submit_element.wait_for(state="visible", timeout=5000)
    await submit_element.click()
    
    return True
