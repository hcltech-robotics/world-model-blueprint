# Deployment templates

This directory contains deployment templates for the execution lanes described by the blueprint. Templates intentionally avoid concrete customer identifiers, cluster names, credentials, paths, or account values.

## Lanes

| Lane | Template |
| --- | --- |
| Brev pilot execution | [brev/pilot-run.md](brev/pilot-run.md) |
| Brev Launchable workflow | [brev/launchable-workflow.md](brev/launchable-workflow.md) and [brev/world-model-launchable.ipynb](brev/world-model-launchable.ipynb) |
| B200-class Slurm and Megatron | [slurm/cosmos-training.sbatch](slurm/cosmos-training.sbatch) |
| Kubernetes inference | [kubernetes/inference-service.yaml](kubernetes/inference-service.yaml) |
| OSMO workflow orchestration | [osmo/world-model-workflow.yaml](osmo/world-model-workflow.yaml) |

Each lane must be resolved by the infrastructure owner before use. Do not record secret values in these templates or in generated manifests.
