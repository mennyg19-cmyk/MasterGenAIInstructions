# Apply MasterGenAI rules via Cloud Agents (into `main`)

Source of truth: **`mennyg19-cmyk/MasterGenAIInstructions` `main`** (Composer orchestrator + Grok/Sonnet/Opus routing).

`update-all.ps1` only works on your Windows machine (local `registry.json` paths). For GitHub repos, run **one Cloud Agent per target repo**.

## Prompt (paste into each target repo’s Cloud Agent)

Use model **Composer 2.5 Standard**. Paste:

```text
Apply the latest MasterGenAIInstructions agent rules into this repo and land them on main.

Source: github.com/mennyg19-cmyk/MasterGenAIInstructions (branch main)
Copy from that repo:
- template/.cursor/rules/* → this repo’s .cursor/rules/
- template/AGENTS.md → this repo’s AGENTS.md
- If this repo uses Cloud Agents: merge CodeGraph install steps from template/.cursor/environment.json into this repo’s .cursor/environment.json (create it if missing)

Do NOT overwrite .cursor/rules/deploy-awareness.mdc (project-owned).
Do NOT wipe project-specific git-discipline / deploy notes.

Work on a short-lived branch if needed, then MERGE into main (squash or merge commit OK). Do not leave an open draft PR — finish with rules on main.
After merge: confirm main has the new subagents Job table (Composer UI default, Grok implement, Sonnet Loop B, Opus premier) and walkthrough-protocol hard-locked to Composer 2.5 Standard.
```

## Repos to apply (GitHub — Cloud Agent)

Do these via [cursor.com/agents](https://cursor.com/agents) (one agent each):

| Repo | URL | Notes |
|---|---|---|
| **AchimSales** | https://github.com/mennyg19-cmyk/AchimSales | Cloud agents; keep Azure deploy-awareness |
| **MenEZmanim** | https://github.com/mennyg19-cmyk/MenEZmanim | In local registry |
| **Tomchei-Shabbos-Website** | https://github.com/mennyg19-cmyk/Tomchei-Shabbos-Website | Matches Tomche paths in registry |
| **allprobuildingsupplies** | https://github.com/mennyg19-cmyk/allprobuildingsupplies | |
| **achim-cron-ping** | https://github.com/mennyg19-cmyk/achim-cron-ping | Small; still stamp AGENTS/rules if agents touch it |
| **model-duel-menezmanim** | https://github.com/mennyg19-cmyk/model-duel-menezmanim | Optional if you still use agents here |
| **master-model-duel** | https://github.com/mennyg19-cmyk/master-model-duel | Optional if you still use agents here |

**Skip (not app rule targets):**

| Repo | Why |
|---|---|
| MasterGenAIInstructions | Already updated (source) |
| ponytail | Upstream tool fork |
| codegraph | Upstream tool fork |

## Local-only paths (`registry.json` — use PC `update-all`)

These are registered locally; many are **not** in the GitHub org list. Stamp with:

```powershell
cd <path-to-MasterGenAIInstructions>
git checkout main
git pull
.\update-all.ps1 -AutoCommit
```

| Registry path |
|---|
| `C:\Users\Menny\Documents\Family\Tomche Shabbos 6-3-26\Tomche Shabbos Website` |
| `D:\Projects\Others\Tomche Shabbos Website` |
| `D:\Projects\Personal\ZmanimRebuild` |
| `D:\Projects\Others\MenEZmanim` |
| `D:\Projects\Others\StepSupporter` |
| `C:\Users\Menny\OneDrive - Achim Importing Co., Inc\Achim Importing Co., Inc. Team Site - D365 F&O\scripts` |
| `C:\Users\Menny\Documents\Personal\Program\App` |
| `C:\Users\Menny\Documents\Family\Tomchei Shabbos Shopify` |
| `C:\Users\Menny\Documents\Family\Tomche-website-rebuild-gpt` |
| `C:\Users\Menny\Documents\Family\Tomche-website-rebuild-opus` |
| `C:\Users\Menny\Documents\Personal\Program\App\Daily12Stepper` |
| `C:\Users\Menny\Documents\Personal\Program\App\DailyPlanner` |
| `C:\Users\Menny\Documents\Personal\Program\App\GenMap` |
| `C:\Users\Menny\Documents\Personal\Program\App\JustForToday` |
| `C:\Users\Menny\Documents\Personal\Program\App\JustForTodayNew` |
| `C:\Users\Menny\Documents\Personal\Program\App\LifeTrackPro-Clean` |
| `C:\Users\Menny\Documents\Personal\Program\App\MasterGenAIInstructions` |
| `C:\Users\Menny\Documents\Personal\Program\App\zmanim-app` |
| `C:\Users\Menny\Documents\Personal\Program\App\zmanim-app-v2` |

After any apply: set Cursor UI model to **Composer 2.5 Standard**.
