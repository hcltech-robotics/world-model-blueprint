# Infrastructure and execution

## Purpose

A world model blueprint is not complete until it says where the work runs. The infrastructure plan covers training, evaluation, inference, simulation, and agent-operated workflows across small pilot environments and large production clusters.

Use the run planner before committing to an execution lane:

```bash
scripts/wmb new-manifest --schema schemas/run-request.schema.json --output artifacts/run-request.json
scripts/wmb run-plan --request artifacts/run-request.json --output artifacts/run-plan.json
```

The planner is deliberately conservative. It routes by workload type, scale, node count, real-time needs, hardware-in-the-loop requirements, and workflow orchestration needs. It does not replace platform-owner review.

<p align="center">
  <img src="assets/execution-lanes.svg" alt="Execution lane selection across Brev, B200 Slurm, Megatron, OSMO, Kubernetes, Ray, NIM, Dynamo, and FlashDreams" width="920">
</p>

## Execution matrix

| Environment | Best fit | Avoid when |
| --- | --- | --- |
| Local GPU workstation | Smoke tests, prompt work, caption inspection, small inference checks, data schema validation | The run must become promotion evidence or requires multi-node training. |
| Brev managed GPU instance | Pilot SFT, single-node multi-GPU runs, short evaluation, reproducible demos, temporary GPU access | The run requires multi-node coordination, shared filesystem semantics, or long-lived production service hosting. |
| B200-class Slurm cluster | Large Cosmos SFT, long-running adaptation, high-throughput evaluation, checkpoint generation, team-owned production training | Data is not on shared storage, SSH and scheduler access are not ready, or checkpoint/restart policy is undefined. |
| Megatron on Slurm or Kubernetes | Massive distributed training, long context, MoE, high-throughput scale-out, and performance-critical training | The task is only a pilot SFT run or the team cannot operate parallelism, checkpointing, and resiliency controls. |
| Kubernetes GPU cluster | NIM Operator, OSMO, Ray, cloud-native training, inference services, production-adjacent workloads | GPU scheduling, storage classes, namespaces, secrets, pools, and observability are not already governed. |
| FlashDreams runtime | Interactive autoregressive video, self-forcing world generation, closed-loop simulation, real-time operator preview | The target can tolerate batch latency or the model cannot meet the required memory and latency profile. |
| SkyPilot-managed cloud | Portable cloud training and experiments across providers | Spot interruption would be unacceptable or checkpoint resume has not been tested. |

## Brev lane

Brev is the small-run lane. Use it for early Cosmos Framework SFT runs, captioning pilots, TAO-assisted annotation, smaller evaluations, and inference experiments where a managed single instance is enough.

Operational requirements:

- `brev` CLI access and authenticated session.
- Explicit GPU type and count.
- Object storage or verified instance-local paths for data movement.
- NGC and Hugging Face credentials passed through environment or secret mechanisms, never committed.
- Clear lifecycle: create or reuse instance, run, collect artefacts, stop or delete.

The Brev lane should produce the same run manifest as larger lanes: source data, model, recipe, container image, command, environment, checkpoint location, and output artefacts.

## B200-class Slurm lane

B200-class clusters are the large-run lane for expensive training and evaluation. They are appropriate when the work needs multiple nodes, high memory, fast interconnect, shared storage, and scheduler-managed capacity.

Operational requirements:

- Passwordless SSH to a Slurm login node.
- Approved account, partition, wall time, and node or GPU request.
- Container image strategy, typically with Pyxis/Enroot or the site-approved equivalent.
- Shared filesystem paths for datasets, checkpoints, logs, Hugging Face cache, and framework cache.
- NGC and Hugging Face credentials handled through the site-approved secret path.
- Checkpoint cadence aligned with queue policy and failure recovery.
- Run log capture and post-run artefact collection.

The launch contract must record node count, GPUs per node, rendezvous settings, master port policy, container mounts, dataset paths, output paths, and scheduler job id. Do not invent scheduler ids or cluster names in documentation.

## Megatron massive-training lane

Megatron-Core and Megatron Bridge are the massive-training lane. Use them when scale, context length, model size, MoE routing, or cluster efficiency requires explicit distributed training architecture.

Operational requirements:

- Recipe selection for pretraining, SFT, PEFT, or performance benchmarking.
- Parallelism plan covering tensor, pipeline, context, expert, and data parallelism.
- Hardware-topology mapping, especially keeping tensor parallelism inside an NVLink domain where possible.
- Checkpoint format and conversion plan.
- Fault tolerance, straggler detection, preemption policy, and restart policy.
- Memory plan covering activation recompute, FSDP, optimizer sharding, and allocator settings.
- Performance plan covering communication overlap, CUDA graph compatibility, and regression thresholds.

Do not present throughput benchmark recipes as production training recipes. They are useful for capacity planning and upper-bound performance, not as a substitute for a governed model adaptation run.

## Kubernetes and Ray lane

Kubernetes is the service and cloud-native workflow lane. Use it for NIM Operator, OSMO, Ray-based jobs, Dynamo inference recipes, and environments where training and serving share cluster services.

Operational requirements:

- Reachable kubeconfig or in-cluster service account.
- GPU operator or device plugin with allocatable GPUs.
- Namespace, service account, storage class, and image-pull secret.
- Model-cache persistent volume policy.
- Health and readiness checks for services.
- Log and metrics collection.

Ray-based launchers should distinguish one-shot jobs from long-lived clusters. Long-lived clusters are useful for development loops and repeated runs; ephemeral jobs are safer for one-off training.

## OSMO lane

OSMO is the preferred orchestration layer when a workflow crosses the Physical AI stack: synthetic or real data, simulation, training, evaluation, edge testing, and hardware-in-the-loop. It is especially useful when one programme needs to run the same workflow across local, cloud, on-prem, and edge compute without rewriting the pipeline.

Operational requirements:

- OSMO CLI access and authenticated profile.
- Registered compute pools for the required platforms.
- Dataset and storage credentials for each backend.
- Workflow YAML with explicit task images, platforms, resources, dependencies, inputs, and outputs.
- Output dataset policy, including versioning and retention.
- Preflight checks for pools, credentials, image access, and workflow interpolation values.

Use OSMO for multi-stage data factories, Isaac Sim synthetic data generation, reinforcement learning, model training, model evaluation, HIL validation, and workflow automation. Do not use it as a substitute for model governance; it orchestrates the work, but promotion still depends on the evidence.

## Inference lane

Inference should be planned before large training begins. The supported serving path determines export format, checkpoint handling, model loading, latency tests, observability, and rollback.

Preferred serving order:

1. NIM for production endpoints where the selected Cosmos model and mode are supported.
2. FlashDreams for interactive autoregressive video or world-model serving, including self-forcing and closed-loop simulation.
3. Dynamo recipes for Kubernetes-hosted OpenAI-compatible inference where a validated recipe matches the model and GPU profile.
4. vLLM or Transformers for reasoner endpoints where the checkpoint and runtime are validated.
5. Cosmos Framework inference for custom checkpoints, research jobs, batch generation, and modes not yet covered by production serving.

Every inference deployment needs input and output schemas, model identity, versioned runtime configuration, access control, monitoring, evaluation drift checks, and a rollback target.

## Inference acceleration

The acceleration plan should be explicit for every serving path:

- NIM optimised containers for supported model surfaces.
- FlashDreams AR cache, KV cache, context parallelism, classifier-free guidance parallelism, streaming decoder, and CUDA graph wrapping for interactive rollouts.
- vLLM batching and cache management for reasoner endpoints.
- Tensor parallel, context parallel, pipeline parallel, and data-parallel sharding where the backend supports them.
- BF16 or other validated precision settings.
- Model-cache placement near GPUs.
- Smoke tests for OpenAI-compatible endpoints where applicable.

## Execution manifest

Every training, evaluation, or inference run should record:

- Execution lane.
- Hardware profile.
- Container image or environment.
- Source model and checkpoint.
- Dataset manifest.
- Recipe or serving configuration.
- Secrets referenced by handle, not value.
- Cache, data, checkpoint, and log paths.
- OSMO workflow id or scheduler job id where applicable.
- Inference backend, runner, cache, parallelism, precision, and acceleration settings.
- Job or instance identifier created by the platform.
- Output artefacts.
- Reviewer and promotion status.

The execution manifest should be validated before launch, and the resulting run plan should be archived with the training, evaluation, or deployment record.
