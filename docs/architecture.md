# Architecture

## Problem framing

Entity resolution is a two-stage systems problem: reduce the candidate space without losing too many true matches, then score candidate pairs with enough transparency to support operational review.

## Pipeline

```text
Input records
   ↓
Canonical normalization
   ↓
Blocking / candidate generation
   ↓
Feature extraction
   ↓
Weighted scoring
   ↓
Threshold decision
   ↓
Union-find clustering
   ↓
Canonical entity groups
```

## Complexity

Without blocking, pairwise comparison is O(n²). This reference implementation currently uses deterministic keys such as normalized email, phone, or name prefix. Production systems typically use multiple blocking passes and inverted indexes to increase recall while keeping candidate counts bounded.

## Explainability

Pair decisions are decomposed into feature-level scores rather than one opaque value. This lets operators inspect whether a match was driven by email, phone, name, or address similarity and adjust weights safely.

## Clustering

Accepted pair matches are converted into connected components with union-find. This is fast and simple, but transitive closure can amplify a single bad edge. Production systems should therefore monitor large cluster growth and may require stronger consistency checks before merging high-risk records.

## Production evolution

A production service would add:

- multi-pass blocking
- durable canonical entity IDs
- reversible merge lineage
- match-review queues
- probabilistic calibration
- metrics for precision, recall, and candidate reduction
- batch and streaming execution modes
- partition-aware processing for large datasets
