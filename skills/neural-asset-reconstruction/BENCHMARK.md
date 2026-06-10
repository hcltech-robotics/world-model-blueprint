# Benchmark: Neural asset reconstruction

The skill is evaluated on whether it routes asset and reconstruction tasks to real upstream NVIDIA/skills capabilities, records service surfaces honestly, and protects rights, provenance, and validation gates before downstream use.

## Eval cases

1. **NuRec route from multi-sensor evidence**: given calibrated camera, LiDAR, telemetry, and rights records, the skill should choose `physical-ai-neural-reconstruction`, route through `nurec-index`, `ncore`, and `nre`, and require reconstruction metrics and simulator review.
2. **Content Agents enrichment**: given an existing USD with missing material and physics evidence, the skill should choose Content Agents material, physics, and validation capabilities, preferring REST service mode when a service-like lane is required.
3. **CAD-to-SimReady handoff**: given source CAD and a SimReady objective, the skill should route to `omniverse-cad-to-simready`, define Content Agents enrichment only when needed, and hand off to `simready-content-integration`.
4. **Asset Harvester route**: given captured logs and an object reuse objective, the skill should route to NuRec `asset-harvester` and require provenance, review, and validation before dataset or SimReady use.
5. **Rights ambiguity stop**: when permitted use is unknown, the skill should refuse generation or reconstruction, record missing rights evidence, and route to governance.
6. **Synthetic leakage control**: when generated variants may contaminate evaluation, the skill should route split policy to `world-model-data-factory` and require holdout protection.
7. **OVRTX headless rendering**: when the task asks for previews, videos, simulation frames, or sensor outputs, the skill should route to the correct OVRTX setup, renderer, USD loading, render settings, stepping, status, warmup, output reading, and sensor skills.

## Pass criteria

- The answer names real upstream skills and capabilities.
- The answer never invents repositories, endpoints, asset IDs, customer data, approvals, or benchmark values.
- The answer distinguishes NIM-backed, REST, gRPC, CLI, container, and manual-review execution surfaces.
- The answer distinguishes OVRTX Python or C SDK rendering from NIM-backed services.
- The answer records rights and derivative-use gates before reconstruction or generation.
- The answer defines validation evidence before SimReady, dataset, evaluation, or deployment handoff.
- The answer names the next local blueprint skill and expected artefact.
