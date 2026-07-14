# Menny's Rule Preferences (canonical)

Resolved 2026-06-10 (ponytail). Updated 2026-06-16 (codegraph, babysitter Tier 1). Updated 2026-06-17 (Julius Brussee skills Tier 1). Updated 2026-07-14 (Terra default, Spec gate, Premier-only hard gates). Copied into each project's README § Rule Preferences via template.

| Area | Choice |
|---|---|
| **Unknown conflict** | Default protocol-safe, keep building, tell user + offer to record in README § Rule Preferences |
| **Ponytail intensity** | **full** (always on every session) |
| **Anti-slop** | **Always on** (Tier 1 in `ponytail.mdc` — unslop patterns, no CLI/plugin). Chat, comments, commits, HANDOFF, DECISION-LOG. Code logic exact; precision beats voice on security/runbooks/legal |
| **Gate discipline** | **Mandatory stop** (babysitter Tier 1, rules only — no npm). No next phase/todo/spawn until gate complete. `.scratch/run-state.md` for rebuilds/autonomous |
| **Command output** | Summarize long terminal output; failures = file:line + message; huge logs → `.scratch/last-command.log` |
| **PowerShell execution** | **No inline `$`** in agent shell — write `.scratch/agent-run.ps1`, run with `-File`. Simple commands without `$` OK inline. See `workflow.mdc` |
| **CodeGraph lookup** | **Hybrid** — MCP `codegraph_*` OR CLI when `.codegraph/` exists. **Grep/SemanticSearch forbidden for structure when index healthy.** Read/grep literals only. Init/sync if missing; one attempt then fallback |
| **CodeGraph no MCP** | **Use CLI** — never grep-for-symbol because MCP missing; parent runs CLI for subagents |
| **CodeGraph deterministic** | Same query + index = same facts any model; multi-model value is **judgment**, not re-reading files |
| **Rebuild Phase 0** | **A+B hybrid** — parent writes graph-backbone digests; 2 Everyday families/area (Terra+Sonnet); escalate area to Sol+Fable if architecture-load-bearing; subagents use MCP if available, else parent runs queries |
| **Subagents + CodeGraph** | Subagent checks `codegraph status` (CLI) or `codegraph_status` (MCP); uses whichever is available; if neither, reads parent digest + parent runs follow-up queries via MCP or CLI |
| **codegraph_impact** | Mandatory before rename/delete/signature change/refactor |
| **CodeGraph setup** | `bootstrap` / `apply` / `update-all` auto-run MCP install (once/machine) + `codegraph init` or `sync` (per project) when CLI is on PATH |
| **Rebuild reference app** | Init codegraph in this repo **and** reference path when named |
| **Rebuild scope** | Ask when a feature feels speculative/bolted-on; don't auto-drop |
| **Dependencies** | Ponytail ladder — no new package unless stdlib + native + existing deps fail |
| **Testing** | Hybrid — testing-protocol floor, ponytail-shaped minimal tests |
| **Walkthrough headers** | **Off** (archived; `enable walkthroughs` to restore) |
| **Chat style** | Terse routine + full explain; **anti-slop always on** (ponytail) |
| **Reviews** | Routine phase: Terra Loop A + Sonnet Loop B + Sonnet quality. Production/go-live: Sol + Fable + Fable quality. Trust-boundary always Premier. Checklist + evidence + review-admin + fix-canary |
| **Complex requests** | Fix-don't-suggest — build what was asked |
| **Spec gate vs fix-don't-suggest** | Product ambiguity / Spec gate fail → **grill wins** (stop, mini-grill). Clear bug fix with known expected behavior → **build wins** |
| **God files** | Split on refactor or >500 lines / mixed concerns — token-aware |
| **Multi-model subagents** | Full protocol for rebuild/redesign + production-merge loops; routine phase = Everyday dual-family; single-model elsewhere unless "use more models" |
| **Default models** | Full Job table in `subagents.mdc`. **UI default = Terra** (not Auto). Everyday build = Terra/Sonnet/Codex. Premier (Sol/Fable) only at hard gates. Redesign default = Gemini+Terra+Grok |
| **Wrong parent model** | If parent ≠ Job slug (or Auto/unknown on judgment work) → **spawn** Task with the correct model; do not self-run the protocol as a substitute |
| **Verification** | Tiered — smoke for small fixes; full checklist for features/rebuilds/phases |
| **Protocol artifacts** | Ask when an artifact feels heavy; otherwise use protocol formats |
| **Grill (planning)** | Spec gate → mini-grill. Rebuild: ask y/n before Phase 0; redesign: after brief; say **grill me** anytime (`grill-protocol.mdc`) |
| **Plan review** | **senior review** / **junior to senior** on agent-written plans (`plan-review.mdc`) — Everyday for medium; Premier for rebuild-class |
| **Context canary** | On demand — **canary** / long high-stakes sessions (`context-canary.mdc`) |
| **UI craft** | `interface-kit.mdc` after design direction chosen; not during redesign competition |
| **Prose de-slop** | Long-form publishable text — **deslop this prose** (`prose-deslop.mdc`); routine chat stays ponytail |
