# Why the panel is 25 raters (and where 28, 27 and 26 came from)

Working notes and earlier artifacts in this repository refer to the HEXACO rater
panel as 28, 27, 26 and 25 raters. All four numbers are correct. They count two
different things, and this file records which is which so no reader has to guess.

**The paper reports a single panel: 25 distinct LLM raters across nine provider
families.** Everything below explains what the other counts were.

## The four numbers

Two independent choices produce four counts:

- **slots vs models**: Grok 4.3 was run twice, in slots `xai_1` and `xai_2`.
  Counting slots gives one more than counting distinct models.
- **with or without the two late additions**: Hermes-3 and Jamba-Large-1.7 were
  added late for one specific analysis (below) and are not part of the panel.

| count | counts | includes Grok twice | includes the two additions | artifact |
|---|---|---|---|---|
| 28 | slots | yes | yes | `bipolarity_atlas_v2.csv` (28 rows) |
| 27 | distinct models | no | yes | `bipolarity_atlas_v2.csv` (27 unique models) |
| 26 | slots | yes | no | `bipolarity_atlas.csv`, `synthetic_vs_canonical.csv` |
| **25** | **distinct models** | **no** | **no** | **`panel25/panel25_canonical_r.csv`** ← the paper |

28 → 27 and 26 → 25 are the same subtraction (the duplicate Grok run).
28 → 26 and 27 → 25 are the other one (the two additions).

## Who is not in the 25, and why

### Hermes-3 70B and Jamba-Large-1.7

These two were recruited under **Amendment 9**, registered *before* the calls
were made, for one purpose: to break a confound in the pre-registered
**alignment-regime contrast**. `alignment_regime_classification_v2.csv` states
the rationale verbatim:

- `nousresearch/hermes-3-llama-3.1-70b`, "2nd provider for DPO-primary regime"
- `ai21/jamba-large-1.7`, "2nd provider for CAI regime"

The problem being attacked was that each provider family committed to a single
alignment regime, so regime and family were collinear and regime could not be
tested as an independent predictor. Adding a second provider to the two
thinnest regime cells was the designed remedy, and it worked as intended:
`v8_c1_strategy_2_lrt.json` records the resulting coverage as CAI 2,
DPO-primary 2, RLHF-pure 2, RLHF-Hybrid 6.

**The contrast still failed, structurally rather than empirically.** With the
expanded roster the likelihood-ratio test remained rank-deficient (the artifact
records `"regime collinear with family (rank-deficient)"`), and the secondary
ANOVA was non-significant (F = 1.49, p = 0.245). Regime is not separable from
family in any between-family design; establishing it would require a
within-family regime contrast. The contrast was therefore retracted, and the
two models had served their only purpose.

They were **canonical-only by design**, not by oversight. The analysis they were
recruited for reads canonical fusion alone, so they were never given synthetic
or OCEAN ratings. That is also why they cannot appear in the substrate
falsifier, which requires the same rater to score both populations.

Their canonical ratings are committed here and are not hidden:

| model | canonical \|r(H, A)\| | n | synthetic | file |
|---|---|---|---|---|
| Hermes-3 70B | 0.9156 | 60 | none | `pivot6_hexaco_atlas/hexaco_ratings_hermes_1.json` |
| Jamba-Large-1.7 | 0.8342 | 60 | none | `pivot6_hexaco_atlas/hexaco_ratings_ai21_1.json` |

Both sit far above the pre-registered 0.30 floor, and would rank 4th and 6th of
26 on canonical fusion. Including them would raise the reported panel mean from
0.7515 to 0.7607. **The exclusion is conservative**: it works against the
paper's claim, not for it.

The retracted analysis they were recruited for is shipped here in full:
`v8_c1_strategy_2_lrt.json` (Amendment 9, expanded roster) alongside
`v8_c1_regime_restricted_lrt.json`, `v8_c1_strategy_15_lrt.json` and
`v8_b4_base_arch_lrt.json` (the earlier attempts on the unexpanded roster).

### The duplicate Grok run (`xai_2`)

`xai_2` is a second run of `x-ai/grok-4.3`, the same model already present as
`xai_1`. It is excluded so that each distinct model contributes exactly one
rater, which matters because the panel is already family-clustered (a disclosed
limitation). Its data is committed and behaves like the rest of the panel:
canonical \|r\| = 0.6269 (n = 49), synthetic \|r\| = 0.108 (n = 22),
Δ = −0.519, a *steeper* off-cache collapse than the panel mean of −0.447.

### Models classified but never rated

`alignment_regime_classification_v2.csv` classifies 29 models, four of which
appear in no rating artifact: `x-ai/grok-3`, `x-ai/grok-4-07-09`,
`gemini-2.0-flash`, `meta-llama/llama-3.1-405b-instruct`. The two Grok entries
are the snapshots deprecated by xAI mid-project, which is why Grok 4.3 was
substituted under Amendment 1. These models were candidates on a classification
sheet; they were never part of any panel.

## Why the panel was not enlarged after the fact

Adding the two canonical-only models to the panel would create a 27-rater
Experiment 2 and a 25-rater Experiment 3, reintroducing exactly the shifting
denominator this file exists to explain, and it would be an inclusion decided
after their values were known to favor the reported effect. (Their original
recruitment was pre-registered under Amendment 9 and is not post-hoc; moving
them into the headline panel now would be.) Re-running them on the synthetic
population is not a clean remedy either, for reasons documented in the synthetic
substrate notes.

The panel is therefore frozen at the 25 distinct models that scored **both**
populations under the same probe, which is what makes the falsifier a
within-rater contrast.

## Authoritative source

For any panel number, `panel25/panel25_results.json` is authoritative; it is
regenerated deterministically by `panel25/compute_panel25.py` from the committed
per-rater CSV. Artifacts that predate the standardization carry a superseded
banner naming the values that changed.
