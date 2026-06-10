# Operating playbook: Governance provenance lead

## Role in the blueprint

Role: make the end-to-end world-model capability defensible to engineering, safety, regulatory, legal, and operations leaders.

## Decision model

Use the following sequence for every engagement:

1. **Scope**: determine whether the current request belongs to this skill or should be routed to an upstream owner.
2. **Evidence**: list the records already available and the records that are required by `schemas/governance-record.schema.json`.
3. **Risk**: identify safety, privacy, rights, export-control, operational, and deployment risks.
4. **Action**: produce only actions that can be executed through repository tools, controlled platform tools, or named human review.
5. **Handoff**: name the downstream skill and the exact artefact it should receive.

## Tool procedure

```bash
scripts/wmb new-manifest --schema schemas/governance-record.schema.json --output artifacts/governance-provenance-lead.json
scripts/wmb validate-manifest --schema schemas/governance-record.schema.json --manifest artifacts/governance-provenance-lead.json
scripts/wmb readiness-report --root artifacts --output artifacts/readiness.md
```

For execution-lane decisions, use:

```bash
scripts/wmb run-plan --request artifacts/run-request.json --output artifacts/run-plan.json
```

For repository release checks, use:

```bash
scripts/wmb skill-audit --root . --output artifacts/skill-audit.json
python3 benchmarks/run_benchmarks.py --output artifacts/benchmark-report.json
```

## Evidence table

| Evidence class | Acceptable source | Not acceptable |
| --- | --- | --- |
| Data or asset identity | Controlled manifest, registry, storage inventory, source-control path | Invented names, unreviewed notes, inaccessible paths |
| Rights and permitted use | Legal, programme, quality, or asset-owner record | Informal assumption |
| Safety scope | Safety case, hazard analysis, approved stage gate | Generic statement that the system is safe |
| Platform identity | Actual scheduler, OSMO, Kubernetes, Brev, or registry output | Guessed account, partition, job id, namespace, or endpoint |
| Model identity | Model registry, checkpoint manifest, license record | Local filename without lineage |

## Handoff rules

- Handoff to `world-model-data-factory` when the blocker is data quality, split policy, annotation, or enrichment.
- Handoff to `simready-content-integration` when the blocker is digital-twin fidelity, OpenUSD, SimReady validation, or scenario coverage.
- Handoff to `cosmos-post-training-lead` when the blocker is recipe, checkpoint, model surface, or export.
- Handoff to `infrastructure-orchestration-lead` when the blocker is compute lane, scheduler, storage, or workflow orchestration.
- Handoff to `real-time-inference-lead` when the blocker is serving backend, latency, cache, precision, graph capture, or API contract.
- Handoff to `evaluation-safety-lead` when the blocker is evidence, safety gate, metric, baseline, or promotion.
- Handoff to `deployment-operations-lead` when the blocker is service ownership, observability, incident response, integration, or rollback.
- Handoff to `governance-provenance-lead` when the blocker is rights, privacy, export control, lineage, retention, or approval.
