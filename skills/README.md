# Agent skills

This directory contains the blueprint's production agent skills. Each skill is intentionally bounded and supplied with operational resources: activation instructions, a governance card, a benchmark description, detailed references, eval cases, metadata, and a runnable manifest check script.

The skills are designed to get an autonomy programme all the way from data and physical assets to a deployable world-model capability:

1. Analyse existing real data, simulator output, CAD/OpenUSD assets, logs, actions, telemetry, rights, and gaps.
2. Create the data factory and simulation pipeline that can produce model-ready evidence.
3. Route neural reconstruction, Content Agents enrichment, OVRTX headless rendering, CAD-to-SimReady conversion, harvested object assets, video augmentation, and generated defect examples through the appropriate upstream NVIDIA/skills or OVRTX capability.
4. Convert the business's physical differentiators into SimReady assets, scenarios, and synthetic-data workflows.
5. Plan Cosmos-class post-training, checkpoint export, evaluation, and promotion.
6. Select the right execution lane, from Brev pilots to B200-class Slurm, Megatron, OSMO, Kubernetes, or Ray.
7. Serve the model efficiently through NIM, FlashDreams, Dynamo, Cosmos Framework inference, vLLM, Transformers, or an approved edge path.
8. Feed deployment and simulator evidence back into the next curation, training, and safety cycle.

## Skill set

| Skill | Responsibility |
| --- | --- |
| `autonomy-data-strategist` | Frame the autonomy objective, data gaps, rights constraints, and adaptation hypothesis. |
| `world-model-data-factory` | Plan curation, enrichment, annotation, captioning, synthetic variation, and dataset release gates. |
| `neural-asset-reconstruction` | Route NuRec/NRE, Content Agents, OVRTX headless rendering, CAD-to-SimReady, object harvesting, augmentation, and generated asset work to `NVIDIA/skills` or `NVIDIA-Omniverse/ovrtx/skills`. |
| `simready-content-integration` | Plan CAD, OpenUSD, SimReady, Omniverse, Isaac Sim, and simulation scenario integration. |
| `cosmos-post-training-lead` | Plan Cosmos 3-class SFT, action modelling, checkpoint export, and evaluation handoff. |
| `infrastructure-orchestration-lead` | Select Brev, OSMO, Slurm, Megatron, Kubernetes, Ray, or local execution lanes. |
| `real-time-inference-lead` | Select NIM, FlashDreams, Dynamo, Cosmos Framework, vLLM, or Transformers serving lanes. |
| `evaluation-safety-lead` | Define offline, simulation, shadow, advisory, and operational promotion gates. |
| `deployment-operations-lead` | Plan production deployment, integration, observability, rollback, and incident controls. |
| `governance-provenance-lead` | Maintain rights, lineage, privacy, export-control, safety, and audit evidence. |

## Package anatomy

Each skill directory contains:

| Path | Purpose |
| --- | --- |
| `SKILL.md` | Activation criteria, required inputs, repository tools, workflow, output contract, quality gates, and stop conditions. |
| `skill-card.md` | Human-readable capability, artefacts, tools, risks, and controls. |
| `BENCHMARK.md` | Evaluation cases and pass criteria for the skill. |
| `benchmark/evals.json` | Evaluator scenarios with questions, expected skill, optional script, ground truth, and expected behaviours. |
| `references/operating-playbook.md` | Detailed operating procedure and handoff rules. |
| `references/output-contract.md` | Required deliverable structure and acceptance criteria. |
| `scripts/run-checks.sh` | Schema-specific manifest validation wrapper. |
| `evals/benchmark-cases.json` | Lightweight skill evaluation metadata. |
| `agents/openai.yaml` | UI-facing skill metadata. |

## Outcome coverage

| Outcome | Primary skills |
| --- | --- |
| SimReady assets for business differentiators | `neural-asset-reconstruction`, `simready-content-integration`, `world-model-data-factory`, `governance-provenance-lead` |
| Fine-tuned Cosmos-class world model | `autonomy-data-strategist`, `world-model-data-factory`, `cosmos-post-training-lead`, `evaluation-safety-lead` |
| Efficient inference in simulation and real-system workflows | `real-time-inference-lead`, `infrastructure-orchestration-lead`, `deployment-operations-lead`, `evaluation-safety-lead` |
| Continuous sim-to-real improvement loop | All skills, with governance and evaluation as persistent gates |

## Common operating standard

- Use programme records and source-controlled manifests as the source of truth.
- Do not invent names, identifiers, data, accounts, cluster details, or benchmark values.
- Do not expose secrets or private data in responses, logs, manifests, or repository files.
- Stop for human review before model promotion, real-system integration, external publication, or destructive infrastructure actions.
- Produce concise artefacts that can be reviewed by engineering, safety, legal, and operations leaders.
