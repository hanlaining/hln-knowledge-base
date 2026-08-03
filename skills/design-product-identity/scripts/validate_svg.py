#!/usr/bin/env python3
"""Validate a production logo SVG for structure and unsafe content."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET


def local_name(value: str) -> str:
    return value.rsplit("}", 1)[-1].lower()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("svg")
    return parser.parse_args()


def validate(path: Path) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        raw = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return {"ok": False, "path": str(path), "errors": [str(exc)], "warnings": []}
    if "<!DOCTYPE" in raw.upper() or "<!ENTITY" in raw.upper():
        errors.append("DOCTYPE and ENTITY declarations are not allowed")
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        errors.append(f"Invalid XML: {exc}")
        return {"ok": False, "path": str(path), "errors": errors, "warnings": warnings}
    if local_name(root.tag) != "svg":
        errors.append("Root element must be svg")
    view_box = root.attrib.get("viewBox") or root.attrib.get("viewbox")
    if not view_box:
        errors.append("SVG must define viewBox")
    elif len(re.findall(r"-?[0-9]+(?:\.[0-9]+)?", view_box)) != 4:
        errors.append("viewBox must contain four numeric values")
    if "width" not in root.attrib or "height" not in root.attrib:
        warnings.append("width and height are recommended for predictable exports")

    node_count = 0
    for node in root.iter():
        node_count += 1
        name = local_name(node.tag)
        if name in {"script", "foreignobject", "iframe", "object", "embed"}:
            errors.append(f"Unsafe or non-vector element is not allowed: {name}")
        if name == "image":
            errors.append("Embedded or linked raster image is not allowed in a production logo SVG")
        for attribute, value in node.attrib.items():
            attr_name = local_name(attribute)
            lowered = value.strip().lower()
            if attr_name.startswith("on"):
                errors.append(f"Event handler attribute is not allowed: {attr_name}")
            if attr_name in {"href", "src"} and lowered and not lowered.startswith("#"):
                errors.append(f"External or data reference is not allowed: {attr_name}")
            if "javascript:" in lowered:
                errors.append("javascript URL is not allowed")
    return {
        "ok": not errors,
        "path": str(path),
        "viewBox": view_box,
        "nodeCount": node_count,
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
    }


def main() -> int:
    args = parse_args()
    result = validate(Path(args.svg).expanduser().resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
