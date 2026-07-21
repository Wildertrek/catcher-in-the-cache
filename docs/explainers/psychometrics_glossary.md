# Psychometrics Glossary for CS Readers

> If you read modern ML papers but haven't touched stats since the
> first-year sequence, this is the cheat sheet. Each term is one
> short paragraph: what it is, the intuition, and where it appears
> in the paper.

---

## Correlation flavors

### Pearson $r$
The standard linear-correlation coefficient. $r = +1$ is perfect
positive linear association, $r = 0$ is no linear association,
$r = -1$ is perfect negative. **Throughout the paper** $r$ is reported
between traits (within a rater, across characters) or between method
outputs (across characters). The substrate falsifier's load-bearing
quantity is **mean $|r|$ within rater across the 60 canonical
characters between H and A**: 0.75 on canon, 0.30 on synth (signed +0.23, not the designed -0.74).

### Spearman $\rho$
Pearson on the ranks. Robust to outliers and to monotonic-but-not-linear
relationships. **Used for RQ6.3** (capability null: $\rho$ between
rater Arena rank and bipolarity strength).

### Lin's Concordance Correlation Coefficient (CCC)
A correlation that penalizes both **location bias** (different means)
and **scale bias** (different ranges). $\mathrm{CCC} = +1$ requires
points exactly on $y = x$. **Used at Bar 1** as a stricter alternative
to Pearson $r$ for GT recovery: a method can have $r = 0.9$ with
predictions that are 0.3 lower than GT on average, but its CCC will
penalize that bias.

### Intraclass Correlation Coefficient (ICC)
Correlation that measures **within-cluster agreement** vs
across-cluster variance. $\mathrm{ICC} = 0$ → no clustering (members
of the same group are no more similar than random pairs).
$\mathrm{ICC} = 1$ → every group is internally homogeneous and
distinct from every other group. **Used in RQ6.2**: do raters from
the same provider family cluster on their canonical-substrate
bipolarity strength? Yes, ICC permutation $p_{\mathrm{BH}} = 0.008$.

---

## Test flavors

### Paired Wilcoxon signed-rank test
Non-parametric paired test. Given pairs $(x_i, y_i)$, computes whether
the median of $x_i - y_i$ differs from zero. Robust to non-normal
distributions. **The load-bearing test for RQ6.9**: each rater
contributes one pair (its canonical $|r|$, its synthetic $|r|$); 25
pairs total. $W = 0$ means every rater's canon $|r|$ was strictly
higher than its synth $|r|$ (or vice versa, but here, canon > synth
in every case).

### McNemar test
Paired binary test. Used when each subject is classified
yes/no under two conditions, e.g., for classification ablations.

### Likelihood Ratio Test (LRT)
Tests whether a more complex model fits significantly better than a
simpler nested one. **Used in RQ6.7**: does adding alignment-regime
to a family-coded random-effects model add information beyond family?
Answer: $\chi^2 = 0.081$, $p = 0.78$ → no.

### Permutation test
Non-parametric significance test: shuffle the labels many times,
compute the test statistic under each shuffle, see where the observed
statistic falls in that empirical null distribution. **Used for the
ICC test in RQ6.2** (where the analytic null distribution of ICC is
not clean).

### Bootstrap CI (confidence interval)
Resample with replacement many times, compute the statistic each
time, take the 2.5% and 97.5% percentiles for a 95% CI. **Used
throughout the paper** (10,000 resamples) for CIs on MAE, $r$,
$\Delta$, etc.

---

## Multiple-comparisons correction

### Benjamini-Hochberg false-discovery-rate control (BH-FDR)
When testing many hypotheses, the per-test $\alpha = 0.05$ would
produce many false positives. BH-FDR controls the **expected
proportion of false discoveries** among rejected nulls. **The Pivot
6 inferential family** (RQ6.1, 6.2, 6.3, 6.7, 6.9 + ancillary) is
corrected as a single BH-FDR family at $\alpha = 0.05$. Reported
$p$-values are the BH-corrected $p_{\mathrm{BH}}$.

### Bonferroni correction
Stricter alternative to BH: multiply each $p$ by the family size.
Used as a sensitivity check throughout, when BH-significant tests
also survive Bonferroni, the paper says so.

---

## Effect sizes

### Cohen's $d$
Standardized mean difference: (mean group 1 - mean group 2) / pooled SD.
Used in earlier drafts; mostly replaced by
$\Delta$ in original $r$-units for interpretability.

### $\eta^2$ (eta-squared)
Proportion of variance explained by a grouping factor. **Used for
the ICC permutation effect size in RQ6.2**: $\eta^2 = 0.70$ means
70% of between-rater variance on bipolarity strength is explained
by provider family.

### $\Delta R^2$
Improvement in $R^2$ when adding predictors to a regression. **Used
in RQ6.7**: $\Delta R^2 = +0.000$ from adding alignment regime to a
family-coded model.

---

## Psychometric structure

### Factor structure
The set of latent dimensions a measurement instrument is built to
recover. OCEAN has a 5-factor structure; HEXACO has 6. Factor
structure is normally validated via factor analysis on item-level
responses, but in this paper we treat each LLM rater's output
*as if it were an instrument* and ask whether its emergent factor
structure matches.

### Bipolarity (in this paper)
Two factors that should mostly be independent (low $|r|$) but
end up anti-correlated (high negative $r$). The H ↔ A fusion
on canonical characters is the bipolarity finding: these factors are
not supposed to be a single axis with a sign flip, but every LLM
in the panel treats them that way on canonical chars. On synthetic
chars the bipolarity drops, the diagnostic gap.

### Multitrait-multimethod (MTMM) matrix
A $T \times T$ matrix where $T$ traits are measured by $M$ methods;
the $5 \times 5$ block in the paper has all OCEAN pairs across all
method pairs. **The corrected Campbell-Fiske three-inequality test**
(Bar 2) requires: (i) monotrait $r$ across methods should exceed (ii)
heterotrait-monomethod and (iii) heterotrait-heteromethod $r$.

### Convergent vs discriminant validity
- **Convergent:** Different methods measuring the same trait should
  agree. ($r$ between M3-O and M4-O should be high.)
- **Discriminant:** Different traits should not agree even when
  measured by the same method. ($r$ between M4-O and M4-C should be
  low.)

Bipolarity violates discriminant validity. Bar 2's three inequalities
are convergent-vs-discriminant inequalities.

### Cronbach's $\alpha$
Reliability coefficient: how internally consistent are the items of
an instrument? Out of scope for the paper (we don't run item-level
analyses on the LLM outputs) but referenced for the BFI / IPIP
instruments.

---

## Activation-probe terminology (§4.4)

### Layer-depth probe
For an open-weight LLM with $L$ layers, extract hidden-state
activations at $L'$ depth percentiles (e.g., $L' = 5$ at 12.5% /
25% / 50% / 75% / 87.5% of depth). Each gives a residual-stream
representation per token.

### Mean-pool-256
Average the activations across 256 tokens of input (typically the
character's evidence pack). Produces one fixed-dimensional vector
per (model, layer, character). The pool variant matters: alternatives
include max-pool, last-token, attention-pool.

### Pool-ablation
Comparison across pool variants. **§4.4 finding**: Llama-70B shows the
depth gradient only on mean-pool; Mixtral-8×22B shows the gradient
on all pool variants. Interpreted as architecture-conditional (dense
vs sparse-MoE).

### Ridge probe / MLP probe
Two linear-ish probes trained on (activation → GT trait):
- **Ridge** = L2-regularized linear regression. **Load-bearing in §4.4.**
- **MLP** = 1 × 64 hidden-layer feedforward. **Sensitivity check
  only.** With $n = 60$ canonical characters as the training substrate,
  the MLP is **underpowered** (non-linear-probe refit degraded $75/79$ negative
  $R^2_H$), so the Ridge probe carries the inferential load and the
  MLP probe is reported as a directional consistency check.

### Latent $r$
Pearson $r$ between probe output (from activations) and GT trait,
across the test characters. The §4.4 finding: $r$ rises with depth
in three families (Meta, Qwen, Mistral-MoE) at 70B+ scale.

---

## Diagnostic-protocol vocabulary

### Pre-registration (pre-reg)
The practice of publicly committing to hypotheses, thresholds, and
analysis decisions **before** running the test. The paper's the cross-rater panel
RQs are pre-registered with locked thresholds (e.g., RQ6.9's
$|\Delta| \geq 0.15$ threshold was committed before the synthetic-substrate
LLM calls).

### Branch A / Branch B (mode-dissociation)
A pre-registered **disjunctive** hypothesis structure: Branch A is
the primary prediction; Branch B is a fallback path that is
*also* pre-registered (so it isn't post-hoc rationalization). The
mode-dissociation result: Branch A *falsified* at locked
thresholds (missed by 0.107 and 0.015), Branch B retained, and this
is not p-hacking because Branch B was pre-registered.

### Falsifier / falsification threshold
A pre-registered observation that, if observed, would refute the
hypothesis. RQ6.9's load-bearing claim is structured as a falsifier:
*"If the substrate gap is below 0.15 in either direction, we retract
the canonical-prior story."* The observation (-0.447) is $3\times$
the threshold; the falsifier *didn't fire*.

### LOBO (leave-one-book-out)
A held-out generalization scheme: train on all characters except
those from one book, test on that book's characters. **Used by M3
and M6** to prevent within-book leakage (e.g., training on Mr. Darcy
and testing on Elizabeth Bennet from the same novel).

### LOAO (leave-one-author-out)
Stricter: train on all characters except by one author, test on that
author. Used for cross-author transfer.

---

## A quick map of what each test answers

| Test in paper | Question | RQ |
|---|---|---|
| Mean $|r|$ floor on canon | Does every rater fusion H and A? | RQ6.1 |
| ICC permutation by family | Do same-family raters cluster on bipolarity? | RQ6.2 |
| Spearman $\rho$ vs Arena | Is bipolarity strength a function of model capability? | RQ6.3 (NULL) |
| LRT regime vs family | Does alignment regime add info beyond family? | RQ6.7 (retracted at power) |
| Paired Wilcoxon | Does bipolarity drop on synthetic substrate? | RQ6.9 |
| Ridge probe per layer | Does trait-relevant signal scale with depth in the activations? | §4.4 activation |
| Subject-mode vs judge-mode delta | Does the bipolarity exist in the model's *own* self-report? | mode-dissociation §4.X |

---

## Further reading

- The formal acronym + term card (with paper section refs):
  [`../appendix/glossary.md`](../appendix/glossary.md)
- The Campbell-Fiske MTMM appendix:
  [`../appendix/rq2_mtmm_full_tables.md`](../appendix/rq2_mtmm_full_tables.md)
- The HEXACO cross-provider triangulation appendix:
  [`../appendix/rq7_hexaco_cross_provider.md`](../appendix/rq7_hexaco_cross_provider.md)
