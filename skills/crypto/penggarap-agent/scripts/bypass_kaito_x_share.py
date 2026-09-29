# Origin Domain: waitlist.gte.xyz
# Date: 2026-08-21
# Specific Symptom: Playwright hangs/loses context on X (Twitter) intent share popup during Kaito waitlist apply flow.

async def bypass_kaito_share(page, share_selector="button:has-text('Post on X')", timeout=10000):
    import urllib.parse
    try:
        async with page.expect_popup(timeout=timeout) as popup_info:
            await page.locator(share_selector).click()
        
        popup = await popup_info.value
        await popup.wait_for_load_state('domcontentloaded')
        share_url = popup.url
        await popup.close()
        
        parsed = urllib.parse.urlparse(share_url)
        params = urllib.parse.parse_qs(parsed.query)
        tweet_text = params.get('text', [''])[0]
        link_param = params.get('url', [''])[0]
        
        return {
            'success': True,
            'content': f'{tweet_text} {link_param}'.strip(),
            'raw_url': share_url
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}
