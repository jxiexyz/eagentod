# Pitfall: tg_join_group.py on Telegram Bots

If `bot_automator.py` times out or fails on a Telegram Bot (`t.me/BotName_bot`), DO NOT attempt to use `tg_join_group.py` as a fallback. 
`tg_join_group.py` is strictly for channels/groups. Running it on a Bot User ID will result in:
`Cannot cast InputPeerUser to any kind of InputChannel.`

**Action:** If `bot_automator.py` times out or fails on a bot, report ❌ (timeout/unresponsive bot) and move on.
