# Apply walkthrough + CodeGraph to AchimSales

This Cloud Agent (MasterGenAIInstructions) **cannot push** to `mennyg19-cmyk/AchimSales` (GitHub 403 — no write permission on that repo).

**Model note (2026-10-13):** Walkthrough is now **Composer 2.5 Standard** (not Luna). Prefer copying current rules from this repo over the older `achim-sales-walkthrough-codegraph.patch` (that patch still mentions Luna/Terra).

## Option A (recommended): Cloud Agent *on* AchimSales

1. Open https://cursor.com/agents and start a Cloud Agent **in the AchimSales repo** (model: **Composer 2.5 Standard**)
2. Paste:

```
Copy codebase walkthrough + model routing + CodeGraph cloud install from MasterGenAIInstructions into this repo.

Source repo: mennyg19-cmyk/MasterGenAIInstructions
Branch: cursor/composer-grok-claude-routing-120f (or main once merged)

Copy at least:
- .cursor/rules/walkthrough-protocol.mdc
- .cursor/rules/subagents.mdc (Job tables)
- .cursor/rules/vocabulary.mdc (walkthrough triggers)
- .cursor/rules/review-protocol.mdc
- .cursor/rules/workflow.mdc (Spec gate + model routing lines)
- AGENTS.md model-routing bullets
- Merge CodeGraph install into .cursor/environment.json (see MasterGenAIInstructions template/.cursor/environment.json)

Preserve deploy-awareness.mdc Azure targets. Do not wipe project-specific git-discipline PR rules.
UI default / walkthrough = Composer 2.5 Standard. Then open a PR.
```

Fresh file copies also live under `_meta/patches/achim-sales-files/` in MasterGenAIInstructions (walkthrough at least).

## Option B: apply locally / in any clone with write access

```bash
git clone https://github.com/mennyg19-cmyk/AchimSales.git
cd AchimSales
git checkout -b cursor/walkthrough-composer-codegraph-120f
# Prefer file copy from MasterGenAIInstructions (current Composer routing), not the legacy .patch
git push -u origin cursor/walkthrough-composer-codegraph-120f
```

## What you should end up with

- `walkthrough-protocol.mdc` (**Composer 2.5 Standard** hard lock)
- vocabulary / subagents / review / workflow / AGENTS updates for Composer + Grok + Sonnet + Opus
- CodeGraph on Cloud Agents via environment `install`
- README Rule Preferences row if the project keeps one

After merge: rebuild Cloud Agent environment snapshot, start agent as **Composer 2.5 Standard**, say `walkthrough`.
