# Rule Context — the incidents behind the rules

The rules in `template/` are deliberately terse. This file preserves the real failures that
produced them, so future rule edits don't accidentally delete a hard-won lesson. This file is
NOT shipped to projects and is never loaded by agents during normal work.

## Rebuild failures

- **~75% of UI features silently dropped** in an early rebuild. Source of: "every feature survives,"
  stable inventory IDs, route manifest, enumerated (never sampled) reviews.
- **An entire page (the order builder) shipped missing** while both builder and reviewer overlooked
  it — the review sampled instead of enumerating. Source of: route-coverage diff first, per-ID
  ledger, PRESENT/PARTIAL/STUB/MISSING with evidence.
- **Engine with no car**: beautiful backend, read-only skeleton pages. Source of: "UI and internals
  built together," no-stubs rule.
- **"Port every page" framing** caused the user to re-scope mid-stream twice. Source of: "old app is
  the reference for WHAT exists, not HOW to build it."
- **A converged plan invented behavior the real app didn't have** (separate finalize paths). Source
  of: "canonical audit wins" conflict-resolution rule.
- **One model converged two proposals by silently picking a winner.** Source of: debate-to-consensus
  loop; same models defend their own proposals.

## Subagent failures

- **A "multi-model" audit silently ran on one model the whole time** — a rejected slug led the agent
  to drop the `model` param and fall back to itself. Source of: "never fall back to your own model."
- **Self-labeled artifacts proved nothing** ("by Claude Opus" bylines on files whose real model was
  unknown). Source of: orchestrator stamps the assigned model on every artifact.
- **Stateless debate rounds lost the thread** — models reopened settled points. Source of: feed the
  full running DEBATE-LOG every round.

## Review failures

- **Reviewer timed out → agent declared done from the compile check** — shipped broken API wiring,
  stub mutations, and security gaps the completed review had caught. Source of: "a review must
  return results."
- **Security reviewed file-by-file missed real holes**: public offline-checkout could mark orders
  paid, setup created a developer account with no secret, permission overrides accepted arbitrary
  keys, public draft creation trusted client-supplied product/option/add-on IDs. Source of:
  trust-boundary review by entry point.
- **Invariants drifted between audit, proposals, and build** (donation handling, delivery stop
  counts) and caused bugs. Source of: the invariant ledger.
- **Review cadence contradiction**: git-discipline said push every change, rebuild-protocol said
  review before every commit — the agent picked the lax reading and pushed unreviewed code.
  Source of: review-protocol owns cadence; fast checks per commit, loop at phase/production gates.

## Deploy failures

- **Eight straight ERROR preview deploys went unnoticed** (ZmanimRebuild): the rebuild dropped the
  monorepo but Vercel's Root Directory still said `apps/web`; local builds and tests were green the
  whole time. Source of: platform-green verification, "structure changes require platform-settings
  changes," smoke-deploy hard gate.
- **"Should pass" while the build was red** forced the user to repeatedly say "check yourself."
  Source of: observe-and-quote-the-real-status rule.
- **Server/client boundary violation** (`"use client"` importing a server-only module) passed tsc
  and shipped a red Vercel build. Source of: run the real production build locally; `server-only`.
- **Production deployed from `fresh-start` while `main` was abandoned code.** Source of: never
  assume `main` is production; document branch strategy.
- **A "done" redesign sat on an unmerged branch, invisible online**; fixes landed on a feature
  branch while prod kept building `main`. Source of: "done = visible online."
- **`prisma db push --accept-data-loss` in a build script** — the single most dangerous recurring
  issue; can drop columns on every deploy. Source of: database deploy rules.
- **A rebuild pointed at the old populated DB** — schema mismatch 500'd `/admin` on first load.
  Source of: fresh isolated DB for rebuilds.
- **Code written against an imagined schema** caused dozens of stacked CI failures. Source of: read
  `schema.prisma` before coding against an entity.
- **Env var present only in Production scope killed every Preview build.** Source of: check scope,
  not just presence.
- **Missing Clerk middleware crashed deploys; missing sign-in pages 404'd.** Source of: auth
  completeness checklist.
- **"Verified" order builder was broken on an empty dev DB** — page loaded an empty 200 and was
  called done. Source of: an empty 200 is not working; seed then verify.
- **Tests silently hit `localhost` dev DB instead of the test schema** — green run proved nothing.
  Source of: test DB isolation; flag-gated DB tests must be ON in the done-gate.

## Git/process failures

- **A temp commit-message file got committed** into an app repo; **a 24MB PNG got merged**. Source
  of: don't-commit-junk rules, `.scratch/` convention.
- **Deferred cleanup that was explicitly requested never happened.** Source of: clean up in real
  time.
- **PowerShell BOM** broke Prisma migrations/JSON parsers; **stray parent lockfile** confused
  Turbopack root detection; build output piped through Select-String lost errors. Source of: the
  Windows/PowerShell section.

## Redesign failures

- **The agent designed one homepage itself** instead of spawning competing models — the user had to
  stop it ("did you read the protocol?"). Source of: "you do NOT design it yourself."
- **Generated copy muddled what the product actually was** — the user had to correct it. Source of:
  the brand/domain brief in discovery.
