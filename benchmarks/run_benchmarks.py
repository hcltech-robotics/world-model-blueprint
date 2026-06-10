#!/usr/bin/env python3
"""Run blueprint packaging benchmarks."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str]) -> dict[str, object]:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        env={"PYTHONPATH": str(ROOT / "src")},
        text=True,
        capture_output=True,
        check=False,
    )
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
        "passed": completed.returncode == 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    report: dict[str, object] = {"benchmarks": []}
    benchmarks: list[dict[str, object]] = report["benchmarks"]  # type: ignore[assignment]

    benchmarks.append({"name": "repository_validation", **run([sys.executable, "scripts/validate_repository.py"])})
    benchmarks.append(
        {
            "name": "cli_repository_validation",
            **run([sys.executable, "-m", "world_model_blueprint.cli", "validate-repo", "--root", "."]),
        }
    )
    benchmarks.append(
        {
            "name": "skill_eval_suite_validation",
            **run(
                [
                    sys.executable,
                    "-m",
                    "world_model_blueprint.cli",
                    "skill-audit",
                    "--root",
                    ".",
                    "--output",
                    str(Path(tempfile.gettempdir()) / "world-model-blueprint-skill-audit.json"),
                ]
            ),
        }
    )

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        schema = ROOT / "schemas" / "run-request.schema.json"
        skeleton = tmp_path / "run-request.json"
        plan = tmp_path / "run-plan.json"
        benchmarks.append(
            {
                "name": "manifest_skeleton_generation",
                **run(
                    [
                        sys.executable,
                        "-m",
                        "world_model_blueprint.cli",
                        "new-manifest",
                        "--schema",
                        str(schema),
                        "--output",
                        str(skeleton),
                    ]
                ),
            }
        )
        skeleton.write_text(
            json.dumps(
                {
                    "workload_type": "massive-training",
                    "scale": "massive",
                    "node_count": 8,
                    "requires_realtime": True,
                    "requires_hil": True,
                    "requires_workflow_orchestration": True,
                    "gpu_memory_gb": 192,
                    "data_location": "controlled programme storage",
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        benchmarks.append(
            {
                "name": "run_request_validation",
                **run(
                    [
                        sys.executable,
                        "-m",
                        "world_model_blueprint.cli",
                        "validate-manifest",
                        "--schema",
                        str(schema),
                        "--manifest",
                        str(skeleton),
                    ]
                ),
            }
        )
        benchmarks.append(
            {
                "name": "execution_lane_routing",
                **run(
                    [
                        sys.executable,
                        "-m",
                        "world_model_blueprint.cli",
                        "run-plan",
                        "--request",
                        str(skeleton),
                        "--output",
                        str(plan),
                    ]
                ),
            }
        )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    failed = [item for item in benchmarks if not item["passed"]]
    if failed:
        print(json.dumps(report, indent=2), file=sys.stderr)
        return 1
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
