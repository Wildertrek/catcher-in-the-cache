# OCEAN-HP cheap-head model card

**Last updated:** 2026-05-13
**Companion paper:** *The Catcher in the Cache: Retrieval, Not
Measurement, in LLM Personality Inference* (the LLM-free OCEAN-HP
cheap-head regressor)
**Companion notebook:** `notebooks/02_method_bakeoff_results.ipynb` §14
**Practitioner's guide:** `docs/practitioners_guide.md`

This directory ships two trained Ridge regression models that together
constitute the LLM-free OCEAN-HP cheap-head measurement instrument. At
inference time, character mean-utterance text is converted to a 3072-d
embedding (OpenAI `text-embedding-3-large`, mean-pool), then both heads
are evaluated to produce a 7-vector `[O, C, E, A, N, H, A_HEX]`.

## Files shipped

| File | Outputs | Training corpus | Label source | LOBO MAE |
|---|---|---|---|---|
| `ocean_ridge_regressor_v2_cheap.pkl` | O, C, E, A, N (5-d) | 562 chars / 75 works | M4 multi-provider LLM consensus (Anthropic + OpenAI + Google) | 0.297 |
| `hexaco_ridge_heads_v3_full562.pkl` | H, A_HEX (2-d) | 562 chars / 75 works | Claude Sonnet 4.5 single-provider HEXACO probe (one-time, 2026-05-13, $3.30) | 0.352 / 0.311 |

## Data provenance

- **Source corpus:** 75 canonical works from Project Gutenberg
  (`https://www.gutenberg.org/`), CC0-licensed public-domain text. Works
  span 19th-c English novel (Austen, Dickens, Brontë, Eliot, Hardy,
  Trollope), 20th-c English novel (Lawrence, Forster, Hardy, Wharton),
  Shakespearean drama, Russian translation (Tolstoy, Dostoevsky), French
  translation (Hugo, Flaubert), American 19th-c (Hawthorne, Melville,
  Twain), and contemporary literary fiction selectively. See
  `paper_artifacts/method_bakeoff_v4/books_metadata.json`
  for the full work list, Project Gutenberg IDs, and per-work checksums.
- **Character extraction:** BookNLP-based extraction of named character
  utterances with coreference resolution; full pipeline documented in
  `pillar1/`.
- **OCEAN ground-truth (training-time teacher signal):** M4
  multi-provider LLM consensus on character mean utterances under a
  redaction protocol. Three rater families (Anthropic Claude Sonnet 4.6,
  OpenAI GPT-5.2, Google Gemini 2.5 Pro), median aggregation.
- **HEXACO H + A_HEX ground-truth (training-time teacher signal):**
  Single-provider Anthropic Claude Sonnet 4.5 HEXACO probe on
  character mean utterances under the same redaction protocol. One-time
  full-corpus run executed 2026-05-13 at $3.30 total API spend.

## Licenses

- **Code:** MIT (see `LICENSE`)
- **Data:** CC-BY-4.0 (see
  `LICENSE-DATA`)
- **Trained-model artifacts (.pkl):** CC-BY-4.0 (data-derived). Users
  redistributing these models must preserve attribution to: (1) Project
  Gutenberg as the upstream text source; (2) the companion paper as
  the methodology source; (3) the LLM provider whose labels were used
  to train the head (Anthropic for HEXACO heads, multi-provider for
  OCEAN-5 head).

## Known limits

1. **English-only training corpus.** No cross-language validation
   performed. Do not deploy on non-English text without revalidation.
2. **Literary-character training labels.** The teacher signals (M4
   panel + HEXACO probe) were obtained on literary-character
   utterances, not on real-person speech. Real-person deployment
   requires a separate validation track; consider this artifact
   unfit for clinical or actuarial use without revalidation.
3. **H↔A_HEX factor purity gap.** Training labels exhibit H↔A_HEX
   correlation r=0.68 (vs human-rater norm r ∈ [0.20, 0.30]). The
   cheap head inherits and amplifies this: regressor LOBO H↔A_HEX
   correlation r=0.76. H and A_HEX are not orthogonal in this
   instrument. Closing the gap requires human-rater HEXACO training
   labels (drafted in `docs/human_hexaco_panel/`, not yet executed).
4. **No incremental predictive validity test.** No pre-registered
   downstream task currently shows the augmented 7-vector beating
   OCEAN-5 alone with a fair downstream comparison.
5. **Single-provider HEXACO heads (Claude only).** Unlike the OCEAN-5
   head (multi-provider consensus), the H and A_HEX heads inherit
   Claude-only variance. Cross-provider robustness of the 7-vector
   output is bounded above by Claude's HEXACO-probe behaviour on
   the training corpus.

## Forbidden uses

- Real-person personality assessment without independent revalidation.
- Hiring / actuarial / clinical decision-making.
- Any downstream task that conditions on H and A_HEX being orthogonal
  (they are not; see Known limits 3).

## Reproducing the heads

```bash
# (in a Python 3.12 environment)
python scripts/method_bakeoff_v4/train_hexaco_heads_v3.py
python scripts/method_bakeoff_v4/ocean_hp_cheap_head.py
```

Cold-start regeneration of the training labels (the M4 panel + HEXACO
probe runs) is ~$300-500 in API spend over ~80 hours; the cached
predictions ship in `paper_artifacts/method_bakeoff_v4/`.
