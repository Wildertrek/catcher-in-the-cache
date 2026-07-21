# Deployment Quickstart, "Can I Use This in My Chatbot?"

> For ML engineers, persona-bot builders, and anyone who skimmed the
> paper looking for the "what do I install" answer. Three flavors:
> high-accuracy / cheap-and-fast / structural-probe. Concrete steps,
> pseudocode, where to find prompts.

---

## TL;DR

**Use HEXACO as the construct space for LLM persona work.** OCEAN's
Agreeableness conflates the moral axis (Honesty-Humility) with warmth
(Communion), and no OCEAN variant resolves that conflation. Deployment
is then a label-availability tiering:

1. **If an LLM is available at run time, probe in HEXACO directly.**
   This is the recommended path. It pays the per-call LLM cost but
   targets the construct space the comparison endorses.
2. **If you need a cheap LLM-free regressor at scale, the OCEAN
   O/C/E cheap regressor is the safe floor today.** O, C, and E lie *off*
   the fused moral axis, so they transfer to out-of-cache
   (synthetic/novel) characters. The same head also emits A, N, H, and
   A_HEX, but only O/C/E are trustworthy out-of-cache (A and N are
   weak; H and A_HEX carry the canonical H↔A_HEX fusion and are
   research-replication-only out-of-cache).

A future cache-free HEXACO regressor would unify both tiers; until it
ships, the floor is O/C/E.

If you specifically want top accuracy on canonical literary characters
and cost is not a constraint, use **M4 multi-provider consensus**
(Anthropic + OpenAI + Google median).

If you need to know *whether* a persona is canonical-trope vs novel
and the cheap regressor's out-of-cache caveats apply, use **M6 SCPI** as a
similarity probe before initializing.

For the formal instrument-by-instrument table with measured
deployment profiles, see
[`../practitioners_guide.md`](../practitioners_guide.md).

---

## Step 1: Choose the right method for your use case

| Use case | Method | Cost | Latency | Why |
|---|---|---|---|---|
| Persona-init when an LLM is available at run time (recommended) | **Run-time HEXACO probe** | ~$0.005–0.02 / persona | ~10–30 s | Targets the recommended construct space; H separates the moral axis from warmth |
| LLM-free persona-init at scale (the floor) | **OCEAN O/C/E cheap regressor** | $0.0001 / persona | < 1 s | O/C/E lie off the fused moral axis and transfer out-of-cache; sub-second, cost-stable at scale |
| Best raw accuracy on a *canonical* character | **M4 multi-provider consensus** | ~$0.02 / character | ~30 s | Highest MAE / r against weighted GT |
| Cross-cultural / non-Anglo persona | **M3 RF regressor on text embeddings** | $0.0001 / character | < 1 s | Less retrieval contamination than M4 on out-of-distribution chars |
| Structural similarity ("is X like Bennet?") | **M6 SCPI kNN** | $10^{-6}$ / character | < 100 ms | Pure retrieval baseline; fast |
| Self-report-style trait elicitation | **Subject-mode probe (mode-dissociation)** | ~$0.01 / call | ~10 s | The model rates itself, not a target |

---

## Step 2: Concrete deployment with the OCEAN cheap regressor (the LLM-free floor)

> This is the floor path (tier 2). It emits seven factors, but only
> O/C/E are trustworthy out-of-cache, treat A/N as weak and H/A_HEX
> as research-replication-only on synthetic/novel characters (see Step
> 3 and Step 4). If you have an LLM available at run time, prefer the
> run-time HEXACO probe instead.

### What you need
- The cheap regressor Ridge weights: `personality_models/ocean_ridge_regressor_v2_cheap.pkl` (OCEAN-5)
  and `personality_models/hexaco_ridge_heads_v3_full562.pkl` (H / A_HEX heads)
- An `text-embedding-3-large` API key (OpenAI)
- The character's text (utterances, dialogue, or a short description)

### Pseudocode

```python
import joblib
import numpy as np
from openai import OpenAI

# Load the trained heads (each .pkl is a dict, not a bare sklearn model)
ocean_head = joblib.load("personality_models/ocean_ridge_regressor_v2_cheap.pkl")["model"]
hp = joblib.load("personality_models/hexaco_ridge_heads_v3_full562.pkl")

# Get character utterances (or description, or pasted dialogue)
character_text = """
"I could easily forgive his pride, if he had not mortified mine."
"I am the happiest creature in the world."
...
"""  # Bennet utterances pooled (>= 5 quotes recommended)

# Embed via text-embedding-3-large
emb = np.array([OpenAI().embeddings.create(
    model="text-embedding-3-large",
    input=character_text
).data[0].embedding])  # 3072-d vector

ocean = ocean_head.predict(emb)[0]        # [O, C, E, A, N], each in [-1, +1]
h     = hp["model_H"].predict(emb)[0]     # Honesty-Humility
a_hex = hp["model_P"].predict(emb)[0]     # HEXACO Agreeableness
```

The fully-worked version (with sanity checks and the out-of-cache trust
table) is in [`../practitioners_guide.md`](../practitioners_guide.md).

That is the full deployment pipeline. One API call (embedding), one
local matrix multiply, one OCEAN-6 vector out.

### Cost calculation

- text-embedding-3-large: $0.00013 / 1K tokens. A character's
  pooled utterances are ~2K tokens → ~$0.00026
- Local Ridge predict: $0

So total ~$0.0001 per persona-init, sub-second wall-clock.

---

## Step 3: Run-time HEXACO probe vs the OCEAN cheap regressor floor

The construct-space recommendation is **HEXACO**. The choice between
the two deployment tiers is a label-availability decision, not a
trait-vector preference:

| Situation | Use |
|---|---|
| You can afford an LLM call per persona at run time | **Run-time HEXACO probe** (recommended path; H separates the moral axis from warmth) |
| You need an LLM-free regressor at Project-Gutenberg scale | **OCEAN cheap regressor, O/C/E only** (the floor) |
| Need to distinguish *sincere* from *manipulative* in the persona spec | **Run-time HEXACO probe**: H is the load-bearing signal and the cheap regressor H is research-only out-of-cache |
| Working with synthetic / novel character archetypes | **OCEAN cheap regressor O/C/E**, or the HEXACO probe if an LLM is available; do **not** trust the cheap regressor H/A_HEX out-of-cache |

**Which cheap regressor outputs to trust out-of-cache.** The cheap regressor
emits seven factors (`O, C, E, A, N, H, A_HEX`), but they do not all
generalize equally to characters absent from the LLM training cache:

| Cheap-head factor | Out-of-cache status |
|---|---|
| **O, C, E** | **Trustworthy.** These lie off the fused moral axis and transfer to synthetic/novel characters. This is why O/C/E is the floor. |
| A, N | Weak out-of-cache; use with caution. |
| H, A_HEX | **Research-replication-only out-of-cache.** The single-provider HEXACO heads (Claude Sonnet 4.5 labels) carry the canonical H↔A_HEX fusion (Mode 2). For run-time moral-axis signal, use the LLM HEXACO probe instead. |

Why O/C/E is the floor: it is **not** that the cheap regressor labels are
human-derived. The OCEAN cheap regressor is trained on M4 multi-provider
LLM-consensus labels. O/C/E transfer out-of-cache because those three
factors lie off the fused moral axis, not because of any
LLM-independent supervision.

---

## Step 4: When the cheap regressor will fail you

The cheap regressor was trained on 562 canonical literary characters. Its
extrapolation profile:

| Out-of-distribution direction | What to expect |
|---|---|
| Modern dialogue (post-1950) | Degraded but usable; LOAO Shakespeare +0.020 MAE, well within tolerance |
| Genre shift (drama vs novel) | A prior distillation study's LOAO shows +0.029 MAE max; safe |
| Synthetic / novel characters absent from training cache | **This is the headline finding.** O/C/E still transfer (they lie off the fused moral axis) and are the trustworthy floor. The moral-axis outputs degrade: the cheap regressor H/A_HEX carry the canonical H↔A_HEX fusion and are research-replication-only here; A and N are weak. For run-time moral-axis signal on these characters, use the LLM HEXACO probe. |
| Non-Anglo / non-Western archetypes | Limited validation. The 562-char training set is Anglo-American + translated European. Cross-cultural validation is a planned follow-up |
| Real persons (vs literary characters) | **Out of scope.** Real-person / clinical measurement is a separate track, not addressed here |

---

## Step 5: Where the prompts and code live

| Artifact | Path |
|---|---|
| Cheap head weights | `personality_models/*.pkl` (see [`MODEL_CARD.md`](../../personality_models/MODEL_CARD.md)) |
| Cheap head training code | `notebooks/02_method_bakeoff_results.ipynb` |
| M4 / M5 prompt specifications | [`method_zoo.md`](method_zoo.md) |
| Comparison CSVs | `paper_artifacts/method_bakeoff_v4/bootstrap_per_method.csv` (and siblings) |
| Reproducibility map | [`../reproducibility.md`](../reproducibility.md) |

---

## What to *not* do

- **Don't use M4 for novel/synthetic personas.** The retrieval-driven
  accuracy that makes M4 great on Bennet is *exactly* the thing the
  paper diagnoses as a measurement-validity hazard. M4 will produce a
  confident, internally consistent, *wrong* vector for a persona it
  has no prior for.
- **Don't average across methods naively.** M2/M3/M4/M5/M6 disagree
  for principled reasons (the comparison section). Pick one, not a soup.
- **Don't deploy to clinical settings.** Real-person / clinical
  measurement is a separate track. This paper's instruments are for
  literary / character / non-clinical persona work.

---

## Further reading

- Full instrument catalog with measured deployment profiles:
  [`../practitioners_guide.md`](../practitioners_guide.md)
- Cheap-head architecture deep dive:
  [`../appendix/cheap_head_deployment.md`](../appendix/cheap_head_deployment.md)
- Method definitions:
  [`method_zoo.md`](method_zoo.md)
- Which trait vector to use:
  [`battery_zoo.md`](battery_zoo.md)
