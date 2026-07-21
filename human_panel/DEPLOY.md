# Deploy guide, the human panel, step by step

Everything needed to run the human arm on a survey platform (Prolific for recruiting +
Qualtrics/Google Forms for the instrument, or any equivalent). The design is locked (see
`DESIGN.md`); this is the operational recipe. When ratings come back, `analyze_human.py`
produces the result and the recognition split.

## 0. Before launch
- **Ethics:** an informed-consent page + IRB/exempt determination (rating fictional
  characters from short text is typically minimal-risk, but that call is the
  collaborator's). Collect no PII beyond a platform-issued rater ID.
- **Rater population:** literate, English-fluent adults with some exposure to classic
  literature/film, so recognition varies across the canonical characters (the linchpin
  needs that variance). Educated general public or humanities/English students are ideal;
  psychology/HEXACO experts are not needed as the primary sample. A collaborating instructor's students or
  colleagues fit well. **Target ~20–25 raters** (each rates a balanced half → ~10–12
  ratings/character; recruit a few extra to absorb exclusions).

## 1. Assignment (lean single-arm design)
- **One condition for everyone: name-redacted** (evidence only). The redacted stimuli
  are embedded directly in the Colab notebook
  (`notebooks/human_rating_colab.ipynb`); no separate booklet file is shipped.
  The name-shown arm is optional future work.
- **Each rater rates a seeded, balanced half**: 10 canonical + 10 synthetic of the 40
  (panel_ids C01–C40) in random order, ~35–45 min. Halves are deterministic in the
  rater ID so coverage balances; ~20–25 raters give ~10–12 ratings/character. The
  Colab notebook does all of this automatically.

## 2. Per-character flow (repeat for each of the 20)
1. Show the character block (evidence only; name hidden).
2. **Two holistic ratings** (this is the paper's instrument, do NOT use a long item
   battery):
   - **Honesty-Humility (H):** slider/7-point, −1 = very low (manipulative, greedy,
     boastful, entitled) … +1 = very high (sincere, fair, modest, unassuming).
   - **Agreeableness (A):** −1 = very low (harsh, critical, stubborn, quick to anger) …
     +1 = very high (forgiving, gentle, patient, tolerant).
   - Offer a **"the text gives no information"** checkbox (scored as missing, not neutral).
3. **Recognition probe** (the linchpin): *"Have you encountered this character before
   (book, film, class, elsewhere)?"* → **yes / no / unsure**.
4. Optional one-line rationale: *"What in the text drove your ratings?"*

## 3. Quality control
- **Two embedded attention checks per rater** (explicit-instruction entries; the Colab
  inserts one in each half of the session). Exclude failers, `analyze_human.py`
  applies this on the raw rows, so a "no information" tick is not an escape.
- Exclude straight-lining (zero variance across characters) and below-time-floor sessions.
- Apply exclusions **before** analysis.

## 4. Export → analysis
Export to `responses.csv` with **one row per (rater, character)**:
```
rater_id,panel_id,condition,H,A_HEX,recognition,no_info
R001,C07,redacted,0.4,-0.6,no,false
```
- `condition` ∈ {redacted, named}; `H`,`A_HEX` ∈ [−1, 1]; `recognition` ∈ {yes,no,unsure};
  `no_info` ∈ {true,false}. (Most platforms export wide; a short reshape gets here.)
Then:
```
python analysis/analyze_human.py responses.csv     # H1 (synthetic r) + H2 (recognition split) + exclusions
```

## 5. What the result says
- **Main:** synthetic characters should give a **negative** consensus r(H, A_HEX) from
  text (~−0.4 to −0.74), humans measure the design; canonical will likely stay positive.
- **Recognition split (the payoff):** among canonical characters, do raters who
  **recognized** the character show **higher** fusion than those who did **not**?
  Recognized → fused = retrieval (the human cache); no difference = the fusion is in the
  text (halo). This is the within-human test LLMs cannot provide, the closing result.

## Validation
This pipeline was dry-run end-to-end with LLM agents standing in for humans
(`human_dryrun.py` → `analyze_human.py`); the plumbing and the analysis are verified. The
recognition split's "canonical, not-recognized" cell is sparse for LLMs (they recognize
almost every canonical character, that is the point); humans populate it.
