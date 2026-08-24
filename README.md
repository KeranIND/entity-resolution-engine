# Entity Resolution Engine

A deterministic, explainable entity-matching pipeline for turning noisy customer records into canonical entities.

The project models a problem I have worked on at enterprise scale: duplicate records are rarely exact duplicates. Names drift, phone numbers are formatted differently, emails contain aliases, addresses are incomplete, and naive O(n²) comparison does not scale.

## Architecture

```text
Raw records
    ↓
Normalization
    ↓
Blocking / candidate generation
    ↓
Feature-level similarity
    ↓
Weighted match score
    ↓
Decision threshold
    ↓
Union / canonical entity graph
```

The important design choice is separating **candidate generation** from **matching**. Blocking keeps the comparison set tractable; scoring then remains transparent enough to explain why two records were linked.

## Design goals

- deterministic and reproducible matching
- explainable feature-level scores
- configurable thresholds and weights
- pluggable blocking strategies
- no hidden external services
- clear separation between normalization, scoring, and clustering

## Example

```python
from entity_resolution.engine import EntityResolver

records = [
    {"id": "1", "name": "Kiran Indugula", "email": "kiran@example.com"},
    {"id": "2", "name": "K. Indugula", "email": "kiran@example.com"},
]

resolver = EntityResolver()
clusters = resolver.resolve(records)
```

## Repository structure

```text
src/entity_resolution/
  normalize.py      # canonical field transforms
  similarity.py     # explainable similarity features
  engine.py         # blocking, scoring and union-find clustering
tests/
  test_engine.py

docs/
  architecture.md
```

## Why this project

Entity resolution looks simple until scale and false positives matter. A production-quality system must balance recall, precision, latency, explainability, and operational safety. This repository focuses on those boundaries instead of hiding the problem behind a single fuzzy-match function.

## Roadmap

- benchmark synthetic datasets at 100K / 1M+ records
- add phonetic and address-aware features
- add probabilistic calibration
- add streaming/incremental resolution
- expose metrics for candidate reduction and match quality

Built as an original public reference implementation; it contains no employer or client code.