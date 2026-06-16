# Agent Instructions

Rules for ALL agents (Cursor, Claude Code, Codex, etc.). Full rulebook: `.cursor/rules/*.mdc`.

## How the rules stack

1. **Ponytail (always on, full)** -- `ponytail.mdc`: ladder, anti-bloat, terse routine chat, **anti-slop always on** (no CLI).
2. **CodeGraph (always on when MCP configured)** -- `codegraph.mdc`: deterministic structural index; hybrid with Read/grep.
3. **Discipline** -- `workflow.mdc`, `clean-code.mdc`, `git-discipline.mdc`, `deploy-awareness.mdc`, `vocabulary.mdc`.
4. **Protocols (on demand)** -- rebuild, redesign, review, testing, autonomous, subagents.
5. **README § Rule Preferences** -- standing choices when rules disagree.

## Read-Before-Acting Index

| When | Read |
|---|---|
| Before any edit | `workflow.mdc` + `ponytail.mdc` + `codegraph.mdc` + `clean-code.mdc` |
| Structural code questions | `codegraph.mdc` (codegraph_* before grep-for-symbol) |
| Rebuild / redesign / hotfix / cleanup / autonomous / hand off | matching `*-protocol.mdc` |
| Commits / deploys | `git-discipline.mdc` + `deploy-awareness.mdc` |
| Subagents | `subagents.mdc` (graph-backbone + MCP-if-available pattern) |
| Phase review / production merge | `review-protocol.mdc` |
| Tests | `testing-protocol.mdc` |
| Rule conflict | README § Rule Preferences + `ponytail.mdc` |

## CodeGraph essentials

- **Deterministic:** same query + index = same output for any model. Models differ in *interpretation*, not graph facts.
- **Hybrid:** codegraph for structure; Read/grep for literals. Run `codegraph init` if `.codegraph/` missing.
- **Rebuild Phase 0:** parent graph-backbone → multi-model auditors (try MCP; parent fills gaps).
- **`codegraph_impact`** before refactor/rename/delete.

## Absolutes

- Orient: HANDOFF → README (Rule Preferences) → this file → DECISION-LOG (recent). Init codegraph if missing.
- Ponytail full + anti-slop always on; tiered verification; production review loop; platform green after push.
- Subagents: explicit model, paths not pastes, proof-of-read, codegraph_status first, terse replies.
