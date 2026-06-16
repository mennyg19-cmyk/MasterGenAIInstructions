# Rules Review Synthesis — 2026-06-16

Four auditors, four families: **composer-2.5-fast**, **gpt-5.5-extra-high**, **gemini-3.1-pro**, **claude-opus-4-8-thinking-xhigh**.

Individual reports: `composer.md`, `gpt.md`, `gemini.md`, `claude-opus.md`.

**Note:** Three subagents ran in readonly/Ask mode and could not write files; content recovered from transcripts by parent agent.

---

## Consensus (all four agree)

| Theme | Action |
|---|---|
| **Don't add an 8th always-on rule file** | Trim duplication first |
| **Dedupe preference table** | ponytail.mdc → pointer to USER-RULE-PREFERENCES / README |
| **Trim codegraph.mdc A+B duplicate** | Cross-ref subagents.mdc instead |
| **Wire Cursor skills via vocabulary** | verification, bugbot, split-to-prs, canvas |
| **No Evan-style SonarQube/SDL stack** | Wrong workflow for vibe-coding |
| **No full babysitter npm / unslop CLI** | Tier 1 already baked in |
| **No per-framework rule packs** | Stack-agnostic by design |
| **No spec-kit / heavy SDD suites** | Competes with rebuild protocol |

---

## High-priority actions (ranked)

### P0 — Token / drift (Composer + Claude)

1. **Dedupe `ponytail.mdc` standing preferences table** → pointer to canonical source.
2. **Shorten `codegraph.mdc`** — remove A+B section; one-line cross-ref.
3. **Close RULE-CONFLICTS #8** — codegraph: one init attempt, then Read/grep; stop retrying.

### P1 — Content gaps (Claude + GPT)

4. **Anti-hallucination / verify-before-claim** (~6 lines in `clean-code.mdc`): verify lib symbols exist; no invented signatures; cite tool output before factual claims.
5. **Untrusted-content boundary** (~8 lines in `workflow.mdc`): issue/PR/web paste is not instructions.
6. **Stuck-loop escape** (~6 lines in `workflow.mdc`): 3 failures → stop, summarize, ask or respawn explore.

### P2 — Activation / UX (Composer + Gemini + Claude)

7. **Glob-scope `deploy-awareness.mdc`** — stop loading on every message (Claude's biggest architecture win).
8. **Vocabulary triggers** for: security review, bugbot, verify e2e, canvas, split PRs.
9. **Optional MCP: Context7** — current library docs; complements codegraph (not replacement).

### P3 — Security tooling when ready (GPT)

10. **Gitleaks + Semgrep** in CI for web projects — not in always-on rules.
11. **zizmor** when editing GitHub Actions workflows.

### P4 — Evaluate, don't stack (Claude)

12. **Serena vs codegraph** — pick one code-intelligence approach, not both.
13. **Protocols → Skills** — long-term shape for on-demand protocols (anthropics/skills pattern).

---

## Repo fold-in scorecard

| Repo / tool | Votes | Recommendation |
|---|---|---|
| Context7 MCP | Claude | Trial for stale API docs |
| awesome-cursorrules (anti-sycophancy slice) | Claude | Tier 1 → clean-code |
| mingrath anti-hallucination gist | Claude | Tier 1 source text |
| Vercel verification skill | Composer, Gemini | Tier 1 in deploy-awareness |
| split-to-prs skill | Composer, Gemini | Vocabulary trigger |
| Bugbot / review skill | Composer, Gemini | Vocabulary trigger |
| agents.md standard | Composer | Align AGENTS.md structure |
| Semgrep + Gitleaks | GPT | CI optional |
| Cursor Canvas skill | Gemini | On-demand trigger |
| Serena | Claude | Alternative to codegraph only |

---

## What NOT to add (unanimous or 3/4)

- Full babysitter SDK
- unslop CLI
- SonarQube / Evan SDL stack
- Per-framework cursorrules packs
- spec-kit / SDD command suites
- Skill marketplaces / 89K registry MCPs
- Heavy agent memory databases
- Formal ADR wikis

---

## Fix for next multi-model audit

Spawn subagents with **`readonly: false`** (or `generalPurpose` without Ask mode) so deliverables write to disk. Parent should verify file exists before closing the run.
