.PHONY: validate format-check format benchmarks skill-audit site site-serve

PYTHON ?= python3
MKDOCS ?= $(PYTHON) -m mkdocs
PYTHONPATH := src
export PYTHONPATH

validate:
	$(PYTHON) scripts/validate_repository.py
	$(PYTHON) -m world_model_blueprint.cli validate-repo --root .

format-check:
	$(PYTHON) -m world_model_blueprint.cli format --check README.md docs skills benchmarks deploy schemas configs scripts src pyproject.toml .github

format:
	$(PYTHON) -m world_model_blueprint.cli format README.md docs skills benchmarks deploy schemas configs scripts src pyproject.toml .github

benchmarks:
	$(PYTHON) benchmarks/run_benchmarks.py --output artifacts/benchmark-report.json

skill-audit:
	$(PYTHON) -m world_model_blueprint.cli skill-audit --root . --output artifacts/skill-audit.json

site:
	$(MKDOCS) build --strict

site-serve:
	$(MKDOCS) serve
