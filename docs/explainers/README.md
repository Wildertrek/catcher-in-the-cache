# Explainers

Plain-language companions to *The Catcher in the Cache: Retrieval, Not
Measurement, in LLM Personality Inference* (Raetano, Gregor, Tamang,
ACM TIST under review).

The paper is dense by submission-page-budget necessity. These
explainers bleed off the friction without changing the science. Each
one targets a different reader profile and a different cluster of
"wait, what does that mean?" moments.

If the formal appendix is the reference card, this folder is the
tour guide.

---

## Tier 1, Core reader-friction fixes

**"I have five minutes and I just want the takeaway."**
→ [`reading_guide.md`](reading_guide.md)

**"Just explain the main figure / the central result to me."**
→ [`the_catch_explained.md`](the_catch_explained.md)

**"The numbers don't reconcile on first read (the 25-rater panel, 76 vs 75
vs 60+20 books, 562 characters)."**
→ [`numbers_decoder.md`](numbers_decoder.md)

**"OCEAN, HEXACO, OCEAN-6, OCEAN-HP, A vs A_HEX vs H, what is what?"**
→ [`battery_zoo.md`](battery_zoo.md)

**"M2 / M3 / M4 / M5 / M6, what does each method actually do?"**
→ [`method_zoo.md`](method_zoo.md)

**"I know LLMs but the psychometrics stats are foreign (ICC, MTMM,
Wilcoxon paired, BH-FDR)."**
→ [`psychometrics_glossary.md`](psychometrics_glossary.md)

---

## Tier 2, Topical deep dives

**"I'm a psychologist, what is an activation probe doing?"**
→ [`activation_probe_for_psychologists.md`](activation_probe_for_psychologists.md)

**"I'm an ML engineer, can I use this in my chatbot? How?"**
→ [`deployment_quickstart.md`](deployment_quickstart.md)

**"Which pre-registered questions were merged or retracted, and why?"**
→ [`rq_decoder.md`](rq_decoder.md)

**"How were the 20 synthetic characters made? Why does the design hold?"**
→ [`why_synthetic_chars.md`](why_synthetic_chars.md)

**"Why is the paper called 'The Catcher in the Cache'?"**
→ [`title_explainer.md`](title_explainer.md)

---

## Reading order by section of the paper

| If you got stuck at... | Read this first |
|---|---|
| §1 introduction headline numbers | [`numbers_decoder.md`](numbers_decoder.md) |
| §1 deployment tiering (HEXACO construct space; OCEAN cheap regressor floor) | [`battery_zoo.md`](battery_zoo.md) |
| §2.2 the 5-tier / 11-subtype GT taxonomy | [`numbers_decoder.md`](numbers_decoder.md) §3 |
| §3 the M2–M6 method definitions | [`method_zoo.md`](method_zoo.md) |
| §3 testing-rounds table (Pivots + Amendments) | [`rq_decoder.md`](rq_decoder.md) |
| §3 the Bar 1 / Bar 2 / Bar 3 diagnostic protocol | [`psychometrics_glossary.md`](psychometrics_glossary.md) |
| §4.2 RQ2.1 universal collapse claim | [`battery_zoo.md`](battery_zoo.md) §H vs A_HEX |
| §4.3 RQ3.1 collapse (n=25 panel) | [`numbers_decoder.md`](numbers_decoder.md) §1 |
| §4.3 the paired-collapse hero figure (how to read it) | [`the_catch_explained.md`](the_catch_explained.md) |
| §4.3 synthetic-substrate design | [`why_synthetic_chars.md`](why_synthetic_chars.md) |
| §4.4 activation-probe layer-depth, MLP, pool-ablation | [`activation_probe_for_psychologists.md`](activation_probe_for_psychologists.md) |
| §5 deployment tiering (HEXACO probe vs OCEAN cheap regressor floor) | [`deployment_quickstart.md`](deployment_quickstart.md) |
| Title (Catcher in the Cache) | [`title_explainer.md`](title_explainer.md) |

---

## Cross-references

- **Formal acronym + term reference card:**
  [`../appendix/glossary.md`](../appendix/glossary.md)
- **Deployment-time choice guide (which instrument to use):**
  [`../practitioners_guide.md`](../practitioners_guide.md)
- **Reproducibility (where the artifacts live):**
  [`../reproducibility.md`](../reproducibility.md)
- **Headline-number to artifact map:** the reproduction table in the
  [repo README](../../README.md)

---

## Provenance

Drafted 2026-05-21 in response to a reader-friction audit on
the paper. Not part of the manuscript submission; provided as
open companion material.
