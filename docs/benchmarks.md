# Benchmarks

## Purpose

The benchmark harness verifies blueprint readiness. It checks packaging, schemas, CLI behaviour, skill resources, and deterministic execution-lane routing. It does not assert model performance, training throughput, safety acceptance, or compliance.

## Benchmark command

```bash
make benchmarks
```

The runner writes `artifacts/benchmark-report.json`.

## Included checks

| Check | What it verifies |
| --- | --- |
| Repository validation | Documentation markers, skill frontmatter, architecture diagrams, schemas, deploy templates, and benchmark files. |
| CLI validation | `wmb validate-repo` runs through the package entry point. |
| Skill eval suite validation | Every skill has `benchmark/evals.json` with multiple scenarios and required checks. |
| Manifest skeleton generation | `wmb new-manifest` can generate a schema-shaped record. |
| Manifest validation | `wmb validate-manifest` accepts a complete run request. |
| Execution lane routing | `wmb run-plan` produces deterministic recommendations for massive, real-time, HIL, and orchestrated workloads. |

## Skill benchmarks

Each skill includes its own `BENCHMARK.md`, lightweight `evals/benchmark-cases.json`, and a richer `benchmark/evals.json` suite patterned after the NVIDIA skills benchmark format. The packaging audit checks that every skill includes:

- Required `SKILL.md` and `skill-card.md`.
- `BENCHMARK.md`.
- `benchmark/evals.json` with at least six scenario cases.
- `references/`.
- `scripts/`.
- `evals/`.
- `agents/`.
- A sufficiently detailed activation body.

Each case in `benchmark/evals.json` must include:

- `id`
- `question`
- `expected_skill`
- `expected_script`
- `ground_truth`
- `expected_behavior`
