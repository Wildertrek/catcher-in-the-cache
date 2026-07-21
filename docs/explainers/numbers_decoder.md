# Numbers Decoder

> If you noticed that the corpus is 76 books and the comparison is 75,
> this explainer reconciles every recurring number in one place.

The numbers all check out. They differ because they count different
populations, the paper says so each time but doesn't put them in
one table. Here is that table.

---

## 1. Rater counts (the panel)

| Number | Population | Where it appears | Why this number |
|---|---|---|---|
| **25** | Cross-rater panel | RQ6.1, RQ6.2, RQ6.3, RQ6.7, §4.4 activation probe families; §4.3 RQ6.9, Table 1 | The full panel of frontier LLM raters; the same 25 distinct models in both canonical mode and the synthetic paired test |
| **9** | Provider ecosystems | abstract, §1, §3.3 | Distinct labs / API homes (Anthropic, OpenAI, Google, Meta, Mistral, xAI, DeepSeek, Cohere, Qwen, counted by ecosystem, not by checkpoint) |
| **12** | Open-weight activation-probe panel | §4.4 | Open-weight subset of the 25 (closed-weight raters cannot give us hidden activations) |
| **3** | Activation probe scaling families | §4.4 | Meta + Qwen + Mistral-MoE, the three families at 70B+ that converge on layer-depth dissociation |
| **6** | mode-dissociation subset | §4.X | Representative subset for subject-mode self-report (cheaper to elicit at $N=10$ per model) |
| **3** | M4 multi-provider consensus | §3.3 | Anthropic + OpenAI + Google: the three providers that vote in the M4 median (not the same as the 25-rater panel, which is the *substrate of the falsifier test*; M4 is a *method-comparison competitor*) |

### The panel, in one sentence

The panel is 25 distinct LLMs across 9 provider families (Grok 4.3 was
run once; the Amendment-9 additions Hermes-3 and Jamba were dropped),
and the same 25 raters carry both the canonical RQs and the synthetic
paired test. This is the pre-registration lock count.

---

## 2. Corpus counts (the books and characters)

| Number | Population | Where it appears | Why this number |
|---|---|---|---|
| **76** | Pipeline corpus | §2.1 | Full set of Project-Gutenberg works processed by the pipeline (BookNLP + coref + evidence packs) |
| **75** | Comparison subset | §2.1 | 76 minus *Julius Caesar*: BookNLP collapses Marcus Brutus and Decius Brutus into a single coref cluster, so no character in that play has clean joint-coverage across all five methods. Excluded on a coverage criterion, not a content criterion |
| **30** | Novels in pipeline | various | Novel slice of the 76 |
| **46** | Drama plays in pipeline | various | Drama slice of the 76 (Shakespeare's complete corpus plus Ibsen, Sophocles) |
| **562** | Comparison character set | §2.1, §4 | Characters in the 75 comparison books with joint M2/M3/M4/M5/M6 coverage *and* at least one ground-truth entry. Inclusion is by joint method coverage, not by mention-count threshold |
| **60** | Canonical-substrate test set | §4.3 RQ6.9, §3 Bar 3 | Frozen-canon subset paired against the 20 synthetic chars for the substrate falsifier (chosen for cross-source GT overlap and canonical recognizability) |
| **20** | Synthetic literary characters | §4.3 RQ6.9 | Authored synthetic characters matched in genre / period / role to canonical anchors, designed to be absent from any LLM training corpus (see [`why_synthetic_chars`] tier-2 explainer) |
| **185** | AGT-only sensitivity subset | §6.1, appendix `agt_only_sensitivity.md` | Characters with at least one peer-reviewed AGT source (the "purest" GT slice, used for the contamination sensitivity check) |
| **115 / 328 / 119** | Mention-quartile breakdown | §2.1 | Descriptive corpus balance: bottom-quartile (sparse) / mid-band / top-quartile (named protagonist), these are descriptive, not a selection criterion |

---

## 3. Ground-truth taxonomy

| Number | What it is | Why it matters |
|---|---|---|
| **5** | GT source types | AGT / SGT / PGT / MGT / CGT, five qualitatively distinct provenance tiers |
| **11** | Weighted (tier, subtype) entries | 3 AGT subtypes + 2 SGT + 2 PGT + 1 MGT + 3 CGT = 11; the authoritative implementation is `aperture_gt_taxonomy.TIER_TABLE` |
| **1.00** | AGT peer-tier-1 weight | High-impact peer-reviewed psych-criticism journals (highest-trust GT) |
| **0.85** | MGT weight | Authors-of-record direct OCEAN annotation |
| **0.80** | SGT authoritative weight | Curated sources like Zimbardo & Johnson on Shakespeare |
| **0.55** | PGT Open Psychometrics SWCPQ weight | External dataset, lower weight |
| **0.20–0.35** | CGT weights | LLM consensus fallback, deliberately downweighted to avoid method-self-evaluation circularity. Headline tables filter CGT *out* |

---

## 4. Probe / methodology counts

| Number | What it counts | Section |
|---|---|---|
| **5** | Methods in the comparison (M2 through M6) | §3 |
| **3** | Diagnostic Bars (Bar 1 / Bar 2 / Bar 3) | §3 |
| **5** | OCEAN factors | universal |
| **6** | HEXACO factors | universal |
| **7** | OCEAN-HP factors (OCEAN-5 + H + A_HEX), the cheap regressor output; only O/C/E trustworthy out-of-cache | §1 deployment tiering |
| **6** | OCEAN-6 factors (OCEAN-5 + H, drops A_HEX), a described OCEAN augmentation, not the recommendation (HEXACO is the recommended construct space) | §1 deployment tiering |
| **3072** | Embedding dimensionality | M3 uses `text-embedding-3-large` mean-pooled over character utterances |
| **44** | BFI items (OCEAN Inventory) | mode-dissociation bridge: §4.X / Amendment 11 |
| **50** | IPIP-50 items | mode-dissociation holdout |
| **5** | Layer-depth percentiles for activation probe | §4.4 |
| **256** | Mean-pool window (tokens) | §4.4 |
| **64** | MLP probe hidden width | §4.4 (with the caveat: $n=60$ substrate underpowered for MLP, so MLP is sensitivity check, Ridge is load-bearing) |
| **69** | (Model, layer) cells for the MLP probe robustness check | §4.4 |
| **10** | $N$ subject-mode elicitations per model (mode-dissociation) | §4.X mode dissociation |

---

## 5. Statistical counts

| Number | What it is | Section |
|---|---|---|
| **9** | Inferential tests in the BH-FDR family (RQ6.1 through RQ6.9) | §3, §4 |
| **0.05** | $\alpha$ for the BH-FDR family | §3 |
| **0.30** | Pre-registered $|r|$ floor for RQ6.1 universal-collapse claim | §3 |
| **0.15** | Pre-registered $|\Delta|$ threshold for RQ6.9 PRIOR_DRIVEN | §3 |
| **0.40** | Pre-registered $\Delta$ threshold for mode-dissociation Branch A falsification | §4.X |
| **10000** | Bootstrap resamples used throughout for CIs | §3.7 |
| **0.75** | Observed mean $|r|$ on canonical substrate (RQ2.1 / pre-reg RQ6.1; panel $0.752$) | Experiment 2 |
| **0.30** | Observed mean $|r|$ on synthetic substrate (paired, RQ3.1 / pre-reg RQ6.9; $0.304$) | Experiment 3 |
| **$-0.447$** | Paired delta (canonical $|r|$ minus synthetic $|r|$) | Experiment 3 |
| **$1.5 \times 10^{-7}$** | BH-corrected $p$ on the substrate-falsifier paired Wilcoxon (one-sided $p_{\mathrm{raw}} = 2.98 \times 10^{-8}$, rank 1 of the 5-test family). Earlier drafts printed $6.0 \times 10^{-8}$, which is the *two-sided unadjusted* $p$, not a BH-corrected one | Experiment 3 |
| **$+0.75$** | Signed mean $r(H, A_{\mathrm{HEX}})$ on canonical | Experiment 3 |
| **$+0.23$** | Signed mean $r$ on synthetic (20 of 25 positive); the retrieval discriminator vs designed $-0.74$ | Experiment 3 |

---

## 6. RQ numbering, what happened to 6.4, 6.5, 6.6, 6.8?

The paper presents the cross-rater panel RQs as **RQ6.1, RQ6.2, RQ6.3, RQ6.7, RQ6.9**.
The gaps are not buried results, they are pre-registered slots that
were either rolled into another RQ during analysis or retracted for
underpower:

| RQ | Status |
|---|---|
| 6.1 | Universal collapse, PASSED, in paper |
| 6.2 | Family clustering, PASSED, in paper |
| 6.3 | Capability null vs Arena rank, NULL (reported) |
| 6.4 | Rolled into 6.2 (within-family resolution) during analysis |
| 6.5 | Rolled into 6.7 (regime contrast subsumes alignment-stratification) |
| 6.6 | Retracted pre-data at adequate-power audit |
| 6.7 | Alignment regime, retracted *at adequate power*; reported as retracted, not as a positive finding |
| 6.8 | Rolled into 6.9 (the substrate-paired version is the load-bearing test; 6.8 was the canon-only baseline that now lives as 6.1) |
| 6.9 | PRIOR_DRIVEN substrate falsifier, load-bearing, PASSED, $3\times$ threshold |

Full the cross-rater panel chronology is in §3.X testing-rounds table. A
sanitized amendments log is on the F-list as a Tier 2 explainer
(`amendments_log.md`).

---

## 7. Quick-reconciliation lookup

If you are reading the paper and one of these numbers throws you,
this is the row to check:

| Number you saw | What it counted |
|---|---|
| 25 raters | Full cross-rater panel (canonical and synth-paired; same 25 distinct models) |
| 9 providers | Provider ecosystems, not checkpoints |
| 12 raters (activation probe) | Open-weight subset |
| 76 books | Pipeline corpus |
| 75 books | Comparison (Julius Caesar excluded for BookNLP coref failure) |
| 60 canon | Frozen-canon substrate-test subset |
| 20 synth | Synthetic-substrate substrate-test subset |
| 562 chars | Full comparison (joint M2–M6 coverage) |
| 185 chars | AGT-only sensitivity subset |
| 3 providers | M4 consensus (Anthropic + OpenAI + Google), *not* the 25 panel |
| 6 models | mode-dissociation subset |

When in doubt, the number you want is in §3 (the design table) or
the appendix [`glossary.md`](../appendix/glossary.md).
