# Quickstart

Use this path to validate a fresh checkout, prepare the manifest workspace, and run the first governed agent workflow.

## Clone

```bash
git clone git@github.com:hcltech-robotics/world-model-blueprint.git
cd world-model-blueprint
```

## Validate the repository

```bash
make validate
make skill-audit
make benchmarks
```

## Build the documentation site

```bash
python3 -m pip install -e ".[docs]"
make site
```

The generated static site is written to `site/`.

## Configure the LLM runtime

```bash
cp deploy/.env.example deploy/.env
```

Set one of the runtime keys in `deploy/.env`:

```bash
WMB_LLM_API_KEY=
NVIDIA_API_KEY=
WMB_LLM_BASE_URL=https://integrate.api.nvidia.com/v1
WMB_LLM_MODEL=nvidia/nemotron-3-nano-30b-a3b
```

`WMB_LLM_API_KEY` takes precedence. `NVIDIA_API_KEY` is accepted as the default fallback for hosted NVIDIA NIM workflows.

## Set the programme objective

Set the authorised objective before running the agent workflow:

```bash
export WMB_AGENT_OBJECTIVE="Adapt a Cosmos-class world model for the approved autonomy programme."
```

Use the programme's approved wording. Keep sensitive source data and restricted identifiers outside the repository.

## Generate manifest skeletons

```bash
mkdir -p artifacts/manifests
for schema in schemas/*.schema.json; do
  scripts/wmb new-manifest \
    --schema "$schema" \
    --output "artifacts/manifests/$(basename "$schema" .schema.json).json"
done
```

Fill the generated manifests from authorised evidence, then check readiness:

```bash
scripts/wmb readiness-report \
  --root artifacts/manifests \
  --output artifacts/readiness.md
```

## Run the agent workflow

```bash
scripts/wmb agent-workflow \
  --config configs/agent-workflow.json \
  --env-file deploy/.env \
  --evidence-root artifacts/manifests \
  --output artifacts/agent-workflow.md
```

For a focused run, specify the stage:

```bash
scripts/wmb agent-workflow \
  --env-file deploy/.env \
  --evidence-root artifacts/manifests \
  --stage post-training \
  --output artifacts/post-training-agent-plan.md
```

## Use the Launchable path

For a Brev-oriented pilot run:

```bash
scripts/wmb-agent-launchable
```

The Launchable command loads `deploy/.env`, validates the repository, runs the benchmark harness, creates missing manifest skeletons, writes a readiness report, and runs the configured agent workflow over the manifest directory.

## Review outputs

Generated artefacts are written under `artifacts/` and are intentionally ignored by Git. Keep programme-specific evidence, restricted data, and approval records in the controlled programme system, then reference them in manifests.
