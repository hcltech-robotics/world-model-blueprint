# Output contract: SimReady content integration

## Required deliverable

Primary output: Simulation asset integration plan and SimReady asset manifest.

## Minimum sections

1. **Decision**: what the skill recommends and why.
2. **Evidence used**: source records, manifests, logs, registry outputs, and owner approvals used in the decision.
3. **Missing evidence**: required fields or controls not yet available.
4. **Risk position**: rights, privacy, safety, operational, regulatory, and deployment risks.
5. **Commands**: concrete repository commands for validation, manifest creation, readiness reporting, or run planning.
6. **Handoffs**: downstream skills and the artefacts they receive.
7. **Review gates**: where a human owner must approve before work proceeds.

## Artefact checklist

- SimReady asset manifest.
- asset conversion plan.
- validation plan.
- scenario catalogue.
- synthetic data interface.

## Acceptance criteria

- Required manifest validates against `schemas/simready-asset-manifest.schema.json`.
- No invented names, identifiers, records, paths, or benchmark values are present.
- All assumptions are marked as missing evidence or review items.
- The next operator can run the listed commands without needing to infer repository structure.
- The output is concise enough for an executive review but specific enough for an engineer to execute.
