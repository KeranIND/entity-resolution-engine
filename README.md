# Enterprise CRM Entity Resolution Engine

A public reference implementation of the **same problem class I worked on in enterprise CRM systems**: resolving duplicate Leads, Contacts, Accounts, and customer identities across millions of records without relying on exact matching.

In my Walmart Business work, data quality and deduplication operated at multi-million-record scale, including work across approximately **600K Leads and 2.4M Contacts**. This repository is a clean-room implementation built from first principles to demonstrate the architecture, trade-offs, and safety controls behind that kind of system. It contains **no employer code, schemas, credentials, or proprietary business logic**.

## Problem

Enterprise CRM data rarely arrives cleanly:

```text
Lead A
  Alex Morgan
  alex.morgan@example.com
  +1 (555) 010-1234

Contact B
  A. Morgan
  ALEX.MORGAN@example.com
  5550101234
```

A useful system has to answer two different questions:

1. Which records are plausible candidates for comparison?
2. Given a candidate pair, is the evidence strong enough to link or merge them safely?

## Architecture

```text
CRM ingestion
  Leads / Contacts / Accounts
            ↓
Canonical normalization
            ↓
Multi-pass candidate generation
            ↓
Feature-level similarity
            ↓
Weighted evidence model
            ↓
Decision policy
   ├── auto-link
   ├── review
   └── reject
            ↓
Canonical customer graph
            ↓
Merge lineage + provenance
```

The design deliberately separates **candidate generation** from **match scoring**. That keeps comparison cost bounded while letting precision/recall be tuned independently.

## Enterprise-specific concerns modeled here

- Lead ↔ Contact identity resolution
- exact and fuzzy email matching
- phone normalization
- name normalization and similarity
- source-system provenance
- merge survivorship policy
- reversible merge lineage
- false-positive protection
- canonical customer IDs
- explicit auto-match vs review thresholds

## Repository structure

```text
src/entity_resolution/
  normalize.py
  similarity.py
  engine.py
  crm.py              # Lead/Contact/Account adapters
  provenance.py       # source + merge lineage
  merge_policy.py     # field survivorship rules

tests/
  test_engine.py
  test_crm_resolution.py

docs/
  architecture.md
  enterprise-crm-case-study.md
```

## Why this is directly related to my work

I have designed and built Salesforce/data-quality automation around onboarding, account/contact ingestion, ownership routing, opportunity workflows, integrations, and duplicate-record handling in large enterprise environments. This project isolates the identity-resolution part of that work into a public system that can be reviewed without exposing any client implementation.

The code is not a retrospective copy of a production system. It is a new implementation of a problem I have actually solved, using synthetic examples and public-safe abstractions.

## Engineering goals

- deterministic and reproducible decisions
- explainable feature-level evidence
- bounded candidate generation rather than O(n²) matching
- safe merge semantics
- measurable precision/recall trade-offs
- explicit provenance and auditability
- architecture suitable for batch or streaming evolution

## Next engineering steps

- multi-pass blocking indexes
- large synthetic benchmark generator
- precision/recall evaluation harness
- cluster explosion detection
- manual-review queue abstraction
- incremental matching for new CRM records
- durable canonical identity store

This repository is intentionally tied to my real enterprise architecture experience while remaining completely independent of employer source code.