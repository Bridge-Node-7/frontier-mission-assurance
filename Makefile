.PHONY: install test lint validate assumptions coverage impact receipt reproduce report schema boundary evaluate fingerprint scientific-discovery orbital-recovery orbital-recovery-benchmark ftqc ftqc-evaluate demo check clean

install:
	python -m pip install -e '.[dev]'

test:
	pytest

lint:
	ruff check src tests scripts

validate:
	fma validate examples/frontier_program/graph.yaml

assumptions:
	fma assumptions examples/frontier_program/graph.yaml

coverage:
	fma coverage examples/frontier_program/graph.yaml

impact:
	fma impact examples/frontier_program/graph.yaml ASSUMP-CYCLE-COMPOSITION

receipt:
	fma receipt examples/research_receipt/receipt.yaml
	fma decision examples/frontier_program/graph.yaml examples/frontier_program/decision-receipt.yaml

reproduce:
	fma reproduce examples/research_receipt/receipt.yaml

report:
	mkdir -p build
	fma report examples/frontier_program/graph.yaml --out build/assurance-report.md

schema:
	pytest -q tests/test_schemas.py

boundary:
	python scripts/public_boundary_scan.py .

evaluate:
	python scripts/evaluate_public_reference.py

fingerprint:
	python scripts/environment_fingerprint.py --out build/environment-fingerprint.json

scientific-discovery:
	python scripts/validate_scientific_discovery.py .

orbital-recovery:
	python scripts/validate_orbital_recovery_assurance.py .

orbital-recovery-benchmark:
	python scripts/run_orbital_recovery_synthetic_benchmark.py .

ftqc:
	python scripts/validate_ftqc_assurance.py .

ftqc-evaluate:
	python scripts/evaluate_ftqc_reference.py .

demo: evaluate

check: lint test validate assumptions coverage receipt reproduce report evaluate fingerprint scientific-discovery orbital-recovery orbital-recovery-benchmark ftqc ftqc-evaluate boundary

clean:
	rm -rf build dist .pytest_cache .ruff_cache .coverage *.egg-info src/*.egg-info
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
