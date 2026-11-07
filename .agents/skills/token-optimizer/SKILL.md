---
name: token-optimizer
description: >-
  Comprehensive guide for optimizing token usage in AI interactions. Activate
  this skill when the user asks to reduce token consumption, improve prompt
  efficiency, eliminate wasteful context, compress conversations, audit token
  usage, or write token-efficient code and prompts. Also activate when planning
  large multi-step tasks where context window management is critical.
---

# Token Optimizer

A systematic, actionable playbook for minimizing token waste and maximizing
the quality of information per token across prompts, code context, subagents,
and agent responses.

---

## 1. Core Principles

| Principle | Rule |
|-----------|------|
| **Precision over verbosity** | Every token must carry information. Remove tokens that restate, decorate, or hedge without adding meaning. |
| **Lazy loading** | Do not load context you *might* need. Load context you *will* need. |
| **Hierarchy of cost** | System prompt tokens > Conversation history tokens > Single-turn tokens. Optimize the most expensive layer first. |
| **Lossless compression** | Reduction must never sacrifice correctness, safety, or required nuance. |

---

## 2. Prompt Engineering — Eliminating Wastage

### 2.1 Anti-patterns to Eliminate

```
❌ WASTEFUL                              ✅ OPTIMIZED
─────────────────────────────────────────────────────────────
"Could you please, if you don't         "List 5 bugs in auth.py."
 mind, list maybe 5 or so bugs
 that you find in auth.py?"

"As an AI language model, I will        [omit — never self-describe]
 now proceed to analyze..."

"I hope this helps! Let me know         [omit — conversational filler]
 if you need anything else!"

"Sure! Great question! Absolutely!"     [omit — sycophantic openers]

Re-pasting the full 500-line file       Paste only the relevant function
 to ask about one function.             or line range.

Asking for JSON + explaining JSON       Just ask for JSON.
 in prose + a code example of JSON.
```

### 2.2 Prompt Structure Template (token-efficient)

```
ROLE: <one line — only if non-default role matters>
TASK: <imperative verb + object + constraint>
CONTEXT: <minimum necessary background — bullet form>
OUTPUT: <format, length, schema>
```

### 2.3 Compression Heuristics

- **Replace prose lists with bullet-delimited values**: `name, age, city` not "the name, the age, and the city of the person."
- **Use abbreviations for repeated terms** after first definition: define `ctx = context window`, then use `ctx`.
- **Omit articles and conjunctions** in structured data fields (not in prose explanations where clarity matters).
- **Prefer code over prose** for structured logic — 10 lines of code > 2 paragraphs describing the same logic.
- **Use schema references** instead of repeating field definitions: "follow schema in `types.ts`" is better than re-listing every field.

---

## 3. Code Context — What to Include vs. Exclude

### 3.1 Selection Rules

Include **only**:

```
✅ The function/class directly under discussion
✅ Its immediate dependencies (types, called functions) — signatures only
✅ Relevant config or schema excerpts (not full files)
✅ Error messages verbatim (never paraphrase)
✅ Diffs instead of full files when change is <30% of file
```

Exclude:

```
❌ License headers and boilerplate comments
❌ Unrelated functions in the same file
❌ Full file when only one section is relevant
❌ Duplicate definitions already in the conversation
❌ Generated files (lock files, build artifacts, minified JS)
❌ Binary/encoded content (base64, hex dumps) unless inspecting encoding
```

### 3.2 Reference vs. Paste Strategy

| File size | Action |
|-----------|--------|
| < 50 lines | Paste inline |
| 50–300 lines | Paste only the relevant section with line numbers |
| > 300 lines | Reference the file path + line range; read on demand |
| Generated / binary | Never paste; describe structure only |

### 3.3 Diff Format (preferred for edits)

Always provide code changes as unified diffs when modifying existing code,
not full file replacements:

```diff
--- a/auth.py
+++ b/auth.py
@@ -42,7 +42,7 @@ def login(user, pwd):
-    token = jwt.encode(payload, SECRET)
+    token = jwt.encode(payload, SECRET, algorithm="HS256")
```

---

## 4. Conversation & History Management

### 4.1 When to Summarize

Trigger a conversation summary (via `/compact`) when:
- History exceeds ~60% of the model's context window.
- The active topic has fully changed (new feature, new file domain).
- More than 10 consecutive tool-call/result pairs have accumulated.

### 4.2 Summary Format (token-efficient)

```
GOAL: <original user objective — 1 sentence>
DONE: <completed steps — bullet, past tense, no prose>
STATE: <current file/function/variable of interest>
NEXT: <immediate next action>
OPEN: <unresolved decisions or blockers>
```

### 4.3 History Pruning Rules

- Remove intermediate reasoning steps once a conclusion is reached.
- Collapse repeated tool calls with identical parameters into one representative entry.
- Replace large tool *responses* (file reads, search results) with a single-sentence summary once their content has been acted upon.

---

## 5. Subagent & Multi-Agent Token Discipline

### 5.1 Delegate Narrow Tasks

Each subagent prompt must follow the **TRIM** rule:

```
T — Task:    One concrete deliverable only.
R — Refs:    Minimal file paths or data the subagent needs.
I — Intent:  What the parent will do with the result.
M — Mode:    Output format (JSON, diff, summary, file path).
```

### 5.2 Return Contracts

Subagents must return:
- Results in the declared output format only.
- No explanatory prose unless `Mode = prose`.
- File paths instead of file contents when the parent can read the file itself.

### 5.3 Avoid Subagent Sprawl

| Situation | Action |
|-----------|--------|
| Task fits in < 20 tool calls | Do it inline; no subagent |
| Task is parallelizable AND independent | Launch subagents in parallel |
| Subagent result is not used | Kill the subagent immediately |
| Subagent context is > 50% done | Summarize before continuing |

---

## 6. Response Generation — Agent Output Discipline

Agents (including this one) must apply these rules to their own responses:

### 6.1 Response Length Calibration

| Request type | Max response length |
|--------------|---------------------|
| Yes/no question | 1–2 sentences |
| Factual lookup | 1 short paragraph or list |
| Code change | Diff or the changed function only |
| Explanation of concept | 3–5 paragraphs max |
| Design / architecture | Artifact (markdown file), not inline |
| Long analysis | Artifact with executive summary inline |

### 6.2 Forbidden Patterns in Responses

```
❌ Re-summarizing what the user just said before answering.
❌ Listing all the things you are "about to" do before doing them.
❌ Repeating the full content of an artifact you just created.
❌ Closing pleasantries ("Hope this helps!", "Feel free to ask!").
❌ Hedging every statement ("It's worth noting that...", "Generally speaking...").
❌ Explaining what a common tool/command does when the user clearly knows.
```

### 6.3 Preferred Patterns

```
✅ Answer first, context second (inverted pyramid).
✅ Use bullet/table for 3+ parallel items.
✅ Use code blocks for all commands, paths, and identifiers.
✅ Link to files instead of quoting them.
✅ State unknowns explicitly rather than hedging.
```

---

## 7. Token Audit Checklist

Run through this before submitting any long prompt or agent task:

```
[ ] Is each sentence load-bearing? (Remove decorative sentences.)
[ ] Does context include anything not referenced in the task?
[ ] Are any definitions repeated from earlier in the conversation?
[ ] Can code blocks be replaced with file path + line range references?
[ ] Are tool calls batched where possible (parallel, non-dependent)?
[ ] Is the output format specified concisely (schema / example)?
[ ] Is the expected response length appropriate for the task?
[ ] Can a subagent be avoided for tasks solvable in < 20 tool calls?
[ ] Is history ready to compact if > 60% of context window is used?
```

---

## 8. Quick Reference — Token Cost Rankings

From most to least expensive per token of utility:

```
1. System prompt           → Edit rarely; every byte costs every request.
2. Injected file content   → Use line ranges, not full files.
3. Conversation history    → Compact aggressively.
4. Tool call results       → Summarize after use.
5. Single-turn user input  → Optimize at composition time.
6. Agent response          → Self-enforce brevity rules.
```

---

## 9. Applying This Skill

When activated, do the following in order:

1. **Identify the waste layer** — which category (prompt, code context, history,
   subagent, response) is the primary source of token waste.
2. **Apply the relevant section** from this skill (§2–§6).
3. **Run the audit checklist** (§7) on the revised prompt or plan.
4. **Report savings** only if the user asked for a report; otherwise just apply
   the optimizations silently and proceed.

