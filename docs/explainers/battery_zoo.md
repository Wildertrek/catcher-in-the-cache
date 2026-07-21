# Battery Zoo, OCEAN, HEXACO, OCEAN-6, OCEAN-HP

> If you've been counting traits and getting a different number each
> time, this is for you. The paper uses six related-but-distinct trait
> vectors. They share machinery but differ in factor count, factor
> names, and deployment use.

---

## The short version

| Vector | Factors | When the paper uses it |
|---|---|---|
| **OCEAN** | 5 (O / C / E / A / N) | Default OCEAN reference. The lingua franca of trait psych |
| **HEXACO** | 6 (H / E_HEX / X / A_HEX / C_HEX / O_HEX) | Lexical six-factor model; introduces Honesty-Humility |
| **OCEAN-HP** | 7 (OCEAN + H + A_HEX) | Augmented vector; what the cheap regressor emits (only O/C/E trustworthy out-of-cache) |
| **OCEAN-6** | 6 (OCEAN + H, *no A_HEX*) | A described OCEAN augmentation (drops the redundant HEXACO-A); see note below, the construct-space recommendation is HEXACO, not OCEAN-6 |
| **BFI** | 5-factor instrument (44 items) | A specific BFI test used for the mode-dissociation bridge |
| **IPIP-50** | 5-factor instrument (50 items) | A specific OCEAN test used as mode-dissociation holdout |

The first four are **trait vectors** (what is being measured).
The last two are **instruments** (how you measure it). Mixing them
up is the most common reader-friction moment in §3.

---

## Why so many?

OCEAN (OCEAN) has been the dominant trait model in psychology since
the 1990s. HEXACO (Ashton & Lee, 2007) is a lexical six-factor model
that adds **Honesty-Humility (H)** as a sixth factor and reorganizes
the OCEAN-Agreeableness (A) variance: roughly, OCEAN-A splits across
HEXACO-A (now anchored on patience / forgiveness / gentleness)
and HEXACO-H (sincerity / fairness / lack of greed).

This split matters for LLM personality measurement because:

1. **OCEAN-A is bipolar on canonical literary characters.** A
   manipulative villain reads high on OCEAN Agreeableness because
   the OCEAN-A factor mixes "kind" with "submissive", and the villain
   is often *agreeably submissive in scene* while morally corrupt.
   HEXACO surfaces the manipulation in H, leaving A_HEX cleaner.

2. **The H ↔ A_HEX fusion is the paper's diagnostic signal.** On
   canonical characters, LLM raters anti-correlate H and A_HEX at mean
   $|r| = 0.75$. On synthetic characters they drop to $|r| \approx 0.30$.
   That gap (-0.447) is the load-bearing finding.

3. **The deployment recommendation is HEXACO as the construct space.**
   No OCEAN variant resolves the moral-axis-vs-warmth conflation in A,
   so HEXACO is the recommended construct space for LLM persona work.
   Deployment is then a label-availability tiering: probe in HEXACO
   directly when an LLM is available at run time (the recommended
   path), or fall back to the OCEAN O/C/E cheap regressor as the LLM-free
   floor at scale (O/C/E lie off the fused moral axis and transfer
   out-of-cache; A/N are weak and H/A_HEX research-only out-of-cache).

---

## The full picture

```
                OCEAN (OCEAN)            HEXACO (six-factor)
                ┌──────────────┐            ┌──────────────────┐
                │              │            │   H             │
                │              │            │   (Honesty-      │
                │              │   ┌────────│    Humility)    │
                │              │   │        │                  │
                │  O           │   │        │   O_HEX          │
                │  C           │   │        │   C_HEX          │
                │  E           │   │        │   X (Extraversion)│
                │  A           │──────┐     │   A_HEX          │
                │  N           │   │  │     │   E_HEX (Emotion)│
                │              │   │  │     │                  │
                └──────────────┘   │  └──→──│   (HEXACO-A)    │
                                    │        └──────────────────┘
                                    │
                                    └──────→  some OCEAN-A variance
                                              loads onto HEXACO-H
```

OCEAN-A is approximately a mixture of HEXACO-A and HEXACO-H. The
paper's bipolarity finding is that LLM raters fusion that variance
back together on canonical characters in a way that mirrors what
HEXACO unmixes.

---

## The six trait vectors in detail

### 1. OCEAN, the OCEAN

| Factor | Letter | Anchors |
|---|---|---|
| Openness | O | curious, imaginative, abstract |
| Conscientiousness | C | organized, responsible, hard-working |
| Extraversion | E | outgoing, energetic, sociable |
| Agreeableness | A | warm, cooperative, kind |
| Neuroticism | N | anxious, moody, emotionally reactive |

**Range:** $[-1, +1]$ per factor throughout the APERTURE system.
**Use:** Default reference; every method M2–M6 emits an OCEAN vector.

### 2. HEXACO, the lexical six-factor model

| Factor | Letter | Anchors |
|---|---|---|
| **Honesty-Humility** | **H** | **sincere, modest, fair vs. manipulative, greedy, entitled** |
| Emotionality | E_HEX | anxious, vulnerable, sentimental |
| eXtraversion | X | sociable, lively (≈ OCEAN-E) |
| Agreeableness | A_HEX | patient, forgiving, gentle |
| Conscientiousness | C_HEX | organized, disciplined (≈ OCEAN-C) |
| Openness | O_HEX | curious, unconventional (≈ OCEAN-O) |

**Range:** $[-1, +1]$ per factor.
**Use:** Bar 2 cross-method MTMM and the activation probe latent test.

H is the factor of interest for the substrate falsifier. A_HEX is its
partner in the bipolarity fusion.

### 3. OCEAN-HP, OCEAN plus the two HEXACO factors that matter

OCEAN-5 + H + A_HEX = 7-D vector.

- "HP" = H + Patience. (A_HEX's lexical anchor in the HEXACO literature
  is patience / gentleness, hence the shorthand.)
- Proposed in the paper's earlier framing as the "right" vector
  for literary character modeling.
- Current framing: this is the vector the cheap regressor emits,
  but only its O/C/E factors are trustworthy out-of-cache. A/N are
  weak and the cheap regressor H/A_HEX are research-replication-only on
  synthetic/novel characters (they carry the canonical H↔A_HEX
  fusion). It is a described artifact, not the recommendation.

### 4. OCEAN-6: a described OCEAN augmentation (not the recommendation)

OCEAN-5 + H = 6-D vector.

- Drops A_HEX (which is the partner-in-redundancy with both H and
  OCEAN-A).
- Backwards-compatible with downstream surfaces keyed on OCEAN-5
  (just one extra column).
- It does beat OCEAN-HP on Bar 2 (the A/A_HEX/H redundancy cluster is
  where OCEAN-HP fails), but **no OCEAN variant resolves the
  moral-axis-vs-warmth conflation in A.** The construct-space
  recommendation is therefore **HEXACO**, not OCEAN-6: probe in HEXACO
  at run time when an LLM is available (the recommended path), or use
  the OCEAN O/C/E cheap regressor as the LLM-free floor at scale. OCEAN-6
  is documented here for completeness, not as the headline guidance.

### 5. BFI, OCEAN Inventory (the instrument)

- 44 items, OCEAN-keyed.
- Used in the mode-dissociation BFI→HEXACO bridge (Amendment 11): can we recover
  HEXACO factor structure from a BFI input via the survey's atlas?
  Answer: yes, kNN accuracy 0.720 ≥ 0.55 pre-reg threshold.
- BFI's known property: BFI-A residualizes onto HEXACO-H, i.e., when
  you take OCEAN Agreeableness and project it through the HEXACO
  factor space, the leftover variance lands on H. The mode-dissociation test
  confirms this in our panel.

### 6. IPIP-50: public-domain OCEAN instrument

- 50 items, public domain (BFI is copyrighted).
- Used as the mode-dissociation holdout instrument: trained the BFI→HEXACO bridge
  on BFI items, validated on IPIP-50.

---

## How to read the factor symbols in the paper

| Symbol | What | Where it appears |
|---|---|---|
| **O, C, E, A, N** | OCEAN factors | universal |
| **A** | OCEAN Agreeableness (when not subscripted) | §1, §4 |
| **A_HEX** or **A** in HEXACO context | HEXACO Agreeableness | §3, §4.3 |
| **H** or **HH** | HEXACO Honesty-Humility | §4 (load-bearing) |
| **E_HEX** | HEXACO Emotionality | §4.4 probe |
| **X** | HEXACO eXtraversion (avoids name-clash with OCEAN-E) | §4.4 |
| **O_HEX, C_HEX** | HEXACO Openness / Conscientiousness | §4.4 |

When the paper says **"$|r|_{H \leftrightarrow A_{\mathrm{HEX}}}$"**, it
means the absolute Pearson correlation between Honesty-Humility and
HEXACO-Agreeableness, taken within a single rater across the 60
canonical characters.

When the paper says **"OCEAN-HP"**, it means the 7-D OCEAN-5 + H +
A_HEX vector.

When the paper says **"OCEAN-6"**, it means the 6-D OCEAN-5 + H vector
(no A_HEX).

---

## Quick deployment guide

| Goal | Use |
|---|---|
| Standard psych-aligned trait inference | OCEAN |
| LLM persona work, construct space | **HEXACO** (the recommendation; H separates the moral axis from warmth) |
| Need Honesty-Humility for moral character work, LLM available at run time | Run-time **HEXACO probe** (recommended path) |
| Diagnostic / falsifier work (substrate retrieval test) | OCEAN-HP |
| Cross-instrument bridge / equating between BFI and HEXACO | BFI input → panel → HEXACO output |
| Production persona-init at scale, LLM-free | **OCEAN O/C/E cheap regressor**: the floor; O/C/E transfer out-of-cache, A/N weak, H/A_HEX research-only (see [`../practitioners_guide.md`](../practitioners_guide.md)) |

For the formal instrument-by-instrument table with measured
deployment profiles (MAE, latency, cost), see
[`../practitioners_guide.md`](../practitioners_guide.md).
