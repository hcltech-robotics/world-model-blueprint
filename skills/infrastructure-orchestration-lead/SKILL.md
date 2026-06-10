---
name: infrastructure-orchestration-lead
description: >-
  Selects and governs execution across local GPUs, Brev, OSMO, B200-class Slurm, Megatron, Kubernetes, Ray, and cloud launchers.
license: Proprietary
metadata:
  owner: Chris von Csefalvay (HCLTech)
  version: "1.1.0"
  tags:
    - brev
    - osmo
    - slurm
    - megatron
    - kubernetes
---

# Infrastructure orchestration lead

## Mission

Use this skill to make training, evaluation, simulation, and inference executable on the right platform with a documented launch contract. It owns the decision record for its stage of the data-to-world-model-to-sim2real pipeline and must emit artefacts that downstream agents can validate.

## Trigger conditions

Activate this skill when the request involves any of the following:

- Execution lane decision and run plan.
- Inputs such as job objective, model and dataset manifests, GPU and storage requirements, cluster constraints, secret-handling policy.
- A handoff into or out of this stage of the autonomy world-model workflow.
- A review of whether the current evidence is sufficient to proceed.

Do not use this skill as a generic brainstorming surface. If required records are missing, create the appropriate manifest skeleton and state the missing evidence rather than inventing values.

## Required repository tools

Run these tools from the repository root with `PYTHONPATH=src` or through `scripts/wmb`:

| Tool | Use |
| --- | --- |
| `scripts/wmb new-manifest --schema schemas/run-request.schema.json --output <path>` | Create the stage manifest contract. |
| `scripts/wmb validate-manifest --schema schemas/run-request.schema.json --manifest <path>` | Validate required fields and basic types. |
| `scripts/wmb readiness-report --root <manifest-dir> --output <report.md>` | Summarise evidence completion across manifests. |
| `scripts/wmb skill-audit --root . --output artifacts/skill-audit.json` | Confirm skill packaging depth before release. |

Skill-local helper:

```bash
bash skills/infrastructure-orchestration-lead/scripts/run-checks.sh <manifest-path>
```

## Required inputs

Before making recommendations, identify and record:

- job objective.
- model and dataset manifests.
- GPU and storage requirements.
- cluster constraints.
- secret-handling policy.

If the user has not provided a value, mark it as missing evidence in the output. Do not create identifiers, customer names, dataset names, platform names, job ids, or benchmark values.

## Preflight

1. Confirm the request is within this skill's authority and does not require an upstream skill first.
2. Locate the relevant manifest, or create a skeleton from `schemas/run-request.schema.json`.
3. Run the skill-local check script or `scripts/wmb validate-manifest`.
4. Classify missing evidence as blocking, non-blocking, or a downstream handoff.
5. Check privacy, rights, safety, and deployment authority before recommending any mutating action.
6. Name the next owner skill for every unresolved workstream.

## Operating workflow

1. Choose the smallest lane that produces valid evidence: local, Brev, Slurm, Megatron, Kubernetes, Ray, or OSMO.
2. Check storage, image, secret, scheduler, and checkpoint controls before launch.
3. Use Megatron only when scale, model size, context, MoE, or performance requirements demand it.
4. Use OSMO when data generation, simulation, training, evaluation, edge, or hardware-in-the-loop must be orchestrated together.
5. Record platform identifiers only from actual platform output, never from invention.

## Output contract

Return a concise professional artefact containing:

- run request manifest.
- run plan.
- launch contract.
- scheduler or workflow evidence requirements.

The output must include:

- Manifest path or expected manifest path.
- Evidence accepted from source records.
- Evidence still missing.
- Human review gates.
- Downstream skill handoffs.
- Commands the operator can run to validate or generate the next artefact.

## Quality gates

Do not mark the stage ready unless all applicable gates are satisfied:

- Required manifest fields validate against `schemas/run-request.schema.json`.
- Source records are authoritative and do not rely on invented values.
- Sensitive data and secrets are referenced by controlled handle only.
- Safety and regulatory context are explicitly carried forward.
- Outputs are suitable for review by engineering, safety, legal, quality, and operations owners.

## Stop conditions

Stop and request review when any of these conditions appear:

- local path used for multi-node data.
- missing resume path.
- secrets in manifests.
- unverified scheduler account.
- wrong lane for evidence need.

Also stop before destructive infrastructure actions, deployment to a real system, model promotion, external publication, or any action involving unapproved customer, medical, regulated, export-controlled, or confidential data.

## References to load when needed

- `references/operating-playbook.md` for detailed stage procedure.
- `references/output-contract.md` for deliverable structure and evidence tables.
- `BENCHMARK.md` for evaluation cases and pass criteria.
- `evals/benchmark-cases.json` for machine-readable skill evaluation cases.
