# Per-Rater Decomposition of M4 Consensus (the paper Appendix)

This appendix expands the per-rater decomposition condensed in §4 of the paper. The body paragraph reports the headline numbers (M4 consensus MAE 0.230 vs single raters 0.242 / 0.286 / 0.306; Google Extraversion MAE 0.409 masked in the median); this file ships the full per-trait breakdown + bootstrap CIs.

## Overall per-rater performance

Per-rater performance against weighted multi-source ground truth on the comparison corpus (562 characters across 75 books), with 10,000-resample paired-character bootstrap 95% CIs. All three raters returned valid OCEAN vectors on 97.7% of the corpus (n ≈ 551 paired).

| Rater | Model | MAE | MAE 95% CI | Pearson r |
|-------|-------|-----|------------|-----------|
| OpenAI | gpt-5.2 | **0.242** | [0.235, 0.250] | 0.738 |
| Anthropic | claude-opus-4-6 | 0.286 | [0.276, 0.295] | **0.742** |
| Google | gemini-3-pro-preview | 0.306 | [0.296, 0.315] | 0.663 |
| **M4 consensus** | 3-rater median | **0.230** | **[0.223, 0.237]** | **0.770** |

The single strongest rater (OpenAI) loses to M4 consensus by 0.012 MAE.

## Per-trait MAE by rater

Lower is better; bold marks the per-trait single-rater winner. OpenAI wins four of five traits on point-wise accuracy.

| Rater | O | C | E | A | N |
|-------|---|---|---|---|---|
| OpenAI | **0.220** | **0.249** | **0.225** | 0.246 | **0.270** |
| Anthropic | 0.287 | 0.266 | 0.274 | 0.251 | 0.351 |
| Google | 0.251 | 0.318 | **0.409** | **0.246** | 0.297 |

**Google fails the conventional 0.30 threshold on Extraversion** (MAE 0.409). This rater-level failure is masked when only the M4 consensus median is reported. The per-rater breakdown is the load-bearing diagnostic.

## Three load-bearing findings (from §4)

1. **Consensus contributes signal even when one panel member is clearly strongest.** The strongest single rater (OpenAI, MAE 0.242) loses to the M4 consensus median (0.230) by 0.012 MAE.

2. **MAE ranking ≠ Pearson r ranking.** MAE ranks OpenAI < Anthropic < Google; Pearson r ranks Anthropic ≈ OpenAI > Google. The M4 median captures both rank orderings.

3. **Rater-level failures hide in consensus.** Google's Extraversion MAE (0.409) exceeds the 0.30 threshold. Practitioners selecting single-rater deployments need this per-rater breakdown.

## Reproducer

These numbers are recomputed from the shipped per-rater predictions in `paper_artifacts/method_bakeoff_v4/per_llm_bakeoff.csv` (one row per character per rater family, with predicted and ground-truth OCEAN), summarised in `paper_artifacts/method_bakeoff_v4/per_llm_bakeoff_summary.md`; the M4 consensus column comes from the `M4_consensus` block of `predictions.json`. No separate `per_rater_*.csv` derivative is shipped.

---

_Provenance: condensed from the "Per-rater decomposition of M4 consensus" subsection in the paper. Source: `paper_artifacts/method_bakeoff_v4/per_llm_bakeoff.csv`._
