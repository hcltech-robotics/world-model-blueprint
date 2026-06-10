#!/usr/bin/env bash
#SBATCH --job-name=world-model-training
#SBATCH --nodes=<node-count>
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-node=<gpus-per-node>
#SBATCH --time=<walltime>
#SBATCH --partition=<partition>
#SBATCH --account=<account>
#SBATCH --output=<log-dir>/%x-%j.out
#SBATCH --error=<log-dir>/%x-%j.err

set -euo pipefail

module purge

export WORLD_MODEL_MANIFEST="<training-run-manifest>"
export WORLD_MODEL_OUTPUT_DIR="<checkpoint-dir>"
export WORLD_MODEL_DATA_DIR="<dataset-dir>"
export WORLD_MODEL_CACHE_DIR="<cache-dir>"

python3 -m world_model_blueprint.cli validate-manifest \
  --schema schemas/training-run-manifest.schema.json \
  --manifest "${WORLD_MODEL_MANIFEST}"

# Site owners replace this block with the approved Cosmos Framework,
# Megatron Bridge, or Megatron-Core launch command.
srun --container-image="<container-image>" \
  --container-mounts="<mounts>" \
  bash -lc '<training-command>'
