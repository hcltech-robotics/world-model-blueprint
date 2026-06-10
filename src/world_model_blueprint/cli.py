"""Command-line tools for the world model blueprint."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT_MARKERS = ("README.md", "docs", "skills")
DEFAULT_AGENT_CONFIG = "configs/agent-workflow.json"
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
)


@dataclass
class CheckResult:
    ok: bool
    message: str


def repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if all((candidate / marker).exists() for marker in ROOT_MARKERS):
            return candidate
    return current


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def load_env_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(path)
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'\"")
        if key and key not in os.environ:
            os.environ[key] = value


def iter_text_files(paths: list[Path]) -> list[Path]:
    suffixes = {".md", ".json", ".yaml", ".yml", ".toml", ".py", ".sh"}
    output: list[Path] = []
    for path in paths:
        if path.is_dir():
            output.extend(
                child
                for child in path.rglob("*")
                if child.is_file()
                and child.suffix in suffixes
                and ".git" not in child.parts
                and "outputs" not in child.parts
                and "artifacts" not in child.parts
            )
        elif path.is_file() and path.suffix in suffixes:
            output.append(path)
    return sorted(set(output))


def normalise_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    lines = [line.rstrip() for line in text.splitlines()]
    compact: list[str] = []
    blank_run = 0
    for line in lines:
        if line:
            blank_run = 0
            compact.append(line)
        else:
            blank_run += 1
            if blank_run <= 2:
                compact.append("")
    return "\n".join(compact).rstrip() + "\n"


def command_format(args: argparse.Namespace) -> int:
    files = iter_text_files([Path(path) for path in args.paths])
    changed: list[Path] = []
    for path in files:
        if path.suffix == ".json":
            formatted = json.dumps(read_json(path), indent=2, sort_keys=True) + "\n"
        else:
            formatted = normalise_text(path)
        original = path.read_text(encoding="utf-8")
        if formatted != original:
            changed.append(path)
            if not args.check:
                path.write_text(formatted, encoding="utf-8")
    if changed:
        for path in changed:
            print(path)
        return 1 if args.check else 0
    print("format check passed")
    return 0


def schema_type_ok(expected: str, value: Any) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "number":
        return isinstance(value, int | float) and not isinstance(value, bool)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    return True


def validate_schema(schema: dict[str, Any], payload: Any, path: str = "$") -> list[str]:
    errors: list[str] = []
    expected_type = schema.get("type")
    if isinstance(expected_type, list):
        if not any(schema_type_ok(item, payload) or (item == "null" and payload is None) for item in expected_type):
            errors.append(f"{path}: expected one of {expected_type}")
            return errors
    elif isinstance(expected_type, str) and expected_type != "null" and not schema_type_ok(expected_type, payload):
        errors.append(f"{path}: expected {expected_type}")
        return errors
    if payload is None:
        return errors
    if "enum" in schema and payload not in schema["enum"]:
        errors.append(f"{path}: value is not in allowed set")
    if isinstance(payload, dict):
        for key in schema.get("required", []):
            if key not in payload:
                errors.append(f"{path}.{key}: required field is missing")
            elif payload[key] in ("", [], {}):
                errors.append(f"{path}.{key}: required field is empty")
        properties = schema.get("properties", {})
        for key, value in payload.items():
            if key in properties:
                errors.extend(validate_schema(properties[key], value, f"{path}.{key}"))
    if isinstance(payload, list) and "items" in schema:
        for index, value in enumerate(payload):
            errors.extend(validate_schema(schema["items"], value, f"{path}[{index}]"))
    return errors


def skeleton_from_schema(schema: dict[str, Any]) -> Any:
    schema_type = schema.get("type")
    if isinstance(schema_type, list):
        schema_type = next((item for item in schema_type if item != "null"), "string")
    if schema_type == "object":
        return {key: skeleton_from_schema(value) for key, value in schema.get("properties", {}).items()}
    if schema_type == "array":
        return []
    if schema_type == "boolean":
        return False
    return None


def command_validate_manifest(args: argparse.Namespace) -> int:
    schema = read_json(Path(args.schema))
    payload = read_json(Path(args.manifest))
    errors = validate_schema(schema, payload)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("manifest validation passed")
    return 0


def command_new_manifest(args: argparse.Namespace) -> int:
    schema = read_json(Path(args.schema))
    payload = skeleton_from_schema(schema)
    write_json(Path(args.output), payload)
    print(Path(args.output))
    return 0


def non_empty(value: Any) -> bool:
    return value not in (None, "", [], {})


def manifest_completion(schema: dict[str, Any], payload: dict[str, Any]) -> tuple[int, int, list[str]]:
    required = schema.get("required", [])
    missing = [key for key in required if key not in payload or not non_empty(payload[key])]
    return len(required) - len(missing), len(required), missing


def command_readiness_report(args: argparse.Namespace) -> int:
    root = Path(args.root)
    schema_dir = Path(args.schema_dir)
    rows: list[tuple[str, int, int, list[str]]] = []
    for schema_path in sorted(schema_dir.glob("*.schema.json")):
        manifest_path = root / schema_path.name.replace(".schema.json", ".json")
        if not manifest_path.exists():
            rows.append((schema_path.stem.replace("-manifest.schema", ""), 0, len(read_json(schema_path).get("required", [])), ["manifest absent"]))
            continue
        schema = read_json(schema_path)
        payload = read_json(manifest_path)
        complete, total, missing = manifest_completion(schema, payload)
        rows.append((schema_path.stem.replace("-manifest.schema", ""), complete, total, missing))
    lines = [
        "# Blueprint readiness report",
        "",
        "| Manifest | Required fields complete | Missing evidence |",
        "| --- | ---: | --- |",
    ]
    for name, complete, total, missing in rows:
        missing_text = ", ".join(missing) if missing else "None"
        lines.append(f"| {name} | {complete}/{total} | {missing_text} |")
    lines.extend(
        [
            "",
            "Promotion requires all required fields to be complete and accepted by the responsible owners.",
            "",
        ]
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    print(output)
    return 0


def command_run_plan(args: argparse.Namespace) -> int:
    request = read_json(Path(args.request))
    scale = request.get("scale")
    workload = request.get("workload_type")
    realtime = bool(request.get("requires_realtime"))
    hil = bool(request.get("requires_hil"))
    node_count = int(request.get("node_count") or 1)
    gpu_memory = int(request.get("gpu_memory_gb") or 0)
    lanes: list[str] = []
    if scale == "pilot" and node_count <= 1:
        lanes.append("brev")
    if workload in {"training", "evaluation"} and (scale == "large" or node_count > 1):
        lanes.append("b200-slurm")
    if workload == "massive-training" or scale == "massive":
        lanes.append("megatron")
    if hil or request.get("requires_workflow_orchestration"):
        lanes.append("osmo")
    if realtime:
        lanes.append("flashdreams")
    if not lanes:
        lanes.append("local-gpu")
    plan = {
        "recommended_lanes": lanes,
        "minimum_controls": [
            "dataset manifest",
            "rights and permitted-use record",
            "checkpoint and resume policy",
            "evaluation gate",
            "serving rollback target",
        ],
        "inference_backend": "flashdreams" if realtime else "nim-or-framework",
        "notes": {
            "gpu_memory_gb": gpu_memory,
            "node_count": node_count,
            "request_workload_type": workload,
        },
    }
    write_json(Path(args.output), plan)
    print(Path(args.output))
    return 0


def read_limited(path: Path, limit: int = 16000) -> str:
    text = path.read_text(encoding="utf-8")
    if len(text) <= limit:
        return text
    return text[:limit] + "\n\n[content truncated by workflow runner]\n"


def collect_evidence(root: Path) -> str:
    if not root.exists():
        return "No evidence directory exists yet."
    suffixes = {".json", ".md", ".txt"}
    parts: list[str] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix not in suffixes:
            continue
        rel = path.relative_to(root)
        parts.append(f"## {rel}\n\n{read_limited(path, 10000)}")
    return "\n\n".join(parts) if parts else "Evidence directory exists but contains no supported evidence files."


def api_key_from_config(llm_config: dict[str, Any]) -> str | None:
    env_names = [llm_config.get("api_key_env", "WMB_LLM_API_KEY")]
    env_names.extend(llm_config.get("fallback_api_key_env", ["NVIDIA_API_KEY"]))
    for name in env_names:
        value = os.getenv(str(name), "")
        if value:
            return value
    return None


def env_or_default(env_name: str, default: Any) -> Any:
    return os.getenv(env_name) or default


def llm_settings(config: dict[str, Any]) -> dict[str, Any]:
    llm_config = config.get("llm", {})
    api_key = api_key_from_config(llm_config)
    require_key = os.getenv("WMB_LLM_REQUIRE_API_KEY", str(llm_config.get("require_api_key", True))).lower() not in {"0", "false", "no"}
    if require_key and not api_key:
        key_env = llm_config.get("api_key_env", "WMB_LLM_API_KEY")
        fallback = ", ".join(llm_config.get("fallback_api_key_env", ["NVIDIA_API_KEY"]))
        raise RuntimeError(f"missing LLM API key; set {key_env} or one of: {fallback}")
    return {
        "api_key": api_key,
        "base_url": env_or_default(llm_config.get("base_url_env", "WMB_LLM_BASE_URL"), llm_config.get("default_base_url", "https://integrate.api.nvidia.com/v1")),
        "model": env_or_default(llm_config.get("model_env", "WMB_LLM_MODEL"), llm_config.get("default_model", "nvidia/nemotron-3-nano-30b-a3b")),
        "temperature": float(os.getenv("WMB_LLM_TEMPERATURE", str(llm_config.get("temperature", 0.2)))),
        "max_tokens": int(os.getenv("WMB_LLM_MAX_TOKENS", str(llm_config.get("max_tokens", 4096)))),
        "timeout": int(os.getenv("WMB_LLM_TIMEOUT_SECONDS", str(llm_config.get("timeout_seconds", 180)))),
    }


def chat_completion(settings: dict[str, Any], messages: list[dict[str, str]]) -> str:
    endpoint = os.getenv("WMB_LLM_CHAT_COMPLETIONS_URL") or settings["base_url"].rstrip("/") + "/chat/completions"
    headers = {"Content-Type": "application/json"}
    if settings.get("api_key"):
        headers["Authorization"] = f"Bearer {settings['api_key']}"
    payload = {
        "model": settings["model"],
        "messages": messages,
        "temperature": settings["temperature"],
        "max_tokens": settings["max_tokens"],
    }
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=settings["timeout"]) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")[:2000]
        raise RuntimeError(f"LLM request failed with HTTP {exc.code}: {body}") from exc
    choices = data.get("choices", [])
    if not choices:
        raise RuntimeError("LLM response did not include choices")
    message = choices[0].get("message", {})
    content = message.get("content")
    if not isinstance(content, str) or not content.strip():
        raise RuntimeError("LLM response did not include message content")
    return content.strip()


def stage_messages(stage: dict[str, Any], objective: str, evidence: str, root: Path) -> list[dict[str, str]]:
    skill_name = stage["skill"]
    skill_dir = root / "skills" / skill_name
    skill_path = skill_dir / "SKILL.md"
    if not skill_path.exists():
        raise FileNotFoundError(skill_path)
    skill_card = skill_dir / "skill-card.md"
    output_contract = skill_dir / "references" / "output-contract.md"
    skill_material = [
        "# Skill instructions",
        read_limited(skill_path),
    ]
    if skill_card.exists():
        skill_material.extend(["# Skill card", read_limited(skill_card)])
    if output_contract.exists():
        skill_material.extend(["# Output contract", read_limited(output_contract)])
    system = "\n".join(
        [
            "You are operating the world model blueprint agent workflow.",
            "Use British English.",
            "Use only supplied evidence and repository contracts.",
            "Do not invent customer names, dataset identifiers, deployment identifiers, benchmark values, approvals, access rights, or regulatory conclusions.",
            "When evidence is absent, state the missing evidence and the owner or review gate that must supply it.",
            "Never emit secret values, access tokens, private keys, credentials, or production endpoints.",
            "Return a serious professional Markdown section that can be appended to a programme record.",
        ]
    )
    user = "\n\n".join(
        [
            f"# Programme objective\n{objective}",
            f"# Workflow stage\n{stage['id']}: {stage['name']}",
            f"# Stage instruction\n{stage['instruction']}",
            "\n\n".join(skill_material),
            f"# Evidence supplied\n{evidence}",
            "# Required response shape\n"
            "## Decisions\n"
            "## Manifest updates\n"
            "## Missing evidence\n"
            "## Commands or artefacts to run next\n"
            "## Review gates\n"
            "## Next agent handoff\n",
        ]
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def command_agent_workflow(args: argparse.Namespace) -> int:
    root = repo_root(Path.cwd())
    if args.env_file:
        env_path = Path(args.env_file)
        load_env_file(env_path if env_path.is_absolute() else root / env_path)
    objective = args.objective or os.getenv("WMB_AGENT_OBJECTIVE")
    if not objective:
        print("missing programme objective; pass --objective or set WMB_AGENT_OBJECTIVE", file=sys.stderr)
        return 1
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = root / config_path
    config = read_json(config_path)
    evidence_root = Path(args.evidence_root)
    if not evidence_root.is_absolute():
        evidence_root = root / evidence_root
    evidence = collect_evidence(evidence_root)
    stages = config.get("stages", [])
    selected = set(args.stage or [])
    if selected:
        stages = [stage for stage in stages if stage.get("id") in selected]
    if not stages:
        print("no matching workflow stages", file=sys.stderr)
        return 1
    settings = None if args.dry_run else llm_settings(config)
    lines = [
        "# World model agent workflow",
        "",
        f"Objective: {objective}",
        "",
        f"Evidence root: `{evidence_root}`",
        f"Configuration: `{config_path}`",
        "",
    ]
    if settings:
        lines.extend(
            [
                "## LLM runtime",
                "",
                f"- Model: `{settings['model']}`",
                f"- Base URL: `{settings['base_url']}`",
                "- API key: supplied through environment",
                "",
            ]
        )
    else:
        lines.extend(["## LLM runtime", "", "- Dry run: no LLM request was made.", ""])
    for stage in stages:
        print(f"agent workflow stage: {stage['id']}", file=sys.stderr)
        messages = stage_messages(stage, objective, evidence, root)
        lines.extend([f"## {stage['name']}", "", f"Skill: `{stage['skill']}`", ""])
        if args.dry_run:
            lines.extend(
                [
                    "### Prompt package",
                    "",
                    "```text",
                    messages[-1]["content"][:12000],
                    "```",
                    "",
                ]
            )
        else:
            lines.extend([chat_completion(settings, messages), ""])
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(output)
    return 0


def skill_score(skill_dir: Path) -> dict[str, Any]:
    required = ["SKILL.md", "skill-card.md", "BENCHMARK.md", "benchmark/evals.json"]
    files = {name: (skill_dir / name).exists() for name in required}
    dirs = {name: (skill_dir / name).is_dir() for name in ("references", "scripts", "evals", "agents")}
    skill_lines = (skill_dir / "SKILL.md").read_text(encoding="utf-8").count("\n") + 1
    eval_count = 0
    eval_path = skill_dir / "benchmark" / "evals.json"
    if eval_path.exists():
        try:
            eval_payload = read_json(eval_path)
            if isinstance(eval_payload, list):
                eval_count = len(eval_payload)
        except json.JSONDecodeError:
            eval_count = 0
    score = sum(files.values()) + sum(dirs.values()) + (1 if skill_lines >= 120 else 0) + (1 if eval_count >= 6 else 0)
    return {
        "skill": skill_dir.name,
        "score": score,
        "max_score": len(files) + len(dirs) + 2,
        "files": files,
        "directories": dirs,
        "eval_count": eval_count,
        "skill_lines": skill_lines,
    }


def command_skill_audit(args: argparse.Namespace) -> int:
    root = Path(args.root)
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    report = [skill_score(path.parent) for path in skills]
    write_json(Path(args.output), {"skills": report})
    failing = [item for item in report if item["score"] < item["max_score"]]
    if failing:
        for item in failing:
            print(f"{item['skill']}: {item['score']}/{item['max_score']}", file=sys.stderr)
        return 1
    print("skill audit passed")
    return 0


def command_validate_repo(args: argparse.Namespace) -> int:
    root = Path(args.root)
    docs = sorted(root.glob("**/*.md")) + [path for path in (root / "LICENSE", root / "NOTICE") if path.exists()]
    for path in docs:
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for marker in DEVELOPMENT_MARKERS:
            if marker in text:
                print(f"{path.relative_to(root)} contains {marker}", file=sys.stderr)
                return 1
    for skill in sorted((root / "skills").glob("*/SKILL.md")):
        text = skill.read_text(encoding="utf-8")
        if not re.match(r"^---\n.*?\n---\n", text, re.DOTALL):
            print(f"{skill.relative_to(root)} missing frontmatter", file=sys.stderr)
            return 1
        if not (skill.parent / "skill-card.md").exists():
            print(f"{skill.parent.relative_to(root)} missing skill-card.md", file=sys.stderr)
            return 1
        eval_path = skill.parent / "benchmark" / "evals.json"
        if not eval_path.exists():
            print(f"{skill.parent.relative_to(root)} missing benchmark/evals.json", file=sys.stderr)
            return 1
        eval_payload = read_json(eval_path)
        if not isinstance(eval_payload, list) or len(eval_payload) < 6:
            print(f"{eval_path.relative_to(root)} must contain at least six eval scenarios", file=sys.stderr)
            return 1
        for item in eval_payload:
            if not isinstance(item, dict) or item.get("expected_skill") != skill.parent.name:
                print(f"{eval_path.relative_to(root)} contains an invalid skill eval case", file=sys.stderr)
                return 1
    print("repository validation passed")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wmb")
    sub = parser.add_subparsers(required=True)

    fmt = sub.add_parser("format", help="Format markdown, JSON, YAML, TOML, Python, and shell files.")
    fmt.add_argument("paths", nargs="+")
    fmt.add_argument("--check", action="store_true")
    fmt.set_defaults(func=command_format)

    validate_manifest = sub.add_parser("validate-manifest", help="Validate a manifest against a bundled JSON schema subset.")
    validate_manifest.add_argument("--schema", required=True)
    validate_manifest.add_argument("--manifest", required=True)
    validate_manifest.set_defaults(func=command_validate_manifest)

    new_manifest = sub.add_parser("new-manifest", help="Create an empty manifest from a JSON schema.")
    new_manifest.add_argument("--schema", required=True)
    new_manifest.add_argument("--output", required=True)
    new_manifest.set_defaults(func=command_new_manifest)

    readiness = sub.add_parser("readiness-report", help="Summarise manifest completion.")
    readiness.add_argument("--root", required=True)
    readiness.add_argument("--schema-dir", default="schemas")
    readiness.add_argument("--output", required=True)
    readiness.set_defaults(func=command_readiness_report)

    run_plan = sub.add_parser("run-plan", help="Generate an execution-lane recommendation from a run request.")
    run_plan.add_argument("--request", required=True)
    run_plan.add_argument("--output", required=True)
    run_plan.set_defaults(func=command_run_plan)

    agent_workflow = sub.add_parser("agent-workflow", help="Run the agent-driven blueprint workflow with an OpenAI-compatible LLM.")
    agent_workflow.add_argument("--config", default=DEFAULT_AGENT_CONFIG)
    agent_workflow.add_argument("--objective")
    agent_workflow.add_argument("--evidence-root", default="artifacts")
    agent_workflow.add_argument("--output", default="artifacts/agent-workflow.md")
    agent_workflow.add_argument("--env-file")
    agent_workflow.add_argument("--stage", action="append", help="Run only the named stage id. May be repeated.")
    agent_workflow.add_argument("--dry-run", action="store_true")
    agent_workflow.set_defaults(func=command_agent_workflow)

    skill_audit = sub.add_parser("skill-audit", help="Check skill packaging depth.")
    skill_audit.add_argument("--root", default=".")
    skill_audit.add_argument("--output", required=True)
    skill_audit.set_defaults(func=command_skill_audit)

    validate_repo = sub.add_parser("validate-repo", help="Validate repository policy and skill packaging.")
    validate_repo.add_argument("--root", default=".")
    validate_repo.set_defaults(func=command_validate_repo)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
