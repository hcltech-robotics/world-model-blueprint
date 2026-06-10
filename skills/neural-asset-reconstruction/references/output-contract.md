# Output contract: Neural asset reconstruction

## Required sections

The skill output must contain these sections:

1. **Manifest**: path to the neural asset manifest or the expected path if it has not yet been created.
2. **Accepted evidence**: source records accepted from manifests, registries, storage handles, legal records, platform records, or review notes.
3. **Missing evidence**: records required before the route can execute, classified as blocking or non-blocking.
4. **Selected route**: reconstruction, Content Agents enrichment, CAD-to-SimReady, video augmentation, defect generation, or manual review.
5. **Upstream NVIDIA/skills and OVRTX invocation plan**: exact upstream skill names, expected inputs, service surface, and expected outputs.
6. **NIM and service surface**: whether hosted NIM, private NIM, OpenAI-compatible endpoint, Content Agents REST, NRE gRPC, CLI, container, simulator bridge, or manual review applies.
7. **Validation gates**: render quality, USD loadability, material plausibility, physics plausibility, SimReady validation, reconstruction metrics, split leakage, and human review.
8. **Handoff**: next local owner skill, artefact, manifest path, and review gate.

## Acceptance criteria

An acceptable output:

- Uses `schemas/neural-asset-manifest.schema.json` as the contract.
- Names the actual upstream route without inventing a tool or repository.
- Keeps endpoint URLs, credentials, asset paths, and customer records out of prose unless supplied as controlled handles.
- Records whether the route is NIM-backed, OpenAI-compatible, REST, gRPC, OVRTX Python or C SDK, CLI, container, scheduler-backed, or manual.
- Includes a validation path before generated or reconstructed assets are used for training, simulation, or evaluation.
- Routes data-split decisions to `world-model-data-factory` and asset conformance to `simready-content-integration`.

## Minimal artefact template

```markdown
## Manifest

- Path:
- Status:

## Accepted evidence

| Evidence | Source record | Use |
| --- | --- | --- |

## Missing evidence

| Evidence | Blocking | Needed for |
| --- | --- | --- |

## Selected route

- Route:
- Reason:
- Service surface:

## Upstream NVIDIA/skills invocation plan

| Skill | Inputs | Outputs | Review gate |
| --- | --- | --- | --- |

## Validation gates

| Gate | Owner | Evidence |
| --- | --- | --- |

## Handoff

- Next skill:
- Artefact:
- Review gate:
```
