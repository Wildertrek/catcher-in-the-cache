# Artifact schema

Column and field meanings for the artifacts the paper and the README verification
checklist point at. Written because these tables were shipped without a data
dictionary: a reader could open them, but not know what a column meant without
reverse-engineering it from the code.

Every artifact here is a cached output. Nothing needs an API key to read.

---

## `synthetic_vs_canonical.csv`

One row per LLM rater. This is the table behind the paper's central claim, and the one
`panel25/compute_panel25.py` consumes.

| column | type | meaning |
|---|---|---|
| `slot` | string | rater identifier, `<provider>_<n>`. The provider prefix is what groups raters into the 9 families used for the family-clustered test |
| `model` | string | the exact model version rated with, as the provider named it |
| `n_canon` | int | number of canonical characters this rater scored |
| `abs_r_canon` | float | absolute within-rater correlation between Honesty-Humility and HEXACO Agreeableness, on canonical characters. High means the two factors are fused |
| `n_synth` | int | number of synthetic, out-of-corpus characters this rater scored |
| `abs_r_synth` | float | the same correlation on synthetic characters |
| `delta_synth_minus_canon` | float | `abs_r_synth − abs_r_canon`. Negative means the fusion weakened off-cache, which is the paper's result |

**The row count is 26; the panel is 25.** `xai_2` is a duplicate run of `x-ai/grok-4.3`
at the same seed as `xai_1` and is excluded. Averaging all 26 rows yields `-0.4508`, the
superseded figure from an earlier draft, not the `-0.4473` the paper reports.
`compute_panel25.py` applies the exclusion and records it under `excluded` and
`exclusion_reason` in its output.

## `panel25/panel25_results.json`

Output of `compute_panel25.py`. The values the paper reports.

| field | meaning |
|---|---|
| `panel`, `n_raters`, `n_families` | panel composition after exclusion |
| `excluded`, `exclusion_reason` | which rater was dropped and why |
| `canonical_mean_abs_r` | mean fusion on canonical characters (`0.7515`) |
| `synthetic_mean_abs_r` | mean fusion on synthetic characters (`0.3043`) |
| `mean_delta` | mean collapse (`-0.4473`) |
| `n_decreased` | raters whose fusion decreased off-cache (`25` of 25) |
| `raters_above_030_canonical` | raters clearing the pre-registered floor on canonical characters |
| `raters_below_030_synthetic` | raters falling below it on synthetic characters |
| `signed_r` | the signed rather than absolute correlation, used for the subject-mode check |

## `panel25/panel25_canonical_r.csv`

Per-rater detail behind `canonical_mean_abs_r`.

| column | meaning |
|---|---|
| `model` | model version |
| `family` | provider family, the unit of the family-clustered significance test |
| `abs_r_H_A_HEX` | absolute within-rater r between Honesty-Humility and HEXACO Agreeableness |
| `ci_low`, `ci_high` | bootstrap 95% confidence interval on that correlation |

## `character_manifest_synthetic.csv`

The 20 synthetic characters used as the falsifier, and their canonical counterparts.

| column | meaning |
|---|---|
| `manifest_index` | position in the manifest |
| `op_id`, `op_name` | identifier and name of the canonical character the synthetic one was matched to |
| `book` | source work of the canonical counterpart |
| `coref_id` | BookNLP coreference id of the canonical character, the key used throughout the pipeline |
| `held_out_subset` | whether the row belongs to the held-out evaluation subset |
| `utterances` | number of utterances in the character's evidence pack |
| `flagged_by_neg_control` | flagged by the negative-control novelty check, meaning the synthetic character may not be fully out-of-corpus |

## The synthetic character text itself

The prose each rater actually saw is published, not just the derived correlations:

- `synthetic_characters_substrate.json` and `synthetic_characters_substrate_batchA_22.json`
  — the generated characters under a `characters` key
- `synthetic_characters_curation.md` — how they were written and selected
- `synthetic_characters_verification.json` — the novelty check, including which characters
  were flagged

The two substrate files are two generation batches, not duplicates of one another; see
`docs/explainers/synthetic_substrate_batches.md`.
