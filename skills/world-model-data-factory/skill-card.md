# Skill card: World model data factory

## Capability

Converts real, simulated, and synthetic observations into model-ready evidence with repeatable quality gates.

## Trigger inputs

- source manifests.
- sensor/action schemas.
- caption and label sources.
- rights records.
- simulation output.

## Produced artefacts

- dataset manifest.
- curation plan.
- split policy.
- augmentation strategy.
- release gate record.

## Tools and references

- Schema: `schemas/dataset-manifest.schema.json`
- Local check script: `skills/world-model-data-factory/scripts/run-checks.sh`
- Operating playbook: `skills/world-model-data-factory/references/operating-playbook.md`
- Output contract: `skills/world-model-data-factory/references/output-contract.md`
- Benchmark cases: `skills/world-model-data-factory/evals/benchmark-cases.json`

## Quality gates

- Manifest validation passes.
- Missing evidence is explicit.
- Human review gates are named.
- Downstream skill handoffs are concrete.
- No operational identifiers or benchmark values are invented.

## Risks and controls

- train-test leakage.
- weak caption quality.
- missing action semantics.
- synthetic data overwhelming real coverage.
- unresolved consent or license.
