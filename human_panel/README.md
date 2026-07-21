# Human rating panel

Materials to collect human HEXACO ratings for the retrieval-vs-measurement test.

## For raters, one click, no setup

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Wildertrek/catcher-in-the-cache/blob/main/human_panel/human_rating_colab.ipynb)

Open the notebook, run the cells in order, enter your ID, rate 20 characters (two
sliders + a required recognition question each), then run the last cell to download
your `responses_<id>.csv` and email it to the address shown in the notebook. ~35-45 min.

## For the organizer
- `human_rating_colab.ipynb`, self-contained rating instrument (stimuli embedded; no
  repo access or answer key). Share the Colab badge link above with raters.
- `DESIGN.md`, the design rationale: why holistic ratings, why the recognition split is
  the primary test, and the three dry-run iterations that locked the instrument.
- `DEPLOY.md`, full protocol (assignment, attention checks, export schema, analysis).
- `PREREGISTRATION.md`, hypotheses, decision rule, power, rater population.
- Collect the returned `responses_*.csv` files, concatenate, and run
  `analyze_human.py` (in the private research kit) for the main result + recognition split.

**Target sample:** ~20-25 raters (each rates a seeded, balanced half of the 40
characters, so ~10-12 ratings per character). Raters should be literate and have some classic-literature/film exposure so
recognition varies. See `DEPLOY.md` / `PREREGISTRATION.md`.
