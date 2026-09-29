# Tesserapp (tesserapp.org) Raffle Automation Reference

Tesserapp adalah Web3 raffle platform (gated entries, X tasks, Discord verification, wallet checks).

## Core Architecture & State
- **URL Pattern:** `https://tesserapp.org/raffle/<raffle-slug>`
- **Linked Accounts in CDP Chrome (`localhost:9222`):**
  - X / Twitter: `@chiquast`
  - EVM Wallet: `0x444b38c15ccc46db22b9590497023d91e506b2ff` (Linked)
  - Discord: `yaelah` (ID Linked, email `yantow713@gmail.com`)
- **Backend Verification Flow:**
  When user clicks `ENTER RAFFLE`, frontend dispatches concurrent API requests:
  1. `POST /user/check-requirements` (Discord server, roles, min followers, wallet status)
  2. `POST /twitter/check-follows` (`{"targets": [...], "forceEscalate": true}`)
  3. `POST /twitter/check-reply` (`{"tweetId": "...", "raffleId": "..."}`)
  4. `POST /raffles/entry-challenge` -> receives nonce & challenge token
  5. `POST /raffles/<raffleId>/enter` -> receives HTTP 201 with `enteredAt`, `multiplier`

## Automated Execution Steps

### 1. Extract Tasks from Raffle Page
Connect over CDP (`http://127.0.0.1:9222`), navigate to target raffle:
```javascript
const links = Array.from(document.querySelectorAll('a')).map(a => ({ text: a.innerText.trim(), href: a.href }));
const followLinks = links.filter(l => l.href.includes('intent/follow') || l.href.includes('x.com/'));
const replyLinks = links.filter(l => l.href.includes('intent/tweet?in_reply_to='));
const discordLinks = links.filter(l => l.href.includes('discord.gg/'));
```

### 2. Solve Requirements Autonomously
1. **X Follow Tasks:**
   - Extract screen name from URL (`?screen_name=<handle>` or `x.com/<handle>`).
   - Get numeric ID: `python3 ~/.hermes/scripts/x_research.py user <handle> | jq -r .id`
   - Execute follow: `mcp__airdrop_tools__x_action(action="follow", target_id="<numeric_id>")`
2. **X Like / Retweet Tasks:**
   - Extract tweet ID from URL (`/status/<tweet_id>`).
   - Execute: `mcp__airdrop_tools__x_action(action="like", target_id="<tweet_id>")`
   - Execute: `mcp__airdrop_tools__x_action(action="retweet", target_id="<tweet_id>")`
3. **X Reply Task:**
   - Read tweet first: `mcp__airdrop_tools__x_read_tweet(tweet_id="<tweet_id>")`
   - Send concise non-emoji reply: `mcp__airdrop_tools__x_reply_tweet(tweet_id="<tweet_id>", text="<reply under 15 words>")`
4. **Discord Join (if needed):**
   - If server not joined, join via Telethon/invite or browser session. If Discord role gated and user lacks role, mark as role-gated blocker.

### 3. Trigger Submission & Verify Artifact
- Click button: `button:has-text("ENTER RAFFLE")`
- Await 3-5 seconds for API completion.
- **Genuine DOM Proof Artifact:**
  - Banner / Toast text: `"You're in. Good luck!"`
  - Body status: `"ENTERED"`
  - API response: `[201] https://api.tesserapp.org/raffles/<id>/enter`
- Report to Topic 42 with the exact DOM verification text: `✅ Kelar bro! tesserapp.org: You're in. Good luck! (ENTERED)`
