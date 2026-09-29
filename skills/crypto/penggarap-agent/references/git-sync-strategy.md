# Git Sync Strategy (VPS to GitHub)

**CRITICAL:** For the `jxiexyz/hermesfull` repository (which stores the V2 airdrop worker architecture and skills), the **local VPS (`~/.hermes/skills/`) is ALWAYS the source of truth.**

## Rule: Never Pull/Overwrite Local
When asked to "check the GitHub repo" or "commit to the repo":
1. **NEVER run `git clone` and copy the remote contents over the local `~/.hermes/skills/` directory.** The remote GitHub repository is often a stale backup. Overwriting local skills with the remote repository will destroy the user's recent, un-pushed work.
2. **ALWAYS Push:** The direction of synchronization must always be **Local -> Remote**.
   - Review local changes.
   - Commit them.
   - Push to `origin`.

If you accidentally delete or overwrite a local skill because you assumed the GitHub repo was newer, the user will (justifiably) be extremely angry. Don't do it.

## Correct Workflow for Syncing
```bash
# Inside the local skill directory (or a temp git repo initialized from local files)
git add .
git commit -m "update: concise message"
git push origin main
```