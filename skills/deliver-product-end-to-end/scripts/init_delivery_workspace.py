#!/usr/bin/env python3
"""Initialize a non-destructive .product-delivery state directory."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, help="Existing project root")
    return parser.parse_args()


def safe_project_root(raw: str) -> Path:
    root = Path(raw).expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"Project root does not exist or is not a directory: {root}")
    if root == Path("/") or root == Path.home().resolve():
        raise ValueError("Refusing to initialize a broad filesystem or home-directory target")
    return root


def copy_templates(root: Path) -> dict[str, object]:
    skill_root = Path(__file__).resolve().parent.parent
    template_root = skill_root / "assets" / "project-state"
    if not template_root.is_dir():
        raise ValueError(f"Template directory is missing: {template_root}")

    target_root = root / ".product-delivery"
    target_root.mkdir(mode=0o755, exist_ok=True)
    (target_root / "runtime").mkdir(mode=0o755, exist_ok=True)

    created: list[str] = []
    skipped: list[str] = []
    for source in sorted(template_root.rglob("*")):
        relative = source.relative_to(template_root)
        target = target_root / relative
        if source.is_dir():
            target.mkdir(mode=0o755, parents=True, exist_ok=True)
            continue
        target.parent.mkdir(mode=0o755, parents=True, exist_ok=True)
        if target.exists():
            skipped.append(str(relative))
            continue
        shutil.copy2(source, target)
        created.append(str(relative))

    return {
        "root": str(root),
        "stateDirectory": str(target_root),
        "created": created,
        "skippedExisting": skipped,
        "overwritten": [],
    }


def main() -> int:
    args = parse_args()
    try:
        result = copy_templates(safe_project_root(args.root))
    except (OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps({"ok": True, **result}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
