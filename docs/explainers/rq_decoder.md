# RQ Decoder, the cross-rater panel Inferential Family + Amendments Log

> If the gaps in the RQ numbering (6.1, 6.2, 6.3, 6.7, 6.9, what about
> 6.4, 6.5, 6.6, 6.8?) made you suspect buried results, this explainer
> shows what every slot in the cross-rater panel family was, what each one
> resolved to, and what the eleven amendments changed.
>
> Short version: **healthy pre-registration produces non-consecutive numbering**.
> The gaps are slots that were rolled into other RQs during analysis or
> retracted *at adequate power*. Reporting them as gaps is the
> alternative to silently deleting them, which would be the corner-cut
> we are trying to avoid.

---

## The cross-rater panel RQ family

| RQ | Status in paper | Disposition |
|---|---|---|
| **RQ6.1** | Reported, PASSED | Universal collapse on canon: all 25 raters above pre-reg $|r| \geq 0.30$ floor; mean $|r| = 0.75$ |
| **RQ6.2** | Reported, PASSED | Family clustering: ICC permutation $p_{\mathrm{BH}} = 0.008$, $\eta^2 = 0.70$ |
| **RQ6.3** | Reported, NULL | Capability null vs Arena rank: Spearman $\rho = -0.165$, $95\%$ CI $[-0.54, +0.27]$ |
| **RQ6.4** | **Rolled into RQ6.2** | Within-family resolution; the family-clustering RQ already covered it |
| **RQ6.5** | **Rolled into RQ6.7** | Alignment-stratification; the regime-contrast RQ subsumed it |
| **RQ6.6** | **Retracted pre-data** | At adequate-power audit, this slot was underpowered for the test it asked. Retracted before data collection rather than reported as a noise null |
| **RQ6.7** | Reported as retracted | Alignment regime: LRT $\chi^2 = 0.081$, $p = 0.78$. Retracted *at adequate power* (the test had power; the effect just wasn't there); reported transparently rather than silently dropped |
| **RQ6.8** | **Rolled into RQ6.1** | The canon-only baseline that became the universal-collapse RQ |
| **RQ6.9** | Reported, PASSED, **load-bearing** | PRIOR_DRIVEN substrate falsifier: $\Delta = -0.447$, $3\times$ pre-reg threshold; $p_{\mathrm{BH}} = 1.5 \times 10^{-7}$ |
| **RQ6.10** | **Deferred, not reported** | Base-vs-instruct contrast. OpenRouter exposes no base (non-instruction-tuned) variants of the target models, so this needs local GPU weight-loading (Amendment 3 scope). Deferred to the activation-probe follow-up; it is not in the BH-FDR family and no result is claimed from it. See `paper_artifacts/pivot6_hexaco_atlas/results.md` |

The **BH-FDR family is not the same list**. Its composition is fixed by the
pre-registration artifact `bh_fdr_pivot6_results.json` (`family_size = 5`):

| rank | test | p_raw | p_BH |
|---|---|---|---|
| 1 | RQ6.9 substrate falsifier (paired Wilcoxon, one-sided) | 2.98e-8 | 1.49e-7 |
| 2 | H2 family clustering (ICC permutation) | 0.0032 | **0.0080** |
| 3 | H4 open vs closed | 0.1619 | 0.270 |
| 4 | H3 capability correlation | 0.4749 | 0.594 |
| 5 | H5 head-to-head proxy | 1.0 | 1.0 |

Two members are *not* in the RQ6.x numbering (H4, H5), and two RQ6.x questions are
*not* in the family: **RQ6.7 is excluded** because it was retracted, and **RQ6.1 uses a
Wilson confidence interval rather than a p-value** and is reported separately. Values
above are recomputed on the standardized 25-rater panel by
[`paper_artifacts/pivot6_hexaco_atlas/panel25/compute_panel25.py`](../../paper_artifacts/pivot6_hexaco_atlas/panel25/).

---

## Reader-facing crosswalk

The paper renumbers the surviving RQs into an experiment-grouped, reader-facing
scheme; the pre-registered identifiers below are the authoritative record. This is
the crosswalk the paper's RQ-coverage table cites.

| Reader-facing | Pre-registered | Question |
|---|---|---|
| **RQ1.1** | RQ1 | best method (leaderboard) |
| **RQ1.2** | RQ2 | methods converge (MTMM) |
| **RQ1.3** | RQ3 | external validity |
| **RQ1.4** | RQ6 | per-trait verdict |
| **RQ1.5** | RQ7 | Agreeableness recoverable |
| **RQ1.6** | RQ8 | per-trait specialization |
| **RQ1.7** | RQ11 | construct space head-to-head |
| **RQ2.1** | RQ6.1 | fusion universal across raters |
| **RQ2.2** | RQ6.2 | family clustering |
| **RQ2.3** | RQ6.7 | alignment regime (retracted) |
| **RQ3.1** | RQ6.9 | collapse off-cache (substrate falsifier) |
| **RQ3.2** | new | cache-membership gauge |
| **S1** | RQ4 | cost-accuracy frontier (companion) |
| **S2** | RQ9 | single-LLM-probe regime (companion) |
| **S3** | RQ10 | archetype stability (companion) |
| **S4** | Amendment 11 | subject-mode dissociation: judge $0.79 \to$ subject $0.41$ (companion \S A.13). Pre-registered as an amendment rather than a numbered RQ, so it has no RQ$n$ identifier |

**Construct-space label crosswalk (RQ1.7 / paper Table 4).** The paper labels the three construct vectors HEXACO / OCEAN-H1 / OCEAN-H2; the companion artifacts (`paper_artifacts/hexaco6_head_to_head/`) label the same three HEXACO / OCEAN-6 / OCEAN-HP. So **OCEAN-H1 = OCEAN-6** (OCEAN + H, without HEXACO-A) and **OCEAN-H2 = OCEAN-HP** (OCEAN + H + HEXACO-A). The monotrait pass counts agree either way: 18/18, 15/18, 14/21.

Retired / merged (no reader-facing code, logged here only): RQ5, RQ6.3 (capability
null, reported as supporting), RQ6.4 -> RQ2.2, RQ6.5 -> RQ2.3, RQ6.6 (retracted
pre-data), RQ6.8 -> RQ2.1.

---

## Why non-consecutive numbering is good science

The instinct on reading "RQ6.1, RQ6.2, RQ6.3, RQ6.7, RQ6.9" (and a deferred RQ6.10) is
suspicion: *"what happened to the others, were they buried?"*

The honest answer is: pre-registration produces gaps when (i) you
register more RQs than survive an adequate-power audit, (ii) some
sub-RQs roll into a larger RQ once the analysis path is locked, and
(iii) some pre-reg slots are retracted (with explicit reporting).

The alternative is to silently re-number after analysis. Most
unregistered work does that, and it conceals an obvious form of
selection bias.

So the gaps are evidence of pre-registration honesty, not of buried
findings. Every gap is documented above.

---

## The amendments log (A1 through A11)

The paper's testing-round chronology
references "Amendment 1 through 11." Each is a pre-registered scope
change committed before its associated LLM calls. Summary:

| Amendment | What it scoped | Why |
|---|---|---|
| **A1** | Panel composition lock for the cross-rater panel (target $n=26$; realized $n=25$) | Pre-data panel freeze; xAI deprecation later collapsed xai_1 + xai_2 → grok-4.3, so the realized panel is the 25 raters used throughout this companion |
| **A2** | Name-swap ablation protocol | Pre-data lock on the H2 falsifier |
| **A3** | Generative-consistency check | Pre-data lock on within-rater stability check |
| **A4** | Diachronic probe ($6$ raters, $3$ families) | Pre-data lock on family-asymmetric replication |
| **A5** | De novo EFA ($N \in [132, 2004]$) | Pre-data lock on loading-level collapse |
| **A6** | Bar 1 BH-FDR family scoping | Pre-data: $50$ tests in Bar 1 family |
| **A7** | Bar 2 MTMM monotrait floor | Pre-data: $|r| \geq 0.30$ for cell inclusion |
| **A8** | Bar 3 OP-overlap scoping | $n = 60$ Open-Psychometrics-overlap subset locked |
| **A9** | Panel expansion: add Hermes-3 + Jamba-Large-1.7 (later dropped) | post-panel: these two were never re-run on the synthetic substrate, so they were dropped from the panel. The final panel is the pre-registration-lock set of 25 distinct LLMs across 9 families, see [`numbers_decoder.md`](numbers_decoder.md) |
| **A10** | Activation probe scoping | Pre-data: $5$ depth percentiles, mean-pool-256, Ridge load-bearing, MLP sensitivity |
| **A11** | Within-model subject-mode check ($6$ models, $N=10$ elicitations each) | Pre-data lock on the judge-vs-subject dissociation; locked Branch-A criteria (subject median $|r| < 0.30$ **or** $\Delta \geq 0.40$). Reported as **S4**; artifact `pivot6_hexaco_atlas/v8_d4b_within_model_subject.json` |

The full chronology with notebook reproducer links is in §3.X of the
paper (Table "Testing-round chronology") and is summarized in the §3
prose.

---

## Quick cross-references

| Topic | Where |
|---|---|
| The 25-rater panel (A9 additions dropped) | [`numbers_decoder.md`](numbers_decoder.md) §1 |
| What "adequate power" means here | [`psychometrics_glossary.md`](psychometrics_glossary.md) (RQ6.7 retraction) |
| Activation probe (RQ-adjacent, not in the BH-FDR family) | [`activation_probe_for_psychologists.md`](activation_probe_for_psychologists.md) |
