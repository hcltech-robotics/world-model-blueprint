# Toolchain

## Purpose

The blueprint includes executable tooling so agents can inspect, validate, format, benchmark, and plan work through repository contracts. The tools do not train models or deploy services by themselves; they create the governed artefacts that make those actions reviewable.

## Command entry points

| Command | Purpose |
| --- | --- |
| `scripts/wmb format` | Normalise markdown, JSON, YAML, TOML, Python, and shell files. |
| `scripts/wmb validate-repo` | Validate repository policy, documentation markers, and skill packaging. |
| `scripts/wmb new-manifest` | Generate an empty manifest from a schema. |
| `scripts/wmb validate-manifest` | Validate required fields and basic types for a manifest. |
| `scripts/wmb readiness-report` | Summarise manifest completion across an evidence directory. |
| `scripts/wmb run-plan` | Route a run request across local, Brev, Slurm, Megatron, OSMO, Kubernetes, Ray, and FlashDreams lanes. |
| `scripts/wmb agent-workflow` | Run the agent-driven workflow with an OpenAI-compatible LLM, supplied objective, evidence directory, and local skills. |
| `scripts/wmb skill-audit` | Check skill depth, references, scripts, evals, benchmark files, and agent metadata. |
| `scripts/wmb-agent-launchable` | Prepare a Brev-compatible workspace, run validation and benchmarks, generate manifests, and execute the agent workflow. |

## Make targets

| Target | Command |
| --- | --- |
| Validate repository | `make validate` |
| Check formatting | `make format-check` |
| Apply formatting | `make format` |
| Run benchmark harness | `make benchmarks` |
| Audit skill packaging | `make skill-audit` |

## Operating pattern

1. Generate or locate the relevant manifest.
2. Validate it with the schema-specific command.
3. Produce a readiness report.
4. Use `run-plan` when compute or inference routing is required.
5. Run `agent-workflow` when the programme objective and evidence should be processed by the local skills through a configured LLM.
6. Run `skill-audit` and benchmarks before release.

The toolchain deliberately avoids customer-specific identifiers, secret values, scheduler ids, dataset ids, endpoint ids, and benchmark claims. Those values belong in controlled programme systems and must be copied only from authoritative records.

## Agent runtime

The agent workflow uses `configs/agent-workflow.json` to define the ordered skill stages and LLM settings. By default it targets the NVIDIA hosted NIM-compatible endpoint at `https://integrate.api.nvidia.com/v1` and reads the model from `WMB_LLM_MODEL`.

Required environment:

```bash
cp deploy/.env.example deploy/.env
```

Set either `WMB_LLM_API_KEY` or `NVIDIA_API_KEY` in `deploy/.env`. For local NIM serving, set `WMB_LLM_BASE_URL` to the local `/v1` endpoint and set `WMB_LLM_MODEL` to the served model name. The runner sends the selected skill instructions, skill card, output contract, programme objective, and evidence directory to the model; it does not send secret values from the environment.
