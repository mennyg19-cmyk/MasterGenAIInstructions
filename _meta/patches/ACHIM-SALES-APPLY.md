# Apply rules to AchimSales (Cloud Agent → `main`)

Canonical instructions + full repo list: **`_meta/CLOUD-APPLY.md`**.

## Prompt (AchimSales Cloud Agent)

Model: **Composer 2.5 Standard**. Paste:

```text
Apply the latest MasterGenAIInstructions agent rules into this repo and land them on main.

Source: github.com/mennyg19-cmyk/MasterGenAIInstructions (branch main)
Copy from that repo:
- template/.cursor/rules/* → this repo’s .cursor/rules/
- template/AGENTS.md → this repo’s AGENTS.md
- Merge CodeGraph install steps from template/.cursor/environment.json into this repo’s .cursor/environment.json (create if missing)

Do NOT overwrite .cursor/rules/deploy-awareness.mdc (keep Azure targets).
Do NOT wipe project-specific git-discipline / deploy notes.

Work on a short-lived branch if needed, then MERGE into main. Do not leave an open draft PR — finish with rules on main.
Confirm main has Composer UI default / Grok implement / Sonnet Loop B / Opus premier, and walkthrough hard-locked to Composer 2.5 Standard.
```

After merge: rebuild the Cloud Agent environment snapshot if `environment.json` changed, then start agents as **Composer 2.5 Standard**.
