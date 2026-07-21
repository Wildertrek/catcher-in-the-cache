# The coupling prior (cached reproduction)

Rating 20 synthetic (out-of-corpus) characters from their **name alone** yields a
strongly fused `r(H, A_HEX) ~ +0.83` -- on characters that do not exist -- while rating
the same characters from their **text** recovers the designed anti-correlation `~ -0.45`.
The fusion is a generic coupling prior summoned by the absence of evidence, not a
retrieved memory.

- `responses_holistic.csv` -- cached holistic H / A_HEX ratings (3 providers x 3 personas
  x 40 characters x 3 conditions: name-only / text-redacted / text+name).
- `panel_kind.json` -- panel_id -> canonical | synthetic.
- `recompute_coupling.py` -- recomputes the 2x3 table + bootstrap CIs at `$0`
  (`python recompute_coupling.py`).

Providers: Claude Haiku 4.5, GPT-4o-mini, Gemini 2.5 Flash. A frontier-rater replication
is the planned camera-ready step.

## Figure (cut from the paper)

The coupling-prior figure was cut from the paper (v13) to save space; the finding is kept
in prose (Experiment 3, "The coupling prior: fusion without evidence"). The figure lives in
the companion at `docs/figures/coupling_prior.pdf`, regenerated from the numbers that
`recompute_coupling.py` produces.
