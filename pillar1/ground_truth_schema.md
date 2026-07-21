# Ground-Truth Schema (v3)

Ground-truth files use a layered source-taxonomy to attribute each OCEAN vector to an evidence class.

## Source types

| Code | Name | Examples | Typical weight |
|------|------|----------|----------------|
| **AGT** | Authoritative Ground Truth | Expert annotations, named-rater panels | 1.00 |
| **SGT** | Scholarly Ground Truth | Peer-reviewed personality analyses | 0.80 |
| **PGT** | Proximal Ground Truth | Crowd-sourced curated sets (e.g., Big Five Backstage) | 0.40 |
| **MGT** | Model Ground Truth | Labels produced by other ML systems | 0.20 |
| **CGT** | Consensus Ground Truth | Aggregated multi-source labels without independent validation | 0.10 |

## File shape

```json
{
  "schema_version": "3.0",
  "book_id": "pride_and_prejudice",
  "characters": [
    {
      "canonical_name": "Elizabeth Bennet",
      "coref_id": "elizabeth_bennet_coref_01",
      "sources": [
        {
          "source_type": "AGT",
          "subtype": "expert_panel",
          "ocean": {"O": 0.82, "C": 0.61, "E": 0.71, "A": 0.55, "N": -0.32},
          "citation": "Internal annotation, 2025-11",
          "weight": 1.0
        }
      ]
    }
  ]
}
```

## Known caveat: B5B within-play duplicates

The Big Five Backstage (BFB) source assigns binary labels that can collapse to identical OCEAN vectors for distinct characters within the same work. Use the `bfb_uniq_ratio` helper (in the parent research repo) to filter works below `r_u < 0.70` before downstream Pearson claims. Observed ratios include:

- A Doll's House: 0.40
- Hedda Gabler: 0.57
- An Enemy of the People: 0.67
- Ghosts: 0.80
- A Christmas Carol: 0.86

Where possible, prefer AGT or SGT over BFB-derived PGT for drama.
