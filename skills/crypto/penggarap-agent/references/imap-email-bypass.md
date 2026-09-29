# IMAP Email Bypass for OTPs & Verification Links

## The Problem
When a web3 airdrop or waitlist form requires an email OTP or verification link, attempting to automate Gmail via a headless browser (Puppeteer/Playwright/CDP) causes two major issues:
1. **State Loss:** Navigating away from the active form in the same tab destroys the form's session state. When returning, the form resets.
2. **Security Blocks:** Google's anti-bot systems frequently flag headless browsers, triggering Turnstile/reCAPTCHA loops or outright blocking logins.

## The Solution: IMAP Python Script
Never use the browser to read email. Instead, use a lightweight Python IMAP script (`gmail.py`) to fetch the latest emails in the background, extract the required data using regex, and return it to the agent.

### Usage in Agent Workflow
```bash
# Fetch 6-digit OTP
python3 /home/ubuntu/.hermes/scripts/gmail.py "junamkaudek@gmail.com" "APP_PASSWORD" "otp" "project_keyword"

# Fetch Verification Link
python3 /home/ubuntu/.hermes/scripts/gmail.py "junamkaudek@gmail.com" "APP_PASSWORD" "link" "project_keyword"
```

### gmail.py Implementation
```python
import imaplib
import email
import re
import sys
from email.header import decode_header

def fetch_gmail(email_addr, app_password, action="otp", keyword=""):
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_addr, app_password)
        mail.select("inbox")
        
        status, messages = mail.search(None, "ALL")
        if status != "OK": return "Error: Cannot search emails"
            
        email_ids = messages[0].split()
        if not email_ids: return "Error: Inbox empty"
            
        # Check last 5 emails
        for e_id in reversed(email_ids[-5:]):
            res, msg_data = mail.fetch(e_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    sender = msg.get("From", "")
                    subject_hdr = decode_header(msg.get("Subject", ""))[0]
                    subject = subject_hdr[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(subject_hdr[1] if subject_hdr[1] else "utf-8", errors="ignore")
                        
                    if keyword and keyword.lower() not in sender.lower() and keyword.lower() not in subject.lower():
                        continue
                        
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode(errors="ignore")
                                break
                    else:
                        body = msg.get_payload(decode=True).decode(errors="ignore")
                        
                    if action == "otp":
                        m = re.search(r'\b(\d{4,8})\b', body)
                        return m.group(1) if m else "OTP not found"
                    elif action == "link":
                        m = re.search(r'https?://[^\s"\'<>]+', body)
                        return m.group(0) if m else "Link not found"
                    else:
                        return body[:1000]
                        
        return "No matching email found"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    print(fetch_gmail(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else ""))
```
