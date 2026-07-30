# Objections, and where the evidence is

A referee arrives with a doubt, not a file path. This page maps each objection to the
artifact that speaks to it, so checking one takes a minute rather than an afternoon.

The list is not defensive framing. Items 1 through 8 are the paper's own stated
limitations, quoted from its Limitations section; the last three are objections raised
by reviewers of earlier drafts. **Two of them we cannot currently answer, and those say
so.**

---

## The one worth checking first

**"The fusion is an evaluative halo on vivid canonical characters, not retrieval."**

This is the objection the paper stands or falls on, so it gets the shortest path.

Rating 20 synthetic characters **from their name alone** — characters that do not exist,
carrying no text at all — yields a strongly fused `r(H, A_HEX) ≈ +0.83`. Rating **the
same characters from their text** recovers the designed anti-correlation, about `-0.45`.
Same characters, so vividness and prose quality are constant by construction, and a halo
account has to explain why the condition carrying the *least* information fuses *most*.

```bash
python paper_artifacts/coupling_prior/recompute_coupling.py    # $0, cached
```

The cell was pre-registered and re-run before the paper leaned on it:
[`replication_2026-07-27/`](../paper_artifacts/coupling_prior/replication_2026-07-27/)
carries `SPEC.md` written before the run, the runner, and the results. It came back at
**+0.91, 95% CI [0.80, 0.96]**.

---

## The paper's own eight limitations

| # | Objection | Where the evidence is |
|---|---|---|
| 1 | **Within-LLM scope.** Ground truth, methods and raters share an LLM substrate in places; the synthetic substrate is n = 20 | Substrate, curation and novelty checks in [`paper_artifacts/pivot6_hexaco_atlas/`](../paper_artifacts/pivot6_hexaco_atlas/). Rater independence is **not answered**; see "what we cannot answer" below |
| 2 | **Corpus scope.** Anglo-American plus translated canon | Full ground truth for all 75 works in [`data/aperture-data-v1/ground_truth/`](../data/aperture-data-v1/ground_truth/) — inspect the actual coverage rather than take our word |
| 3 | **Probe population.** The activation probe is open-weight only and population-disjoint from the panel | [nb 08](../notebooks/08_activation_probe_dissociation.ipynb). The paper claims it corroborates rather than establishes the mechanism, and this is why |
| 4 | **Default model state.** No persona steering; the base-versus-instruct contrast was pre-registered and deferred | Deviations from pre-registration are listed in the paper's own Appendix A.4, not hidden here |
| 5 | **Characterization depth.** Canonical and synthetic match token count and register but not depth | The name-only conditions above are the answer: they hold characterization constant and still show the effect |
| 6 | **Clustered raters.** Raters cluster by provider family, so rater-level tests overstate precision | `family_clustering` in [`panel25_results.json`](../paper_artifacts/pivot6_hexaco_atlas/panel25/panel25_results.json): ICC 0.5774. The paper reports the family-level test as the headline **because of** this, not despite it |
| 7 | **Rater-set-dependent residual sign.** The off-cache signed residual ranges +0.23 to −0.45 across panels | [`signed_r_results.json`](../paper_artifacts/pivot6_hexaco_atlas/signed_r_results.json) (carries a `_SUPERSEDED` note: it is the 26-rater run) and the coupling-prior panel. The variation is real and reported, not smoothed |
| 8 | **Judge versus subject mode.** The manipulation check runs in subject mode; the main result is judge mode | CA.13 in [`further_analyses.md`](appendix/further_analyses.md) |

## Objections raised by earlier reviewers

| Objection | Where the evidence is |
|---|---|
| **The reference standard is partly model-derived, so the result is circular** | [`agt_only_sensitivity.md`](appendix/agt_only_sensitivity.md) — restricting ground truth to peer-reviewed scholarship only (n = 185) *strengthens* the convergent result. The paper calls this the "scholarly-only subset"; AGT is Academic Ground Truth, the same thing |
| **The cache-membership gauge's AUC 0.99 is too good to be true** | It is an upper bound and the paper says so where the number appears. It is measured on an engineered contrast: [nb 05](../notebooks/05_cache_map.ipynb) |
| **The headline numbers are not reproducible** | Two files and four numbers, no API key, in the [README](../README.md#verify-the-central-claim-in-two-minutes). Nine of ten notebooks run keyless from cached artifacts in about a minute total |

---

## What we cannot answer

Stated plainly, because a companion that answers everything is not credible.

**No human validation of the synthetic substrate.** The whole falsifier rests on 20
generated characters, and no human has confirmed they encode the separation they were
designed to encode. The study that would close this is written, pre-registered and
IRB-gated but **has not run**: [`human_panel/`](../human_panel/) holds the design, the
pre-registration and the rating instrument. What you get today is a protocol, not data.

**No rater independence.** The 25 raters cluster by provider family at ICC 0.577. The
paper's response is statistical — report the family-level test as the headline and label
the rater-level one anti-conservative — not empirical. A genuinely independent panel means
human raters, which is the same missing study as above.

**The decisive ablation is not possible.** The clean test would hold text constant and
vary only cache membership. Elizabeth Bennet cannot be un-cached. The synthetic
characters are the closest available substitute, which is why their construction is
published in full and why the name-only condition matters so much.
