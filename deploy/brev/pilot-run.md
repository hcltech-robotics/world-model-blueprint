# Brev pilot run template

Use Brev for short single-instance work: dataset inspection, curation pilots, first SFT runs, lightweight evaluation, and inference smoke tests.

## Required inputs

- GPU type and count.
- Container image or repository environment.
- Dataset staging location.
- Output artefact location.
- Secret handles for gated model and registry access.
- Cleanup policy.

## Command shape

```bash
brev open
python3 -m world_model_blueprint.cli validate-manifest --schema schemas/training-run-manifest.schema.json --manifest <manifest>
python3 -m world_model_blueprint.cli run-plan --request <run-request> --output <run-plan>
```

Replace angle-bracket arguments from controlled programme records. Do not write credential values into commands, manifests, logs, or notebooks.
