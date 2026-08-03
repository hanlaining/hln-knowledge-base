#!/usr/bin/env python3
"""Collect a compact, non-sensitive macOS resource snapshot for scheduling."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Optional


def run_text(command: list[str], timeout: float = 3.0) -> Optional[str]:
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def sysctl_int(name: str) -> Optional[int]:
    text = run_text(["sysctl", "-n", name])
    try:
        return int(text) if text is not None else None
    except ValueError:
        return None


def memory_snapshot() -> dict[str, object]:
    total = sysctl_int("hw.memsize")
    free_percent: Optional[float] = None
    pressure = run_text(["memory_pressure", "-Q"])
    if pressure:
        match = re.search(r"free percentage:\s*([0-9.]+)%", pressure, re.IGNORECASE)
        if match:
            free_percent = float(match.group(1))

    swap_total_mb: Optional[float] = None
    swap_used_mb: Optional[float] = None
    swap = run_text(["sysctl", "-n", "vm.swapusage"])
    if swap:
        total_match = re.search(r"total\s*=\s*([0-9.]+)([MG])", swap)
        used_match = re.search(r"used\s*=\s*([0-9.]+)([MG])", swap)

        def to_mb(match: Optional[re.Match[str]]) -> Optional[float]:
            if not match:
                return None
            value = float(match.group(1))
            return value * 1024 if match.group(2) == "G" else value

        swap_total_mb = to_mb(total_match)
        swap_used_mb = to_mb(used_match)

    return {
        "totalBytes": total,
        "freePercent": free_percent,
        "swapTotalMB": swap_total_mb,
        "swapUsedMB": swap_used_mb,
    }


def process_counts() -> dict[str, int]:
    output = run_text(["ps", "-axo", "comm="])
    counts = {"claude": 0, "browser": 0, "build": 0, "database": 0, "test": 0}
    if not output:
        return counts
    for raw in output.splitlines():
        name = Path(raw.strip()).name.lower()
        if "claude" in name:
            counts["claude"] += 1
        if name in {"chromium", "google chrome", "playwright", "webkit"} or "chrome" in name:
            counts["browser"] += 1
        if name in {"cargo", "rustc", "xcodebuild", "gradle", "webpack", "vite", "tsc"}:
            counts["build"] += 1
        if name in {"postgres", "mysqld", "redis-server", "mongod"}:
            counts["database"] += 1
        if name in {"pytest", "jest", "vitest", "go", "mvn"}:
            counts["test"] += 1
    return counts


def thermal_snapshot() -> dict[str, Optional[int]]:
    output = run_text(["pmset", "-g", "therm"])
    result: dict[str, Optional[int]] = {"cpuSpeedLimit": None, "schedulerLimit": None}
    if not output:
        return result
    for key, target in (("CPU_Speed_Limit", "cpuSpeedLimit"), ("Scheduler_Limit", "schedulerLimit")):
        match = re.search(rf"{key}\s*=\s*(\d+)", output)
        if match:
            result[target] = int(match.group(1))
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", default=".", help="Filesystem path used for disk capacity")
    parser.add_argument("--output", help="Optional JSON output path")
    parser.add_argument("--overwrite", action="store_true", help="Explicitly replace an existing JSON snapshot")
    return parser.parse_args()


def write_snapshot(raw_output: str, text: str, overwrite: bool) -> None:
    requested = Path(raw_output).expanduser()
    if requested.is_symlink():
        raise ValueError(f"Refusing symlink output target: {requested}")
    output = requested.resolve()
    if output in {Path("/"), Path.home().resolve()} or output.is_dir():
        raise ValueError(f"Refusing broad or directory output target: {output}")
    if output.suffix.lower() != ".json":
        raise ValueError("Snapshot output must use a .json filename")
    if (output.exists() or output.is_symlink()) and not overwrite:
        raise ValueError(f"Refusing to overwrite existing snapshot without --overwrite: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    if temporary.exists() or temporary.is_symlink():
        raise ValueError(f"Refusing to reuse existing temporary path: {temporary}")
    temporary.write_text(text + "\n", encoding="utf-8")
    temporary.replace(output)


def main() -> int:
    args = parse_args()
    check_path = Path(args.path).expanduser().resolve()
    if not check_path.exists():
        print(json.dumps({"ok": False, "error": f"Path does not exist: {check_path}"}))
        return 1
    cpu_count = os.cpu_count() or 1
    try:
        load1, load5, load15 = os.getloadavg()
    except OSError:
        load1 = load5 = load15 = 0.0
    disk = shutil.disk_usage(check_path)
    snapshot = {
        "schemaVersion": 1,
        "capturedAt": datetime.now(timezone.utc).isoformat(),
        "platform": sys.platform,
        "cpu": {
            "logicalCount": cpu_count,
            "load1": round(load1, 3),
            "load5": round(load5, 3),
            "load15": round(load15, 3),
            "load1PerLogicalCpu": round(load1 / cpu_count, 3),
        },
        "memory": memory_snapshot(),
        "disk": {
            "path": str(check_path),
            "totalBytes": disk.total,
            "freeBytes": disk.free,
            "freePercent": round(disk.free / disk.total * 100, 2) if disk.total else None,
        },
        "thermal": thermal_snapshot(),
        "processCounts": process_counts(),
    }
    text = json.dumps(snapshot, ensure_ascii=False, indent=2)
    try:
        if args.output:
            write_snapshot(args.output, text, args.overwrite)
        else:
            print(text)
    except (OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
