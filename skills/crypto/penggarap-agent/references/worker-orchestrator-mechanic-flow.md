# Worker Orchestrator & Mechanic Flow

When the Worker Agent (ag/gemini-3.5-flash-low) encounters a roadblock or hallucinated a success, the Orchestrator will automatically summon the Mechanic Agent (ag/gemini-pro-agent) to write a bypass tool.

## Rules for the Worker
1. **Never Hallucinate Success.** You must output EXACTLY the verification string.
2. Example: `VERIFICATION: 0xYourTxHash` or `VERIFICATION: https://success.url`
3. If you do not provide this, you fail the attempt and the Mechanic is called.

## Rules for the Mechanic
1. You write generic bypass functions in `/home/ubuntu/.hermes/scripts/penggarap_tools.py`.
2. Do not hardcode URLs or specific selectors. Use parameters like `page`, `selector`, `wait_time`.
3. You MUST update this skill (`penggarap-agent`) via `skill_manage(action='patch')` to document your new tool so the Worker knows how to use it next time.

## Script Location
The Orchestrator script is located at:
`/home/ubuntu/.hermes/scripts/orchestrator.py`

Run it with:
`python3 /home/ubuntu/.hermes/scripts/orchestrator.py "Task description"`