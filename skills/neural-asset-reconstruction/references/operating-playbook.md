# Operating playbook: Neural asset reconstruction

## Role in the blueprint

Role: decide whether a missing or strategic physical differentiator should be reconstructed from sensor evidence, converted from source assets, enriched by Content Agents, rendered headlessly with OVRTX, harvested as a reusable object, generated as synthetic visual evidence, or sent back for human review.

## Decision model

Use the following sequence for every engagement:

1. **Objective**: name the physical asset, scene, behaviour, defect, or environment capability needed by the programme.
2. **Evidence**: classify source evidence as real sensors, CAD/OpenUSD, reference images, simulation, video, telemetry, actions, or review notes.
3. **Rights**: confirm permitted use for source and derivative assets before any generation or reconstruction plan.
4. **Route**: select a real upstream NVIDIA/skills route or NuRec sibling skill; do not invent an agent or tool.
5. **Service surface**: prefer NIM-compatible, REST, or gRPC service boundaries when available; otherwise record CLI/container execution honestly.
6. **Validation**: require asset validation, visual inspection, simulator loading, physical plausibility, and leakage checks before promotion.
7. **Handoff**: send the resulting artefact to the next local skill with a named manifest and review gate.

## Tool procedure

```bash
scripts/wmb new-manifest --schema schemas/neural-asset-manifest.schema.json --output artifacts/neural-asset-reconstruction.json
scripts/wmb validate-manifest --schema schemas/neural-asset-manifest.schema.json --manifest artifacts/neural-asset-reconstruction.json
scripts/wmb readiness-report --root artifacts --output artifacts/readiness.md
```

For execution-lane decisions, use:

```bash
scripts/wmb run-plan --request artifacts/run-request.json --output artifacts/run-plan.json
```

For repository release checks, use:

```bash
scripts/wmb skill-audit --root . --output artifacts/skill-audit.json
python3 benchmarks/run_benchmarks.py --output artifacts/benchmark-report.json
```

## Route table

| Condition | Route | Next local owner |
| --- | --- | --- |
| CAD, mesh, or source USD exists and the objective is simulation readiness | `omniverse-cad-to-simready` | `simready-content-integration` |
| Existing USD needs material, physics, texture, or validation automation | Content Agents material, physics, texture, validation | `simready-content-integration` |
| Real multi-sensor recording should become a neural scene | `physical-ai-neural-reconstruction`, `nurec-index`, `ncore`, `nre` | `simready-content-integration` and `evaluation-safety-lead` |
| Captured object instances should become reusable 3D assets | `asset-harvester` | `simready-content-integration` |
| Reconstructed scene must feed repeated simulator render requests | `nre` gRPC serving | `deployment-operations-lead` |
| USD assets, scenes, videos, previews, lidar/radar outputs, semantic labels, or simulator frames must render headlessly | `NVIDIA-Omniverse/ovrtx` skills for setup, renderer creation, USD loading, render settings, camera outputs, stepping, status, warmup, render-output reads, and sensor configuration | `simready-content-integration`, `world-model-data-factory`, and `evaluation-safety-lead` |
| Rendered reconstruction needs cleanup or harmonisation | `nurec-fixer` | `evaluation-safety-lead` |
| Missing coverage can be addressed by generated video variants | `physical-ai-video-data-augmentation` | `world-model-data-factory` |
| Inspection or defect scenarios need synthetic examples | `physical-ai-defect-image-generation` | `world-model-data-factory` and `evaluation-safety-lead` |
| Large USD scenes load slowly or preview poorly | `omniverse-usd-performance-tuning`, `omniverse-realtime-viewer` | `simready-content-integration` |

## Evidence table

| Evidence class | Acceptable source | Not acceptable |
| --- | --- | --- |
| Asset identity | Controlled asset registry, source-control path, manifest, or storage handle | Informal name without provenance |
| Sensor data | Capture manifest with calibration, timing, sensor frame, storage handle, and rights | Uncalibrated clips or anonymous uploads |
| CAD/OpenUSD | Source-control path, PLM export, registry handle, or controlled package | Detached file with unknown license |
| Rights | Legal, programme, data owner, or asset owner record | Assumption that internal access implies permitted use |
| Service surface | Approved NIM, REST, gRPC, CLI, container, or scheduler record | Guessed endpoint or token |
| Validation | Asset Validator, SimReady validation, Content Agents validation, render review, simulator load, metrics, or human review | Visual impression without record |

## Handoff rules

- Handoff to `world-model-data-factory` when generated clips, defect images, augmented video, or reconstruction renders must enter dataset splits.
- Handoff to `simready-content-integration` when the output is USD, USDZ, PLY, splat, materialised USD, physics-authored USD, or a scenario asset.
- Handoff to `cosmos-post-training-lead` only after the generated or reconstructed evidence has dataset and validation records.
- Handoff to `infrastructure-orchestration-lead` when the selected upstream route needs Brev, Slurm, Kubernetes, OSMO, container registry, storage, or GPU scheduling decisions.
- Handoff to `real-time-inference-lead` when a reconstructed scene or world-model service must be served into a simulator, replay system, or shadow loop.
- Handoff to `evaluation-safety-lead` when physical fidelity, synthetic-to-real usefulness, reconstruction quality, or safety relevance is the blocker.
- Handoff to `deployment-operations-lead` when gRPC, REST, simulator, observability, incident, or rollback ownership must be established.
- Handoff to `governance-provenance-lead` when rights, privacy, export control, retention, licenses, or approval records are incomplete.

## Invocation policy

When the route uses `NVIDIA/skills`, name the skill directory exactly and include the reason it was selected. If the task requires NuRec sibling skills, name `nurec-index` first, then the specific sibling skill it should route to. If the source asset needs Content Agents, name the relevant Material, Physics, Texture, or Validation Agent capability and whether REST service or CLI execution is preferred.

When the route uses OVRTX, reference the upstream `NVIDIA-Omniverse/ovrtx/skills` entries needed for the task rather than copying setup or rendering recipes. A typical headless preview or video route should name `project-setup-python`, `renderer-creation`, `loading-usd`, `render-settings`, `camera-outputs-rt2`, `stepping-and-rendering`, `reading-render-output`, `status-queries`, and `warmup`. Add `configuring-lidar-sensors`, `configuring-radar-sensors`, `semantic-labels`, `reading-sensor-pointclouds`, or `render-product-device-pinning` when the render product requires those outputs.

Do not run upstream commands from this blueprint unless the operator has provided the source paths, credentials, and platform authorisation. The local output is the invocation plan, manifest, review gate, and handoff record.
