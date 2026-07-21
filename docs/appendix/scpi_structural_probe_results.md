# SCPI as a Structural Probe over the Canonical-Character Space

## Results from NB07 Panels G + H, author-style fingerprinting + author-similarity heatmap

**Date:** 2026-05-20
**Source notebook:** `07_scpi_character_clusters.ipynb` sections 11–13 (research-repo notebook, private; available on request). The full results are reproduced in this document.
**Reproduction:** ~10 s on Mac M-series via `jupyter nbconvert --execute`; $0 API spend; minimal Python 3.12 stack (numpy + pandas + scipy + scikit-learn + matplotlib). Requires `books_metadata.json` for the book → author mapping (in this repo at `paper_artifacts/method_bakeoff_v4/books_metadata.json`).

This document is the standalone results summary for the SCPI expansion in NB07. The comparison / bipolarity-diagnostic content (NB07 sections 1–10) is the original the paper §4 RQ1–RQ7 reproducer; sections 11–13 below position SCPI as a **structural probe** over the canonical-character corpus, with two novel applications and a methodological-family roadmap.

---

## Headline finding

**LLM-rater OCEAN consensus on canonical literary characters recovers author-level stylistic signatures.** The 562 characters of the comparison corpus cluster by author in OCEAN space; the resulting 22-author centroid map reproduces empirically-known stylistic neighborhoods (Dickens ↔ Austen, the dramatists' cluster) and identifies Bram Stoker as the consistent outlier (Gothic-horror cast genuinely distinct from social-realism characters).

**Implication:** SCPI is a structural probe, not just an M6 comparison measurement method. The same FAISS-k-NN-over-embedding architecture that the survey/atlas paper's Semantic Personality Index applied to 44 personality models applies here to 562 characters, and by extension to authors, LLM-generated personas, and genres.

---

## Panel G, Author-style fingerprinting (22 authors, ≥ 3 characters)

For each author with ≥ 3 characters in the comparison corpus, we computed the M4 multi-provider consensus OCEAN centroid. Author-name normalization handles two failure modes in the raw Project Gutenberg metadata: "Last, First" vs "First Last" ordering and the "Leo, graf Tolstoy" honorific. Final canonical-name aggregation merges Tolstoy and Dostoevsky variants.

### Author centroids (top 15 by character count)

| Author | n chars | O | C | E | A | N | Within-author scatter |
|---|---|---|---|---|---|---|---|
| William Shakespeare | 305 | +0.14 | +0.09 | +0.20 | −0.08 | +0.26 | 0.42 |
| Charles Dickens | 36 | +0.07 | +0.23 | +0.26 | +0.11 | +0.10 | 0.50 |
| Jane Austen | 32 | +0.02 | +0.22 | +0.30 | +0.16 | +0.08 | 0.49 |
| **Fyodor Dostoevsky** | 22 | **+0.40** | −0.04 | +0.35 | −0.10 | **+0.55** | 0.41 |
| Henrik Ibsen | 21 | +0.06 | +0.16 | +0.14 | −0.07 | +0.39 | 0.39 |
| Oscar Wilde | 21 | +0.15 | +0.13 | +0.21 | −0.03 | +0.11 | 0.48 |
| **Leo Tolstoy** | 17 | +0.16 | +0.12 | +0.32 | **+0.34** | +0.40 | 0.37 |
| Joseph Conrad | 10 | +0.23 | −0.08 | −0.03 | −0.15 | +0.22 | 0.30 |
| Charlotte Brontë | 10 | +0.09 | +0.35 | +0.10 | −0.20 | +0.10 | 0.49 |
| George Bernard Shaw | 10 | +0.21 | +0.10 | +0.22 | +0.12 | +0.19 | 0.42 |
| Robert Louis Stevenson | 10 | +0.03 | +0.23 | −0.34 | +0.11 | +0.30 | 0.36 |
| Sophocles | 7 | +0.03 | +0.29 | −0.16 | +0.04 | +0.33 | 0.32 |
| F. Scott Fitzgerald | 7 | +0.09 | +0.02 | +0.49 | −0.17 | +0.36 | 0.36 |
| **Franz Kafka** | 7 | **−0.21** | +0.16 | **−0.20** | −0.11 | +0.31 | **0.25** |

### Interpretation

- **Dostoevsky** is the canonical "tortured Russian intellectual": high Openness (+0.40), low Agreeableness (−0.10), very high Neuroticism (+0.55). The character cast (Raskolnikov, the Karamazov brothers, Prince Myshkin) is intellectual, emotionally volatile, morally complex.
- **Tolstoy** is also intellectually open and emotionally volatile but markedly warmer (A = +0.34 vs Dostoevsky's −0.10), the "warm psychological realism" axis distinguishes the two Russians.
- **Austen** + **Dickens** sit very close: both warm, balanced, moderately extraverted, low neuroticism. 19th-century British social realism produces a clean, narrow trait signature.
- **Conrad** is the cold isolated wanderer: low E, low A, low C, Marlow and his ghostly Africa.
- **Kafka** has the **tightest within-author scatter (0.25)**, meaning his characters most consistently share a profile: introverted (E = −0.20), closed (O = −0.21), mildly neurotic (N = +0.31), the "Kafkaesque" archetype is empirically real.
- **Stevenson** has the lowest Extraversion centroid in the corpus (−0.34); his characters are introverts almost categorically (Jekyll, Hyde, Treasure Island's Jim Hawkins).

### PCA structure

PC1 loads on Agreeableness (0.84) + Conscientiousness (0.46), the warm/prosocial axis.
PC2 loads on Extraversion (0.72) + Openness (0.62), the expressive/intellectual axis.
Combined, PC1+PC2 explain the bulk of author-centroid variance.

---

## Panel H, Author-similarity matrix

Pairwise Euclidean distances between author centroids in 5-D OCEAN space. Mean pairwise distance: 0.595. Maximum: 1.366.

### 8 most-similar author pairs (closest centroids)

| Pair | Distance | Interpretation |
|---|---|---|
| Charles Dickens ↔ Jane Austen | 0.088 | 19th-c British social realism cluster, closest pair in the corpus |
| William Shakespeare ↔ Oscar Wilde | 0.158 | Dramatists with similarly diverse character casts |
| William Shakespeare ↔ Henrik Ibsen | 0.177 | Dramatist cluster expansion |
| Oscar Wilde ↔ George Bernard Shaw | 0.182 | Late-Victorian / Edwardian witty social dramatists |
| Charles Dickens ↔ Oscar Wilde | 0.191 | Mid/late-Victorian social-comic register |
| Robert Louis Stevenson ↔ Sophocles | 0.203 | Convergent C+ and N+ profiles (didactic moral tension) |
| George Bernard Shaw ↔ Mark Twain | 0.207 | Anglo-American satirists |
| Charles Dickens ↔ George Bernard Shaw | 0.213 | British social commentary across eras |

### 5 most-distant author pairs

| Pair | Distance | Interpretation |
|---|---|---|
| Emily Brontë ↔ Bram Stoker | 1.366 | Wuthering Heights (intense Yorkshire family) vs Dracula (monsters + victims), opposite corners of OCEAN space |
| Emily Brontë ↔ Herman Melville | 1.180 | Yorkshire moor vs whaling ship |
| Lewis Carroll ↔ Bram Stoker | 1.157 | Whimsical children's fantasy vs Gothic horror |
| Franz Kafka ↔ Bram Stoker | 1.101 | Existential dread (introverted, closed) vs Gothic dread (monstrous, dramatic) |
| Joseph Conrad ↔ Bram Stoker | 1.081 | Both dark but in opposite ways: Conrad cold-introspective, Stoker dramatic-monstrous |

**Bram Stoker is the consistent outlier**, appearing in 4 of 5 most-distant pairs. *Dracula*'s character cast (the Count, Mina, Jonathan Harker, Van Helsing, Renfield) is genuinely structurally different from the rest of the corpus, Stoker writes character roles, not rounded social characters in the sense the comparison measures.

---

## Panel J, Inter-method disagreement as a deployment-relevant uncertainty signal (deferred)

In prototyping, the per-character standard deviation across M2–M5 OCEAN predictions correlates weakly with M4 prediction error (Pearson r = +0.111, p = 0.012; Spearman ρ = +0.074, p = 0.091; quartile-difference in M4 MAE between high-disagreement and low-disagreement chars: +0.020). The signal is statistically detectable but practically small, inter-method disagreement is NOT a reliable router-signal between the cheap regressor and M4 consensus.

**Honest interpretation:** the LLM and RF methods agree more than they disagree on hard characters, and the small disagreement quartile-effect (~2 percentage points in MAE) is not enough to drive deployment-time routing. Deferred from the notebook; flagged here as a negative result.

---

## Section 13: Methodological family

SCPI is the character-level analogue of the survey/atlas paper's Semantic Personality Index (SPI). Same architecture (FAISS k-NN over OpenAI `text-embedding-3-large` + similarity-weighted profile inheritance); different unit of analysis.

| Index | Unit | Embedding source | Status |
|---|---|---|---|
| **SPI** | Personality models (44) | Trait-definition text + items | The survey/atlas paper |
| **SCPI** | Literary characters (562) | Character utterances + narrator dialogue | This paper (M6 + Panels G/H above) |
| **SAPI** | Authors (22 with ≥ 3 chars) | Author-aggregated character centroids | Sketched in Panel G; standalone paper candidate |
| **SPPI** | LLM-generated personas | Persona-prompt embeddings | Future work, persona-pool diversity audit, persona-drift monitoring |
| **SGPI** | Genres / periods / movements | Genre-aggregated centroids | Future work, literary-anthropology angle (Victorian vs Modernist, Russian vs Anglo-American) |

The architectural pattern: any unit you can embed in OpenAI's 3072-d semantic space can be SPI-indexed, k-NN-queried, and similarity-weighted-inherited. Each application has discovery promise.

---

## Standalone publication potential

Panels G + H + the §13 family discussion together form the empirical core of a workshop / methods paper:

**Working title:** *"SCPI: A Structural Probe over Canonical-Character Space, with Applications to Author-Style Fingerprinting."*

**Length:** ~6–8 pages.

**Target venues:**
- ACL findings (computational literary studies track)
- NeurIPS workshops: Foundation Model Interpretability; Causal Representation Learning; Computational Cognitive Neuroscience
- CogSci conference
- PNAS for the social-science angle
- Or a Cognitive Science / Digital Humanities journal submission

**Executable companion artifact:** NB07 (this notebook). $0 API spend; 4 figures (Panel A through Panel H); runs in ~10 seconds on free Colab.

**Contributions to claim:**

1. SCPI methodology: FAISS-k-NN-over-character-embedding structural probe over canonical-character corpus.
2. Author-style fingerprinting application: 22-author centroid map recovers known stylistic clusters (Dickens ↔ Austen at d=0.088) and outliers (Stoker in 4 of 5 most-distant pairs).
3. Empirical author identifiability finding: 19th-c British social realism produces a narrow, distinguishable trait signature; Russian psychological realism produces a high-Openness high-Neuroticism cluster; dramatists cluster by diverse character casts; Gothic horror is a structural outlier.
4. Methodological family roadmap: SPI → SCPI → SAPI → SPPI → SGPI; the architectural pattern generalises to any embeddable unit of analysis.
5. Honest negative result: inter-method disagreement is not a useful deployment-time uncertainty signal (Panel J prototyping, deferred from the notebook with disclosure).

**Relationship to the paper:** Panels G + H are an extension beyond the comparison / Catcher-in-the-Cache scope. They don't change any headline number; they reposition SCPI as a structural probe that earns its own treatment. The expansion gives the paper a clean "what's next" arrow into a future standalone methods paper.

---

## Reproducibility

| Asset | Path | Notes |
|---|---|---|
| Notebook | `07_scpi_character_clusters.ipynb` (private research repo; available on request) | 29 cells (14 md + 15 code) |
| Data | `paper_artifacts/method_bakeoff_v4/predictions.json` | 562 chars × M2–M6 OCEAN + GT |
| Book metadata | `books_metadata.json (in this repo at `paper_artifacts/method_bakeoff_v4/books_metadata.json`)` | 76 books → author + format |
| Outputs | NB07 inline (Panels G + H + §13 markdown) | PNG figures rendered at execute time |
| CI status | NB07 is in supporting-reproducer table (not CI primary matrix) | Runs locally / on Colab; not smoke-tested per-push |

The notebook handles the missing-dependency case gracefully: if `books_metadata.json` is not found locally (e.g., Colab without the private research repository mounted), Panel G prints a skip notice and the comparison primary panels still reproduce.

---

_Generated: 2026-05-20. Source: NB07 sections 11–13 execution (private research repo; available on request)._
