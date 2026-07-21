# Cheap-Head Ridge Regressor, Deployment Details, the paper Appendix

This appendix expands the cheap regressor deployment details condensed in §4 of the paper. The body subsection reports the headline (Ridge regressor over OpenAI text-embedding-3-large mean-utterance pool with per-factor LOBO MAE/r table; ~60× faster and ~61× cheaper than M4 baseline); this file ships the architecture details, deployment-cost calculation, and factor-purity inheritance discussion.

**Where this regressor sits in the deployment recommendation.** The construct-space recommendation for LLM persona work is **HEXACO**: probe in HEXACO directly when an LLM is available at run time (the recommended path). This cheap regressor is the **LLM-free floor** for use at scale. It emits seven factors, but only its **O/C/E** outputs are trustworthy out-of-cache (on synthetic/novel characters): O, C, and E lie off the fused moral axis and transfer. A and N are weak out-of-cache, and the cheap regressor H and A_HEX are research-replication-only out-of-cache (they are trained on single-provider Claude Sonnet 4.5 HEXACO labels and carry the canonical H↔A_HEX fusion). The O/C/E generalization comes from the off-axis geometry of those factors, **not** from any LLM-independent or human-derived supervision; the OCEAN head is trained on M4 multi-provider LLM-consensus labels.

## Architecture details

**Feature.** OpenAI `text-embedding-3-large` 3072-dimensional embeddings, mean-pooled over each character's quoted utterances + narrator-attributed dialogue. Embedding API cost: ~$0.001/char.

**OCEAN-5 head.** Ridge regressor with α = 1.0 (selected by 5-fold cross-validation grid search over α ∈ {0.01, 0.1, 1.0, 10.0, 100.0}). Trained on the 562-character corpus with M4 multi-provider consensus labels as the teacher signal (mean of Anthropic Claude Sonnet 4.5 + OpenAI gpt-5.2 + Google Gemini 2.5 Pro per-trait predictions).

**H and A_HEX heads.** Ridge regressor over the same 3072-d embedding feature, α = 0.1 (selected by 5-fold CV grid search; lower α than OCEAN-5 because the HEXACO probe targets have lower variance and benefit from less regularization). Trained on the full 562-char corpus with single-provider Claude Sonnet 4.5 HEXACO probe labels as the teacher signal. One-time training cost: $3.30 for the full-corpus HEXACO probe.

**Inference path.** Single OpenAI embedding API call (~0.5 s/char, ~$0.001/char) followed by Ridge prediction (~1 ms/char on commodity CPU). Total: ~0.5 s/char and ~$0.001/char.

## Deployment-cost comparison

| Method | Latency | Cost | Speed multiplier | Cost multiplier |
|---|---|---|---|---|
| M4 baseline (mean of 3 frontier providers) | ~30 s/char | ~$0.061/char | 1× | 1× |
| Cheap head Ridge (this regressor) | **~0.5 s/char** | **~$0.001/char** | **60×** | **61×** |

The price of the speedup is the per-factor MAE gap reported in the body Table relative to the teacher signal, correctness up to a known, documented LOBO-validated tolerance.

## Factor-purity inheritance

The within-rater H↔A_HEX correlation in the teacher labels (r = 0.681) propagates into the cheap regressor (r = 0.761 on LOBO predictions). The regressor cannot recover orthogonality the teacher labels did not produce. This is a measurement-side limit (the LLM rater doesn't cleanly separate H from A_HEX on this substrate, see RQ7 cross-provider replication appendix), not a regressor-side limit.

Practitioners deploying the cheap regressor against literary-character text inherit this factor-purity gap. The HEXACO factor-purity panel (extension flag F3, Prolific n=30 human-rater HEXACO panel) is the queued anchor against which to validate H and A_HEX deployment.

## Pickle locations and minimal loader

The trained Ridge regressors ship as committed pickles:
- `personality_models/ocean_ridge_regressor_v2_cheap.pkl`, OCEAN-5 head
- `personality_models/hexaco_ridge_heads_v3_full562.pkl`, H + A_HEX heads
- `personality_models/MODEL_CARD.md`, model card with provenance + training metadata

Minimal loader code in the practitioner's guide (`docs/practitioners_guide.md`) implements a 10-line wrapper that takes a character name + utterance corpus and returns the seven-factor vector. For out-of-cache deployment, trust only the O/C/E outputs of that vector (the LLM-free floor); use a run-time HEXACO probe for the moral-axis signal when an LLM is available.

## Reproducer

Cheap-head LOBO numbers are computed in `notebooks/02_method_bakeoff_results.ipynb` (cell loading `paper_artifacts/method_bakeoff_v4/ocean_hp_cheap_head_v3.json`).

---

_Provenance: condensed from §4.X "LLM-free OCEAN-HP cheap regressor" subsection in the paper. Source: ocean_hp_cheap_head_v3.json + ocean_ridge_regressor_v2_cheap.pkl + hexaco_ridge_heads_v3_full562.pkl. Reproducer: NB02 cheap regressor cells._
