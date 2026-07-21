# RQ7 HEXACO Cross-Provider Triangulation, the paper Appendix

This appendix expands the cross-provider HEXACO triangulation condensed in §4 RQ7 of the paper. The body paragraph reports the headline numbers (pairwise H inter-rater r ∈ [0.80, 0.87]; M4-A vs each provider's H at r ∈ [0.58, 0.69]; OP-A vs each provider's H at r ∈ [0.21, 0.27]; Steiger Z p < 0.01 across all three rater families; within-rater H↔A_HEX collapse universal across providers); this file ships the full per-comparison tables.

## Full cross-provider HEXACO triangulation table

n=60 OP-overlap characters, Claude Sonnet 4.5 + OpenAI gpt-5.2 + Google gemini-2.5-pro.

### Pairwise inter-rater agreement on H (Honesty-Humility)

| Comparison | n | Pearson r | p |
|---|---|---|---|
| Claude vs OpenAI | 60 | **0.872** | 1.2×10⁻¹⁹ |
| Claude vs Google | 60 | **0.818** | 1.5×10⁻¹⁵ |
| OpenAI vs Google | 60 | **0.797** | 2.4×10⁻¹⁴ |

### Pairwise inter-rater agreement on A_HEX (HEXACO Agreeableness)

| Comparison | n | Pearson r | p |
|---|---|---|---|
| Claude vs OpenAI | 60 | 0.797 | 2.5×10⁻¹⁴ |
| Claude vs Google | 60 | 0.722 | 7.7×10⁻¹¹ |
| OpenAI vs Google | 60 | 0.756 | 2.9×10⁻¹² |

### Each provider's H vs OP-A (the bipolarity-confounded label)

| Comparison | n | Pearson r [CI] | p |
|---|---|---|---|
| H (Claude) vs OP-A | 60 | 0.265 [-0.09, +0.58] | 0.040 |
| H (OpenAI) vs OP-A | 60 | 0.213 [-0.09, +0.48] | 0.102 |
| H (Google) vs OP-A | 60 | 0.236 [-0.07, +0.53] | 0.069 |

### Each provider's H vs M4-A and pipeline GT-A

| Comparison | n | Pearson r | p |
|---|---|---|---|
| H (Claude) vs M4-A | 60 | **0.691** | 1.0×10⁻⁹ |
| H (OpenAI) vs M4-A | 60 | **0.584** | 9.9×10⁻⁷ |
| H (Google) vs M4-A | 60 | **0.667** | 5.9×10⁻⁹ |

## Steiger Z test on dependent correlations

Because each provider's H is correlated with both M4-A and OP-A, the two comparisons share H and are dependent. We apply Steiger's Z test for the difference of dependent correlations (Steiger 1980) to test whether each provider's H-vs-M4-A correlation differs significantly from its H-vs-OP-A correlation.

| Rater family | t statistic | p value |
|---|---|---|
| Claude | +3.58 | 0.0007 |
| OpenAI | +2.82 | 0.0065 |
| Google | +3.54 | 0.0008 |

Across all three rater families the H-vs-M4-A agreement exceeds the H-vs-OP-A agreement at p < 0.01, formally rejecting the null that the two correlations are equal.

## HEXACO factor-purity replication across providers

The within-Claude H↔A_HEX correlation reported in the body Table 1, r=0.581, was flagged as unusually high relative to the human-population literature norm r ∈ [0.20, 0.30]. The cross-provider replication answers whether this is a Claude-specific factor-purity issue or a structural property of contemporary frontier LLM raters on literary-character text.

| Rater family | Within-rater H vs A_HEX r | Bootstrap 95% CI |
|---|---|---|
| Claude | 0.581 | [0.399, 0.730] |
| OpenAI | 0.659 | [0.526, 0.762] |
| Google | 0.615 | [0.419, 0.778] |

(n=60 chars, 10,000 bootstrap resamples.)

The collapse replicates. All three rater families recover an H-vs-A_HEX correlation roughly twice the human-population norm. We read this as a structural LLM-rater limit: contemporary frontier LLMs do not cleanly separate the H and Agreeableness factors when scoring literary characters, even with explicit framework-prompt scaffolding. The qualitative inversion pattern (charismatic antagonists low on H, warm-affiliative chars high on H + A_HEX) is preserved across all three providers, but factor purity is weaker than human-rater HEXACO data, a finding that motivates the human-rater HEXACO panel flagged as extension flag F3.

## Single-prompt sensitivity check

A natural alternative is that scoring both factors in one rater pass induces within-prompt anchoring. We tested this on Claude Sonnet 4.6 with the same 60 chars under (i) one combined prompt and (ii) two separated single-factor prompts. Separation does not drop the correlation: r_sep = 0.866 vs r_comb = 0.693. The factor-purity gap is a representational property of the rater, not a prompt-engineering artifact.

## Reproducer

These numbers are computed in `notebooks/02_method_bakeoff_results.ipynb` (cell loading `paper_artifacts/method_bakeoff_v4/hexaco_cross_provider_summary.json` and `hexaco_predictions_*.json`).

---

_Provenance: condensed from §4.X "Cross-provider replication" sub-paragraph in the paper RQ7. Source: hexaco_cross_provider_summary.json + hexaco_predictions_anthropic.json / _openai.json / _google.json. Reproducer: NB02 RQ7 cells._
