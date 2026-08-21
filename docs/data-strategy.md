# Data strategy

## Data objective

The data strategy answers one question: what evidence does the world model need in order to improve the autonomy capability without making the system less safe, less lawful, or less predictable?

The data plan is created before training. It names the target behaviour, the operating domain, the required modalities, the known gaps, the quality gates, and the evaluation split.

Create the dataset contract before enrichment:

```bash
scripts/wmb new-manifest --schema schemas/dataset-manifest.schema.json --output artifacts/dataset.json
scripts/wmb validate-manifest --schema schemas/dataset-manifest.schema.json --manifest artifacts/dataset.json
```

The dataset manifest travels with all derived clips, captions, labels, simulation outputs, and training records.

<p align="center">
  <img src="../assets/data-factory.svg" alt="Data and SimReady factory from real evidence and digital assets to model-ready datasets" width="920">
</p>

<p align="center">
  <img src="../assets/neural-asset-services.svg" alt="Neural reconstruction and asset creation route through NVIDIA skills, Content Agents, NuRec, and downstream handoff" width="920">
</p>

## Required data classes

### Real observations

Use video, images, audio, depth, state estimates, telemetry, and event logs from the target system or a close operational analogue. Preserve timing, calibration, sensor placement, platform state, and environmental context.

### Actions and controls

For action-conditioned modelling, retain action vectors, joint commands, end-effector states, vehicle controls, implement states, timestamps, and any controller mode transitions. Store action dimensionality and embodiment mapping as part of the dataset contract.

### Simulation and digital assets

Use OpenUSD, SimReady assets, neural reconstructions, harvested object assets, simulator scenes, physics parameters, synthetic render metadata, and scenario definitions. Treat simulation output and generated assets as data with provenance, not as anonymous generated media.

The neural asset lane should run before SimReady conformance when the programme needs to reconstruct a scene from sensor evidence, extract reusable objects from captured logs, enrich USD assets with Content Agents, render headless previews or videos with OVRTX, produce sensor-simulation outputs, or generate asset variants to fill coverage gaps. The agent should route these tasks through `neural-asset-reconstruction`, which names the applicable `NVIDIA/skills` or OVRTX capability and records whether the execution surface is NIM-compatible, REST, gRPC, OVRTX Python or C SDK, CLI, containerised, scheduler-backed, or manual review.

### Labels, captions, and reasoning traces

Use human labels when safety or clinical meaning matters. Use VLM-derived captions, TAO video reasoning annotation, VSS-style video summaries, boxes, masks, tracks, event intervals, and QA pairs where they improve scale or consistency. Review the labels that affect promotion gates.

### Safety and failure evidence

Keep near misses, incidents, interventions, simulator failures, out-of-domain inputs, low-confidence outputs, and reviewer disagreements. These records are usually more valuable than large volumes of routine data.

## Dataset design

Datasets should be scenario-based. A scenario record should capture:

- Task and operating domain.
- Embodiment and sensor configuration.
- Source modality and calibration.
- Environmental conditions.
- Action schema, if applicable.
- Labels, captions, and review state.
- Rights, license, consent, and sensitivity.
- Split assignment.
- Transformations and generated derivatives.

Splits should separate scenario families, dates, sites, platforms, or operators where leakage would make evaluation misleading.

## Curation and enrichment

The data factory should perform:

- Quality filtering for corrupt media, missing timestamps, sensor drift, duplicate clips, and unusable labels.
- Coverage analysis across domain conditions, tasks, objects, instruments, terrain, weather, lighting, and failure modes.
- Caption generation and structured prompt creation where the model consumes structured descriptions.
- Video reasoning annotation for QA, physical plausibility, temporal localisation, and task reasoning.
- Synthetic augmentation only against named coverage gaps.
- Sampling for human review before full-scale processing.

## Synthetic data policy

Synthetic data is acceptable when it is traceable, labelled as synthetic, and evaluated against real-world performance. It should target known gaps such as rare weather, low light, occlusions, tool interactions, adverse terrain, simulator-only hazards, or safety-critical edge cases.

Do not let synthetic volume hide weak real-world coverage. Promotion gates should report performance separately on real, synthetic, mixed, and simulator-derived evaluation sets.

## Data gates

Data enters training only after:

- Rights and permitted use are recorded.
- Sensitive or regulated content is classified.
- Calibration and timing are sufficient for the task.
- Labels or captions pass sampled review.
- Leakage checks are complete.
- The data owner and model owner accept the intended use.

Rejected data should retain a rejection reason so that the programme can distinguish legal, quality, safety, and relevance failures.
