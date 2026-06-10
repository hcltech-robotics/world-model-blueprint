---
name: simready-content-integration
description: >-
  Plans conversion and validation of CAD, OpenUSD, SimReady assets, Omniverse scenes, Isaac Sim scenarios, and synthetic-data pipelines.
license: Proprietary
metadata:
  owner: Chris von Csefalvay (HCLTech)
  version: "1.1.0"
  tags:
    - omniverse
    - simready
    - openusd
    - isaac-sim
---

# SimReady content integration

## Mission

Use this skill to turn physical differentiators into simulation-ready assets and scenario evidence for world-model training and evaluation. It owns the decision record for its stage of the data-to-world-model-to-sim2real pipeline and must emit artefacts that downstream agents can validate.

## Trigger conditions

Activate this skill when the request involves any of the following:

- Simulation asset integration plan and SimReady asset manifest.
- Inputs such as CAD or OpenUSD assets, robot or machine description, materials and textures, physics requirements, scenario requirements.
- A handoff into or out of this stage of the autonomy world-model workflow.
- A review of whether the current evidence is sufficient to proceed.

Do not use this skill as a generic brainstorming surface. If required records are missing, create the appropriate manifest skeleton and state the missing evidence rather than inventing values.

## Required repository tools

Run these tools from the repository root with `PYTHONPATH=src` or through `scripts/wmb`:

| Tool | Use |
| --- | --- |
| `scripts/wmb new-manifest --schema schemas/simready-asset-manifest.schema.json --output <path>` | Create the stage manifest contract. |
| `scripts/wmb validate-manifest --schema schemas/simready-asset-manifest.schema.json --manifest <path>` | Validate required fields and basic types. |
| `scripts/wmb readiness-report --root <manifest-dir> --output <report.md>` | Summarise evidence completion across manifests. |
| `scripts/wmb skill-audit --root . --output artifacts/skill-audit.json` | Confirm skill packaging depth before release. |

Skill-local helper:

```bash
bash skills/simready-content-integration/scripts/run-checks.sh <manifest-path>
```

## Required inputs

Before making recommendations, identify and record:

- CAD or OpenUSD assets.
- robot or machine description.
- materials and textures.
- physics requirements.
- scenario requirements.

If the user has not provided a value, mark it as missing evidence in the output. Do not create identifiers, customer names, dataset names, platform names, job ids, or benchmark values.

## Preflight

1. Confirm the request is within this skill's authority and does not require an upstream skill first.
2. Locate the relevant manifest, or create a skeleton from `schemas/simready-asset-manifest.schema.json`.
3. Run the skill-local check script or `scripts/wmb validate-manifest`.
4. Classify missing evidence as blocking, non-blocking, or a downstream handoff.
5. Check privacy, rights, safety, and deployment authority before recommending any mutating action.
6. Name the next owner skill for every unresolved workstream.

## Operating workflow

1. Classify assets by visual, geometric, physical, sensor, semantic, and behavioural fidelity needs.
2. Identify which assets encode business-critical differentiators and deserve high-fidelity treatment.
3. Plan OpenUSD, SimReady, Omniverse, Isaac Sim, and Content Agents workflows with validation gates.
4. Connect scenarios to dataset splits, synthetic generation, evaluation, and real-system telemetry.
5. Record performance checks for large USD stages and streaming workloads.

## Output contract

Return a concise professional artefact containing:

- SimReady asset manifest.
- asset conversion plan.
- validation plan.
- scenario catalogue.
- synthetic data interface.

The output must include:

- Manifest path or expected manifest path.
- Evidence accepted from source records.
- Evidence still missing.
- Human review gates.
- Downstream skill handoffs.
- Commands the operator can run to validate or generate the next artefact.

## Quality gates

Do not mark the stage ready unless all applicable gates are satisfied:

- Required manifest fields validate against `schemas/simready-asset-manifest.schema.json`.
- Source records are authoritative and do not rely on invented values.
- Sensitive data and secrets are referenced by controlled handle only.
- Safety and regulatory context are explicitly carried forward.
- Outputs are suitable for review by engineering, safety, legal, quality, and operations owners.

## Stop conditions

Stop and request review when any of these conditions appear:

- asset rights ambiguity.
- unvalidated physics.
- poor USD performance.
- mismatch between simulated and measured behaviour.
- scenario catalogue not linked to evaluation.

Also stop before destructive infrastructure actions, deployment to a real system, model promotion, external publication, or any action involving unapproved customer, medical, regulated, export-controlled, or confidential data.

## References to load when needed

- `references/operating-playbook.md` for detailed stage procedure.
- `references/output-contract.md` for deliverable structure and evidence tables.
- `BENCHMARK.md` for evaluation cases and pass criteria.
- `evals/benchmark-cases.json` for machine-readable skill evaluation cases.
