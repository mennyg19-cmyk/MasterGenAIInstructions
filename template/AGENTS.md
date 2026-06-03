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
| **rebuild** | Multi-agent rebuild of internals. UI stays pixel-identical. See Rebuild Protocol. |
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

## Rebuild Protocol

See `rebuild-protocol.mdc` for the full 6-phase multi-agent workflow. Summary: multi-model audit + chat history mining (find past bugs, late additions, pain points), feature inventory cross-referenced against build history, architecture proposals from premier agents, debate and converge into a granular plan (every screen, route, component, endpoint gets its own todo -- general todos are a failure), build todo-by-todo with review gates, final scope review. UI stays pixel-identical. Everything technical is on the table (framework, language, hosting, packages) unless the user says otherwise.

---

## Redesign Protocol

See `redesign-protocol.mdc` for the full 6-phase workflow. Summary: discovery conversation about pain points, UX audit, multiple design proposals from different models with visual HTML previews the user can open in a browser to compare side by side, user review and iteration, phased build, final review. Everything visual/frontend is on the table (CSS framework, component library, layout approach) unless the user says otherwise.

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

Project-specific. See `deploy-awareness.mdc` for this project's deploy targets, trigger files, commands, and post-deploy checks.
