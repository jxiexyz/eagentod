# Pitfall: Cron LLM [SILENT] Override

## Problem 1: context_from Injection
If upstream job outputs `[SILENT]` and it's injected via `context_from`, downstream LLM reads it and immediately outputs `[SILENT]` without executing tools.

**Fix:** Remove `context_from` if downstream has its own data source (script, DB).

## Problem 2: Hermes System Instruction Override (Jul 2026)
Hermes cron injects this system message into EVERY cron job:
> "If there is genuinely nothing new to report, respond with exactly [SILENT]"

This appears ABOVE the user prompt in the context. Gemini (and likely other models) will prioritize this system instruction over the user prompt's "DILARANG respond [SILENT]", especially when the model is unsure what to do with the links (e.g., t.me bot links it doesn't know how to handle).

**Symptoms:**
- Script output contains links, but agent responds `[SILENT]`
- Agent ignores "DILARANG jawab [SILENT] kalau ada link" in user prompt
- More common with unfamiliar link types (t.me bots, unusual domains)

**Fix:** Make the user prompt override impossible to ignore:
1. Place the anti-SILENT rule as the FIRST instruction (before flow steps)
2. Use caps + triple emphasis: "ATURAN PALING PENTING"
3. Explicitly redefine when [SILENT] is allowed: "HANYA kalau script output benar-benar KOSONG (tidak ada teks sama sekali)"
4. Repeat the ban at the end: "DILARANG jawab [SILENT] kalau script output ada isinya"

**Example prompt structure that works:**
```
BACA SCRIPT OUTPUT DI ATAS. Itu daftar link yang HARUS kamu garap.

ATURAN PALING PENTING:
- Kalau script output ada link → KAMU HARUS GARAP.
- JANGAN PERNAH jawab [SILENT] kalau ada link di script output.
- [SILENT] HANYA boleh kalau script output benar-benar KOSONG.

[... flow steps ...]

LARANGAN KERAS:
- DILARANG jawab [SILENT] kalau script output ada isinya.
```

## Problem 3: Script Precheck Architecture
Best pattern: use cron `script` field with a precheck script. When script stdout is empty, Hermes doesn't invoke LLM at all → 0 tokens wasted on idle cycles. When non-empty, stdout is injected as "Script Output" section in the prompt.

This sidesteps the [SILENT] problem entirely for empty-queue cases.
