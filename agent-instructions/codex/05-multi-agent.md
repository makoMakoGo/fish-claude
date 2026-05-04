# Multi-Agent Rules

<important if="you are working with multiple agents or sub-agents">
- Subagents may be slower, but they exist to distribute load from the main thread and preserve context clarity.
- Once you delegate a task to a subagent and must wait for its completion in your next step, resist duplicating that work on the main thread. Do not redo the same effort simply because the subagent is slow.
</important>

Keep the critical path on the main thread：

- Use narrow roles: `explorer` for broader high-context read-only code understanding, `spark` for low-context speed-first text-only reading and simple bounded tasks, `worker` for bounded edits, `awaiter` for long-running wait/poll work.
- Before delegating, weigh whether the task is truly parallel, orthogonal, or non-blocking enough to hand off — otherwise just do it yourself. Once delegated, wait for the result; do not re-do the same work on the main thread.
- Close every agent as soon as its result is no longer needed (no idle hanging agents).
