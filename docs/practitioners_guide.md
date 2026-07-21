# Practitioner's Guide

**Last updated:** 2026-05-13
**Companion paper:** *The Catcher in the Cache: Retrieval, Not
Measurement, in LLM Personality Inference*
**Companion notebook:** `notebooks/02_method_bakeoff_results.ipynb`

This guide answers one question: **which measurement instrument should I
use for my downstream task?** It is the deployment-time companion to
the paper. All numbers below are reproducible from cached artifacts in
`paper_artifacts/method_bakeoff_v4/` via notebook 02.

---

## The recommendation, in one paragraph

**Use HEXACO as the construct space for LLM persona work.** OCEAN's
Agreeableness conflates the moral axis (Honesty-Humility) with warmth
(Communion), and no OCEAN variant, including the OCEAN-HP vector this
guide catalogs, resolves that conflation. Deployment is a
label-availability tiering: (1) if an LLM is available at run time,
probe in HEXACO directly (the recommended path); (2) if you need a
cheap LLM-free regressor at scale, the OCEAN **O/C/E cheap regressor** is
the safe floor today, because O, C, and E lie *off* the fused moral
axis and transfer to out-of-cache (synthetic/novel) characters. The
cheap regressor also emits A, N, H, and A_HEX, but A/N are weak out-of-cache
and the cheap regressor H/A_HEX are research-replication-only there (the H
and A_HEX heads are trained on single-provider Claude Sonnet 4.5 labels
and carry the canonical H↔A_HEX fusion). A future cache-free HEXACO
regressor would unify both tiers.

> **Note on labels, to avoid a common error.** The OCEAN cheap regressor is
> trained on **M4 multi-provider LLM-consensus** labels. O/C/E transfer
> out-of-cache because those factors lie off the fused moral axis , 
> **not** because the training labels are human-derived or
> LLM-independent. There are no cache-free OCEAN labels available today.

---

## Quick-pick decision table

| Use case | Recommended instrument | Why |
|---|---|---|
| Persona-init when an LLM is available at run time (recommended) | **Run-time HEXACO probe** | Targets the recommended construct space; H separates the moral axis from warmth |
| Project-Gutenberg-scale character profiling (10⁴–10⁶ chars), LLM-free | **OCEAN O/C/E cheap regressor (the floor)** | Only option at this scale; ~$0.001/char, ~0.5 s/char; O/C/E transfer out-of-cache |
| Real-time persona conditioning at scale, LLM-free | **OCEAN O/C/E cheap regressor (the floor)** | Sub-second inference enables real-time conditioning; trust O/C/E, not the cheap regressor H/A_HEX, out-of-cache |
| Single-character precision measurement (e.g., literary criticism) | **M4 multi-provider consensus** | Best raw accuracy: MAE 0.230, r 0.770 vs weighted GT |
| You only need OCEAN-5 and bipolarity is not a concern | **OCEAN-5 cheap regressor alone** | Avoids H/P factor-purity caveat without losing OCEAN signal |
| Moral-axis signal (sincere vs manipulative) | **Run-time HEXACO probe** | H is load-bearing; the cheap regressor H is research-only out-of-cache, so use an LLM probe when an LLM is available |
| Pre-OCEAN narrative-role labeling (protagonist / hero / etc.) | **OCEAN-5 cheap regressor alone** | Fair-DV test: OCEAN-only wins 3 of 4 DVs (HP adds complexity without gain on these reference labels) |
| Human-aligned construct validation | **Not yet available** | Defer until the n=30 HEXACO observer-form panel is run (drafted, launch-ready) |
| Drama / Shakespeare-heavy corpora | **OCEAN O/C/E cheap regressor** with awareness of LOAO gap | A prior distillation study's LOAO: Shakespeare +0.020 MAE, within tolerance |

---

## Instrument catalog with measured deployment profiles

All measurements on the 562-character / 75-work comparison corpus. CIs
are 10,000-resample paired-character bootstrap.

### M4: Multi-provider LLM consensus

- **Inputs:** Character utterances (text).
- **Outputs:** OCEAN-5 only.
- **Architecture:** Median across Anthropic Claude Sonnet 4.6, OpenAI
  GPT-5.2, Google Gemini 2.5 Pro probing each character on OCEAN.
- **Headline accuracy (vs weighted multi-source GT, n=562):**
  - MAE 0.230 [0.224, 0.237]
  - Pearson r 0.770 [0.754, 0.786]
  - CCC 0.764 [0.748, 0.780]
- **Latency:** ~30 s/char (three provider API calls).
- **Cost:** ~$0.05/char.
- **When to use:** Best raw accuracy. One-off precision measurement,
  benchmark establishment, training-time teacher signal for distillation.
- **When NOT to use:** Anything at scale ($25,000 for Project Gutenberg
  500k chars vs $50 for cheap regressor).
- **Reproducibility:** `paper_artifacts/method_bakeoff_v4/predictions.json`
  (`M4_consensus` per char).

### M3: Random-forest regressor

- **Inputs:** Cached `text-embedding-3-large` embeddings + cached M4
  features (strong head) OR embeddings only (cheap regressor Ridge variant).
- **Outputs:** OCEAN-5 only.
- **Headline accuracy (in-distribution, n=562):**
  - MAE 0.262 [0.255, 0.270]
  - Pearson r 0.649 [0.627, 0.671]
- **Headline accuracy (LOBO, n=562):**
  - MAE 0.312 [0.304, 0.319]
  - Pearson r 0.356 [0.327, 0.385]
- **Latency:** ~1 ms/char inference + ~0.5 s/char embedding API.
- **Cost:** ~$0.001/char.
- **When to use:** OCEAN-5 at scale where the M3 RF specifically is
  preferred over Ridge (it isn't usually, a prior distillation study
  showed Ridge beats RF by 4.5%).
- **Reproducibility:** `paper_artifacts/method_bakeoff_v4/predictions.json`
  (`M3_regressor`).

### M5: Held-out single-provider LLM probe

- **Inputs:** Character utterances.
- **Outputs:** OCEAN-5 only.
- **Architecture:** Single rater family (Claude) probed with
  rater-blind evidence packs.
- **Headline accuracy (vs weighted GT, n=516):**
  - MAE 0.270 [0.261, 0.278]
  - Pearson r 0.633 [0.607, 0.659]
- **Latency:** ~10 s/char.
- **Cost:** ~$0.005/char.
- **When to use:** Middle-ground option when M4 is too expensive but
  you still want LLM-quality measurement.

### M6: SCPI (Semantic Character Personality Index, k-NN)

- **Inputs:** `text-embedding-3-large` of character mean utterances.
- **Outputs:** OCEAN-5 inheritance from nearest training neighbors.
- **Headline accuracy (LOBO, n=562):**
  - MAE 0.328 [0.320, 0.337]
  - Pearson r 0.308 [0.275, 0.341]
- **Architectural finding:** Embedding nearest-neighbors organize by
  author and historical period, not by personality content (the paper
  §3 SCPI architectural-failure finding). Wickham's nearest neighbors
  are warm Austen heroes regardless of trait similarity. **Do not
  deploy SCPI alone for personality measurement; use it as a
  provenance / case-study diagnostic only.**
- **Reproducibility:** `paper_artifacts/method_bakeoff_v4/scpi_diagnostic.csv`.

### M2: Classifier (RF/SVC/LR/kNN ensemble)

- **Inputs:** Character utterances → embeddings → discretized OCEAN buckets.
- **Outputs:** OCEAN-5 categorical predictions, output to [-1, +1].
- **Headline accuracy (n=562):**
  - MAE 0.367 [0.358, 0.375]
  - Pearson r 0.118 [0.081, 0.153]
- **Status:** Below the MAE 0.30 deployment threshold. **Reported here
  only because it documents a methodology the relaxed Campbell-Fiske
  MTMM test would falsely pass; the corrected test with the
  monotrait $r \geq 0.30$ floor catches its degeneracy.**
- **When to use:** Don't. It's archived for reference.

### **OCEAN cheap regressor, the LLM-free deployment floor (trust O/C/E out-of-cache)**

> This regressor emits seven factors, but the recommendation is to use
> only its **O/C/E** outputs out-of-cache. The construct-space
> recommendation is HEXACO (run-time probe when an LLM is available);
> this cheap regressor is the LLM-free floor at scale. A/N are weak
> out-of-cache and the cheap regressor H/A_HEX are research-replication-only
> there (single-provider Claude Sonnet 4.5 training labels carry the
> canonical H↔A_HEX fusion).

- **Inputs:** Character mean utterances → `text-embedding-3-large` (3072-d).
- **Outputs:** 7-vector = `[O, C, E, A, N, H, P]` (trust O/C/E out-of-cache; A/N weak; H/A_HEX research-only).
- **Architecture:**
  - OCEAN-5 head: Ridge α=1.0, trained on M4 multi-provider consensus
    labels for 562 chars across 75 works.
  - H head: Ridge α=0.1 (5-fold CV-selected), trained on Claude Sonnet 4.5
    HEXACO probe labels for the same 562 chars.
  - P head: Ridge α=0.1, same training set.
- **Headline per-factor LOBO performance (n=562):**

| Factor | LOBO MAE [CI] | LOBO Pearson r [CI] |
|---|---|---|
| O | 0.297 [0.281, 0.312] | 0.426 [0.358, 0.492] |
| C | 0.315 [0.298, 0.333] | 0.416 [0.346, 0.483] |
| E | 0.257 [0.242, 0.272] | 0.474 [0.409, 0.534] |
| A | 0.351 [0.332, 0.370] | 0.447 [0.379, 0.508] |
| N | 0.264 [0.248, 0.281] | 0.411 [0.341, 0.480] |
| H (Honesty-Humility) | 0.352 [0.331, 0.373] | 0.518 [0.454, 0.578] |
| A_HEX (HEXACO Agreeableness) | 0.311 [0.293, 0.329] | 0.629 [0.575, 0.679] |

- **Latency:** ~0.5 s/char (single embedding API call) + ~1 ms/char Ridge predict.
- **Cost:** ~$0.001/char.
- **Speedup vs M4:** ~60× faster, ~61× cheaper.
- **Known limit:** Factor-purity gap inherits from teacher. Teacher
  H↔P correlation is r=0.68 on 562 chars; cheap regressor LOBO predictions
  reproduce r=0.76 (vs human-rater norm r ∈ [0.20, 0.30]). H and P are
  not orthogonal in this regressor; closing the gap requires
  human-rater HEXACO training labels.
- **Reproducibility:** `paper_artifacts/method_bakeoff_v4/ocean_hp_cheap_head_v3.json`;
  model artifacts ship in `personality_models/hexaco_ridge_heads_v3_full562.pkl`
  (H + A_HEX heads) and `personality_models/ocean_ridge_regressor_v2_cheap.pkl`
  (OCEAN-5 head). See `personality_models/MODEL_CARD.md` for data
  provenance, license, and known limits.

---

## Minimal deployment code

```python
import joblib, numpy as np
from openai import OpenAI

# Load the trained heads (one-time)
ocean_head = joblib.load("personality_models/ocean_ridge_regressor_v2_cheap.pkl")["model"]
hp_head = joblib.load("personality_models/hexaco_ridge_heads_v3_full562.pkl")

client = OpenAI()

def measure_ocean_hp(character_utterances: str) -> dict:
    """Return a 7-vector {O,C,E,A,N,H,A_HEX} from raw character utterance text.

    The output key 'A_HEX' is the HEXACO Agreeableness factor (see the paper
    §sec:naming-proposal for the proposed 'P' single-letter shorthand that
    motivates the OCEAN-HP model name).
    """
    emb = client.embeddings.create(
        model="text-embedding-3-large",
        input=character_utterances,
    ).data[0].embedding
    x = np.asarray(emb, dtype=np.float32).reshape(1, -1)  # (1, 3072)
    ocean5 = ocean_head.predict(x)[0]  # length 5
    h = hp_head["model_H"].predict(x)[0]
    a_hex = hp_head["model_P"].predict(x)[0]  # pickle key is "model_P"; output is A_HEX
    return {
        "O": float(ocean5[0]), "C": float(ocean5[1]), "E": float(ocean5[2]),
        "A": float(ocean5[3]), "N": float(ocean5[4]),
        "H": float(h), "A_HEX": float(a_hex),
    }
```

All outputs are on the OCEAN convention [-1, +1] scale, M4-anchored.

---

## Sanity checks before deployment

1. **Quote-input minimum.** The training-time teacher consumed ~30
   quotes per character. Below ~5 quotes the embedding becomes
   unreliable. Flag low-quote chars as such; do not silently emit a
   point estimate.
2. **Period/author leakage.** SCPI showed that character embeddings
   cluster by author and period (the paper §3). If your deployment
   corpus is dominated by one author / era, expect within-cluster
   homogeneity and consider author-stratified evaluation before
   trusting downstream comparisons across authors.
3. **Bipolarity-zone characters.** When a character has high OCEAN-A
   AND low H, the OCEAN-A reading alone is misleading. Always emit
   the H output alongside OCEAN-A for downstream conditioning that
   may be safety-relevant (e.g., honesty/manipulation distinctions).
4. **Confidence intervals.** The point estimates above have non-trivial
   CIs. For decision-making at thresholds (e.g., "is this character
   above 0.5 on H?"), use the LOBO MAE as an uncertainty floor, not
   the point estimate.

---

## Open validation gaps (what this guide does **not** promise)

1. **Human-rater HEXACO alignment**: the H and P heads are trained on
   Claude Sonnet 4.5 probe labels. Human alignment is the planned
   follow-up (n=30 observer-form panel, drafted in `docs/human_hexaco_panel/`).
2. **External downstream-task incremental validity**: no
   pre-registered task currently shows OCEAN-HP beating OCEAN-5 with
   a fair downstream comparison.
3. **Real-person measurement**: all training labels are on literary
   characters. Real-person trait measurement requires a separate
   validation track; do not deploy this regressor on real-person text
   without re-validation.
4. **Cross-language generalization**: training corpus is English; no
   cross-language validation has been run.

---

## Reproducing the numbers in this guide

```bash
# OCEAN-HP cheap regressor LOBO metrics (Table above)
python scripts/method_bakeoff_v4/train_hexaco_heads_v3.py
# OCEAN-5 cheap regressor LOBO metrics
python scripts/method_bakeoff_v4/ocean_hp_cheap_head.py
# All RQ headline numbers + this guide's source data
jupyter nbconvert --to notebook --execute notebooks/02_method_bakeoff_results.ipynb
```

from cached artifacts; the one-time training-time HEXACO probe ran on
2026-05-13 at $3.30 and its outputs ship in the repo).
