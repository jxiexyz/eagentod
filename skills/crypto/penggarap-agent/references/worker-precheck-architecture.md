# Worker Precheck Script Architecture (Jul 2026)

## Pattern
Cron job uses `script` field pointing to `worker_precheck.py`. Script reads Topic 31 DB, filters links, prints to stdout. Hermes behavior:
- **Stdout empty** → LLM never invoked (0 tokens). ~95% of runs.
- **Stdout non-empty** → Injected as "Script Output" section in prompt. Agent sees links and garap.

## Link Filtering (at source, not in LLM)
`worker_precheck.py` and `get_topic31.py` both filter:

### Skip domains (never airdrop targets)
x.com, twitter.com, discord.gg, discord.com, t.co, play.google.com, apps.apple.com, youtube.com, youtu.be, medium.com, mirror.xyz, github.com, docs.google.com, notion.so

### Skip patterns
- `OkxWalletPayBot` in URL
- `galxe.com` (separate job)
- t.me links without `?start=` (group links, not bot)

### Task naming
- Web: `domain (Msg ID)` — e.g., `conso.xyz (Msg 1785083781)`
- TG bot: `t.me/BotName (Msg ID)` — e.g., `t.me/poinly_bot (Msg 1785076426)`

### Dedup
- Checks against `worker_done.json` (union of `done` + `failed` arrays)
- Within-run dedup by `domain:msg_id` key

## worker_done.json Hygiene
- Items should NOT appear in both `done` and `failed`. Periodically clean:
  ```python
  both = set(done) & set(failed)
  done = [x for x in done if x not in both]  # keep in failed only
  ```
- `update_done.py` adds to `done` before garap starts
- `update_failed.py` adds to `failed` after failure
- Both check for duplicates before appending

## Cron Job Config
- `script: worker_precheck.py` — precheck feeds data
- `skills: ['penggarap-agent']` — SOP loaded
- `workdir: /home/ubuntu/.hermes/scripts` — scripts resolve relative
- `model: ag/gemini-pro-agent` via `custom:9router`
- `schedule: every 15m`
