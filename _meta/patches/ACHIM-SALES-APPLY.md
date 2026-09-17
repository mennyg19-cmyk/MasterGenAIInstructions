# Apply walkthrough + CodeGraph to AchimSales

This Cloud Agent (MasterGenAIInstructions) **cannot push** to `mennyg19-cmyk/AchimSales` (GitHub 403 — no write permission on that repo).

## Option A (recommended): Cloud Agent *on* AchimSales

1. Open https://cursor.com/agents and start a Cloud Agent **in the AchimSales repo**
2. Paste:

```
Apply the walkthrough + CodeGraph patch from MasterGenAIInstructions.
Repo: mennyg19-cmyk/MasterGenAIInstructions
File: _meta/patches/achim-sales-walkthrough-codegraph.patch
Branch to create: cursor/walkthrough-luna-codegraph-120f
Base: main
Then open a PR.

Preserve deploy-awareness.mdc Azure targets. Do not wipe project-specific git-discipline PR rules.
```

## Option B: apply the patch locally / in any clone with write access

```bash
git clone https://github.com/mennyg19-cmyk/AchimSales.git
cd AchimSales
git checkout -b cursor/walkthrough-luna-codegraph-120f
curl -fsSL https://raw.githubusercontent.com/mennyg19-cmyk/MasterGenAIInstructions/cursor/model-routing-spec-gate-120f/_meta/patches/achim-sales-walkthrough-codegraph.patch | git am
git push -u origin cursor/walkthrough-luna-codegraph-120f
gh pr create --base main --fill
```

(If the MasterGenAIInstructions branch isn’t merged yet, use that branch’s raw URL or copy the patch file from the PR.)

## What the patch adds

- `walkthrough-protocol.mdc` (Luna-only teaching tour)
- vocabulary / subagents / codegraph / AGENTS updates
- README Rule Preferences row
- `.cursor/environment.json`, `install.sh`, `run-dev.sh` (Cloud Agent bootstrap from pending env PR #40) + CodeGraph install step
- `.gitignore` allows those `.cursor` env files

After merge: rebuild Cloud Agent environment snapshot, start agent as **GPT-5.6 Luna**, say `walkthrough`.
