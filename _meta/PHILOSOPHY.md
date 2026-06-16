# Why This Exists

I got tired of repeating myself to AI agents.

Every project, every session, I'd say the same things: commit and push after every change, don't suggest when I tell you to fix, write in plain English, don't stop until the job is done. I'd correct the same mistakes: agents silently changing UI when I asked for a refactor, making up business logic instead of asking, leaving three dev servers running on different ports.

So I built **MasterGenAIInstructions** — one place where all my rules live. One bootstrap script stamps them into every new project. Agents follow my workflow from the first commit.

The core protocols grew from real experience: hundreds of hours of AI-assisted development across Python/Flask, React Native, Next.js, and more. They evolved from corrections in actual sessions, patterns in chat histories, and mistakes I got tired of seeing.

This is not a framework. It's practical rules that make agents work the way I want them to.

---

## How the stack is designed

Different tools solve different problems. They are **layered**, not merged into one blob:

| Layer | Job | Analogy |
|---|---|---|
| **Protocols** (this repo) | *What* to do and *when* — rebuild inventory, review loops, deploy gates | The playbook |
| **Ponytail** | *How* to implement — YAGNI, ladder, shortest diff | The senior dev at the keyboard |
| **CodeGraph** | *How to navigate* code — deterministic structure, not guessing from grep | The map |
| **Unslop** (Tier 1) | *How replies sound* — drop AI-isms, save tokens on chat | The editor |
| **Babysitter** (Tier 1) | *When to stop* — gates, checkpoints, don't flood context with logs | The stage manager |

**Protocols stay in charge of scope and quality.** Integrations make day-to-day work leaner without quietly dropping features or skipping reviews.

When layers disagree, agents use the conflict protocol in `ponytail.mdc`: name it, offer options, default protocol-safe, tell me, offer to record in README § Rule Preferences. Expanded playbook: `_meta/RULE-CONFLICTS.md`. Canonical choices: `_meta/USER-RULE-PREFERENCES.md`.

**Integration style:** External repos are mostly **Tier 1** — ideas and patterns baked into `.mdc` rule files. No competing plugin stacks, no extra npm in every project. CodeGraph is the exception: it's an optional external CLI/MCP you install once per machine and init per repo.

---

## Credits — where the rules came from

### Original protocols (Menny / MasterGenAIInstructions)

**What they do:** Own the workflows I actually run — multi-phase rebuilds with sacred feature inventories, debate-to-consensus architecture, diff-scoped phase reviews, expectation checklists in `.scratch/`, DECISION-LOG / HANDOFF, subagent mechanics (paths not pastes, proof-of-read, family diversity), deploy verification, autonomous BLOCKED stops, hotfix/cleanup/redesign paths.

**Where they live:** `rebuild-protocol.mdc`, `review-protocol.mdc`, `subagents.mdc`, `workflow.mdc`, `autonomous-mode.mdc`, and the rest of `template/.cursor/rules/`.

**Why they exist:** Agents are eager to skip steps, shrink scope, and declare done from memory. These protocols encode the corrections I kept making by hand.

---

### Ponytail — coding posture

- **Credit:** [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) (MIT). Menny's fork: [mennyg19-cmyk/ponytail](https://github.com/mennyg19-cmyk/ponytail).
- **What it does:** Lazy senior-dev discipline — YAGNI, stdlib/native first, no unrequested abstractions, shortest working diff, `ponytail:` comments on deliberate shortcuts. Full intensity always on.
- **Where it lives:** `ponytail.mdc` (always on). Ladder referenced from `clean-code.mdc`.
- **How we integrated it:** Always-on rule + conflict protocol. Ponytail does **not** replace rebuild scope or review gates — on conflict, protocols win scope; ponytail wins *how* things are built.
- **Also owns:** Ponytail-review at phase gates (complexity hunt: delete/stdlib/native/yagni/shrink).

---

### Unslop — anti-slop voice (Tier 1)

- **Credit:** [MohamedAbdallah-14/unslop](https://github.com/MohamedAbdallah-14/unslop) (MIT).
- **What it does:** Strips AI-isms from prose — sycophancy openers, stock vocab (delve, tapestry, …), hedging stacks, tricolon padding, em-dash pileups. Subtract, don't add. Keeps code/logic exact; precision beats voice on security and runbooks.
- **Where it lives:** Baked into `ponytail.mdc` § Chat output (always on). Cross-refs in `workflow.mdc`, `subagents.mdc`, `session-handoff.mdc`.
- **How we integrated it:** **Tier 1 only** — pattern list in rules, no `/unslop` command, no pip install, no always-on plugin file. Saves tokens by banning filler in routine replies and artifacts (HANDOFF, commits, DECISION-LOG).
- **What we did not take:** LLM rewriter mode, detector evasion, voice-match profiles — not needed for dev workflow.

---

### CodeGraph — structural code intelligence

- **Credit:** [colbymchenry/codegraph](https://github.com/colbymchenry/codegraph). Menny's fork: [mennyg19-cmyk/codegraph](https://github.com/mennyg19-cmyk/codegraph).
- **What it does:** Tree-sitter AST + SQLite index. Deterministic MCP tools (`codegraph_search`, `codegraph_callers`, `codegraph_impact`, …). Same query + same index = same facts for any model.
- **Where it lives:** `codegraph.mdc` (always on). Woven into `rebuild-protocol.mdc` Phase 0, `subagents.mdc`, `vocabulary.mdc` (refactor → impact first).
- **How we integrated it:** Hybrid lookup — codegraph for structure; Read/grep for literals and configs. **A+B rebuild pattern:** parent writes `graph-backbone/` digests (shared facts); subagents interpret with different models and drill down via MCP if available. Agents run `codegraph init` if `.codegraph/` is missing.
- **Setup:** `codegraph install` once per machine (MCP); `codegraph init` per project. Bootstrap offers init when CLI is present.

---

### Babysitter — gate discipline (Tier 1)

- **Credit:** [a5c-ai/babysitter](https://github.com/a5c-ai/babysitter) (MIT).
- **What it does (full product):** JS process definitions, stop hooks, event-sourced `.a5c/runs/` journal, token compression — enforces workflow in code, not markdown.
- **What we took:** **Tier 1 only** — the *ideas*, not the npm plugin:
  - **Mandatory stop** at gates — no next phase/todo/spawn until checklists, reviews, and platform builds are clean.
  - **Command output discipline** — summarize long terminal output; huge logs → `.scratch/last-command.log`.
  - **Run checkpoint** — `.scratch/run-state.md` for rebuilds and autonomous runs (lighter than a full journal).
- **Where it lives:** `workflow.mdc`, `review-protocol.mdc`, `rebuild-protocol.mdc`, `autonomous-mode.mdc`, `session-handoff.mdc`.
- **What we did not take:** `@a5c-ai/babysitter-sdk`, Cursor experimental plugin, lossy context compression hooks — rules-only enforcement is enough for now; hotfix still gets a documented lighter gate per `hotfix-protocol.mdc`.

---

## Token strategy

Rules are expensive — every always-on file loads every session. This system optimizes deliberately:

- **~7 always-on files**, ~10 on demand (rebuild, review, subagents load only when triggered).
- **Walkthrough headers off** — archived `code-walkthrough.mdc`; codegraph + clear naming replace file-navigation overhead.
- **Subagents:** pass paths, not pasted documents; ≤10-line replies; graph-backbone instead of six blind tree walks.
- **Anti-slop + terse routine chat** — shorter outputs.
- **Command output discipline** — don't burn context on test logs.
- **DECISION-LOG rotation** — keep session-start reads cheap.
- **Human meta** (`RULE-CONFLICTS.md`, `USER-RULE-PREFERENCES.md`) not auto-loaded into agents.

---

## What "done" means for an agent

An agent following this stack should:

1. Orient: HANDOFF → run-state → README Rule Preferences → AGENTS.md → recent DECISION-LOG.
2. Build with ponytail ladder + anti-slop voice.
3. Navigate structure with codegraph when indexed.
4. Complete gates before advancing; log decisions; verify in the running app.
5. Review at phase boundaries until clean; platform green after push.

That's the operating system. Everything else is vocabulary for triggering the right protocol on demand.
