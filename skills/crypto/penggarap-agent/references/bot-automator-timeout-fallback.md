# bot_automator.py Timeout Fallback

## Symptom
Running `bot_automator.py` on a valid Telegram bot link repeatedly results in `[Command timed out after 60s]` (exit code 124) without any `sqlite3` database lock errors.

## Cause
`bot_automator.py` might hang trying to parse complex bot states, waiting for specific UI elements, or dealing with unhandled exceptions in its event loop. 

## Resolution / Fallback
If `bot_automator.py` times out consistently, use a minimal inline Telethon script via `terminal(command='python3 -c "..."')` to manually send the `/start` payload and read the immediate response. This bypasses the complex logic of `bot_automator.py`.

Example fallback script (replace `BOT_USERNAME` and `START_PAYLOAD`):
```python
import asyncio, os
from telethon import TelegramClient

API_ID = 37646267
API_HASH = '09f73a878754a488adc925ba9772725e'
SESSION_FILE = os.path.expanduser('~/.hermes/tg_new')

async def run():
    client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
    await client.start()
    
    chat = 'BOT_USERNAME'
    payload = 'START_PAYLOAD'
    
    # clear chat history first just in case
    async for msg in client.iter_messages(chat, limit=10):
        await msg.delete()
        
    await client.send_message(chat, f'/start {payload}')
    
    print('Waiting for bot response...')
    await asyncio.sleep(3)
    
    async for msg in client.iter_messages(chat, limit=1):
        print('MSG:', msg.text)
        if msg.buttons:
            for row in msg.buttons:
                for btn in row:
                    print('BTN:', btn.text)
    
    await client.disconnect()

asyncio.run(run())
```
This minimal script will output the bot's response text and buttons. **This is ONLY step 1 — reconnaissance.**

## CRITICAL: /start Is NOT Completion

Sending `/start` and reading the welcome message is **NEVER** a completed airdrop. You MUST continue:

### After /start, check the response:
1. **Bot has callback buttons** (BTN text with URL: None) → You must click them via `msg.click(text="Button Text")` or `msg.click(i=0, j=0)`
2. **Bot has URL buttons** (BTN text with URL: https://...) → Open URL in browser if it's a task, or note it as a webapp/mini-app
3. **Bot asks for tasks** (join channels, follow X, submit wallet) → Complete ALL tasks before reporting

### Full interaction template:
```python
import asyncio, os
from telethon import TelegramClient

API_ID = 37646267
API_HASH = '09f73a878754a488adc925ba9772725e'
SESSION_FILE = os.path.expanduser('~/.hermes/tg_new')

async def run():
    client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
    await client.start()
    
    chat = 'BOT_USERNAME'
    payload = 'START_PAYLOAD'
    
    async for msg in client.iter_messages(chat, limit=10):
        await msg.delete()
        
    await client.send_message(chat, f'/start {payload}')
    await asyncio.sleep(5)
    
    # Read response + buttons
    async for msg in client.iter_messages(chat, limit=1):
        print('MSG:', msg.text)
        if msg.buttons:
            for i, row in enumerate(msg.buttons):
                for j, btn in enumerate(row):
                    print(f'BTN[{i},{j}]:', btn.text, '| URL:', getattr(btn, 'url', None))
        
        # Click first callback button to proceed (adapt as needed)
        if msg.buttons:
            try:
                result = await msg.click(i=0, j=0)
                print('CLICKED:', msg.buttons[0][0].text)
                await asyncio.sleep(3)
                # Read NEW response after click
                async for new_msg in client.iter_messages(chat, limit=1):
                    print('NEW MSG:', new_msg.text)
                    if new_msg.buttons:
                        for row in new_msg.buttons:
                            for btn in row:
                                print('NEW BTN:', btn.text)
            except Exception as e:
                print('CLICK ERROR:', e)
    
    await client.disconnect()

asyncio.run(run())
```

### Decision tree after reading bot response:
- Welcome + "Play/Farm/Earn" button → **Click it**, read next screen, continue
- Task list (join X, follow, submit wallet) → **Complete each task** via MCP/Telethon
- "You already joined" / balance shown → **✅ already done**
- Mini App / WebApp button only → **❌ skip** (TMA hard-block)
- No response / error → **❌ bot mati**

### What counts as ✅ for TG bots:
- All available tasks completed (channels joined, X followed, wallet submitted)
- OR bot shows "Completed" / balance / reward confirmation
- NEVER just "/start sent" or "welcome message received"
