# File Compressor — Agent Rules

## Token Optimization Policy

This project uses the **token-optimizer** skill. The agent MUST follow token
efficiency rules at all times when working in this codebase:

- Never paste full files when a line-range reference suffices.
- Always use diffs (not full replacements) for code edits.
- Keep responses concise — answer first, context second.
- Compact conversation history when it exceeds ~60% of the context window.
- Batch independent tool calls in parallel.
- Remove sycophantic openers, filler text, and re-summaries from all responses.

> When asked to optimize prompts, code context, or agent plans in this project,
> activate the `token-optimizer` skill for the full playbook.

