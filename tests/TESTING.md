# Testing Guide

## Smoke Test

```bash
python3 src/pneuma_phi_edge_research_v2.py --seconds 3
```

Expected result:

- multiple Edge cycles;
- JSON and CSV artifacts;
- 5/5 core stability tests;
- extended compatibility and archive tests.

## Configuration Inspection

```bash
python3 src/pneuma_phi_edge_research_v2.py --show-config
```

Change thresholds or simulated sensor ranges in the generated JSON configuration,
rerun the program, and compare CSV outputs.
