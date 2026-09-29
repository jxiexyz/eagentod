# Strict Persistence Pattern in Cron Prompts

## The Problem: Premature Surrender
Agent workers naturally tend toward the path of least resistance. If `browser_navigate` returns a blank page, or a button click fails on the first try, the agent will often immediately conclude `FAILED: Site unreachable` or `FAILED: Button not working` and move on.

The user explicitly rejected this behavior:
> "hmm apakah ini seperti gamau berusaha? mskdnya cara ini gagal kita test cara lain, kalo udah mentok baru ggal?"

## The Solution: Explicit Persistence Constraints

When authoring prompts for cron jobs that execute web tasks, you MUST include strict persistence rules that force the LLM to exhaust multiple approaches before it is allowed to fail.

### The Pattern to Inject

Include this block in the cron prompt:

```yaml
CRITICAL RULE: MINIMAL 8 BROWSER ACTIONS sebelum boleh report FAILED. Jangan cepat nyerah!

GARAP DENGAN GIGIH (8+ actions):
- browser_navigate(url) → kalau blank: wait 10s → retry
- browser_snapshot() → analisis semua element
- Try multiple: Email/Google OAuth → Connect Wallet → form fill → submit
- Minimal 8 actions (navigate + snapshot + click + type dll) sebelum nyerah

FAIL CRITERIA (after trying hard):
- Cloudflare captcha > 3 retry
- Site 404/500
- Not airdrop (Discord/Twitter only)
- Missing credential
```

### Metrics (Before / After)

Applying this pattern yielded immediate results in production:

**Target:** `datahive.ai`
- **Before Pattern**: Agent tried `Connect Wallet`, couldn't immediately find a success banner, and reported `❌ Failed - unable to find success text`.
- **After Pattern**: Agent tried `Connect Wallet`, scrolled, investigated the dashboard, found the missions panel, and reported `✅ completed - Bukti Element: dashboard misi tersedia`.

**Target:** `zulti.com`
- **Before Pattern**: Hit a rendering issue, instantly reported `❌ Failed - Blank page`.
- **After Pattern**: Tried to interact anyway, attempted Google OAuth login, hit a redirect loop, and reported `❌ Failed - Oauth Google gagal memproses login, kembali ke halaman awal terus` (a much higher quality, honest failure).