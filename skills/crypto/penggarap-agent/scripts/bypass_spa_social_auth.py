# Metadata: Origin Domain: event.neosoul.ai | Date: 2026-08-21 | Symptom: React SPA failure during EVM wallet connect, dynamic invite code input, and Twitter OAuth popup.

def bypass_spa_auth(page, invite_code: str, wallet_selector: str = 'text=Connect Wallet', invite_input_selector: str = 'input', twitter_selector: str = 'text=Twitter'):
    try:
        if page.locator(wallet_selector).is_visible():
            page.click(wallet_selector)
            page.wait_for_timeout(2000)

        for el in page.locator(invite_input_selector).all():
            placeholder = (el.get_attribute('placeholder') or '').lower()
            if 'code' in placeholder or 'invite' in placeholder:
                el.fill(invite_code)
                page.keyboard.press('Enter')
                page.wait_for_timeout(1000)
                break

        if page.locator(twitter_selector).is_visible():
            with page.expect_popup() as popup_info:
                page.click(twitter_selector)
            popup = popup_info.value
            popup.wait_for_load_state('domcontentloaded')
            auth_btn = popup.locator('[data-testid="OAuth_Consent_Button"]')
            if auth_btn.is_visible():
                auth_btn.click()
            try:
                popup.wait_for_event('close', timeout=10000)
            except:
                pass
        
        return True
    except Exception as e:
        print(f'Bypass error: {e}')
        return False
