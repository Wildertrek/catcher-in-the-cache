# Reading Guide, the paper in Five Minutes

> *The Catcher in the Cache: Retrieval, Not Measurement, in LLM
> Personality Inference.* Raetano, Gregor, Tamang. ACM TIST under review.

For: anyone who picked up the paper, read a page or two, and wants
the takeaway before deciding to keep going.

---

## The one-sentence claim

When a modern LLM rates Elizabeth Bennet's personality, the
LLM is mostly retrieving a memorized character prior from its training
data, not measuring traits from the text in front of it.

## The one-paragraph version

We probed 25 frontier LLMs from 9 provider ecosystems on 60 canonical
literary characters (Bennet, Raskolnikov, Hamlet, Frankenstein, etc.) and
20 synthetic literary characters matched to the canon. On the canonical
characters, every LLM in our panel produced a sharp anti-correlation
between two trait dimensions that should mostly be independent: HEXACO
Honesty-Humility (H) and HEXACO Agreeableness (A). Mean
$|r| = 0.75$ across the panel, with all 25 raters above the
pre-registered 0.30 floor. On synthetic characters that look the same
on the page but cannot be in any LLM's training corpus, that
anti-correlation drops by $\Delta = -0.447$ (paired Wilcoxon $W = 0$,
$p_{\mathrm{BH}} = 1.5 \times 10^{-7}$). The same models, the same
prompts, the same probe battery, and the trait structure collapses
into something much closer to noise. The cleanest read of that gap
is canonical-substrate retrieval inflation: the LLMs are pattern-matching
to a stored personality summary for Bennet that they cannot do for a
character that doesn't exist outside our experiment.

## The headline number

**$\Delta = -0.447$** on the canonical-vs-synthetic paired Wilcoxon,
three times the pre-registered $|\Delta| \geq 0.15$ falsification threshold
(see §4.3, row RQ3.1).

The intuition: if LLMs were *measuring* personality from text, the
H↔A fusion should not depend on whether the character is famous.
It does, by a lot.

## Why this matters

| For... | The implication |
|---|---|
| LLM evaluation researchers | Personality benchmarks built on canonical characters confound retrieval ability with measurement validity. |
| AI safety / alignment | "Trait probes" of LLM behavior need synthetic controls; canonical probes overstate apparent trait structure. |
| Computational literary studies | LLM-generated character profiles are reliable on canonical chars *for retrieval-style use cases* (citation, summary, lookup) but not for novel character analysis. |
| Persona-init for chatbots | Use HEXACO as the construct space: probe in HEXACO at run time if an LLM is available (recommended), or fall back to the OCEAN O/C/E cheap regressor as the LLM-free floor at scale (O/C/E transfer out-of-cache; treat the cheap regressor H/A as research-only and A/N as weak there). |
| Open-weight safety research | The same retrieval signature appears in layer activations of open-weight models at 70B+ across three model families (Meta, Qwen, Mistral-MoE). |

## What the paper is *not* claiming

- **Not** "LLMs cannot do personality inference at all." On the
  canonical substrate, their outputs are stable, internally consistent,
  and correlate strongly with scholarly attributions.
- **Not** "the answer is mode-dissociation alone." The bipolarity
  collapse on synthetic characters persists even in subject-mode
  self-report, just with ~48% attenuation (mode-dissociation, §4.X).
- **Not** "training-data leakage is the whole story." We rule out
  capability (Arena rank), alignment regime, and family-by-family
  clustering as primary drivers in pre-registered tests.

## Where to look next

| Question | Section |
|---|---|
| How do you know the synthetic chars are "matched" to canon? | §2.1 corpus, [`why_synthetic_chars`](#) (tier-2 explainer) |
| How does ground truth work for fictional characters? | §2.2 + worked Bennet example |
| What are M2–M6 actually doing? | §3 + [`method_zoo.md`](method_zoo.md) |
| What is the activation probe seeing? | §4.4 + [`psychometrics_glossary.md`](psychometrics_glossary.md) §activation |
| If LLMs are retrieving, can I still use them? | §5 deployment + [`../practitioners_guide.md`](../practitioners_guide.md) |
| What about real humans? Does this transfer? | §6 limitations + the named F3 follow-up (HEXACO human-rater panel) |

## The title

"The Catcher in the Cache" is a Salinger reference (*The Catcher in the
Rye*, 1951). Holden Caulfield is not in our 76-book pipeline corpus,
but he is in every LLM rater's training cache, which is precisely
the phenomenon the paper diagnoses. The cache catches.

---

*Total read time so far: ~5 minutes. If you got this far and want to
keep going, the paper is built to be readable in one sitting; if you
hit a number that doesn't reconcile, jump to
[`numbers_decoder.md`](numbers_decoder.md). If you hit a stats term you
haven't seen recently, [`psychometrics_glossary.md`](psychometrics_glossary.md)
has one paragraph per term.*
