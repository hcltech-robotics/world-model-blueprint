# Skill card: Neural asset reconstruction

## Capability

Routes neural reconstruction, object harvesting, Content Agents enrichment, OVRTX headless rendering, CAD-to-SimReady conversion, and asset-generation work to the correct upstream NVIDIA/skills or OVRTX capability before the output is used for SimReady, synthetic data, simulation, or evaluation.

## Trigger inputs

- Sensor captures, video, camera, LiDAR, radar, depth, stereo, IMU, telemetry, or action logs.
- CAD, source meshes, OpenUSD, USDZ, PLY, splats, reference images, or simulator scenes.
- Requests for NuRec, NRE, NCore, Asset Harvester, Content Agents, material assignment, physics classification, texture generation, validation, video augmentation, defect generation, or neural reconstruction.
- Requests for OVRTX headless rendering of previews, videos, simulator frames, camera outputs, lidar, radar, semantic segmentation, or render validation evidence.
- Need to decide whether an asset route is NIM-backed, REST, gRPC, OVRTX Python or C SDK, CLI, containerised, scheduler-backed, or manual review.

## Produced artefacts

- Neural asset manifest.
- Upstream NVIDIA/skills invocation plan.
- Content Agents and service-surface plan.
- Reconstruction or asset-creation route.
- Validation gates and human review record.
- SimReady or data-factory handoff.

## Tools and references

- Schema: `schemas/neural-asset-manifest.schema.json`
- Local check script: `skills/neural-asset-reconstruction/scripts/run-checks.sh`
- Operating playbook: `skills/neural-asset-reconstruction/references/operating-playbook.md`
- Output contract: `skills/neural-asset-reconstruction/references/output-contract.md`
- Benchmark cases: `skills/neural-asset-reconstruction/evals/benchmark-cases.json`
- Upstream catalogue: `NVIDIA/skills`
- OVRTX skills: `NVIDIA-Omniverse/ovrtx/skills`

## Quality gates

- Manifest validation passes.
- Selected upstream capability is real and named.
- Rights, calibration, service surface, and validation evidence are explicit.
- Missing evidence is marked rather than invented.
- Downstream handoff names the local owner skill and artefact.

## Risks and controls

- source rights ambiguity.
- calibration or timing gaps.
- unvalidated reconstruction quality.
- generated derivative leakage into evaluation holdouts.
- generated USD or physics output without validation.
- rendered previews, videos, or sensor outputs used without render settings, status, warmup, and output-read validation.
- overstating CLI or container workflows as NIM-backed services.
