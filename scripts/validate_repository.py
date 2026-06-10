#!/usr/bin/env python3
"""Validate the blueprint repository."""

from __future__ import annotations

import re
import sys
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCUMENTATION = sorted(ROOT.glob("**/*.md")) + [
    path for path in (ROOT / "LICENSE", ROOT / "NOTICE") if path.exists()
]
SKILLS = sorted((ROOT / "skills").glob("*/SKILL.md"))
SKIP = {ROOT / "scripts" / "validate_repository.py"}
REQUIRED_PATHS = (
    "pyproject.toml",
    "Makefile",
    "scripts/wmb",
    "scripts/wmb-agent-launchable",
    "scripts/generate_diagrams.py",
    "src/world_model_blueprint/cli.py",
    "configs/agent-workflow.json",
    "benchmarks/benchmark-spec.json",
    "benchmarks/run_benchmarks.py",
    "deploy/README.md",
    "deploy/.env.example",
    "deploy/brev/launchable-workflow.md",
    "deploy/brev/world-model-launchable.ipynb",
    "schemas/programme-intake-manifest.schema.json",
    "schemas/dataset-manifest.schema.json",
    "schemas/neural-asset-manifest.schema.json",
    "schemas/simready-asset-manifest.schema.json",
    "schemas/training-run-manifest.schema.json",
    "schemas/inference-service-manifest.schema.json",
    "schemas/evaluation-manifest.schema.json",
    "schemas/governance-record.schema.json",
    "schemas/run-request.schema.json",
)
DEVELOPMENT_MARKERS = (
    "TO" + "DO",
    "FIX" + "ME",
    "W" + "IP",
    "lorem " + "ipsum",
    "AC" + "ME",
    "Copy" + "right (c) 2026 " + "Chris " + "von " + "Csefalvay",
    "pending " + "transfer",
    "currently maintained " + "under",
    "Verification " + "status",
    "source-" + "reviewed",
    "No external " + "signature",
    "NVIDIA-" + "style practices adopted",
)


def fail(message: str) -> None:
    print(f"validation failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_markers() -> None:
    for path in DOCUMENTATION:
        if path in SKIP:
            continue
        text = path.read_text(encoding="utf-8")
        for marker in DEVELOPMENT_MARKERS:
            if marker in text:
                fail(f"{path.relative_to(ROOT)} contains {marker}")


def check_skills() -> None:
    frontmatter = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
    if not SKILLS:
        fail("no skills found")
    for path in SKILLS:
        text = path.read_text(encoding="utf-8")
        match = frontmatter.match(text)
        if not match:
            fail(f"{path.relative_to(ROOT)} is missing YAML frontmatter")
        meta = match.group(1)
        expected = path.parent.name
        if f"name: {expected}" not in meta:
            fail(f"{path.relative_to(ROOT)} name does not match directory")
        if "description:" not in meta:
            fail(f"{path.relative_to(ROOT)} is missing description")
        card = path.parent / "skill-card.md"
        if not card.exists():
            fail(f"{path.parent.relative_to(ROOT)} is missing skill-card.md")
        for rel in (
            "BENCHMARK.md",
            "benchmark/evals.json",
            "references/operating-playbook.md",
            "references/output-contract.md",
            "scripts/run-checks.sh",
            "evals/benchmark-cases.json",
            "agents/openai.yaml",
        ):
            if not (path.parent / rel).exists():
                fail(f"{path.parent.relative_to(ROOT)} is missing {rel}")
        check_skill_eval_suite(path.parent)
        if len(text.splitlines()) < 120:
            fail(f"{path.relative_to(ROOT)} is too thin")


def check_skill_eval_suite(skill_dir: Path) -> None:
    path = skill_dir / "benchmark" / "evals.json"
    expected_skill = skill_dir.name
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{path.relative_to(ROOT)} is invalid JSON: {exc}")
    if not isinstance(payload, list):
        fail(f"{path.relative_to(ROOT)} must be a JSON array")
    if len(payload) < 6:
        fail(f"{path.relative_to(ROOT)} must contain at least six eval scenarios")
    seen: set[str] = set()
    for index, item in enumerate(payload):
        if not isinstance(item, dict):
            fail(f"{path.relative_to(ROOT)} item {index} must be an object")
        required = ("id", "question", "expected_skill", "expected_script", "ground_truth", "expected_behavior")
        for key in required:
            if key not in item:
                fail(f"{path.relative_to(ROOT)} item {index} is missing {key}")
        if item["id"] in seen:
            fail(f"{path.relative_to(ROOT)} duplicate id {item['id']}")
        seen.add(item["id"])
        if item["expected_skill"] != expected_skill:
            fail(f"{path.relative_to(ROOT)} item {item['id']} expected_skill does not match directory")
        if not isinstance(item["question"], str) or not item["question"].strip():
            fail(f"{path.relative_to(ROOT)} item {item['id']} question is empty")
        if item["expected_script"] is not None and not isinstance(item["expected_script"], str):
            fail(f"{path.relative_to(ROOT)} item {item['id']} expected_script must be null or string")
        if not isinstance(item["ground_truth"], str) or not item["ground_truth"].strip():
            fail(f"{path.relative_to(ROOT)} item {item['id']} ground_truth is empty")
        behaviour = item["expected_behavior"]
        if not isinstance(behaviour, list) or len(behaviour) < 4 or not all(isinstance(entry, str) and entry.strip() for entry in behaviour):
            fail(f"{path.relative_to(ROOT)} item {item['id']} needs at least four expected behaviour checks")


def check_architecture() -> None:
    for rel in (
        "docs/assets/architecture.svg",
        "docs/assets/architecture.mmd",
        "docs/assets/data-factory.svg",
        "docs/assets/neural-asset-services.svg",
        "docs/assets/agent-workflow.svg",
        "docs/assets/execution-lanes.svg",
        "docs/assets/inference-services.svg",
    ):
        if not (ROOT / rel).exists():
            fail(f"{rel} is missing")


def check_toolchain() -> None:
    for rel in REQUIRED_PATHS:
        if not (ROOT / rel).exists():
            fail(f"{rel} is missing")


def main() -> None:
    check_markers()
    check_skills()
    check_architecture()
    check_toolchain()
    print("repository validation passed")


if __name__ == "__main__":
    main()
