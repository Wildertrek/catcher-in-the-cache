# The Catch, Explained: How to Read the Hero Figure

> The paper's central claim, *LLMs retrieve, they don't measure*, lives
> in one figure (Fig. 6 of the paper, the paired-collapse scatter). This explainer
> walks through that figure in plain language: what each axis is, what the
> diagonal means, why every dot falling below it is "the catch," and why
> it matters for anyone building LLM personas.

![The paired-collapse scatter: per-rater H–A fusion on canonical
(in-cache) vs synthetic (out-of-cache) characters. All 25 raters fall
well below the y = x diagonal.](catcher_hero.png)

---

## The one-sentence version

Each dot is one LLM rater. The figure shows that the personality
"structure" these models appear to measure on famous literary characters
**largely evaporates when the same models rate characters that aren't in
their training data**, which is the signature of *retrieval from memory*,
not *measurement from text*.

---

## What this figure is, and what it is not

**It is a falsifier, not a leaderboard.** The figure asks one yes/no
question: does the H↔A fusion depend on whether the character is in the
training cache? The answer is yes, for all 25 raters. It does **not**
rank the models, and it does not show that any model measures personality
well. The synthetic characters were authored with H and A *anti*-correlated
(designed r = −0.74 in the released set, −0.39 in the initial batch most
raters scored; both published, see
[`synthetic_substrate_batches.md`](synthetic_substrate_batches.md)), so a
rater that genuinely measured them from the text would land below zero,
not at the fused +0.75. GPT-5's 0.007 means "no consistent relation
at all", which beats fusing but is not measurement. **No rater recovered the
designed structure.**

**Do not read the diagonal as the ideal.** This is the single most common
misreading, and it is an honest mistake: in most scatter plots a reader has
seen, calibration curves and predicted-vs-actual plots, the `y = x` line is
exactly where you *want* points to sit. Here it is the null being refuted.
A rater hugging the diagonal is not the most accurate one, it is the one
whose fusion is stimulus-invariant, which in this panel means it keeps
fusing H and A even on characters it has never seen. Gemini 2.5 Flash-Lite
is closest to the line (−0.091) and is the *worst* differentiator off-cache;
GPT-5 is farthest from it (−0.726) and the best. Closeness to the line
measures consistency, not accuracy.

---

## What is actually being measured

Two HEXACO personality factors that valid measurement is supposed to keep
**separate**:

- **H = Honesty-Humility**, sincerity, fairness, non-manipulation,
  modesty. The "is this character morally straight?" axis.
- **A = HEXACO Agreeableness**, patience, tolerance, gentleness. The
  "is this character warm / easy to get along with?" axis.

In personality theory (Wiggins; Ashton & Lee), these are two distinct
axes. The classic problem they identified: **OCEAN** Agreeableness
smushes them together, so a charming-but-corrupt villain scores
"agreeable" and the moral axis disappears. A *valid* measurement keeps H
and A apart.

The number we track is **|r(H, A)|**, within one rater, the absolute
correlation between its H scores and its A scores across the
characters it rated:

- **High |r| → the rater is fusing the two axes** (bad: it can't tell
  honesty apart from warmth).
- **Low |r| → it keeps them distinct** (good).

So every dot's position is "how badly does this rater fuse honesty with
agreeableness?", measured two different ways.

---

## The two axes of the figure

- **X-axis, canonical (in-cache) characters.** The rater's fusion score
  on famous literary characters (Elizabeth Bennet, Daisy Buchanan, …) that
  are *definitely in the model's training data*.
- **Y-axis, synthetic (out-of-cache) characters.** The *same rater's*
  fusion score on **constructed** characters, matched on genre, period,
  and role, but **absent from any training corpus**, and authored so that
  H and A are deliberately *decoupled*. (The characters came in two
  generation batches, an initial 22 and a released 20; each rater is scored
  on exactly what it saw. Details:
  [`synthetic_substrate_batches.md`](synthetic_substrate_batches.md).)

The only thing that changes between a dot's x and y position is **whether
the character lives in the training cache.** Same model, same prompt, same
HEXACO probe.

---

## Every element on the chart

| Element | What it means |
|---|---|
| **Dashed `y = x` diagonal** | The null hypothesis: "the fusion is a fixed quirk of the rater." If the H↔A fusion were just a rating-scale / response-style bias, it would be the *same* on cached and novel characters, so every dot would land *on* this line. **This is the line the result has to beat.** |
| **Every dot below the line** | For all 25 raters, fusion is much higher on cached characters than on novel ones. The fusion is *not* a fixed property, it switches off when the character is unfamiliar. |
| **Thin vertical "drop" lines** | Each connects a rater's spot on the diagonal down to its real point. Length = how much the fusion collapses off-cache. Long drops everywhere = a big, consistent effect. |
| **Gray dotted "0.30 floor"** | The pre-registered threshold for "real fusion." Because the line is drawn *horizontally*, it reads against the **y-axis only**: it shows that **14 of the 25 raters fall below 0.30 off-cache**. The companion claim that all 25 clear 0.30 *on-cache* is about the x-axis, and a horizontal line cannot show it (you would need a vertical line at x = 0.30). Gray, not red: red is reserved throughout the paper for "out-of-cache / fail". |
| **Dash-dotted line at x = 0.450** | The **human self-report anchor**: r = 0.4501, 95% CI [0.4389, 0.4617], from the Open-Source Psychometrics IPIP-HEXACO sample (n = 22,299 after validity filtering; committed as `paper_artifacts/pivot6_hexaco_atlas/ipip_persona/human_baseline_result.json`). The shaded sliver is that CI. Every judge-mode rater sits to its right. **Do not read this as "LLMs over-fuse and humans do not"** , see below. |
| **Black ✗ (mean)** | The average rater: **0.75 fusion on cached → 0.30 on novel.** The headline collapse. |
| **Stats box** | Δ = −0.447 (average drop), all 25/25 raters down, paired Wilcoxon W = 0, p_BH = 1.5×10⁻⁷. The p-value says "not noise"; the **Δ = −0.447** (3× the pre-registered threshold) carries the strength. |
| **Color *and* marker shape** | Provider family (Anthropic, OpenAI, Google, …), double-encoded so the figure survives greyscale printing and color-vision deficiency. The effect holds across *every* vendor, not one model's quirk. |
| **The 9 named dots** | Callouts, i.e. illustrative flagships chosen to span the range: the largest collapse (GPT-5, -0.726), the second largest (DeepSeek R1, -0.680), the smallest (Gemini 2.5 Flash-Lite, -0.091), and the highest on-cache fusion (Llama 3.3 70B, 0.966). They are not a separate category; the other 16 raters behave the same way. |

---

## Three things the chart does not say

**1. Low `|r|` does not mean "backwards."** The axes are *absolute*
correlations, so direction is discarded. A rater near the bottom is not
scoring the characters in reverse; it simply shows **no consistent linear
relation between H and A in either direction**. The signed story is
genuinely messier and is handled separately in the paper (§4.3): one panel
recovers +0.83 on the synthetic set, a cheaper three-model panel recovers
-0.45, which is why the load-bearing evidence is the *magnitude* collapse
plus the subject-mode manipulation check, not the from-text sign.

**2. The human line is a mode reference, not a human-vs-LLM verdict.** The
0.450 anchor is a *between-person self-report* correlation: across 22,299 people,
high scorers on Honesty-Humility also score somewhat high on Agreeableness. The
axes here are *judge mode*: one model rating 60 characters, and how much its two
scores track each other. Those are different measurements, and the mode matters
more than the species.

When the comparison **is** mode-matched, the gap largely disappears. Administering
the identical 240-item IPIP-HEXACO to three frontier raters in subject mode
(answering *as* the character) gives a canonical r(H, A) of **+0.449**, level with
the human **+0.450** (notebook `07_ipip_human_anchor.ipynb`); the paper's
six-model check reports the same direction, judge-mode median 0.79 attenuating to
**0.41** in subject mode against the human 0.45.

So the honest reading of the horizontal gap in Fig 6 is *judge mode fuses more
than subject mode*, not *LLMs fuse more than people*. What survives either way is
the vertical collapse: in subject mode the same raters go from +0.449 on canonical
characters to **-0.332** on synthetic ones, actually recovering the designed
decoupling. The cache effect is the robust finding; the human comparison is
scale-setting.

**3. Chance is not zero, and the two axes have different sample sizes.**
The x coordinate is a correlation across up to **60** canonical characters;
the y coordinate is across roughly **20** synthetic ones (14 to 22 per rater,
after parse failures and the two-batch history). At n = 20, two genuinely
unrelated variables still produce `|r| ~ 0.185` on average by chance alone
(for n = 60 it is ~0.104). So the synthetic mean of **0.30 is above chance,
but not enormously so**. That is not a hole in the result, it is exactly
the "generic coupling prior" the paper describes: a weakened, character-
independent tendency that survives when there is no memorized prior left
to retrieve. Readers who compute the chance floor themselves should find
the paper already accounts for it.

---

## Why the pattern means "retrieval, not measurement"

If a model were genuinely **reading personality out of the text**, its
fusion score should depend on the actual characters. On the synthetic set
, authored to keep H and A apart, a real measurer should show *low*
fusion, and it does. But on canonical characters it shows *high* fusion
that matches the well-known OCEAN conflation.

The cleanest explanation: on famous characters the model isn't reading the
text in front of it, it's **retrieving a memorized prior** built during
pretraining, and that prior carries the cultural conflation of the two
axes. Off-cache, there's no prior to retrieve, so the fusion drops. **That
gap is "the catch."**

One honest detail in the figure: the synthetic mean is **0.30, not 0**, 
so genuine text-measurement isn't *absent*, it's just *dominated* by
retrieval on cached characters.

---

## The interesting twist in the individual dots

- **Strongest collapses (drop almost to zero):** GPT-5 (0.73 → 0.01),
  Gemini 2.5 Pro (0.65 → 0.02), Claude Opus 4.6 (0.71 → 0.09). For these
  raters the fusion is *almost entirely* cache-driven: with nothing to
  retrieve, the two axes come apart. Note this is **not** a capability
  effect. RQ6.3 pre-registered that test and it came back null (Spearman
  ρ = −0.165 against Arena rank, 95% CI [−0.54, +0.27]), and the pattern
  is visibly not a capability ordering: older GPT-4o snapshots sit at the
  residual-high end while GPT-5 sits at the collapsing end, and GPT-5.2
  starts *higher* than GPT-5.
- **Residual-high (stay above the floor off-cache):** GPT-4o (0.92 →
  0.62), Gemini 2.5 Flash-Lite (0.74 → 0.65), Claude Haiku (0.79 → 0.57).
  These keep fusing the axes even on novel characters, for them more of
  the fusion is an input-independent tendency.

Either way, **all 25 raters fall well below the diagonal**, so for every
model the fusion is substantially cache-driven.

---

## Every rater's score (all 25 nodes)

The figure keeps only a few labels for legibility. Here is every node, so you
can identify any dot. Sorted by canonical (in-cache) fusion, high to low.
Reproduce or re-plot interactively in the Colab notebook
[`09_catcher_in_the_cache.ipynb`](../../notebooks/09_catcher_in_the_cache.ipynb);
machine-readable source:
[`synthetic_vs_canonical.csv`](../../paper_artifacts/pivot6_hexaco_atlas/synthetic_vs_canonical.csv).

| Rater | Family | Canonical \|r\| | Synthetic \|r\| | Delta |
|---|---|--:|--:|--:|
| Llama 3.3 70B | Meta | 0.966 | 0.430 | -0.536 |
| GPT-4o (2024-08) | OpenAI | 0.920 | 0.623 | -0.297 |
| GPT-4o (2024-05) | OpenAI | 0.918 | 0.402 | -0.516 |
| Llama 3.1 70B | Meta | 0.907 | 0.378 | -0.528 |
| Llama 4 Maverick | Meta | 0.893 | 0.546 | -0.348 |
| Qwen 2.5 72B | Qwen | 0.806 | 0.539 | -0.267 |
| GPT-5.2 | OpenAI | 0.806 | 0.248 | -0.558 |
| Claude Sonnet 4 | Anthropic | 0.796 | 0.253 | -0.543 |
| Claude Haiku 4.5 | Anthropic | 0.789 | 0.567 | -0.222 |
| Claude Sonnet 4.5 | Anthropic | 0.777 | 0.268 | -0.509 |
| DeepSeek R1 | DeepSeek | 0.777 | 0.097 | -0.681 |
| Mistral Large 2411 | Mistral | 0.765 | 0.153 | -0.612 |
| Gemini 2.5 Flash-Lite | Google | 0.742 | 0.651 | -0.091 |
| GPT-5 | OpenAI | 0.733 | 0.007 | -0.726 |
| o4-mini | OpenAI | 0.726 | 0.359 | -0.367 |
| Command A | Cohere | 0.719 | 0.529 | -0.190 |
| Claude Opus 4.6 | Anthropic | 0.712 | 0.085 | -0.626 |
| Gemma 4 26B | Google | 0.699 | 0.290 | -0.409 |
| DeepSeek V3.1 | DeepSeek | 0.678 | 0.161 | -0.518 |
| Grok 4.3 | xAI | 0.667 | 0.148 | -0.519 |
| Qwen3 32B | Qwen | 0.646 | 0.379 | -0.267 |
| Gemini 2.5 Pro | Google | 0.645 | 0.022 | -0.623 |
| Gemini 3.1 Pro | Google | 0.574 | 0.200 | -0.374 |
| Gemini 3 Pro | Google | 0.573 | 0.182 | -0.391 |
| Gemini 2.5 Flash | Google | 0.553 | 0.089 | -0.464 |
| **Mean (n=25)** | | **0.752** | **0.304** | **-0.447** |

All 25 raters decreased; the smallest collapse is Gemini 2.5 Flash-Lite
(-0.091), the largest is GPT-5 (-0.726).

## The signed fusion: retrieval, not just attenuation

The table above reports absolute $|r|$, which shows the collapse but cannot
on its own discriminate retrieval from measurement. Because the synthetic
characters are authored with H and A anti-correlated (designed
$r = -0.74$), faithful measurement would recover a *negative* fusion
($r \approx -0.74$) while retrieval imposes the *positive* fusion seen on
canonical characters. The signed within-rater correlation decides between them:

| Substrate | signed $r(H, A_{\mathrm{HEX}})$ |
|---|---|
| Canonical (in cache) | **+0.75** |
| Synthetic (out of cache) | **+0.23** (positive in 20 of 25 raters) |
| Designed truth | $-0.74$ (released set; $-0.39$ in the initial batch) |

The synthetic signed mean is **+0.23** (95% CI [0.12, 0.34], sign test
$p = 0.004$), positive, not the $-0.74$ faithful measurement predicts. The
positive sign also rules out simple attenuation: independent noise on a true
$-0.74$ signal would shrink the magnitude toward zero from the negative side,
never flip the mean positive. On out-of-corpus characters there is no specific
entry to retrieve, so the residual is a weakened, *generic* H-A coupling prior
the raters impose on any character they cannot place, not text-driven
measurement. Reproduce with
[`panel25/compute_panel25.py`](../../paper_artifacts/pivot6_hexaco_atlas/panel25/compute_panel25.py)
→ `panel25/panel25_results.json` (the 25-rater panel the paper reports). The parent
`compute_signed_r.py` → `signed_r_results.json` is the superseded 26-rater run.

## Why this figure matters

1. **It's the dual of Meyer et al. (2026).** They showed that when an LLM
   is the *subject* of a personality test, its answers are dominated by a
   response bias. This figure shows that when an LLM is the *instrument*
   measuring someone else's personality, its apparent accuracy is
   dominated by cache retrieval. The diagonal is literally drawn as their
   alternative explanation, and the data refute it, because a fixed bias
   cannot switch off when only cache membership changes.
2. **It's the stepping stone to persona deployment.** Any system that
   initializes a persona by asking an LLM to "rate this character"
   inherits exactly this: on a known archetype (Hero, Ruler, Caregiver)
   it retrieves a memorized prior; on a *novel* persona it cannot be
   trusted. That is the whole motivation for a cache-free instrument.

In short: the figure turns a subtle, abstract claim, "LLMs retrieve
rather than measure", into something you can see in one glance: **25
dots, all collapsed far below the line that says 'this is real.'**

---

## Related explainers

- **How the synthetic characters were built and why the design holds:**
  [`why_synthetic_chars.md`](why_synthetic_chars.md)
- **The two generation batches (22 initial / 20 released) and who scored which:**
  [`synthetic_substrate_batches.md`](synthetic_substrate_batches.md)
- **Why the panel is 25 raters (and where 26/27/28 came from):**
  [`panel_roster_history.md`](panel_roster_history.md)
- **Why the paper is called "The Catcher in the Cache":**
  [`title_explainer.md`](title_explainer.md)
- **H vs OCEAN Agreeableness vs HEXACO Agreeableness and the rest of the battery alphabet soup:**
  [`battery_zoo.md`](battery_zoo.md)
- **The stats (Wilcoxon paired, BH-FDR, ICC):**
  [`psychometrics_glossary.md`](psychometrics_glossary.md)
- **How the recurring counts reconcile (the 25-rater panel, 9 families, etc.):**
  [`numbers_decoder.md`](numbers_decoder.md)
