# Telegram Mini App (TMA) Limitations

## Issue
When automating Telegram airdrop bots via `bot_automator.py`, the bot may respond with a prompt to open a Web App / Mini App (e.g., "Tap [START EARN] to open the app").

## Limitation
Currently, `bot_automator.py` **does not support** clicking Web App buttons or extracting TMA URLs natively. Sending the wallet address as a chat message will fail if the bot strictly expects it via the TMA interface. 

## Action
If you encounter a bot requiring TMA interaction:
1. Do not attempt to guess or brute-force the TMA URL via scripts.
2. Immediately report the task as skipped/failed to `post_topic42.py` (e.g., "❌ [BotName] mentok bro, minta masukin lewat Mini App (TMA), bot_automator ga support tap web app button. Skip dulu.").
3. Run `cleanup_tabs.py` and proceed to the next task.
