# Method Zoo, M1 through M6

> The paper evaluates six methods that produce an OCEAN trait
> vector for each character: M1, M2, M3, M4, M5, M6. They are the
> methods in the comparison. This explainer says what each one does, what
> goes in, what comes out, and walks Elizabeth Bennet through them
> end-to-end.

---

## The short version

| Method | Architecture | Input | Output | When to use |
|---|---|---|---|---|
| **M1** | Embedding prototype: cosine to OCEAN trait-anchor embeddings (training-free) | character embedding | OCEAN-5 | The training-free floor (Bar-1 baseline) |
| **M2** | Random-Forest classifier (5-class per utterance) | character utterances | OCEAN-5 | Baseline; predates this paper |
| **M3** | Random-Forest regressor on character embeddings | text-embedding-3-large mean-pool per character | OCEAN-5 | Cheap and fast at scale |
| **M4** | Multi-provider LLM consensus | character evidence pack + probe battery | OCEAN-5 | Best raw accuracy (load-bearing in the comparison) |
| **M5** | Single held-out LLM probe | same as M4 but redacted character name | OCEAN-5 | Sensitivity check on M4 |
| **M6** | Semantic Character Personality Index (SCPI) | character embedding, kNN over labeled prior chars | OCEAN-5 | LOBO-fair retrieval baseline; the structural probe |

**M1 is the survey/atlas prototype and the precursor to this paper**: an
embedding-prototype baseline (cosine similarity to the survey's OCEAN trait-anchor
embeddings, no training) that this line of work grew out of, see the
[survey atlas OCEAN entry](https://github.com/Wildertrek/survey/blob/main/atlas/01_trait_based/ocean/MODEL_CARD.md)
and its [trait-anchor embeddings](https://github.com/Wildertrek/survey/blob/main/Embeddings/ocean_embeddings.csv).
On this corpus it is computed as the **training-free MAE floor** (MAE 0.427,
n=557; reproducer `paper_artifacts/method_bakeoff_v4/m1_baseline.py`). On the
calibration-free rank correlation it is no better than the M2 classifier (r 0.145 vs
0.118), so it floors MAE but is not a strong method; reported as a Bar-1 reference
only and not carried into the convergent-validity analysis. The
numbering runs M1 through M6, continuous with the survey's atlas prototype.

---

## What goes in, for every method

Each method gets, per character:

1. **Character utterances**: direct-quote spans extracted by BookNLP
   (post-quote attribution and coref). Bennet has ~$N$ utterances
   pooled across all chapters of *Pride and Prejudice*.

2. **Context windows**: for utterances that need surrounding text
   to disambiguate (e.g., sarcastic speech).

3. **Character evidence pack**: the fused utterances + context
   windows + author/title metadata that get handed to LLM methods.

The methods differ in what they *do* with this input, not what they
*receive*.

---

## M2: Random-Forest classifier

### Architecture
Per-utterance 5-class classifier (one of 5 OCEAN bins, per factor),
trained on a corpus of OCEAN-labeled utterances.

### What it computes
For each character utterance, a 5-class probability vector per OCEAN
factor. Aggregate over utterances → expected-value continuous trait
score per factor.

### Why it's in the comparison
M2 was the original baseline from a prior distillation study. It's
included to anchor the "how much does each architectural step add"
comparison.

### Strengths and weaknesses
- ✔ Fast, cheap, interpretable (RF feature importance).
- ✘ Per-utterance bag-of-words style features lose document-level
  signal; struggles with characters whose trait expression is
  *between-utterance* (e.g., Hamlet's whose conscientiousness is in
  the gap between his soliloquies and his actions).

---

## M3: Random-Forest regressor on character embeddings

### Architecture
1. Concatenate all of a character's utterances.
2. Mean-pool the `text-embedding-3-large` (3072-d) embeddings over
   utterances → one 3072-d vector per character.
3. Train an RF regressor for each OCEAN factor independently.

### What it computes
A direct regression from the 3072-d character embedding to a
continuous OCEAN-5 vector. Trained LOBO (leave-one-book-out): no
training character ever comes from the same book as a test character.

### Why it's in the comparison
M3 is the cheap-and-fast end of the trade-off. Notebook
`02_method_bakeoff_results.ipynb` shows M3 deployment at ~$0.0001
per character, ~0.5s per character.

### Strengths and weaknesses
- ✔ Cheap; LOBO-fair; competitive with M4 on Bar 1 ground-truth recovery.
- ✘ No factor-purity guarantee (the trained head can learn arbitrary
  factor combinations).

---

## M4: Multi-provider LLM consensus

### Architecture
1. Hand each character's evidence pack to **three independent LLMs**:
   - Anthropic Claude Sonnet 4.5/4.6
   - OpenAI GPT-5.x
   - Google Gemini 2.5 Pro
2. Each LLM emits an OCEAN-5 vector for that character.
3. Take the **per-factor median** across the three providers.

### What it computes
A consensus OCEAN-5 vector aggregating three LLM raters. The median
buffers single-provider outlier behavior (e.g., Google's Extraversion
collapse on certain character types; see appendix
[`per_rater_decomposition.md`](../appendix/per_rater_decomposition.md)).

### Why it's in the comparison
M4 is the load-bearing method. Best raw accuracy: MAE ≈ 0.230,
Pearson $r \approx 0.770$ vs weighted GT.

### Strengths and weaknesses
- ✔ Highest single-method accuracy on Bar 1.
- ✘ Expensive (3 API calls per character); the *very thing the paper
  diagnoses*, retrieval from training cache, boosts apparent
  accuracy on canonical chars and is the reason for the paired
  substrate test on synthetic chars.

---

## M5: Single held-out LLM probe

### Architecture
Same prompt and battery as M4, but:
- Only one LLM (Anthropic Claude Sonnet 4.5).
- Character name and book title **redacted** from the evidence pack
  before the call.

### What it computes
A "what does the LLM say if it doesn't know who this is?" OCEAN-5
vector. This is the most direct sensitivity check on whether M4's
accuracy is retrieval-driven.

### Why it's in the comparison
M5 vs M4 → the gap between named and name-redacted gives an early
read on the canonical-prior signal that the substrate falsifier
(RQ6.9) later quantifies more rigorously.

### Strengths and weaknesses
- ✔ Targets the retrieval-vs-measurement question directly.
- ✘ Single-rater (no consensus); higher variance than M4.

---

## M6: Semantic Character Personality Index (SCPI)

### Architecture
1. Embed each character (same `text-embedding-3-large` mean-pool as M3).
2. For test character $c$: find the $k$ nearest labeled characters in
   the **rest of the corpus** (LOBO: nearest neighbors come from
   different books).
3. Output OCEAN-5 = similarity-weighted average of the neighbors'
   GT labels.

### What it computes
A *retrieval-based* OCEAN-5 vector for each character. Structurally,
M6 is "the cheapest possible retrieval baseline", no learned
parameters beyond the embedding.

### Why it's in the comparison
M6 is the structural-probe baseline. It anchors the SCPI / SPI / SAPI
methodological family (see appendix
[`scpi_structural_probe_results.md`](../appendix/scpi_structural_probe_results.md)).

### Strengths and weaknesses
- ✔ Cheapest method ($\sim 10^{-6}$ per character); fully
  interpretable (you can see which neighbors voted).
- ✘ Floor for trait inference on characters with no semantic
  neighbors in the labeled set (genre-isolated characters fail).

---

## How the comparison combines them (Bar 1 / Bar 2 / Bar 3)

The methods compete on three "Bars":

**Bar 1, Ground-truth recovery.** Each method's output is compared to
the weighted multi-source GT (Eq. 1 in §2.2). Metrics: MAE, Pearson
$r$, Lin's CCC.

**Bar 2, MTMM convergent validity.** All pairs of methods are
compared via the corrected Campbell-Fiske three-inequality test on
the $5 \times 5$ OCEAN MTMM matrix. The convergent triangle of
M3↔M4↔M5 holds across all three inequalities; M2 and M6 fail on
one or more.

**Bar 3, External concurrent validity.** A held-out $n=60$ subset
with Open Psychometrics SWCPQ Ridge-mapped OCEAN labels gives an
external reference. M4 wins; M3 close behind.

For deployment-time *single-instrument* choices, see
[`../practitioners_guide.md`](../practitioners_guide.md).

---

## Worked example, Elizabeth Bennet

The paper's §2.2 box gives the *ground-truth* worked example for
Bennet (AGT + PGT consensus → $\hat O = +0.69$, $\hat C = +0.63$,
$\hat E = +0.31$, $\hat A = +0.28$, $\hat N = -0.03$).

Here is the *predicted* side: what each method produces for Bennet on
trait $O$, end-to-end.

### Inputs (shared across all methods)
- Character ID: Bennet (book: *Pride and Prejudice*, Austen)
- Utterance count: from the per-book character registry
  (`rag_indices/1342_pride_and_prejudice/pillar1/character_registry.json`)
  in the private research repository; not redistributed with this companion.
- Mean-pool embedding: 3072-d vector (cached in
  `paper_artifacts/method_bakeoff_v4/character_embeddings.npz`)

### M2 output
- Per-utterance classifier votes aggregated to expected value on $O$.
- Per-character predictions are in the `M2_classifier` block of each entry
  in `paper_artifacts/method_bakeoff_v4/predictions.json`.

### M3 output
- Bennet's 3072-d embedding → RF regressor → continuous $\hat O$.
- See the `M3_regressor` block of each entry in
  `paper_artifacts/method_bakeoff_v4/predictions.json`.

### M4 output
- Anthropic: $O \to$ value $A$
- OpenAI: $O \to$ value $B$
- Google: $O \to$ value $C$
- M4 output: $O \to \mathrm{median}(A, B, C)$
- Per-character per-provider matrix in
  `m4_per_provider_predictions.csv`; consensus in
  `m4_predictions.csv`.

### M5 output
- Same as the Anthropic call in M4 except the prompt sees
  `[CHARACTER]` and `[BOOK]` placeholders instead of "Elizabeth Bennet"
  and "Pride and Prejudice".
- See `m5_predictions.csv` and the gap-vs-M4 table.

### M6 output
- Bennet's nearest $k$ neighbors in embedding space (across other
  books) → similarity-weighted average of their GT-$O$ labels.
- See `m6_predictions.csv` and the appendix
  [`m6_k_sensitivity.md`](../appendix/m6_k_sensitivity.md).

### Final comparison comparison
The CSV `per_character_predictions.csv` ships every character's
GT-$O$, $\hat O$ from every method, and the per-method residual.
For Bennet, the residuals are all within $\pm 0.10$ of the GT-$O$
of $+0.69$, Bennet is a *canonical-easy* character. The interesting
characters are ones with $|\mathrm{residual}| > 0.30$, which the
appendix walks through in
[`rq2_mtmm_full_tables.md`](../appendix/rq2_mtmm_full_tables.md).

---

## Reading the method-comparison CSVs

The cached artifacts in
[`../../paper_artifacts/method_bakeoff_v4/`](../../paper_artifacts/method_bakeoff_v4/)
ship:

| File | Contents |
|---|---|
| `per_character_predictions.csv` | 562 chars × (5 methods × 5 OCEAN factors + GT) |
| `m4_per_provider_predictions.csv` | 562 chars × (3 providers × 5 factors) |
| `character_embeddings.npz` | 562 × 3072 `text-embedding-3-large` mean-pool matrix |
| `bar1_results.csv` | Per-method MAE / r / CCC vs weighted GT |
| `bar2_mtmm_matrix.csv` | $5 \times 5$ MTMM matrix, all pairs |
| `bar3_op_overlap_results.csv` | OP-overlap concurrent validity |

If you want the methods to reproduce on a new character, the
end-to-end pipeline is in `notebooks/02_method_bakeoff_results.ipynb`.
