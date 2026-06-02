# MasterGenAIInstructions

Personal agent operating system for AI-assisted development. Bootstrap new projects with Cursor rules, portable AGENTS.md, and workflow protocols pre-loaded so agents work your way from commit zero.

## What's In Here

```
MasterGenAIInstructions/
|-- bootstrap.ps1        # PowerShell scaffolder (primary)
|-- bootstrap.sh         # Bash version (cross-platform)
|-- template/            # Everything below gets copied into new projects
|   |-- .cursor/rules/   # 13 Cursor rule files
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

### Starting a New Project

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
- **13 Cursor rule files** covering vocabulary, workflow, git discipline, clean code, review gates, autonomous mode, testing, code walkthroughs, rebuild/redesign/hotfix protocols, deploy awareness, and session handoff.
- **AGENTS.md** -- same rules in portable format for Claude Code, Codex, or any AI tool.
- **DECISION-LOG.md**, **TESTING-STRATEGY.md**, **HANDOFF.md** -- seeded templates ready to use.
- Proper `.gitignore`.

### After Bootstrapping

1. Open the new project in Cursor.
2. Fill in `deploy-awareness.mdc` with your deploy targets.
3. Start building -- agents already know your workflow.

## Rule Files

### Always-On (9 files, loaded every session)

| File | Purpose |
|---|---|
| `vocabulary.mdc` | What every command word means |
| `workflow.mdc` | Core principles, tone, onboarding, security |
| `git-discipline.mdc` | Branching, commits, push behavior |
| `clean-code.mdc` | Code quality, naming, anti-AI-slop, dependencies |
| `review-protocol.mdc` | When and how to use review subagents |
| `autonomous-mode.mdc` | Unattended operation rules |
| `testing-protocol.mdc` | Testing strategy alongside code |
| `code-walkthrough.mdc` | File-level plain-English documentation |
| `deploy-awareness.mdc` | Project-specific deploy config (template) |

### Triggered by Description (4 files, loaded when relevant)

| File | Trigger |
|---|---|
| `rebuild-protocol.mdc` | User says "rebuild" |
| `redesign-protocol.mdc` | User says "redesign" |
| `hotfix-protocol.mdc` | User says "hotfix" or "production is broken" |
| `session-handoff.mdc` | End of session or context limit |

## Updating the Template

Edit rule files in this repo. New projects bootstrapped afterward get the latest rules. Existing projects keep their copy -- edit those in-place if needed.

## Using Without Cursor

`AGENTS.md` in each bootstrapped project contains the same rules in portable format. It works with Claude Code, Codex, or any AI tool that reads project docs.
