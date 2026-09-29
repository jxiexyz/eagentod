#!/usr/bin/env python3
import asyncio
import re
import json
import os
from telethon import TelegramClient

API_ID = 37646267
API_HASH = '09f73a878754a488adc925ba9772725e'
SESSION_FILE = '/home/ubuntu/.hermes/tg_new.session'
GROUP_ID = -1003818905785
TOPIC_ID = 31

DONE_FILE = '/home/ubuntu/.hermes/airdrop_data/worker_done.json'

async def main():
    if not os.path.exists(DONE_FILE):
        with open(DONE_FILE, 'w') as f:
            json.dump({"done": [], "failed": []}, f)
            
    with open(DONE_FILE, 'r') as f:
        data = json.load(f)
        done_list = data.get("done", [])
        failed_list = data.get("failed", [])

    client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
    await client.connect()
    
    if not await client.is_user_authorized():
        print("Error: Telethon session not authorized.")
        return
        
    messages = await client.get_messages(GROUP_ID, reply_to=TOPIC_ID, limit=30)
    
    # Reverse so we process oldest unread first
    messages.reverse()
    
    found = False
    for msg in messages:
        text = msg.text or ""
        # Match Project Name (either **Name** or plain URL line)
        urls = re.findall(r'https?://[^\s<>"]+', text)
        
        if not urls:
            continue
            
        for url in urls:
            # Simple domain extraction for project name if **Name** isn't used
            domain_match = re.search(r'https?://(?:www\.)?([^/]+)', url)
            project_name = domain_match.group(1) if domain_match else url
            
            identifier = f"{project_name} (Msg {msg.id})"
            
            # Skip if already done or failed
            if identifier in done_list or identifier in failed_list:
                continue
                
            # Print the FIRST ungaraped project and exit (one by one batching)
            print(f"**{identifier}**\n{url}")
            found = True
            break
            
        if found:
            break
            
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())