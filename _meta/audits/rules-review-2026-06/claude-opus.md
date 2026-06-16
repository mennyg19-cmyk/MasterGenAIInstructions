# Rules Review — Architecture & Landscape Lens

Model: claude-opus-4-8-thinking-xhigh
Date: 2026-06-16

## Proof of read

- **README.md** — 17 rule files (7 always-on: vocabulary, workflow, ponytail, codegraph, git-discipline, clean-code, deploy-awareness; 10 on-demand). Layer stack diagram credits genAITemplate (foundation) → protocols → ponytail+unslop Tier 1 → codegraph → babysitter Tier 1. Bootstrap/apply/update-all + registry.json distribution.
- **PHILOSOPHY.md** — "tired of repeating myself"; 6-layer table (foundation/protocols/ponytail/codegraph/unslop/babysitter). Integration style = **Tier 1** (patterns baked into .mdc, no competing plugin/npm); codegraph the only external CLI/MCP exception. Token strategy section: ~7 always-on, walkthroughs archived, paths-not-pastes.
- **USER-RULE-PREFERENCES.md** — ~24-row canonical table (ponytail full, anti-slop always on, mandatory-stop gates, hybrid codegraph, A+B rebuild, codegraph_impact mandatory, walkthroughs off, multi-model rebuild/redesign-only).
- **RULE-CONFLICTS.md** — layer-ownership table + 10 resolved standing prefs + 9-entry open conflict matrix; explicitly "not auto-loaded" to save tokens.
- **AGENTS.md** — portable mirror: 5-step stack, Read-Before-Acting index, codegraph essentials, Absolutes (orient order, gate+command discipline, subagent rules).
- **17 .mdc** — read in full. vocabulary (command→protocol index), workflow (gate discipline + expectation files + run-state + command-output + security), ponytail (ladder + anti-slop + standing-pref table), codegraph (hybrid + A+B parent/subagent), git-discipline (owns all git, platform-green gate), clean-code (Rule of 2, naming, anti-AI-tics, one-pattern-per-concern), deploy-awareness (local+platform gates, Prisma rules, Windows BOM note), review-protocol (cadence single-source, diff-scoped phase / whole-app go-live, invariant ledger, trust-boundary security), subagents (roster + family diversity + debate-to-consensus, slugs centralized here), rebuild (Phase 0–5, sacred inventory, debate), redesign (model-competition previews), autonomous (DECISION-LOG format + rotation), testing (alongside-code, DB isolation), session-handoff, hotfix (lighter gates), cleanup, code-walkthrough (disabled).

## Top 5 rule ideas

1. **Anti-hallucination / verify-before-claim rule (biggest content gap).** The stack governs *voice* (unslop) and *code style* (clean-code anti-AI-tics) but has no rule against inventing APIs/signatures or claiming success unverified. Scattered cousins exist (workflow "verify in running app", deploy "read schema first") but no general directive. Add ~6 lines to clean-code.mdc: before calling a third-party symbol verify it exists in deps; never invent signatures (propose install instead); tool-first not memory-first; no factual claim about code/state without a cited source. Tier 1, highest ROI.
2. **Use Cursor's glob / auto-attach activation — the unused fourth gear.** The token strategy is hand-rolled (always-on vs vocabulary-triggered) while the platform's `globs:` Auto-Attach tier sits idle. deploy-awareness.mdc (73 lines, ~half template comments) loads on every message including pure-frontend edits; testing-protocol could auto-attach to test globs. Convert deploy-awareness + any stack-config rule to glob-scoped. This is the cleanest win and it *advances the stack's own stated token goal*.
3. **Collapse preference duplication (drift risk).** The same standing choices live in 4 places: README § Rule Preferences (runtime authority), USER-RULE-PREFERENCES.md, ponytail.mdc's table, RULE-CONFLICTS.md's resolved table. For the one thing that changes most, single-source-of-truth is broken. Make ponytail.mdc's table a 2-line pointer to canonical; keep one editable source.
4. **Stale-docs guard for dependencies.** clean-code/ponytail say "pin versions, ladder before adding" but never warn that training-data API knowledge is stale. One line: "check current docs (or Context7) before using a library API you haven't verified this session." Prevents deprecated-method bloat; pairs with idea #1.
5. **Plan protocols-as-Skills as the long-term shape.** The 10 on-demand protocols are textbook Agent Skills (complex reusable workflows). vocabulary.mdc + AGENTS.md hand-roll the trigger/portability that SKILL.md now standardizes cross-tool. Not urgent, but the maintainable end-state is a thin always-on core + protocols as skills, not a 17-file rule pile.

## Top 5 repos

1. **PatrickJS/awesome-cursorrules → anti-sycophancy-code-discipline.mdc** — verify-library-existence, no-invented-signatures, refuse-to-validate-without-evidence. Tier 1 fold-in for idea #1. https://github.com/PatrickJS/awesome-cursorrules/blob/main/rules/anti-sycophancy-code-discipline-cursorrules-prompt-file.mdc
2. **mingrath anti-hallucination gist** — 5 tight rules (tool-first, no chain-guessing, cite-the-source). Cleanest source text to adapt. https://gist.github.com/mingrath/7e292d9ca976f63e499db971f21b6bbe
3. **upstash/context7** — MCP install; current version-specific library docs. Direct fix for stale-API hallucination (idea #4). Near-zero setup, complements (doesn't overlap) codegraph. https://github.com/upstash/context7
4. **oraios/Serena** (~25k stars, LSP, 40+ langs) — evaluate as a codegraph *alternative*, not addition. Live symbol-level edit/refactor; deterministic like codegraph but no prebuilt index. https://github.com/oraios/Serena
5. **anthropics/skills + philipbankier/awesome-agent-skills** — reference for migrating protocols to portable SKILL.md and mapping the wider ecosystem. https://github.com/anthropics/skills · https://github.com/philipbankier/awesome-agent-skills

## Top 3 avoid

1. **Per-framework cursorrules** (Next.js/React/Django packs from awesome-cursorrules). The stack is intentionally stack-agnostic vibe-coding; these bloat always-on context and fight the ladder. Keep skipping them.
2. **spec-kit / SDD command suites** (github/spec-kit, spec-kit-command-cursor). Heavy /specify→/plan→/tasks ceremony that overlaps rebuild Phase 0–3 and would become a competing protocol stack — violates the explicit "no competing plugin stacks" rule.
3. **Wholesale skill marketplaces & runtime plugins** (skill-retrieval-mcp 89K registries, babysitter npm, unslop CLI). Discovery noise for a curated single-user system and against the Tier-1 philosophy. Also: do **not** run Serena *and* codegraph together — two code-intelligence indexes is the "two things that do the same job" clean-code violation; pick one.

## Verdict

This is a mature, unusually well-layered system: single-source ownership ("owns X" headers), explicit credits, a real conflict protocol, and disciplined Tier-1 restraint. Two architecture issues are worth fixing: it **ignores Cursor's native glob/auto-attach activation** while hand-rolling token strategy, and it **duplicates the preference table across four files**. One content gap matters — **anti-hallucination / verify-before-claim** — and it's a small Tier-1 add. Long-term, the protocol layer wants to become Skills, not more .mdc. Hold the line on framework rules and SDD suites.
