# Skill card: Evaluation safety lead

## Capability

Separates model quality from deployment readiness and makes promotion evidence reproducible.

## Trigger inputs

- candidate model.
- baseline model.
- scenario manifests.
- safety requirements.
- deployment stage.

## Produced artefacts

- evaluation manifest.
- promotion criteria.
- failure review plan.
- rollback triggers.

## Tools and references

- Schema: `schemas/evaluation-manifest.schema.json`
- Local check script: `skills/evaluation-safety-lead/scripts/run-checks.sh`
- Operating playbook: `skills/evaluation-safety-lead/references/operating-playbook.md`
- Output contract: `skills/evaluation-safety-lead/references/output-contract.md`
- Benchmark cases: `skills/evaluation-safety-lead/evals/benchmark-cases.json`

## Quality gates

- Manifest validation passes.
- Missing evidence is explicit.
- Human review gates are named.
- Downstream skill handoffs are concrete.
- No operational identifiers or benchmark values are invented.

## Risks and controls

- aggregate score hides safety regression.
- simulator-only evidence used for operational authority.
- held-out leakage.
- baseline absent.
- failure cases not routed back.
