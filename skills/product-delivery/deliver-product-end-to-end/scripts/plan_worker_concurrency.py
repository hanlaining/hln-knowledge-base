#!/usr/bin/env python3
"""Plan incremental worker launches from resource snapshots and ready issues."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Optional


def load_json(path: str) -> Any:
    return json.loads(Path(path).expanduser().resolve().read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", required=True)
    parser.add_argument("--candidates", required=True)
    parser.add_argument("--previous-snapshot")
    parser.add_argument("--ramp-step", type=int, default=1)
    parser.add_argument("--review-backlog", type=int, default=0)
    parser.add_argument("--red-load-per-cpu", type=float, default=1.50)
    parser.add_argument("--yellow-load-per-cpu", type=float, default=0.90)
    parser.add_argument("--red-memory-free", type=float, default=5.0)
    parser.add_argument("--yellow-memory-free", type=float, default=15.0)
    parser.add_argument("--red-disk-free", type=float, default=5.0)
    parser.add_argument("--yellow-disk-free", type=float, default=10.0)
    parser.add_argument("--yellow-swap-growth-mb", type=float, default=512.0)
    return parser.parse_args()


def number(value: Any) -> Optional[float]:
    return float(value) if isinstance(value, (int, float)) else None


def classify(snapshot: dict[str, Any], previous: Optional[dict[str, Any]], args: argparse.Namespace) -> tuple[str, list[str]]:
    reasons: list[str] = []
    red = False
    yellow = False
    load = number(snapshot.get("cpu", {}).get("load1PerLogicalCpu"))
    memory_free = number(snapshot.get("memory", {}).get("freePercent"))
    disk_free = number(snapshot.get("disk", {}).get("freePercent"))
    swap_used = number(snapshot.get("memory", {}).get("swapUsedMB"))
    previous_swap = number(previous.get("memory", {}).get("swapUsedMB")) if previous else None

    if load is not None:
        if load >= args.red_load_per_cpu:
            red, reasons = True, reasons + [f"load_per_cpu={load:.2f} reached red threshold"]
        elif load >= args.yellow_load_per_cpu:
            yellow, reasons = True, reasons + [f"load_per_cpu={load:.2f} reached yellow threshold"]
    if memory_free is not None:
        if memory_free <= args.red_memory_free:
            red, reasons = True, reasons + [f"memory_free={memory_free:.1f}% reached red threshold"]
        elif memory_free <= args.yellow_memory_free:
            yellow, reasons = True, reasons + [f"memory_free={memory_free:.1f}% reached yellow threshold"]
    if disk_free is not None:
        if disk_free <= args.red_disk_free:
            red, reasons = True, reasons + [f"disk_free={disk_free:.1f}% reached red threshold"]
        elif disk_free <= args.yellow_disk_free:
            yellow, reasons = True, reasons + [f"disk_free={disk_free:.1f}% reached yellow threshold"]
    if swap_used is not None and previous_swap is not None:
        growth = swap_used - previous_swap
        if growth >= args.yellow_swap_growth_mb:
            yellow, reasons = True, reasons + [f"swap grew by {growth:.1f} MB"]
    thermal = snapshot.get("thermal", {})
    for key in ("cpuSpeedLimit", "schedulerLimit"):
        limit = number(thermal.get(key))
        if limit is not None and limit < 70:
            red, reasons = True, reasons + [f"{key}={limit:.0f}%"]
        elif limit is not None and limit < 90:
            yellow, reasons = True, reasons + [f"{key}={limit:.0f}%"]
    if args.review_backlog >= 3:
        yellow, reasons = True, reasons + [f"review backlog={args.review_backlog}"]

    if red:
        return "RED", reasons
    if yellow:
        return "YELLOW", reasons
    return "GREEN", reasons or ["resource signals are within configured thresholds"]


def select_candidates(payload: Any, state: str, ramp_step: int) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    if isinstance(payload, list):
        candidates = payload
        active_ids: set[str] = set()
        active_scopes: set[str] = set()
    elif isinstance(payload, dict):
        candidates = payload.get("candidates", [])
        active_ids = {str(value) for value in payload.get("activeIssueIds", [])}
        active_scopes = {str(value) for value in payload.get("activeWriteScopes", [])}
    else:
        raise ValueError("Candidates JSON must be an array or object")
    if not isinstance(candidates, list):
        raise ValueError("candidates must be an array")

    selected: list[dict[str, Any]] = []
    rejected: list[dict[str, str]] = []
    selected_scopes: set[str] = set()
    heavy_selected = False
    ordered = sorted(
        (item for item in candidates if isinstance(item, dict)),
        key=lambda item: (-int(item.get("priority", 0)), str(item.get("id", ""))),
    )
    for item in ordered:
        issue_id = str(item.get("id", ""))
        resource_class = str(item.get("resourceClass", "medium"))
        scopes = {str(value) for value in item.get("writeScopes", [])}
        if not issue_id:
            rejected.append({"id": "<missing>", "reason": "missing issue id"})
            continue
        if issue_id in active_ids:
            rejected.append({"id": issue_id, "reason": "already active"})
            continue
        if not bool(item.get("ready", True)) or not bool(item.get("authorized", True)):
            rejected.append({"id": issue_id, "reason": "not ready or not authorized"})
            continue
        if scopes & (active_scopes | selected_scopes):
            rejected.append({"id": issue_id, "reason": "write scope conflict"})
            continue
        if state == "RED":
            rejected.append({"id": issue_id, "reason": "resource state RED"})
            continue
        if state == "YELLOW" and resource_class != "light":
            rejected.append({"id": issue_id, "reason": "YELLOW only allows light work"})
            continue
        if resource_class == "heavy" and heavy_selected:
            rejected.append({"id": issue_id, "reason": "only one new heavy worker per ramp"})
            continue
        if len(selected) >= max(0, ramp_step):
            rejected.append({"id": issue_id, "reason": "incremental ramp step reached"})
            continue
        selected.append(item)
        selected_scopes.update(scopes)
        heavy_selected = heavy_selected or resource_class == "heavy"
    return selected, rejected


def main() -> int:
    args = parse_args()
    try:
        if args.ramp_step < 0:
            raise ValueError("ramp-step must be zero or greater")
        snapshot = load_json(args.snapshot)
        previous = load_json(args.previous_snapshot) if args.previous_snapshot else None
        payload = load_json(args.candidates)
        state, reasons = classify(snapshot, previous, args)
        selected, rejected = select_candidates(payload, state, args.ramp_step)
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 1
    result = {
        "ok": True,
        "resourceState": state,
        "hardLimit": None,
        "rampStep": args.ramp_step,
        "launch": selected,
        "rejected": rejected,
        "reasons": reasons,
        "note": "This plan does not authorize work or override Graph/file ownership checks.",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
