# RQ2 / Bar 2 Corrected Campbell-Fiske MTMM, the paper Appendix

This appendix expands the corrected Campbell-Fiske MTMM tables condensed in §4 RQ2 of the paper. The body paragraph reports the headline finding (three pairs recover 5/5 OCEAN at corrected criterion + floor: M3↔M4, M3↔M5, M4↔M5) and the cleanest contamination-free pair (M3↔M5 monotrait min r=0.589 on Neuroticism). This file ships the full per-pair tables.

## Corrected Campbell-Fiske 3-inequality MTMM test per method pair

**n_conv_3ineq** = traits passing all three inequalities (max-aggregated heterotrait, both within-method floors).
**n_conv_floor** = additionally clearing the absolute monotrait r ≥ 0.30 floor.
**monotrait_min** = smallest monotrait-heteromethod r across the five OCEAN traits for the pair.

| Method A | Method B | 3-ineq pass | + floor pass | monotrait_min |
|---|---|---|---|---|
| M3 regressor | M4 consensus | 5/5 | 5/5 | 0.807 |
| M3 regressor | M5 probe | 5/5 | **5/5** | 0.589 |
| M4 consensus | M5 probe | 5/5 | 5/5 | 0.553 |
| M3 regressor | M6 SCPI | 3/5 | 3/5 | 0.260 |
| M4 consensus | M6 SCPI | 2/5 | 0/5 | 0.220 |
| M5 probe | M6 SCPI | 3/5 | 2/5 | 0.244 |
| M2 classifier | M3 regressor | 4/5 | 2/5 | 0.103 |
| M2 classifier | M4 consensus | 3/5 | 1/5 | 0.063 |
| M2 classifier | M5 probe | 4/5 | 2/5 | 0.126 |
| M2 classifier | M6 SCPI | 1/5 | 0/5 | -0.043 |

The triangle of contamination-free convergent pairs is M3↔M4 / M3↔M5 / M4↔M5. M2 classifier and M6 SCPI fall below the monotrait floor on most pairs.

## Cross-method aggregate Pearson r with bootstrap 95% CIs

10,000-resample paired-character bootstrap over the 5·n trait-character pairs. M3↔M4 / M3↔M5 / M4↔M5 triangle clears r ≥ 0.50 on the lower CI bound for two of three pairs.

| Method A | Method B | n | r [CI] | r_lo > 0.5 | r_lo > 0.7 |
|---|---|---|---|---|---|
| M3 regressor | M4 consensus | 2810 | **0.841** [0.827, 0.854]† | yes | **yes** |
| M3 regressor | M5 probe | 2580 | **0.664** [0.640, 0.687]† | yes | no |
| M4 consensus | M5 probe | 2580 | **0.689** [0.664, 0.714]† | yes | no |
| M3 regressor | M6 SCPI | 2810 | 0.333 [0.299, 0.367] | no | no |
| M4 consensus | M6 SCPI | 2810 | 0.255 [0.219, 0.290] | no | no |
| M5 probe | M6 SCPI | 2580 | 0.330 [0.294, 0.367] | no | no |
| M2 classifier | M3 regressor | 2810 | 0.264 [0.229, 0.299] | no | no |
| M2 classifier | M4 consensus | 2810 | 0.228 [0.191, 0.263] | no | no |
| M2 classifier | M5 probe | 2580 | 0.201 [0.165, 0.237] | no | no |
| M2 classifier | M6 SCPI | 2810 | 0.020 [-0.015, 0.055] | no | no |

† Disattenuated r (Spearman 1904 correction with reliability proxy 1 − mean|r_within|, Schmitt & Stults 1986): M3↔M4 saturates at 1.0 (consistent with the contamination-circular caveat); M3↔M5 0.80; M4↔M5 0.84.

## Reading

The three contamination-free pairs each recover the full OCEAN-5 vector at the corrected three-inequality test with monotrait floor. The aggregate r (cross-method) clears the conventional 0.50 lower-CI bound for all three pairs, and clears 0.70 lower-CI bound on the contamination-circular M3↔M4 pair (expected; M3 was trained on M4 labels). The contamination-clean pairs (M3↔M5 and M4↔M5) provide the load-bearing convergent-validity evidence.

## Reproducer

These tables are computed in `notebooks/02_method_bakeoff_results.ipynb` (cells loading `paper_artifacts/method_bakeoff_v4/mtmm_matrix.csv`, `mtmm_convergent_discriminant.csv`, `agreement_with_ci.csv`, and `disattenuated_method_r.json`).

---

_Provenance: condensed from §4.X "RQ2 / Bar 2 Convergent validity" subsection in the paper. Source: method_bakeoff_v4/mtmm_*.csv files. Reproducer: NB02 RQ2 cells._
