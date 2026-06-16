# Menny's Rule Preferences (canonical)

Resolved 2026-06-10 (ponytail). Updated 2026-06-16 (codegraph). Copied into each project's README § Rule Preferences via template.

| Area | Choice |
|---|---|
| **Unknown conflict** | Default protocol-safe, keep building, tell user + offer to record in README § Rule Preferences |
| **Ponytail intensity** | **full** (always on every session) |
| **Anti-slop** | **Always on** (Tier 1 in `ponytail.mdc` — unslop patterns, no CLI/plugin). Chat, comments, commits, HANDOFF, DECISION-LOG. Code logic exact; precision beats voice on security/runbooks/legal |
| **CodeGraph lookup** | **Hybrid** — codegraph_* when `.codegraph/` exists; Read/grep for literals/configs; run `codegraph init` if missing (don't only ask) |
| **CodeGraph deterministic** | Same query + index = same facts any model; multi-model value is **judgment**, not re-reading files |
| **Rebuild Phase 0** | **A+B hybrid** — parent writes graph-backbone digests; 2 families/area interpret + audit; subagents use MCP if available, else parent runs queries |
| **Subagents + CodeGraph** | Subagent checks `codegraph_status`; uses MCP if yes; if no, reads parent digest + parent runs follow-up queries |
| **codegraph_impact** | Mandatory before rename/delete/signature change/refactor |
| **CodeGraph setup** | Bootstrap offers `codegraph init` when CLI present; global `codegraph install` once per machine |
| **Rebuild reference app** | Init codegraph in this repo **and** reference path when named |
| **Rebuild scope** | Ask when a feature feels speculative/bolted-on; don't auto-drop |
| **Dependencies** | Ponytail ladder — no new package unless stdlib + native + existing deps fail |
| **Testing** | Hybrid — testing-protocol floor, ponytail-shaped minimal tests |
| **Walkthrough headers** | **Off** (archived; `enable walkthroughs` to restore) |
| **Chat style** | Terse routine + full explain; **anti-slop always on** (ponytail) |
| **Reviews** | Hybrid + **strong ponytail-review** mandatory at every phase gate |
| **Complex requests** | Fix-don't-suggest — build what was asked |
| **God files** | Split on refactor or >500 lines / mixed concerns — token-aware |
| **Multi-model subagents** | Full protocol for rebuild/redesign only; single-model elsewhere unless "use more models" |
| **Verification** | Tiered — smoke for small fixes; full checklist for features/rebuilds/phases |
| **Protocol artifacts** | Ask when an artifact feels heavy; otherwise use protocol formats |
