Model: composer-2.5-fast

# MasterGenAIInstructions Rules Audit — 2026-06-16

Lens: token efficiency and minimalism (~7 always-on `.mdc` files).

> Recovered from subagent transcript (Ask/readonly mode blocked file write).

---

## 1. Proof-of-read

### README.md
Personal agent OS forked from Evan's genAITemplate: bootstrap/apply/update-all stamp 17 Cursor rules + AGENTS.md into projects. Layered stack (protocols → ponytail+unslop → codegraph → babysitter Tier 1). Seven always-on rules, ten on-demand; walkthroughs disabled; human conflict docs live in `_meta/` and are not auto-loaded.

### PHILOSOPHY.md
Documents why the stack exists (session corrections, not a framework) and how layers divide labor: protocols own scope/gates, ponytail owns implementation minimalism, codegraph owns structural facts, unslop/babysitter are Tier 1 bakes only. Token strategy is explicit: subagents get paths not pastes, rotate DECISION-LOG, summarize command output.

### USER-RULE-PREFERENCES.md
Canonical standing resolutions (2026-06-10 ponytail, 2026-06-16 codegraph/babysitter): full ponytail, anti-slop always on, mandatory gate stops, hybrid codegraph, A+B rebuild backbone, walkthroughs off, multi-model only on rebuild/redesign, tiered verification, fix-don't-suggest.

### RULE-CONFLICTS.md
Human playbook mirroring preferences with nine conflict matrices; most resolved. Open item #8: codegraph always-on vs no MCP (options A keep rule / B on-demand). Design intent: Tier 1 integrations only, no competing npm stacks.

### AGENTS.md
Portable 35-line index: stack order, read-before-acting table, codegraph essentials, absolutes (orient sequence, gates, subagent mechanics). Duplicates some always-on content by design for non-Cursor tools.

### Rule files (17 `.mdc`)
**Always-on (7):** vocabulary, workflow, ponytail, codegraph, git-discipline, clean-code, deploy-awareness. **On-demand (9):** review, autonomous, testing, subagents, rebuild, redesign, hotfix, cleanup, session-handoff. **Disabled (1):** code-walkthrough (`alwaysApply: false`). Strong cross-referencing; largest always-on files are workflow (~114 lines), deploy-awareness (~79), ponytail (~73), clean-code (~72), codegraph (~63).

---

## 2. Top 5 new rule ideas

1. **Edit `ponytail.mdc` — dedupe standing preferences table (lines 55–68)**  
   Replace 14-line duplicate of README § Rule Preferences with one pointer: "Canonical list: README § Rule Preferences / `_meta/USER-RULE-PREFERENCES.md`." Saves ~13 lines every session on the busiest always-on file.

2. **Edit `codegraph.mdc` — remove duplicated A+B section (lines 40–48)**  
   Parent/subagent graph pattern already lives in `subagents.mdc` and `rebuild-protocol.mdc` Phase 0. One-line cross-ref here saves ~10 always-on lines without losing behavior.

3. **Edit `vocabulary.mdc` — skill and review triggers (on-demand, ~6 lines)**  
   Add command rows: `"security review"` → trust-boundary in `review-protocol.mdc`; `"bugbot"` / `"automated code review"` → readonly Bugbot subagent per Cursor review skill; `"Vercel deploy debug"` / `"why isn't this working"` → read verification skill before guessing. Zero always-on cost.

4. **Edit `deploy-awareness.mdc` — Tier 1 verification bullets (~8 lines)**  
   Fold Vercel verification skill pattern: browser → API → data → response, infer stack from repo before acting. Cuts redeploy loops; no new file.

5. **Edit `USER-RULE-PREFERENCES.md` + one line in `codegraph.mdc` — close conflict #8**  
   Record: "Always load `codegraph.mdc`; if no MCP and no CLI after one init attempt, stop retrying — Read/grep only." Prevents token burn on impossible setup without demoting the rule to on-demand.

---

## 3. Top 5 repos/tools to fold in

| Name | URL | What it does | Tier | Fit |
|---|---|---|---|---|
| **agents.md standard** | https://agents.md | Portable AGENTS.md spec for cross-tool parity | Tier 1 — align template section order/names only | 4 |
| **Vercel verification skill** | Cursor plugin (`verification` SKILL.md) | End-to-end flow verification before "done" | Tier 1 — 8 lines in `deploy-awareness.mdc` + vocabulary trigger | 5 |
| **Cursor Bugbot subagent** | Built into Cursor (review-bugbot skill) | Diff-scoped automated review | Tier 1 — vocabulary + optional `review-protocol.mdc` pointer | 4 |
| **babysitter (hooks path)** | https://github.com/a5c-ai/babysitter | Stop hooks / run journal (full product) | Tier 2 optional — Cursor hooks on rebuild/autonomous only; keep rules-only default | 3 |
| **split-to-prs skill** | Cursor skill (`split-to-prs`) | Split large change sets into reviewable PRs | Tier 1 — one vocabulary row; load skill on demand | 3 |

Already integrated at fit 5 (no action): ponytail, unslop Tier 1, codegraph CLI/MCP, babysitter Tier 1 ideas, genAITemplate bootstrap pattern.

---

## 4. Top 3 things NOT to add

1. **Full `@a5c-ai/babysitter-sdk` npm plugin** — Duplicates mandatory-stop rules already in `workflow.mdc`; adds per-project dependency and competes with Cursor-native hooks.

2. **unslop CLI / LLM rewriter / `/unslop` command** — PHILOSOPHY explicitly rejected; adds latency, extra always-on surface, and fights the "subtract don't add" goal.

3. **Eighth always-on rule file** (e.g. standalone skills-index, walkthroughs re-enabled, SonarQube/SDL from Evan's original stack) — Breaks ~7-file budget; compliance tooling targets a different workflow than vibe-coding and costs tokens every session.

---

## 5. Overall verdict

The stack is mature and incident-driven. The main token leak is **always-on duplication**: ponytail's preferences table and codegraph's subagent section repeat content already canonical elsewhere. Trim those two files before adding anything new. Gaps are **trigger wiring** (skills, Bugbot, verification) and **conflict #8 closure** — all achievable via small edits to existing on-demand or always-on files, not new layers. Stay at seven always-on files; fold external value as Tier 1 bullets and vocabulary triggers, not npm plugins.
