#!/usr/bin/env python3
"""Validate, sync, and refresh Cursor model assignments.

Canonical job→slug data: _meta/model-roster.json
Synced human tables: .cursor/rules/subagents.mdc (and template twin)
Live catalog sources (in order):
  1. CURSOR_API_KEY → GET https://api.cursor.com/v1/models
  2. cursor-agent --list-models / agent models (if on PATH)
  3. --catalog-file PATH (offline / CI artifact)

Usage:
  python lib/model-roster.py check
  python lib/model-roster.py sync
  python lib/model-roster.py fetch [--catalog-file PATH]
  python lib/model-roster.py diff  [--catalog-file PATH] [--json]
  python lib/model-roster.py report [--catalog-file PATH] [--out PATH]

diff/report exit codes:
  0 = assigned slugs all present; no actionable catalog delta
  1 = roster/sync failure (check)
  2 = missing assigned slugs OR notable new catalog models (needs human review)
  3 = could not fetch a catalog (auth / network / no CLI)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
ROSTER_JSON = ROOT / "_meta" / "model-roster.json"
CATALOG_LATEST = ROOT / "_meta" / "model-catalog-latest.json"
CATALOG_SNAPSHOT = ROOT / "_meta" / "model-catalog-snapshot.json"
REPORT_DEFAULT = ROOT / ".scratch" / "model-roster-report.md"
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
CURSOR_MODELS_URL = "https://api.cursor.com/v1/models"

# Families we care about when surfacing "new models"
INTERESTING_PREFIXES = (
    "gpt-",
    "claude-",
    "composer-",
    "gemini-",
    "grok-",
    "cursor-grok-",
    "kimi-",
    "glm-",
)


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
                if any(
                    part in slug
                    for part in (
                        "workflow",
                        "protocol",
                        "scratch",
                        "codegraph",
                        "ponytail",
                        ".mdc",
                    )
                ):
                    continue
                looks_modelish = any(
                    tok in slug
                    for tok in (
                        "gpt-",
                        "claude-",
                        "composer-",
                        "gemini-",
                        "grok-",
                        "codex",
                        "fable",
                        "sonnet",
                        "sol-",
                        "terra-",
                        "luna-",
                        "-medium",
                        "-fast",
                        "-high",
                    )
                )
                if looks_modelish and slug not in known:
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


def _basic_auth_header(api_key: str) -> str:
    import base64

    token = base64.b64encode(f"{api_key}:".encode()).decode()
    return f"Basic {token}"


def fetch_catalog_from_api(api_key: str) -> dict[str, Any]:
    req = urllib.request.Request(
        CURSOR_MODELS_URL,
        headers={
            "Authorization": _basic_auth_header(api_key),
            "Accept": "application/json",
            "User-Agent": "MasterGenAIInstructions-model-roster/1.0",
        },
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        payload = json.loads(resp.read().decode())
    items = payload.get("items") or payload.get("models") or []
    models: list[dict[str, Any]] = []
    for item in items:
        mid = item.get("id") or item.get("modelId")
        if not mid:
            continue
        models.append(
            {
                "id": mid,
                "displayName": item.get("displayName") or mid,
                "aliases": item.get("aliases") or [],
                "description": item.get("description") or "",
            }
        )
    return {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "source": "api.cursor.com/v1/models",
        "models": sorted(models, key=lambda m: m["id"]),
    }


def fetch_catalog_from_cli() -> dict[str, Any] | None:
    candidates = [
        ["cursor-agent", "--list-models"],
        ["cursor-agent", "models"],
        ["agent", "models"],
        ["agent", "--list-models"],
    ]
    for cmd in candidates:
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
        if proc.returncode != 0:
            continue
        text = (proc.stdout or "").strip()
        if not text:
            continue
        models = parse_cli_model_list(text)
        if models:
            return {
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "source": " ".join(cmd),
                "models": models,
            }
    return None


def parse_cli_model_list(text: str) -> list[dict[str, Any]]:
    """Parse `cursor-agent --list-models` / `agent models` text or JSON."""
    text = text.strip()
    if text.startswith("{") or text.startswith("["):
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            payload = None
        if isinstance(payload, list):
            return [
                {"id": m if isinstance(m, str) else m.get("id"), "displayName": m if isinstance(m, str) else m.get("displayName", m.get("id")), "aliases": [], "description": ""}
                for m in payload
                if (isinstance(m, str) or m.get("id"))
            ]
        if isinstance(payload, dict):
            items = payload.get("items") or payload.get("models") or []
            return [
                {
                    "id": m.get("id"),
                    "displayName": m.get("displayName") or m.get("id"),
                    "aliases": m.get("aliases") or [],
                    "description": m.get("description") or "",
                }
                for m in items
                if m.get("id")
            ]

    models: list[dict[str, Any]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.lower().startswith("available") or line.startswith("#"):
            continue
        # Formats like: "gpt-5.6-terra-medium  GPT Terra (current)" or "  - gpt-5.6-terra-medium"
        line = re.sub(r"^[\-\*\d\.\)]\s*", "", line)
        m = re.match(r"`?([a-z0-9][a-z0-9.\-]+)`?", line)
        if not m:
            continue
        slug = m.group(1)
        if any(x in slug for x in ("http", "cursor.com", "github")):
            continue
        if not any(slug.startswith(p) for p in INTERESTING_PREFIXES) and "-" not in slug:
            continue
        rest = line[m.end() :].strip(" -:|()")
        models.append(
            {
                "id": slug,
                "displayName": rest or slug,
                "aliases": [],
                "description": "",
            }
        )
    # de-dupe
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for model in models:
        if model["id"] in seen:
            continue
        seen.add(model["id"])
        out.append(model)
    return sorted(out, key=lambda m: m["id"])


def load_catalog_file(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if "models" not in payload:
        raise ValueError(f"{path} missing 'models' array")
    return payload


def get_catalog(catalog_file: Path | None = None) -> dict[str, Any]:
    if catalog_file:
        return load_catalog_file(catalog_file)

    api_key = os.environ.get("CURSOR_API_KEY") or os.environ.get("CURSOR_CLOUD_API_KEY")
    if api_key:
        return fetch_catalog_from_api(api_key)

    cli = fetch_catalog_from_cli()
    if cli:
        return cli

    if CATALOG_LATEST.exists():
        print(
            "WARN: no API key / CLI — using last saved _meta/model-catalog-latest.json",
            file=sys.stderr,
        )
        return load_catalog_file(CATALOG_LATEST)

    raise RuntimeError(
        "No model catalog available. Set CURSOR_API_KEY, install cursor-agent, "
        "or pass --catalog-file."
    )


def catalog_ids(catalog: dict[str, Any]) -> set[str]:
    ids: set[str] = set()
    for model in catalog.get("models", []):
        mid = model.get("id")
        if mid:
            ids.add(mid)
        for alias in model.get("aliases") or []:
            ids.add(alias)
    return ids


def is_interesting(slug: str) -> bool:
    return any(slug.startswith(p) for p in INTERESTING_PREFIXES)


def suggest_replacements(missing: str, available: set[str]) -> list[str]:
    """Heuristic cousins for a missing assigned slug (human still decides)."""
    parts = missing.split("-")
    stems = []
    if "terra" in missing:
        stems.append("terra")
    if "sol" in missing:
        stems.append("sol")
    if "fable" in missing:
        stems.append("fable")
    if "sonnet" in missing:
        stems.append("sonnet")
    if "composer" in missing:
        stems.append("composer")
    if "grok" in missing:
        stems.append("grok")
    if "gemini" in missing:
        stems.append("gemini")
    if "codex" in missing:
        stems.append("codex")
    if missing.startswith("gpt-"):
        stems.append("gpt-")
    if missing.startswith("claude-"):
        stems.append("claude-")

    scored: list[tuple[int, str]] = []
    for cand in available:
        score = 0
        for stem in stems:
            if stem in cand:
                score += 2
        # prefer same effort keywords
        for effort in ("medium", "fast", "high", "thinking"):
            if effort in missing and effort in cand:
                score += 1
        if score:
            scored.append((score, cand))
    scored.sort(key=lambda x: (-x[0], x[1]))
    return [c for _, c in scored[:8]]


def build_diff(roster: dict, catalog: dict[str, Any]) -> dict[str, Any]:
    assigned = sorted(all_slugs(roster))
    available = catalog_ids(catalog)
    missing = sorted(s for s in assigned if s not in available)
    present = sorted(s for s in assigned if s in available)

    prev_ids: set[str] = set()
    if CATALOG_SNAPSHOT.exists():
        try:
            prev = load_catalog_file(CATALOG_SNAPSHOT)
            prev_ids = catalog_ids(prev)
        except (OSError, ValueError, json.JSONDecodeError):
            prev_ids = set()

    # First snapshotless run: do not flood with "everything is new" — only check assigned.
    if prev_ids:
        new_interesting = sorted(
            s for s in available if is_interesting(s) and s not in prev_ids and s not in assigned
        )
        gone_interesting = sorted(s for s in prev_ids if is_interesting(s) and s not in available)
    else:
        new_interesting = []
        gone_interesting = []

    suggestions = {m: suggest_replacements(m, available) for m in missing}

    actionable = bool(missing) or bool(new_interesting)
    return {
        "fetched_at": catalog.get("fetched_at"),
        "source": catalog.get("source"),
        "catalog_count": len(available),
        "assigned_count": len(assigned),
        "assigned_present": present,
        "assigned_missing": missing,
        "suggestions": suggestions,
        "new_interesting": new_interesting[:40],
        "gone_interesting": gone_interesting[:40],
        "actionable": actionable,
        "roster_version": roster.get("version"),
    }


def write_report_md(diff: dict[str, Any], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# Model roster report — {date.today().isoformat()}",
        "",
        f"Source: `{diff.get('source')}` at `{diff.get('fetched_at')}`",
        f"Catalog models: **{diff.get('catalog_count')}** · Assigned slugs: **{diff.get('assigned_count')}** · Roster version: `{diff.get('roster_version')}`",
        "",
    ]
    if diff["assigned_missing"]:
        lines.append("## Assigned slugs missing from Cursor catalog")
        lines.append("")
        lines.append("These Job-table slugs are no longer returned by the catalog. Update `_meta/model-roster.json`.")
        lines.append("")
        for slug in diff["assigned_missing"]:
            tips = diff["suggestions"].get(slug) or []
            tip = ", ".join(f"`{t}`" for t in tips) if tips else "_none found_"
            lines.append(f"- `{slug}` — suggested cousins: {tip}")
        lines.append("")
    else:
        lines.append("## Assigned slugs")
        lines.append("")
        lines.append("All assigned roster slugs are present in the catalog.")
        lines.append("")

    if diff["new_interesting"]:
        lines.append("## New interesting models since last snapshot")
        lines.append("")
        for slug in diff["new_interesting"]:
            lines.append(f"- `{slug}`")
        lines.append("")
        lines.append(
            "Human decision: map any of these into Everyday / Premier / Cheap jobs if they replace Terra/Sol/Fable/Sonnet."
        )
        lines.append("")

    if diff["gone_interesting"]:
        lines.append("## Interesting models gone since last snapshot")
        lines.append("")
        for slug in diff["gone_interesting"]:
            lines.append(f"- `{slug}`")
        lines.append("")

    lines.extend(
        [
            "## What to do next",
            "",
            "1. Edit `_meta/model-roster.json` (Job assignment is a judgment call — do not auto-remap).",
            "2. `python lib/model-roster.py sync`",
            "3. `python lib/model-roster.py check`",
            "4. Commit this MasterGenAIInstructions repo.",
            "5. On your Windows machine: `.\\update-all.ps1 -AutoCommit` to push rules into every registered app.",
            "6. Optionally refresh the snapshot: copy `_meta/model-catalog-latest.json` → `_meta/model-catalog-snapshot.json`.",
            "",
        ]
    )
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def cmd_fetch(catalog_file: Path | None) -> int:
    try:
        catalog = get_catalog(catalog_file)
    except Exception as exc:  # noqa: BLE001 — CLI surface
        print(f"fetch FAILED: {exc}", file=sys.stderr)
        return 3
    CATALOG_LATEST.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    print(
        f"Fetched {len(catalog.get('models', []))} models from {catalog.get('source')} → {_rel(CATALOG_LATEST)}"
    )
    return 0


def cmd_diff(catalog_file: Path | None, as_json: bool) -> int:
    try:
        catalog = get_catalog(catalog_file)
    except Exception as exc:  # noqa: BLE001
        print(f"diff FAILED: {exc}", file=sys.stderr)
        return 3
    CATALOG_LATEST.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    roster = load_roster()
    diff = build_diff(roster, catalog)
    if as_json:
        print(json.dumps(diff, indent=2))
    else:
        print(f"source={diff['source']} catalog={diff['catalog_count']} assigned={diff['assigned_count']}")
        if diff["assigned_missing"]:
            print("MISSING assigned:")
            for slug in diff["assigned_missing"]:
                tips = ", ".join(diff["suggestions"].get(slug) or [])
                print(f"  - {slug}  (cousins: {tips or 'none'})")
        else:
            print("All assigned slugs present.")
        if diff["new_interesting"]:
            print(f"NEW interesting ({len(diff['new_interesting'])}):")
            for slug in diff["new_interesting"][:20]:
                print(f"  - {slug}")
        print("ACTIONABLE" if diff["actionable"] else "OK — no roster action required")
    return 2 if diff["actionable"] else 0


def cmd_report(catalog_file: Path | None, out: Path) -> int:
    try:
        catalog = get_catalog(catalog_file)
    except Exception as exc:  # noqa: BLE001
        print(f"report FAILED: {exc}", file=sys.stderr)
        return 3
    CATALOG_LATEST.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    roster = load_roster()
    diff = build_diff(roster, catalog)
    write_report_md(diff, out)
    print(f"Wrote { _rel(out) }")
    print("ACTIONABLE" if diff["actionable"] else "OK — no roster action required")
    return 2 if diff["actionable"] else 0


def _rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "command",
        choices=["check", "sync", "fetch", "diff", "report"],
        help="check|sync|fetch|diff|report",
    )
    parser.add_argument("--catalog-file", type=Path, help="Offline catalog JSON")
    parser.add_argument("--json", action="store_true", help="JSON output for diff")
    parser.add_argument("--out", type=Path, default=REPORT_DEFAULT, help="Report markdown path")
    args = parser.parse_args()

    if args.command == "check":
        return cmd_check()
    if args.command == "sync":
        return cmd_sync()
    if args.command == "fetch":
        return cmd_fetch(args.catalog_file)
    if args.command == "diff":
        return cmd_diff(args.catalog_file, args.json)
    if args.command == "report":
        return cmd_report(args.catalog_file, args.out)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
