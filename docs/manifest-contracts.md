# Manifest contracts

## Purpose

Manifests are the source-of-truth records passed between skills. They prevent agents from relying on conversational memory or inferred values when a programme moves from data to simulation, post-training, inference, evaluation, and deployment.

## Schemas

| Schema | Owned by | Purpose |
| --- | --- | --- |
| `programme-intake-manifest.schema.json` | `autonomy-data-strategist` | Target capability, embodiment, operating domain, safety owner, and regulatory context. |
| `dataset-manifest.schema.json` | `world-model-data-factory` | Modalities, lineage, rights, split policy, calibration, quality gates, and permitted use. |
| `neural-asset-manifest.schema.json` | `neural-asset-reconstruction` | Neural reconstruction, Content Agents enrichment, upstream NVIDIA/skills route, service surface, and validation handoff. |
| `simready-asset-manifest.schema.json` | `simready-content-integration` | OpenUSD or SimReady assets, differentiators, fidelity targets, validation, and synthetic-data use. |
| `training-run-manifest.schema.json` | `cosmos-post-training-lead` | Base model, model surface, recipe, execution lane, checkpoint policy, parallelism, and serving target. |
| `inference-service-manifest.schema.json` | `real-time-inference-lead`, `deployment-operations-lead` | Backend, checkpoint, integration target, latency target, acceleration, observability, access control, and rollback. |
| `evaluation-manifest.schema.json` | `evaluation-safety-lead` | Candidate, baseline, slices, metrics, regression suites, safety acceptance, and promotion stage. |
| `governance-record.schema.json` | `governance-provenance-lead` | Artefact lineage, license review, privacy review, export control, retention, access, gates, and risk acceptance. |
| `run-request.schema.json` | `infrastructure-orchestration-lead` | Workload type, scale, node count, real-time needs, HIL needs, and orchestration requirements. |

## Creating a manifest

```bash
scripts/wmb new-manifest \
  --schema schemas/programme-intake-manifest.schema.json \
  --output artifacts/programme-intake.json
```

The generated manifest is a contract, not evidence. Null values mean the field still needs authoritative programme input.

## Validating a manifest

```bash
scripts/wmb validate-manifest \
  --schema schemas/programme-intake-manifest.schema.json \
  --manifest artifacts/programme-intake.json
```

Validation catches missing required fields, empty values, basic type mismatches, and enum mismatches. It does not replace legal, safety, regulatory, or quality review.
