#!/usr/bin/env python3
"""Validate and sync model slug assignments from _meta/model-roster.json.

Canonical data: _meta/model-roster.json
Human-facing rules: .cursor/rules/subagents.mdc (auto-synced table sections)
Protocols name jobs; JSON + subagents pick slugs.

Usage:
  python lib/model-roster.py check     # exit 1 on drift or unknown slugs
  python lib/model-roster.py sync      # rewrite marked sections in subagents.mdc
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROSTER_JSON = ROOT / "_meta" / "model-roster.json"
SUBAGENT_PATHS = [
    ROOT / ".cursor" / "rules" / "subagents.mdc",
    ROOT / "template" / ".cursor" / "rules" / "subagents.mdc",
]
RULE_GLOBS = [
    ROOT / ".cursor" / "rules",
    ROOT / "template" / ".cursor" / "rules",
]
MARKERS = {
    "roster": ("<!-- MODEL_ROSTER:BEGIN -->", "<!-- MODEL_ROSTER:END -->"),
    "tiers": ("<!-- MODEL_TIERS:BEGIN -->", "<!-- MODEL_TIERS:END -->"),
    "jobs": ("<!-- MODEL_JOBS:BEGIN -->", "<!-- MODEL_JOBS:END -->"),
}
SLUG_RE = re.compile(r"`([a-z0-9][a-z0-9.\-]+)`")


def load_roster() -> dict:
    with ROSTER_JSON.open(encoding="utf-8") as f:
        return json.load(f)


def all_slugs(data: dict) -> set[str]:
    slugs = {entry["slug"] for entry in data["roster"]}
    for tier in data["tiers"].values():
        slugs.update(tier["slugs"])
    for job in data["jobs"]:
        slugs.update(job["slugs"])
    for key in ("routine_review", "go_live_review"):
        slugs.update(data[key].values())
    slugs.discard("")
    return slugs


def render_roster_table(data: dict) -> str:
    lines = [
        "| Slug | Family / role |",
        "|---|---|",
    ]
    for entry in data["roster"]:
        lines.append(f"| `{entry['slug']}` | {entry['family']} ({entry['role']}) |")
    return "\n".join(lines)


def render_tiers_table(data: dict) -> str:
    lines = [
        "| Tier | Slugs | Use for |",
        "|---|---|---|",
    ]
    for key in ("premier", "everyday", "cheap"):
        tier = data["tiers"][key]
        slug_list = ", ".join(f"`{s}`" for s in tier["slugs"])
        lines.append(f"| **{tier['label']}** | {slug_list} | {tier['use_for']} |")
    gpt_note = (
        "GPT-5.6: **Sol** > **Terra** > **Luna** (if spawnable). "
        "Task currently accepts Sol/Terra at **medium** only. Fable replaces Opus; **medium only**."
    )
    ui = (
        f"**Recommended Cursor UI default (human):** `{data['ui_default_slug']}` ({data['ui_default_label']}). "
        "GPT is the primary family for Everyday work. Sonnet is the deliberate second family for dual-pass review. "
        "**Do not use Auto** as the main agent — Auto can silent-route mid-protocol and defeat Job routing."
    )
    return "\n".join(lines) + "\n\n" + gpt_note + "\n\n" + ui


def render_jobs_table(data: dict) -> str:
    lines = [
        "| Job | Slug(s) |",
        "|---|---|",
    ]
    for job in data["jobs"]:
        if job["slugs"]:
            slug_cell = "; ".join(f"`{s}`" for s in job["slugs"])
        else:
            slug_cell = "CodeGraph — not a model contest"
        lines.append(f"| **{job['job']}** | {slug_cell} |")
    routing = (
        "**Routing rule:** hard-to-reverse judgment → Premier (Sol/Fable); "
        "everyday build + routine gates → Terra/Sonnet; cheap/wide/long → Grok or Composer-fast; "
        "design competition → Gemini + Everyday (+ Premier if user asks); facts → CodeGraph. "
        "**Harden with Spec gate + expectation checklists** so Everyday can replace Premier on thumbtack work."
    )
    return "\n".join(lines) + "\n\n" + routing


def replace_marked_section(content: str, begin: str, end: str, body: str) -> str:
    pattern = re.compile(re.escape(begin) + r".*?" + re.escape(end), re.DOTALL)
    replacement = f"{begin}\n{body}\n{end}"
    if not pattern.search(content):
        raise ValueError(f"Markers not found: {begin} ... {end}")
    return pattern.sub(replacement, content, count=1)


def sync_subagents(data: dict) -> list[str]:
    changed: list[str] = []
    roster_body = render_roster_table(data)
    tiers_body = render_tiers_table(data)
    jobs_body = render_jobs_table(data)

    for path in SUBAGENT_PATHS:
        if not path.exists():
            continue
        original = path.read_text(encoding="utf-8")
        updated = original
        updated = replace_marked_section(updated, *MARKERS["roster"], roster_body)
        updated = replace_marked_section(updated, *MARKERS["tiers"], tiers_body)
        updated = replace_marked_section(updated, *MARKERS["jobs"], jobs_body)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed.append(str(path.relative_to(ROOT)))
    return changed


def extract_marked(content: str, begin: str, end: str) -> str | None:
    pattern = re.compile(re.escape(begin) + r"\n(.*)\n" + re.escape(end), re.DOTALL)
    match = pattern.search(content)
    return match.group(1).strip() if match else None


def check_subagents_sync(data: dict) -> list[str]:
    errors: list[str] = []
    expected = {
        "roster": render_roster_table(data),
        "tiers": render_tiers_table(data),
        "jobs": render_jobs_table(data),
    }
    for path in SUBAGENT_PATHS:
        if not path.exists():
            errors.append(f"missing {path.relative_to(ROOT)}")
            continue
        content = path.read_text(encoding="utf-8")
        for name, (begin, end) in MARKERS.items():
            actual = extract_marked(content, begin, end)
            if actual is None:
                errors.append(f"{path.relative_to(ROOT)}: missing {name} markers")
                continue
            if actual != expected[name]:
                errors.append(
                    f"{path.relative_to(ROOT)}: {name} section out of sync — run: python lib/model-roster.py sync"
                )
    return errors


def scan_rule_slugs(known: set[str]) -> list[str]:
    errors: list[str] = []
    ignore_files = {"subagents.mdc"}
    for rules_dir in RULE_GLOBS:
        if not rules_dir.exists():
            continue
        for path in sorted(rules_dir.glob("*.mdc")):
            if path.name in ignore_files:
                continue
            text = path.read_text(encoding="utf-8")
            for slug in SLUG_RE.findall(text):
                if slug in known:
                    continue
                if slug.endswith(".mdc") or slug.startswith("gpt-") is False and "medium" not in slug and "fast" not in slug and "codex" not in slug and "gemini" not in slug and "grok" not in slug and "composer" not in slug and "claude" not in slug and "fable" not in slug and "sonnet" not in slug and "sol" not in slug and "terra" not in slug:
                    continue
                if any(part in slug for part in ("workflow", "protocol", "scratch", "codegraph", "ponytail")):
                    continue
                if slug not in known:
                    errors.append(f"{path.relative_to(ROOT)}: unknown model slug `{slug}`")
    return errors


def cmd_check() -> int:
    data = load_roster()
    known = all_slugs(data)
    errors: list[str] = []
    errors.extend(check_subagents_sync(data))
    errors.extend(scan_rule_slugs(known))

    if errors:
        print("model-roster check FAILED:")
        for err in errors:
            print(f"  - {err}")
        print("\nFix: edit _meta/model-roster.json, then run: python lib/model-roster.py sync")
        return 1

    print(f"model-roster check OK ({len(known)} slugs, version {data['version']})")
    return 0


def cmd_sync() -> int:
    data = load_roster()
    changed = sync_subagents(data)
    if changed:
        print("Synced subagents.mdc sections from _meta/model-roster.json:")
        for path in changed:
            print(f"  - {path}")
    else:
        print("subagents.mdc already in sync with _meta/model-roster.json")
    return cmd_check()


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in {"check", "sync"}:
        print(__doc__.strip())
        return 2
    if sys.argv[1] == "check":
        return cmd_check()
    return cmd_sync()


if __name__ == "__main__":
    raise SystemExit(main())
