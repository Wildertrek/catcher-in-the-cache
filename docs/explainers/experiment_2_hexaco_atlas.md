# Experiment 2: The HEXACO Panel, do the raters reproduce a *known* human structure?

A plain-language explainer. No statistics background needed. This is the second of the paper's three
experiments; read `experiment_1_three_bars.md` first if you haven't.

## Why this experiment exists (the one-sentence version)
Experiment 1 proved the measuring tools *work*. Experiment 2 asks a sharper question: **when the raters
measure, do they reproduce a personality structure that psychologists already know is real?** If they
do, the instrument isn't just internally consistent, it's calibrated to something true about human
personality. That's what earns the right to use it, in Experiment 3, to catch the raters retrieving
instead of measuring.

## What the panel is
We take **25 LLM raters** from **9 provider ecosystems** (Anthropic, OpenAI, Google, Meta, Qwen,
Mistral, and more), give each the same **HEXACO** personality questionnaire, and have them rate the same
**60 famous literary characters**. HEXACO is the six-factor model (Honesty-Humility, Emotionality,
eXtraversion, Agreeableness, Conscientiousness, Openness), the one that adds a dedicated
**Honesty-Humility** factor the OCEAN lacks.

## The finding: the raters fuse two factors that are supposed to be separate
Across all 25 raters, **Honesty-Humility and HEXACO Agreeableness are fused at a within-rater correlation
of |r| = 0.75**, every single rater above the pre-registered floor, and stable across repeated runs
(seed-to-seed wobble of only 0.062).

Here's why that's the *right* thing to find, not a bug:

- Decades ago, psychologists showed that **OCEAN Agreeableness quietly mixes two different things** , 
  warmth *and* honesty. HEXACO was built to split them apart into separate A and H factors.
- The classic literary villain is the giveaway: **polite and charming, but morally corrupt.** A OCEAN
  rater calls him "agreeable" and never sees the moral axis. HEXACO is supposed to separate the two.
- Our raters **don't** keep them separate, they fuse H back into A, reproducing the *exact* old OCEAN
  impurity that HEXACO was designed to remove.

So the raters recover a **documented, real** feature of personality structure. That's what certifies the
instrument: it behaves like a known-good measuring device, reproducing a structure psychologists already
mapped.

## Amplified, not invented
Is the fusion just made up? No, there's a **real but modest** overlap between these two traits in actual
humans: **r = 0.45** in a sample of 22,299 people who took the questionnaire, and **0.20–0.30** in the
broader norming literature. The raters take that genuine overlap and **inflate it** to 0.75. They amplify
a real signal; they don't conjure one from nothing. (This matters for Experiment 3: an *amplified real
thing* is exactly what should collapse when there's nothing to amplify.)

## The raters cluster by family
The fusion isn't random across models, it **clusters by provider family** (a statistical test confirms
it: ICC permutation p = 0.008, corrected for multiple comparisons). Models from the same maker fuse to
similar degrees. Family means run from about **0.59** (Google, the least fused) to **0.92** (Meta, the
most). This says the effect is a property of *how models are built and trained*, not a per-model fluke.

## The panel count
The panel is **25 distinct LLMs across 9 provider families**: the pre-registration-lock set. (Grok 4.3
was run once; the two late Amendment-9 additions, Hermes-3 and Jamba, were never re-run on the synthetic
substrate and were dropped.) The same 25 raters carry both the canonical panel and the Experiment 3
synthetic paired test.

## An honest retraction (good science on display)
We pre-registered a guess: maybe a model's **alignment training method** (how it was fine-tuned), not its
provider, drives the fusion. When we tested it properly, **it didn't hold**: training method turned out
to be almost perfectly tangled up with provider (each family uses basically one recipe), so the two can't
be told apart in our sample. Under the one grouping that *can* separate them, the effect vanishes
(a likelihood-ratio test returns essentially nothing: χ² = 0.081, p = 0.78). So we **retracted** the
alignment-training claim and report only what the data supports: the clustering is by provider family.

## Why Experiment 2 sets up "the catch"
Experiment 2 establishes that the fusion is **real, strong, reproducible, and family-clustered**: on
**famous** characters the models have read many times. But that's exactly the problem the whole paper is
about: a fusion this robust on *cached* characters could be genuine measurement **or** a memorized prior
the model retrieves. Experiment 2 can't tell them apart, because every character here is one the models
know.

That's the hand-off to **Experiment 3**: take the same raters, the same probe, and the same fusion, and
point them at **invented characters no model has ever seen**. If the 0.75 fusion is measured from the
text, it should survive. If it's retrieved from memory, it should collapse. (It collapses.)
