# Skill card: SimReady content integration

## Capability

Turns physical differentiators into simulation-ready assets and scenario evidence for world-model training and evaluation.

## Trigger inputs

- CAD or OpenUSD assets.
- robot or machine description.
- materials and textures.
- physics requirements.
- scenario requirements.

## Produced artefacts

- SimReady asset manifest.
- asset conversion plan.
- validation plan.
- scenario catalogue.
- synthetic data interface.

## Tools and references

- Schema: `schemas/simready-asset-manifest.schema.json`
- Local check script: `skills/simready-content-integration/scripts/run-checks.sh`
- Operating playbook: `skills/simready-content-integration/references/operating-playbook.md`
- Output contract: `skills/simready-content-integration/references/output-contract.md`
- Benchmark cases: `skills/simready-content-integration/evals/benchmark-cases.json`

## Quality gates

- Manifest validation passes.
- Missing evidence is explicit.
- Human review gates are named.
- Downstream skill handoffs are concrete.
- No operational identifiers or benchmark values are invented.

## Risks and controls

- asset rights ambiguity.
- unvalidated physics.
- poor USD performance.
- mismatch between simulated and measured behaviour.
- scenario catalogue not linked to evaluation.
