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
- **CodeGraph:** Hybrid lookup; run `codegraph init` if missing; parent graph-backbone + subagents use MCP if available else parent fills gaps. Rebuild: init reference app path too. `codegraph_impact` mandatory before refactor/rename/delete.
- **Rebuild Phase 0:** A+B hybrid -- parent deterministic graph backbone, then 2 model families per area for judgment (not six blind file walks).
- **Rebuild scope:** Ask when a feature feels speculative; never auto-drop inventory IDs.
- **Dependencies:** Ponytail ladder — no new package unless stdlib + native + existing deps fail.
- **Testing:** Hybrid — testing-protocol floor, ponytail-minimal tests (no fixture forests).
- **Walkthrough headers:** Off (saves tokens). Say `enable walkthroughs` to restore archived rule.
- **Chat:** Terse for routine edits; full prose for explain / decisions / conflicts.
- **Reviews:** Mandatory ponytail-review at every phase gate + correctness/security loop.
- **Complex requests:** Fix-don't-suggest — build what was asked.
- **God files:** Split on refactor or >500 lines / mixed concerns.
- **Multi-model subagents:** Rebuild/redesign only unless I say "use more models".
- **Verification:** Tiered — smoke for small fixes; full checklist for features/rebuilds/phases.
- **Artifacts:** Ask when an artifact feels heavy; otherwise use protocol formats.

<!-- Add new resolutions below after conflicts: -->
