# Skill card: Infrastructure orchestration lead

## Capability

Makes training, evaluation, simulation, and inference executable on the right platform with a documented launch contract.

## Trigger inputs

- job objective.
- model and dataset manifests.
- GPU and storage requirements.
- cluster constraints.
- secret-handling policy.

## Produced artefacts

- run request manifest.
- run plan.
- launch contract.
- scheduler or workflow evidence requirements.

## Tools and references

- Schema: `schemas/run-request.schema.json`
- Local check script: `skills/infrastructure-orchestration-lead/scripts/run-checks.sh`
- Operating playbook: `skills/infrastructure-orchestration-lead/references/operating-playbook.md`
- Output contract: `skills/infrastructure-orchestration-lead/references/output-contract.md`
- Benchmark cases: `skills/infrastructure-orchestration-lead/evals/benchmark-cases.json`

## Quality gates

- Manifest validation passes.
- Missing evidence is explicit.
- Human review gates are named.
- Downstream skill handoffs are concrete.
- No operational identifiers or benchmark values are invented.

## Risks and controls

- local path used for multi-node data.
- missing resume path.
- secrets in manifests.
- unverified scheduler account.
- wrong lane for evidence need.
