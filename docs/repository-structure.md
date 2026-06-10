# Repository structure

## Top-level layout

| Path | Purpose |
| --- | --- |
| `README.md` | Entry point and executive overview. |
| `docs/` | Blueprint documentation, architecture, governance, data, deployment, toolchain, and source map. |
| `skills/` | Agent skills with cards, references, scripts, benchmarks, evals, and metadata. |
| `schemas/` | JSON contracts for programme, data, neural assets, SimReady assets, training, inference, evaluation, governance, and run planning. |
| `configs/` | Agent workflow and LLM runtime configuration. |
| `src/world_model_blueprint/` | Python CLI package used by agents and CI. |
| `scripts/` | Repository command wrappers, validation, agent workflow execution, and Launchable automation. |
| `benchmarks/` | Benchmark specification and runner. |
| `deploy/` | Brev, Slurm, Kubernetes, and OSMO templates. |
| `.github/workflows/` | Continuous validation workflow. |

## Release expectations

Before a release or handoff:

1. Run `make format-check`.
2. Run `make validate`.
3. Run `make skill-audit`.
4. Run `make benchmarks`.
5. Run `scripts/wmb agent-workflow --dry-run` or the Brev Launchable path when agent orchestration changed.
6. Review generated artefacts under `artifacts/` or the configured Launchable artefact root.

The repository should remain free of private data, secrets, operational identifiers, customer names, scheduler ids, endpoint ids, gated model weights, and unsupported benchmark claims.
