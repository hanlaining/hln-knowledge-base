#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT_DIR = Path(__file__).resolve().parent


class DeliveryScriptsTest(unittest.TestCase):
    def run_script(self, name: str, *args: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, str(SCRIPT_DIR / name), *args],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def test_initialize_and_validate_empty_state(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "project"
            root.mkdir()
            first = self.run_script("init_delivery_workspace.py", "--root", str(root))
            self.assertTrue(json.loads(first.stdout)["ok"])
            second = self.run_script("init_delivery_workspace.py", "--root", str(root))
            self.assertTrue(json.loads(second.stdout)["skippedExisting"])
            manifest = json.loads((root / ".product-delivery" / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["schemaVersion"], 2)
            self.assertEqual(manifest["approvalPolicy"], "INTERACTIVE")
            validated = self.run_script("validate_delivery_state.py", "--root", str(root))
            payload = json.loads(validated.stdout)
            self.assertTrue(payload["ok"])
            self.assertIn("No Rxx requirements recorded yet", payload["warnings"])

    def test_traceability_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "project"
            root.mkdir()
            self.run_script("init_delivery_workspace.py", "--root", str(root))
            requirements = root / ".product-delivery" / "requirements.md"
            requirements.write_text("# 产品需求\n\n## R01 [confirmed] 必须可见\n", encoding="utf-8")
            result = self.run_script("validate_delivery_state.py", "--root", str(root), expected=1)
            self.assertIn("Confirmed requirement R01 is not mapped", result.stdout)

    def test_delegated_approval_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "project"
            root.mkdir()
            self.run_script("init_delivery_workspace.py", "--root", str(root))
            state_root = root / ".product-delivery"
            (state_root / "requirements.md").write_text(
                "# 产品需求\n\n## R01 [confirmed] 提醒快过期食材\n",
                encoding="utf-8",
            )
            (state_root / "acceptance.md").write_text(
                "# 验收\n\n## AC01 快过期提醒可见\n\n- Related requirements: R01\n- Status: draft\n",
                encoding="utf-8",
            )
            manifest_path = state_root / "manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest.update(
                {
                    "stage": "PRODUCT_CONFIRMED",
                    "approvedStages": ["PRODUCT_CONFIRMED"],
                    "approvalPolicy": "DELEGATED_SUPERVISOR",
                    "delegatedScope": ["PRODUCT_CONFIRMED"],
                    "reservedUserActions": ["USER_ACCEPTED"],
                    "stageApprovals": {
                        "PRODUCT_CONFIRMED": {
                            "approved_by": "reviewer:product-01",
                            "reviewed_artifacts": ["requirements.md", "acceptance.md"],
                            "evidence": ["evidence/index.md"],
                            "decision_reason": "R01 and AC01 are traceable and the MVP boundary is explicit.",
                        }
                    },
                }
            )
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            payload = json.loads(
                self.run_script("validate_delivery_state.py", "--root", str(root)).stdout
            )
            self.assertTrue(payload["ok"])

            manifest["stageApprovals"] = {}
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            failed = self.run_script("validate_delivery_state.py", "--root", str(root), expected=1)
            self.assertIn("has no stageApprovals record", failed.stdout)

    def test_legacy_manifest_remains_valid(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "project"
            root.mkdir()
            self.run_script("init_delivery_workspace.py", "--root", str(root))
            manifest_path = root / ".product-delivery" / "manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["schemaVersion"] = 1
            for field in ("stageApprovals", "approvalPolicy", "delegatedScope", "reservedUserActions"):
                manifest.pop(field)
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            payload = json.loads(
                self.run_script("validate_delivery_state.py", "--root", str(root)).stdout
            )
            self.assertTrue(payload["ok"])
            self.assertIn(
                "Legacy manifest schemaVersion 1 has no delegated-approval provenance",
                payload["warnings"],
            )

    def test_green_and_red_concurrency(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            candidates = root / "candidates.json"
            candidates.write_text(
                json.dumps(
                    {
                        "candidates": [
                            {"id": "A", "priority": 10, "resourceClass": "medium", "writeScopes": ["frontend"], "ready": True, "authorized": True},
                            {"id": "B", "priority": 5, "resourceClass": "light", "writeScopes": ["docs"], "ready": True, "authorized": True},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            green = root / "green.json"
            green.write_text(json.dumps({"cpu": {"load1PerLogicalCpu": 0.2}, "memory": {"freePercent": 50}, "disk": {"freePercent": 50}, "thermal": {}}), encoding="utf-8")
            result = self.run_script("plan_worker_concurrency.py", "--snapshot", str(green), "--candidates", str(candidates))
            payload = json.loads(result.stdout)
            self.assertEqual(payload["resourceState"], "GREEN")
            self.assertEqual([item["id"] for item in payload["launch"]], ["A"])

            red = root / "red.json"
            red.write_text(json.dumps({"cpu": {"load1PerLogicalCpu": 2.0}, "memory": {"freePercent": 50}, "disk": {"freePercent": 50}, "thermal": {}}), encoding="utf-8")
            result = self.run_script("plan_worker_concurrency.py", "--snapshot", str(red), "--candidates", str(candidates))
            payload = json.loads(result.stdout)
            self.assertEqual(payload["resourceState"], "RED")
            self.assertEqual(payload["launch"], [])

    def test_resource_snapshot_requires_explicit_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            snapshot = root / "snapshot.json"
            self.run_script("collect_resource_snapshot.py", "--path", str(root), "--output", str(snapshot))
            self.assertTrue(snapshot.is_file())
            refused = self.run_script(
                "collect_resource_snapshot.py",
                "--path",
                str(root),
                "--output",
                str(snapshot),
                expected=1,
            )
            self.assertIn("Refusing to overwrite", refused.stdout)
            self.run_script(
                "collect_resource_snapshot.py",
                "--path",
                str(root),
                "--output",
                str(snapshot),
                "--overwrite",
            )

    def test_invalid_candidate_returns_json_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            snapshot = root / "snapshot.json"
            snapshot.write_text(
                json.dumps({"cpu": {"load1PerLogicalCpu": 0.2}, "memory": {}, "disk": {}, "thermal": {}}),
                encoding="utf-8",
            )
            candidates = root / "candidates.json"
            candidates.write_text(json.dumps({"candidates": [{"id": "A", "priority": None}]}), encoding="utf-8")
            result = self.run_script(
                "plan_worker_concurrency.py",
                "--snapshot",
                str(snapshot),
                "--candidates",
                str(candidates),
                expected=1,
            )
            self.assertFalse(json.loads(result.stdout)["ok"])


if __name__ == "__main__":
    unittest.main()
