# Governance

## Governance objective

World model adaptation for autonomy must be governed as a safety, data, and deployment system. Governance is not a final approval meeting; it is a continuous record of what data was used, why it was lawful and appropriate, how the model changed, what risks remain, and what deployment scope is permitted.

Use the governance record schema to make the audit trail explicit:

```bash
scripts/wmb new-manifest --schema schemas/governance-record.schema.json --output artifacts/governance-record.json
scripts/wmb readiness-report --root artifacts --output artifacts/readiness.md
```

## Required records

Each model promotion should have:

- Autonomy objective and approved deployment scope.
- Data manifest with rights, source, sensitivity, and split information.
- Training manifest with recipe, checkpoint, environment, and configuration.
- Evaluation manifest with datasets, scenarios, metrics, and failures.
- Safety review with limitations and accepted risks.
- Deployment manifest with runtime, endpoint, access policy, and rollback.
- Agent activity record where agents contributed to the workflow.

## Data governance

Data must be classified before curation:

- Ownership and permitted use.
- Consent and privacy status.
- Medical, safety-critical, export-controlled, or contractual sensitivity.
- Retention and deletion requirements.
- Restrictions on derivative synthetic data.
- Approval state for training, evaluation, or deployment monitoring.

Sensitive data should be processed in controlled environments with least-privilege access. Secrets must not be written into prompts, logs, skills, notebooks, or documentation.

## Model governance

Every adapted checkpoint must be traceable to:

- Base model and license.
- Training data and transformation lineage.
- Training recipe and runtime.
- Evaluation evidence.
- Known limitations.
- Deployment scope.
- Rollback artefact.

No model should be promoted on aggregate scores alone. Promotion must consider scenario slices, rare events, safety failures, regression against the previous model, and real versus synthetic performance.

## Agent governance

Agents should be governed like production automation:

- Skills have named owners.
- Skill cards describe outputs and risks.
- Agents operate under least privilege.
- Human review gates are explicit.
- Agent-generated artefacts are reviewed before use in training, deployment, or safety acceptance.
- Signing, scanning, and benchmark claims require actual artefacts and controlled release records.

## Safety posture

For autonomy, the safe default is advisory use. A world model may support analysis, simulation, review, and forecasting before it is allowed near control. Control-adjacent use requires a separate safety case, runtime monitoring, fail-safe design, and approval from the responsible engineering and safety owners.
