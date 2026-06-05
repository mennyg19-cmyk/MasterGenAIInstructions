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
