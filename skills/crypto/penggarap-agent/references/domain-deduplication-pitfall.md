# Domain Deduplication Pitfall

When Telegram channels repost the same airdrop/campaign links under slightly different project names or in new message IDs, the worker may get stuck in a loop repeatedly processing the same target domain (e.g., `app.rally.fun`) and failing on the same rules.

## Root Causes & Fix Pattern

1. **Worker Precheck (`worker_precheck.py`)**: 
   Deduplication must track the raw `domain` globally across the pending queue (`if domain in seen_domains:`), NOT `domain:msg_id`. Tracking by `msg_id` defeats deduplication when the same link is posted in multiple messages.
   
2. **Researcher Cron (`momo_researcher_cron.py`)**: 
   Deduplication must check the `base_domain` of the extracted URL against previously posted projects, rather than relying solely on exact string matches of the project name (e.g., "Rally" vs "Rally Campaigns"). Expand the dedupe logic to canonicalize domains and check if they already exist in the `posted_projects` set.