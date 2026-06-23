# Rule Conflicts: Integrated Stack Playbook

Reference for humans and for agents when surfacing options. Not auto-loaded into every session (saves tokens). Agents use the conflict protocol in `ponytail.mdc`; this file is the expanded playbook.

Standing resolutions belong in each project's **README § Rule Preferences** so agents stop re-asking.

Canonical preferences: `_meta/USER-RULE-PREFERENCES.md`.

---

## How the stack works

| Layer | Source | What it owns | Always on? |
|---|---|---|---|
| **genAITemplate** | [EvanPokroy/genAITemplate](https://github.com/EvanPokroy/genAITemplate) | Foundation: bootstrap + stamp agent instructions into new repos | N/A (historical) |
| **Protocols** | Menny / [MasterGenAIInstructions](https://github.com/mennyg19-cmyk/MasterGenAIInstructions) (evolved from genAITemplate) | Rebuild inventory, review loops, deploy gates, autonomous BLOCKED | On demand |
| **Ponytail** | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | Ladder, YAGNI, anti-bloat, terse chat, conflict protocol | Yes |
| **Anti-slop** | [unslop](https://github.com/MohamedAbdallah-14/unslop) Tier 1 in `ponytail.mdc` | Drop AI-isms; human voice in chat, comments, commits, HANDOFF | Yes |
| **CodeGraph** | [codegraph](https://github.com/colbymchenry/codegraph) in `codegraph.mdc` | Deterministic structural lookup; hybrid with Read/grep; A+B rebuild backbone | Yes |
| **Gate discipline** | [babysitter](https://github.com/a5c-ai/babysitter) Tier 1 in `workflow.mdc` | Mandatory stop at gates; command output discipline; `.scratch/run-state.md` | Yes |
| **Clean-code** | Menny (MasterGenAIInstructions) | Naming, code anti-tics, UI consistency, Rule of 2 | Yes |
| **Workflow** | Menny (MasterGenAIInstructions) | Orientation, execution discipline, expectation files, security | Yes |
| **On conflict** | `ponytail.mdc` | Explain → options → README preferences → protocol-safe default | Yes |
| **Julius skills** | [JuliusBrussee/skills](https://github.com/JuliusBrussee/skills) Tier 1 | Grill, plan-review, interface-kit, prose-deslop, context-canary | On demand |

**Design intent:** Protocols own scope and quality gates. Ponytail + integrations keep day-to-day work lean — fewer tokens, less slop, fewer deps — without quietly dropping features or skipping reviews.

**Integrated repos:** Tier 1 only (patterns baked into rules). No unslop CLI, no babysitter npm, no codegraph as a project dependency — external CLI/MCP tools are fine.

---

## Resolved standing preferences (do not re-ask)

| Conflict | Menny's choice |
|---|---|
| Rebuild scope vs YAGNI | Protocol wins scope; ponytail wins how. Ask before DROP-with-approval. |
| Walkthrough headers vs brevity | **Walkthroughs off** (`code-walkthrough.mdc` disabled). Clear naming + codegraph for navigation. |
| Testing depth vs minimal | Hybrid — `testing-protocol.mdc` floor, ponytail-shaped minimal tests. |
| God files vs fewest files | Split on refactor, >500 lines, or mixed concerns. |
| Multi-model vs minimal process | Rebuild/redesign only unless "use more models." |
| Fix-don't-suggest vs question | Build what was asked. |
| Artifacts vs terse chat | Artifacts follow protocol formats; anti-slop = direct facts, not padding. |
| CodeGraph vs grep | Hybrid — MCP or CLI for structure when indexed; Read/grep for literals only. No MCP ≠ grep. |
| Gate discipline vs hotfix | Hotfix skips multi-agent review loop; single self-review per `hotfix-protocol.mdc` / `review-protocol.mdc` deviations. |
| Don't stop until done vs mandatory stop | Finish the whole run; **do not skip gates** on the way (`workflow.mdc`). |

---

## Conflict matrix (open options — only if README has no entry)

### 1. Rebuild / inventory scope vs YAGNI

| | Ponytail | Protocol |
|---|---|---|
| **Says** | Question speculative work | Every inventory ID and route must ship |

**Resolved default:** A — protocol wins scope, ponytail wins implementation.

---

### 2. Walkthrough headers vs chat brevity

**Resolved:** Walkthroughs **off**. Say `enable walkthroughs` to restore archived rule.

---

### 3. Testing depth vs ponytail minimum

**Resolved default:** A — protocol floor, ponytail-shaped tests.

---

### 4. God-file split vs fewest files

**Resolved default:** A — split when >500 lines, mixed concerns, or refactor command.

---

### 5. Multi-model review vs minimal process

**Resolved default:** A — full gates at phase/production merge; ponytail between gates.

---

### 6. "Fix don't suggest" vs questioning complex requests

**Resolved default:** C — strict fix-don't-suggest; no lazy slice and re-argue.

---

### 7. Decision logs / expectation files vs minimal prose

**Resolved default:** A — artifacts not subject to chat brevity; anti-slop still applies (no slop, complete facts).

---

### 8. CodeGraph always-on vs no MCP configured

| | Codegraph rule | Reality |
|---|---|---|
| **Says** | Load every session; init if missing | MCP may not be wired in every session (subagents never get MCP) |

**Resolved default:** Keep CodeGraph rule loaded. If MCP tools aren't in session but CLI is on PATH and `.codegraph/` exists, use CLI (`codegraph explore`, `codegraph query`, …) — **not grep**. If both MCP and CLI unavailable after one init attempt, stop retrying and use Read/grep fallback for that run.

---

### 9. Anti-slop in ponytail vs clean-code Anti-AI-Tics

**Not a conflict.** Ponytail/unslop = prose voice (chat, commits, HANDOFF). Clean-code = code patterns (nesting, try/catch, verbosity). Both apply.

---

### 10. Caveman (Julius) vs ponytail + plain-English tone

| | Caveman | This stack |
|---|---|---|
| **Says** | Telegraphic ~75% token compression always | Plain English (`workflow.mdc`); ponytail terse routine + full explain when needed |

**Resolved default:** Do **not** install caveman always-on. Optional user request for extra compression only if they explicitly ask — ponytail + anti-slop is the standing choice.

---

## Recording a standing preference

In the project README § Rule Preferences. Agents check before re-asking on the same conflict.
