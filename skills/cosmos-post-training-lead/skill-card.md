# Skill card: Cosmos post-training lead

## Capability

Turns model-ready evidence into a governed Cosmos-class adaptation plan that can run and be served.

## Trigger inputs

- programme intake manifest.
- dataset manifest.
- base model and license.
- recipe candidate.
- serving target.

## Produced artefacts

- training run manifest.
- recipe selection.
- checkpoint policy.
- export plan.
- evaluation handoff.

## Tools and references

- Schema: `schemas/training-run-manifest.schema.json`
- Local check script: `skills/cosmos-post-training-lead/scripts/run-checks.sh`
- Operating playbook: `skills/cosmos-post-training-lead/references/operating-playbook.md`
- Output contract: `skills/cosmos-post-training-lead/references/output-contract.md`
- Benchmark cases: `skills/cosmos-post-training-lead/evals/benchmark-cases.json`

## Quality gates

- Manifest validation passes.
- Missing evidence is explicit.
- Human review gates are named.
- Downstream skill handoffs are concrete.
- No operational identifiers or benchmark values are invented.

## Risks and controls

- training before baseline evaluation.
- checkpoint that cannot be served.
- action schema mismatch.
- parallelism plan absent.
- no rollback target.
