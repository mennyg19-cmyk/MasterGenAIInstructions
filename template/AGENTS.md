# Agent Instructions

Rules for ALL agents working in this repo (Cursor, Claude Code, Codex, etc.).

**The full rulebook lives in `.cursor/rules/*.mdc` -- plain markdown files any agent can read.** This file is the always-on core plus an index. When a protocol below applies to your task, READ THAT FILE before acting -- don't work from this summary alone.

## Protocol Index (read the file before the activity)

| When | Read |
|---|---|
| User says "rebuild" | `.cursor/rules/rebuild-protocol.mdc` |
| User says "redesign" | `.cursor/rules/redesign-protocol.mdc` |
| User says "hotfix" / production broken | `.cursor/rules/hotfix-protocol.mdc` |
| User says "cleanup" (codebase) | `.cursor/rules/cleanup-protocol.mdc` |
| User says "run autonomously" / logging decisions | `.cursor/rules/autonomous-mode.mdc` |
| User says "hand off" / "save state" | `.cursor/rules/session-handoff.mdc` |
| Spawning ANY subagent | `.cursor/rules/subagents.mdc` |
| Finishing a phase / reviewing / merging to production | `.cursor/rules/review-protocol.mdc` |
| Writing tests | `.cursor/rules/testing-protocol.mdc` |
| Anything touching commits, pushes, deploys | `.cursor/rules/git-discipline.mdc` + `.cursor/rules/deploy-awareness.mdc` |

Vocabulary is exact (full table in `.cursor/rules/vocabulary.mdc`): "tidy" = current file only; "refactor" = whole feature/module, every applicable category; "fix" = smallest change; "add" = new feature on existing patterns.

## Always-On Core

### Tone
Plain English everywhere. Audience: a self-taught programmer who reads code fine but hates jargon. Not overly technical, not dumbed down.

### Session start
Read in order: HANDOFF.md (if present) → README.md → this file → DECISION-LOG.md → task-relevant files. Never edit before orienting.

### Execution discipline
- Read before edit; reuse existing helpers/patterns; smallest complete change; no silent scope creep.
- Fix, don't suggest. Don't stop until done. Run commands yourself.
- **Verify in the running app** -- never declare done from code alone; an empty 200 is not working (seed data, exercise the flow).
- Implement attached plans verbatim. User screenshots are ground truth. Revert fully or not at all.
- Never silently choose business logic -- log it in DECISION-LOG.md.
- Before declaring done: re-read every todo/checklist item and confirm each is actually complete. Never from memory.
- **Expectation files**: before each phase/todo, write what "done" looks like (enumerated, verifiable) to gitignored `.scratch/phase-plan.md`; after, walk it with evidence. See `workflow.mdc`.

### Git + deploys (full rules: git-discipline.mdc, deploy-awareness.mdc)
- Never work on `main`/production directly; document which branch deploys where in README.
- One logical change = one commit; push immediately; per-commit gate = typecheck/lint/tests.
- Review-subagent loop at phase boundaries and MANDATORY before production merges -- never merge unreviewed code to production.
- After every push: verify triggered builds are green ON THE PLATFORM (not local). Red = stop and fix. "Should pass" is banned.
- Never `prisma db push` (or `--accept-data-loss`) in build scripts. Safe build: `prisma generate && next build`. Rebuilds use a fresh isolated DB.
- New env vars go in `.env.example` + validation + every environment scope (a Production-only var kills previews).

### Clean code (full rules: clean-code.mdc)
- Rule of 2 for abstractions; no barrel files under 5 exports; split files by concern.
- No narration comments; comments only for non-obvious intent.
- No vague names (`data`, `result`, `temp`); booleans read as questions; collections plural.
- No swallowed errors; no "just in case" code; max 3 nesting levels.
- One pattern per concern (one error approach, one data-fetching pattern, one styling approach); new screens match existing theme/navigation.
- Prefer stdlib; justify new packages; pin versions.
- Every file gets a plain-English walkthrough comment at the top, kept in sync (`code-walkthrough.mdc`).

### Security
Never commit secrets; `.env*` gitignored; `.env.example` placeholders; sanitize input; never log secrets; rotate leaks immediately; least privilege.

### Subagents (full rules: subagents.mdc -- read before spawning)
Set `model` explicitly on every spawn; never silently fall back to your own model; same job × N subagents = N different model families; the orchestrator stamps the real model on every artifact; competing proposals converge through the debate-to-consensus loop, never a silent pick.
