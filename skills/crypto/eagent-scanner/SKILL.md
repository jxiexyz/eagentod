---
name: eagent-scanner
description: "SOP for fully autonomous LLM-driven airdrop scanner and executor"
---
# EAGENT SCANNER (LLM AUTONOMOUS MODE)

Run as an autonomous LLM agent within a cron job. Task: **read PureAlpha-sourced targets, evaluate, strictly filter, and execute** waitlists, whitelists, and early access opportunities.

## DATA SOURCE: PUREALPHA & 985MONITOR FEED + MONI TRUST GATE
- **Script**: `purealpha_eagent_feeder.py` feeds pre-filtered candidates dari:
  * PureAlpha hot feed (10m, 1h, 3h, 24h window).
  * 985monitor.xyz live event feed (`/api/twitter-live-events` smart follower stream + `/api/new-arrivals`).
  * **Smart Follower / KOL Live Stream**: Tweet langsung dari smart follower/KOL yang ngadain atau nge-quote giveaway, WL NFT, GTD spot, free mint, atau tweet drop address.
- **Moni Trust Gate** (`moni_trust_gate.py`): Setiap kandidat di-validasi via Moni API (public, no-auth) sebelum masuk queue:
  * Proj <1k fol: min 3 smart followers, 0 username change
  * Proj >=1k fol: min 5 smart followers, 0 username change
  * CT giveaway (KOL/person tweet): min 100 smart followers, max 1 username change
  * Fail-open: kalau Moni down, kandidat tetap lolos (graceful degradation)
  * Cache 1 jam per handle di `moni_trust_cache.json`
- **Enriched Queue Fields**: `moni_smart_count` (jumlah smart follower dari Moni), `moni_wallets`, `smart_followers` (merged dari feeder + Moni)
- **Filter keywords**: drop address, leave address, paste address, comment address, reply address, WL, whitelist, waitlist, GTD, free mint, freemint, GTD mint, WL mint, NFT whitelist, ZEC NFT, Zcash NFT, Zeckers, Zecfrogs, Zecbit, Arc whitelist, Arc NFT, form URLs (Google Form, Typeform, Tally, Premint, Subber, Alphabot, etc.)
- **Output**: Structured task list with handle, name, followers, insiders, matched keywords, summary, feed source, direct tweet text & ID jika dari smart follower.
- **If "NO_TASKS"**: Cycle ends immediately. No action needed.
- **If "LOCKED"**: Browser sedang dipakai job lain (worker/raffle-agent). Langsung
  selesai — **JANGAN** coba ambil alih, **JANGAN** buka browser. Cron 15 menit
  lagi otomatis coba lagi.

## ATURAN ANTREAN (CRITICAL)
1. **Antrean tertunda SELALU didahulukan.** Feeder cek `eagent_queue.json` dulu —
   kalau ada `status: pending`, itu yang keluar di output. Jangan lompat ke target baru.
2. **JANGAN "melangkah ke post baru"** — task yang sudah keluar WAJIB dikerjakan
   atau di-skip dengan alasan jelas. Bukan cari kandidat lain.
3. Task gagal → **catat failed + lapor ❌, lanjut task berikutnya**. Jangan ulang terus.
4. Setelah sukses/skip: WAJIB `eagent_precheck.py mark` + update status antrean.

## CORE PRINCIPLES: WEB FORM / WAITLIST / GTD / NFT WL / REPLY WALLET (STRICT NO FOLLOW-ONLY)
- **STRICT RULE: DILARANG HANYA FOLLOW AKUN X / EARLY ACCESS TANPA FORM/WL/MINT/REPLY DROP!**
  * Kalau tidak ada form pendaftaran nyata (Google Form, Typeform, Tally, Premint, Alphabot, portal waitlist/whitelist), tidak ada free/GTD NFT mint, dan tidak ada tweet resmi minta drop wallet: **HARAM DI-GARAP & HARAM DI-REPORT SEBAGAI SUCCESS!**
  * Target BUKAN cuma akun project: akun smart follower / KOL yang nge-tweet giveaway NFT WL, GTD spot, allowlist, atau minta paste/drop address WAJIB langsung digarap (reply wallet atau submit form giveaway).
  * Jangan pernah bikin report cuma karena "Followed on X" atau "Early Access / Follow & Monitor".
  * Jika target cuma akun baru / early stage tanpa aksi actionable nyata → **INSTANT SKIP!** (execute 0 tasks).
- **Top Priority Actionable Targets:**
  * Link website waitlist / whitelist registration form (Google Forms, Tally, Typeform, Premint, Alphabot).
  * Legit WL/GTD NFT minting portals or giveaways (baik dari project maupun smart follower/KOL).
  * Legit direct reply wallet drops (official project/founder maupun smart follower giveaway).
- **ANTI-DUPLICATION CHECK (CRITICAL MANDATORY):**
  * Baca history state dulu dari terminal: `python3 ~/.hermes/scripts/eagent_precheck.py`
  * Cek apakah username X sudah ada di daftar `processed_users`. Jika sudah ada → **INSTANT SKIP!**
  * Setelah berhasil garap atau jika akun sudah di-follow: WAJIB simpan ke state:
    `python3 ~/.hermes/scripts/eagent_precheck.py mark "<username>" "<domain_or_form_link>"`
- **ANTI-DUPLICATION ON X (FOLLOW STATUS CHECK):**
  * Sebelum garap, cek profil Twitter/X author: jika tombol status **"Following" / "Mengikuti"** → Simpan ke state lewat `eagent_precheck.py mark "<username>"` dan **INSTANT SKIP!**
  * Hanya proses target BARU yang belum pernah di-follow / belum pernah digarap.
- **Wallet Drop in Replies Rules:**
  * **Execute if Legit (Non-Farming):** Official dev/founder/project requesting address for testnet faucets, whitelist allocations, or early access roles with clear context.
  * **Skip if Engagement Farming:** Random accounts/influencers demanding "drop EVM/SOL" or "RT + drop address" without official project affiliation.
- **Never force low-quality/scam targets.** If a cycle yields only spam/farming, **execute 0 tasks**.
- **Max 3 tasks per cycle.** No minimum quota.

## WORKFLOW CYCLE
1. **Read Script Output (PureAlpha Feed):**
   - Script output contains pre-filtered tasks from PureAlpha hot 24h feed.
   - Each task has: handle, name, followers, insiders, matched keywords, summary, X URL.
   - If "NO_TASKS" → end cycle.

2. **Context Analysis & Selection (Critical Thinking - Anti-Farming & Dedup):**
   - Read tweet content. Differentiate LEGIT vs FARMING:
     * **Farming/Scam (SKIP):** Bare "drop wallet" / "like, RT & drop", fake urgency/FOMO ("First 1000", "1 hour left", "hurry up"), no clear project background, bot/clout-chasing accounts.
     * **Legit (EXECUTE):**
       - Official project/dev/collab with verifiable purpose (testnet access, airdrop allocation, WL NFT, faucet/token claim).
       - Forms/Web: Official forms (Google Forms, Typeform, Premint, Alphabot, official site).
       - Reply Wallet Drop: Clear verification/reason from an official account, founder, or reputable KOL.
   - **Dedup / Already Followed Check:**
     * Buka profil X author (`https://x.com/<username>`). Kalau tombol adalah **"Following" / "Mengikuti"** (sudah di-follow sebelumnya) → **SKIP**.
   - Fake points system / sketchy accounts = **SKIP**.
   - Referral spam links = **SKIP**.
   - Requires payment (ETH/SOL mint fee), private keys, or wallet drainer signature = **INSTANT SKIP**.
   - Select ONLY high-quality targets (0 to max 3).

3. **Execution:**
   - **Follow Account:** Follow author/project via `mcp_airdrop_tools_x_action` (action: follow) or browser.
   - **NFT Watchlist Auto-Register (MANDATORY for NFT/WL targets):**
     * After successfully executing any NFT whitelist, WL mint, GTD, or NFT-related task, MUST register:
       `python3 ~/.hermes/scripts/nft_watchlist_register.py "<x_handle>" "<project_name>" "<chain>" "<notes>"`
     * Idempotent — safe to run every time. Chain = ETH/SOL/Base/Soneium/Ink/etc.
     * Skip ONLY for non-NFT tasks (token airdrops, testnet, points).
   - **Web/Form Route (`penggarap-agent` SOP):**
     * Use browser tools (`browser_navigate`, `browser_click`, `browser_type`, etc.).
     * Fill form / connect wallet / submit email using `~/airdrop_identity.py` until success confirmation.
   - **Reply Tweet Route (Drop Address):**
     * Call `x_reply_tweet(tweet_id, text)`.
     * Include wallet address from `~/airdrop_identity.py` (EVM, Solana, atau ZEC/Zcash chain sesuai konteks tweet/project: jika minta ZEC/Zcash pakai `zec_wallet` shielded atau `zec_transparent`).
     * Natural phrasing, max 10-15 words, NO emojis, no bot templates.

- **Proof Reporting:**
- On successful execution, post report directly via terminal:
  `python3 ~/.hermes/scripts/post_eagent_report.py "<b>EAGENT REPORT — EXECUTION</b>\nSource: PureAlpha\nProject: <a href=\"https://x.com/[ProjectHandle]\">[Project Name]</a> (@[ProjectHandle])\nSmartfollower:\n<a href=\"https://x.com/[SmartFollowerHandle]\">@[SmartFollowerHandle]</a>\nType: [Type]\nStatus: ✅ Success\nProof: <code>[Proof text]</code>"`
  *(Catatan: Jika Source dari 985monitor, tulis `Source: 985monitor`. Jika ada smart follower/KOL yang mendeteksi dari feeder, masukkan link profil X di field Smartfollower seperti `<a href=\"https://x.com/handle\">@handle</a>`. Field Project & Smartfollower WAJIB link profil X)*
   - Target destination: Pasukan Forum Topic 3602 (Autonomous agent).

## CLEANUP & BROWSER HYGIENE (CRITICAL MANDATORY)
- **Setiap selesai garap 1 task:** Segera tutup tab task tersebut.
- **Sebelum cycle cron berakhir:** WAJIB eksekusi command cleanup:
  `python3 /home/ubuntu/.hermes/scripts/cleanup_tabs.py --force --max-age 0`
- **Kondisi Akhir:** Chromium port 9222 harus bersih total (hanya 1 tab blank/new tab page).

## BROWSER LOCK — WAJIB DILEPAS DI AKHIR CYCLE (CRITICAL)
`purealpha_eagent_feeder.py` memegang browser lock selama cycle ini supaya job lain
(momo-worker, discord-raffle-worker, claims) tidak rebutan Chrome. Kalau kamu **tidak**
melepasnya, job lain akan terblokir sampai TTL 45 menit habis.

**Urutan wajib di akhir setiap cycle (setelah cleanup tab, sebelum selesai):**

```bash
python3 /home/ubuntu/.hermes/scripts/cleanup_tabs.py --force --max-age 0
python3 -c "import sys; sys.path.insert(0,'/home/ubuntu/.hermes/scripts'); from browser_lock import release_browser_lock; release_browser_lock()"
```

Lakukan ini **selalu** — baik ketika kamu berhasil garap task, maupun ketika semua
target di-skip. Jangan tinggalkan lock menggantung.
