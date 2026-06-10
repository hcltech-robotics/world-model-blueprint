# Benchmark: Evaluation safety lead

## Purpose

Evaluate whether the skill can produce Evaluation manifest and promotion gate plan from authoritative records, identify missing evidence, and route downstream work without inventing operational details.

## Required artefacts

- `SKILL.md`
- `skill-card.md`
- `references/operating-playbook.md`
- `references/output-contract.md`
- `scripts/run-checks.sh`
- `evals/benchmark-cases.json`
- `benchmark/evals.json`

## Evaluation suites

The lightweight `evals/benchmark-cases.json` file names the packaging cases used by repository checks. The richer `benchmark/evals.json` file is the evaluator-facing suite patterned after NVIDIA skills benchmarks. It contains scenario objects with:

- `id`
- `question`
- `expected_skill`
- `expected_script`
- `ground_truth`
- `expected_behavior`

The suite covers happy-path planning, missing evidence, rights or safety ambiguity, downstream routing, and skill-specific edge cases. Every case must preserve the repository rule against invented names, identifiers, data, platform values, endpoint values, approvals, and benchmark claims.

## Pass criteria

- The skill uses repository tools instead of hand-written ad hoc validation.
- Required fields are checked against `schemas/evaluation-manifest.schema.json`.
- Sensitive values are never requested in plain text.
- Output includes evidence, missing evidence, review gates, commands, and handoffs.
- No invented platform, dataset, customer, model, endpoint, or benchmark identifiers appear.
