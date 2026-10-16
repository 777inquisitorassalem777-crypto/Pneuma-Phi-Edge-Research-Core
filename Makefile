.PHONY: test run-sci run-arch clean

test:
	PYTHONPATH=. pytest -q

run-sci:
	PYTHONPATH=. python -m pneuma_edge.cli run --mode scientific --steps 80 --scenario stress --export out_sci.json

run-arch:
	PYTHONPATH=. python -m pneuma_edge.cli run --mode archetypal --steps 60 --scenario stress --export out_arch.json

clean:
	rm -f *.json *.md audit.jsonl
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
