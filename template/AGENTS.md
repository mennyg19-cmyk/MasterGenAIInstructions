# Agent Instructions

Rules for ALL agents working in this repo (Cursor, Claude Code, Codex, etc.).

**The full rulebook lives in `.cursor/rules/*.mdc` -- plain markdown files any agent can read.** This file is only a router plus the absolutes. When a row below matches your task, READ THAT FILE before acting -- never work from memory or from this summary.

## Read-Before-Acting Index

| When | Read |
|---|---|
| Any session, before any edit | `.cursor/rules/workflow.mdc` (orientation, execution discipline, expectation files) |
| User says "rebuild" / "redesign" / "hotfix" / "cleanup" / "run autonomously" / "hand off" | the matching `*-protocol.mdc` / `autonomous-mode.mdc` / `session-handoff.mdc` (exact vocabulary: `vocabulary.mdc`) |
| Writing or changing code | `.cursor/rules/clean-code.mdc` + `.cursor/rules/code-walkthrough.mdc` |
| Committing, pushing, branching | `.cursor/rules/git-discipline.mdc` |
| Anything that deploys (or after any push) | `.cursor/rules/deploy-awareness.mdc` |
| Spawning ANY subagent | `.cursor/rules/subagents.mdc` |
| Finishing a phase / reviewing / merging to production | `.cursor/rules/review-protocol.mdc` |
| Writing tests | `.cursor/rules/testing-protocol.mdc` |

## The Absolutes (full detail lives in the files above)

- Plain English everywhere; audience is a self-taught programmer who hates jargon.
- Orient before editing: HANDOFF.md (if present) → README.md → this file → DECISION-LOG.md (recent entries).
- Verify in the running app -- never declare done from code alone; an empty 200 is not working.
- Before declaring done: re-read every todo/checklist item and confirm each is complete. Never from memory.
- Never work directly on the production branch; review loop is mandatory before production merges.
- After every push: verify triggered builds are green ON THE PLATFORM. "Should pass" is banned.
- Never `prisma db push` / `--accept-data-loss` in build scripts.
- Never commit secrets; `.env*` gitignored; `.env.example` placeholders.
- Subagents: `model` set explicitly, different families per job, documents passed as file paths with a read-in-full order and proof-of-read, replies are short summaries.
- Never silently choose business logic -- log it in DECISION-LOG.md.
