# Deployment and integration

## Deployment principles

Deploy the world model as a controlled service, not as an experiment embedded in a robot or simulator. The service must have versioned inputs and outputs, access control, observability, model identity, data retention policy, and rollback.

Deployment planning covers both training execution and inference serving. The same model may be trained on a B200-class cluster, evaluated on a smaller GPU pool, orchestrated through OSMO, served through NIM, Dynamo, or FlashDreams, and then integrated into a simulator or real-system shadow path.

Deployment work should begin from validated manifests:

```bash
scripts/wmb validate-manifest --schema schemas/training-run-manifest.schema.json --manifest <training-run-manifest>
scripts/wmb validate-manifest --schema schemas/inference-service-manifest.schema.json --manifest <inference-service-manifest>
scripts/wmb run-plan --request <run-request> --output <run-plan>
```

The templates in `deploy/` provide the shape of the execution lane. Platform owners must resolve account, namespace, storage, image, secret, and endpoint values from controlled systems.

<p align="center">
  <img src="../assets/inference-services.svg" alt="Inference service choices across NIM, FlashDreams, Dynamo, Cosmos Framework, vLLM, and Transformers" width="920">
</p>

## Training execution lanes

### Brev for pilot runs

Use Brev for smaller single-instance work: dataset pilots, captioning, first SFT runs, short evaluations, and inference checks. Brev is appropriate when the job fits on one instance, the team needs a fast managed GPU environment, and the input and output data can be staged through object storage or explicit instance paths.

Do not use Brev for multi-node training. Record the instance type, GPU count, container image, mounted paths, credentials used by handle rather than value, and cleanup status.

Template: [deploy/brev/pilot-run.md](https://github.com/hcltech-robotics/world-model-blueprint/blob/main/deploy/brev/pilot-run.md).

### Local GPU workstations

Use local workstations for smoke tests, schema checks, prompt and caption review, and short framework inference jobs. Local runs are not promotion evidence unless the environment is captured and the run is reproducible.

### Slurm for B200-class clusters

Use Slurm for large SFT, high-throughput evaluation, and long-running adaptation work on managed DGX or on-prem clusters, including B200-class systems. Jobs should be submitted through scheduler-owned allocations, container runtimes such as Pyxis/Enroot where available, and shared storage for datasets, checkpoints, logs, and caches.

Before submission, verify passwordless access to the login node, the target partition or queue, account policy, container image access, shared filesystem paths, and checkpoint cadence. Use one scheduler task per node when the training launcher spawns per-GPU workers itself.

Template: [deploy/slurm/cosmos-training.sbatch](https://github.com/hcltech-robotics/world-model-blueprint/blob/main/deploy/slurm/cosmos-training.sbatch).

### Megatron for massive training

Use Megatron-Core and Megatron Bridge when the programme leaves ordinary SFT scale: very large models, long context, MoE, custom parallelism, large cluster efficiency work, or pretraining-style runs. The deployment plan should name the recipe, entry point, parallelism dimensions, checkpoint format, data path, and performance target.

For Slurm-based Megatron Bridge work, prefer the site-approved Slurm-native launch shape when the script initialises distributed state from Slurm variables. Keep repository, data, checkpoints, logs, Hugging Face cache, and framework cache on shared storage. Use resiliency controls, straggler detection, preemption handling, and memory tuning before launching expensive jobs.

### Kubernetes, Ray, and OSMO

Use Kubernetes for cloud-native GPU platforms, NIM Operator, OSMO workflows, and production-adjacent inference. Use Ray or NeMo-RL-style launchers when the job is inherently distributed and benefits from cluster lifecycle management. Use OSMO when the workflow spans physical AI data generation, simulation, model training, evaluation, hardware-in-the-loop, or edge testing across heterogeneous compute.

Before applying jobs, verify GPU operator or device plugin state, storage class, image-pull secrets, service accounts, namespace policy, node placement, OSMO pool state, data credentials, workflow YAML, and output dataset policy.

Templates: [deploy/kubernetes/inference-service.yaml](https://github.com/hcltech-robotics/world-model-blueprint/blob/main/deploy/kubernetes/inference-service.yaml) and [deploy/osmo/world-model-workflow.yaml](https://github.com/hcltech-robotics/world-model-blueprint/blob/main/deploy/osmo/world-model-workflow.yaml).

### SkyPilot and cloud-agnostic launchers

Use SkyPilot-style launchers where the team needs portable execution across cloud GPU providers. Spot or preemptible capacity is acceptable only with short checkpoint intervals and a tested resume path.

## Deployment surfaces

### NIM

Use NIM when the selected model surface is available and the deployment needs production-grade serving. NIM is the preferred path for standardised deployment, OpenAI-compatible APIs where supported, container lifecycle management, and integration with enterprise infrastructure.

### Cosmos Framework inference

Use Cosmos Framework inference for custom checkpoints, research validation, batch generation, and workflows that need the framework's current mode support before a NIM path exists.

### vLLM and Transformers

Use vLLM or Transformers for reasoner serving where the model, checkpoint, and runtime are validated for the workload. This path is useful for OpenAI-compatible reasoner endpoints and controlled research services.

### FlashDreams

Use FlashDreams for high-performance interactive inference and serving of autoregressive video and world models. It is the preferred lane for self-forcing, streaming video generation, interactive driving or robotics worlds, and closed-loop simulation where latency matters.

FlashDreams deployments must record runner slug, model integration, checkpoint source, GPU memory requirement, cache policy, context parallelism, CUDA graph settings, decoder path, and frame-rate target. Interactive serving still requires access control, observability, safety limits, and rollback.

### Dynamo

Use NVIDIA Dynamo-style Kubernetes recipes where the serving target is a production-grade, OpenAI-compatible inference deployment on a GPU cluster and an existing recipe matches the model, backend, GPU type, and deployment mode. Validate recipes, secrets, model-cache storage, GPU resources, and health endpoints before routing users or simulators to the service.

### Edge and workstation deployment

Edge deployment requires a separate readiness decision. The model must meet latency, power, thermal, memory, reliability, and fail-safe constraints. Edge deployment should begin in shadow mode or simulator-in-the-loop before real-system authority is granted.

## Integration targets

### Simulation

The model integrates with Omniverse, Isaac Sim, custom OpenUSD simulators, replay systems, and scenario generation tools. Simulation should be used for regression, safety testing, counterfactual analysis, and closed-loop rollout review.

### Real systems

Real-system integration starts in observation mode. The model may provide captions, forecasts, candidate rollouts, risk scores, or review signals before it is allowed to influence control. Any movement from advisory to control-adjacent use requires safety review.

### Human review

Human review consoles should show source data, model output, confidence or uncertainty where available, version identity, scenario metadata, and previous related failures. Review decisions become data for the next curation cycle.

## Operations

Operational controls include:

- Model registry and artefact storage.
- Runtime configuration registry.
- Training job registry with execution lane, scheduler or instance identity, container image, data manifest, and checkpoint policy.
- Access control and credential management.
- Observability for latency, throughput, error rates, GPU use, queue depth, and output classes.
- Inference acceleration records, including precision, cache strategy, parallelism, graph capture, batch policy, and serving backend.
- Evaluation drift monitoring.
- Incident capture and rollback.
- Periodic review of data rights, retention, and safety limits.

## Promotion stages

1. Offline evaluation against held-out data.
2. Simulator evaluation with scenario replay and stress cases.
3. Shadow deployment against real-system observations.
4. Human-reviewed advisory mode.
5. Limited operational use within the approved scope.
6. Expanded use only after new evidence and review.

Each stage needs its own exit criteria. Do not reuse a simulator-only promotion decision as permission for real-system authority.
