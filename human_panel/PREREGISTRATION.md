# Pre-Registration: Human Recognition Panel (retrieval vs. halo)

**Study.** Do human raters, reading name-redacted character text, (a) recover the
designed Honesty-Humility / HEXACO-Agreeableness structure that LLM judges fail to
recover on out-of-corpus characters, and (b) show more H/A fusion on canonical
characters they *recognize* than on ones they do not? Humans have no training
"cache"; their honest, per-character recognition variance is the instrument that
separates retrieval from a text halo, the test LLMs structurally cannot provide
(content identifies famous characters to a model even with names hidden).

**Parent result (Paper 2 v13).** LLM judge-mode within-rater r(H, A_HEX) is +0.75 on
canonical characters and +0.23 on 20 synthetic out-of-corpus characters (designed
r = −0.74). A subject-mode LLM check recovered −0.33 from the synthetic text
(excluding stimulus poverty), and a name-only probe showed a +0.83 fused prior with
no text at all. Open questions: the judge-mode evaluative halo, and the absence of
any non-LLM measurement on the stimuli.

## Design (locked)
- **Single arm, name-redacted.** No name-shown condition (an earlier factorial design
  was superseded; see *Superseded design* below).
- **Stimuli:** 40 characters, 20 canonical (in-cache) + 20 synthetic (designed
  H/A_HEX anti-correlated, corpus-level r = −0.74), as name-redacted evidence packs
  (min ~660 chars of quoted dialogue each), blinded and shuffled.
- **Assignment:** each rater rates a **seeded, balanced half** (10 canonical + 10
  synthetic of the 40), order randomized per rater; ~35–45 min per session. Halves
  are deterministic in the rater ID, so coverage balances across raters.
- **Instrument:** holistic ratings, one Honesty-Humility slider and one
  Agreeableness slider per character on [−1, +1] with HEXACO-keyed anchors, plus a
  required recognition question ("Have you encountered this character before, book,
  film, class, elsewhere?": yes / no / unsure), a "text gives no information" option
  (scored as missing, not neutral), and an optional one-line rationale.
- **Raters:** ~20–25 literate, English-fluent adults (18+) with some classic
  literature/film exposure, so recognition varies. Lay raters by design (the human
  population anchor in the paper, n = 22,299 IPIP, is laypeople).
- **Delivery:** self-contained Colab notebook → per-rater CSV
  (`rater_id, panel_id, condition, H, A_HEX, recognition, no_info, rationale,
  elapsed_min`) → concatenated → frozen analysis.

## Hypotheses and decision rules
- **H1 (measurement).** Consensus-human r(H, A_HEX) across the 20 synthetic
  characters is negative. Decision: character-bootstrap 95% CI upper bound < 0 →
  supported; r < 0 with CI spanning 0 → suggestive, extend collection; r ≥ 0 → not
  supported (and itself informative: even humans fail to recover the design).
- **H2 (retrieval vs. halo, the linchpin).** Among canonical characters, the
  consensus r(H, A_HEX) computed from ratings where the rater *recognized* the
  character exceeds the value computed from ratings where they did not.
  Decision: r_yes − r_no > 0.15 with both cells estimable (≥ 3 characters each) →
  retrieval supported (the human cache made visible); no difference at adequate
  coverage → the fusion is in the text (halo), and the paper's retrieval framing for
  the canonical residual must soften. Either outcome is decisive and publishable.

## Frozen analysis and quality control
- **Frozen analysis:** `analyze_human.py` (H1 main cells, H2 recognition
  split, exclusions), frozen before data collection and held in the private research
  kit rather than redistributed here (see `README.md`). No analysis is conditioned on
  the observed effect.
- **Exclusions (pre-committed, applied before analysis):** raters failing either of
  the two embedded attention checks (H ≥ +0.5 and A ≤ −0.5 required on ATTN entries,
  checked on raw rows so a "no information" tick is not an escape); raters with no
  attention-check rows; zero-variance (straight-lined) sessions. Session elapsed time
  is recorded; implausibly fast sessions (< 10 min) are reviewed and may be excluded
  with the reason logged.
- **Missing data:** "no information" rows are missing, not neutral; the export gate
  requires the recognition question answered on every entry.

## Power
The H1 decision rule is a sign test against a designed r = −0.74 and saturates early:
simulation of the locked design (holistic single rating per construct, per-rating SD
up to 0.6) reaches power ≥ 0.95 by ~5 raters per character; with ~20–25 raters each
covering half the panel (~10–12 ratings/character), H1 is amply powered. The binding
constraint is **H2 cell coverage**: enough recognized *and* not-recognized ratings
per canonical character, which depends on the rater pool's actual recognition rate
and is why N targets ~20–25 rather than the H1 minimum. If either H2 cell has < 3
estimable characters, we extend collection rather than reinterpret.

## Known limitations (pre-declared)
1. **Recognition question placement.** Recognition is asked on the same screen as the
   ratings (after the sliders), not in a separate second pass; this may cue
   identification attempts during rating. The bias direction inflates
   recognized-cell fusion, i.e., it works *against* a clean H2 null, a positive H2
   at this placement therefore needs the caveat, while a null H2 is conservative.
2. **Single-item measures.** One holistic rating per construct per rater; reliability
   comes from consensus across ~10–12 raters per character, and the unit of analysis
   is the consensus rating, not the individual rater. The item-battery alternative
   was piloted and measured a different construct (see `DESIGN.md`).
3. The synthetic characters are LLM-authored; the designed −0.74 is authorial intent.

## Superseded design (disclosure)
An earlier version of this pre-registration specified a 2×2 name × substrate
factorial using a 16-item observer battery. Both elements were dropped after
in-silico dry runs: the item battery shifted the construct being measured, and name
manipulation cannot isolate the cache (for LLMs, content identifies famous
characters; for humans, the recognition question replaces it). No human data were
collected under the superseded design. The factorial remains documented in the git
history and in `DESIGN.md` ("How we got here").
