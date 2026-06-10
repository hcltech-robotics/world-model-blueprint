# Benchmarks

The benchmark suite checks whether the blueprint is operationally equipped. 

## Benchmark surfaces

| Surface | What is measured | Required evidence |
| --- | --- | --- |
| Repository package | Documentation, schemas, scripts, deploy artefacts, and validation workflow | `scripts/validate_repository.py`, `wmb validate-repo` |
| Skill depth | Skill body length, skill cards, benchmark files, references, evals, and scripts | `wmb skill-audit` |
| Manifest contracts | Required field coverage and schema consistency | `wmb validate-manifest`, `wmb new-manifest` |
| Readiness reporting | Completeness summary for programme evidence | `wmb readiness-report` |
| Execution planning | Deterministic routing across Brev, Slurm, Megatron, OSMO, Kubernetes, Ray, and FlashDreams | `wmb run-plan` |

## Running benchmarks

```bash
make benchmarks
```

The benchmark runner writes a JSON report to `artifacts/benchmark-report.json`.
