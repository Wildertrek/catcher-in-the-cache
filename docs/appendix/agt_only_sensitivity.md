# AGT-only sensitivity check, Bars 1 + 2 verified; Bar 3 deferred

This appendix supports the source-stratified-MAE claim in
**§6.1 (GT and method lineage contamination)**: that the
load-bearing convergent-validity numbers do not change materially
when the corpus is restricted to characters whose ground truth
includes at least one **AGT** (Academic Ground Truth: peer-reviewed
psychological-criticism scholarship) source, i.e., the highest
single-source weight tier (S/A bands at weights 0.50–1.00; see
`aperture_gt_taxonomy.TIER_TABLE`).

## Subset construction

- **Full comparison corpus**: 562 characters across 75 works.
- **AGT-only subset**: characters with at least one source of
  `source_type == "AGT"` in their `ground_truth.json` source list,
  regardless of additional SGT / PGT / MGT / CGT sources also
  contributing to the per-character consensus.
- **n = 185 characters (33% of corpus)** survive the AGT-only filter.

Source: `data/ground_truth/<book>.json` (in this repo)
joined to the comparison predictions at `(book, coref_id)`.

## Bar 1: Per-method GT recovery (verified)

| Method | MAE (full) | r (full) | CCC (full) | MAE (AGT) | r (AGT) | CCC (AGT) | \|ΔMAE\| |
|---|---:|---:|---:|---:|---:|---:|---:|
| M2 classifier | 0.367 | 0.118 | 0.010 | 0.403 | 0.125 | 0.011 | **0.037** |
| **M3 regressor** | **0.262** | **0.649** | **0.646** | **0.254** | **0.732** | **0.729** | **0.009** |
| **M4 consensus** | **0.230** | **0.770** | **0.764** | **0.229** | **0.798** | **0.790** | **0.001** |
| **M5 probe** | **0.270** | **0.633** | **0.630** | **0.296** | **0.588** | **0.583** | **0.026** |
| M6 SCPI | 0.328 | 0.308 | 0.268 | 0.379 | 0.176 | 0.131 | **0.050** |

**Bar 1 verdict**: M3/M4/M5 convergent triangle stable within ±0.026
MAE; max |ΔMAE| = 0.026 (M5), well within §6.1 ±0.03 tolerance.

## Bar 2: Cross-method MTMM convergent triangle (verified; **strengthens**)

Per-pair monotrait-heteromethod $r$ minimum across the 5 OCEAN traits:

| Method pair | Monotrait min (full, 562) | Monotrait min (AGT, 185) | Δ |
|---|---:|---:|---:|
| **M3↔M4 (contamination-circular)** | +0.807 | +0.894 | **+0.087** |
| **M3↔M5 (contamination-clean)** | +0.589 | +0.706 | **+0.116** |
| **M4↔M5 (contamination-clean)** | +0.553 | +0.633 | **+0.080** |
| M3↔M6 SCPI | +0.260 | +0.218 | −0.042 |
| M4↔M6 SCPI | +0.220 | +0.162 | −0.058 |
| M5↔M6 SCPI | +0.244 | +0.197 | −0.047 |
| M2↔M4 (classifier) | +0.063 | +0.167 | +0.104 |
| M2↔M5 (classifier) | +0.126 | +0.282 | +0.156 |

**Bar 2 verdict**: The convergent-validity triangle (M3↔M4↔M5)
**strengthens** on the AGT-only subset, monotrait minima rise by
+0.08 to +0.12 across all three pairs. This is the direction the
§6.1 contamination story predicts: if M3↔M4 agreement were
artificially inflated by shared CGT-band signal, restricting to
AGT-attested chars (where CGT contributes less weight) should
WEAKEN the contamination-circular pair. Instead, all three
load-bearing pairs gain, consistent with AGT chars being
higher-attestation, denser-evidence main characters that all
three methods read more cleanly.

M6 SCPI pairs weaken slightly (−0.04 to −0.06), reproducing
§5.3's finding that SCPI's author/period-clustering signal is
dominated by canonical-protagonist density (and AGT-attested chars
are precisely the canonical protagonists). M2 classifier pairs
shift but remain below the §3 absolute-monotrait floor (0.30)
at both subset sizes, the §6.4 known-degenerate disclosure holds.

## Bar 3: AGT∩OP-overlap (deferred to a future revision / R&R)

Bar 3 uses the n=60-char OP-overlap subset (§4.3). The AGT∩OP
intersection is **35 characters**: adequate for direction-of-effect
verification but too small for tight bootstrap CI estimation. Bar 3
AGT-only sensitivity is therefore deferred to a future revision / R&R cycle
where it can be paired with the F3 human-rater HEXACO anchor
expansion (which moves Bar 3 from LLM-rater consensus toward
human-anchored ground truth, expanding the n).

The Bar 1 + Bar 2 verification is the load-bearing answer to
§6.1's contamination question: the convergent-validity argument
gets STRONGER, not weaker, when restricted to AGT-attested chars.

## What this shows (across all verified bars)

**1. The contamination story holds AND strengthens.** §6.1 worries
that M3↔M4 r = 0.841 might be inflated by shared CGT-band signal.
The Bar 2 AGT-only check shows M3↔M4 monotrait minimum *rises*
from 0.807 to 0.894 on AGT-only, while the contamination-clean
M3↔M5 pair rises by even more (+0.116). The convergent triangle
is intact and stronger on the cleanest-GT subset.

**2. The §6.1 ±0.03 tolerance holds for the load-bearing triangle
on Bar 1.** M3 (Δ=0.009), M4 (Δ=0.001), M5 (Δ=0.026). M5's larger
shift is dominated by AGT chars being slightly harder for the
single-rater Anthropic probe to read consistently, likely an
artifact of those chars' richer multi-source GT producing more
nuanced trait vectors than M5's single-pass elicitation can match.

**3. M2 and M6 outside-tolerance shifts are not load-bearing.**
M2 (Δ=0.037) is the classifier-as-regressor failure mode already
deprecated in §6.4. M6 (Δ=0.050) is SCPI's known author/period-
clustering weakness on canonical-protagonist density (already
discussed in §5.3 + §5.9). Neither method enters the convergent-
validity triangle, so their AGT-shift does not threaten the §6.1
contamination story.

## Reproduction

```bash
python3 - << 'EOF'
import json, glob, os
preds = json.load(open(
  'paper_artifacts/method_bakeoff_v4/predictions.json'
))['predictions']
char_tiers = {}
for f in glob.glob(
  '<RESEARCH_REPO>/rag_indices/*/pillar1/ground_truth.json'
):
    book = os.path.basename(os.path.dirname(os.path.dirname(f)))
    d = json.load(open(f))
    for c in d.get('characters', []):
        char_tiers[(book, str(c.get('coref_id','')))] = {
            s.get('source_type') for s in c.get('sources', [])
            if s.get('source_type')
        }
agt = [p for p in preds
       if 'AGT' in char_tiers.get((p['book'], str(p['coref_id'])), set())]
# Bar 1: aggregate MAE / r / CCC over OCEAN traits per method
# Bar 2: per-pair Pearson r per trait, monotrait minimum per pair
EOF
```

Full numerical output:
- Bar 1: [`paper_artifacts/method_bakeoff_v4/agt_only_sensitivity.json`](../../paper_artifacts/method_bakeoff_v4/agt_only_sensitivity.json)
- Bar 2: [`paper_artifacts/method_bakeoff_v4/agt_only_bar23_sensitivity.json`](../../paper_artifacts/method_bakeoff_v4/agt_only_bar23_sensitivity.json)

---

*Generated 2026-05-21 as Tier 1 P0+P1 verification of §6.1 contamination
caveat (Bar 1; Bar 2; Bar 3 deferred to a future revision / R&R when
paired with F3 human-rater HEXACO anchor expansion of the n=60 OP-overlap subset).*
