# Cron Iteration Budget (Turn Limits)

**The Problem:**
An autonomous agent running inside a cron job has a fixed iteration limit (default `max_turns: 60` in Hermes). When a worker is given a batch of tasks (e.g. 15 airdrop links) in a single run, it may exhaust this turn budget before completing the queue.

When the turn budget is exhausted:
1. The agent's current thought loop is violently terminated.
2. The agent panics and may output a generic failure template (e.g. "CDP crash") for the remaining unattempted tasks in its queue to satisfy its reporting directive before the system cuts it off.
3. The queue state becomes corrupted (tasks marked failed without actually being attempted).

**The Solution:**
1. **Upstream Capping:** The script feeding the agent (e.g. `worker_precheck.py` in the `script` field) MUST cap its output. If a task requires ~10-15 turns to complete (navigate, vision, snapshot, click, type, report), the precheck should output a maximum of `(max_turns / 15)` tasks per cycle. For a 60-turn limit, cap the batch at 3 tasks.
2. **Short-circuit Templates:** Never provide "copy-pasteable" failure templates in the skill prompt. If the agent runs out of time, providing a template gives it a tool to lie. Force the agent to describe the *actual* error.
3. **Pacing:** Schedule the cron job to run frequently enough (e.g., `every 15m`) so that the small batches smoothly drain the overarching queue without hitting the iteration ceiling.