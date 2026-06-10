# Skill card: Governance provenance lead

## Capability

Makes the end-to-end world-model capability defensible to engineering, safety, regulatory, legal, and operations leaders.

## Trigger inputs

- license records.
- data manifests.
- model manifests.
- evaluation decisions.
- deployment records.

## Produced artefacts

- governance record.
- artefact lineage map.
- approval gate map.
- retention and access policy.

## Tools and references

- Schema: `schemas/governance-record.schema.json`
- Local check script: `skills/governance-provenance-lead/scripts/run-checks.sh`
- Operating playbook: `skills/governance-provenance-lead/references/operating-playbook.md`
- Output contract: `skills/governance-provenance-lead/references/output-contract.md`
- Benchmark cases: `skills/governance-provenance-lead/evals/benchmark-cases.json`

## Quality gates

- Manifest validation passes.
- Missing evidence is explicit.
- Human review gates are named.
- Downstream skill handoffs are concrete.
- No operational identifiers or benchmark values are invented.

## Risks and controls

- unlicensed derivative data.
- privacy review absent.
- lineage break.
- approval record missing.
- secret exposure.
