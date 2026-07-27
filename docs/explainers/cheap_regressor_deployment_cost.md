# Cheap regressor: per-character deployment cost

Moved here from the paper's appendix on 2026-07-27 to keep the manuscript within the
ACM TIST 25-page limit. The cost model itself belongs to the companion distillation
paper, which derives it; this page records the figure the discussion section cites.

## What it costs

| Method | Latency | Cost/char | Speedup | Cost cut |
|---|---|---|---|---|
| M4 Consensus (3 providers) | ~30 s/char | ~$0.061/char | 1x | 1x |
| Distilled cheap regressor | ~0.5 s/char | ~$0.001/char | ~60x | **61x** |

Cost figures are computed in companion notebook 10. Latency is an order-of-magnitude
estimate. Multipliers are relative to the M4 baseline.

## Why one table covers two models

The OCEAN cheap regressor is a Ridge regressor over mean-pooled
`text-embedding-3-large` features (canonical LOBO MAE 0.297, artifact
`synth_regressor_benchmark.json`). It is the label-free floor the paper recommends for
Openness, Conscientiousness, and Extraversion.

It is distinct from the leaderboard's M3 random-forest regressor (LOBO MAE 0.312,
notebook 10), but the two share a deployment pipeline: one embedding call plus a fitted
prediction. The embedding call dominates and the fitted step is microseconds either way,
so the cost profile above applies to both.

## What the speedup costs you

The roughly 60x speedup and 61x cost reduction are paid for in per-factor MAE relative
to the teacher signal, documented in the paper's leaderboard and label-propagation
results. The cheap path is recommended only for Openness, Conscientiousness, and
Extraversion; the factors on the fused moral axis are deferred, not cheaply measured.

Architecture, training, and pickle provenance: `cheap_head_deployment.md`.
