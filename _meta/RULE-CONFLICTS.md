# Rule Conflicts: Ponytail vs MasterGenAI Instructions

Reference for humans and for agents when surfacing options. Not auto-loaded into every session (saves tokens). Agents use the conflict protocol in `ponytail.mdc`; this file is the expanded playbook.

Standing resolutions belong in each project's **README § Rule Preferences** so agents stop re-asking.

---

## How the stack works

| Layer | What it owns | Always on? |
|---|---|---|
| **Ponytail** | *How* to implement: ladder, anti-bloat, terse chat output, `ponytail:` comments | Yes |
| **Clean-code** | Naming, anti-slop, UI consistency, one-pattern-per-concern, Rule of 2 | Yes |
| **Workflow** | Orientation, execution discipline, expectation files, security basics | Yes |
| **Protocols** | *What* to do and *when*: rebuild inventory, review loops, deploy gates, autonomous BLOCKED | On demand |
| **On conflict** | Explain both sides → options → README preferences → ask or protocol-safe default | Yes |

**Design intent:** Your workflow stays in control of scope, quality gates, and multi-agent rigor. Ponytail keeps day-to-day coding lean -- less token burn, less AI slop, fewer deps -- without quietly dropping features or skipping reviews.

---

## Conflict matrix (with resolution options)

### 1. Rebuild / inventory scope vs YAGNI

| | Ponytail | Your rule |
|---|---|---|
| **Says** | Skip speculative features; question whether work needs to exist | Every inventory ID and route must ship; nothing dropped |
| **Tension** | Ultra ponytail may want to challenge a feature | Rebuild treats inventory as sacred |

**Options:**
- **A (recommended default): Protocol wins scope, ponytail wins implementation.** Build every required ID; use the ladder for *how* (stdlib, no extra deps, minimal UI wiring).
- **B: Ponytail wins on speculative extras.** Ship inventory only; defer nice-to-haves with user approval logged as DROP-with-approval.
- **C: User re-scopes.** Pause rebuild; user trims inventory explicitly.

---

### 2. Walkthrough headers vs chat brevity

| | Ponytail | Your rule |
|---|---|---|
| **Says** | ≤3 lines after code; cut long explanations | Every file gets a plain-English walkthrough block at top |

**Options:**
- **A (recommended default): Split surfaces.** Walkthrough headers stay in files; ponytail brevity applies to agent chat and inline code comments only.
- **B: Shorter walkthroughs.** One-line file purpose + function list only (still present, trimmed).
- **C: No walkthroughs.** Ponytail wins; rely on clear code only (loses your readability goal).

---

### 3. Testing depth vs ponytail one-check minimum

| | Ponytail | Your rule |
|---|---|---|
| **Says** | One runnable smoke check for non-trivial logic | Tests alongside code; regression test per bug fix; TESTING-STRATEGY entries |

**Options:**
- **A (recommended default): Protocol floor, ponytail shape.** Meet testing-protocol requirements; keep each test minimal (no fixture forests).
- **B: Ponytail minimum only.** One check per module until user asks for more (faster, weaker gate).
- **C: Full suite as today.** Protocol wins entirely; ponytail only affects production code, not test count.

---

### 4. God-file split vs fewest files

| | Ponytail | Your rule |
|---|---|---|
| **Says** | Fewest files possible | Split god files by concern; refactor covers structure |

**Options:**
- **A (recommended default): Concern split when commanded.** Default to fewest files; split when file is >500 lines, mixed concerns, or user said refactor.
- **B: Never split.** Ponytail wins; one file until unbearable.
- **C: Aggressive split.** Clean-code wins; ponytail applies inside each resulting file.

---

### 5. Multi-model review / subagents vs minimal process

| | Ponytail | Your rule |
|---|---|---|
| **Says** | Shortest path; avoid redundant work | Multi-family reviews, debate loops, proof-of-read -- non-negotiable at phase gates |

**Options:**
- **A (recommended default): Gates stay; ponytail between gates.** Full review loop at phase/production merge; ponytail ladder for all implementation between gates.
- **B: Lighter reviews.** Self-review + one independent pass (faster, weaker).
- **C: Full protocol always.** No ponytail influence on process (coding style only).

---

### 6. "Fix don't suggest" vs questioning complex requests

| | Ponytail | Your rule |
|---|---|---|
| **Says** | Ship lazy version and ask if full version needed | Implement direct instructions; don't offer alternatives unless asked |

**Options:**
- **A (recommended default): Implement + one-line lazy note.** Do what user asked; append single line if a simpler path existed (lite ponytail behavior) without stalling.
- **B: Ponytail questions first.** Pause and ask before building complex asks (conflicts with fix-don't-suggest).
- **C: Strict fix-don't-suggest.** No lazy alternatives mentioned unless user asks.

---

### 7. Decision logs / expectation files vs minimal prose

| | Ponytail | Your rule |
|---|---|---|
| **Says** | Terse output | DECISION-LOG format, expectation checklists with evidence |

**Options:**
- **A (recommended default): Not in scope for ponytail brevity.** Artifacts follow workflow/autonomous formats; ponytail applies to code and casual chat only.
- **B: Terse logs.** Shorter DECISION-LOG entries (risk: loses audit trail).

---

## Recording a standing preference

In the project README:

```markdown
## Rule Preferences

- **Rebuild scope vs YAGNI:** A -- protocol wins scope, ponytail wins how.
- **Walkthrough vs brevity:** A -- headers stay, chat stays terse.
- **Testing:** A -- protocol floor, ponytail-shaped tests.
```

Agents check this section before re-asking on the same conflict.
