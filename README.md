# MasterGenAIInstructions

Personal agent operating system for AI-assisted development. Bootstrap new projects with Cursor rules, portable AGENTS.md, and workflow protocols pre-loaded so agents work your way from commit zero.

## What's In Here

```
MasterGenAIInstructions/
|-- bootstrap.ps1        # PowerShell: create a new project
|-- bootstrap.sh         # Bash: create a new project
|-- manager.pyw          # Double-click GUI manager (Python/tkinter)
|-- apply.ps1            # PowerShell: apply rules to an existing project
|-- apply.sh             # Bash: apply rules to an existing project
|-- update-all.ps1       # PowerShell: push rule updates to all registered projects
|-- registry.json        # List of projects using these rules
|-- template/            # Everything below gets copied into new projects
|   |-- .cursor/rules/   # 15 Cursor rule files (ponytail always on)
|   |-- AGENTS.md        # Portable playbook for non-Cursor environments
|   |-- DECISION-LOG.md  # Template for autonomous decisions
|   |-- TESTING-STRATEGY.md
|   |-- HANDOFF.md
|   |-- .gitignore
|   |-- README.md        # Project README template
|-- _meta/
    |-- PHILOSOPHY.md    # Why this system exists
```

## Quick Start

### GUI Manager (recommended)

Double-click `manager.pyw` to open the GUI. It has tabs for:
- **New Project** -- create a bootstrapped project with all rules
- **Apply to Existing** -- add rules to an existing project
- **Update All** -- push rule changes to every registered project
- **Registry** -- view and manage registered projects

Requires Python 3 (uses tkinter, no extra installs).

### Command Line: Starting a New Project

```powershell
# PowerShell
.\bootstrap.ps1
```

```bash
# Bash
./bootstrap.sh
```

The script will ask for:
1. Project name
2. Description
3. Destination directory (default: current directory)
4. Whether to create a private GitHub repo

It copies the template files, replaces placeholders, initializes git, and optionally creates and pushes to a GitHub repo.

### What You Get

A new project directory with:
- **14 Cursor rule files** covering vocabulary, workflow, ponytail (always-on minimalism), git discipline, clean code, review gates, autonomous mode, testing, code walkthroughs, rebuild/redesign/hotfix protocols, deploy awareness, and session handoff.
- **AGENTS.md** -- same rules in portable format for Claude Code, Codex, or any AI tool.
- **DECISION-LOG.md**, **TESTING-STRATEGY.md**, **HANDOFF.md** -- seeded templates ready to use.
- Proper `.gitignore`.

### Applying to an Existing Project

```powershell
# PowerShell
.\apply.ps1 -TargetDir "C:\path\to\existing\project"
```

```bash
# Bash
./apply.sh /path/to/existing/project
```

This copies the 14 rule files and AGENTS.md into the project. It creates DECISION-LOG.md, TESTING-STRATEGY.md, and HANDOFF.md only if they don't already exist. It never touches your README.md, .gitignore, or any project code.

### After Bootstrapping or Applying

1. Open the new project in Cursor.
2. Fill in `deploy-awareness.mdc` with your deploy targets.
3. Start building -- agents already know your workflow.

## Rule Files

### Always-On (7 files, loaded every session)

| File | Purpose |
|---|---|
| `vocabulary.mdc` | Command words + protocol index |
| `workflow.mdc` | Core principles, tone, onboarding, security |
| `ponytail.mdc` | Always-on lazy senior-dev posture (YAGNI, ladder, anti-bloat, anti-slop); conflict protocol vs other rules |
| `codegraph.mdc` | Always-on CodeGraph MCP usage (deterministic graph; hybrid A+B parent/subagent pattern) |
| `git-discipline.mdc` | Branching, commits, push behavior |
| `clean-code.mdc` | Code quality, naming, anti-AI-slop, dependencies |
| `code-walkthrough.mdc` | File-level plain-English documentation |
| `deploy-awareness.mdc` | Project-specific deploy config (template) |

### Load on Demand

| File | Trigger |
|---|---|
| `review-protocol.mdc` | Phase complete, review, production merge |
| `autonomous-mode.mdc` | "run autonomously" / decision logging |
| `testing-protocol.mdc` | Writing tests |
| `subagents.mdc` | Spawning any subagent |
| `rebuild-protocol.mdc` | User says "rebuild" |
| `redesign-protocol.mdc` | User says "redesign" |
| `hotfix-protocol.mdc` | User says "hotfix" or "production is broken" |
| `cleanup-protocol.mdc` | User says "cleanup" or "clean up the codebase" |
| `session-handoff.mdc` | End of session or context limit |

Conflict playbook (human reference, not auto-loaded): `_meta/RULE-CONFLICTS.md`.

## Updating Rules Across All Projects

When you edit a rule in this repo, push the changes to all registered projects:

```powershell
.\update-all.ps1
```

This copies the updated `.cursor/rules/` and `AGENTS.md` to every project in `registry.json`. It will offer to commit the changes in each project. Projects that no longer exist are automatically removed from the registry.

## Using Without Cursor

`AGENTS.md` in each bootstrapped project contains the same rules in portable format. It works with Claude Code, Codex, or any AI tool that reads project docs.
