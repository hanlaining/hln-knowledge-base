#!/usr/bin/env python3
"""Validate product-delivery state, traceability, and Graph issue contracts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any


STAGES = {
    "DISCOVERY",
    "PRODUCT_CONFIRMED",
    "STRUCTURE_APPROVED",
    "BRAND_AND_VISUAL_APPROVED",
    "FIGMA_PROTOTYPE_APPROVED",
    "TECH_PLAN_APPROVED",
    "CONTRACT_APPROVED",
    "BACKEND_FOUNDATION_PASSED",
    "FRONTEND_AND_BACKEND_IMPLEMENTED",
    "INTEGRATION_PASSED",
    "ACCEPTANCE_PASSED",
    "USER_ACCEPTED",
}
ISSUE_STATES = {
    "pending",
    "ready",
    "running",
    "review",
    "blocked",
    "passed",
    "failed",
    "deferred",
}
REQUIREMENT_RE = re.compile(
    r"^##\s+(R\d{2,})\s+\[(confirmed|inferred|unknown|conflict)\]\s+(.+)$",
    re.MULTILINE,
)
ACCEPTANCE_RE = re.compile(r"^##\s+(AC\d{2,})\s+(.+)$", re.MULTILINE)
RELATED_RE = re.compile(r"^[-*]\s*Related requirements:\s*(.+)$", re.MULTILINE)
STATUS_RE = re.compile(r"^[-*]\s*Status:\s*(\w+)", re.MULTILINE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, help="Project root")
    return parser.parse_args()


def load_json(path: Path, errors: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"Missing required file: {path}")
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid JSON in {path}: line {exc.lineno}, column {exc.colno}")
    return None


def sections(text: str, matches: list[re.Match[str]]) -> dict[str, str]:
    result: dict[str, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        result[match.group(1)] = text[match.start() : end]
    return result


def validate_markdown(state_root: Path, errors: list[str], warnings: list[str]) -> tuple[dict[str, str], dict[str, dict[str, Any]]]:
    req_path = state_root / "requirements.md"
    ac_path = state_root / "acceptance.md"
    try:
        req_text = req_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        errors.append(f"Missing required file: {req_path}")
        req_text = ""
    try:
        ac_text = ac_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        errors.append(f"Missing required file: {ac_path}")
        ac_text = ""

    requirement_matches = list(REQUIREMENT_RE.finditer(req_text))
    requirements: dict[str, str] = {}
    for match in requirement_matches:
        req_id, status = match.group(1), match.group(2)
        if req_id in requirements:
            errors.append(f"Duplicate requirement id: {req_id}")
        requirements[req_id] = status

    acceptance_matches = list(ACCEPTANCE_RE.finditer(ac_text))
    acceptance_sections = sections(ac_text, acceptance_matches)
    acceptance: dict[str, dict[str, Any]] = {}
    mapped_requirements: set[str] = set()
    for match in acceptance_matches:
        ac_id = match.group(1)
        if ac_id in acceptance:
            errors.append(f"Duplicate acceptance id: {ac_id}")
            continue
        body = acceptance_sections[ac_id]
        related_match = RELATED_RE.search(body)
        status_match = STATUS_RE.search(body)
        related = re.findall(r"R\d{2,}", related_match.group(1)) if related_match else []
        status = status_match.group(1).lower() if status_match else ""
        if not related:
            errors.append(f"{ac_id} has no Related requirements")
        if not status:
            errors.append(f"{ac_id} has no Status")
        for req_id in related:
            mapped_requirements.add(req_id)
            if req_id not in requirements:
                errors.append(f"{ac_id} references unknown requirement {req_id}")
        acceptance[ac_id] = {"related": related, "status": status}

    for req_id, status in requirements.items():
        if status == "confirmed" and req_id not in mapped_requirements:
            errors.append(f"Confirmed requirement {req_id} is not mapped to an AC")

    evidence_path = state_root / "evidence" / "index.md"
    evidence_text = evidence_path.read_text(encoding="utf-8") if evidence_path.exists() else ""
    if not evidence_path.exists():
        errors.append(f"Missing required file: {evidence_path}")
    for ac_id, data in acceptance.items():
        if data["status"] == "passed" and ac_id not in evidence_text:
            errors.append(f"Passed acceptance {ac_id} has no evidence index entry")

    if not requirements:
        warnings.append("No Rxx requirements recorded yet")
    if not acceptance:
        warnings.append("No ACxx acceptance cases recorded yet")
    return requirements, acceptance


def validate_graph(graph: Any, requirements: dict[str, str], acceptance: dict[str, dict[str, Any]], errors: list[str]) -> int:
    if not isinstance(graph, dict) or not isinstance(graph.get("issues"), list):
        errors.append("graph.json must contain an issues array")
        return 0
    required = {
        "id",
        "title",
        "state",
        "requirements",
        "acceptanceCases",
        "dependsOn",
        "blocks",
        "produces",
        "validates",
        "owner",
        "worker",
        "worktree",
        "allowedFiles",
        "forbiddenFiles",
        "resourceClass",
        "evidence",
    }
    seen: set[str] = set()
    for issue in graph["issues"]:
        if not isinstance(issue, dict):
            errors.append("Every graph issue must be an object")
            continue
        issue_id = str(issue.get("id", "<missing>"))
        missing = sorted(required - set(issue))
        if missing:
            errors.append(f"{issue_id} missing fields: {', '.join(missing)}")
        if issue_id in seen:
            errors.append(f"Duplicate graph issue id: {issue_id}")
        seen.add(issue_id)
        if issue.get("state") not in ISSUE_STATES:
            errors.append(f"{issue_id} has invalid state: {issue.get('state')}")
        if issue.get("resourceClass") not in {"light", "medium", "heavy"}:
            errors.append(f"{issue_id} has invalid resourceClass")
        worktree = issue.get("worktree")
        if worktree and not Path(str(worktree)).is_absolute():
            errors.append(f"{issue_id} worktree must be absolute when set")
        for req_id in issue.get("requirements", []):
            if req_id not in requirements:
                errors.append(f"{issue_id} references unknown requirement {req_id}")
        for ac_id in issue.get("acceptanceCases", []):
            if ac_id not in acceptance:
                errors.append(f"{issue_id} references unknown acceptance case {ac_id}")
    return len(graph["issues"])


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    state_root = root / ".product-delivery"
    errors: list[str] = []
    warnings: list[str] = []
    if root == Path("/") or root == Path.home().resolve():
        errors.append("Refusing a broad filesystem or home-directory target")
    if not state_root.is_dir():
        errors.append(f"Missing state directory: {state_root}")

    manifest = load_json(state_root / "manifest.json", errors)
    graph = load_json(state_root / "graph.json", errors)
    if isinstance(manifest, dict):
        if manifest.get("stage") not in STAGES:
            errors.append(f"Invalid manifest stage: {manifest.get('stage')}")
        approved = manifest.get("approvedStages")
        if not isinstance(approved, list) or any(item not in STAGES for item in approved):
            errors.append("manifest approvedStages must be a list of valid stages")
    elif manifest is not None:
        errors.append("manifest.json must contain an object")

    requirements, acceptance = validate_markdown(state_root, errors, warnings)
    issue_count = validate_graph(graph, requirements, acceptance, errors) if graph is not None else 0
    result = {
        "ok": not errors,
        "root": str(root),
        "stage": manifest.get("stage") if isinstance(manifest, dict) else None,
        "counts": {"requirements": len(requirements), "acceptanceCases": len(acceptance), "issues": issue_count},
        "warnings": warnings,
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
