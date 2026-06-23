# MasterGenAIInstructions

Personal agent operating system for AI-assisted development. Bootstrap new projects with Cursor rules, portable AGENTS.md, and workflow protocols pre-loaded so agents work your way from commit zero.

**Lineage:** Forked and rebuilt from [Evan Pokroy's genAITemplate](https://github.com/EvanPokroy/genAITemplate) (Menny's fork: [mennyg19-cmyk/genAITemplate](https://github.com/mennyg19-cmyk/genAITemplate)) into this Cursor-native system.

**Philosophy and credits:** [_meta/PHILOSOPHY.md](_meta/PHILOSOPHY.md) — why this exists, how the layers fit together, and who we borrowed from.

## What's In Here

```
MasterGenAIInstructions/
|-- bootstrap.ps1        # PowerShell: create a new project
|-- bootstrap.sh         # Bash: create a new project
|-- manager.pyw          # Double-click GUI manager (Python/tkinter)
|-- apply.ps1            # PowerShell: apply rules to an existing project
|-- apply.sh             # Bash: apply rules to an existing project
|-- update-all.ps1       # PowerShell: push rule updates to all registered projects
|-- registry.json        # List of projects using these rules
|-- template/            # Everything below gets copied into new projects
|   |-- .cursor/rules/   # 22 Cursor rule files (6 always-on + 1 auto-attach)
|   |-- AGENTS.md        # Portable playbook for non-Cursor environments
|   |-- DECISION-LOG.md  # Template for autonomous decisions
|   |-- TESTING-STRATEGY.md
|   |-- HANDOFF.md
|   |-- .gitignore
|   |-- README.md        # Project README template
|   |-- .github/workflows/
|       |-- agent-guardrails.yml  # Optional CI: gitleaks + semgrep + zizmor
|-- _meta/
    |-- PHILOSOPHY.md    # Why this exists, credits, how layers fit
    |-- USER-RULE-PREFERENCES.md  # Canonical standing conflict resolutions
    |-- RULE-CONFLICTS.md         # Expanded conflict playbook (not auto-loaded)
```

## The rule stack (credits & what each layer does)

Rules are **layered**. Protocols own scope and quality gates; integrations make daily work leaner without dropping features or skipping reviews.

```
┌──────────────────────────────────────────────────────────┐
│  README § Rule Preferences  — your standing choices      │
├──────────────────────────────────────────────────────────┤
│  Protocols (on demand)  — rebuild, review, subagents…    │  ← Menny (evolved from Evan's template)
├──────────────────────────────────────────────────────────┤
│  Ponytail  — how to implement (ladder, YAGNI, brevity)   │  ← DietrichGebert/ponytail
│  + Unslop Tier 1  — anti-slop voice in ponytail.mdc      │  ← MohamedAbdallah-14/unslop
├──────────────────────────────────────────────────────────┤
│  CodeGraph  — structural navigation (MCP + CLI)          │  ← colbymchenry/codegraph
├──────────────────────────────────────────────────────────┤
│  Babysitter Tier 1  — gates, cmd output, run-state       │  ← a5c-ai/babysitter (rules only)
├──────────────────────────────────────────────────────────┤
│  Julius Brussee skills (Tier 1)  — grill, plan-review, UI craft   │  ← grill-me, junior-to-senior, interface-kit, …
├──────────────────────────────────────────────────────────┤
│  CI guardrails (optional)  — gitleaks · semgrep · zizmor │  ← language-agnostic workflow
├──────────────────────────────────────────────────────────┤
│  genAITemplate  — bootstrap + “one place for agent rules”│  ← EvanPokroy (foundation)
└──────────────────────────────────────────────────────────┘
```

### [Evan Pokroy / genAITemplate](https://github.com/EvanPokroy/genAITemplate) — foundation

| | |
|---|---|
| **Original repo** | [EvanPokroy/genAITemplate](https://github.com/EvanPokroy/genAITemplate) |
| **Menny's fork** | [mennyg19-cmyk/genAITemplate](https://github.com/mennyg19-cmyk/genAITemplate) |
| **What Evan built** | A lightweight **meta-prompt / agent project template**: bash bootstrap (`deploy-new-project.sh`), a documentation operating system (`MASTER-INSTRUCTIONS.md`, `_meta/PRINCIPLES.md`, trace journals, ADR wiki), and the core idea that new projects should ship with agent instructions pre-loaded — not pasted from chat every session. |
| **What carries forward here** | Bootstrap-and-apply workflow (`bootstrap.ps1`, `apply.ps1`, `update-all.ps1`, `registry.json`), “stamp rules into every repo,” portable agent docs (`AGENTS.md`), and the goal of not repeating yourself to agents. |
| **What Menny replaced** | Evan's stack was security/SDL- and SonarQube-centric and not Cursor-native. MasterGenAIInstructions is `.cursor/rules/*.mdc`, vibe-coding workflows (rebuild, multi-model review, deploy verification), optional lightweight CI (`agent-guardrails.yml`: gitleaks + semgrep + zizmor instead of SonarQube), and Menny's own protocols — built on Evan's scaffolding idea, not a port of his rule content. |

### Menny's protocols (this repo — evolved from genAITemplate)

Multi-agent workflows built from real session corrections: sacred rebuild inventories, debate-to-consensus, diff-scoped phase reviews, expectation files (`.scratch/phase-plan.md`), DECISION-LOG / HANDOFF, subagent proof-of-read, deploy verification, autonomous BLOCKED stops.

**Files:** `rebuild-protocol.mdc`, `review-protocol.mdc`, `grill-protocol.mdc`, `plan-review.mdc`, `subagents.mdc`, `workflow.mdc`, `autonomous-mode.mdc`, `git-discipline.mdc`, `clean-code.mdc`, `deploy-awareness.mdc`, and others.

### [Ponytail](https://github.com/DietrichGebert/ponytail) — how to code

| | |
|---|---|
| **License** | MIT |
| **Fork** | [mennyg19-cmyk/ponytail](https://github.com/mennyg19-cmyk/ponytail) |
| **What it does** | Lazy senior-dev posture: YAGNI, stdlib/native first, shortest diff, no unrequested abstractions, ponytail-review at phase gates |
| **Rule file** | `ponytail.mdc` (always on, full intensity) |
| **On conflict** | Protocol-safe default; ponytail wins *how*, protocols win *what* |

### [Unslop](https://github.com/MohamedAbdallah-14/unslop) — how replies sound (Tier 1)

| | |
|---|---|
| **License** | MIT |
| **What it does** | Drops AI-isms (sycophancy, stock vocab, hedging stacks). Terse routine chat; direct HANDOFF/commits. Code logic stays exact. |
| **Integration** | Patterns baked into `ponytail.mdc` — **no** CLI, **no** `/unslop`, **no** extra plugin |
| **Not taken** | LLM rewriter, detector evasion, voice-match |

### [CodeGraph](https://github.com/colbymchenry/codegraph) — how to navigate code

| | |
|---|---|
| **License** | MIT (upstream) |
| **Fork** | [mennyg19-cmyk/codegraph](https://github.com/mennyg19-cmyk/codegraph) |
| **What it does** | Deterministic AST index via MCP (`codegraph_search`, `codegraph_callers`, `codegraph_impact`, `codegraph_files`, …). Hybrid with Read/grep for literals. |
| **Rule file** | `codegraph.mdc` (always on) |
| **Rebuild** | A+B hybrid: parent `graph-backbone/` digests + multi-model judgment |
| **Setup** | Automatic: scripts run `codegraph install` (once/machine, if missing) + `codegraph init` or `sync` (per project) on bootstrap, apply, and update-all when the CLI is on PATH. Install CLI from [colbymchenry/codegraph](https://github.com/colbymchenry/codegraph) if missing. |

### [Babysitter](https://github.com/a5c-ai/babysitter) — when to stop (Tier 1)

| | |
|---|---|
| **License** | MIT |
| **What it does (full product)** | JS process enforcement, stop hooks, `.a5c/runs/` journal, compression |
| **What we took** | Mandatory gate stops, command output summarization, `.scratch/run-state.md` checkpoints |
| **Integration** | Ideas in `workflow.mdc` + cross-refs — **no** `@a5c-ai/babysitter-sdk`, **no** npm plugin |
| **Exception** | Hotfix uses lighter gates per `hotfix-protocol.mdc` |

### [Julius Brussee / Caveman skills](https://github.com/JuliusBrussee/skills) — planning, prose, UI craft (Tier 1)

Patterns adapted from [JuliusBrussee/skills](https://github.com/JuliusBrussee/skills) (MIT). **No** `npx skills add`, **no** caveman always-on (conflicts with ponytail + plain-English tone). **Not taken:** caveman telegraphic mode, loop-factory CLI, cavemem.

| Skill (upstream) | What we took | Rule file |
|---|---|---|
| **grill-me** | Calibrated planning interview — one Q at a time, recommended answers | `grill-protocol.mdc` |
| **junior-to-senior** | Staff plan review — fog/tunnel, evidence, promoted plan v2 | `plan-review.mdc` |
| **interface-kit** | UI implementation priority stack + anti-generic aesthetics | `interface-kit.mdc` |
| **f\*ck-slop** | Deep prose de-slop loop (negative parallelism, verify passes) | `prose-deslop.mdc` |
| **context-canary** | Per-turn canary + trip/checkpoint protocol | `context-canary.mdc` |
| **loop-factory** | Grill gate before locked phase plans — ideas only, no CLI | `workflow.mdc`, `autonomous-mode.mdc` |

| | |
|---|---|
| **Rebuild** | Asks user (y/n) before Phase 0 whether to run grill |
| **Redesign** | Grill gate after REDESIGN-BRIEF, before audit |
| **Triggers** | `vocabulary.mdc` — "grill me", "senior review", "canary", "polish UI", "deslop this prose" |

### CI guardrails — automated safety outside the agent (optional)

Not Cursor rules — a **GitHub Actions workflow** that complements `deploy-awareness.mdc` and `review-protocol.mdc` trust-boundary checks. Ships in every bootstrapped project; tune or disable per repo.

| Tool | Repo | What it does |
|---|---|---|
| **gitleaks** | [gitleaks/gitleaks](https://github.com/gitleaks/gitleaks) | Scans git history and the working tree for leaked secrets (API keys, tokens, credentials). |
| **semgrep** | [semgrep/semgrep](https://github.com/semgrep/semgrep) | Static analysis with `p/default` — language-agnostic security and bug patterns without assuming Node/Python/Go. |
| **zizmor** | [zizmor/zizmor](https://github.com/zizmor/zizmor) | Security linter for `.github/workflows/*` (permissions, dangerous patterns, pinned actions). |

| | |
|---|---|
| **Workflow file** | `template/.github/workflows/agent-guardrails.yml` |
| **When it runs** | PR, push to `main`, manual `workflow_dispatch` |
| **Bootstrap** | Copied with the full template — new projects get it automatically |
| **apply.ps1** | Copies guardrails by default (skips if already present). Use `-NoGuardrails` to skip: `.\apply.ps1 -TargetDir path` |
| **update-all.ps1** | Copies guardrails + syncs CodeGraph in every registered project by default. Use `-NoGuardrails` to skip workflow copy: `.\update-all.ps1 -AutoCommit` |

Agents catch many issues in rules; CI catches what slips through (secrets in commits, common vulns, unsafe workflow YAML). Add language-specific build/test jobs separately — this file is safety rails only.

### Conflict resolution

- **At runtime:** `ponytail.mdc` conflict protocol → README § Rule Preferences
- **Canonical list:** `_meta/USER-RULE-PREFERENCES.md`
- **Human playbook:** `_meta/RULE-CONFLICTS.md` (not auto-loaded — saves tokens)

## Quick Start

### GUI Manager (recommended)

Double-click `manager.pyw` to open the GUI. It has tabs for:
- **New Project** -- create a bootstrapped project with all rules
- **Apply to Existing** -- add rules to an existing project
- **Update All** -- push rule changes to every registered project
- **Registry** -- view and manage registered projects

Requires Python 3 (uses tkinter, no extra installs).

### Command Line: Starting a New Project

```powershell
# PowerShell
.\bootstrap.ps1
```

```bash
# Bash
./bootstrap.sh
```

The script will ask for:
1. Project name
2. Description
3. Destination directory (default: current directory)
4. Whether to create a private GitHub repo

It copies the template files, replaces placeholders, initializes git, and optionally creates and pushes to a GitHub repo.

### What You Get

A new project directory with:
- **22 Cursor rule files** — 6 always-on, 1 auto-attach (`deploy-awareness.mdc`), 15 on demand (see below). Integrates [ponytail](https://github.com/DietrichGebert/ponytail), [unslop](https://github.com/MohamedAbdallah-14/unslop) anti-slop (Tier 1), [codegraph](https://github.com/colbymchenry/codegraph), [babysitter](https://github.com/a5c-ai/babysitter) gate discipline (Tier 1), and [Julius Brussee skills](https://github.com/JuliusBrussee/skills) (Tier 1) — rules only, no extra npm.
- **`.github/workflows/agent-guardrails.yml`** — optional CI: [gitleaks](https://github.com/gitleaks/gitleaks) + [semgrep](https://github.com/semgrep/semgrep) + [zizmor](https://github.com/zizmor/zizmor). Language-agnostic; tune per project.
- **AGENTS.md** -- same rules in portable format for Claude Code, Codex, or any AI tool.
- **DECISION-LOG.md**, **TESTING-STRATEGY.md**, **HANDOFF.md** -- seeded templates ready to use.
- Proper `.gitignore`.

### Applying to an Existing Project

```powershell
# PowerShell
.\apply.ps1 -TargetDir "C:\path\to\existing\project"
```

```bash
# Bash
./apply.sh /path/to/existing/project
```

This copies the 22 rule files and AGENTS.md into the project. It creates DECISION-LOG.md, TESTING-STRATEGY.md, and HANDOFF.md only if they don't already exist. It never touches your README.md, .gitignore, or any project code.

### After Bootstrapping or Applying

1. Open the new project in Cursor.
2. Fill in `deploy-awareness.mdc` with your deploy targets.
3. Review `.github/workflows/agent-guardrails.yml` — enabled by default on new repos; remove jobs or pin semgrep rulesets (`p/security-audit`, etc.) as needed. Org repos may need a `GITLEAKS_LICENSE` secret.
4. Start building — agents already know your workflow.

**Tuning CI guardrails:** drop jobs you don't need; add language build/test workflows separately. See **CI guardrails** in the rule stack section above.

## Rule Files

### Always-On (6 files, loaded every session)

| File | Purpose |
|---|---|
| `vocabulary.mdc` | Command words + protocol index |
| `workflow.mdc` | Core principles, gate discipline, command output, expectation files, security |
| `ponytail.mdc` | Ladder, anti-bloat, anti-slop (unslop Tier 1), conflict protocol |
| `codegraph.mdc` | CodeGraph MCP — hybrid structural lookup; A+B parent/subagent pattern |
| `git-discipline.mdc` | Branching, commits, push behavior |
| `clean-code.mdc` | Code quality, naming, anti-AI-tics, dependencies |

### Auto-Attach (1 file, via globs)

| File | Purpose |
|---|---|
| `deploy-awareness.mdc` | Deploy/env/workflow safety; auto-attaches on deploy-related files |

### Load on Demand (15 files)

| File | Trigger |
|---|---|
| `review-protocol.mdc` | Phase complete, review, production merge |
| `plan-review.mdc` | "senior review" / "junior to senior" / large agent-written plan |
| `grill-protocol.mdc` | "grill me" / redesign grill gate / rebuild if user opts in |
| `autonomous-mode.mdc` | "run autonomously" / decision logging |
| `testing-protocol.mdc` | Writing tests |
| `subagents.mdc` | Spawning any subagent |
| `rebuild-protocol.mdc` | User says "rebuild" |
| `redesign-protocol.mdc` | User says "redesign" |
| `interface-kit.mdc` | UI implementation after direction chosen |
| `prose-deslop.mdc` | Long-form publishable prose de-slop |
| `context-canary.mdc` | "canary" / context rot / long high-stakes session |
| `hotfix-protocol.mdc` | User says "hotfix" or "production is broken" |
| `cleanup-protocol.mdc` | User says "cleanup" or "clean up the codebase" |
| `session-handoff.mdc` | End of session or context limit |
| `code-walkthrough.mdc` | **Disabled** (saves tokens). Say `enable walkthroughs` to restore |

Conflict playbook (human reference, not auto-loaded): `_meta/RULE-CONFLICTS.md`.

## Updating Rules Across All Projects

When you edit a rule in this repo, push the changes to all registered projects:

```powershell
.\update-all.ps1
```

This copies the updated `.cursor/rules/` and `AGENTS.md` to every project in `registry.json`. It will offer to commit the changes in each project. Projects that no longer exist are automatically removed from the registry.

## Using Without Cursor

`AGENTS.md` in each bootstrapped project contains the same rules in portable format. It works with Claude Code, Codex, or any AI tool that reads project docs.
