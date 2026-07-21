# Paper Artifacts

Cached intermediate results behind the paper's tables, figures, and headline
numbers. The reproduction notebooks in [`../notebooks/`](../notebooks/) load these
files directly, so every result runs at `$0` (no API calls, no cold re-run). The
paper-claim to artifact-path mapping is the reproduction table in the repo-root
[`README.md`](../README.md).

## Directory layout

```
paper_artifacts/
├── method_bakeoff_v4/     Six-method comparison (Experiment 1): per-method
│                          predictions, bootstrap MAE/r/CCC, MTMM matrices,
│                          per-character embeddings, the M1 reproducer
│                          (m1_baseline.py), and the synthetic-substrate
│                          regressor benchmark (synth_regressor_benchmark.json).
├── pivot6_hexaco_atlas/   Cross-rater HEXACO panel (Experiments 2-3; "pivot6" is the
│                          frozen internal name of this experiment round): 25-rater
│                          H/A_HEX ratings, the synthetic-vs-canonical collapse
│                          (Δ = -0.447), signed-r discriminator
│                          (compute_signed_r.py + signed_r_results.json), the
│                          cache-membership gauge data, the register-matched and
│                          IPIP controls, and the cached activation-probe
│                          summaries.
├── hexaco6_head_to_head/  Construct-space head-to-head (RQ1.7): HEXACO vs
│                          OCEAN-6 vs OCEAN-HP MTMM cell counts.
└── notebook04_lobo/       Leave-one-book-out cross-validation for the cost-accuracy
                           regressor (S1): lobo_results.json + run_lobo.py.
```

All artifacts are shipped in-repo and fully reproduce the paper. The raw
per-model activation-probe hidden-state dumps (~1 GB) are the one exception: they
are not redistributed, and the probe notebooks run from the cached summaries here.
