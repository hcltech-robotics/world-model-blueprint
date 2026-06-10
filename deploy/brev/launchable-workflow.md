# Brev Launchable workflow

## Purpose

The Brev Launchable path runs the pilot version of the blueprint workflow in a single GPU development environment. It is intended for programme intake, evidence review, manifest preparation, agent-driven planning, small data-factory experiments, smoke tests, and smaller Cosmos-class adaptation runs. Larger post-training jobs remain routed through the Slurm, Megatron, OSMO, or Kubernetes templates.

## Runtime contract

The Launchable uses the repository as the control plane and stores generated artefacts outside the checkout where possible.

| Area | Default |
| --- | --- |
| Source checkout | Repository root |
| Generated artefacts | `/ephemeral/world-model-blueprint/${USER}/artifacts` when `/ephemeral` exists |
| Shared caches | `/ephemeral/world-model-blueprint/${USER}/cache` when `/ephemeral` exists |
| Environment file | `deploy/.env` |
| Agent workflow config | `configs/agent-workflow.json` |
| Launch command | `scripts/wmb-agent-launchable` |

## Environment

Create the environment file from the template:

```bash
cp deploy/.env.example deploy/.env
```

Set either `WMB_LLM_API_KEY` or `NVIDIA_API_KEY`. The default endpoint is the NVIDIA hosted NIM-compatible API at `https://integrate.api.nvidia.com/v1`; set `WMB_LLM_BASE_URL` to a local NIM endpoint when self-hosting.

Set `WMB_AGENT_OBJECTIVE` to the programme objective before running the Launchable. Keep secrets in `deploy/.env` or the Brev secret manager; do not copy them into manifests, reports, notebooks, or logs.

## Run

```bash
scripts/wmb-agent-launchable
```

The command:

1. Loads `deploy/.env` without printing secret values.
2. Places caches and generated artefacts under `/ephemeral` when available.
3. Runs repository validation, skill audit, and benchmark harness.
4. Generates empty manifests for every schema that does not yet have an evidence file.
5. Produces a readiness report.
6. Runs the agent workflow over the manifest directory using the configured LLM.

If no LLM API key is present, the command runs the agent workflow in dry-run mode and writes the prompt package that would be sent to the model. This keeps the Launchable useful for environment validation without leaking or fabricating credentials.

## Outputs

| Output | Purpose |
| --- | --- |
| `reports/readiness.md` | Manifest completeness and missing evidence summary. |
| `reports/agent-workflow.md` | Agent-generated programme plan, missing evidence, review gates, commands, and handoffs. |
| `reports/benchmark-report.json` | Repository benchmark output from the standard harness. |
| `reports/skill-audit.json` | Skill packaging audit result. |

Generated outputs are programme artefacts. Move them into the appropriate controlled system before using them as review evidence.
