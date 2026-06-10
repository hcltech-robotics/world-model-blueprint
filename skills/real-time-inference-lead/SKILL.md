---
name: real-time-inference-lead
description: >-
  Plans serving through NIM, FlashDreams, Dynamo, Cosmos Framework inference, vLLM, Transformers, and edge or simulator runtimes.
license: Proprietary
metadata:
  owner: Chris von Csefalvay (HCLTech)
  version: "1.1.0"
  tags:
    - inference
    - flashdreams
    - nim
    - dynamo
    - real-time
---

# Real-time inference lead

## Mission

Use this skill to make the adapted world model usable in batch, simulator, shadow, advisory, and real-time workflows with explicit acceleration controls. It owns the decision record for its stage of the data-to-world-model-to-sim2real pipeline and must emit artefacts that downstream agents can validate.

## Trigger conditions

Activate this skill when the request involves any of the following:

- Inference service manifest and acceleration plan.
- Inputs such as checkpoint and export record, latency target, integration target, GPU profile, evaluation gate.
- A handoff into or out of this stage of the autonomy world-model workflow.
- A review of whether the current evidence is sufficient to proceed.

Do not use this skill as a generic brainstorming surface. If required records are missing, create the appropriate manifest skeleton and state the missing evidence rather than inventing values.

## Required repository tools

Run these tools from the repository root with `PYTHONPATH=src` or through `scripts/wmb`:

| Tool | Use |
| --- | --- |
| `scripts/wmb new-manifest --schema schemas/inference-service-manifest.schema.json --output <path>` | Create the stage manifest contract. |
| `scripts/wmb validate-manifest --schema schemas/inference-service-manifest.schema.json --manifest <path>` | Validate required fields and basic types. |
| `scripts/wmb readiness-report --root <manifest-dir> --output <report.md>` | Summarise evidence completion across manifests. |
| `scripts/wmb skill-audit --root . --output artifacts/skill-audit.json` | Confirm skill packaging depth before release. |

Skill-local helper:

```bash
bash skills/real-time-inference-lead/scripts/run-checks.sh <manifest-path>
```

## Required inputs

Before making recommendations, identify and record:

- checkpoint and export record.
- latency target.
- integration target.
- GPU profile.
- evaluation gate.

If the user has not provided a value, mark it as missing evidence in the output. Do not create identifiers, customer names, dataset names, platform names, job ids, or benchmark values.

## Preflight

1. Confirm the request is within this skill's authority and does not require an upstream skill first.
2. Locate the relevant manifest, or create a skeleton from `schemas/inference-service-manifest.schema.json`.
3. Run the skill-local check script or `scripts/wmb validate-manifest`.
4. Classify missing evidence as blocking, non-blocking, or a downstream handoff.
5. Check privacy, rights, safety, and deployment authority before recommending any mutating action.
6. Name the next owner skill for every unresolved workstream.

## Operating workflow

1. Prefer NIM when the selected model surface is supported and production deployment is required.
2. Use FlashDreams for streaming autoregressive video, self-forcing, low-latency closed-loop simulation, and interactive world-model serving.
3. Use Dynamo when Kubernetes-hosted OpenAI-compatible serving has a validated recipe for the backend and GPU profile.
4. Use Cosmos Framework inference, vLLM, or Transformers for custom checkpoints and validated reasoner endpoints.
5. Regression-test any change to precision, cache policy, batching, graph capture, or parallelism.

## Output contract

Return a concise professional artefact containing:

- inference manifest.
- backend decision.
- cache and precision plan.
- API contract.
- rollback controls.

The output must include:

- Manifest path or expected manifest path.
- Evidence accepted from source records.
- Evidence still missing.
- Human review gates.
- Downstream skill handoffs.
- Commands the operator can run to validate or generate the next artefact.

## Quality gates

Do not mark the stage ready unless all applicable gates are satisfied:

- Required manifest fields validate against `schemas/inference-service-manifest.schema.json`.
- Source records are authoritative and do not rely on invented values.
- Sensitive data and secrets are referenced by controlled handle only.
- Safety and regulatory context are explicitly carried forward.
- Outputs are suitable for review by engineering, safety, legal, quality, and operations owners.

## Stop conditions

Stop and request review when any of these conditions appear:

- checkpoint format unsupported.
- latency target absent.
- cache invalidation untested.
- closed-loop use without safety stage.
- observability absent.

Also stop before destructive infrastructure actions, deployment to a real system, model promotion, external publication, or any action involving unapproved customer, medical, regulated, export-controlled, or confidential data.

## References to load when needed

- `references/operating-playbook.md` for detailed stage procedure.
- `references/output-contract.md` for deliverable structure and evidence tables.
- `BENCHMARK.md` for evaluation cases and pass criteria.
- `evals/benchmark-cases.json` for machine-readable skill evaluation cases.
