# World model blueprint for autonomy programmes

## Executive overview

Autonomy programmes fail when data, simulation, model adaptation, safety, and deployment are treated as separate workstreams. A world model programme should instead operate as one evidence system: real observations and action traces define the problem; simulation and synthetic data expand coverage; post-training adapts the model to the embodiment and task; evaluation decides whether the model is fit for controlled use; deployment closes the loop back to operators, simulators, and real systems.

This blueprint defines that operating system for organisations adapting Cosmos 3-class world models. The target reader is a senior engineering, simulation, data, safety, or platform leader who needs to decide what to build, what to measure, what to automate with agents, and what must remain under human review.

The intended outcome is a complete capability rather than an isolated model artefact: simulation-ready business differentiators, a fine-tuned Cosmos-class world model, an efficient inference surface, and a governed loop from real data to simulation and back again.

## Use cases

The blueprint is appropriate when the system must reason about, generate, or forecast the physical world:

- Surgical robotics, including endoscopic video understanding, action-conditioned future rollouts, and simulation-backed policy evaluation.
- Agricultural machinery, including crop-row navigation, implement interaction, terrain and weather variation, and rare-event simulation.
- Autonomous vehicles and mobile robots, including forward dynamics, inverse dynamics, behavioural forecasting, and safety case evidence.
- Industrial robots, including manipulation, inspection, facility simulation, and synthetic data generation.
- Smart infrastructure, including video understanding, incident analysis, and policy-aware operational agents.

The blueprint does not assume that Cosmos 3 is always the only model in the system. TAO, VSS, NeMo, Omniverse, Isaac Sim, NIM, FlashDreams, OSMO, Megatron, retrieval, guardrails, and classical perception models are used where they are the right operational tool.

## Reference architecture

<p align="center">
  <img src="../assets/architecture.svg" alt="Simplified world model blueprint architecture" width="920">
</p>

The architecture has five operating blocks:

1. **Scope** captures the autonomy objective, embodiment, operating design domain, safety case, deployment target, and decision that the world model must support.
2. **Data and assets** collects real video, action traces, telemetry, simulator output, CAD/OpenUSD assets, neural reconstructions, SimReady scenarios, captions, labels, safety events, and human review decisions under a common lineage model.
3. **Adapt** uses Cosmos Framework, Brev, B200 Slurm, and Megatron as appropriate for supervised fine-tuning, reasoner alignment, generator adaptation, action-conditioned modelling, checkpoint export, and evaluation handoff.
4. **Serve** chooses NIM, FlashDreams, Dynamo, vLLM, Transformers, or Cosmos Framework inference based on model surface, latency, and integration target.
5. **Operate** connects simulator, shadow, advisory, and production-adjacent workflows through OSMO, Kubernetes, Ray, observability, rollback, and governance.

The architecture diagram is maintained in [assets/architecture.svg](assets/architecture.svg) with an editable Mermaid source in [assets/architecture.mmd](assets/architecture.mmd).

## Reference implementation surfaces

The blueprint includes repository artefacts that agents and operators can run:

- `schemas/` defines the records that move between workstreams.
- `scripts/wmb` creates and validates manifests, formats repository files, produces readiness reports, audits skill depth, and recommends execution lanes.
- `skills/*/scripts/run-checks.sh` gives each skill a deterministic local validation entry point.
- `benchmarks/run_benchmarks.py` verifies repository packaging, CLI behaviour, manifest generation, validation, and execution-lane routing.
- `deploy/` provides Brev, Slurm, Kubernetes, and OSMO templates that infrastructure owners can resolve against controlled platform records.
- `.github/workflows/validate.yml` runs the validation stack on push and pull request.

These artefacts are intentionally generic. They do not contain customer data, secret values, cluster names, job ids, endpoint identifiers, or benchmark claims.

## Execution environments

Training and inference are planned as explicit deployment lanes:

<p align="center">
  <img src="../assets/execution-lanes.svg" alt="Execution lane selection for pilots, large training, massive training, orchestration, and real-time serving" width="920">
</p>

- **Brev and local GPU workstations** for pilot SFT runs, dataset validation, captioning pilots, evaluation dry runs, and single-node inference experiments.
- **B200-class Slurm and Megatron clusters** for large Cosmos 3 SFT, massive distributed training, high-throughput evaluation, and runs that need shared high-performance storage.
- **Kubernetes, Ray, and OSMO** for cloud-native training, Physical AI workflow orchestration, simulation, hardware-in-the-loop, OSMO data factory workflows, NIM Operator deployments, and production inference services.
- **Dynamo, NIM, FlashDreams, vLLM, Transformers, and Cosmos Framework inference** for model serving, depending on the selected model surface, latency target, and deployment requirements.

This is not optional plumbing. A fine-tuning plan is incomplete until it names the execution lane, storage model, checkpoint policy, secrets handling, observability plan, and inference handoff.

## Real-time world-model serving

Some autonomy use cases need more than batch generation or offline evaluation. Closed-loop simulation, teleoperation preview, operator-in-the-loop planning, and interactive driving or robotics worlds need low-latency rollout generation. For those cases, the blueprint uses FlashDreams-style inference architecture:

- Streaming autoregressive rollout loops with explicit cache lifecycle.
- KV-cache and autoregressive cache management.
- Context parallelism and classifier-free guidance parallelism where useful.
- CUDA graph wrapping for stable low-latency execution.
- Streaming encoders and decoders for per-step control inputs and video output.
- Runner registration and model-specific integrations rather than ad hoc scripts.

This lane is the right choice when a stakeholder asks for real-time, self-forcing, closed-loop, or interactive world-model behaviour. It should still pass the same safety, provenance, and deployment gates as offline inference.

## Agent operating model

Agents are part of the production blueprint. They do not replace engineering judgement; they make the work repeatable, inspectable, and bounded.

The repository defines ten skills:

- `autonomy-data-strategist`
- `world-model-data-factory`
- `neural-asset-reconstruction`
- `simready-content-integration`
- `cosmos-post-training-lead`
- `infrastructure-orchestration-lead`
- `real-time-inference-lead`
- `evaluation-safety-lead`
- `deployment-operations-lead`
- `governance-provenance-lead`

Each skill has a `SKILL.md`, `skill-card.md`, `BENCHMARK.md`, references, eval cases, agent metadata, and a check script. The skills follow the Agent Skills structure of a portable directory with required `name` and `description` metadata, concise activation instructions, and detailed references loaded only when needed. Skill cards document ownership, use boundaries, outputs, dependencies, and known risks.

## Data strategy

Data selection is the central technical decision. The programme should not collect everything. It should collect the observations, action traces, contexts, and failure cases that explain the target capability.

The minimum data plan includes:

- Observations: video, images, audio where relevant, depth or state estimates where available, and simulator frames.
- Actions: robot joint commands, end-effector poses, vehicle controls, implement states, or other embodiment-specific control vectors.
- Context: operating domain, task, scene, weather, lighting, camera geometry, calibration, platform state, and safety constraints.
- Labels and captions: human labels, VLM-derived captions, structured event descriptions, QA pairs, masks, boxes, tracks, and simulator metadata.
- Evidence: provenance, consent or rights, sensor calibration, transformations, filtering decisions, and review outcomes.

Synthetic data is used to close specific coverage gaps, not to create volume for its own sake. Simulation and generation should be tied to a real validation question: rare weather, low light, tissue deformation, crop occlusion, tool interaction, unsafe near misses, or other long-tail events.

## Cosmos adaptation strategy

Cosmos 3 provides Reasoner and Generator surfaces across world understanding, world generation, action modelling, future prediction, and physical reasoning. Cosmos Framework is the implementation path for supervised fine-tuning and checkpoint handling. NIM is the preferred production serving surface when the required model and mode are available.

The adaptation strategy is:

- Baseline the unadapted model on domain-specific tasks before collecting new data.
- Build a curated dataset that captures the desired input-output contract: captioning, future rollout, action prediction, inverse dynamics, physical plausibility, temporal localisation, or task planning.
- Choose the smallest adaptation that can pass the promotion gates: prompt and retrieval, captions and data filtering, parameter-efficient adaptation, full SFT, or action post-training.
- Export checkpoints and evaluate them against held-out scenarios, safety cases, and simulator-derived regressions.
- Promote only with traceable evidence and a rollback path.

## Simulation and real-system integration

Simulation is not an offline ornament. It is the place where the model is challenged before it touches a real system.

The integration pattern is:

- Use Omniverse, Isaac Sim, OpenUSD, and SimReady workflows to create simulation-ready assets and environments.
- Use `neural-asset-reconstruction` to decide when to invoke `NVIDIA/skills` and OVRTX routes for Physical AI neural reconstruction, NuRec/NRE, NCore, Asset Harvester, Content Agents material/physics/texture/validation, CAD-to-SimReady, OVRTX headless previews/videos/sensor simulation, video augmentation, and defect image generation.
- Use Content Agents-style material and physics assignment where it reduces manual authoring burden, with validation before use.
- Use Cosmos Generator and action modes to create candidate futures, synthetic variations, and policy rollouts.
- Use FlashDreams for interactive autoregressive world-model rollouts where the simulator or operator loop needs real-time response.
- Use OSMO to orchestrate multi-stage workflows that combine simulation, synthetic data, model training, evaluation, and edge or hardware-in-the-loop testing.
- Use real-system telemetry to identify simulator gaps.
- Use simulator failures to drive targeted data collection and post-training.

## Deployment strategy

The deployment path depends on latency, data sensitivity, model surface, and integration target:

- Hosted or private NIM for production endpoints where the model and mode are supported.
- FlashDreams for high-performance interactive video and world-model inference where streaming or self-forcing behaviour is required.
- Cosmos Framework inference for research, custom checkpoint validation, and workflows not yet covered by NIM.
- vLLM or Transformers surfaces for OpenAI-compatible reasoner endpoints where appropriate.
- Edge or workstation deployment only after model size, latency, thermal budget, fail-safe behaviour, and monitoring are proven.

Every deployment path must include observability, access control, model versioning, input and output retention policy, runtime guardrails, and a rollback path.

## Success criteria

A programme is ready for controlled deployment when it can show:

- The data was selected for the autonomy objective and operating domain.
- The training and evaluation sets are separated by scenario, platform, and time where needed.
- The adapted model improves on the baseline for the target task without unacceptable regressions.
- Simulation and real-world evaluation agree on the main failure modes.
- Safety and governance reviewers can reproduce the evidence trail.
- Agents can operate the workflow without exceeding their documented authority.
