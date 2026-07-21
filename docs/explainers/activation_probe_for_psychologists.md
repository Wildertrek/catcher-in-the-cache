# The Activation Probe, for Psychologists Who Don't Read ML Papers

> §4.4 of the paper runs an *activation probe* on open-weight LLMs at
> 7B–72B scale. If "activation probe," "layer-depth dissociation," and
> "mean-pool-256" are foreign vocabulary, this is the explainer.

The activation probe is what lets the paper claim that the
canonical-prior signal isn't just a property of LLM outputs (which a
prompted-rating experiment could hide) but is sitting in the
*representations* of the LLM itself, layer by layer.

---

## What an LLM looks like, from the outside

Picture a transformer LLM as a stack of $L$ identical processing
layers. A text input enters at layer 0, flows through layers 1, 2,
3, ..., $L$, and a final read-out head emits the next-token
prediction (or, for chat, the response).

At every layer, the model carries a **hidden state** for every token
in the input: a $d$-dimensional vector (typically $d \in [4096, 8192]$
for modern models). That vector is the model's "current representation"
of that token's meaning at that layer.

The hidden states are *the* internal substrate of the model. Everything
the model knows is encoded in them. So if a model has memorized
Elizabeth Bennet's personality from training data, that memorization
shows up *in the hidden states for a Bennet input*, at some layer,
in some form.

The activation probe is the tool that asks: yes or no?

---

## What "activation probe" means concretely

For an open-weight LLM (Llama, Qwen, Mistral, etc., where we can
inspect internals), we do this:

1. **Feed the model a character's evidence pack** (the same text any
   M4 rater would see, character utterances + context).
2. **Capture the hidden states at every layer** for every token in
   the input.
3. **Reduce to one fixed vector per (model, character, layer)** by
   averaging across tokens. (We use mean-pool-256: average the
   first 256 tokens' hidden states. Other "pool variants" are
   max-pool, last-token, attention-weighted; we tested these in the
   pool-ablation contrast.)
4. **Train a small probe** (a Ridge regressor or an MLP) to predict
   the ground-truth OCEAN/HEXACO trait from that fixed vector.
5. **Score on held-out characters.** If the probe's predictions
   correlate well with GT, the trait information was *present in
   that layer's hidden states*.

The probe is the read-out tool. It is not the model. It is a thin
diagnostic regression that asks: "is this trait recoverable from
this layer's representations?"

---

## What "layer-depth dissociation" means

We run the probe at 5 depth percentiles: 12.5% / 25% / 50% / 75% /
87.5% of the model's layer count. So a Llama-70B with 80 layers
gets probed at layers 10, 20, 40, 60, 70.

**The finding:** trait-relevant correlation goes *up* with depth in
three independent model families at 70B+ scale.

| Family | At ~12% depth | At ~87% depth |
|---|---|---|
| Llama-70B-Instruct (Meta) | $r = +0.80$ | $r = +0.07$ |
| Qwen-72B | (similar gradient, $\Delta_{\mathrm{depth}} = -1.05$) | |
| Mistral-MoE-8×22B | (similar gradient) | |

(Numbers are the load-bearing Ridge probe on HEXACO-H. Llama-70B
shows the strongest gradient on mean-pool only; Mixtral shows it on
all pool variants. The pool-ablation finding below.)

The reverse direction would be "layer flat", no trait signal
distinguishable across layers. We rule that out at $\Delta = -0.73$
to $-1.05$.

### What this means in psychometric language

If the model is "measuring" the trait from text in front of it, we'd
expect the trait signal to *emerge gradually* through depth as more
linguistic processing happens, a shallow-to-deep building of
representation. That's the standard ML interpretability story.

If the model is "retrieving" a stored character prior from training,
we'd expect the trait signal to be *present near the top* (where
memorized facts about famous entities are known to live) and *less
present in the middle layers* (where general linguistic processing
happens).

The Llama-70B result fits the retrieval profile. The convergence on
three independent 70B+ families across two architectural categories
(dense and sparse-MoE) is what makes it a finding rather than a
single-model curiosity.

---

## Mean-pool, max-pool, attention-pool, pool-ablation

When you have hidden states for 256 input tokens and you want one
vector per character, you have to pool them. The standard choices:

| Pool variant | What it does | When it works |
|---|---|---|
| **Mean-pool-256** | Average across all 256 tokens | Distributes signal evenly; what we report by default |
| **Max-pool** | Take the dimensionwise maximum | Captures peak salience features |
| **Last-token** | Just use the last token's hidden state | Captures the model's "summary representation"; standard for some interpretability work |
| **Attention-pool** | Attention-weighted average | Mimics what the model itself would do downstream |

The **pool-ablation contrast (§4.4)** compares the depth-gradient
across pool variants:

- **Llama-70B (dense):** depth gradient appears *only* on mean-pool.
  Max-pool and last-token are flat.
- **Mixtral-8×22B (sparse-MoE):** depth gradient appears *across all*
  pool variants.

This is interpreted as an architectural-conditional finding: the
sparse-MoE routing in Mixtral spreads the canonical-prior signal more
uniformly across the residual stream, while Llama concentrates it in
positionally-distributed traces that only mean-pool recovers.

---

## Ridge vs MLP probe (and why one is load-bearing)

| Probe | What it is | Use in paper |
|---|---|---|
| **Ridge** | L2-regularized linear regression: $\hat y = w^T x + b$ with penalty on $\|w\|^2$ | **Load-bearing.** All headline numbers in §4.4 are Ridge. |
| **MLP** | 1 × 64-unit hidden-layer feedforward neural net | **Sensitivity check only.** |

Why the asymmetry? The training substrate for the probe is the same
$n = 60$ canonical characters. A 1×64 MLP with thousands of parameters
can overfit a regression problem with only 60 training points, and
in our non-linear-probe refit, it did: 75 of 79 (model, layer) cells had
*negative* $R^2$ on the held-out half, which means the MLP was worse
than predicting the mean.

A Ridge probe with strong L2 penalty doesn't have that pathology.
It's the load-bearing read-out; the MLP is reported as the *direction*
check ("does the trait signal exist at all?") rather than as a
quantitative result.

This is why §4.4's Table~1 row reads *"Activation probe: MLP probe
robustness (substrate-underpowered)"*, we ran it, we report it, and
we flag explicitly that the $n=60$ substrate is too small for MLP
inference.

---

## Dense vs sparse-MoE (one-paragraph)

A **dense** transformer activates every parameter on every token.
A **sparse-mixture-of-experts (MoE)** transformer activates only a
subset of "expert" feed-forward blocks per token, gated by a routing
network. Mixtral-8×22B has 8 experts; ~2 are active per token.

For the activation probe this matters because the *information
geometry* of a sparse-MoE residual stream is shaped by the gating
decisions, not just the linear processing depth. The pool-ablation
finding is the empirical signature: dense models concentrate the
canonical-prior signal positionally; sparse-MoE distributes it.

---

## What you'd see if the probe were *not* working

To rule out the "we trained any probe and got a number out" reading:

- **Mean cross-character $r$ for shuffled-label baselines** ≈ 0 in
  every cell (see appendix tables).
- **Within-trait shuffle test**: shuffling GT labels across characters
  destroys the depth gradient.
- **Across-pool consistency**: the dense-MoE difference is a
  controllable variable, not a confound, both architectures get
  the same probe code path.

These sanity checks live in `paper_artifacts/pivot6_hexaco_atlas/`
in the companion repo.

---

## Bottom line

The activation probe is a thin diagnostic regressor that read out a
specific question from open-weight LLM internals: *"is the
canonical-prior signal sitting in the model's hidden states, and
where?"* Answer: yes, with a depth gradient that scales to 70B+ across
three independent architectures. That's harder to reconcile with
"measurement from text" than with "retrieval against a memorized
character prior."

Further detail: see [`CATCHER.md` §4.2](../../CATCHER.md) and notebooks
[`08_activation_probe_dissociation`](../../notebooks/08_activation_probe_dissociation.ipynb)
/ [`09_catcher_in_the_cache`](../../notebooks/09_catcher_in_the_cache.ipynb).
