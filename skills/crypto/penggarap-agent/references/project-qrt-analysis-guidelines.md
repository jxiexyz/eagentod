# Project QRT & Tweet Analysis Guidelines (English Only)

When an airdrop / whitelist task strictly requires posting a Quote Retweet (QRT) or tweet about the project to earn points or complete verification:

## 1. Core Principles
- **Language**: MUST BE 100% ENGLISH. No Indonesian, no broken slang.
- **Length**: Maximum 280 characters. Dense, concise, high information density.
- **Tone**: Insightful, objective, analytical conviction (why bullish / why it matters to the ecosystem).
- **No Tagging Spam**: NEVER tag random accounts (no @ekonuriyanto, no @leonking69z). Only tag the project handle if required by the quest.
- **NO Static Templates**: Do NOT reuse boilerplate templates. Dynamically analyze the project value prop based on its real narrative, chain/ecosystem, and utility.

## 2. Structure (Dense Analysis in < 280 chars)
1. **Ecosystem & Thesis**: Contextualize project in its ecosystem (e.g. ZEC, Soneium, Monad, Berachain, Base, Solana).
2. **Value Prop & Mechanism**: What does it actually solve/build? (e.g. yield-bearing NFT, privacy DeFi primitive, AI agent coordination layer, intent-based swap).
3. **Ecosystem Catalyst / Bullish Factor**: Why it drives network activity or sustainable utility.

## 3. Example Reference
> "The expansion of privacy-native apps on $ZEC is gaining momentum. @ZeckersNFT isn't just an avatar collection—it links NFT assets directly to $ZEC yield mechanisms. Holding aligns incentives with ecosystem growth as utility and on-chain sinks scale." (258 chars)

## 4. Execution Rules
- Inspect project info from the webpage / target tweet first (`browser_snapshot` or `x_read_tweet`).
- Generate a project-specific insight adhering to the principles above.
- Verify character count <= 280 before posting.
- **Preferred Method (Zero DOM / No selector trap):**
  Append the target tweet URL directly to the text:
  `mcp_airdrop_tools_x_post_with_image(text=f"{analysis}\n\nhttps://x.com/{target_author}/status/{tweet_id}")`
  X automatically converts the trailing status URL into a native Quote Tweet.
- **CRITICAL PITFALL: NEVER search global `[data-testid="retweet"]` on a status page:**
  If the main tweet was already retweeted, its button is `[data-testid="unretweet"]`. A global `page.query_selector('[data-testid="retweet"]')` will bypass the main tweet and grab the first UNRETWEETED comment/reply below it, quoting a random user's comment!
- **CDP Fallback (If manual browser click strictly needed):**
  Scope selector ONLY inside the main tweet article:
  ```python
  main_article = page.locator('article[data-testid="tweet"]').first
  rt_btn = main_article.locator('[data-testid="retweet"], [data-testid="unretweet"]').first
  await rt_btn.click()
  # Then click "Quote" / "Kutip" from the opened dropdown menu
  ```
