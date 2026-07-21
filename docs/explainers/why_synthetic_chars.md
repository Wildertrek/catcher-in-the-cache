# Why Synthetic Characters, The Matched-Substrate Design

> Note: the synthetic set was generated in two batches (an initial 22 and a
> regenerated, released 20). Which raters scored which, and why the result does
> not depend on it, is in [`synthetic_substrate_batches.md`](synthetic_substrate_batches.md).

> The paper's load-bearing falsifier (RQ6.9) pairs 60 canonical
> literary characters against 20 *synthetic* literary characters. If
> "synthetic characters" sounds like "we just made some up," this
> explainer says what design constraints they had to meet, how they
> were generated, and why they support the retrieval-vs-measurement
> diagnosis they support.

---

## The design problem

The RQ6.1 finding, all 25 LLM raters fusion H and A_HEX into
$|r| = 0.75$ on canonical characters, admits two competing readings:

1. **Measurement reading.** LLMs really *can* infer the H↔A_HEX
   fusion from text, and the consistent value across 25 independent
   raters reflects a genuine psychometric property of literary
   characters.

2. **Retrieval reading.** LLMs have memorized character priors from
   training data (criticism, summaries, fan analysis), and the
   consistent fusion reflects shared retrieval from a shared
   training corpus, not measurement.

These readings have identical predictions on canonical characters
(both predict $|r| \approx 0.75$). To discriminate them, we need a
substrate where the two readings predict *different* outcomes.

**Synthetic characters do exactly that.** A character that cannot be
in any LLM's training data has no retrievable prior. Under the
measurement reading, $|r|$ should be similar. Under the retrieval
reading, $|r|$ should drop sharply.

Observed drop: $\Delta = -0.447$ ($3\times$ the pre-reg threshold).

The *signed* analysis sharpens this. The synthetics are authored at
$r = -0.74$, so faithful measurement would recover a negative fusion
while retrieval imposes the positive canonical fusion. The observed
synthetic signed $r = +0.23$ (positive in 20 of 25 raters), not the
$-0.74$ measurement predicts, so the residual is retrieval-direction,
not measurement. The positive sign also rules out simple attenuation.
See [`the_catch_explained.md`](the_catch_explained.md) and
[`compute_signed_r.py`](../../paper_artifacts/pivot6_hexaco_atlas/compute_signed_r.py).

---

## What "synthetic character" had to mean

A synthetic character serves the design only if it satisfies a
specific set of constraints:

1. **Absent from training corpora of all 25 panel raters.**
   Otherwise the rater has retrievable prior and the falsifier
   collapses to the canonical substrate.

2. **Readable as a literary character.** A random-string name and
   garbled dialogue would yield $|r| \approx 0$ trivially, the
   collapse to noise wouldn't be informative because the rater
   wouldn't have anything to measure. The synthetic chars must
   produce coherent, OCEAN/HEXACO-codable input.

3. **Matched in genre, period, register to canonical anchors.** If
   the synthetic chars all read as modern dialogue while the
   canonical chars are 19th-century novel-form, any observed drop
   could be a genre confound, not a substrate confound.

4. **Matched in role / archetype.** If the canonical chars are all
   protagonists and synthetic chars are all minor characters, the
   drop could be a mention-count or evidence-density confound.

5. **Out-of-corpus, not retrievable.** The chars must occupy a region
   no panel rater could have memorized. They were LLM-drafted (Claude
   Opus 4.6), both prose and v0 targets, under a human-designed
   H↔A_HEX decoupling constraint (designed $r = -0.74$). LLM authorship
   is acceptable for the substrate falsifier because the falsifier reads
   the *text* (the decoupling lives in the prose, demonstrated by the
   observed collapse), and out-of-corpus placement is verified
   independently by embedding distance, not by authorship.

6. **Pre-data lock.** The synthetic char set must be locked before
   any synthetic-substrate ratings are collected, to rule out
   selection-on-outcome.

The full synthetic-char generation pipeline satisfies all six.

---

## How they were generated

The 20 synthetic literary characters were LLM-drafted (Claude Opus
4.6), both the prose evidence packs and the v0 OCEAN-6 / HEXACO
targets, under a human-designed H↔A_HEX decoupling constraint
(designed $r = -0.74$). Process summary:

1. **Anchor selection.** Each synthetic char is anchored to a
   canonical character in the comparison set (matched in genre, period,
   role).
2. **Trait spec.** A target OCEAN-6 / HEXACO profile is committed
   for each synthetic char *before* any LLM rating is collected. This
   profile is the synthetic-side ground truth.
3. **Drafted evidence pack.** Each synthetic char gets ~10–20
   utterances + a short biographical context, totaling ~2K tokens
   (matched to canonical character evidence-pack sizes), drafted to
   convey the decoupling so the collapse is genuinely carried by the
   text.
4. **Review.** Each synthetic char was reviewed for genre / period /
   register match against its anchor.
5. **Pre-data lock.** The set was committed to the private research repository,
   timestamped, before the LLM panel was queried in synthetic mode.

Because the characters are LLM-drafted, the decoupling cannot rest on
authorship; it rests on (a) the text, the bipolarity collapse is
observed directly when raters read the evidence packs, and (b)
independent verification that the chars sit out-of-corpus by embedding
distance, not by any claim about who wrote them.

The synthetic char specs ship in
`paper_artifacts/pivot6_hexaco_atlas/synthetic_characters_substrate_v0.json`
in the companion repo (the anchor, target OCEAN-6 / HEXACO, evidence
pack, and pre-data lock timestamp per character); the period-matched
register-robustness set is in
`paper_artifacts/pivot6_hexaco_atlas/register_matched/`.

---

## What we matched, and what we did not

**Matched:**

| Dimension | How |
|---|---|
| Genre | Each synthetic char anchored to a canonical char in the same genre slot |
| Period / register | Drafted in the prose style of the anchor period |
| Role | Protagonist-tier chars matched to protagonist anchors; supporting chars to supporting anchors |
| Evidence-pack token count | ~2K tokens to match canonical median |
| Target trait coverage | Synthetic OCEAN-6 spec covers the same range observed in canonical |

**Not matched (by design):**

| Dimension | Why not |
|---|---|
| Literary fame | The whole point: synthetic chars have *zero* fame |
| Training-data presence | The whole point: synthetic chars are absent from training corpora |
| Number of published critical-analysis sources | Synthetic chars have none |

The unmatched dimensions are exactly the dimensions the falsifier
tests. The matched dimensions are the confound controls.

---

## Why 20 (not 60 or 6)

The synthetic-substrate $n$ was chosen by a power calculation against
the pre-reg $|\Delta| \geq 0.15$ threshold:

- Smallest detectable effect size $|\Delta| = 0.15$
- Within-rater paired design (each rater is its own control)
- Bootstrap CI half-width target: $\leq 0.10$ on individual rater $|r|$
- 25-rater paired Wilcoxon at $\alpha = 0.05$ requires $\geq 18$ pairs
  to detect $\Delta = 0.15$ at 80% power against a within-character
  variance of $\sigma^2 \approx 0.05$

$n = 20$ exceeds the power requirement with a margin. The synthetic-set
size was locked before the threshold-and-power audit at A8/A11.

---

## What if the LLM raters could see through the design?

The honest concern: maybe an LLM rater can spot a synthetic char ("oh,
this isn't Bennet, this is some made-up thing") and rate it
differently for that reason, not because of retrieval failure.

This is checked in the following ways:

1. **Out-of-corpus placement by embedding distance.** Rather than
   relying on authorship, out-of-corpus placement is verified
   independently with the cache-membership gauge: the synthetic chars'
   median embedding distance (0.41) sits below the canonical 5th
   percentile (0.61), placing them outside the region of memorized
   canonical priors. A formal authorship-detection probe (asking raters
   to classify each character as canonical or synthetic from the
   evidence pack alone) is queued; its backing artifact is not yet
   populated, so no accuracy result is claimed here.

2. **Within-rater consistency.** If raters were systematically
   "downweighting" synthetic chars rather than measuring them, we'd
   see lower within-rater consistency on synth-side OCEAN-6
   predictions. We don't.

3. **Cross-rater agreement.** Cross-rater agreement on synthetic
   chars is lower than on canonical chars, exactly as the retrieval
   reading predicts. The measurement reading predicts equal agreement.

---

## What the design *can't* rule out

Honest limitations:

- **Drafting source.** The 20 chars were LLM-drafted (Claude Opus 4.6)
  under a single human-designed decoupling constraint. A
  human-authored or multi-source character set, with human-judged
  labels, would be stronger and is the F3 follow-up's purpose.
- **Period coverage.** Anglo-American + translated European, matched
  to the canonical corpus. Non-Western synthetic chars not included.
- **Anchor density.** Some canonical chars get multiple synthetic
  anchors; some get none. The pairing is per-character, not
  perfectly stratified.

These limitations are recorded in §6 of the paper and motivate the
**F3 follow-up** (human-rater HEXACO panel: a $n=30$ Prolific panel
rating both canonical and synthetic chars to anchor the LLM panel to
human raters).

---

## Bottom line

The synthetic-substrate design is the load-bearing experiment of the
paper. Its scientific weight rests on the matched-design constraints
and the pre-data lock. The observed drop of $\Delta = -0.447$
(three times the threshold) is what a retrieval reading predicts and
a measurement reading does not.

---

## Further reading

- The full RQ6.9 PRIOR_DRIVEN section: §4.3 of the paper
- The 25-rater panel and how the counts reconcile: [`numbers_decoder.md`](numbers_decoder.md)
- The pre-registration structure: [`rq_decoder.md`](rq_decoder.md)
- The activation-probe parallel finding (substrate signature in
  hidden states): [`activation_probe_for_psychologists.md`](activation_probe_for_psychologists.md)
