# The standardized 25-rater panel

The paper reports Experiment 2 and Experiment 3 on a single **25-rater panel**
(9 provider families). Notebooks `03_hexaco_atlas_reproducer.ipynb` and
`04_synthetic_characters.ipynb` compute this same panel: they read the files in this
directory (`panel25_results.json`, `panel25_canonical_r.csv`) or filter the duplicate
Grok 4.3 run (`xai_2`) out of the parent CSVs, so their executed outputs match the
paper (`delta = -0.447`, mean `|r| = 0.75`, ICC = 0.577, eta^2 = 0.697).

**This directory is the authoritative source for the panel; notebooks 03 and 04
reproduce it.**

The panel has also been described as 26, 27 and 28 raters at various points. Those
counts differ by whether the duplicate Grok 4.3 run is counted and whether two
canonical-only models are included; all four are reconciled, with the excluded
models' results, in [`docs/explainers/panel_roster_history.md`](../../../docs/explainers/panel_roster_history.md).

| file | what it is |
|---|---|
| `compute_panel25.py` | derives every headline from `../synthetic_vs_canonical.csv`; deterministic (seed 42) |
| `panel25_results.json` | its output, regenerate with `python compute_panel25.py` |
| `panel25_canonical_r.csv` | per-family canonical means + bootstrap CIs behind Fig. 5 |

## What the panel is

25 distinct LLM raters = every row of `../synthetic_vs_canonical.csv` except `xai_2`,
a duplicate run of `x-ai/grok-4.3` at the same seed as `xai_1`. The Amendment-9
additions (Hermes-3, Jamba-Large-1.7) were never re-run on the synthetic substrate
and are absent from that file already. 25 is the pre-registration lock count.

## Reproduced numbers

| quantity | value | paper |
|---|---|---|
| canonical mean \|r(H,A)\| | 0.7515 | 0.75 |
| synthetic mean \|r(H,A)\| | 0.3043 | 0.30 |
| mean delta | **-0.4473** | **-0.447** |
| raters that decreased | 25 / 25 | all 25 |
| canonical raters above the 0.30 floor | 25 / 25 | 25/25 |
| synthetic raters below the 0.30 floor | 14 / 25 | 14 of 25 (Fig. 6 caption) |
| family clustering ICC(1) | 0.5774 | 0.577 |
| family clustering eta^2 | 0.6973 | 0.697 |
| permutation p, unadjusted | 0.0032 | see below |
| signed synthetic r (mean) | +0.2315 | +0.23 |
| signed synthetic 95% CI | [0.123, 0.338] | [0.12, 0.34] |
| raters with positive signed r | 20 / 25 | 20 of 25 |
| sign test p | 0.0041 | 0.004 |

## BH-adjusted family-clustering p

`compute_panel25.py` emits both the unadjusted permutation `p_raw` and the
BH-adjusted value, over the pre-registered five-test family recorded in
`bh_fdr_pivot6_results.json` (RQ6.9_PRIOR_DRIVEN, H2_family_clustering,
H4_open_vs_closed, H3_capability_correlation, H5_head_to_head_proxy).

Sorted ascending, family clustering (H2) sits at **rank 2 of 5**, so
`p_BH = p_raw x 5/2`. With 200,000 permutations this script gets
`p_raw = 0.0032149839`, giving `p_BH = 0.008037`. The paper reports **0.008**,
which is this value.

For RQ6.9, the script's BH-adjusted p is `1.49e-07` (one-sided `p_raw = 2.98e-08`
times 5/1). Where the paper quotes `6.0e-8` for RQ6.9 that is the two-sided
*unadjusted* Wilcoxon p (`5.96e-08`), not a BH-adjusted value.

Both values are far below 0.05 and no conclusion turns on the adjustment.
Earlier drafts of this file quoted `p_BH = 0.006` at rank 3 of 5; that was a
reconstruction against the superseded panel and is wrong on both the rank and
the value. `panel25_results.json` is authoritative.
