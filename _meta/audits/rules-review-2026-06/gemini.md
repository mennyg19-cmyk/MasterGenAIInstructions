Model: gemini-3.1-pro

# MasterGenAIInstructions Rules Audit — 2026-06-16

Lens: workflow UX and developer experience for vibe-coding.

> Recovered from subagent transcript (Ask/readonly mode blocked file write). Expanded from final summary.

---

## 1. Proof-of-read

Parsed MasterGenAIInstructions end-to-end: README stack, PHILOSOPHY layers, USER-RULE-PREFERENCES, all 17 `.mdc` files, AGENTS.md index.

**Focus:** Where agents still confuse a self-taught developer, missing vocabulary triggers, onboarding gaps, Cursor-native features not wired into vocabulary.

**Strengths:** Clear command vocabulary (`rebuild`, `hand off`, `ponytail-review`), HANDOFF + run-state resume, plain-English tone, tiered verification.

**UX gaps:** No rule for visual artifacts (canvases, tables users can't read in chat), no explicit "stuck loop" escape hatch, MCP/skills not indexed in vocabulary, large diffs not guided toward split PRs, verification skill not triggered by natural phrases.

---

## 2. Top 5 new rule ideas

1. **`canvas.mdc` or vocabulary trigger → canvas skill (on-demand)**  
   When output is analytical (audits, billing, architecture reviews, data tables): use Cursor Canvas instead of huge markdown in chat. Saves context and matches how Menny reads results.

2. **`stuck.mdc` bullets in `workflow.mdc` (~6 lines, Tier 1)**  
   If the same error repeats 3× or the agent is circling: stop, summarize what was tried, list 2 hypotheses, ask Menny OR switch approach (smaller scope, read-only explore subagent). Prevents death spirals.

3. **MCP / skills flight check in `vocabulary.mdc`**  
   Triggers: `"use codegraph"`, `"run bugbot"`, `"verify end to end"`, `"split into PRs"`, `"canvas"` → which skill/protocol to load. Agents forget installed MCP/skills without a router row.

4. **PR split guidance (`vocabulary.mdc` + pointer to split-to-prs skill)**  
   When diff > N files or user says "too big to review": load split-to-prs skill; don't dump one giant PR. Improves reviewability without new always-on file.

5. **E2E verify trigger in `deploy-awareness.mdc` / vocabulary**  
   Natural phrases: "why isn't this working", "it's broken in prod" → verification skill checklist before more code changes.

---

## 3. Top 5 repos/skills

| Name | What it does | Tier | Fit |
|---|---|---|---|
| **Cursor Canvas skill** | Rich layout for analytical deliverables | Tier 1 — vocabulary trigger | 5 |
| **split-to-prs skill** | Split branches into reviewable PRs | Tier 1 — vocabulary row | 4 |
| **Cursor Loop skill** | Recurring /loop prompts | Tier 1 — only if you use loops | 3 |
| **Vercel verification skill** | Browser → API → data → response | Tier 1 bullets in deploy-awareness | 5 |
| **Bugbot subagent** | Automated diff review | Tier 1 — vocabulary + review-protocol pointer | 4 |

---

## 4. Top 3 avoid

1. **Heavy agent memory DBs** (persistent preference stores) — CHI research links to sycophancy drift; you already use README § Rule Preferences.

2. **Formal ADR wikis** (Evan's genAITemplate style) — DECISION-LOG + HANDOFF are enough; ADRs add ceremony.

3. **Auto-formatters that fight the IDE** in rules — let Prettier/ESLint config be source of truth; don't duplicate in `.mdc`.

---

## 5. Verdict

Rule stack is strong for process. Next UX leap: **wire Cursor-native skills into vocabulary** (canvas, verification, bugbot, split PRs) and add a **stuck-loop escape** in workflow. All on-demand or Tier 1 bullets — zero new always-on files.
