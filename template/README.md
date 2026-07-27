# {{PROJECT_NAME}}

{{DESCRIPTION}}

## Directory Structure

<!-- Update this as the project grows -->

```
{{PROJECT_NAME}}/
|-- .cursor/rules/    # Agent rules (Cursor-native)
|-- .codegraph/       # CodeGraph index (local, gitignored -- run codegraph init)
|-- AGENTS.md          # Portable agent instructions
|-- DECISION-LOG.md    # Autonomous decisions + review findings
|-- TESTING-STRATEGY.md # Testing plan built alongside code
|-- HANDOFF.md         # Current state for next session
```

## Getting Started

<!-- How to set up and run the project -->

### Optional CI guardrails (language-agnostic)

This template includes `.github/workflows/agent-guardrails.yml` with:

- `gitleaks` (secrets)
- `semgrep` (static scan)
- `zizmor` (GitHub Actions workflow lint)

Keep or remove jobs based on project needs. Add your stack-specific build/test jobs separately.

## Patterns and Conventions

<!-- Document the patterns chosen for this project in the first session:
- Error handling approach:
- Data fetching pattern:
- State management:
- Styling approach:
- Test framework:
-->

## Deploy Targets

<!-- See .cursor/rules/deploy-awareness.mdc for deploy configuration -->

## Reference Apps

<!-- If this project is based on another app, document the source-of-truth split:
- UI/UX source:
- Business logic source:
- Data format source:
-->

## Rule Preferences

Menny's standing resolutions. Agents check here before re-asking.

- **Unknown conflict:** Default protocol-safe, keep building; tell user and offer to add the resolution here.
- **Ponytail intensity:** full (always on).
- **Anti-slop:** always on, baked into ponytail — no CLI; chat, comments, commits, HANDOFF, DECISION-LOG; code logic exact.
- **Gate discipline:** mandatory stop at every gate (babysitter Tier 1, rules only — no npm). `.scratch/run-state.md` for long runs.
- **Command output:** summarize long terminal output; full logs to `.scratch/last-command.log`.
- **PowerShell:** never inline `$` in agent shell — use `.scratch/agent-run.ps1` + `-File` (`workflow.mdc`).
- **CodeGraph:** Hybrid lookup; auto init/sync on bootstrap/apply/update-all. **No Grep/SemanticSearch for structure when index healthy** — MCP or CLI only; Read/grep for literals.
- **Rebuild Phase 0:** Parent graph backbone, then **Opus-exclusive** inventory (not Terra+Sonnet dual).
- **Rebuild scope:** Ask when a feature feels speculative; never auto-drop inventory IDs.
- **Dependencies:** Ponytail ladder — no new package unless stdlib + native + existing deps fail.
- **Testing:** Hybrid — testing-protocol floor, ponytail-minimal tests (no fixture forests).
- **Walkthrough headers:** Off (saves tokens). Say `enable walkthroughs` to restore archived rule.
- **Chat:** Terse routine; full explain when needed; anti-slop always (no sycophancy/stock vocab/hedging).
- **Reviews:** Routine phase = Terra + Sonnet (+ Sonnet quality). Production/go-live = Sol + Fable (+ Fable quality). Autonomous phase gates = **spawn Fable**. Trust-boundary = Sol primary. Checklist + evidence; review-admin; fix-canary. See `review-protocol.mdc`.
- **Complex requests:** Fix-don't-suggest — build what was asked.
- **Spec gate vs fix-don't-suggest:** Product ambiguity → grill wins; clear bug fix with known expected behavior → build wins. Spec gate in `workflow.mdc`.
- **God files:** Split on refactor or >500 lines / mixed concerns.
- **Multi-model subagents:** Rebuild/redesign + production-merge loops; inventory = Opus only; routine phase Everyday dual-family; else single-model unless I say "use more models".
- **Default models:** Job table in `subagents.mdc`. **UI default = Terra** (not Auto). **Grill me = Opus** (switch gate). **Autonomous = Grok build + spawn Fable review**. Redesign default = Gemini+Terra+Grok.
- **Wrong parent model:** Spawn the Job table model — **except full grill / grill me**: STOP and tell me to switch to Opus 5 (do not spawn grill).
- **Autonomous models:** Grok high implements; spawn Fable for phase review → fix.
- **Verification:** Tiered — smoke for small fixes; full checklist for features/rebuilds/phases.
- **Artifacts:** Ask when an artifact feels heavy; otherwise use protocol formats.
- **Grill:** Spec gate → mini-grill (Terra). `grill me` / full grill → Opus 5 parent required.
- **Plan review:** `senior review` / `junior to senior` on agent-written plans.
- **Canary:** on demand for long sessions (`canary` / `context canary`).
- **UI craft:** `interface-kit.mdc` after direction chosen — not during redesign model competition.
- **Prose de-slop:** long-form publishable text only (`deslop this prose`).
