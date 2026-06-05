# Rebuild Retro #2 — Decision Log (autonomous session)

Mining the Tomche Shabbos rebuild transcript (ebf0b06c, now 2580 lines / 113 subagents) to harden the rules after the second rebuild attempt "missed a lot." User is away; working autonomously per `autonomous-mode.mdc`.

## High-signal findings from the parent transcript (confirmed by me)

1. **Wrong/outdated model slugs in the rules.** The rebuild protocol lists `claude-opus-4-8-thinking-high` (INVALID) and only 3 families. Real available slugs: `claude-4.5-opus-high-thinking`, `claude-4.6-opus-max-thinking`, `claude-4.6-sonnet-medium-thinking`, `claude-opus-4-8-thinking-xhigh`, `composer-2.5-fast`, `gemini-3.1-pro`, `gpt-5.2-codex`, `gpt-5.5-extra-high`, `grok-4.3`, `grok-build-0.1`, `kimi-k2.5`. User explicitly named families: gemini, opus, codex, sonnet, grok, kimi (line 2087). An invalid slug makes a subagent fall back to the parent model — silently defeating multi-model coverage.

2. **Agent claimed builds passed without checking** (lines 2035 "check yourself to make sure they passed", 2049 "check again", 1964 "vercel and github are coming back bad", 2014 "both failed"). Post-commit build verification existed as a rule but the agent didn't self-trigger it.

3. **Redesign protocol ignored** (line 2066): user expected multiple subagents on different models each building a viewable homepage proposal to pick from; agent built one itself. Redesign protocol needs the same mechanical hardening rebuild got (how to spawn, exact slugs, produce viewable previews, don't do it yourself).

4. **Pixel-identical over-correction confirmed as wrong** (lines 1509, 1515) — already addressed in the reframe, keep.

5. **Entire feature area silently dropped despite being in the inventory** (user, this session): the ENTIRE order builder was captured in FEATURE-INVENTORY.md but never built — and BOTH the main agent AND the reviewer missed it. Root cause: nothing mechanically reconciles "every inventory line" against "what was actually built and verified in the running app." The review sampled instead of enumerating. "There may even be more" — so the inventory-to-build reconciliation must be exhaustive and line-by-line, no sampling, with evidence (route + interaction/screenshot) per line. Build is NOT done while any inventory line lacks a verified status.

6. **Review must loop until clean** (user, this session; also originally requested line 1518 "check again until the check is clean" — NOT enforced). One review pass is not enough. After the main agent fixes a review's findings, a FRESH review agent (different model, no prior context so it can't rubber-stamp its own work) must run again. Repeat until a review returns ZERO findings. "Done" is forbidden until a clean review pass exists.

## Decisions
- Fix model slugs across ALL rules; list the full current roster and instruct to use the `model` param + verify the slug is valid (fall back = bug).
- Harden redesign-protocol mechanically (mirror rebuild's "how to spawn" + "do not do it yourself" + viewable previews).
- Strengthen post-commit build verification into a self-triggered, mandatory gate (agent checks without being told).
- Await deep-miner subagents (Claude/GPT/Composer) for the full issue list before finalizing.

## Round 2 — deep-miner findings folded in (Claude miner returned an exhaustive report)

The transcript was not one rebuild but four overlapping attempts, each "missed a lot." Additional recurring root causes and the rules that now address them:

- **Weak local build gate.** `tsc`+lint passed but `next build`/Turbopack failed (a `"use client"` file imported a server-only module) and CI failed on Prettier. Fix landed only on a feature branch while prod built `main`. → deploy-awareness: full gate now requires `prettier --check` + real `next build` + `import "server-only"` guards, and **re-run the whole gate after every batch of fixes**.
- **"Should pass" without verifying.** Agent declared CI green without checking; user had to say "check yourself"/"check again." → deploy-awareness: "should pass" banned; observe and quote real status.
- **"Done" ≠ visible online.** A redesign was "done" on an unmerged branch, not deployed, not visible; preview builds dead because env vars were Production-scope only. → deploy-awareness: "Done = merged to deploy branch + READY + live with data"; env-scope parity rule.
- **DB issues.** Rebuild deployed against the OLD populated DB → `/admin` 500. Empty dev DB read as "page broken" / a falsely "verified" page. Pervasive schema↔code field-name drift (code written from memory of a redesigned schema). → deploy-awareness: fresh isolated DB branch for rebuilds; read schema before coding an entity; "empty 200 is not working" (seed first); smoke deploy must hit an authenticated page against the real DB.
- **Coarse parallel subagents.** A "phase" covering 2+ pages was handed to one background subagent → stubs merged, parity never checked. → rebuild Phase 4.1: one page per subagent max; parent verifies each in the running app.
- **Reviews substituted by compile checks.** Agent concluded reviews "timed out," declared done from zero TS errors; the completed reviews had found broken API wiring + stub mutations + security gaps. → review-protocol: a review must RETURN RESULTS; on timeout, re-spawn smaller; never substitute "it compiles"; no idle-poll-then-declare-done.
- **Committing junk + deferring cleanup.** A 24MB PNG, PDFs, and a temp commit-message file got committed; cleanup deferred against the user's explicit instruction. → git-discipline: never commit temp/build artifacts, keep heavy assets/previews out of the repo, stage explicitly, clean up in real time.
- **Scope + brand churn.** Plan said "port pixel-identical," forcing two re-scopes; redesign copy drifted from the brand. → rebuild plan must state WHAT-not-HOW (no "port"); redesign Phase 0 captures a brand brief.

## Round 3 — GPT + Composer miner findings (genuinely new gaps)

All three miners completed. GPT (subagent-log mining) and Composer (keyword sweep) confirmed the above and added:

- **Security reviewed by file, not by trust boundary** → real holes shipped (public checkout marking an order paid by cash/check, setup creating a dev with no secret, permission overrides accepting arbitrary keys, draft creation trusting client-supplied IDs). → review-protocol: mandatory trust-boundary review (actor + auth proof, server-side validation, server-derived money/role/ownership, side effects, abuse test) for anything touching payments/auth/roles/orders.
- **Domain invariants drifted** (donations, delivery counts) between audit/plan/build. → review-protocol: invariant ledger; reviews cite invariant IDs.
- **Model diversity unverifiable** — proposals self-labeled their model. → subagents.mdc: orchestrator records the real assigned model on each artifact; self-labels prove nothing.
- **Plan contradicted the canonical audit** (split finalizePOS the audit said didn't exist). → rebuild Phase 3: contradictions resolved explicitly (canonical wins / intentionally differs / needs approval).
- **To-fix items weren't gated** like features. → rebuild Phase 1: to-fix items get `F#` IDs, accounted for KEEP/FIX/DROP in the ledger.
- **Integration DB tests silently skipped / hit the wrong DB** (global prisma singleton → localhost; RUN_DB_IT off by default). → testing-protocol: isolated test DB; flag-gated DB tests must be ON in the gate that decides "done."

## Decisions
