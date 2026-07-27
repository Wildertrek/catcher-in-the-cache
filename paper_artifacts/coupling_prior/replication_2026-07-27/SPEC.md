# Coupling prior at panel scale: spec

## Why

Paper 2's identification argument now rests on a within-synthetic contrast: the *same* 20
synthetic characters fuse Honesty-Humility with Agreeableness at **+0.83** when rated from a
name alone, and collapse to **+0.23** when rated from their text. Because the characters are
identical across those two cells, stimulus vividness and prose quality are held constant, and
the evaluative-halo alternative cannot explain the swing.

That argument is load-bearing and its name-only cell currently rests on **3 providers**
(Claude Haiku 4.5, GPT-4o-mini, Gemini 2.5 Flash), while every other headline in the paper uses
the 25-rater panel. The companion already flags this: *"A frontier-rater replication is the
planned camera-ready step."*

## Design

| | canonical (20) | synthetic (20) |
|---|---|---|
| name + title only, no text | replicate | **the cell that matters** |
| text, name redacted | replicate | replicate |
| text + name | already have (25-rater) | already have (25-rater) |

Run the **name-only** condition across the full 25-rater panel (the panel25 roster, `xai_2`
excluded as a duplicate seed). Same probe, same scale, same holistic H/A elicitation as the
3-provider run, so the new numbers are directly comparable to the existing +0.83.

## Pre-registered predictions

- **P1.** Synthetic name-only fusion stays high on the 25-rater panel, r(H,A) >= +0.5.
- **P2.** It exceeds the synthetic *text* fusion on the same panel (+0.23) by >= 0.3.
- **FALSIFIER.** If synthetic name-only fusion on the frontier panel is < +0.3, or does not
  exceed the text cell, the halo alternative is NOT excluded and the identification argument
  in Experiment 3 must be withdrawn and the limitation restored.

Report family-clustered (9 provider families), consistent with the paper's headline statistic.

## Cost

20 characters x 25 raters x 1 call = **500 calls**, ~1.3k input / ~200 output tokens each.
Rough order: **$10-25** depending on roster mix. Smoke test first (2 raters x 3 characters).

## Open items before the full run

1. **Prompt parity.** Must reuse the exact name-only prompt from the 3-provider run, or the
   comparison to +0.83 is not clean. Source: `paper_artifacts/coupling_prior/`.
2. **Titles.** The synthetic records carry `op_name` (e.g. "Dorrit Kessane") with
   `book = SYNTHETIC`. The original name-only condition used "name and title"; confirm what
   title string was shown, and reuse it verbatim.
3. **Batch.** Use the released frozen set of 20, not the initial 22.
