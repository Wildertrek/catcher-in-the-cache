# Method Comparison (Six Methods) + Cross-Provider HEXACO Triangulation

> Folder name note: `method_bakeoff_v4` is the frozen internal artifact-generation name
> (v4 = fourth data-generation run), kept so file paths in the paper and notebooks stay
> stable. "Six methods" = M1-M6; M1, the training-free floor, was added after this
> folder was named.

This folder contains the reproducibility artifacts for *The Catcher in the Cache: Retrieval, Not Measurement, in LLM Personality Inference* (under review, ACM TIST).

The paper compares five OCEAN inference methods on 562 ground-truth-annotated literary characters across 75 canonical works under a three-bar diagnostic protocol (per-method ground-truth recovery, corrected MTMM convergent validity, and external concurrent validity against Open Psychometrics SWCPQ), augmented with cross-provider HEXACO triangulation. The headline empirical finding is that OCEAN Agreeableness exhibits a bipolarity-style construct disagreement with one external label source that replicates across three independent rater families.

## Files in this folder

### Bar 1: per-method ground-truth recovery (562 chars)
- `bootstrap_per_method.csv`, per-method per-trait MAE / r / CCC with 10,000-resample paired-character bootstrap CIs (columns: `method, trait, n, MAE, MAE_lo, MAE_hi, r, r_lo, r_hi, CCC, CCC_lo, CCC_hi`; `_lo`/`_hi` are the 95% CI bounds; `trait = ALL` is the pooled row)
- `per_trait_winner.csv`, per-trait paired-bootstrap winner with BH-FDR-adjusted p-values
- `agreement_with_ci.csv`, pairwise inter-method agreement with bootstrap CIs

### Bar 2: corrected Campbell-Fiske MTMM (3 inequalities + 0.30 monotrait floor)
- `mtmm_matrix.csv`, full MTMM matrix with within-method off-diagonal cells
- `mtmm_convergent_discriminant.csv`, per-pair convergent/discriminant counts (3-of-4 strict + monotrait floor)
- `validated_traits.csv`, per-trait verdict combining the bars

### Bar 3: external concurrent validity vs Open Psychometrics SWCPQ
- `external_op_per_method.csv`, per-method per-trait MAE / r / CCC against OP labels
- `external_op_summary.csv`, top-line summary
- `calibration_heldout.csv`, 500 stratified random 30/30 train/test splits per method per trait
- `calibration_heldout_summary.json`, held-out generalization decision summary

### HEXACO cross-provider triangulation
- `hexaco_predictions.json`, 60-char Claude Sonnet 4.5 HH + A_HEXACO scores
- `hexaco_predictions_openai.json`, same 60 chars, OpenAI gpt-5.2
- `hexaco_predictions_google.json`, same 60 chars, Google gemini-2.5-pro
- `hexaco_diagnostic.csv` / `_openai.csv` / `_google.csv`, per-provider correlation diagnostics
- `hexaco_cross_provider.csv`, cross-provider correlations (pairwise HH agreement, HH vs OP-A, HH vs M4-A)
- `hexaco_cross_provider_summary.json`, pre-registered triangulation criterion result

### SCPI nearest-neighbor diagnostic
- `scpi_diagnostic.csv`, per-character disagreement-extreme nearest neighbors via SCPI FAISS
- `spi_projection.csv`, character-utterance embeddings projected through HEXACO/IPC panel

### Human-rater HEXACO panel (designed, not run)
- `panel_evidence_packs_manifest.json`, pre-registered 30-character selection for the future human-rater HEXACO panel (UTK IRB Cat 2 application + Prolific consent drafted separately)

## Reproducing the headline numbers

The CSVs above are direct outputs of `aperture_validation_v2.py`, `aperture_external_op.py`, `aperture_hexaco_probe.py` (per-provider), `scripts/hexaco_cross_provider.py`, and `scripts/calibration_heldout.py` in the parent project.

To re-run the analysis on these cached outputs (no new API spend):
- See the `notebooks/` directory in the repository root for reproduction notebooks
- See `paper_artifacts/method_bakeoff_v4/` (this folder) for raw data

## Triangulation criterion (pre-registered, met)

From `hexaco_cross_provider_summary.json`:
- Pairwise HH inter-rater r >= 0.7 across Claude / OpenAI / Google: **YES** (0.872, 0.818, 0.797)
- Each provider's HH disagreeing with OP-A at |r| < 0.4: **YES** (0.265, 0.213, 0.236)
- Decision: bipolarity claim is provider-independent triangulation across three rater families.

## Additional artifacts

These additional files extend the artifacts above. The folder name `method_bakeoff_v4/` is kept as the canonical artifact path (no rename):

- `stacked_ridge_ceiling.json`, RQ5 stacked-ridge ceiling on $\{M3, M4, M5, M6\}$ → OP labels under LOO ($\alpha=1.0$). Establishes how far four signal sources can be combined linearly against the external SWCPQ label, providing the ceiling reference for the body-text RQ5 result.
- `ocean_hp_cheap_head_v3.json`, LLM-free OCEAN-HP cheap-head Ridge regressor metadata. Reports H r=0.518 and $A_{\mathrm{HEX}}$ r=0.629 against the M4 teacher consensus on 562 chars under LOBO. Pickle ships in `personality_models/hexaco_ridge_heads_v3_full562.pkl`.

The files above remain untouched and continue to reproduce all headline numbers.

## License

Code: MIT (see repository LICENSE).
Data derived from public-domain literary text (Project Gutenberg) and the Open Psychometrics SWCPQ aggregated dataset (CC BY-NC-SA 4.0): see LICENSE-DATA.
