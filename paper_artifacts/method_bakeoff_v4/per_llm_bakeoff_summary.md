# Per-LLM head-to-head against weighted multi-source GT

Total characters with per-provider data: 551

## Overall MAE / r per provider (lower MAE = better)

| Provider | n chars | MAE | MAE 95% CI | Pearson r |
|----------|---------|-----|------------|-----------|
| Anthropic | 556 | 0.286 | [0.276, 0.295] | 0.742 |
| OpenAI | 557 | 0.242 | [0.235, 0.250] | 0.738 |
| Google | 540 | 0.306 | [0.296, 0.315] | 0.663 |

## Per-trait MAE per provider

| Provider | O | C | E | A | N |
|----------|---|---|---|---|---|
| Anthropic | 0.287 | 0.266 | 0.274 | 0.251 | 0.351 |
| OpenAI | 0.220 | 0.249 | 0.225 | 0.246 | 0.270 |
| Google | 0.251 | 0.318 | 0.409 | 0.254 | 0.297 |

## Per-trait Pearson r per provider

| Provider | O | C | E | A | N |
|----------|---|---|---|---|---|
| Anthropic | 0.739 | 0.739 | 0.703 | 0.848 | 0.678 |
| OpenAI | 0.731 | 0.714 | 0.709 | 0.831 | 0.710 |
| Google | 0.683 | 0.672 | 0.530 | 0.804 | 0.716 |