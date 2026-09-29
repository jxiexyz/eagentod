# Worker Architecture: Standalone Script vs Hermes Cron

## Background
Airdrop automation workers historically ran as standalone Python scripts (e.g., `airdrop_worker.py`) using `playwright.async_api` and raw LLM completion calls to simulate an agent.

This architecture has proven **fundamentally flawed** and should be avoided in favor of native Hermes cron jobs equipped with browser tools.

## The Flaws of Standalone Python Scripts

1. **LLM Blindness**: Standalone scripts rely on `document.body.innerText` for context. The LLM has to parse this and output raw commands like `CLICK: Connect Wallet`. 
2. **Selector Guessing**: When the LLM issues a text command, the Python script uses a heuristic `page.click(f'button:has-text("{sel}")')` to find the target. This fails catastrophically on:
   - React portals
   - Shadow DOM elements
   - Nested iframes
   - SVG icons without text labels
   - Google Forms with obfuscated `entry.12345` IDs.
3. **Execution Loop Hangs**: Asynchronous while-loops in Python easily hang if a popup is missed, if an `evaluate()` call blocks, or if the LLM backend times out. The entire worker queue halts.

## The Hermes Native Advantage (Cron + Browser Tools)

By moving the worker into the native Hermes cron engine (`momo-worker-agent`), we unlock:

1. **True Accessibility Trees**: Instead of raw text, the agent gets `browser_snapshot()` which provides a rich accessibility tree with exact element references (`@e1`, `@e2`).
2. **Exact Targeting**: The agent executes `browser_click(ref="@e5")` which clicks the exact node ID via CDP, bypassing all the selector-guessing heuristic failures.
3. **User Preference Compliance**: The user explicitly demanded:
   > "gw mau si worker tuh gini garapnya pake browsrr click manual view biar dia bisa garap full jgn cuma nagndelin inject"
   Native browser tools fulfill this requirement perfectly by routing real CDP click/type events to the exact elements.
4. **Built-in Timeout/Safety**: Hermes handles context limits, tool timeouts, and loop detection automatically.

## Implementation Standard

Never write a standalone `while turns < MAX_TURNS: action = llm(...)` Python script for airdrop execution. 

Instead, create or update a cron job that:
1. Loads the `penggarap-agent` skill.
2. Has the `browser` and `mcp_airdrop_tools` toolsets enabled.
3. Reads the queue (e.g., `python3 get_topic31.py`).
4. Executes natively within the agent's turn loop using `browser_navigate`, `browser_snapshot`, `browser_click`, and `browser_type`.