# Design rationale: the human recognition panel

**One line.** Human raters read name-redacted character text and rate Honesty-Humility
and Agreeableness; a per-character recognition question then splits their canonical
ratings into recognized vs. not-recognized. If fusion tracks *recognition* rather than
the text, the paper's retrieval account is confirmed by a rater with no training cache;
if recognized and unrecognized ratings fuse alike, the fusion is in the text (halo) and
the retrieval framing must soften.

## What the paper leaves open (why humans, why this design)
Paper 2 establishes the collapse (canonical fusion +0.75 vs. synthetic +0.23 against a
designed −0.74) and excludes stimulus-poverty (subject-mode check recovers −0.33 from
the synthetic text). Two alternatives survive, and both require a **non-LLM** rater:

1. **Judge-mode evaluative halo**: maybe canonical characters are just richer,
   halo-eliciting stimuli, and the fusion is genuinely in the text.
2. **No non-LLM measurement**: every result so far is within the LLM family.

Crucially, LLMs cannot resolve (1) even with names hidden: our LLM probe shows
canonical characters stay fused at +0.79 under name redaction because the *content*
still identifies them ("To be or not to be" is Hamlet, name or no name). You cannot
de-cache a famous character from a model. **Humans are different: some genuinely will
not recognize a redacted canonical character**, and they will tell you so. That
honest variance in recognition is the instrument.

## The locked design (lean, single-arm)
- **Stimuli:** 40 characters, 20 canonical (in-cache) + 20 synthetic (designed
  H/A_HEX anti-correlated at −0.74), as **name-redacted** evidence packs, blinded and
  shuffled. Every rater rates a seeded, balanced half (10 canonical + 10 synthetic;
  ~35–45 min); halves are deterministic in the rater ID so coverage balances.
- **Instrument:** **holistic** ratings, one H slider, one A_HEX slider per character
  (−1 to +1), NOT an item battery (see "how we got here"). Plus a per-character
  **recognition question** (yes / no / unsure), a "text gives no information" option,
  and an optional one-line rationale.
- **Raters:** ~20–25 literate, English-fluent adults with some classic-lit/film
  exposure (recognition must *vary*); ~10–12 ratings/character. No psychology background
  needed, the population anchor in the paper (n=22,299 IPIP) is laypeople.
- **Delivery:** one-click Colab (`human_panel/` in the companion); responses emailed as
  CSV; frozen analysis in `analyze_human.py`.

## The two predictions (primary tests)
1. **Synthetic measurement check:** consensus-human r(H, A_HEX) across the 20
   synthetics is **negative** (direction of the designed −0.74). Humans measure from
   text what LLM judges failed to recover (+0.23).
2. **The recognition split (the linchpin):** among canonical characters, ratings by
   raters who **recognized** the character fuse more than ratings by raters who did
   **not**. Recognized → fused = retrieval (the human cache made visible, per rater,
   per character). No difference = the fusion is in the text (halo), and the paper's
   claim must be softened. Either outcome is decisive and publishable.

## How we got here (three in-silico iterations, the instrument choice is earned)
1. A 16-item observer battery, dry-run through LLM agents, **measured a different
   construct**: item-grounding pushes any rater toward text-measurement, and a 2×2
   name manipulation on that form *inverted* (naming reduced fusion). Deploying it
   would have produced an off-message result. **Item batteries are out.**
2. A name-shown/name-redacted manipulation cannot isolate the cache for famous
   characters (content identifies them; the +0.79 result above). **Name manipulation
   is out as the primary lever; recognition is in.**
3. The paper's own **holistic probe** (rate overall H, overall A) run through a 3-way
   LLM cache manipulation reproduced the paper's phenomena cleanly, including the
   coupling-prior result now in §4. **The holistic instrument, held identical between
   the LLM baseline and the human panel, is locked.**

All plumbing (stimuli → Colab → CSV → analysis incl. the recognition split) has been
dry-run end-to-end with LLM agents standing in for humans; the analysis runs on the
real schema unchanged.

## What the result buys
A confirmed recognition split is the paper's closing figure: the same fusion, switched
by the rater's own memory, in an instrument with no training corpus at all, retrieval
demonstrated in humans, halo excluded, and the missing non-LLM measurement supplied in
one study. See `PREREGISTRATION.md` for hypotheses, decision rules, and power;
`DEPLOY.md` for the operational recipe.
