# Metadata: bubblebuns.xyz, 2026-08-26, bot_check_failed / Turnstile rejection on stale form
import asyncio

async def run(page):
    """
    Bypass for BubbleBuns WL form where 'bot_check_failed' or 'session_expired' occurs
    due to stale tickets and Turnstile tokens. We extract current values, reload, 
    quickly refill, natively click the turnstile, and submit.
    """
    print("[*] Extracting current form values before reload...")
    values = await page.evaluate('''() => {
        return {
            handle: document.getElementById('in-handle') ? document.getElementById('in-handle').value : '',
            wallet: document.getElementById('in-wallet') ? document.getElementById('in-wallet').value : '',
            tweet: document.getElementById('in-tweet') ? document.getElementById('in-tweet').value : '',
            category: document.getElementById('in-category') ? document.getElementById('in-category').value : 'art',
            bun: document.getElementById('in-bun') ? document.getElementById('in-bun').value : '',
            why: document.getElementById('in-why') ? document.getElementById('in-why').value : ''
        };
    }''')
    
    print("[*] Reloading for fresh ticket and Turnstile...")
    await page.reload(wait_until='domcontentloaded')
    await asyncio.sleep(4)
    
    print("[*] Restoring form values...")
    await page.evaluate('''v => {
        if(document.getElementById('in-handle')) document.getElementById('in-handle').value = v.handle;
        if(document.getElementById('in-wallet')) document.getElementById('in-wallet').value = v.wallet;
        if(document.getElementById('in-tweet')) document.getElementById('in-tweet').value = v.tweet;
        if(document.getElementById('in-category')) document.getElementById('in-category').value = v.category;
        if(document.getElementById('in-bun')) document.getElementById('in-bun').value = v.bun;
        if(document.getElementById('in-why')) document.getElementById('in-why').value = v.why;
    }''', values)
    
    print("[*] Solving Turnstile via native mouse click...")
    ts_widget = await page.query_selector('#ts-widget, .cf-turnstile')
    if ts_widget:
        box = await ts_widget.bounding_box()
        if box:
            click_x = box['x'] + 30
            click_y = box['y'] + box['height'] / 2
            await page.mouse.move(click_x, click_y, steps=5)
            await page.mouse.down()
            await asyncio.sleep(0.1)
            await page.mouse.up()
            
            for _ in range(15):
                await asyncio.sleep(1)
                token = await page.evaluate('''() => {
                    const el = document.querySelector('[name="cf-turnstile-response"]');
                    return el ? el.value : '';
                }''')
                if token:
                    print("[+] Turnstile token acquired!")
                    break
    else:
        print("[-] Turnstile widget not found.")
    
    print("[*] Submitting form...")
    submit_btn = await page.query_selector('#send, button[type="submit"]')
    if submit_btn:
        await submit_btn.click()
        
    await asyncio.sleep(5)
    
    success = await page.evaluate('''() => {
        const succ = document.getElementById('success');
        return succ && succ.style.display === 'block';
    }''')
    if success:
        print("[+] Application successful!")
    else:
        gerr = await page.evaluate('''() => {
            const g = document.getElementById('gerr');
            return (g && g.style.display === 'block') ? g.innerText : null;
        }''')
        if gerr:
            print("[-] Global error:", gerr)
    
    return True
