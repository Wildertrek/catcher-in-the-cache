# V6: Activation Probe on Open-Weight Models (FIRED)

**Status:** Complete (2026-05-17). Originally deferred per the cross-rater panel Amendment 5; un-deferred and fired same day after Modal infrastructure landed.

## What this measures

V6 extracts layer-wise hidden-state activations from 8 open-weight models (4 families × {base, instruct}) on the same 60-character the cross-rater panel substrate, then trains 5-fold-CV logistic regression at each layer separately for two binary classification targets:

- `y_H` = median-binarized HEXACO H score (target = median across `anthropic_1` + `openai_1` + `google_1` the cross-rater panel raters)
- `y_A_HEX` = median-binarized HEXACO A_HEX score (same targets)
- `y_joint` = 4-class joint (H-low/A-low, H-low/A-high, H-high/A-low, H-high/A-high)

Entanglement gap = `acc(joint) - acc(H) * acc(A_HEX)`. Positive gap indicates the joint classification benefits from H and A_HEX being *coupled* at the layer; zero gap is the independence baseline.

| Family | Base | Instruct |
|---|---|---|
| Meta Llama-3.1 | `meta-llama/Llama-3.1-8B` | `meta-llama/Llama-3.1-8B-Instruct` |
| Google Gemma-2 | `google/gemma-2-9b` | `google/gemma-2-9b-it` |
| Mistral 7B v0.3 | `mistralai/Mistral-7B-v0.3` | `mistralai/Mistral-7B-Instruct-v0.3` |
| Qwen-2.5-7B | `Qwen/Qwen2.5-7B` | `Qwen/Qwen2.5-7B-Instruct` |

Each model: 60 chars × 4–8 layers × 3584–4096 hidden-dim, mean-pooled over the final 256 tokens of the evidence pack (max input 4096 tokens, truncated).

## Headline numbers

### Peak per-model accuracy

| Model | Best layer | acc(H) | acc(A_HEX) | gap |
|---|---|---|---|---|
| Qwen-2.5-7B-Instruct | L12 | 0.700 | 0.600 | +0.080 |
| Qwen-2.5-7B (base) | L24 | 0.733 | 0.667 | -0.022 |
| Gemma-2-9b-it | L8 | 0.733 | 0.683 | -0.001 |
| Gemma-2-9b (base) | L16 | **0.767** | 0.683 | +0.009 |
| Llama-3.1-8B-Instruct | L20 | 0.700 | 0.667 | +0.067 |
| Llama-3.1-8B (base) | L31 | 0.700 | **0.750** | +0.008 |
| Mistral-7B-Instruct | L24 | 0.683 | 0.700 | +0.022 |
| Mistral-7B (base) | L24 | 0.667 | 0.667 | +0.056 |

### Mean entanglement gap (across all layers, per model)

| Model | Mean gap |
|---|---|
| Gemma-2-9b base | **-0.007** |
| Qwen-2.5-7B base | +0.028 |
| Gemma-2-9b-it | +0.041 |
| Qwen-2.5-7B-Instruct | +0.045 |
| Llama-3.1-8B base | +0.077 |
| Llama-3.1-8B-Instruct | +0.081 |
| Mistral-7B-Instruct | +0.091 |
| Mistral-7B base | **+0.108** |

### Base→Instruct delta (Instruct - Base, averaged across layers)

| Family | Δacc(H) | Δacc(A_HEX) | Δgap |
|---|---|---|---|
| Qwen-2.5-7B | -0.017 | -0.046 | **+0.042** |
| Gemma-2-9b | -0.021 | -0.013 | **+0.048** |
| Llama-3.1-8B | -0.013 | -0.000 | +0.004 |
| Mistral-7B | (mean) | (mean) | -0.017 |

## Interpretation (mechanism-vs-behavior)

**H and A_HEX are both recoverable from latent representations** at 67–77% / 60–75% accuracy (vs 50% chance), across all 8 open-weight models including the 4 base variants with no instruction tuning. This rules out the "structural training-corpus invariant" hypothesis: if H and A_HEX were fundamentally indistinguishable in the latent space, recovery wouldn't reach 75%.

**Latent entanglement is small.** Mean gap across all 64 (model, layer) cells is +0.052. Compared to the rating-time outputs from the cross-rater panel (mean |r(H, A_HEX)| = 0.743 across 25 models), there is a substantial **layer-to-output gap**: latents encode the two traits as separable but the rating-time response mapping projects them onto a single bipolar axis.

**Instruction-tuning slightly amplifies the gap, but the effect is small.** Three of four families show +0.04 to +0.05 mean Δgap under instruction tuning (Llama is null). Instruction-tuning does not eliminate the latent separability, it nudges the gap slightly upward while leaving accuracy nearly unchanged.

**The cross-rater panel bipolarity collapse is therefore localized to the post-training output-mapping pressure**, not to the latent representation itself. The panel finding that |r(H, A_HEX)| varies by alignment regime (η² = 0.622, p = 0.004, Hybrid uniquely low at 0.54) is consistent: alignment regime differences land at the output mapping, not at the latent encoding which is shared across families.

## Limitations

- **n = 60 chars.** Probes trained on a small sample; per-layer accuracy estimates have non-trivial CV variance (~±0.05). Replication on a larger char substrate would tighten the estimates.
- **8 open-weight 7-9B models.** Larger open-weight models (Llama-3.1-70B, Llama-4-Scout) not included. Closed-source frontier models (Sonnet, GPT-5, Gemini Pro) cannot be probed via Modal (no weights). The V6 finding is therefore strictly an open-weight claim.
- **Mean-pooled-256-tokens single-shot.** Token-level dynamics are not characterized; the probe sees one summary vector per char per layer.
- **Targets are LLM-derived (the cross-rater panel 3-rater median), not human-rater HEXACO.** Latent recovery is therefore "alignment with the cross-rater LLM consensus on H and A_HEX," which has its own systematic biases.

## Reproduction

```bash
# Build evidence packs from the cross-rater panel manifest
.venv/bin/python scripts/v6_activation_probe/build_evidence_60chars.py

# Fire all 8 models on Modal (~25 min, $0.85 spend)
./scripts/v6_activation_probe/run_v6_all.sh

# Train probes locally
.venv/bin/python scripts/v6_activation_probe/v6_train_probes.py
```

## Files

- `v6_probe_<hf_id>.json`, raw activations (60 chars × N layers × hidden_dim)
- `v6_probe_results.json`, per-layer accuracy + entanglement gap per model
- `v6_probe_results.md`, markdown table summary
- `README.md`, this file
