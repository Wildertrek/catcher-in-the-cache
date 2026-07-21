# Factor-vector Bar 2 Head-to-Head, Results

**Corpus:** 60-char OP-overlap subset (n_intersection HEXACO=57, OCEAN-HP=56, OCEAN-6=57)
**Raters:** anthropic, openai, google (Anthropic Sonnet 4.5, OpenAI GPT-5.2, Google Gemini 2.5 Pro)
**Monotrait floor:** r >= 0.3

## Side-by-side

| Metric | HEXACO | OCEAN-HP | OCEAN-6 |
|---|---|---|---|
| n traits | 6 | 7 | 6 |
| n chars (all 3 raters) | 57 | 56 | 57 |
| n rater pairs | 3 | 3 | 3 |
| mean traits clearing 3-inequality (per pair, of total) | 6.00 / 6 | 4.67 / 7 | 5.00 / 6 |
| mean traits clearing 3-ineq + floor (per pair, of total) | 6.00 / 6 | 4.67 / 7 | 5.00 / 6 |
| mean monotrait-heteromethod r | 0.764 | 0.770 | 0.759 |

## Per-rater-pair MTMM detail

### HEXACO (3 rater pairs x 6 traits)

| pair | n_conv_3ineq | n_conv_floor | mono_mean | mono_min |
|---|---|---|---|---|
| anthropic x openai | 6/6 | 6/6 | 0.799 | 0.732 |
| anthropic x google | 6/6 | 6/6 | 0.783 | 0.737 |
| openai x google | 6/6 | 6/6 | 0.711 | 0.556 |

### OCEAN-HP (3 rater pairs x 7 traits)

| pair | n_conv_3ineq | n_conv_floor | mono_mean | mono_min |
|---|---|---|---|---|
| anthropic x openai | 5/7 | 5/7 | 0.832 | 0.795 |
| anthropic x google | 5/7 | 5/7 | 0.748 | 0.643 |
| openai x google | 4/7 | 4/7 | 0.729 | 0.519 |

### OCEAN-6 (3 rater pairs x 6 traits)

| pair | n_conv_3ineq | n_conv_floor | mono_mean | mono_min |
|---|---|---|---|---|
| anthropic x openai | 5/6 | 5/6 | 0.819 | 0.735 |
| anthropic x google | 6/6 | 6/6 | 0.726 | 0.500 |
| openai x google | 4/6 | 4/6 | 0.731 | 0.603 |

## Per-trait cross-rater monotrait-heteromethod r

HEXACO:
- H: r = 0.795
- E_HEX: r = 0.796
- X: r = 0.675
- A_HEX: r = 0.802
- C_HEX: r = 0.765
- O_HEX: r = 0.752

OCEAN-HP:
- O: r = 0.776
- C: r = 0.780
- E: r = 0.656
- A: r = 0.782
- N: r = 0.822
- H: r = 0.799
- A_HEX: r = 0.774

OCEAN-6:
- O: r = 0.757
- C: r = 0.778
- E: r = 0.613
- A: r = 0.832
- N: r = 0.801
- H: r = 0.771

## Per-vector verdict

1. **HEXACO**: 6.00/6 (100%) traits clear 3-ineq + floor per rater pair
2. **OCEAN-6**: 5.00/6 (83%) traits clear 3-ineq + floor per rater pair
3. **OCEAN-HP**: 4.67/7 (67%) traits clear 3-ineq + floor per rater pair

## Pre-registered decision rule (HEXACO vs OCEAN-HP per spec doc)

- HEXACO mean traits clearing 3-ineq + floor per rater pair: 6.00 / 6 (100%)
- OCEAN-HP mean traits clearing 3-ineq + floor per rater pair: 4.67 / 7 (67%)

**HEXACO outperforms OCEAN-HP** (delta 1.33 traits per pair).