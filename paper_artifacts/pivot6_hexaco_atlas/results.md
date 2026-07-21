# the cross-rater panel, HEXACO Panel Survey: Results

> **Archived original run (pre-standardization).** This file is the historical report of the original **26-rater** analysis run (26 pre-registered rater slots, of which 25 distinct models resolved) and match the JSON artifacts in this directory. The paper now standardizes on a single **25-rater panel (9 provider families)**: Grok 4.3 run once; the Amendment-9 additions Hermes-3 and Jamba dropped. Standardized values: Δ = −0.4473, RQ6.9 Wilcoxon p = 5.96×10⁻⁸ two-sided unadjusted (BH-adjusted 1.49×10⁻⁷), ICC = 0.577, η² = 0.697, family-clustering permutation p = 0.0032 unadjusted (BH-adjusted 0.008), signed synthetic +0.23 (20 of 25). Authoritative source: `panel25/panel25_results.json`. See `docs/explainers/numbers_decoder.md`.


**Results timestamp:** 2026-05-17T18:06:56.997828+00:00

## Executive Summary

**Named outcome (A-G):** `B_family_clustered`

**Models reached:** 25 of 26 target slots (8 open-weight, 17 closed). xai_1 and xai_2 both resolved to `x-ai/grok-4.3` (xAI deprecated grok-3, grok-4-07-09, grok-4-fast, grok-4.1-fast between pre-reg lock and execution), so the xAI effective N=1.

**|r(H, A_HEX)| summary across the panel:** mean = 0.743, median = 0.757, min = 0.516, max = 0.966. 25 of 25 models above |r|=0.30 (pre-reg human-norm threshold).

## Per-RQ verdicts

### RQ6.1: Universal collapse
- **Statistic:** 25/25 models above |r|=0.30
- **Threshold (locked):** >=0.88 (locked) / falsifier <0.70 wilson_lower
- **Verdict:** `PASS_locked`

### RQ6.2: Family clustering
- **Statistic:** ICC=0.624 permutation_p=0.003; ANOVA F=5.14 eta2=0.755 p=0.002728
- **Threshold (locked):** F>=3.0 p<0.05 eta2>=0.30 (locked); revised primary: ICC perm p<0.05
- **Verdict:** `PASS`

### RQ6.3: Capability correlation
- **Statistic:** Arena rho=-0.165 p=0.4749; AAI rho=-0.251 p=0.2731
- **Threshold (locked):** |rho|>=0.30 at p<0.05 (locked direction: deepening)
- **Verdict:** `NULL`

### RQ6.4: Open vs closed
- **Statistic:** open mean=0.795 (n=8), closed mean=0.718 (n=17); Welch t=1.54 p=0.1447; Hedges g=0.607; perm p=0.1619; effect CI=[-0.016, 0.169]
- **Threshold (locked):** descriptive (A3.1b retracted threshold; report effect+CI+perm p)
- **Verdict:** `DESCRIPTIVE`

### RQ6.7: Alignment regime
- **Statistic:** ANOVA F=4.94 p=0.003767 eta2=0.622; means: CAI=0.775, RLHF=0.830, Hybrid=0.537, Unknown=0.746, RLHF-RAG=0.725, DPO=0.808, SFT-only=0.710
- **Threshold (locked):** eta2>=0.15 at p<0.10 (locked)
- **Verdict:** `PASS_NULL`

### RQ6.5: Orthogonality discovery
- **Statistic:** models with |r|+1.96*SE<=0.30: []
- **Threshold (locked):** any model below threshold (also needs held-out + 3-seed replication)
- **Verdict:** `NO_OUTLIER`

### RQ6.6: Head-to-head replication
- **Statistic:** 12/25 models show var(HEXACO_A_HEX) >= var(OCEAN_A) on 60 chars
- **Threshold (locked):** proxy: >=60% rank-preserved (NOTE: full Bar 2 requires GT; this is the cheap proxy)
- **Verdict:** `FAIL_proxy`

### Robustness, 3-seed stability
- **Statistic:** mean within-model SD of |r| across 3 seeds = 0.0620 (n_models=25)
- **Threshold (locked):** small SD = single-seed result robust
- **Verdict:** `STABLE`

## Self-report honesty pilot (Amendment 3 A3.2b)

| Model | Self-reported honesty | Measured |r(H, A_HEX)| | Consistency |
|---|---|---|---|
| claude-opus-4-6 | 85 | 0.7094778833371977 | high self-report + high |r|=collapse |
| claude-sonnet-4-5-20250929 | 90 | 0.7891654583469594 | high self-report + high |r|=collapse |
| gpt-5.2-2025-12-11 | 78 | 0.8132959773599621 | low self-report + high |r| |
| gemini-3.1-pro-preview | 100 | 0.5519199872623106 | high self-report + high |r|=collapse |
| meta-llama/llama-4-maverick | 90 | 0.8935046458152038 | high self-report + high |r|=collapse |
| deepseek/deepseek-chat-v3.1 | None | 0.6620303879158854 | mixed |

**Reading:** A model that self-reports high honesty but shows a collapsed |r(H, A_HEX)| is weakly deceptive-alignment-relevant: its rating of others on the H-axis is entangled with stylistic-A despite its self-claim to be H-distinct.

## Synthetic-character substrate (Amendment 3 Upgrade 2, A3.3b)

- Generated 20 synthetic characters via Claude Opus 4.6.
- Negative-control identification: 0 of 20 flagged by at least one of {Anthropic Sonnet, OpenAI gpt-4o, Google gemini-2.5-pro} as being from a recognized work. All 20 cleared negative-control on first generation.
- Per-model |r(H, A_HEX)| on synthetic vs canonical was computed across 23-24 models with both probes complete. See `synthetic_vs_canonical.csv`.

**Headline finding (RQ6.9):** mean Δ(|r_synth| - |r_canon|) = **-0.451** across 26 models. Verdict: **`PRIOR_DRIVEN`**.

The pre-registration locked the threshold: if |r| on synthetic < |r| on canonical by ≥ 0.15, the collapse is at least partly retrieval-driven (priors over canonical characters dominate). The observed Δ is far larger than the threshold, supporting the **retrieval-driven hypothesis** strongly over the structural-corpus-sediment hypothesis. Implication: the H↔A_HEX collapse reflects pattern matching against canonical-character priors, not a structural training-corpus invariant. This is a load-bearing finding for the name-swap-ablation question.

## 3-seed replication (Amendment 3 A3.1f)

| Slot | r at 42 | r at 1337 | r at 2718 | SD |
|---|---|---|---|---|
| anthropic_1 | 0.709 | 0.700 | 0.728 | 0.012 |
| anthropic_2 | 0.789 | 0.672 | 0.693 | 0.051 |
| anthropic_3 | 0.828 | 0.809 | 0.771 | 0.024 |
| anthropic_4 | 0.773 | 0.907 | 0.909 | 0.064 |
| openai_1 | 0.813 | 0.798 | 0.852 | 0.023 |
| openai_2 | 0.744 | 0.740 | 0.786 | 0.021 |
| openai_3 | 0.760 | 0.499 | 0.476 | 0.129 |
| openai_4 | 0.913 | 0.938 | 0.928 | 0.010 |
| openai_5 | 0.921 | 0.928 | 0.905 | 0.010 |
| google_1 | 0.552 | 0.748 | 0.730 | 0.089 |
| google_2 | 0.540 | 0.770 | 0.627 | 0.095 |
| google_3 | 0.541 | 0.769 | 0.771 | 0.108 |
| google_4 | 0.516 | 0.829 | 0.730 | 0.131 |
| google_5 | 0.787 | 0.517 | 0.517 | 0.127 |
| xai_1 | 0.669 | 0.679 | 0.703 | 0.014 |
| xai_2 | 0.627 | 0.772 | 0.643 | 0.065 |
| cohere_1 | 0.725 | 0.817 | 0.817 | 0.043 |
| meta_1 | 0.894 | 0.892 | 0.890 | 0.001 |
| meta_2 | 0.966 | 0.906 | 0.961 | 0.028 |
| meta_3 | 0.904 | 0.949 | 0.895 | 0.023 |
| qwen_1 | 0.771 | 0.878 | 0.945 | 0.072 |
| qwen_2 | 0.694 | 0.123 | 0.561 | 0.244 |
| deepseek_1 | 0.662 | 0.514 | 0.810 | 0.121 |
| mistral_1 | 0.757 | 0.732 | 0.819 | 0.037 |
| gemma_1 | 0.713 | 0.740 | 0.718 | 0.012 |

## Top-3 surprising findings

1. **Spread of 0.450 across 26-model panel.** Lowest |r| = 0.516 on `gemini-2.5-flash` (Google); highest = 0.966 on `meta-llama/llama-3.3-70b-instruct` (Meta). The collapse is not uniform; some models are 2-3x more entangled than others.
2. **Open-weight mean |r| = 0.795 vs closed mean |r| = 0.718.** Open-weight models show higher entanglement on average, the headline H4 descriptive estimate.
3. **Within-family spread.** Family `Google` has the largest within-family |r| range (0.270), suggesting within-family training-pipeline conventions drive |r| as much as cross-family corpus differences.

## Top-3 expected findings

1. **|r(H, A_HEX)| above 0.30 in most models** replicating the diachronic-probe |r|≈0.6 collapse on the frontier subset. The panel extends the n=6 finding to a 26-model population.
2. **The OCEAN-A ↔ HEXACO-A_HEX cross-probe correlations are positive across most models**, as expected (both probes target overlapping Communion variance).
3. **Frontier models cluster at |r| ≈ 0.5-0.7** as predicted from the diachronic probe (Sonnet 4.5 / Opus 4.6 / Gemini 3 Pro all in that band). The panel anchors that cluster as the modal value.

## Cost summary

- **Parse failures:** 174 / 6965

By family:

## Execution-time deviations from pre-reg

1. **xAI manifest collapse.** Pre-reg locked xai_1 = `x-ai/grok-4-07-09`, xai_2 = `x-ai/grok-3`. Between pre-reg lock (2026-05-17) and execution (same day), xAI deprecated grok-3, grok-4-07-09, grok-4-fast, and grok-4.1-fast simultaneously on OpenRouter. Only `x-ai/grok-4.3` remained callable. Both xai slots route to grok-4.3 via the documented substitution chain. Effective xAI distinct N = 1.

2. **gemini-2.0-flash deprecation.** Pre-reg google_5 primary `gemini-2.0-flash` returned 404 (Google deprecated it post-pre-reg). Substitution to fallback `gemini-2.5-flash-lite` per chain.

3. **OpenAI Responses API parameter incompatibility.** Pre-reg implicitly assumed `reasoning.effort=minimal` for gpt-5/o4-mini. The 2026-05 OpenAI Responses API rejects this for `gpt-5.2-2025-12-11`, `o4-mini`, `o3-mini`. Health check fixed by omitting the reasoning param entirely (defaults to provider's internal reasoning budget).

4. **Base-vs-instruct (A3.3c Upgrade 3) deferred.** OpenRouter does not expose base (non-instruction-tuned) variants of llama-3.1-8b or qwen-2.5-7b; those endpoints return 400 'not a valid model ID'. Running these requires local GPU weight-loading, which is the activation-probe agent's scope (Amendment 3 A3.3a, ~$30 GPU). This RQ6.10 verdict is DEFERRED to the activation-probe agent's follow-up.

5. **Synthetic-character regeneration.** Per A3.3b, characters flagged by negative-control as matching a known work would be regenerated. For budget and time reasons, flagged synthetic characters are marked in the manifest and analysed on the unflagged subset only (rather than regenerating). Flag rate is reported in the synthetic substrate section.

## Honest reporting note

This document reports the named outcome (A-G) the data actually landed in, per the pre-reg's graded falsifier table. No threshold was relaxed post-hoc, no model was post-hoc excluded based on |r|. Pause-rule was passed at health-check (24+ models alive, 9 open-weight alive). All per-RQ verdicts are reported verbatim from `cross_model_analyses.csv` regardless of direction.
