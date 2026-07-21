# Appendix (companion-hosted)

The lean paper (<=25pp, ACM TIST) keeps headline tables and the four figures in
the body and deep-links each piece of supporting detail to the specific location
here. This page is the index: every appendix section A.x maps to the exact
notebook, artifact, or explainer that holds it. Each notebook is Colab-ready
(`https://colab.research.google.com/github/Wildertrek/catcher-in-the-cache/blob/main/notebooks/<file>`,
live when the repo is public at submission).

> Note: TIST convention favors a thin in-paper appendix for must-verify tables;
> if the editor requires it, the starred (*) sections below are the ones to pull
> back into the manuscript. Everything else stays here.

## Reading order: Experiment -> RQ -> notebook

The paper is organized as three experiments plus two further analyses. This is the
reproduction reading order; the A.x index below is the detailed map.

| Experiment | RQs (reader-facing / pre-reg) | Notebooks |
|---|---|---|
| **Exp 1, method comparison + construct validity** | RQ1.1-1.7 (RQ1-3,6-8,11) | nb 02 (comparison + 3 bars); M6/SCPI structural-probe detail in [`scpi_structural_probe_results.md`](scpi_structural_probe_results.md); M1 floor = `method_bakeoff_v4/m1_baseline.py` |
| **Exp 2, cross-rater HEXACO panel** | RQ2.1-2.3 (RQ6.1,6.2,6.7) | nb 03 (panel reproducer) |
| **Exp 3, out-of-corpus substrate** | RQ3.1-3.2 (RQ6.9, gauge) | nb 09 (the catch) + `compute_signed_r.py`, nb 04 (synthetic design), nb 05 (cache map), nb 06 (register-matched), nb 07 (subject-mode) |
| **Further analyses** |, | nb 08 (representational probe), nb 10 (label propagation + the S1 cost-accuracy frontier; one notebook covers both) |
| **Supporting (S1-S4)** | RQ4, RQ9, RQ10, Amendment 11 | S1 cost-accuracy frontier = nb 10; S2 single-LLM probe = nb 02 §9; S3 archetype stability = nb 02 §10 + `method_bakeoff_v4/cpm_rq10_ocean_hp_permutation_null.json` (10,000 permutations, the artifact nb 02 actually loads); S4 subject-mode dissociation = [`further_analyses.md` §A.13](further_analyses.md) + `pivot6_hexaco_atlas/v8_d4b_within_model_subject.json` |

Full RQ crosswalk: [`rq_decoder.md`](../explainers/rq_decoder.md). M1 is the
training-free embedding-prototype floor, computed for completeness (Bar-1 baseline
only).

| A.x | Section | Where it lives |
|---|---|---|
| A.1 | GT provenance taxonomy (5-tier / 11-subtype) | [`numbers_decoder.md` §3](../explainers/numbers_decoder.md) + [`method_bakeoff_v4/`](../../paper_artifacts/method_bakeoff_v4/) |
| A.2 | Method specs + verbatim prompts | [`method_zoo.md`](../explainers/method_zoo.md) + [`method_bakeoff_v4/README.md`](../../paper_artifacts/method_bakeoff_v4/README.md) |
| A.3* | Three-bar MTMM machinery + monotrait floor | [`psychometrics_glossary.md`](../explainers/psychometrics_glossary.md) + [nb 02](../../notebooks/02_method_bakeoff_results.ipynb) |
| A.4 | HEXACO re-prompt protocol | [nb 03](../../notebooks/03_hexaco_atlas_reproducer.ipynb) + [`pivot6_hexaco_atlas/`](../../paper_artifacts/pivot6_hexaco_atlas/) |
| A.5* | Per-trait bar detail + leaderboard CIs | [nb 02](../../notebooks/02_method_bakeoff_results.ipynb) |
| A.6 | Panel RQ verdicts + 25-rater panel reconciliation (authoritative numbers: [`pivot6_hexaco_atlas/panel25/`](../../paper_artifacts/pivot6_hexaco_atlas/panel25/)) | [`rq_decoder.md`](../explainers/rq_decoder.md) + [`numbers_decoder.md`](../explainers/numbers_decoder.md) + [nb 03](../../notebooks/03_hexaco_atlas_reproducer.ipynb) |
| A.7* | The catch: per-rater scores + signed-r discriminator + register-match + subject-mode control | [`the_catch_explained.md`](../explainers/the_catch_explained.md) (all 25 scores + signed $r$) + [`compute_signed_r.py`](../../paper_artifacts/pivot6_hexaco_atlas/compute_signed_r.py) (`signed_r_results.json`) + [nb 09](../../notebooks/09_catcher_in_the_cache.ipynb) + [nb 06](../../notebooks/06_register_matched_synth.ipynb) + [nb 07](../../notebooks/07_ipip_human_anchor.ipynb) + [`synthetic_vs_canonical.csv`](../../paper_artifacts/pivot6_hexaco_atlas/synthetic_vs_canonical.csv). Note: the register-match control is now in the paper's in-paper Appendix G. |
| A.8 | Cache map (embedding separation) | [nb 05](../../notebooks/05_cache_map.ipynb) + [`cache_map_viz_data.json`](../../paper_artifacts/pivot6_hexaco_atlas/cache_map_viz_data.json) |
| A.9 | Activation probe: layer trajectories + pool-ablation | [`activation_probe_for_psychologists.md`](../explainers/activation_probe_for_psychologists.md) + [nb 08](../../notebooks/08_activation_probe_dissociation.ipynb) |
| A.10 | Label propagation (regressor inherits the fusion) | [nb 10](../../notebooks/10_regressor_inference.ipynb) (runs the regressor) + [nb 04](../../notebooks/04_synthetic_characters.ipynb) (builds the substrate) + [`synth_regressor_benchmark.json`](../../paper_artifacts/method_bakeoff_v4/synth_regressor_benchmark.json) |
| A.11 | Synthetic-character design | [`why_synthetic_chars.md`](../explainers/why_synthetic_chars.md) + [nb 04](../../notebooks/04_synthetic_characters.ipynb) |
| A.12 | Robustness probes A2-A5 (name-swap 0.848, generative-consistency 0.870, diachronic, de novo EFA) | [`further_analyses.md`](further_analyses.md) |
| A.13 | Subject-mode dissociation (6-model; judge 0.79 -> subject 0.41, Branch A falsified) | [`further_analyses.md`](further_analyses.md) |
| A.14 | Cross-provider triangulation (Steiger's Z) + Big Five Backstage second source | [`further_analyses.md`](further_analyses.md) |
| A.15 | Deployment guide + extended limitations | [`deployment_quickstart.md`](../explainers/deployment_quickstart.md) + [`practitioners_guide.md`](../practitioners_guide.md) |

**Reader entry points:** five-minute overview [`reading_guide.md`](../explainers/reading_guide.md);
the central figure walk-through [`the_catch_explained.md`](../explainers/the_catch_explained.md);
reproducibility [`reproducibility.md`](../reproducibility.md). The headline-number to
artifact map is the reproduction table in the [repo README](../../README.md).
