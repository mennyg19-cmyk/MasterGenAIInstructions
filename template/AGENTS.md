# Agent Instructions

Portable version of the project's Cursor rules for non-Cursor environments (Claude Code, Codex, etc.). If using Cursor, the `.cursor/rules/*.mdc` files are the source of truth -- this file mirrors them.

---

## Vocabulary

These definitions are exact. Do not under-scope or over-scope.

| Command | Meaning |
|---|---|
| **tidy / clean up** | Current file only. Remove dead code, fix naming, inline trivial things. |
| **refactor** | Whole feature or module. Cover every applicable category. |
| **aggressive refactor** | Entire codebase. Every applicable category. |
| **rebuild** | Multi-agent rebuild. Keeps every feature, rebuilds the app properly -- fixes structure, layout, and clashing modules. Not a pixel copy. See Rebuild Protocol. |
| **redesign** | UI/UX overhaul. Keeps core logic intact. Starts with discovery conversation. See Redesign Protocol. |
| **fix** | Specific bug, smallest possible change. |
| **add** | New feature, follow existing patterns. |
| **update / enhance** | Extend an existing feature. |
| **run autonomously** | Scope, surface questions, then work unattended. See Autonomous Mode. |
| **review** | Launch a review subagent on current state. See Review Protocol. |
| **hotfix** | Emergency production fix. Speed over ceremony. See Hotfix Protocol. |
| **hand off / save state** | Write HANDOFF.md for the next session. See Session Handoff. |

If user says "refactor" and you only touch one category, that is a failure.

---

## Workflow

### Tone

All communication uses plain English. Target audience: a self-taught programmer who reads code fine but hates jargon. Not overly technical, not dumbed down.

### Session Start

1. If HANDOFF.md exists, read it first.
2. Read README.md, AGENTS.md, DECISION-LOG.md.
3. Read files relevant to the current task.
4. Never start editing without completing orientation.

### Core Principles

- Read before edit -- scan for existing helpers, components, patterns.
- Smallest complete change -- no drive-by rewrites.
- Match existing patterns -- don't introduce competing approaches.
- No silent scope creep -- restate goal, locate blast radius, check prior art.
- Reference app pattern -- when building from another app, define source-of-truth for UI vs. logic vs. data in README first.
- README is the front door -- keep it current.
- If uncertain and user is present, ask. If autonomous, decide and log.

### Execution Discipline

- Fix, don't suggest -- implement direct instructions, don't offer alternatives unless asked.
- Don't stop until done -- finish all phases, todos, steps.
- Verify in the running app before declaring done.
- Implement plans verbatim -- don't edit the plan file.
- Screenshots are ground truth.
- Revert completely or not at all.
- Continue after interruption -- pick up where you left off.
- Run commands yourself -- don't hand the user instructions.
- Don't silently choose business logic -- log decisions.
- Completion checklist before declaring done -- read through every todo/phase/checklist item and confirm each is actually complete. Never declare done from memory.

### Dev Server Hygiene

- Kill servers you started when done or starting new ones.
- Never leave multiple instances on different ports.
- Report which port the app is on.

### Security Basics

- Never commit secrets. Provide `.env.example` with placeholders.
- `.env` and `.env.local` must be in `.gitignore`.
- Sanitize user input. Never log secrets. Default to least privilege.

---

## Git Discipline

- Never work on `main` directly. Use working branches.
- Auto-commit+push after every completed logical change.
- One logical change = one commit. Push immediately.
- Merge to `main` when a phase or job is done.
- Honest commit messages. Never amend pushed commits.
- Branch naming: `rebuild-auth`, `fix-invoice-calc`, `redesign-dashboard`.
- **Never assume `main` is the production branch.** Check deploy config or README first.
- **Document branch strategy in README on day one**: which branch deploys where, which is for dev, which is for prod.
- **After every push, verify the builds it triggered passed** (Vercel, GitHub Actions, other CI). A push isn't done until its builds are green. See Deploy Awareness.

---

## Clean Code

### Abstraction

- Rule of 2 for new abstractions (2+ real call sites now).
- No barrel files unless 5+ exports. No tiny wrapper components.
- Split files by concern, not by count.

### Comments

- No narration or change-explanation comments.
- Comments for non-obvious intent only. Tone per Workflow section.

### Naming

- No vague names (`data`, `result`, `temp` banned standalone).
- Functions describe what they DO. Booleans read as yes/no questions.
- Collections plural, items singular.

### Error Handling

- No swallowed errors. No defensive code for impossible conditions.
- Error messages: what went wrong + what was expected.

### Anti-AI-Tics

- No unnecessary try/catch. No redundant type assertions.
- No over-verbose code. No "just in case" code.
- Max 3 levels of nesting.

### UI Consistency

- New screens reuse existing header/theme/navigation patterns.
- Back buttons go to origin. If a screen looks different, it's a bug.

### One Pattern Per Concern

- One error-handling approach, one data-fetching pattern, one styling approach, one state management pattern per project.
- Pick in the first session, document in README, never introduce a competing one.

### Dependencies

- Prefer stdlib. State WHY for new packages. Pin versions. No duplicates.

---

## Review Protocol

- A "phase" = work spanning more than one commit.
- Review with a readonly subagent (default: `gpt-5.5-extra-high`) BEFORE committing.
- Review findings go into DECISION-LOG.md.
- Resolve blockers before committing or advancing.
- **"Compiles" is never the bar.** A review must check that the work actually does what it was supposed to, end to end -- not just that it typechecks and lints. For a UI page: is every control present and functional, or a read-only stub? For a bug fix: is the bug gone in the running app?
- **Review is a LOOP, not one pass.** Reviewer reports findings → you fix every one → a FRESH reviewer (different model family, no prior context, so it can't rubber-stamp) re-checks → repeat until a pass returns ZERO findings. "Found things, fixed them, moved on" without a clean re-review is not allowed (the user has been explicit about this).
- **Feature-parity review** (rebuilds / "match the old thing" work): reviewer gets the inventory + old reference and **enumerates every route and every ID -- no sampling** (sampling let an entire page ship missing). Route-coverage diff first (every old route has a working new route), then mark every item PRESENT/PARTIAL/STUB/MISSING with evidence, verified in the running app. Anything unverifiable = MISSING. Phase fails while anything is less than PRESENT.

---

## Autonomous Mode

### Before User Leaves

1. Scope the task. Surface all foreseeable questions.
2. User answers. Confirm understanding. User leaves.

### While Away

- Log every decision in DECISION-LOG.md: What I decided / Options / Choice / Why / Status.
- High-risk decisions (data loss, security, breaking changes): status BLOCKED, commit the log, stop.

### When User Returns

- Present summary: done, decisions, pending.

---

## Testing Protocol

- Build testing strategy alongside code in TESTING-STRATEGY.md.
- Write tests as you go. Test names describe scenarios.
- Test: business logic, user behavior, edge cases, errors, authorization.
- Don't test: framework internals, trivial getters, UI layout.
- Every bug fix gets a regression test.

---

## Code Walkthrough

- Every file gets a plain-English walkthrough block at the top (after imports).
- Lists each function/class in code order with a one-line description.
- Updated whenever functions are added, removed, or renamed.

---

## Subagents & Models

See `subagents.mdc` for the single source of truth. Key points:

- "Spawn a subagent" = **Task tool**, `subagent_type` (`generalPurpose` to write, `explore` for read-only), `run_in_background: true` when parallelizing, and **`model` set explicitly**. The prompt must carry ALL context -- the subagent can't see your chat.
- **Never silently fall back to your own model.** If a slug is rejected, the tool returns the valid list; pick another valid slug. Dropping `model` and running on the parent model defeats the entire point of multi-model coverage and already burned one "multi-model" audit that was secretly single-model.
- **Multi-subagent jobs use different families** (Composer, GPT, Codex, Gemini, Grok, Kimi, Claude Sonnet/Opus). Never the same slug twice for the same job. Diversity beats power -- cheap cross-family models are fine for audits/reviews.
- The roster in `subagents.mdc` is a snapshot; the Task tool's accepted slugs are the real source of truth.

---

## Rebuild Protocol

See `rebuild-protocol.mdc` for the full 6-phase multi-agent workflow.

**What a rebuild is:** the app grew by bolting features on top of features until it's a stack of cards -- messy structure, things in the wrong place, clashing modules, misaligned CSS. A rebuild keeps every feature but builds it again the right way.

**The #1 rule has two halves:**

1. **Keep every feature (sacred).** The old app is the source of truth for WHAT it can do. Nothing gets dropped -- every page, button, dialog, form, import/export, filter, bulk/row action. Read the old code for feature reference so nothing is missed. "Built the engine, skipped the car" (great backend + read-only skeleton pages) is a FAILURE -- every capability must be wired to a real working control. A past rebuild dropped ~75% of UI features; never again.
2. **Improve the look and structure (the point).** This is NOT a pixel-perfect photocopy. Move misplaced things, group related things, fix broken/clashing interactions, and rebuild the CSS so it lines up and is consistent. The app should come out cleaner and more coherent than before. The test is "every feature works AND it's built better," not "it looks identical."

Phase 1 inventory captures both: everything to keep AND a "what's wrong / to fix" list. Plans are organized PAGE BY PAGE with a feature sub-checklist (keep list) plus structural fixes (improve list) -- a coarse phase like "Admin UI" covering 20 pages is how features get lost. Build UI and internals together per feature, not backend-first. Flag significant structural changes for the user. Verify each screen in the running app: features all work, fixes applied, layout clean.

**Critical mechanical requirement:** see `subagents.mdc` (single source of truth for spawning + the model roster). "Spawn a subagent" means use the **Task tool** with `subagent_type: "generalPurpose"` (or `"explore"` for read-only), `run_in_background: true`, and the **`model` parameter set explicitly**. If you omit `model`, the subagent runs on your own model and multi-model coverage is gone. If a slug is rejected, the tool returns the valid list -- **pick another valid slug; NEVER drop `model` and fall back to your own model** (that silent fallback already defeated one "multi-model" audit). For a multi-subagent job, use different families, never the same slug twice.

**Coverage is mechanical, not vibes.** Phase 1 gives every page/feature a stable ID and puts a complete route manifest at the top of FEATURE-INVENTORY.md. Every ID must be claimed by exactly one plan todo. A todo is "done" only when its route actually loads in the running app and every sub-item is verified -- marking a page done that doesn't render is what silently lost an entire page (the order builder). Re-reconcile every few phases. The final review (Phase 5) builds a reconciliation ledger FIRST: a route diff (every old route has a working new route) and an inventory-ID ledger walked line-by-line (no sampling -- sampling is what let a whole page ship missing while builder AND reviewer overlooked it); anything unverifiable is MISSING. The review then LOOPS -- fix findings, re-review on a fresh/different model, repeat until zero findings -- and a hard done-gate (all routes green, all IDs PRESENT, all fixes applied, last review clean, deploy green) must pass before "done."

Summary: multi-model audit (each area audited by at least 2 DIFFERENT model families -- rotate across Composer, GPT, Codex, Gemini, Grok, Kimi, Claude; diversity matters more than power; never the same model twice per area) + chat history mining, feature inventory (IDs + route manifest) cross-referenced against build history, architecture proposals from premier agents, debate and converge into a granular plan (every screen, route, component, endpoint gets its own todo with a keep-list + fix-list, each citing the inventory IDs it covers -- general todos are a failure), **smoke deploy after the foundation scaffold** (catches missing middleware, env vars, build command issues before they stack up), then build todo-by-todo with looped review gates, mid-build reconciliation, and a final enumerated review + done-gate. Every feature is preserved; the structure/layout gets fixed and improved (not a pixel copy). Everything technical is on the table (framework, language, hosting, packages) unless the user says otherwise.

---

## Redesign Protocol

See `redesign-protocol.mdc` for the full workflow. **You do NOT design it yourself.** A redesign is a competition between models: spawn one subagent per design direction, each on a DIFFERENT model family (per `subagents.mdc`), and each builds a real, self-contained, viewable HTML preview of the key screen(s) into `previews/`. The user opens them side by side and picks the parts they like -- the main agent coordinates, it does not produce its own competing design (building one homepage yourself instead of spawning the models is a protocol violation the user has had to stop). When the user says "more options / more models," spin up one per family across the whole roster. Summary: discovery about pain points, UX audit, multi-model proposals with viewable previews, user review and iteration, phased build, looped final review (fix → re-review on fresh eyes → repeat until clean; existing functionality must still work). Everything visual/frontend is on the table (CSS framework, component library, layout approach) unless the user says otherwise.

---

## Hotfix Protocol

Emergency fixes: branch from main as `hotfix/<description>`, reproduce with a test, fix, self-review, merge to main, deploy immediately. Skip multi-agent reviews.

---

## Session Handoff

Write HANDOFF.md with: what's done, what's in progress, what's next, open decisions, gotchas. Overwritten each time.

---

## Cleanup Protocol

See `cleanup-protocol.mdc`. Full codebase sweep for clutter: test artifacts, cache files, logs, old versions, dead code files, temp files. Agent asks about ambiguous items (e.g., multiple app versions), then presents a detailed deletion report -- every file, what it is, why it was created, why delete it. User confirms before anything is deleted. After cleanup, update .gitignore to prevent recurrence.

---

## Deploy Awareness

See `deploy-awareness.mdc` for full rules. Key points:

### Build Verification

Before every commit, run the FULL local gate: type checker (`tsc --noEmit`), linter, formatter check (`prettier --check`), and the real production build (`next build`), plus tests. **`tsc` + lint are not enough** -- only `next build`/Turbopack catches server/client boundary violations (a `"use client"` file importing a server-only module), which shipped a red Vercel build; guard server modules with `import "server-only"`. **Re-run the whole gate after every batch of fixes** (including review fixes) -- pushing fixes blind caused stacked CI failures. Never push code that doesn't compile.

### Post-Commit Build Verification

After every push, verify the builds it triggered actually went green -- don't assume. Vercel: `vercel ls` + `vercel inspect <url>` (or the Vercel MCP), wait for `READY`, read logs and fix if `ERROR`. GitHub Actions: `gh run list` + `gh run watch <id>` / `gh run view <id> --log-failed`. Other hosts (Azure, Netlify, Expo, Docker): check that platform the same way. A red or unverified build is your problem even if the local build was green -- stop and fix before starting the next task. **"Should pass" is banned** -- observe and quote the real status (CI success AND deploy READY); saying "it should pass" while it was red forced the user to repeat "check yourself." No CI/host = no-op, but confirm that's actually the case.

### "Done" = Visible Online

A milestone is done only when it's **merged into the branch that actually deploys** (often NOT `main` -- check), the deployment reached **READY**, and the **live URL shows the new work with real/seeded data**. A "done" redesign that sat on an unmerged branch and wasn't visible online, and fixes made on a feature branch while prod built `main`, were both false "dones." Committed-to-a-branch is not done.

### Database Deploy Rules

- **NEVER** put `prisma db push` or `prisma db push --accept-data-loss` in a build script. This can destroy production data on every deploy.
- **NEVER** put `prisma migrate deploy` in the build command when deploying against an existing DB with unknown migration history.
- **Safe build command**: `prisma generate && next build`.
- Use `prisma migrate` for production, `db push` for local dev only.
- Run migrations manually or in a separate CI step, not in the build.
- **A rebuild gets a fresh, isolated DB branch** -- never point new code at the old project's populated DB (that 500'd `/admin` on first deploy).
- **Read `schema.prisma` for an entity before writing code against it.** Don't write field/enum names from memory (the model was redesigned). Two schema-mismatch errors in a row = stop and generate a field reference; don't keep guessing.

### Environment Variables

- Every new env var: add to `.env.example`, add to env validation schema, document which environments need it, flag in commit message.
- Before deploying: compare `.env.example` against what's set in the deploy target. Missing vars = silent failures.
- **Check env-var scope, not just presence** -- a Vercel var set only in Production makes every Preview build fail. Preview/Dev scopes must hold the same keys Production needs.
- After major features: audit env vars across all environments for drift.

### Auth Framework Completeness

When adding auth (Clerk, Auth0, etc.), verify ALL of these as a set: provider wrapper, middleware file, sign-in/sign-up page routes, env vars in every environment, callback URLs in the auth dashboard. Missing any one causes deploy crashes.

### Smoke Deploy

Deploy early, not after 5 phases of local-only development. After the foundation scaffold, do a smoke deploy that **loads a real authenticated page against the real DB** (not just the homepage -- that's where a schema-mismatch crash hid). Fix any issues before building more features on top.

### An Empty 200 Is Not "Working"

A data-driven page returning 200 with no data is not verified (an "verified" order builder was actually broken on an empty dev DB). Seed realistic data, then confirm real content renders and the primary action works end to end. "200" and "screenshot of the hero" are not verification.

### Windows / PowerShell

- PowerShell `Out-File` adds UTF-8 BOM that breaks Prisma and JSON parsers. Strip with `$content.TrimStart([char]0xFEFF)`.
- Build output capture in PowerShell is fragile. Redirect to file: `2>&1 | Out-File build.log`.
- Stray `package-lock.json` in parent directories can confuse Turbopack workspace root detection.
