# Reference architecture

## Architecture goals

The architecture turns an autonomy problem into an auditable world model programme. It must support:

- Multi-modal data intake from real systems, simulation, neural reconstructions, and digital assets.
- Rights-aware curation, labelling, captioning, and augmentation.
- Cosmos 3 post-training and evaluation.
- Deployment through NIM or validated framework serving.
- Integration with simulation, real systems, and human review.
- Agent-assisted operation under governance controls.
- Executable manifests, checks, benchmarks, and deployment templates that make the architecture operable.

<p align="center">
  <img src="../assets/architecture.svg" alt="Simplified world model blueprint architecture" width="920">
</p>

## System blocks

### Scope

Inputs are the autonomy objective, target embodiment, operating design domain, regulatory or safety constraints, deployment target, data availability, and model surface required. The output is a model adaptation brief that names the task, expected input-output contract, data gaps, evaluation gates, and deployment path.

### Data and assets

This layer records source, ownership, consent, license, permitted use, retention, sensitivity, calibration, sensor context, and transformation history. It rejects data that cannot be used safely or lawfully. It also binds real and synthetic artefacts to their generating scenario, recipe, tool version, and review status.

### Data factory

This layer performs filtering, deduplication, quality scoring, captioning, annotation, synthetic variation, neural reconstruction routing, and dataset balancing. It may use:

- Cosmos Curator-style video curation and filtering.
- Physical AI video augmentation patterns for video enrichment and pseudo-labelling.
- TAO video reasoning annotation and model-specific dataset tools.
- VSS-style video understanding where video search, summarisation, or event extraction is useful.
- Omniverse Replicator, Isaac Sim, OpenUSD, SimReady, Content Agents-style workflows, OVRTX headless rendering, NuRec/NRE, NCore, and Asset Harvester for simulation-ready assets, previews, rendered videos, sensor outputs, neural reconstructions, harvested objects, and synthetic data.

### Adapt

Cosmos Framework is the main training and checkpoint path for Cosmos 3 SFT. Megatron-Core and Megatron Bridge are the massive-training path when scale, context length, MoE, or performance requirements exceed ordinary SFT. The model adaptation layer owns recipe selection, dataset adapters, base checkpoint conversion, launch configuration, logging, checkpoint export, and handoff to evaluation.

Typical adaptation paths include:

- Reasoner alignment for video QA, physical plausibility, temporal localisation, and task reasoning.
- Generator SFT for domain-conditioned video or image generation.
- Action-conditioned modelling for forward dynamics, inverse dynamics, or policy-like outputs.
- Massive distributed training with Megatron Bridge or Megatron-Core when the programme requires explicit TP, PP, CP, EP, DP, FSDP, resiliency, or performance tuning.
- Ancillary TAO training for retrieval, embeddings, perception, video reasoning annotation, and classical vision components.

### Evaluation and promotion

Promotion is evidence-based. The evaluation layer compares the base model and adapted model on held-out scenarios, simulator tests, real-world validation sets, safety events, and regression suites.

The promotion record should include the model version, data manifest, evaluation manifest, risk acceptance, reviewer sign-off, deployment target, rollback target, and limitations.

### Serve

Serving uses NIM where possible, FlashDreams for high-performance interactive autoregressive video or world-model inference, and Cosmos Framework, vLLM, Transformers, Dynamo, or validated internal serving where required. Integration targets include:

- Simulation systems and digital twins.
- Fleet logs and replay systems.
- Human review consoles.
- Real-time autonomy stacks.
- Safety monitors and policy enforcement.
- Enterprise observability and incident systems.

### Operate

The infrastructure fabric spans Brev for smaller single-instance runs, local GPU workstations for smoke tests, B200-class Slurm clusters for large training and evaluation, Megatron for massive distributed training, OSMO for Physical AI workflow orchestration, Kubernetes or Ray for cloud-native workflows, and production inference services through NIM, Dynamo, FlashDreams, vLLM, Transformers, or Cosmos Framework.

This fabric is part of the architecture. It owns scheduling, storage, secrets, checkpointing, observability, acceleration, and rollback for both training and inference.

## Executable artefacts

| Layer | Artefact |
| --- | --- |
| Programme intake | `schemas/programme-intake-manifest.schema.json` |
| Data and rights | `schemas/dataset-manifest.schema.json` |
| Neural and generated assets | `schemas/neural-asset-manifest.schema.json` |
| Simulation assets | `schemas/simready-asset-manifest.schema.json` |
| Model adaptation | `schemas/training-run-manifest.schema.json` |
| Evaluation | `schemas/evaluation-manifest.schema.json` |
| Serving | `schemas/inference-service-manifest.schema.json` |
| Governance | `schemas/governance-record.schema.json` |
| Execution planning | `schemas/run-request.schema.json`, `scripts/wmb run-plan` |
| Release checks | `scripts/validate_repository.py`, `scripts/wmb skill-audit`, `benchmarks/run_benchmarks.py` |

## Agent control plane

Agents sit across the architecture as operators. They are not privileged by default. Each agent works through a skill, produces bounded artefacts, and stops at review gates for secrets, destructive infrastructure changes, model promotion, safety acceptance, or deployment to a real system.

The agent control plane includes:

- Skill loading and routing.
- Skill cards and provenance metadata.
- Secret handling rules.
- Evidence capture.
- Review gates.
- Promotion and rollback records.

## Architecture diagram

The current architecture diagram is stored as [assets/architecture.svg](assets/architecture.svg). The editable Mermaid source is [assets/architecture.mmd](assets/architecture.mmd).

Focused companion diagrams:

- [Data and SimReady factory](assets/data-factory.svg)
- [Neural asset services](assets/neural-asset-services.svg)
- [Agent workflow](assets/agent-workflow.svg)
- [Execution lane selection](assets/execution-lanes.svg)
- [Inference services](assets/inference-services.svg)
