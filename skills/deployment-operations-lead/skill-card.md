# Skill card: Deployment operations lead

## Capability

Turns a candidate model or service into an operated capability with visible authority boundaries and recovery paths.

## Trigger inputs

- inference manifest.
- evaluation decision.
- integration target.
- access policy.
- operator owner.

## Produced artefacts

- deployment plan.
- integration contract.
- observability plan.
- incident plan.
- rollback plan.

## Tools and references

- Schema: `schemas/inference-service-manifest.schema.json`
- Local check script: `skills/deployment-operations-lead/scripts/run-checks.sh`
- Operating playbook: `skills/deployment-operations-lead/references/operating-playbook.md`
- Output contract: `skills/deployment-operations-lead/references/output-contract.md`
- Benchmark cases: `skills/deployment-operations-lead/evals/benchmark-cases.json`

## Quality gates

- Manifest validation passes.
- Missing evidence is explicit.
- Human review gates are named.
- Downstream skill handoffs are concrete.
- No operational identifiers or benchmark values are invented.

## Risks and controls

- service has no owner.
- rollback target absent.
- authority creep.
- telemetry not captured.
- model identity not visible to operators.
