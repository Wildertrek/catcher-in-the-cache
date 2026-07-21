# Reproducibility

## Environment

- **Python:** 3.12 (3.13+ lacks SciPy wheels at time of writing)
- **OS:** macOS (Apple Silicon and Intel) and Linux are both supported; Colab (Ubuntu) is the primary target
- **Dependencies:** pinned in `requirements.txt`

## Determinism

LLM calls are non-deterministic by default. Each notebook sets `temperature=0` where supported and seeds numpy / Python RNGs. Small numerical drift is expected between runs; the notebooks report tolerances on each reported figure.

## Costs (for full re-run)

Approximate per-notebook costs against current provider prices (as of early 2026):

| Notebook | Estimated cost |
|----------|----------------|
| `01_quick_start.ipynb` | $0 with the open-weight fallback; < $0.10 with live multi-provider keys |
| `02_method_bakeoff_results.ipynb` | $0 (cached artifacts) |
| `03_hexaco_atlas_reproducer.ipynb` | $0 (cached artifacts) |
| `04_synthetic_characters.ipynb` | $0 (data card over cached artifacts) |
| `05_cache_map.ipynb` | $0 (cached embeddings) |
| `06_register_matched_synth.ipynb` | $0 (cached artifacts) |
| `07_ipip_human_anchor.ipynb` | $0 (public IPIP download, no keys) |
| `08_activation_probe_dissociation.ipynb` | $0 (cached probe summaries) |
| `09_catcher_in_the_cache.ipynb` | $0 (cached artifacts; the headline reproducer) |
| `10_regressor_inference.ipynb` | $0 (local inference only) |

API keys are loaded from `.env`; see `.env.example` for the expected variables.

## Key results and figures

Each headline result reproduces from the artifacts in
[`paper_artifacts/pivot6_hexaco_atlas/`](../paper_artifacts/pivot6_hexaco_atlas/)
and the Colab-ready notebooks:

| Result | Reproduce from |
|---|---|
| Per-rater collapse (the catch); $|r|$ 0.752→0.304, Δ=−0.447 | [`synthetic_vs_canonical.csv`](../paper_artifacts/pivot6_hexaco_atlas/synthetic_vs_canonical.csv) + [nb 09](../notebooks/09_catcher_in_the_cache.ipynb) |
| Signed-r discriminator (canonical +0.75, synthetic +0.23, designed −0.74) | [`panel25/panel25_results.json`](../paper_artifacts/pivot6_hexaco_atlas/panel25/panel25_results.json) (regenerate with `panel25/compute_panel25.py`). The parent `compute_signed_r.py` → `signed_r_results.json` is the superseded 26-rater run. |
| Family forest; panel mean 0.75 | [`panel25/panel25_canonical_r.csv`](../paper_artifacts/pivot6_hexaco_atlas/panel25/panel25_canonical_r.csv) (25 raters) + [nb 03](../notebooks/03_hexaco_atlas_reproducer.ipynb). The parent `bipolarity_atlas_v2.csv` has 28 rows (the 25 raters, the duplicate `x-ai/grok-4.3`, and the dropped Amendment-9 additions Hermes-3 and Jamba-Large-1.7) and is superseded. |
| Cache map (medians 0.87/0.41, AUC 0.99) | [`cache_map_viz_data.json`](../paper_artifacts/pivot6_hexaco_atlas/cache_map_viz_data.json) + [nb 05](../notebooks/05_cache_map.ipynb) |
| Activation-probe depth dissociation | [nb 08](../notebooks/08_activation_probe_dissociation.ipynb) |
| Register-matched control (canonical 0.65 → register 0.31 → synth 0.39) | [`register_matched/rating_results.json`](../paper_artifacts/pivot6_hexaco_atlas/register_matched/rating_results.json) + [nb 06](../notebooks/06_register_matched_synth.ipynb) |

The manuscript's figure generators (`generate_catcher_hero.py`,
`generate_cache_map.py`, `generate_three_bar_dashboard.py`) live in the paper
repository's `figures/` directory and read these artifacts.

## Random seeds

- Numpy: 42
- Python `random`: 42
- Torch (where used): 42

## Known tolerances

- LLM-rater |r| fusion: ±0.02 across runs (temperature=0, but provider-side non-determinism persists)
- Substrate collapse Δ: ±0.03
- Regressor MAE: exact (local inference, deterministic)

## Reporting issues

Open an issue on the GitHub repository with notebook name, cell number, the error message, and your Python / package versions (`pip freeze`).
