# Anti-Hallucination: False Success Reports (Jul 2026)

## The Problem
Worker agent reports ✅ success without actually completing any airdrop task. Common patterns:

### Pattern 1: Page Title as Proof
Agent opens homepage, reads page title/tagline, reports it as "Bukti Element".
- **Example:** `✅ conso.xyz: completed - Bukti Element: CONSO — Consumer Reputation Layer`
- **Reality:** Site had client-side exception. No form, no action taken.

### Pattern 2: Login ≠ Completion
Agent successfully logs in via OAuth but doesn't complete the actual task (form, waitlist, claim).
- Reports login confirmation as success proof.

### Pattern 3: Navigation ≠ Action
Agent clicks "Launch App" or navigates to a subpage, sees new content, reports it as success.
- No form submitted, no wallet connected, no claim made.

## Root Cause
1. **No vision check** — agent relied on accessibility tree text which showed page title
2. **Weak success criteria** — old SOP just said "see confirmation text" without defining what counts
3. **No before/after comparison** — agent didn't track what text was already on the page vs what appeared after action

## Fix (embedded in skill v1.3.0)
1. **Vision WAJIB** after navigate AND after action — agent must SEE the page
2. **Three-gate success check:**
   - Did you PERFORM a real action? (not just open page)
   - Did you SEE new confirmation text AFTER the action?
   - Is the confirmation text DIFFERENT from what was already on page?
3. **Explicit ban list:** page title, tagline, heading, project name are NOT valid proof
4. **Report format enforces:** "EXACT CONFIRMATION TEXT SETELAH AKSI" — forces agent to quote post-action text

## Detection Heuristics
If a success report's "Bukti Element" matches any of these, it's likely false:
- The project name or domain
- A tagline or marketing copy
- "Welcome to [Project]" that appears on first load (not after action)
- Any heading visible on the landing page before interaction
