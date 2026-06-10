---
name: world-model-data-factory
description: >-
  Plans curation, enrichment, annotation, captioning, augmentation, split policy, and dataset release for world-model training and evaluation.
license: Proprietary
metadata:
  owner: Chris von Csefalvay (HCLTech)
  version: "1.1.0"
  tags:
    - data-factory
    - video
    - tao
    - physical-ai
---

# World model data factory

## Mission

Use this skill to convert real, simulated, and synthetic observations into model-ready evidence with repeatable quality gates. It owns the decision record for its stage of the data-to-world-model-to-sim2real pipeline and must emit artefacts that downstream agents can validate.

## Trigger conditions

Activate this skill when the request involves any of the following:

- Dataset production plan and dataset manifest.
- Inputs such as source manifests, sensor/action schemas, caption and label sources, rights records, simulation output.
- A handoff into or out of this stage of the autonomy world-model workflow.
- A review of whether the current evidence is sufficient to proceed.

Do not use this skill as a generic brainstorming surface. If required records are missing, create the appropriate manifest skeleton and state the missing evidence rather than inventing values.

## Required repository tools

Run these tools from the repository root with `PYTHONPATH=src` or through `scripts/wmb`:

| Tool | Use |
| --- | --- |
| `scripts/wmb new-manifest --schema schemas/dataset-manifest.schema.json --output <path>` | Create the stage manifest contract. |
| `scripts/wmb validate-manifest --schema schemas/dataset-manifest.schema.json --manifest <path>` | Validate required fields and basic types. |
| `scripts/wmb readiness-report --root <manifest-dir> --output <report.md>` | Summarise evidence completion across manifests. |
| `scripts/wmb skill-audit --root . --output artifacts/skill-audit.json` | Confirm skill packaging depth before release. |

Skill-local helper:

```bash
bash skills/world-model-data-factory/scripts/run-checks.sh <manifest-path>
```

## Required inputs

Before making recommendations, identify and record:

- source manifests.
- sensor/action schemas.
- caption and label sources.
- rights records.
- simulation output.

If the user has not provided a value, mark it as missing evidence in the output. Do not create identifiers, customer names, dataset names, platform names, job ids, or benchmark values.

## Preflight

1. Confirm the request is within this skill's authority and does not require an upstream skill first.
2. Locate the relevant manifest, or create a skeleton from `schemas/dataset-manifest.schema.json`.
3. Run the skill-local check script or `scripts/wmb validate-manifest`.
4. Classify missing evidence as blocking, non-blocking, or a downstream handoff.
5. Check privacy, rights, safety, and deployment authority before recommending any mutating action.
6. Name the next owner skill for every unresolved workstream.

## Operating workflow

1. Partition sources into real, simulated, synthetic, safety-event, and edge-case slices.
2. Define quality gates for corruption, duplication, timing, calibration, captions, labels, and action alignment.
3. Choose enrichment lanes: human review, VLM captioning, TAO annotation, VSS-derived summaries, or Physical AI video augmentation.
4. Protect train, validation, test, stress, and holdout splits before enrichment creates derivative leakage.
5. Emit dataset release evidence for post-training, simulation, and evaluation owners.

## Output contract

Return a concise professional artefact containing:

- dataset manifest.
- curation plan.
- split policy.
- augmentation strategy.
- release gate record.

The output must include:

- Manifest path or expected manifest path.
- Evidence accepted from source records.
- Evidence still missing.
- Human review gates.
- Downstream skill handoffs.
- Commands the operator can run to validate or generate the next artefact.

## Quality gates

Do not mark the stage ready unless all applicable gates are satisfied:

- Required manifest fields validate against `schemas/dataset-manifest.schema.json`.
- Source records are authoritative and do not rely on invented values.
- Sensitive data and secrets are referenced by controlled handle only.
- Safety and regulatory context are explicitly carried forward.
- Outputs are suitable for review by engineering, safety, legal, quality, and operations owners.

## Stop conditions

Stop and request review when any of these conditions appear:

- train-test leakage.
- weak caption quality.
- missing action semantics.
- synthetic data overwhelming real coverage.
- unresolved consent or license.

Also stop before destructive infrastructure actions, deployment to a real system, model promotion, external publication, or any action involving unapproved customer, medical, regulated, export-controlled, or confidential data.

## References to load when needed

- `references/operating-playbook.md` for detailed stage procedure.
- `references/output-contract.md` for deliverable structure and evidence tables.
- `BENCHMARK.md` for evaluation cases and pass criteria.
- `evals/benchmark-cases.json` for machine-readable skill evaluation cases.
