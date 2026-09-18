.PHONY: install test lint validate assumptions coverage impact receipt reproduce report schema boundary evaluate fingerprint profile-manifests external-adoption scientific-discovery orbital-recovery orbital-recovery-benchmark ftqc ftqc-evaluate ftqc-case ftqc-compare demo check clean

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

profile-manifests:
	python scripts/validate_profile_manifests.py .

external-adoption:
	fma validate examples/external_research_adoption/graph.yaml
	fma decision examples/external_research_adoption/graph.yaml examples/external_research_adoption/decision-receipt.yaml

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

ftqc-case:
	mkdir -p build
	python scripts/validate_ftqc_case.py profiles/ftqc-assurance/examples/synthetic-neutral-atom/baseline --report build/ftqc-case-decision-basis.md

ftqc-compare:
	mkdir -p build
	python scripts/compare_ftqc_cases.py profiles/ftqc-assurance/examples/synthetic-neutral-atom/baseline profiles/ftqc-assurance/examples/synthetic-neutral-atom/changed-assumption-case --report build/ftqc-change-impact.md

demo: evaluate

check: lint test validate assumptions coverage receipt reproduce report evaluate fingerprint profile-manifests external-adoption scientific-discovery orbital-recovery orbital-recovery-benchmark ftqc ftqc-evaluate ftqc-case ftqc-compare boundary

clean:
	rm -rf build dist .pytest_cache .ruff_cache .coverage *.egg-info src/*.egg-info
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
