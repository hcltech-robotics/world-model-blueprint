# Skill card: Real-time inference lead

## Capability

Makes the adapted world model usable in batch, simulator, shadow, advisory, and real-time workflows with explicit acceleration controls.

## Trigger inputs

- checkpoint and export record.
- latency target.
- integration target.
- GPU profile.
- evaluation gate.

## Produced artefacts

- inference manifest.
- backend decision.
- cache and precision plan.
- API contract.
- rollback controls.

## Tools and references

- Schema: `schemas/inference-service-manifest.schema.json`
- Local check script: `skills/real-time-inference-lead/scripts/run-checks.sh`
- Operating playbook: `skills/real-time-inference-lead/references/operating-playbook.md`
- Output contract: `skills/real-time-inference-lead/references/output-contract.md`
- Benchmark cases: `skills/real-time-inference-lead/evals/benchmark-cases.json`

## Quality gates

- Manifest validation passes.
- Missing evidence is explicit.
- Human review gates are named.
- Downstream skill handoffs are concrete.
- No operational identifiers or benchmark values are invented.

## Risks and controls

- checkpoint format unsupported.
- latency target absent.
- cache invalidation untested.
- closed-loop use without safety stage.
- observability absent.
