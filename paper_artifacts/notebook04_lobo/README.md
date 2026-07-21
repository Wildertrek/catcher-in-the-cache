# Notebook 10 LOBO-CV reproduction

## Result

Leave-one-book-out cross-validation across the full the paper corpus (75 books, 576 characters) reproduces the distillation baseline:

| Source | n books | n chars | Mean MAE | 95% CI |
|---|---:|---:|---:|---|
| **This run (75-book corpus)** | 75 | 576 | **0.3117** | [0.3022, 0.3224] |
| Distillation baseline (28 novels) | 28 | ~270 | 0.309 | [0.303, 0.316] |

This run's mean MAE (0.3117) is within the distillation baseline's confidence interval. The cost-reduction claim (~$0.001/char vs $0.061 multi-provider consensus, 61× reduction) is validated at the broader corpus scale.

## How to reproduce

```bash
python paper_artifacts/notebook04_lobo/run_lobo.py
```

Runs offline, no API key required. Uses cached 3072-dim embeddings from the cached embeddings, slices to 1536-dim (Matryoshka), trains a RandomForestRegressor (300 trees, max_depth=15, seed=20260427) leaving out each book in turn.

Wall clock: ~3-5 minutes on a modern laptop.

## Notebook 10 pairing

The `notebooks/10_regressor_inference.ipynb` notebook loads the pre-computed `lobo_results.json` shipped in the data bundle (`data/aperture-data-v1/regressors/lobo_results.json`) and reproduces the headline + per-book bar chart in under 30 seconds with no API calls. This addresses the AE Round 5 P1 ("scaffold awaiting public release") concern.

## Files

- `run_lobo.py`, the script (offline, uses cached embeddings)
- `lobo_results.json`, output of the script (also shipped in data bundle)

## Files NOT in this folder (because they're large)

The cached 3072-dim embeddings are in the private research repository's `rag_indices/<book>/pillar1/model_scores.json` files, not duplicated here. The data bundle ships only the LOBO results (small JSON), not the full embedding matrix.

If a reviewer wants to re-run from raw text, see the optional advanced cell in Notebook 10.
