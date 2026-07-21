# Experiment 1: The Three Bars, do the methods actually measure personality?

A plain-language explainer. No statistics background needed. If you only read one thing about
Experiment 1, read this.

## Why this experiment exists (the one-sentence version)
Before the paper can ask its real question, *when an LLM scores a character's personality, is it
**measuring** the traits from the text, or **retrieving** a memory of that famous character?*, it has
to first prove that the measuring tools work at all. A broken ruler makes every later measurement
meaningless. **Experiment 1 is the "is the ruler trustworthy?" check.**

It takes six different methods for scoring a character's OCEAN personality and runs each through
three increasingly hard tests, called **bars**. Only methods that clear the bars are trusted as
instruments in Experiments 2 and 3.

## The OCEAN, in one line
Every method outputs five numbers for a character, **O**penness, **C**onscientiousness,
**E**xtraversion, **A**greeableness, **N**euroticism (OCEAN), each on a scale from low to high.

## The six methods (the contestants)
Each reads a character's *evidence pack* (their quotes + description) and outputs an OCEAN score:
- **M1 Prototype**: training-free: just match the text to the nearest labeled example. The floor/baseline.
- **M2 Classifier**: a model trained to label each line, then averaged.
- **M3 Regressor**: turns the text into an embedding, then a simple linear model predicts the traits (the cheap, fast method).
- **M4 Consensus**: asks several frontier LLMs to rate the character and takes the median. The strongest.
- **M5 Probe**: a single held-out LLM, given the text with the character's **name removed**.
- **M6 SCPI**: retrieves the *k* most similar labeled characters and copies their scores.

## The three bars (three tests, hardest last)

### Bar 1: Does each method get the right answer? *(recovery / ground-truth)*
Compare each method's scores to our reference "ground truth" for the characters. We use three
yardsticks, not one, because any single one can be gamed:
- **MAE** (average error), lower is better; **0.30** is the pass line.
- **Pearson r** (does it put characters in the right *order*?), needed because you can get a low error
  just by guessing "average" for everyone. Ordering can't be faked that way.
- **CCC** (does it get the order *and* the scale right?).

**Result:** the multi-model **Consensus (M4) wins**: MAE **0.230**, r **0.77**, CCC **0.76**. Three of the
six clear the 0.30 line (M4, M3, M5). The training-free baseline (M1) floors at MAE **0.427** and, on
ordering, is no better than the weak classifier (r 0.145 vs 0.118), so you genuinely can't do this
without learning; naive text-matching captures almost no trait signal.

### Bar 2: Do independent methods agree with each other? *(convergent validity)*
If two *different* methods, say, an embedding-regressor and an LLM, independently land on the same
traits for a character, that's evidence they're picking up something **real about the character**, not
each method's private quirk. The formal version is the Campbell-Fiske multitrait-multimethod test:
methods should agree on the *same* trait (convergent) more than they blur *different* traits (discriminant).

**Result:** *three* method pairs agree on all five traits. But one of them, Regressor + Consensus , 
does **not** count as independent evidence, because the Regressor was *trained on* the Consensus's labels
(a student agreeing with its own teacher; their five traits agree at **0.83** on average, for exactly
that reason). The agreement that counts is between the two **cross-family** pairs, Regressor-Probe and
Consensus-Probe: their five traits agree at **0.65** and **0.68** on average, and even their *weakest*
single trait clears **0.59** and **0.55**. Those are the "least contaminated" pairs, and they carry the
convergent-validity claim.

### Bar 3: Do the methods agree with an *outside human* source? *(external validity)*
The hardest bar: compare the methods' scores to a completely independent, **non-LLM** yardstick, the
Open Psychometrics "Which Character" crowd ratings, where **~1.5 million people** rated fictional
characters, on the **60 characters that overlap** our corpus.

**Result:** **four of five traits validate externally.** Conscientiousness and Neuroticism validate
**directly**; Openness and Extraversion validate after a per-trait scale adjustment (their *ordering* is
right, the scale just needs re-centering). **Agreeableness fails**: and that failure is not a bug, it's
the paper's pivot: OCEAN Agreeableness is a muddled factor that mixes *warmth* with *honesty*, which
is exactly why the paper turns to **HEXACO**, the model that splits those apart.

## The at-a-glance figure (the three-bar dashboard)
Three panels, left to right = Bar 1, Bar 2, Bar 3. Green = clears the bar, red = fails (Bar 2 adds
amber for partial). In Bar 3, four traits are green and only **A** is red (marked "fails"). The dashed
line in Bars 1 and 3 marks MAE = 0.30.

## Why Experiment 1 matters, the setup for "the catch"
The bars prove the methods produce **real, trait-ordered, mutually-agreeing, externally-valid** scores.
But here is the pivot: **every character in this corpus is famous**: the models have read them all. So
clearing Bar 1 could mean the method *measured* the traits from the text, **or** *retrieved* them from
memory. Bar 1 cannot tell these two apart.

That is the entire reason Experiment 1 only certifies "the instrument works." Experiments 2 and 3 then
take that certified instrument and ask **which route a rating actually takes**: by testing it on
*invented* characters the models have never seen, where measuring and retrieving finally give different
answers.

## Honest fine print (what a careful reader should know)
- **Bar 3, Openness:** an earlier version of the figure mis-marked Openness as failing; it validates
  (rank-order r = 0.61, second-highest; MAE 0.27, below the line), corrected.
- **Bar 1 mixes evaluation regimes:** M3 is shown at its in-distribution error; its held-out (leave-one-
  book-out) error is higher. This matches the leaderboard table, but the honest generalization number for
  the regressor is the held-out one.
- **Bar 2's Regressor-Consensus pair is contaminated by design** (the regressor learned from the
  consensus), so its agreement is discounted; the cross-family pairs carry the convergent-validity claim.
