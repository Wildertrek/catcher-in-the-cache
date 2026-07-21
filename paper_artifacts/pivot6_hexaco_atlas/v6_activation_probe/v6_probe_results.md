# V6 Activation Probe, Results
- Target characters: n=60
- Models probed: Qwen/Qwen2.5-7B-Instruct, Qwen/Qwen2.5-7B, google/gemma-2-9b-it, google/gemma-2-9b, meta-llama/Llama-3.1-8B-Instruct, meta-llama/Llama-3.1-8B, mistralai/Mistral-7B-Instruct-v0.3, mistralai/Mistral-7B-v0.3

## Per-model accuracy (5-fold CV)
| Model | Layer | acc(H) | acc(A_HEX) | acc(joint) | entangle_gap |
|---|---|---|---|---|---|
| `Qwen/Qwen2.5-7B-Instruct` | 4 | 0.667 | 0.600 | 0.450 | +0.050 |
| `Qwen/Qwen2.5-7B-Instruct` | 8 | 0.667 | 0.633 | 0.517 | +0.094 |
| `Qwen/Qwen2.5-7B-Instruct` | 12 | 0.700 | 0.600 | 0.500 | +0.080 |
| `Qwen/Qwen2.5-7B-Instruct` | 16 | 0.700 | 0.633 | 0.500 | +0.057 |
| `Qwen/Qwen2.5-7B-Instruct` | 20 | 0.683 | 0.667 | 0.500 | +0.044 |
| `Qwen/Qwen2.5-7B-Instruct` | 24 | 0.683 | 0.650 | 0.467 | +0.022 |
| `Qwen/Qwen2.5-7B-Instruct` | 28 | 0.667 | 0.700 | 0.433 | -0.033 |
| `Qwen/Qwen2.5-7B` | 8 | 0.683 | 0.650 | 0.517 | +0.073 |
| `Qwen/Qwen2.5-7B` | 16 | 0.700 | 0.633 | 0.533 | +0.090 |
| `Qwen/Qwen2.5-7B` | 24 | 0.733 | 0.667 | 0.467 | -0.022 |
| `Qwen/Qwen2.5-7B` | 28 | 0.683 | 0.700 | 0.450 | -0.028 |
| `google/gemma-2-9b-it` | 4 | 0.717 | 0.683 | 0.450 | -0.040 |
| `google/gemma-2-9b-it` | 8 | 0.733 | 0.683 | 0.500 | -0.001 |
| `google/gemma-2-9b-it` | 12 | 0.683 | 0.667 | 0.567 | +0.111 |
| `google/gemma-2-9b-it` | 16 | 0.700 | 0.683 | 0.500 | +0.022 |
| `google/gemma-2-9b-it` | 20 | 0.683 | 0.650 | 0.483 | +0.039 |
| `google/gemma-2-9b-it` | 24 | 0.700 | 0.600 | 0.517 | +0.097 |
| `google/gemma-2-9b-it` | 28 | 0.717 | 0.617 | 0.483 | +0.041 |
| `google/gemma-2-9b-it` | 31 | 0.717 | 0.667 | 0.533 | +0.056 |
| `google/gemma-2-9b` | 4 | 0.700 | 0.633 | 0.467 | +0.023 |
| `google/gemma-2-9b` | 8 | 0.717 | 0.683 | 0.467 | -0.023 |
| `google/gemma-2-9b` | 12 | 0.717 | 0.650 | 0.467 | +0.001 |
| `google/gemma-2-9b` | 16 | 0.767 | 0.683 | 0.533 | +0.009 |
| `google/gemma-2-9b` | 20 | 0.717 | 0.683 | 0.517 | +0.027 |
| `google/gemma-2-9b` | 24 | 0.700 | 0.650 | 0.483 | +0.028 |
| `google/gemma-2-9b` | 28 | 0.750 | 0.700 | 0.467 | -0.058 |
| `google/gemma-2-9b` | 31 | 0.750 | 0.667 | 0.433 | -0.067 |
| `meta-llama/Llama-3.1-8B-Instruct` | 4 | 0.550 | 0.600 | 0.400 | +0.070 |
| `meta-llama/Llama-3.1-8B-Instruct` | 8 | 0.533 | 0.600 | 0.467 | +0.147 |
| `meta-llama/Llama-3.1-8B-Instruct` | 12 | 0.583 | 0.617 | 0.483 | +0.124 |
| `meta-llama/Llama-3.1-8B-Instruct` | 16 | 0.667 | 0.683 | 0.533 | +0.078 |
| `meta-llama/Llama-3.1-8B-Instruct` | 20 | 0.700 | 0.667 | 0.533 | +0.067 |
| `meta-llama/Llama-3.1-8B-Instruct` | 24 | 0.667 | 0.650 | 0.450 | +0.017 |
| `meta-llama/Llama-3.1-8B-Instruct` | 28 | 0.667 | 0.650 | 0.500 | +0.067 |
| `meta-llama/Llama-3.1-8B-Instruct` | 31 | 0.633 | 0.717 | 0.533 | +0.079 |
| `meta-llama/Llama-3.1-8B` | 4 | 0.567 | 0.567 | 0.400 | +0.079 |
| `meta-llama/Llama-3.1-8B` | 8 | 0.533 | 0.617 | 0.450 | +0.121 |
| `meta-llama/Llama-3.1-8B` | 12 | 0.633 | 0.617 | 0.517 | +0.126 |
| `meta-llama/Llama-3.1-8B` | 16 | 0.667 | 0.650 | 0.567 | +0.133 |
| `meta-llama/Llama-3.1-8B` | 20 | 0.683 | 0.667 | 0.483 | +0.028 |
| `meta-llama/Llama-3.1-8B` | 24 | 0.667 | 0.650 | 0.500 | +0.067 |
| `meta-llama/Llama-3.1-8B` | 28 | 0.650 | 0.667 | 0.483 | +0.050 |
| `meta-llama/Llama-3.1-8B` | 31 | 0.700 | 0.750 | 0.533 | +0.008 |
| `mistralai/Mistral-7B-Instruct-v0.3` | 4 | 0.567 | 0.500 | 0.433 | +0.150 |
| `mistralai/Mistral-7B-Instruct-v0.3` | 8 | 0.567 | 0.533 | 0.417 | +0.114 |
| `mistralai/Mistral-7B-Instruct-v0.3` | 12 | 0.567 | 0.583 | 0.417 | +0.086 |
| `mistralai/Mistral-7B-Instruct-v0.3` | 16 | 0.600 | 0.617 | 0.500 | +0.130 |
| `mistralai/Mistral-7B-Instruct-v0.3` | 20 | 0.617 | 0.683 | 0.550 | +0.129 |
| `mistralai/Mistral-7B-Instruct-v0.3` | 24 | 0.683 | 0.700 | 0.500 | +0.022 |
| `mistralai/Mistral-7B-Instruct-v0.3` | 28 | 0.650 | 0.683 | 0.500 | +0.056 |
| `mistralai/Mistral-7B-Instruct-v0.3` | 31 | 0.683 | 0.717 | 0.533 | +0.044 |
| `mistralai/Mistral-7B-v0.3` | 4 | 0.567 | 0.483 | 0.433 | +0.159 |
| `mistralai/Mistral-7B-v0.3` | 8 | 0.567 | 0.533 | 0.417 | +0.114 |
| `mistralai/Mistral-7B-v0.3` | 12 | 0.567 | 0.567 | 0.433 | +0.112 |
| `mistralai/Mistral-7B-v0.3` | 16 | 0.633 | 0.650 | 0.567 | +0.155 |
| `mistralai/Mistral-7B-v0.3` | 20 | 0.650 | 0.667 | 0.517 | +0.083 |
| `mistralai/Mistral-7B-v0.3` | 24 | 0.667 | 0.667 | 0.500 | +0.056 |
| `mistralai/Mistral-7B-v0.3` | 28 | 0.617 | 0.633 | 0.467 | +0.076 |
| `mistralai/Mistral-7B-v0.3` | 31 | 0.633 | 0.650 | 0.517 | +0.105 |

## Base vs Instruct deltas (Instruct - Base, per layer)
| Family | Layer | Δacc(H) | Δacc(A_HEX) | Δentangle_gap |
|---|---|---|---|---|
| `qwen/qwen2.5-7b` | 8 | -0.017 | -0.050 | -0.022 |
| `qwen/qwen2.5-7b` | 16 | -0.033 | -0.000 | +0.004 |
| `qwen/qwen2.5-7b` | 24 | -0.033 | -0.067 | +0.102 |
| `qwen/qwen2.5-7b` | 28 | +0.017 | -0.067 | +0.085 |
| `google/gemma-2-9b` | 4 | +0.017 | +0.050 | -0.063 |
| `google/gemma-2-9b` | 8 | +0.017 | +0.000 | +0.022 |
| `google/gemma-2-9b` | 12 | -0.033 | +0.017 | +0.110 |
| `google/gemma-2-9b` | 16 | -0.067 | +0.000 | +0.012 |
| `google/gemma-2-9b` | 20 | -0.033 | -0.033 | +0.012 |
| `google/gemma-2-9b` | 24 | -0.000 | -0.050 | +0.068 |
| `google/gemma-2-9b` | 28 | -0.033 | -0.083 | +0.100 |
| `google/gemma-2-9b` | 31 | -0.033 | +0.000 | +0.122 |
| `meta-llama/llama-3.1-8b` | 4 | -0.017 | +0.033 | -0.009 |
| `meta-llama/llama-3.1-8b` | 8 | -0.000 | -0.017 | +0.026 |
| `meta-llama/llama-3.1-8b` | 12 | -0.050 | -0.000 | -0.002 |
| `meta-llama/llama-3.1-8b` | 16 | +0.000 | +0.033 | -0.056 |
| `meta-llama/llama-3.1-8b` | 20 | +0.017 | +0.000 | +0.039 |
| `meta-llama/llama-3.1-8b` | 24 | +0.000 | -0.000 | -0.050 |
| `meta-llama/llama-3.1-8b` | 28 | +0.017 | -0.017 | +0.017 |
| `meta-llama/llama-3.1-8b` | 31 | -0.067 | -0.033 | +0.071 |
