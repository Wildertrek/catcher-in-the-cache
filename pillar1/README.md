# Consensus (multi-provider trait inference)

Trait inference from LLM consensus compared against curated ground truth.

## Metrics

| Metric | Meaning |
|--------|---------|
| **PA** (Profile Accuracy) | Agreement between inferred traits and ground-truth reference |
| **TD** (Trait Distinctiveness) | Separation between character trait vectors vs random baselines |
| **RCS** (Repeat Consistency Score) | Stability of trait outputs across repeated probes |
| **CMC** (Cross-Model Consistency) | Similarity across providers and repeated runs |

## Files

- `consensus_runner.py`, invokes multiple providers, aggregates per-character outputs
- `metrics.py`, PA, TD, RCS, CMC computations

Scripts consume `data/ground_truth/*.json` and a FAISS index from `data/indices/`.

## Quick example

See [`../notebooks/01_quick_start.ipynb`](../notebooks/01_quick_start.ipynb) for an end-to-end run on Pride & Prejudice.

## Ground-truth schema

See [`ground_truth_schema.md`](ground_truth_schema.md) for the v3 AGT / SGT / PGT / MGT / CGT taxonomy.
