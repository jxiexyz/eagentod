# CDP Tab Cleanup — Mandatory Post-Task Flow

## Why This Exists
Worker agent (momo-worker-agent cron) was leaving dead tabs open after each garapan. 3 tabs for Spicenet, KindWorld, Claudinals sat idle for hours eating RAM on a 2GB VPS. Root cause: `penggarap-agent` skill said "Cleanup after task" but had no explicit step or concrete command.

## The Fix (Updated 2026-07-12)

### SKILL.md Rule (Section I, line 21)
**MANDATORY after EVERY task: close current project tab via `browser_cdp(method='Target.closeTarget', params={targetId: '<id>'})`. NEVER leave dead tabs open — 2GB VPS, tabs eat RAM.**

### Cron Prompt (momo-worker-agent, job d10b883c00c5)
Step 5 added: "SETELAH garap SELESAI (done/failed/soip): WAJIB tutup tab project via `browser_cdp(method='Target.closeTarget', params={targetId: '<id>'})`. Jangan biarin tab idle numpuk."

## How to Close a Tab

### 1. Get tab ID
```python
browser_cdp(method='Target.getTargets')
# Look for your project's targetId in the response
```

### 2. Close it
```python
browser_cdp(method='Target.closeTarget', params={'targetId': 'ABC123...'})
```

### 3. Manual cleanup (if agent didn't)
Use `browser_cdp` directly. Example closing 3 dead tabs:
```python
ids = ['8AF373EF331A682E622C53E7E8A3FECD', 'C4260737465F2126B5FF2EC28AA86FD1', '57D2DE416BAB4581DF75E2D8150885CE']
for tid in ids:
    browser_cdp(method='Target.closeTarget', params={'targetId': tid})
```

## Pitfall
- **Agent forgets to call closeTarget**: GC agents (like gemini-2.5-flash-lite) may complete the "garap" task and report, but skip the cleanup step because it's not blocking. Having it as Step 5 in the cron prompt helps but isn't guaranteed. Manual audit via `Target.getTargets` recommended periodically.
- **iframe targets**: Don't close iframes individually — close the parent page target and iframes go with it.