# 9router Model Benchmark — July 2026

**Tested via `http://localhost:20128/v1`** (proxy key `sk-d5d...b866`)

## Test prompt
> "On waitlist page with email form, first action? 5 words max."

## Results

| Model | Reasoning tok | Content | Verdict |
|-------|---------------|---------|---------|
| `gc/gemini-2.5-flash-lite` | 0 | 20+ kata, action-first | ✅ **EXECUTION** |
| `gc/gemini-3.1-flash-lite-preview` | 0 | 35 kata, slight research tendency | ⚠️ Edge case |
| `gc/gemini-2.5-flash` | 24 | 1-2 kata ("Form validation") | ❌ Too brief |
| `gc/gemini-2.5-pro` | 25-478 | 1 kata ("Net"), broken format | ❌ Reasoning monster |
| `ag/gemini-3-flash-agent` | 26 | Empty content | ❌ |
| `ag/gemini-pro-agent` | 27 | Empty content | ❌ |
| `ag/gemini-3.5-flash-low` | 27 | Empty content | ❌ |
| `ag/gemini-3.5-flash-extra-low` | 27 | Empty content | ❌ |
| `ag/gpt-oss-120b-medium` | 30 | Empty content, timeout 30s | ❌ |
| `ag/claude-sonnet-4-6` | - | Timeout | ❌ |

## Key Finding

**All Gemini Agent models (`ag/*-agent`) produce empty content** on 9router. They burn tokens on reasoning (26-30 tok) but output nothing. `gc/gemini-2.5-pro` has extreme reasoning imbalance (478 tok reasoning → 1 word output).

**Only `gc/gemini-2.5-flash-lite` is viable** for execution tasks. Zero reasoning tokens, action-first output, 20-50 words per turn. Use for: fill form, click buttons, navigate, submit.

**Avoid**: `ag/gemini-pro-agent`, `ag/gemini-3-flash-agent`, `gc/gemini-2.5-pro`, `gc/gemini-2.5-flash`.