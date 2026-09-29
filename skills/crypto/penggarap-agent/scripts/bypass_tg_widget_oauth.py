# Metadata: digitsbt.ngrndrewards.com, 2026-08-23, Telegram widget OAuth interaction failure
import asyncio

async def auth_telegram_widget(page, bot_name: str, phone_number: str = None):
    '''
    Handles the Telegram OAuth widget (oauth.telegram.org) login flow.
    Clicks the widget iframe, waits for the popup, enters phone number, 
    and waits for the user to confirm via the Telegram app.
    '''
    try:
        # Click the widget iframe to open the popup
        async with page.expect_popup() as popup_info:
            widget_frame = page.frame_locator(f'iframe[id^="telegram-login-{bot_name}"]')
            await widget_frame.locator('button.tgme_widget_login_button').click(timeout=10000)

        popup = await popup_info.value
        await popup.wait_for_load_state('networkidle')

        # Check if already authorized (popup might close or redirect)
        if popup.is_closed():
            return True

        if phone_number:
            # Wait for the phone number input field
            phone_input = popup.locator('input#login-phone')
            await phone_input.wait_for(state='visible', timeout=15000)
            
            # Clear and fill the phone number
            await phone_input.fill(phone_number)
            
            # Click the Next button
            await popup.locator('button.login_head_submit_btn').click()
            
            print("Phone number submitted. Waiting for manual confirmation in Telegram app...")
            # Wait for the user to click 'Confirm' in their Telegram app
            # The popup will navigate/close once confirmed.
            try:
                await popup.wait_for_event('close', timeout=60000)
                return True
            except:
                print("Timeout waiting for Telegram app confirmation.")
                return False
        
        return False
    except Exception as e:
        print(f"Telegram Widget OAuth failed: {e}")
        return False