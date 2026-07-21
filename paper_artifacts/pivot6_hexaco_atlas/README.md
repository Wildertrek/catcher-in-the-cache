# the cross-rater panel, HEXACO Panel Survey (25-model)

> **Panel note (superseded counts).** The numbers in this file are the original **26-rater** analysis run (26 pre-registered rater slots, of which 25 distinct models resolved) and match the JSON artifacts in this directory. The paper now standardizes on a single **25-rater panel (9 provider families)**: Grok 4.3 run once; the Amendment-9 additions Hermes-3 and Jamba dropped. Standardized values: Δ = −0.4473, RQ6.9 Wilcoxon p = 5.96×10⁻⁸ two-sided unadjusted (BH-adjusted 1.49×10⁻⁷), ICC = 0.577, η² = 0.697, family-clustering permutation p = 0.0032 unadjusted (BH-adjusted 0.008), signed synthetic +0.23 (20 of 25). Authoritative source: `panel25/panel25_results.json`. See `docs/explainers/numbers_decoder.md`.


**One-line summary.** A pre-registered HEXACO+OCEAN panel across 25 frontier
LLM raters from 9 provider ecosystems shows the within-rater
H↔A_HEX bipolarity collapse is **universal** (25/25 models above
|r|=0.30; mean 0.743) but drops by Δ=-0.444 on synthetic
characters absent from any training corpus, the central
**retrieval-not-measurement** finding for the paper.

## Headline verdicts

| RQ | Question | Verdict | Stat |
|---|---|---|---|
| RQ6.1 | Universal collapse | **PASS_locked** | 25/25 models &#124;r&#124; > 0.30 |
| RQ6.2 | Family clustering | **PASS** | ANOVA η²=0.755, p=0.003; ICC perm p=0.003 |
| RQ6.3 | Capability correlation | **NULL** | Arena ρ=-0.165, p=0.475 |
| RQ6.4 | Open vs closed | **DESCRIPTIVE** | open 0.795 vs closed 0.718, g=0.61 |
| RQ6.5 | Orthogonality discovery | **NO_OUTLIER** | no model below 0.30 |
| RQ6.6 | Head-to-head replication | **FAIL_proxy** | 12/25 var(A_HEX) ≥ var(OCEAN-A) |
| RQ6.7 | Alignment regime | **PASS** | η²=0.622, p=0.004; Hybrid uniquely low at 0.54 |
| RQ6.9 | **PRIOR_DRIVEN** (synthetic vs canonical) | **PASS_load_bearing** | mean Δ = **-0.444** (threshold ≥ 0.15) |
| Robustness | 3-seed stability | **STABLE** | mean within-model SD = 0.063 |

## What this panel shows

1. **The H↔A_HEX collapse is not Claude-family-specific.** It replicates universally across Anthropic / OpenAI / Google / Meta / Qwen / DeepSeek / Mistral / Cohere / xAI / Gemma raters.
2. **It is family-clustered.** Provider explains η²=0.755 of variance, p=0.003. Models from the same provider rate more like each other than like the marginal frontier-model norm.
3. **It is alignment-regime-dependent.** Google's hybrid RLHF+SFT+safety-filter pipeline produces a uniquely low mean |r|=0.54 vs CAI 0.78 / RLHF 0.83 / DPO 0.81 / SFT-only 0.71.
4. **It is not driven by capability.** Arena rank correlates ρ=-0.165 (n.s.) with |r|. Bigger / more capable does not mean less entangled.
5. **It is at least partly retrieval-driven, not structural.** On 20 synthetic characters with documented absence from canonical training corpora (3-rater negative-control: 0/20 recognized), the mean |r| drops by Δ=-0.444, three times the pre-registered ≥0.15 threshold. This is the **central reframing finding** for the paper: what looks like personality measurement on canonical literary characters is much more retrieval than structural trait encoding.

## What this panel does not show

1. **Mechanism at the representation level.** Whether H and A_HEX are entangled in the model's latent space or only at the post-training rating-time response is not testable from API calls. The activation-probe pilot (Upgrade 1) is deferred per Amendment 5 pending GPU compute. This is the natural activation-probe follow-up.
2. **Base-vs-instruct delta.** Whether instruction-tuning adds the collapse on top of base-model encoding is similarly deferred per Amendment 6 (OpenRouter does not expose base variants of the candidate families). Same activation-probe follow-up scope.
3. **Out-of-Western-canon generalization.** Synthetic characters are generated in the same broad literary-Western frame; non-Western / non-English substrate is queued for future work.

## Files

- `results.md`, full per-RQ statistical writeup (canonical)
- `analysis_summary.json`, machine-readable summary
- `cross_model_analyses.csv`, per-model statistics
- `bipolarity_atlas.csv`, full bipolarity table
- `bipolarity_atlas_v2.csv`, **superseded.** 28 rows: the 25 panel raters plus the
  duplicate `x-ai/grok-4.3` run and the two dropped Amendment-9 additions (Hermes-3,
  Jamba-Large-1.7). For the panel the paper reports, use `panel25/panel25_canonical_r.csv`.
- `panel25/`, **authoritative** standardized 25-rater panel (`compute_panel25.py`,
  `panel25_results.json`, `panel25_canonical_r.csv`)
- `synthetic_vs_canonical.csv`, Δ per model
- `seed_replication.json`, 3-seed SD per model
- `self_report_honesty_pilot.json`, Amendment 3 A3.2b
- `model_manifest.csv`, model manifest
- `arena_ranking_2026-05-17.csv` / `aai_ranking_2026-05-17.csv`, capability snapshots
- `alignment_regime_classification.csv`, Amendment 3 A3.2a classification
- `character_manifest.csv` / `character_manifest_synthetic.csv` / `character_manifest_20char_ablation.csv`
- `synthetic_characters_substrate.json` / `synthetic_characters_verification.json`, synthetic generation + negative-control
- `correlation_matrices.json`, 6×6 inter-trait correlation matrices per model
- `h5_head_to_head_details.json`, three-way head-to-head per model
- `hexaco_ratings_*.json` / `ocean_ratings_*.json`, raw probe outputs (25 models × seeds × substrates)

## Execution-time deviations

Documented in `results.md` §"Execution-time deviations from pre-reg" and in pre-reg Amendments 5 and 6. Summary: xAI manifest collapse (4 model deprecations same-day forced both slots to grok-4.3, effective N=1); gemini-2.0-flash 404 substitution; OpenAI Responses API parameter cleanup; Upgrade 1 + Upgrade 3 GPU/base-variant deferral.
