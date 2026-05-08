# Multilingual Working-Language Policy

This benchmark compares prompt-language variants. It does not claim that Thai is bad for coding agents.

The sharper idea is to separate three layers:

```text
Human interface language  -> whatever the user thinks in best
Technical working layer   -> concise English by default
Final response language   -> user's language by default
```

## Universal policy

```md
# Multilingual Input Policy

The user may communicate in any language.

Use English as the default working language for technical tasks:
- task briefs
- planning
- code analysis
- TODOs
- comments
- documentation
- commit messages
- test notes

When the user's message is not in English:
1. Extract the intent, constraints, and acceptance criteria.
2. Rewrite them as a compact English working brief.
3. Use that brief for implementation.
4. Keep original-language text only when exact wording matters.

Use the user's language for the final response unless they request another language.

Do not translate user-facing copy, legal text, customer messages, or product wording unless translation is explicitly part of the task.
```

## Why this matters

For software tasks, English often aligns better with:

- code symbols
- errors
- documentation
- package names
- GitHub issues
- API references

But forcing users to write English can increase ambiguity or cognitive load. A working-language policy tries to preserve user comfort while reducing technical-context noise.

## How to interpret results

If variant C is cheaper than A without quality loss, the policy is useful.

If the difference is tiny, do not over-optimize language. Focus instead on:

- shorter prompts
- less verbose agent replies
- better context pruning
- clearer acceptance criteria
- fewer unnecessary planning loops
