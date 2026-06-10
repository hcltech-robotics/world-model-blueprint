---
name: neural-asset-reconstruction
description: >-
  Routes neural reconstruction, Content Agents enrichment, harvested 3D assets, CAD-to-SimReady conversion, and asset-creation work to the correct NVIDIA/skills capability before SimReady handoff.
license: Proprietary
metadata:
  owner: Chris von Csefalvay (HCLTech)
  version: "1.0.0"
  tags:
    - physical-ai
    - nurec
    - content-agents
    - simready
    - openusd
    - nim
---

# Neural asset reconstruction

## Mission

Use this skill to turn captured physical evidence and source assets into a governed neural reconstruction or simulation-ready asset creation plan. It sits between the data factory and SimReady content integration. Its purpose is to decide when the workflow should invoke upstream NVIDIA/skills capabilities, Content Agents, or NuRec/NRE skills, and to produce an auditable handoff into OpenUSD, SimReady, simulation, synthetic data, and world-model evaluation.

The skill should make the asset lane as service-oriented as the approved tooling allows. Prefer NIM-backed or OpenAI-compatible service surfaces for LLM, VLM, captioning, material reasoning, physics classification, validation, and agent orchestration when those surfaces exist. Do not claim that every asset operation is a NIM. Some upstream tools run as CLIs, containers, Omniverse services, Docker Compose stacks, gRPC services, or simulator integrations. Record the actual service surface rather than forcing the terminology.

## Trigger conditions

Activate this skill when a request involves any of the following:

- Neural reconstruction from camera, LiDAR, radar, depth, stereo, IMU, telemetry, or robot logs.
- NuRec, NRE, NCore, USDZ reconstruction, 3D Gaussian splats, or novel-view rendering.
- Harvesting objects or environment assets from video, driving logs, robotics clips, or simulation captures.
- Content Agents-style material assignment, physics classification, texture generation, or validation for USD assets.
- Headless OVRTX rendering for asset previews, thumbnails, inspection frames, rendered videos, simulation rollouts, camera frames, lidar, radar, or semantic segmentation outputs.
- CAD, OpenUSD, or source asset conversion that may need Content Agents before SimReady validation.
- Asset creation, defect image generation, synthetic asset variation, or video augmentation that creates derivative training evidence.
- A decision about whether the next owner is `simready-content-integration`, `world-model-data-factory`, `evaluation-safety-lead`, or an upstream NVIDIA/skills entry.

Do not use this skill for generic dataset curation, model post-training, deployment, or inference-service selection unless the request is specifically about assets, reconstructions, or simulation content. Hand those workstreams to the correct downstream skill.

## Required repository tools

Run these tools from the repository root with `PYTHONPATH=src` or through `scripts/wmb`:

| Tool | Use |
| --- | --- |
| `scripts/wmb new-manifest --schema schemas/neural-asset-manifest.schema.json --output <path>` | Create the neural asset route contract. |
| `scripts/wmb validate-manifest --schema schemas/neural-asset-manifest.schema.json --manifest <path>` | Validate required route fields and evidence classes. |
| `scripts/wmb readiness-report --root <manifest-dir> --output <report.md>` | Summarise manifest completion and missing evidence. |
| `scripts/wmb skill-audit --root . --output artifacts/skill-audit.json` | Confirm skill packaging depth before release. |

Skill-local helper:

```bash
bash skills/neural-asset-reconstruction/scripts/run-checks.sh <manifest-path>
```

## Required inputs

Before recommending an upstream route, identify and record:

- Asset objective: object, scene, environment, defect, motion, or differentiator to reconstruct or create.
- Source evidence: camera, LiDAR, radar, depth, stereo, IMU, telemetry, actions, CAD, OpenUSD, video, reference images, simulation scene, or human review.
- Rights record: capture consent, ownership, license, permitted use, retention, and derivative-use approval.
- Target output: USD, USDZ, PLY, splat asset, materialised USD, SimReady package, preview image, thumbnail, rendered video, sensor frame, point cloud, semantic output, synthetic clip, render validation evidence, or dataset slice.
- Service surface: hosted NIM, private NIM, OpenAI-compatible endpoint, Content Agents REST service, OVRTX Python or C SDK, local CLI, container, gRPC server, simulator bridge, or manual review.
- Validation gates: render quality, geometry, physical behaviour, material plausibility, asset rights, simulator load, performance, safety relevance, and human review.

If a value is missing, mark it as missing evidence. Do not create dataset names, object identifiers, endpoint URLs, account names, job ids, asset paths, benchmark values, or approval records.

## Upstream capability routing

Use the following routing table. When a route is selected, name the upstream skill and the evidence required before invocation.

| Need | Primary route | Notes |
| --- | --- | --- |
| Convert CAD or source meshes into simulation-ready USD with material, physics, texture, validation, and packaging controls | `omniverse-cad-to-simready` in NVIDIA/skills | Use when CAD, mesh, or USD inputs are already available and the goal is OpenUSD or SimReady readiness. |
| Assign materials, classify physics, generate textures, or validate generated USD content with Content Agents | Content Agents material, physics, texture, and validation skills or services | Prefer REST service mode when the operator wants a service-like lane; use CLI when precise local control is needed. |
| Reconstruct a scene from multi-sensor recordings | `physical-ai-neural-reconstruction` in NVIDIA/skills, then NuRec `nurec-index`, `ncore`, and `nre` sibling skills | Use NCore conversion before NRE training; preserve sensor calibration and timing evidence. |
| Extract individual 3D objects from captured logs | NuRec `asset-harvester` | Use when the desired output is reusable object assets rather than a full scene reconstruction. |
| Render reconstructed scenes into new views or simulator queries | NuRec `nre` | Use gRPC serving where a simulator, hardware-in-the-loop harness, or batch renderer needs repeated requests. |
| Render USD assets, scenes, videos, camera previews, lidar/radar outputs, semantic labels, or simulator frames headlessly | `NVIDIA-Omniverse/ovrtx` skills: `project-setup-python`, `renderer-creation`, `loading-usd`, `render-settings`, `camera-outputs-rt2`, `stepping-and-rendering`, `reading-render-output`, `status-queries`, `warmup`, and sensor-specific skills as needed | Use this route for headless previews, validation imagery, synthetic render products, videos, and simulator evidence without building a full Omniverse Kit app. |
| Clean ghosting, floaters, flicker, lighting, or inserted-object appearance in rendered frames | NuRec `nurec-fixer` | Treat harmonisation as derivative generation with provenance and review gates. |
| Create synthetic video variants for world-model data gaps | `physical-ai-video-data-augmentation` in NVIDIA/skills | Route back to `world-model-data-factory` for split policy, leakage control, and dataset release. |
| Generate defect images or visual anomaly examples | `physical-ai-defect-image-generation` in NVIDIA/skills | Use only with a named inspection objective and rights-approved source evidence. |
| Inspect large USD stages or preview assets | `omniverse-realtime-viewer` and `omniverse-usd-performance-tuning` in NVIDIA/skills | Use before promoting assets into repeated training or simulation workloads. |

## NIM-oriented operating policy

Prefer these surfaces in order, when they are available and approved:

1. Hosted or private NIM-compatible LLM/VLM endpoints for agent reasoning, multimodal inspection, captioning, material reasoning, review summarisation, and validation prompts.
2. Content Agents REST services for material, physics, texture, and validation workflows on USD files, especially where the blueprint needs a repeatable service boundary.
3. OVRTX headless rendering through Python or C applications for previews, videos, sensor frames, semantic outputs, and simulator evidence when a full Omniverse Kit application is unnecessary.
4. NRE gRPC serving for repeated neural reconstruction render requests into simulators, replay tools, or batch generation jobs.
5. CLI or container routes for stages that do not have an appropriate service surface yet.
6. Manual review gates when rights, safety, physical fidelity, or reconstruction quality cannot be established automatically.

Do not describe a CLI-only or container-only route as NIM-backed. Instead, say it is selected because it is the current upstream execution path and record the closest service boundary.

## Preflight

1. Confirm the request belongs to neural reconstruction, asset harvesting, Content Agents enrichment, asset creation, or SimReady-adjacent content routing.
2. Locate the relevant manifest, or create a skeleton from `schemas/neural-asset-manifest.schema.json`.
3. Validate the manifest with the skill-local script or `scripts/wmb validate-manifest`.
4. Classify the source evidence and target output.
5. Select the upstream NVIDIA/skills route, or mark `manual_review_required` when evidence is insufficient.
6. Record the service surface and whether it is NIM, OpenAI-compatible, REST, gRPC, CLI, container, simulator bridge, or review-only.
7. Name the next owner skill and the exact artefact it should receive.

## Operating workflow

1. **Separate source types**: distinguish CAD/OpenUSD inputs, captured real-world sensors, simulator output, reference images, and human review notes.
2. **Protect provenance**: bind each derivative asset to rights, capture source, tool version, configuration, and review evidence.
3. **Choose reconstruction or creation lane**: select CAD-to-SimReady, Content Agents enrichment, NCore-to-NRE reconstruction, Asset Harvester, OVRTX headless rendering, video augmentation, defect generation, or manual review.
4. **Plan service execution**: identify whether the lane uses NIM-compatible endpoints, Content Agents REST services, OVRTX Python or C SDK rendering, NRE gRPC, local CLIs, containers, or scheduler workflows.
5. **Define validation gates**: include render quality, physical plausibility, USD loadability, SimReady conformance, simulator behaviour, synthetic-to-real usefulness, and safety relevance.
6. **Hand off deliberately**: route model-ready data questions to `world-model-data-factory`, asset conformance to `simready-content-integration`, compute placement to `infrastructure-orchestration-lead`, and promotion evidence to `evaluation-safety-lead`.

## Output contract

Return a professional artefact containing:

- Neural asset manifest.
- Upstream NVIDIA/skills invocation plan.
- NIM or service-surface plan.
- Source evidence and rights status.
- Reconstruction, enrichment, or asset-creation route.
- Validation and review gates.
- SimReady or data-factory handoff.

The output must include:

- Manifest path or expected manifest path.
- Accepted evidence from authoritative records.
- Missing evidence and whether it blocks execution.
- Selected upstream skill names and why they apply.
- Human review gates.
- Commands the operator can run to validate the manifest and inspect readiness.
- Downstream skill handoffs and their expected artefacts.

## Quality gates

Do not mark the stage ready unless all applicable gates are satisfied:

- Manifest validates against `schemas/neural-asset-manifest.schema.json`.
- The selected upstream route is a real named NVIDIA/skills entry, OVRTX skill entry, or verified upstream skill bundle.
- Rights, retention, and derivative-use records exist before generating or exporting derivative assets.
- Sensor calibration, timing, and coordinate assumptions are recorded for reconstruction routes.
- Generated assets and rendered OVRTX outputs have validation evidence before entering SimReady, dataset release, evaluation, or simulation evidence records.
- Service surfaces, endpoints, tokens, paths, and platform details are referenced by controlled handle only.
- The output does not invent operational identifiers, customer data, benchmark values, approvals, or endpoint URLs.

## Stop conditions

Stop and request review when any of these appear:

- Missing or ambiguous rights for source recordings, CAD, images, or derivative assets.
- Missing sensor calibration or timing needed for NCore/NRE reconstruction.
- Reconstruction quality cannot support the stated simulation or world-model use.
- Generated assets could create leakage into evaluation holdouts.
- Content Agents output has not passed validation or human review.
- The request would deploy to a real system, publish private assets, or use regulated data without explicit approval.

Also stop before destructive infrastructure actions, unapproved external publication, model promotion, real-system deployment, or exposure of secrets.

## References to load when needed

- `references/operating-playbook.md` for detailed route selection and handoff rules.
- `references/output-contract.md` for deliverable structure and acceptance criteria.
- `BENCHMARK.md` for evaluation cases and pass criteria.
- `evals/benchmark-cases.json` for machine-readable skill evaluation cases.
