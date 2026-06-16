# Agent Instructions

Rules for ALL agents (Cursor, Claude Code, Codex, etc.). Full rulebook: `.cursor/rules/*.mdc`.

## How the rules stack

1. **Ponytail (always on, full)** -- `ponytail.mdc`: ladder, anti-bloat, terse routine chat.
2. **Discipline** -- `workflow.mdc`, `clean-code.mdc`, `git-discipline.mdc`, `deploy-awareness.mdc`, `vocabulary.mdc`.
3. **Protocols (on demand)** -- rebuild, redesign, review, testing, autonomous, subagents.
4. **README § Rule Preferences** -- your standing choices when ponytail and protocols disagree.

## Read-Before-Acting Index

| When | Read |
|---|---|
| Before any edit | `workflow.mdc` + `ponytail.mdc` + `clean-code.mdc` |
| Rebuild / redesign / hotfix / cleanup / autonomous / hand off | matching `*-protocol.mdc` |
| Commits / deploys | `git-discipline.mdc` + `deploy-awareness.mdc` |
| Subagents | `subagents.mdc` (multi-model: rebuild/redesign only unless "use more models") |
| Phase review / production merge | `review-protocol.mdc` (ponytail-review + correctness loop) |
| Tests | `testing-protocol.mdc` |
| Rule conflict | README § Rule Preferences + `ponytail.mdc` |

## Menny's Rule Preferences (summary)

See README § Rule Preferences for the full list. Highlights:

- Ponytail **full**, always on. Dependencies: ponytail ladder (no new packages lightly).
- Walkthrough headers **off** (`enable walkthroughs` to restore).
- Chat: terse routine edits; full prose for explain/decisions/conflicts.
- Reviews: **mandatory ponytail-review** at every phase gate + correctness loop.
- Testing: hybrid (protocol floor, minimal tests). God files: split at >500 lines / refactor.
- Multi-model: rebuild/redesign only. Verification: tiered. Artifacts: ask when heavy.
- Unknown conflict: default protocol-safe, keep building, tell user, offer to record preference.
- Complex requests: fix-don't-suggest. Rebuild: ask before dropping speculative features.

## Absolutes

- Orient: HANDOFF → README (incl. Rule Preferences) → this file → DECISION-LOG (recent).
- Verify in running app; tiered depth per `workflow.mdc`.
- Production merge requires review loop; platform green after push.
- Never commit secrets; never `prisma db push` in build scripts.
- Subagents: explicit model, paths not pastes, proof-of-read, terse replies.
