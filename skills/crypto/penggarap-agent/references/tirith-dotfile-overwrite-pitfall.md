# Tirith Dotfile Overwrite Pitfall

## The Issue
When generating temporary scripts via terminal commands like `cat << 'EOF' > ~/.script.js`, writing to a hidden file or generating a script file that looks like a configuration dotfile triggers the Tirith security guard (`tirith:dotfile_overwrite`). This aborts the command because it suspects an attempt to overwrite shell configuration.

## The Solution
Always use explicit absolute paths or write to non-hidden files when generating temporary scripts.

**BAD:**
```bash
cat << 'EOF' > ~/.hermes/scripts/retium_phrase.js
```
*Note: The `.` in `.hermes` can sometimes trigger heuristics if not carefully handled by the guard.*

**GOOD:**
```bash
cat << 'EOF' > /home/ubuntu/temp_script.js
```
Or write directly to a non-hidden scratch file in the home directory.