# The Title, "The Catcher in the Cache"

> One explainer for the title, the cache metaphor, and the
> Salinger reference. For readers who got the joke and want
> the full setup, and for readers who didn't and want to know
> what they missed.

---

## The reference

*The Catcher in the Rye*, J.D. Salinger, 1951. Holden Caulfield's
inner monologue across three days in late-1940s New York, told in
distinctly American adolescent prose. One of the most-taught novels
in American secondary education, in continuous print for 75 years.

Holden gets the title from a mis-remembered Robert Burns lyric:

> *If a body catch a body coming through the rye* (Burns, 1782)

He pictures himself standing at the edge of a cliff above a field
of rye, where children play. His job is to catch them when they run
too close to the edge. "I'd just be the catcher in the rye and all."

---

## The metaphor for this paper

The paper's central diagnosis is that modern LLMs, when asked to rate
the personality of a canonical literary character, are largely
*retrieving* a memorized character prior from training data rather
than measuring traits from the text in front of them. Where is the
memorized prior stored? In the LLM's internal representation of its
training corpus, what we shorthand as **the cache** (using "cache"
in the loose computational sense of "internal store from which
information is retrieved at inference time").

So:

- **"The Cache"** = the LLM's internal representation of its training
  corpus, encoded in its weights, accessible at inference time.
- **"The Catcher"** = the two-part diagnostic apparatus this paper
  introduces: the substrate falsifier (RQ6.9) + the activation probe
  (§4.4). These are the tools that *catch* retrieval-vs-measurement
  in the act.

The double meaning the title trades on: **the cache catches** (canonical
characters are pre-caught, before the text even reaches the rater) and
**we built a catcher for the cache** (a diagnostic that exposes the
retrieval signature).

---

## The Holden parallel, for readers who want one

Holden's project is to catch children before they fall off the cliff.
The paper's project is to catch researchers and practitioners before
they fall off the cliff of confusing retrieval with measurement , 
specifically, before they deploy LLM-based personality measurement to
novel characters where the retrieval prior doesn't exist and the
apparent accuracy on canonical chars won't transfer.

There is also a quieter parallel: Holden Caulfield himself is one of
the most-memorized literary characters in any English-trained LLM's
corpus. The title-note in the paper makes this explicit:

> *J.D. Salinger's* The Catcher in the Rye *(1951) is not among the
> 76 books in our pipeline corpus, but Holden Caulfield is in every
> LLM rater's training cache, which is precisely the phenomenon this
> paper studies. We use "cache" to mean the LLM's internal
> representation of its training corpus, encoded during pretraining
> and retrieved at inference time.*

So the title makes a self-referential point: *the very character whose
name the title invokes is the canonical example of the phenomenon the
paper diagnoses*. Holden is in the cache; the paper is the catcher.

---

## Why "cache" and not "memory" or "training data"

We considered several alternatives:

| Candidate | Why we didn't use it |
|---|---|
| "memory" | Ambiguous with KV-cache, working memory, attention memory in transformers |
| "training data" | Too literal; obscures the inference-time retrieval mechanism |
| "weights" | Too narrow; the retrieved structure is distributed across components |
| "prior" | Too technical; doesn't ring in a title |
| "corpus" | Refers to the external source, not the internal trace |
| **"cache"** | Captures the computational sense ("stored for retrieval"), reads idiomatically in the title, and supports the Salinger reference |

The choice is loose with respect to formal cache hierarchy ("cache"
in CPU architecture is L1/L2/L3 main-memory). In the paper's usage,
"cache" is **the LLM's internal representation of its training
corpus, available at inference time as if from a memorized lookup
table.** The companion repository documents the mechanics in
`CATCHER.md` §4.1.

---

## The footnote-in-titlepage you saw

The first footnote attached to the title says:

> *J.D. Salinger's* The Catcher in the Rye *(1951) is not among the
> 76 books in our pipeline corpus, but Holden Caulfield is in every
> LLM rater's training cache, which is precisely the phenomenon this
> paper studies. We use "cache" to mean the LLM's internal
> representation of its training corpus, encoded during pretraining
> and retrieved at inference time. The companion repository documents
> the mechanics in
> [CATCHER.md §4.1](../../CATCHER.md).*

That footnote IS the title explainer in compressed form. This file
expands it for readers who wanted more setup.

---

## What the title is *not* doing

A few things we want to forestall:

- **Not claiming Salinger had anything to do with LLM personality
  measurement.** The reference is a pun, not a citation.
- **Not implying** Holden Caulfield's adolescent narrator-style is
  somehow a model for LLM behavior. Holden is the canonical
  *example* of a character whose personality LLMs would
  retrievally-rate; the title doesn't analogize the LLM to Holden.
- **Not claiming the cache concept is new.** "Caching" in the
  retrieval-augmented-generation sense, in the memorization sense,
  and in the next-token-distribution sense are all known. We are
  applying it descriptively to a measurement-validity problem.

---

## For readers who want the alternative titles we considered

Working titles (from the git history):

| Title | Tradeoff |
|---|---|
| "Retrieval, Not Measurement: A 25-Rater Panel of LLM Personality on Literary Characters" | Direct, dry, no hook |
| "The Catcher in the Cache: LLM Personality Rating on Canonical and Synthetic Literary Characters" | Hook + descriptive subtitle, but long |
| "The Catcher in the Cache: A 25-Rater Audit of LLM Personality on Literary Characters" | Methodology-anchored subtitle |
| **"The Catcher in the Cache: Retrieval, Not Measurement, in LLM Personality Inference"** ← active | Hook + the thesis-preserving subtitle. The chosen form. |

The trade we made: hook + thesis in the subtitle. The methodology
("25 raters", "canonical + synthetic", "60 + 20") lives in the
abstract and §1, where it belongs.

---

## For non-academic readers

If you came here from a science journalist's article or a Twitter
thread, the takeaway in one paragraph:

LLMs trained on the internet have memorized famous literary
characters in detail, their dialogue, their plots, the critical
analyses of them. When you ask an LLM "what is Elizabeth Bennet's
personality?", the LLM is doing something closer to *looking it up*
than to *figuring it out from the text*. We can prove this by
asking the LLM about characters that don't exist in any training
corpus, characters we wrote ourselves for this experiment, and
showing that the LLM's "measurement" gets much noisier in a specific,
predictable way. The title is a pun on a Salinger novel; the cache
metaphor describes where the memorized character lives inside the LLM.
