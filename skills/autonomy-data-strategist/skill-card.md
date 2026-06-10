# Skill card: Autonomy data strategist

## Capability

Frames an open-ended autonomy ambition as a precise model, data, simulation, safety, and deployment brief.

## Trigger inputs

- autonomy objective.
- embodiment and sensor profile.
- operating domain.
- existing data and assets.
- known safety and regulatory context.

## Produced artefacts

- programme intake manifest.
- model-surface decision.
- evidence gap map.
- next-skill routing plan.

## Tools and references

- Schema: `schemas/programme-intake-manifest.schema.json`
- Local check script: `skills/autonomy-data-strategist/scripts/run-checks.sh`
- Operating playbook: `skills/autonomy-data-strategist/references/operating-playbook.md`
- Output contract: `skills/autonomy-data-strategist/references/output-contract.md`
- Benchmark cases: `skills/autonomy-data-strategist/evals/benchmark-cases.json`

## Quality gates

- Manifest validation passes.
- Missing evidence is explicit.
- Human review gates are named.
- Downstream skill handoffs are concrete.
- No operational identifiers or benchmark values are invented.

## Risks and controls

- unclear deployment authority.
- unsupported model surface.
- missing rights record.
- ambiguous safety owner.
- over-broad target capability.
