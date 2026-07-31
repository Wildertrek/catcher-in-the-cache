# The Catcher in the Cache: Retrieval, Not Measurement, in LLM Personality Inference

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/) [![License: MIT (code)](https://img.shields.io/badge/code-MIT-green.svg)](LICENSE) [![License: CC BY 4.0 (data)](https://img.shields.io/badge/data-CC--BY--4.0-lightgrey.svg)](LICENSE-DATA) [![Literary allusion](https://img.shields.io/badge/allusion-CATCHER.md-purple.svg)](CATCHER.md)

This is the companion repository for *The Catcher in the Cache* (ACM TIST). It contains the notebooks, data artifacts, and explainers needed to reproduce the paper's claims, in Experiment order.

**New here?** The paper in five minutes: [`docs/explainers/reading_guide.md`](docs/explainers/reading_guide.md). Want to score your own characters: [`docs/practitioners_guide.md`](docs/practitioners_guide.md).

**All ten notebooks were executed end-to-end with no API keys set on 2026-07-30; nine complete from cached artifacts alone.** Notebook 01 additionally offers an open-weight fallback, which needs `transformers`, `torch` and `accelerate` from `requirements.txt` rather than an API key.

**Run any notebook in Colab, no install required:**

[![Quick Start](https://img.shields.io/badge/Colab-Quick_Start-4285F4?logo=googlecolab)](https://colab.research.google.com/github/Wildertrek/catcher-in-the-cache/blob/main/notebooks/01_quick_start.ipynb) [![Experiment 1](https://img.shields.io/badge/Colab-Experiment_1-2ecc71?logo=googlecolab)](https://colab.research.google.com/github/Wildertrek/catcher-in-the-cache/blob/main/notebooks/02_method_bakeoff_results.ipynb) [![HEXACO Panel](https://img.shields.io/badge/Colab-HEXACO_Panel-F9AB00?logo=googlecolab)](https://colab.research.google.com/github/Wildertrek/catcher-in-the-cache/blob/main/notebooks/03_hexaco_atlas_reproducer.ipynb) [![The Catch](https://img.shields.io/badge/Colab-The_Catch-8A2BE2?logo=googlecolab)](https://colab.research.google.com/github/Wildertrek/catcher-in-the-cache/blob/main/notebooks/09_catcher_in_the_cache.ipynb) [![Cache Gauge](https://img.shields.io/badge/Colab-Cache_Gauge-FF6F00?logo=googlecolab)](https://colab.research.google.com/github/Wildertrek/catcher-in-the-cache/blob/main/notebooks/05_cache_map.ipynb)

These five are the guided entry points; the reproduction map below carries a Colab badge for every one of the ten notebooks.

## Thesis

![The catch: all 25 raters collapse below the y = x diagonal when rating characters absent from training](docs/explainers/catcher_hero.png)

On canonical literary characters, LLM personality rating is largely **retrieval against a memorized character prior**, not **measurement from the text**. The two are indistinguishable on famous characters, where both give the same answer, but decisive for any system expected to generalize to characters a model has never seen. We establish the effect with one instrument used twice: a 25-rater panel reproduces a structure known from human psychometrics (the Honesty-Humility / Agreeableness conflation), and that same structure collapses on 20 synthetic out-of-corpus characters. A cache-membership gauge separates the two populations almost perfectly (AUC 0.99).

## Where this sits

This is the second paper in a program. The first, a survey and computational atlas of
personality trait models, is published in ACM TIST
([10.1145/3828667](https://doi.org/10.1145/3828667)) with its own companion at
[Wildertrek/survey](https://github.com/Wildertrek/survey). That atlas catalogued the trait
models, and the embedding prototype used here as method M1 comes from it.

This paper turns on that work rather than extending it. The atlas makes a trait probe easy
to build; what we show here is that on canonical characters such a probe is largely
retrieving a memorized prior rather than measuring the text. The correction applies to our
own prior apparatus first.

**Prefer video?** A seven-part series walks the argument, closing with a two-part reviewer
walkthrough of this repository: [`docs/VIDEO_SERIES.md`](docs/VIDEO_SERIES.md).

**Reviewing this?** [`docs/OBJECTIONS.md`](docs/OBJECTIONS.md) maps every objection the paper
anticipates, including the two it cannot answer, to the artifact that speaks to it.

## What this repository is, and what it is not

This is a **verification surface**, not the production pipeline. Every notebook here reads
cached artifacts and re-derives a published number in seconds. That speed is the point, it
is what lets a referee check the paper without an API key, but it can leave a misleading
impression: that the work *is* ten notebooks.

It is not. The cached artifacts are the output of the work, not a shortcut around it.
Producing them took a narrative-ingestion and character-grounding stack that is not in this
repository: BookNLP parsing and coreference resolution, a character registry and
per-character evidence packs, a weighted multi-source ground-truth lattice, multi-provider
consensus runs, a human-validation feedback loop, and the pivots that did not survive. The
paper's evaluation set (75 works, 562 characters) is a curated subset of a larger indexed
corpus. Notebook 03 rebuilds the 25-rater headline in about a second; assembling the panel it
reads took months, and the wider program's provider spend runs to several hundred dollars.

So, concretely:

| | |
|---|---|
| **This repository reproduces** | every headline number in the paper, from committed artifacts, at \$0 |
| **This repository does not reproduce** | the ingestion, grounding, and experiment pipeline that produced those artifacts |
| **Where that lives** | the upstream research monorepo, which is not public; the released substrate, ground truth, and per-rater data are mirrored here in full |

We state this for scope, not for credit. A reader who assumes the notebooks are the method
would draw the wrong conclusion about what was validated and what was merely re-read. What
the notebooks establish is that the published numbers follow from the released data. Whether
that data was produced well is a separate question, and the paper's Limitations section and
[`docs/OBJECTIONS.md`](docs/OBJECTIONS.md) are where we take it up.

## Verify the central claim in two minutes

No install, no notebook, no API key. The paper's headline is that HEXACO
Honesty-Humility and Agreeableness fuse on canonical characters and come apart on
out-of-corpus ones. Two files carry it.

**1. Read the computed result.**
[`paper_artifacts/pivot6_hexaco_atlas/panel25/panel25_results.json`](paper_artifacts/pivot6_hexaco_atlas/panel25/panel25_results.json)

| field | expected | what it means |
|---|---|---|
| `canonical_mean_abs_r` | `0.7515` | fusion on characters the models have read |
| `synthetic_mean_abs_r` | `0.3043` | the same raters on characters that do not exist |
| `mean_delta` | `-0.4473` | the collapse |
| `n_decreased` | `25` | out of 25 raters. Not a subgroup effect |

**2. Recompute it from the raw per-rater data.**

```bash
python paper_artifacts/pivot6_hexaco_atlas/panel25/compute_panel25.py   # needs numpy
```

It reads [`synthetic_vs_canonical.csv`](paper_artifacts/pivot6_hexaco_atlas/synthetic_vs_canonical.csv),
one row per rater, and prints the four numbers above.

> **Read this before computing from the CSV by hand.** The CSV has **26** rows; the
> panel is **25**. The row `xai_2` is a duplicate run of `x-ai/grok-4.3` at the same
> seed as `xai_1` and is excluded. Averaging all 26 rows gives `-0.4508`, which is the
> superseded 26-rater figure from an earlier draft, not the number the paper reports.
> `compute_panel25.py` applies the exclusion and states it in its output under
> `excluded` and `exclusion_reason`.

**Column meanings** for every artifact named above are in
[`paper_artifacts/pivot6_hexaco_atlas/SCHEMA.md`](paper_artifacts/pivot6_hexaco_atlas/SCHEMA.md),
which also points at the synthetic character prose each rater actually saw.

If those four numbers match, the paper's central empirical claim is verified. Everything
else in this repository is detail, robustness, or the argument that the collapse means
retrieval rather than measurement.

## Reproduction map: Experiment to RQ to notebook

**APERTURE** (Automated PERsonality TUning, Representation, and Evaluation) is the multi-method, multi-rater diagnostic system the paper introduces; this repository is its paper-scoped public companion. Method codes M1-M6, the three-bar validity protocol, and all other terms are decoded in [`docs/appendix/glossary.md`](docs/appendix/glossary.md).

Every notebook runs at \$0. Notebooks 02-10 run from cached artifacts with no API keys; notebook 01 (the entry demo) makes live inference calls, and with no provider keys set it falls back to an open-weight rater (Qwen2.5-1.5B-Instruct) so it stays free too; keys are optional and enable the full multi-provider consensus. Open any notebook in Colab via its badge, or run locally (see [Quickstart](#quickstart)).

| Experiment / analysis | Research questions | Notebook | Run |
|---|---|---|---|
| Entry point | live consensus-inference demo on Pride &amp; Prejudice <em>(API keys optional: with none set it falls back to an open-weight rater; $0 headline reproducers are notebooks 03 and 09)</em> | [`01_quick_start`](notebooks/01_quick_start.ipynb) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Wildertrek/catcher-in-the-cache/blob/main/notebooks/01_quick_start.ipynb) |
| **Experiment 1**: method comparison and construct validity | RQ1.1-RQ1.7 (leaderboard, MTMM convergence, external validity, per-trait verdict, construct-space head-to-head) | [`02_method_bakeoff_results`](notebooks/02_method_bakeoff_results.ipynb) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Wildertrek/catcher-in-the-cache/blob/main/notebooks/02_method_bakeoff_results.ipynb) |
| **Experiment 2**: the cross-rater HEXACO panel | RQ2.1-RQ2.3 (fusion universal across 25 raters, family clustering, alignment regime) | [`03_hexaco_atlas_reproducer`](notebooks/03_hexaco_atlas_reproducer.ipynb) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Wildertrek/catcher-in-the-cache/blob/main/notebooks/03_hexaco_atlas_reproducer.ipynb) |
| **Experiment 3**: the out-of-corpus substrate | RQ3.1 (collapse off-cache, &Delta; = -0.447; signed-r discriminator via [`compute_signed_r.py`](paper_artifacts/pivot6_hexaco_atlas/compute_signed_r.py)) | [`03_hexaco_atlas_reproducer`](notebooks/03_hexaco_atlas_reproducer.ipynb) (reproducer), [`04_synthetic_characters`](notebooks/04_synthetic_characters.ipynb) (data card) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Wildertrek/catcher-in-the-cache/blob/main/notebooks/04_synthetic_characters.ipynb) |
| **Experiment 3**: the cache-membership gauge | RQ3.2 (separates in/out of corpus, AUC 0.99) | [`05_cache_map`](notebooks/05_cache_map.ipynb) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Wildertrek/catcher-in-the-cache/blob/main/notebooks/05_cache_map.ipynb) |
| Experiment 3 robustness (appendix) | register-matched substrate control | [`06_register_matched_synth`](notebooks/06_register_matched_synth.ipynb) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Wildertrek/catcher-in-the-cache/blob/main/notebooks/06_register_matched_synth.ipynb) |
| Experiment 3 human anchor (appendix) | same-instrument IPIP-HEXACO persona self-report | [`07_ipip_human_anchor`](notebooks/07_ipip_human_anchor.ipynb) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Wildertrek/catcher-in-the-cache/blob/main/notebooks/07_ipip_human_anchor.ipynb) |
| Further analysis, mechanism | activation probe over 12 open-weight models (early-layer fusion) | [`08_activation_probe_dissociation`](notebooks/08_activation_probe_dissociation.ipynb) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Wildertrek/catcher-in-the-cache/blob/main/notebooks/08_activation_probe_dissociation.ipynb) |
| Further analysis, the hero figure | fusion survives in the cache and collapses out of it, by layer depth (rebuilds Fig. 6 from committed per-rater data) | [`09_catcher_in_the_cache`](notebooks/09_catcher_in_the_cache.ipynb) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Wildertrek/catcher-in-the-cache/blob/main/notebooks/09_catcher_in_the_cache.ipynb) |
| Supporting (S1) + label propagation | cost-accuracy frontier; regressor inherits the fusion (LOBO MAE 0.312) | [`10_regressor_inference`](notebooks/10_regressor_inference.ipynb) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Wildertrek/catcher-in-the-cache/blob/main/notebooks/10_regressor_inference.ipynb) |

The pre-registration crosswalk and the disposition of merged/retracted questions are in [`docs/explainers/rq_decoder.md`](docs/explainers/rq_decoder.md). A guided walk-through of the central result is in [`docs/explainers/the_catch_explained.md`](docs/explainers/the_catch_explained.md), and a plain-language numbers decoder is in [`docs/explainers/numbers_decoder.md`](docs/explainers/numbers_decoder.md). If you find an artifact here describing the panel as 26, 27 or 28 raters rather than 25, [`docs/explainers/panel_roster_history.md`](docs/explainers/panel_roster_history.md) reconciles every count and says who was excluded and why. Method codes (M1-M6) are decoded with worked examples in [`docs/explainers/method_zoo.md`](docs/explainers/method_zoo.md), and the paper's companion-appendix pointers (§A.1-A.15) map to [`docs/appendix/README.md`](docs/appendix/README.md).

## Repository layout

```
notebooks/            10 reproduction notebooks (Experiment order above)
paper_artifacts/
  method_bakeoff_v4/  six-method comparison: predictions, embeddings, per-character CSVs, M1 reproducer
  pivot6_hexaco_atlas/ 25-rater panel ratings, cache-map and catcher viz data,
                       synthetic + register-matched + IPIP substrates, activation-probe summaries
  hexaco6_head_to_head/ construct-space head-to-head (HEXACO / OCEAN-6 / OCEAN-HP)
  notebook04_lobo/    leave-one-book-out splits for the regressor
data/aperture-data-v1/  canonical versioned data bundle: ground_truth/ (76 books),
                      indices/ (Pride and Prejudice worked example), regressors/
                      (1536-d Ridge head + LOBO results)
data/ground_truth/    convenience mirror of data/aperture-data-v1/ground_truth/ (byte-identical)
pillar1/              ground-truth schema, consensus runner, and metrics used by the pipeline
human_panel/          human-rater panel kit: pre-registration, design, deployment guide,
                      and the Colab rating notebook
personality_models/   deployable Ridge regressor heads (OCEAN-HP cheap regressor + HEXACO heads); the M1 reproducer is method_bakeoff_v4/m1_baseline.py
docs/explainers/      plain-language companions to every result
docs/appendix/ detailed in-companion appendix tables (MTMM, per-rater, SCPI, calibration)
docs/figures/         figure-reproduction pointers
CATCHER.md            the Salinger allusion: what the title claims and does not claim
```

> **Ground-truth duplication.** `data/aperture-data-v1/` is the canonical versioned data bundle; `data/ground_truth/` is a byte-identical convenience mirror kept at the shorter path for notebooks that expect it.

> **Note on the activation-probe artifacts.** The raw per-model hidden-state dumps (~1 GB) are not redistributed here; notebooks `08` and `09` run from the cached probe summaries (`catcher_viz_data.json` and the `v6_*_results.json` files). The raw dumps are available in the umbrella repository on request.

## Quickstart

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter lab notebooks/01_quick_start.ipynb
```

Most notebooks read cached artifacts and need no API keys. The few that can re-run live calls say so in their first cell.

## Citation

```bibtex
@article{raetano2026catcher,
  title   = {The Catcher in the Cache: Retrieval, Not Measurement, in LLM Personality Inference},
  author  = {Raetano, Joseph and Gregor, Jens and Tamang, Suzanne},
  journal = {ACM Transactions on Intelligent Systems and Technology},
  note    = {Under review},
  year    = {2026}
}
```

## License

Code is MIT ([LICENSE](LICENSE)); data and derived artifacts are CC BY 4.0 ([LICENSE-DATA](LICENSE-DATA)).
