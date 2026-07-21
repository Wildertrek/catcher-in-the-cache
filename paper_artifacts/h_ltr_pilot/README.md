# H_LTR pilot (S2, the refuted dialogue leg)

Notebook 02 §9 reports the single-LLM-probe regime as two legs: a 1-turn dialogue
probe at `r = 0.28`, **refuted** against the pre-registered 0.30 floor, and the
broader utterance corpus at `r = 0.633`, passed. The second leg is computed live in
the notebook from `method_bakeoff_v4/bootstrap_per_method.csv` (M5, `ALL` row). This
directory supplies the first leg, which was previously cited but not shipped.

| file | what it is |
|---|---|
| `h_ltr_summary.md` | decision summary: P (APERTURE-injected) mean **r = 0.283** across 5 traits, n = 78; C (control) falsifier r = 0.177. Verdict: **H_LTR REFUTED**, reframed as a negative finding |
| `h_ltr_openai_summary.md` | the same pilot on a second provider |
| `per_trait_correlations.csv` | per-trait r behind the 0.283 mean |
| `per_team_correlations.csv` | per-team breakdown |

The paper rounds 0.283 to `r = 0.28`. Full per-observation records, the runner
(`run_h_ltr_pilot.py`) and the figure builder live in the private development repo;
what is here is sufficient to check the reported number.

**Note on notebook 02 §9:** that section currently `print()`s both legs as literals
rather than recomputing them. The 0.633 leg is verifiable against the committed
bootstrap CSV; the 0.283 leg is verifiable against `h_ltr_summary.md` here.
