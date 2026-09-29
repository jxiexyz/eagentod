# Pitfall: x_read_tweet returns "undefined"

Sometimes the `mcp_airdrop_tools_x_read_tweet(tweet_id)` tool fails to parse the tweet and returns exactly `"undefined"`.

**Workaround:**
If you need to read the tweet to understand instructions (e.g., drop SOL address, tag friends), DO NOT skip.
1. Fallback to `web_extract(urls=["https://x.com/i/status/<tweet_id>"])`.
2. The extraction will return the full text of the tweet and comments, allowing you to parse the instructions.
3. Proceed to reply or execute the required action using `mcp_airdrop_tools_x_reply_tweet`.
