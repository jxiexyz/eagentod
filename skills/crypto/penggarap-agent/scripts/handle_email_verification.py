# Origin Domain: intersticedigital.io
# Date: 2026-08-21
# Symptom: Registration blocked at email OTP verification step

import time
import subprocess

async def handle_email_verification(page, email: str, email_selector: str, submit_selector: str, otp_selector: str, otp_submit_selector: str = None):
    """
    Fills email, triggers OTP, waits for OTP via local imap_reader, and fills it.
    """
    await page.wait_for_selector(email_selector, state='visible')
    await page.fill(email_selector, email)
    await page.click(submit_selector)
    
    otp_code = None
    for _ in range(15):
        time.sleep(10)
        try:
            result = subprocess.check_output(
                ['python3', '/home/ubuntu/.hermes/skills/crypto/penggarap-agent/scripts/imap_reader.py', email],
                text=True
            ).strip()
            if result:
                otp_code = result
                break
        except Exception:
            continue
            
    if not otp_code:
        raise Exception("Timeout waiting for email OTP.")
        
    await page.wait_for_selector(otp_selector, state='visible')
    await page.fill(otp_selector, otp_code)
    
    if otp_submit_selector:
        await page.click(otp_submit_selector)
        
    return True
