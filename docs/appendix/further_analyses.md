# Further pre-registered analyses (headline results)

The paper's Experiments 1-3 carry the retrieval-not-measurement claim. These
supporting analyses were pre-registered (amendments A2-A5 and the mode-dissociation
and cross-provider protocols; see [`rq_decoder.md`](../explainers/rq_decoder.md))
and are summarized here with their locked thresholds and observed outcomes. Raw
per-condition artifacts beyond these summaries are available on request.

## A.12 Robustness probes (pre-registered A2-A5)

**Name-swap / literary-priors ablation (A2, n=59).** The 60-character OP-overlap
subset re-rated under three conditions: (a) full evidence, (b) name only, (c)
name-redacted. Locked ceiling |r(evidence, name-only)| <= 0.70; observed **0.848**
(falsifier triggered: on canonical characters, name alone recovers most of the
full-evidence profile). This is the memorization-retrieval result the paper's
out-of-corpus substrate (Experiment 3) was designed to decouple: on canonical
characters, priors and evidence encode the same signal because both reflect
training-corpus presence.

**Generative-consistency channel check (A3, n=28).** Three frontier raters (Claude
Opus 4.6, GPT-5.2, Gemini 3 Pro Preview) each generated ~800-word passages targeted
at characters' M4 OCEAN profiles; the 3x3 generate-and-score recovery matrix has
**min diagonal r = 0.870** with max off-diagonal drop 0.055 (**channel sharing:
strong pass**). Cross-rater convergence on M4 profiles reflects a shared latent
construct, not a per-rater heuristic.

**Diachronic within-family scaling probe (A4, 6 models, n=57).** Per-family
delta-|r(H, A_HEX)| (newer minus older): Anthropic **+0.036**, OpenAI **-0.152**,
Google **-0.061**. The |r| ~ 0.6 fusion replicates across six independently
developed models from three training pipelines but does not scale monotonically
with generation. Named outcome: **H3-mixed (family-asymmetric)**.

**De novo factor structure (A5).** Exploratory factor analysis on the raw panel
rating matrices (no reference to scholarly labels): on four matrices (OCEAN-5
per-rater N=2,004; HEXACO N=171; OCEAN-HP N=168; combined 11-trait N=132),
Horn's parallel analysis recommends **3 / 1 / 2 / 4 factors**, well below the
5/6/7/11 nominally encoded. At every matrix, H, A_HEX, and OCEAN-A co-load on a
single communal-decent factor (**loadings 0.73-0.86**); cross-rater Tucker
congruence on the 4-factor combined solution is phi in [0.94, 0.95]. The collapse
is visible at the loading level, independent of any ground truth.

## A.13 Subject-mode dissociation (6-model, pre-registered)

Within-model subject-mode r(H, A_HEX) from N=10 self-report elicitations per model,
paired against judge-mode |r| from the panel. Locked Branch-A (mode-specific)
criteria: subject median |r| < 0.30 **or** delta >= 0.40. Observed: judge median
**0.792** -> subject median **0.407** (delta 0.385). Both thresholds missed (by
0.107 and 0.015): **Branch B, attenuated-but-persistent** -- the H-A_HEX fusion is
not judge-mode-specific. Per-model: Opus 4.6 judge 0.709 / subject 0.268; GPT-5.2
0.813 / 0.719 (strong subject-mode fusion); with the remaining four models between.
This is the paper's Discussion claim that the two artifact families (respondent-side
response bias, rater-side retrieval) coexist. Note: distinct from the character-level
subject-mode IPIP manipulation check (Experiment 3b), which is in-paper.

## A.14 Cross-provider triangulation and second external source

**Cross-provider replication of the HEXACO triangulation.** The OP-A failure
localization (paper Appendix A) replicates on GPT-5.2 and Gemini 2.5 Pro:
inter-rater H correlations r in [0.80, 0.87]; Steiger's Z for the
consensus-A-vs-H versus OP-A-vs-H contrast is significant at p < 0.01 within each
provider family. The Agreeableness verdict does not rest on a single vendor.

**Big Five Backstage second external source.** The A inversion reproduces on the
Big Five Backstage corpus (Tiuleneva et al. 2024; n=28 Ibsen characters) under a
completely different labeling regime, so the Bar-3 Agreeableness failure is not an
artifact of the SWCPQ Ridge-PCA mapping alone.

## Compute budget

Realized spend for the pre-registered experiment program: **~$85 of a $175
pre-registered cap** (~49%). Pre-specifications were locked as timestamped git
commits before the corresponding LLM calls; the amendment trail is in
[`rq_decoder.md`](../explainers/rq_decoder.md).

## Register-matched control (three substrates)

To separate corpus novelty from prose register, three raters (Claude Opus 4.6, GPT-4o, Gemini 3.1 Pro) scored three substrates under one probe: the canonical characters, a set of period-matched nineteenth-century pastiche characters (written in the register of the canon but absent from it), and the modern synthetic characters. The fusion collapses on the register-matched pastiche just as on the modern synthetics, so the effect tracks absence from the training corpus, not writing style.

| Substrate | mean \|r(H, A)\| | signed mean r(H, A) |
|-----------|----------------:|--------------------:|
| Canonical (same 3 raters) | 0.65 | +0.65 |
| Register-matched (19th-c. pastiche) | 0.31 | +0.02 |
| Modern synthetic | 0.39 | -0.13 |
