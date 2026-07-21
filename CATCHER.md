# The Catcher in the Cache: A Companion to the Title

> *"People always think something's all true."*
> ~ Holden Caulfield, in J.D. Salinger, *The Catcher in the Rye*

This document explains the title of the paper:

> **The Catcher in the Cache: Retrieval, Not Measurement, in LLM Personality Inference**

It is for readers who want to know why the title is a Salinger allusion, what alignment we claim between the novel and the paper, what alignments we *don't* claim, where the literary callbacks are planted in the manuscript, and why the novel itself is not in our 75-work comparison corpus.

---

## 1. *The Catcher in the Rye*: the novel in one paragraph

Sixteen-year-old Holden Caulfield narrates three days in New York after being expelled from Pencey Prep, his fourth boarding school. He wanders the city, encounters phonies and one or two genuine people, fails to connect with anyone, has a near-breakdown after a visit to a former teacher, watches his younger sister Phoebe ride a carousel, and ends the novel in a sanatorium where he has been telling the story all along. The book's central preoccupations are **phoniness vs. authenticity** (Holden's word for the performed-rather-than-genuine), **the catcher metaphor** (Holden's fantasy of standing at the edge of a cliff in a field of rye and catching children before they fall, preserving innocence), **unreliable narration** (Holden filters everything through his own biases), and **retrospective recall** (the whole novel is Holden telling, not living, the story).

## 2. Our paper in one paragraph

APERTURE-the-system tests six methods (M1–M6: a training-free cosine-to-anchors prototype, random-forest classifier, random-forest regressor on embeddings, multi-provider LLM consensus, single held-out LLM probe, $k$-NN retrieval) on 562 literary characters scored against a five-source-type weighted ground-truth taxonomy (eleven weighted entries), evaluated under a three-bar diagnostic protocol (per-method ground-truth recovery, corrected Campbell-Fiske MTMM, external concurrent validity). Four of five OCEAN traits clear the diagnostic; Agreeableness fails Bar 3. A cross-rater HEXACO probe surfaces the deeper finding: when 25 frontier LLM raters score canonical literary characters, the resulting rating signal is dominated by **retrieval against memorized canonical-character priors** rather than text-based **measurement**. The synthetic-substrate test (the cross-rater panel RQ6.9 PRIOR_DRIVEN) is the falsifier: take away the canonical priors and the within-rater H↔A fusion drops by Δ = -0.447, and the signed fusion flips from the designed -0.74 to +0.23 rather than recovering it. A representational probe (V6) inside open-weight models is consistent with the fusion living in early-layer encodings (suggestive corroboration; the linear probes are weak and a non-linear refit did not converge). The mode-dissociation extension shows the bipolarity fusion persists in subject-mode self-report with ~48% attenuation, so the residual is partly representational. The headline: **LLM personality inference on canonical literary characters is largely retrieval, not measurement; a representational correlate at the activation and subject-mode levels corroborates the result rather than rescuing it.**

## 3. The four alignments: why the title is doing real work

### 3.1 Phoniness ↔ Retrieval-not-measurement (the thesis-level alignment)

Holden's central insight: what people *present* (their behavior) doesn't match what they *are*. He calls this phoniness.

Our paper's central finding: what LLMs *present* (a rating that looks like measurement) doesn't match what they're *doing* (retrieving cached profiles). The output is "phony" in Holden's precise sense, a fluent surface masking a different mechanism.

This is the strongest alignment. It earns the title.

### 3.2 The catcher's job ↔ the diagnostic's job (the methodology-level alignment)

Holden's fantasy is to catch children before they fall off the cliff of adulthood. Our diagnostic protocol, three-bar measurement-quality bars plus the substrate Catcher Test plus the activation probe, wants to catch LLMs before they pass retrieval off as measurement, so practitioners don't fall off the cliff of deploying a misunderstood mechanism downstream.

### 3.3 Retrospective recall ↔ LLM retrieval (the mechanism-level alignment)

Holden tells the whole story from a sanatorium, he isn't living the experiences, he's recalling them. The LLM rater isn't reading the evidence pack and inferring trait scores in the moment, it's recalling cached canonical-character data. Both narrators sound authoritative; both are systematically distorted by memory.

### 3.4 The meta-self-reference (the cleverest part)

Holden Caulfield is in every contemporary LLM's training cache. *The Catcher in the Rye* is one of the most-discussed novels in any web-scraped corpus. The paper studies what's cached in LLMs' training data and how that cache distorts rating-time inference.

**The title is literally an instance of the phenomenon the paper documents.** When a reader Googles the title and reads about Holden, they are demonstrating the paper's claim: a canonical character has a cached profile that surfaces immediately on name-match. The LLM does the same thing.

## 4. How the Catcher works (the apparatus that catches the phony at the edge)

In *The Catcher in the Rye*, Holden wants to stand at the edge of a cliff in a field of rye and **catch the children before they fall**, and the word that runs through the novel is **"phony."** That is exactly the paper's shape. The **Cache** is the rye field, the model's memorized priors for canonical characters. Its **edge** is the boundary between the characters a model has memorized (in-cache) and those it has not (out-of-cache). The **fall** is a character getting a *phony* reading: a retrieved prior dressed up as a measurement. The **Catcher** is the apparatus that catches the model in that phoniness, and catches the out-of-cache characters at the edge before they fall.

It catches in three ways, strongest first:

1. **The substrate falsifier** *exposes the phoniness*: confident fusion on cached characters, collapse on 20 synthetic characters built to lie past the edge (mean |r(H,A)| 0.75 → 0.30; signed fusion +0.23, not the designed -0.74). This is the catch.
2. **The cache map / cache-membership gauge (SCPI)** *stands at the edge*: in embedding space, in-cache and out-of-cache characters separate cleanly (canonical median similarity 0.87 vs synthetic 0.41, no overlap), the cache has empty regions no canonical character occupies, and the gauge flags out-of-cache characters before a deployed system hands them a retrieved prior. This is Holden's catch, at the boundary, before the fall.
3. **A representational probe inside the open-weight models** is a *weaker corroboration*: the fusion is already present in the early/shallow encodings and the model separates the axes with depth (suggestive; the probes are weak, see §4.5).

The next subsection unpacks what is being caught: "the Cache".

### 4.1 What we mean by 'the Cache'

In standard computing, a *cache* is fast memory of frequently-accessed content. In this paper's title, **"the Cache" means the LLM's internal representation of its training corpus**: the statistical regularities and content the model encoded during pretraining and can retrieve at inference time.

For canonical literary characters specifically, the cache contains: Wikipedia plot summaries (Elizabeth Bennet's Wikipedia entry runs to roughly 6,000 words; Hamlet's to over 10,000); SparkNotes / CliffsNotes / eNotes character analyses with explicit personality descriptions; literary-criticism trait readings published in peer-reviewed journals; classroom essay corpora that quote and analyse canonical characters; fanfic discussions and trait debates; TV / film adaptation reviews. These artifacts entered the training data through standard web-scraping pipelines (Common Crawl, OpenWebText, ePUB collections, fan wikis).

The cache does not live in the LLM as an explicit lookup table, it lives as patterns distributed across the model's weights. But functionally, for a high-frequency literary entity like Elizabeth Bennet, querying the model with her name plus a personality-rating prompt is *equivalent to* a cache lookup against a memorized profile. The LLM is not (only) inferring traits from the in-context text the prompt supplies; it is (also) retrieving from the cached representation of everything it learned about Elizabeth Bennet during pretraining.

**The substrate falsifier (the catch, §4.2) does not read the cache directly**: we do not have access to LLM training data, and even if we did, the cache lives in weights rather than text. Instead the falsifier forces a *cache miss*: it asks the model to rate 20 synthetic characters with no Wikipedia page, no SparkNotes entry, no fanfic, no published criticism, no scholarly trait reading. When the cache cannot be consulted because there is nothing cached to retrieve, the universal H↔A fusion that was 0.75 on canonical characters drops to 0.30 on synthetic ones (Δ = -0.447), and the *signed* fusion flips from the designed -0.74 to +0.23 rather than recovering the negative target. That is how we infer the cache is consulted on canonical characters: by removing the cache and watching the apparent "measurement" collapse, not to faithful text measurement (which would recover the -0.74), but to a weak generic coupling prior.

**Relationship to 'the Cliff'.** The Cliff is the boundary between pretraining (where the cache is built) and inference (where it is queried). The activation probe (the representational corroboration, §4.2) reaches into the LLM's late-layer activations and asks where on the cliff edge the cached profile becomes the rating output, see Egg E5 in §8 for the metaphor.

**Title meta-joke.** J.D. Salinger's Holden Caulfield lives in every contemporary LLM's cache. *The Catcher in the Rye* is among the most-discussed novels in any web-scraped corpus, with thousands of high-quality character analyses flowing through it into pretraining. The title is itself an instance of the phenomenon it documents, when a reader sees "Catcher in the Cache" and remembers Holden's voice without re-reading the book, that recall is a cache lookup. The LLM does the same thing when asked to rate him.

### 4.2 The pieces of the apparatus

**The catch, substrate falsifier (the cross-rater panel RQ6.9 PRIOR_DRIVEN).** The 25-rater paired test that drops canonical-character priors by running the same HEXACO probe on 20 *synthetic* characters not present in any training corpus. Headline: mean |r(H, A)| collapses from 0.75 (canonical) to 0.30 (synthetic); Δ = -0.447, paired Wilcoxon W=0, p_BH = 1.5×10⁻⁷ after BH-FDR correction (three times the pre-registered |Δ| ≥ 0.15 threshold). The signed fusion is +0.23 on synthetic (not the designed -0.74), so what remains is a generic prior, not measurement. This is the substrate-level catch, without the priors, the entanglement mostly vanishes.

**The edge catcher, cache map / cache-membership gauge (SCPI).** In embedding space the in-cache and out-of-cache characters separate cleanly (canonical median similarity 0.87 vs synthetic 0.41, no overlap), the cache has empty regions no canonical character occupies, and SCPI's retrieval over canonical neighbours re-imposes the fusion on synthetic characters designed to decouple it (+0.92 on a −0.74 design). This is the deployment-facing catch, it stands at the in/out-of-cache boundary and flags the characters about to fall. Detailed in the discussion and notebook `05_cache_map`. *(Note: SCPI here is the cache-membership gauge, not SCPI-as-M6, the weak retrieval method in the comparison; same embeddings, different job, see §4.6.)*

**A representational corroboration, activation probe (V6).** A layer-depth probe on 12 open-weight models (Llama-3.1-8B/70B, Qwen-2.5-7B/72B, Gemma-2-9B, Mistral-7B, Mixtral-8×22B-Instruct). We fit Ridge probes over PCA-50 features of the hidden-state activations to predict the **3-rater frontier-consensus** HEXACO target (not each model's own output) at each layer. Headline: Qwen-72B-Instruct's r(predH, predA) goes from +0.83 at layer 10 to -0.22 at layer 79 (Δ_depth = -1.05): H and A are **entangled in the early/shallow layers** (r ≈ +0.83, close to the 0.75 rating-time fusion) and **separate with depth**: the fusion is present in the shallow encoding rather than built by deep processing, consistent with a retrieved prior. **Caveat:** the linear fits are weak (per-trait R² often negative) and the non-linear MLP did not converge, so this is *suggestive corroboration*, not a mechanism-level catch; a refit targeting each model's own ratings (which exist in the panel) is feasible future work.

### 4.3 How the falsifier and the probe rule out explanations

Beyond the SCPI edge catcher (the deployment-facing gauge in §4.2), the substrate falsifier and the activation probe each rule out a different candidate explanation for the universal canonical |r| = 0.75:

| Candidate explanation for canonical \|r\| = 0.75 | What catches it |
|---|---|
| (a) Genuine training-corpus structure (LLMs really did learn that H and A are coupled in human personality) | **Substrate falsifier rules out (a).** If (a) were true, synthetic characters not in training corpora should show the same fusion; they don't (drops from 0.75 to 0.30, and the signed fusion is +0.23, not the designed -0.74). |
| (b) Retrieval against memorized canonical-character priors | **Substrate falsifier supports (b).** When you can't retrieve (synthetic substrate), the fusion goes away. |
| (c) Post-training pressure (RLHF / DPO / CAI fusion at the output mapping) | **Activation probe localizes (c).** If (c) were the whole story, the entanglement should be visible at late layers (where the output mapping lives) but absent at early layers. That's what the depth gradient at 70B+ scale shows. |

The substrate falsifier selects (b) over (a) at the *substrate* level. The activation probe localizes where (b) and any residual (c) component live in the network. Together with the SCPI edge catcher (§4.2), they document the full retrieval-not-measurement story.

### 4.4 Linguistically: "The Catcher" vs "The Catcher Test"

The vocabulary distinguishes:

- **The Catcher** = the full apparatus: the substrate falsifier, the SCPI edge catcher, and the activation probe (§4.2).
- **The Catcher Test** = the substrate falsifier specifically, as a one-shot falsifier you can describe in a sentence: *take away the canonical priors and watch the trait fusion collapse.*

Both terms are informal. The formal experiment names in the paper, repo, and pre-registration are:

- *Substrate falsifier* (or *the cross-rater panel RQ6.9 PRIOR_DRIVEN*) for the substrate-level catch.
- *V6 activation probe* (or just *activation probe* in reader-facing prose) for the representational corroboration.

### 4.5 The probes inside the activation probe

The activation probe runs two probe types per (model, layer) cell:

- **Ridge probe** (primary, but weak): linear regression with L2 regularization (PCA-50 input → predicted H and A). Measures whether H and A are linearly decodable from the activations. The depth-dissociation pattern is read off this probe, but its per-trait R² is frequently negative (r ≈ 0.30), so the pattern is suggestive corroboration, not a load-bearing result.
- **MLP probe** (sensitivity check): a small non-linear network (1 hidden layer, 64 units, lbfgs solver, PCA-50 input). Asks whether a non-linear function could find separability the Ridge probe misses.

The MLP is included as a *probe-class robustness check*, a reviewer could ask "maybe Ridge is too weak and a non-linear function would find the traits already separated in the activations, which would weaken your dissociation story." The MLP comparison rules that reading out, *provided the substrate supports a non-linear probe*. On our n=60-per-cell substrate it doesn't: the non-linear-probe refit confirmed the MLP overfits at this sample size (75/79 cells with negative R²_H), so the honest reading is that the Ridge probe is the primary (if weak) readout and the MLP is a sensitivity check that ran into substrate-underpowered convergence. Neither probe is load-bearing; the dissociation story is suggestive corroboration that does not depend on the MLP outcome.

### 4.6 What is *not* "the Catcher"

The five-method comparison (M2 RF classifier, M3 RF regressor, M4 multi-provider LLM consensus, M5 single held-out LLM probe, M6 SCPI k-NN retrieval), the three-bar diagnostic protocol (Bar 1 ground-truth recovery / Bar 2 corrected Campbell-Fiske MTMM / Bar 3 external concurrent validity), and the three-way head-to-head among OCEAN-HP / OCEAN-6 / HEXACO are not "the Catcher." They are the *measurement-quality comparison*, the deployment-side validation that identifies **HEXACO as the recommended construct space** for downstream persona work (with a label-availability tiering: run-time HEXACO probe when an LLM is available; the OCEAN O/C/E cheap regressor as the LLM-free floor at scale). The Catcher is what runs *after* the comparison identifies the deployable instrument: it asks whether the instrument is actually measuring or actually retrieving on the canonical-literary substrate. Different question, different apparatus.

**One clarification about SCPI.** SCPI wears two hats, and only one is the Catcher. As **M6 in the comparison**, SCPI is a k-NN *measurement method*, and a deliberately weak one (it just returns the nearest cached character's profile), which is the point. As the **cache-membership gauge / cache map** (§4.2, notebook `05_cache_map`), the *same embeddings* are used not to measure a trait but to detect whether a character sits inside the cache and to find the cache's empty regions. That second role, standing at the edge, is the edge catcher. Same machinery, opposite jobs: M6-as-measurer is what the Catcher catches; SCPI-as-cache-gauge is part of the Catcher doing the catching.

---

## 5. Why *Catcher in the Rye* is not in our 75-work corpus (the lampshade)

Our comparison substrate is 75 nineteenth- and early-twentieth-century Anglo-European canonical works (76 in the full ingestion pipeline; Julius Caesar is dropped from the comparison set for a BookNLP coreference failure). *Catcher in the Rye* (1951) sits outside that window by about thirty years.

This is not an oversight. The corpus was chosen for ground-truth-attribution density (peer-reviewed scholarly trait readings exist densely for the 19th-/early-20th-century canon; less densely for mid-century works) and substrate stability.

But Holden Caulfield is in every LLM rater's training cache, with thousands of high-quality discussions, character analyses, and trait-attribution-style readings flowing through web data into pretraining. **That's the phenomenon the paper studies.** Using Salinger's title to label a phenomenon Salinger's character exemplifies is the title's meta-joke. The title-page footnote in the manuscript lampshades this explicitly.

## 6. Alignments we are *not* claiming

Three Catcher motifs that don't map onto our paper:

| Catcher feature | Why it doesn't map |
|---|---|
| Adolescent angst and Holden's raw, irreverent voice | The paper is scholarly; we borrow Holden's vocabulary (notably "phony") but not his register |
| Loss of innocence / coming-of-age arc | The paper is about a methodological finding, not a developmental story |
| Phoebe / sibling relationship | No analog |
| Pencey expulsion / failure setup | No analog |
| Red hunting hat as protective talisman | No analog |
| Carousel gold-ring scene | A loose conceptual stretch ("we let LLMs ship retrieval-not-measurement, like Holden lets Phoebe risk the gold ring"), we considered it; we don't push it |

Three legitimate alignments plus one meta-self-reference is enough for a literary-allusion title. We don't need every Salinger motif to map.

## 7. Easter-egg trail

The literary allusion is reinforced by six Easter eggs planted in the manuscript and this companion repository. They are designed to reward the reader who notices the first one and starts looking for the rest.

| # | Where | What |
|---|---|---|
| **E1** | §1 epigraph (top of introduction) | The Holden Caulfield quote at the top of this file: *"People always think something's all true."* |
| **E2** | Title-page footnote | A direct lampshade: *The Catcher in the Rye* (1951) is not among the 75 works in our corpus, but Holden Caulfield is in every LLM rater's cache, which is the phenomenon this paper studies |
| **E3** | §7 Acknowledgements | *Finally, we thank J.D. Salinger for the title's framing; any "phoniness" in our methodology is ours, not his.* |
| **E4** | §5 Headline-interpretation paragraph | *In Holden Caulfield's terms, the LLM rating output on canonical literary characters reads as "phony", fluent and confident on its face, but generated from memorized priors rather than from text-based inference.* |
| **E5** | §6 Mechanism-vs-behavior limitation bullet | *The activation probe is our attempt to be the catcher, to grab the LLM at the edge of the cliff between pretraining and inference, before the cached profile becomes the rating output.* |
| **E6** | README (this repo) | Top-line wink: *The phoniness of LLM personality rating on canonical characters is the load-bearing finding of this paper. We catch it in the cache.* |

Each egg leans on one of the three strong alignments (phoniness, the catcher metaphor, retrospective recall). No egg in the recommended set forces a weak alignment.

## 8. Vocabulary glossary

### Literary-allusion vocabulary (informal)

| Catcher term | Paper-domain meaning |
|---|---|
| **Phony** | LLM rating output that looks like measurement but is generated from retrieval against canonical-character priors. The §5 headline-interpretation Holden callback uses this word in Salinger's precise sense. |
| **The Catcher** | The full diagnostic apparatus that catches the retrieval signature: the substrate falsifier, the SCPI edge catcher, and the activation probe. See §4.2 for the mechanics. |
| **The Catcher Test** | The substrate falsifier specifically, the one-shot falsifier that drops the canonical-character priors and observes the resulting drop in trait fusion. Formal name: the cross-rater panel RQ6.9 PRIOR_DRIVEN. |
| **The Cache** | The LLM's *internal representation* of its training corpus, the statistical regularities and content-addressed memory that survive pretraining and can be retrieved at inference time. Not the raw training text (which lives in Common Crawl, ePUB collections, etc.) and not an explicit lookup table; rather, the distributed weight patterns the model learned. For canonical literary characters, the cache contains Wikipedia plot summaries, SparkNotes / CliffsNotes character analyses, peer-reviewed literary criticism, fanfic, classroom essays, and adaptation reviews. See §4.1 for the full unpacking and the cache-miss mechanism the substrate falsifier exploits. |
| **The Cliff** | The boundary between pretraining (where canonical-character profiles are stored in the cache) and inference (where they emerge as rating output). The activation probe is "our attempt to be the catcher, to grab the LLM at the edge of the cliff" (§6 mechanism-vs-behavior bullet, Egg E5). |

### Formal experiment vocabulary (used in paper, repo, and pre-registration)

| Formal term | What it is |
|---|---|
| **Substrate falsifier** | The substrate-level catch (§4.2). Pre-registered as the cross-rater panel RQ6.9 PRIOR_DRIVEN. The paired-design test on 25 panel raters × 60 canonical characters vs 20 synthetic characters; tests whether the universal H↔A fusion persists when canonical priors are removed. Outcome: Δ = -0.447, p_BH = 1.5×10⁻⁷. Falsifies the "genuine training-corpus structure" reading. |
| **Activation probe (V6)** | The representational corroboration (§4.2). Layer-by-layer probe of hidden-state activations from 12 open-weight 7–72B models, asking whether H and A are recoverable from the latent representations at different depths. "V6" is the project-internal name (Validity check 6) used in the repo and commit history; "activation probe" is the reader-facing name in the paper. |
| **Layer-depth dissociation** | The activation-probe finding at 70B+ scale: H and A are entangled in the early/shallow layers (Qwen-72B layer 10: r(predH, predA) = +0.83, ≈ the 0.75 rating-time fusion) and separate with depth (layer 79: -0.22), Δ_depth = -1.05, in three independent families (Meta dense, Qwen dense, Mistral sparse-MoE). The probe targets the 3-rater consensus and the fits are weak, so this is suggestive corroboration. |
| **Ridge probe** | The linear probe inside the activation probe. L2-regularized linear regression mapping PCA-50 features of activations → predicted H and A. *Primary but weak*: the layer-depth dissociation pattern is read off this probe, but its per-trait R² is frequently negative, so it is suggestive corroboration, not a load-bearing result. |
| **MLP probe** | The non-linear probe inside the activation probe. A small Multi-Layer Perceptron (1 hidden layer, 64 units, lbfgs solver, PCA-50 input) included as a *sensitivity check*, does a non-linear function find separability the Ridge probe misses? On our n=60-per-cell substrate the MLP underfits (non-linear-probe refit confirmed); neither probe is load-bearing, and the MLP comparison is a robustness check that ran into substrate-underpowered convergence. |
| **Pool ablation** | A robustness contrast within the activation probe comparing three pooling strategies (mean-pool-last-256 / last-token / first-128-mean) on dense Llama-70B-Instruct vs sparse-MoE Mixtral-8×22B-Instruct. Finds the trait subspace is mean-pool-localized in dense models and pool-distributed in sparse-MoE, a cross-family mechanism contrast. |
| **25-rater panel** | The full set of 25 distinct frontier LLMs (across 9 provider ecosystems) used as the substrate for the universal-collapse finding (RQ6.1). This is the pre-registration-lock count: Grok 4.3 was run once, and the Amendment-9 additions Hermes-3 (NousResearch) and Jamba-Large-1.7 (AI21) were never re-run on the synthetic substrate and were dropped, along with the two provider families they contributed. |
| **Mode-dissociation extension (mode-dissociation)** | Separately pre-registered extension under Amendment 11. Administers HEXACO markers to a 6-model representative subset in *subject-mode* self-report under N=10 multi-elicitation, asking whether the H↔A fusion is judge-mode-specific (Branch A) or generalises (Branch B). Outcome: Branch A falsified at locked thresholds; Branch B retained with ~48% attenuation. Not part of the Catcher proper; complements it by ruling out judge-mode-specificity as the whole story. |

---

## 9. Methodological honesty

A literary-allusion title is decoration unless it does work. We claim three pieces of work here:
1. **Thematic.** Phoniness/authenticity maps onto retrieval/measurement at the thesis level.
2. **Methodological.** The catcher metaphor maps onto the diagnostic + activation-probe apparatus.
3. **Meta-self-referential.** Holden lives in every LLM cache, which is what the paper studies.

If a reviewer asks why a 1951 novel is in the title of a paper about contemporary LLM evaluation, the answer is: because Salinger's character is one of the canonical entities that LLMs have cached profiles for, the title is the paper's claim demonstrated in miniature, and the three thematic alignments earn the allusion. If we couldn't claim those three, we'd have dropped the literary allusion entirely.

We didn't.

, *J.S. Raetano, J. Gregor, S. Tamang. 2026.*
