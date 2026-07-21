# Experiment 3: The Catch, does the fusion survive on characters the models never saw?

A plain-language explainer. Read `experiment_1_three_bars.md` and `experiment_2_hexaco_atlas.md` first.
This is the payoff experiment, the one the whole paper is built to reach.

## The one-sentence version
Experiment 2 showed the raters fuse Honesty-Humility with Agreeableness at 0.75, but on **famous**
characters the models have read many times. **Experiment 3 rebuilds the test on invented characters no
model has ever seen.** If the fusion is *measured from the text*, it should survive. If it's *retrieved
from memory*, it should collapse. It collapses.

## The trick: synthetic characters
We wrote **20 brand-new literary characters** that do not exist anywhere, matched to real canonical
characters on genre, period, length, and prose style, but **absent from any training data**. Crucially,
we authored them so that Honesty-Humility and Agreeableness are **deliberately pulled apart** (designed
correlation **r = −0.74**, the opposite of the fused +0.75). A faithful *measuring* instrument should
recover that designed separation. A *retrieving* one has nothing to look up.

## The result: the fusion collapses
We re-ran the **same 25 raters** with the **same probe** on these invented characters. The fusion
**dropped from 0.75 to 0.30**: a fall of **Δ = −0.447**, and **every single one of the 25 raters
decreased** (a paired test rules out chance overwhelmingly: p ≈ 0.00000006). 

> Same models, same questionnaire, same prompt. **The only thing that changed is whether the character
> exists in the model's memory.** A property that holds on cached characters and vanishes on novel ones
> was never measured from the text, it was retrieved from the cache.

A nuance worth stating honestly: the fusion collapses *toward zero* (to about +0.23 on average), not all
the way down to the designed −0.74. The retrieved prior switches off; what's left is weak and near-zero,
not a clean recovery of the designed structure. That's still decisive, a *measured* signal wouldn't
depend on cache membership at all.

## Ruling out the boring explanation
A skeptic could say: maybe the invented characters are just **thinner**: harder to read, so *no* rater
could recover their structure, cache or not. We tested this two ways, and both fail the skeptic:

1. **Subject mode.** We gave three raters the full 240-item questionnaire and asked them to answer **as**
   each character (rather than *rating* the character). In this mode the design **is** recoverable: on the
   synthetics the correlation comes out **negative (−0.33)**, in the designed direction, while on famous
   characters it matches the real human value (+0.45). So the designed structure is genuinely present in
   the text, the judge-mode failure is specific to *rating*, exactly what a retrieval account predicts.
2. **Fusion without any text at all.** Give a rater only a character's **name and title, no evidence** , 
   and it fuses even harder (**+0.83**). Give it the same character's *text*, and the fusion switches off
   (**−0.45**). Since these characters were never written, the +0.83 can't be a memory of a specific
   character; it's a **generic prior the model falls back on when it cannot measure.**

## The deployable payoff: a cache-membership gauge
The practical takeaway isn't just "LLMs retrieve", it's that **you can tell, per character, when they're
about to.** Every character has a **cache-membership score** (how close it sits to the training corpus).
The famous characters cluster high (median **0.87**); the invented ones cluster low (median **0.41**), and
the two barely overlap. A simple threshold at **0.55** separates them almost perfectly (**AUC 0.99**), with
only a **2.3%** false-flag rate while catching every out-of-cache character.

That gauge is the deployable handoff: before a system trusts an LLM-derived personality for a character,
it can check whether that character is *in cache* (the rating may be retrieved, treat with caution) or
*out of cache* (the model has nothing to retrieve, and, per this experiment, shouldn't be trusted to
measure it either).

## What Experiment 3 establishes
- On cached characters, LLM personality rating is **largely retrieval, not measurement**: shown by a
  structure that holds on famous characters and collapses on invented ones.
- The collapse is **not** stimulus poverty (the design is recoverable in subject mode and switches on/off
  with evidence).
- A **cache-membership gauge** flags the risk per character, turning the finding into a deployable check.

This is why the paper's title is *Catcher in the Cache*: the instrument that looked like it was measuring
personality was, on famous characters, catching a memorized prior out of the cache.
