# Agent Instructions

Rules for ALL agents (Cursor, Claude Code, Codex, etc.). Full rulebook: `.cursor/rules/*.mdc`.

## How the rules stack

1. **Ponytail (always on, full)** -- `ponytail.mdc`: ladder, anti-bloat, terse routine chat, **anti-slop always on** (no CLI).
2. **CodeGraph (always on when indexed)** -- `codegraph.mdc`: deterministic structural index via MCP **or CLI**; hybrid with Read/grep.
3. **Discipline** -- `workflow.mdc`, `clean-code.mdc`, `git-discipline.mdc`, `vocabulary.mdc` (+ `deploy-awareness.mdc` auto-attached on deploy/env/workflow files).
4. **Protocols (on demand)** -- rebuild, redesign, review, grill, plan-review, testing, autonomous, subagents, interface-kit, prose-deslop, context-canary.
5. **README § Rule Preferences** -- standing choices when rules disagree.

## Read-Before-Acting Index

| When | Read |
|---|---|
| Before any edit | `workflow.mdc` + `ponytail.mdc` + `codegraph.mdc` + `clean-code.mdc` |
| Structural code questions | `codegraph.mdc` (MCP or CLI before grep-for-symbol) |
| Rebuild / redesign / hotfix / cleanup / autonomous / hand off | matching `*-protocol.mdc` |
| Grill / stress-test a plan | `grill-protocol.mdc` |
| Senior review of a plan | `plan-review.mdc` |
| Context rot / long session | `context-canary.mdc` (on demand) |
| UI implementation (direction chosen) | `interface-kit.mdc` |
| Publishable long-form prose | `prose-deslop.mdc` |
| Commits / deploys | `git-discipline.mdc` + `deploy-awareness.mdc` |
| Subagents | `subagents.mdc` (graph-backbone + MCP-if-available pattern) |
| Phase review / production merge | `review-protocol.mdc` |
| Tests | `testing-protocol.mdc` |
| Rule conflict | README § Rule Preferences + `ponytail.mdc` |

## CodeGraph essentials

- **Deterministic:** same query + index = same output for any model. Models differ in *interpretation*, not graph facts.
- **Hybrid:** MCP `codegraph_*` or CLI (`codegraph explore`, `codegraph query`, …) for structure; Read/grep for literals. Run `codegraph init` if `.codegraph/` missing.
- **No MCP?** CLI exposes the same graph — do not fall back to grep when CLI works.
- **Rebuild Phase 0:** parent graph-backbone → multi-model auditors (MCP or CLI; parent fills gaps).
- **`codegraph_impact`** before refactor/rename/delete.

## Absolutes

- Orient: HANDOFF → run-state (if present) → README (Rule Preferences) → this file → DECISION-LOG (recent). **`codegraph status` before structural work** — init if missing.
- **No structural Grep:** when index is healthy, Grep/SemanticSearch for symbols, callers, or layout is forbidden (`codegraph.mdc`).
- Gate discipline + command output discipline (`workflow.mdc`); ponytail full + anti-slop always on; tiered verification; production review loop; platform green after push.
- **PowerShell:** no inline `$` — script file in `.scratch/` + `-File` (`workflow.mdc`).
- Subagents: explicit model, paths not pastes, proof-of-read, `codegraph status` first, terse replies.
