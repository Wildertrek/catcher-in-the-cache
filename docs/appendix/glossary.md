# Acronym + Term Glossary

Quick-reference glossary for *The Catcher in the Cache: Retrieval, Not
Measurement, in LLM Personality Inference* (ACM TIST). Organized by
category. First appearance per term cross-referenced to paper section.

---

## System name + identity

| Term | Expansion | First in |
|---|---|---|
| **APERTURE** | Automated PERsonality TUning, Representation, and Evaluation. The multi-method multi-rater diagnostic system this paper introduces. | §1 *The system* |
| **The Catcher** | Informal shorthand for the two-part diagnostic apparatus (substrate falsifier + activation probe) that catches retrieval-vs-measurement on canonical literary characters. | §1 *The Catcher* preamble (§4) |
| **The Cache** | The LLM's internal representation of its training corpus, patterns distributed across the model's weights, accessible at inference time as if from a memorized lookup table. | Title + §1 titlenote |
| **OCEAN** | OCEAN personality traits: Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism. | §1 *Why this work* |
| **HEXACO** | Six-factor lexical personality model: Honesty-Humility, Emotionality, eXtraversion, Agreeableness, Conscientiousness, Openness (Ashton & Lee 2007). | §1 *The experiments* |

## Trait-vector shorthand

| Term | Expansion | First in |
|---|---|---|
| **H** or **HH** | HEXACO Honesty-Humility (sincerity / manipulation / modesty axis). | §1 + §3 |
| **A** (data column `A_HEX`) | HEXACO Agreeableness (forgiveness / gentleness / patience axis, distinct from OCEAN Agreeableness). The paper writes **A** for HEXACO Agreeableness; the released data, columns, and code use **`A_HEX`** to keep it separate from the OCEAN letter A. Both name the same construct. | §1 + §4.5 |
| **OCEAN-HP** | Seven-factor vector: OCEAN-5 + H + A. "HP" = "H" + "P" (Patience shorthand for A); proposed for downstream computational character modeling. | §1 *The experiments* |
| **OCEAN-6** | Six-factor vector: OCEAN-5 + H only (drops A). Backwards-compatible with OCEAN-keyed deployment surfaces, but not the construct-space recommendation: no OCEAN variant resolves the moral-axis-vs-warmth conflation in A, so HEXACO is the recommended construct space (with the OCEAN O/C/E cheap regressor as the LLM-free floor at scale). | §1 *The experiments* |
| **HEXACO** | Standard HEXACO six-factor vector (H, E_HEX, X, A_HEX, C_HEX, O_HEX) as it appears in the released data columns; the paper writes these as H, E, X, A, C, O. | §1 *The experiments* |

## Methods comparison (M2–M6)

| Term | Expansion | First in |
|---|---|---|
| **M2** | Random-Forest classifier (5-class per-utterance OCEAN; deployed as continuous regressor in the comparison). | §3.1 |
| **M3** | Random-Forest regressor on `text-embedding-3-large` character mean-utterance embeddings (3072-d). | §3.2 |
| **M4** | Multi-provider LLM consensus (Anthropic + OpenAI + Google; median across providers). | §3.3 |
| **M5** | Single held-out LLM probe (Anthropic Claude Sonnet 4.5; character name redacted). | §3.4 |
| **M6** | Semantic Character Personality Index (SCPI): similarity-weighted k-NN over character embeddings; LOBO-fair. | §3.5 |

## Ground-truth taxonomy

| Term | Expansion | Weight | First in |
|---|---|---|---|
| **AGT** | Academic Ground Truth (peer-reviewed psychological-criticism scholarship). | 0.50–1.00 per subtype | §2.2 |
| **SGT** | Scholarly Ground Truth (research-agent-curated authoritative sources, e.g., Zimbardo & Johnson on Shakespearean characters). | 0.65–0.80 | §2.2 |
| **PGT** | Psychometric Ground Truth (Open Psychometrics SWCPQ + Big Five Backstage). | 0.40–0.55 | §2.2 |
| **MGT** | Manual Ground Truth (authors-of-record direct annotation). | 0.85 | §2.2 |
| **CGT** | Consensus-as-Ground-Truth (LLM consensus fallback; downweighted to avoid method-self-evaluation circularity). | 0.20–0.35 | §2.2 |

## Diagnostic protocol

| Term | Expansion | First in |
|---|---|---|
| **Bar 1** | Per-method ground-truth recovery (MAE / Pearson r / CCC vs weighted multi-source GT). | §3 |
| **Bar 2** | Corrected Campbell-Fiske three-inequality multitrait-multimethod (MTMM) convergent validity, with absolute monotrait $r \geq 0.30$ floor. | §3 |
| **Bar 3** | External concurrent validity vs Open Psychometrics SWCPQ Ridge-mapped OCEAN labels (n=60 OP-overlap subset). | §3 |
| **MTMM** | Multitrait-multimethod matrix (Campbell & Fiske 1959). | §3 |
| **LOBO** | Leave-One-Book-Out (held-out generalization scheme for M3 + M6). | §3.5 + §4.2 |
| **CCC** | Lin's Concordance Correlation Coefficient (penalises both location and scale bias). | §3.7 |
| **BH-FDR** | Benjamini-Hochberg false-discovery-rate control. | §3 |

## Pre-registration milestones

| Term | Expansion | First in |
|---|---|---|
| **Name-swap ablation** | Literary-priors-vs-sedimentation (name-swap / name-redacted re-rating). | [`further_analyses.md`](further_analyses.md) §A.12 |
| **Generative-consistency test** | Channel-sharing test (3 frontier raters generate × score). | [`further_analyses.md`](further_analyses.md) §A.12 |
| **Diachronic probe** | Within-family scaling probe (6 models, 3 families). | [`further_analyses.md`](further_analyses.md) §A.12 |
| **De novo EFA** | De novo factor structure (EFA on rater matrices). | [`further_analyses.md`](further_analyses.md) §A.12 |
| **the cross-rater panel** | 25-rater HEXACO panel survey + substrate falsifier. | §4.2-4.3 |
| **PRIOR_DRIVEN** | the cross-rater panel RQ6.9 named outcome: synthetic-substrate bipolarity drop selects (b) retrieval over (a) genuine training-corpus structure. | §1 + §4.2 |
| **mode-dissociation** | Mode-dissociation extension (judge-mode vs subject-mode bipolarity fusion test). | [`further_analyses.md`](further_analyses.md) §A.13 |
| **A1–A11** | Pre-registration amendments (chronology in §3 testing-rounds table). | §3 |

## Statistical methods

| Term | Expansion | First in |
|---|---|---|
| **ICC** | Intraclass Correlation Coefficient (McGraw & Wong 1996 reliability framework). | §1 + §4.2 |
| **CR1** | Cluster-Robust SE (asymptotic; Stata-CR1 = HC1 with cluster correction). | [`further_analyses.md`](further_analyses.md) |
| **Wild bootstrap** | Wild cluster bootstrap robustness check (Rademacher signs × per-cluster residuals). | [`further_analyses.md`](further_analyses.md) |
| **Hedges *g*** | Small-sample-corrected effect size (Hedges 1981). | [`further_analyses.md`](further_analyses.md) |
| **LRT** | Likelihood-Ratio Test. | §1 + §4.2 |
| **EFA** | Exploratory Factor Analysis. | [`further_analyses.md`](further_analyses.md) |
| **PCA** | Principal Component Analysis. | §3.5 (SCPI features) + §4.2 |

## Instruments + corpora

| Term | Expansion | First in |
|---|---|---|
| **BFI** | OCEAN Inventory (44-item self-report; John 2008 paradigm). | §4.13 (mode-dissociation bridge) |
| **IPIP-50** | International Personality Item Pool 50-item OCEAN inventory (Goldberg 1999). | §4.13 |
| **NEO-PI-R** | Costa & McCrae 1992 Revised NEO Personality Inventory; M4 probe-prompt style derives from NEO facet definitions. | §3.3 |
| **HEXACO-PI-R** | HEXACO Personality Inventory Revised (Ashton & Lee). | §4.5 |
| **HEXACO-100** | 100-item HEXACO observer form (Lee & Ashton 2018). | §6.9 + §7 F3 |
| **OP / SWCPQ** | Open Psychometrics Statistical "Which Character" Personality Quiz (~1.5M crowd raters, 401 behavioral-attribute scales). | §3 + §4.3 |
| **BFB** | Big Five Backstage drama corpus (Tiuleneva et al. 2024). | §6.11 |
| **PsychoBench** | LLM-personality benchmark in rater-as-subject mode (Huang et al. 2024). | §1 + §4.13 |
| **TRAIT** | LLM-personality benchmark with psychometric framing (Lee et al. 2025). | §1 + §4.13 |

## SCPI methodological family

| Term | Expansion | First in |
|---|---|---|
| **SPI** | Structural Personality Index (from the survey/atlas paper: k-NN over 44 personality-model embeddings). | §1 (survey cite) |
| **SCPI** | Semantic Character Personality Index (k-NN over 562 character embeddings). | §3 (M6) + [`scpi_structural_probe_results.md`](scpi_structural_probe_results.md) |
| **SAPI** | Semantic Author Personality Index (author-level centroids; umbrella-only, available on request). | workshop |
| **SPPI** | Semantic Persona Personality Index (envisioned: LLM-generated persona pool diversity audit). | workshop |
| **SGPI** | Semantic Genre Personality Index (envisioned: genre / period clustering). | workshop |

## Probes + named outcomes

| Term | Expansion | First in |
|---|---|---|
| **V6** | Activation probe (project-internal name; "activation probe" in reader-facing prose). | §4.2 + §7 |
| **H_LTR** | Long-text-recovery hypothesis (refuted at 1-turn dialogue, reconciled at 5k-char utterance corpus). | §4.4 |
| **H_SPI_projection** | Hypothesis: BFI → HEXACO bridge via the survey's SPI. | §4.13 |

## Notebook + reproducer artifacts

| Term | Expansion | First in |
|---|---|---|
| **NB02** | `02_method_bakeoff_results.ipynb` (M2–M6 comparison + RQ1.1–1.7). | Exp 1 |
| **NB03** | `03_hexaco_atlas_reproducer.ipynb` (panel + PRIOR_DRIVEN substrate falsifier). | Exp 2 + Exp 3 |
| **NB04** | `04_synthetic_characters.ipynb` (synthetic substrate, RQ3.1). | Exp 3 |
| **NB05** | `05_cache_map.ipynb` (cache-membership gauge, RQ3.2). | Exp 3 |
| **NB06 / NB07** | `06_register_matched_synth.ipynb` / `07_ipip_human_anchor.ipynb` (Exp 3 controls). | Exp 3 |
| **NB08 / NB09** | `08_activation_probe_dissociation.ipynb` / `09_catcher_in_the_cache.ipynb` (mechanism). | further |
| **NB10** | `10_regressor_inference.ipynb` (label propagation, S1). | supporting |
| _umbrella only_ | `07_scpi_character_clusters.ipynb`, `09_sedimentation_tests.ipynb`, `13_judge_vs_subject_mode_dissociation.ipynb`, `14_human_hexaco_panel.ipynb` live in `Wildertrek/aperture`. |, |

## Follow-up program (F-flags)

| Flag | Scope | Trigger |
|---|---|---|
| **F1** | Closed-source frontier activation probe extension (70B+ scale, gated provider access). | future work |
| **F2** | Multi-snapshot-per-family mode-dissociation extension (resolves mode-dissociation n=1-per-family caveat). | Paired with F1 |
| **F3** | Human-rater HEXACO panel (Prolific n=30; converts bipolarity finding from LLM-rater consensus to human-anchored). | UTK IRB clearance (drafted) |
| **F4** | Substrate expansion to n=100+ synthetic chars with human-authored novel evidence packs. | MFA writing program collaboration |

## Symbol conventions

| Symbol | Meaning | Where |
|---|---|---|
| $\lambda$ | Ridge regularizer (sklearn `alpha` parameter; we use λ for paper-wide consistency) | §3 stacked-ridge ceiling; §4 + §7 |
| $\rho$ | Spearman rank correlation | [`further_analyses.md`](further_analyses.md) |
| $\eta^2$ | Effect size for ANOVA / variance explained | §1 Table 1; §4.2 |
| $\Delta_{\mathrm{depth}}$ | Activation-probe layer-depth dissociation magnitude (r at early layer minus r at late layer) | §7 activation probe |
| $W$ | Wilcoxon signed-rank test statistic | §1 Table 1 (the cross-rater panel RQ6.9) |
| $p_{\mathrm{BH}}$ | BH-FDR-corrected p-value | Throughout |

---

*This glossary is referenced in §3.9 Reproducibility for cold-reader
navigation. Updated 2026-05-21 as Tier 1 improvement closing the
reviewer / new-reader onboarding gap.*
