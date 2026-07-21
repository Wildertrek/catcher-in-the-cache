"""Recompute every Experiment 2/3 headline on the standardized 25-rater panel.

Why this exists
---------------
The paper standardized on a single 25-rater panel (one Grok 4.3 run; the Amendment-9
additions Hermes-3 and Jamba were never re-run on the synthetic substrate and were
dropped). The committed notebook outputs in this directory predate that change and
report the superseded 26-model panel, so a reviewer following the RQ-coverage table
sees delta = -0.451 where the paper reports -0.447. This script derives the paper's
numbers from the same committed CSV so the companion and the paper agree.

The 25-rater panel = every row of synthetic_vs_canonical.csv except `xai_2`, which is
a duplicate run of the same model (x-ai/grok-4.3) at the same seed as `xai_1`.

Run:  python compute_panel25.py        (writes panel25_results.json next to this file)
Deterministic: permutation seed is fixed below and recorded in the output.
"""
import csv, json, os, numpy as np
from scipy.stats import wilcoxon, binomtest

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "synthetic_vs_canonical.csv")
DROP = {"xai_2"}                      # duplicate Grok 4.3 run
SEED, N_PERM = 42, 200_000

# provider family per slot prefix; Gemma is a Google model, folded into Google (9 families)
FAMILY = {"anthropic": "Anthropic", "openai": "OpenAI", "google": "Google", "gemma": "Google",
          "xai": "xAI", "cohere": "Cohere", "meta": "Meta", "qwen": "Qwen",
          "deepseek": "DeepSeek", "mistral": "Mistral"}

rows = [r for r in csv.DictReader(open(SRC)) if r["slot"] not in DROP]
canon = np.array([float(r["abs_r_canon"]) for r in rows])
synth = np.array([float(r["abs_r_synth"]) for r in rows])
fam = np.array([FAMILY[r["slot"].rsplit("_", 1)[0]] for r in rows])

delta = synth - canon


def eta_squared(labels, y):
    grand = y.mean()
    ssb = sum((y[labels == f].size) * (y[labels == f].mean() - grand) ** 2 for f in set(labels))
    return ssb / ((y - grand) ** 2).sum()


def icc1(labels, y):
    """One-way random-effects ICC(1) over unequal group sizes."""
    groups = [y[labels == f] for f in sorted(set(labels))]
    k, n = len(groups), y.size
    grand = y.mean()
    msb = sum(g.size * (g.mean() - grand) ** 2 for g in groups) / (k - 1)
    msw = sum(((g - g.mean()) ** 2).sum() for g in groups) / (n - k)
    k0 = (n - sum(g.size ** 2 for g in groups) / n) / (k - 1)
    return (msb - msw) / (msb + (k0 - 1) * msw)


obs_eta = eta_squared(fam, canon)
rng = np.random.default_rng(SEED)
ge = sum(eta_squared(rng.permutation(fam), canon) >= obs_eta for _ in range(N_PERM))
p_raw = (ge + 1) / (N_PERM + 1)

# --- signed r: the retrieval-vs-measurement discriminator ------------------
# |r| discards the sign that separates retrieval from measurement. The synthetics were
# authored anti-correlated (designed r = -0.74), so faithful measurement predicts a
# negative synthetic signed r. signed_r_results.json in the parent directory is the
# superseded 26-rater version; these are the 25-rater values the paper reports.
signed = json.load(open(os.path.join(HERE, "..", "signed_r_results.json")))
srows = [r for r in signed["per_rater"] if r["rater"] not in DROP]
s_syn = np.array([r["synth_signed_r"] for r in srows])
s_can = np.array([r["canon_signed_r"] for r in srows])
_rng = np.random.default_rng(SEED)
_boot = np.array([_rng.choice(s_syn, s_syn.size, replace=True).mean() for _ in range(20_000)])
n_pos = int((s_syn > 0).sum())

# --- the BH-FDR family -----------------------------------------------------
# Composition is fixed by the pre-registration artifact bh_fdr_pivot6_results.json
# (family_size = 5). RQ6.7 is excluded there because it was retracted; RQ6.1 uses a
# Wilson CI rather than a p-value and is reported separately. The three tests that do
# not depend on this panel keep their recorded p_raw.
W, p_wilcoxon = wilcoxon(synth, canon, alternative="less")
BH_FAMILY = [
    ("RQ6.9_PRIOR_DRIVEN", float(p_wilcoxon)),   # recomputed on this panel
    ("H2_family_clustering", float(p_raw)),      # recomputed on this panel
    ("H4_open_vs_closed", 0.1619),               # from bh_fdr_pivot6_results.json
    ("H3_capability_correlation", 0.4749),       # from bh_fdr_pivot6_results.json
    ("H5_head_to_head_proxy", 1.0),              # from bh_fdr_pivot6_results.json
]
ordered = sorted(BH_FAMILY, key=lambda kv: kv[1])
m = len(ordered)
bh, running_min = {}, 1.0
for i, (name, p) in enumerate(reversed(ordered), 1):
    running_min = min(running_min, p * m / (m - i + 1))
    bh[name] = running_min

out = {
    "panel": "25 distinct LLM raters, 9 provider families (Gemma folded into Google)",
    "excluded": sorted(DROP),
    "exclusion_reason": "duplicate run of x-ai/grok-4.3 at the same seed as xai_1",
    "n_raters": len(rows),
    "n_families": len(set(fam)),
    "canonical_mean_abs_r": round(float(canon.mean()), 4),
    "synthetic_mean_abs_r": round(float(synth.mean()), 4),
    "mean_delta": round(float(delta.mean()), 4),
    "n_decreased": int((delta < 0).sum()),
    "raters_above_030_canonical": int((canon >= 0.30).sum()),
    "raters_below_030_synthetic": int((synth < 0.30).sum()),
    "signed_r": {
        "designed_synthetic_r": signed["designed_synthetic_r"],
        "canonical_signed_mean": round(float(s_can.mean()), 4),
        "synthetic_signed_mean": round(float(s_syn.mean()), 4),
        "synthetic_ci95": [round(float(x), 3) for x in np.percentile(_boot, [2.5, 97.5])],
        "n_positive": n_pos,
        "n_raters": int(s_syn.size),
        "sign_test_p": round(float(binomtest(n_pos, s_syn.size, 0.5).pvalue), 4),
        "note": ("Positive synthetic mean is the retrieval signature: faithful measurement of the "
                 "designed -0.74 would be negative, and simple attenuation would shrink toward zero "
                 "from the negative side rather than flipping sign."),
    },
    "bh_fdr_family": {
        "family_size": m,
        "composition_source": "bh_fdr_pivot6_results.json (pre-registered, family_size=5)",
        "ranks_ascending": [n for n, _ in ordered],
        "p_raw": {n: p for n, p in ordered},
        "p_bh_adjusted": {n: bh[n] for n, _ in ordered},
        "note": ("H2_family_clustering sits at rank 2 of 5, so its BH-adjusted p is p_raw * 5/2. "
                 "RQ6.9's BH-adjusted p is its one-sided p_raw * 5/1; note the paper's 6.0e-8 is the "
                 "two-sided UNADJUSTED Wilcoxon p (5.96e-8), not a BH-adjusted value."),
    },
    "wilcoxon_rq69": {
        "W": float(W),
        "p_one_sided": float(p_wilcoxon),
        "p_two_sided": float(wilcoxon(synth, canon, alternative="two-sided")[1]),
    },
    "family_clustering": {
        "icc1": round(float(icc1(fam, canon)), 4),
        "eta_squared": round(float(obs_eta), 4),
        "permutation_p_raw": round(float(p_raw), 5),
        "n_permutations": N_PERM,
        "seed": SEED,
        "note": ("p_raw is the unadjusted permutation p. The paper reports the "
                 "BH-adjusted value over the RQ2 inferential family; the adjustment "
                 "depends on this test's rank within that family."),
    },
}
if __name__ == "__main__":
    dst = os.path.join(HERE, "panel25_results.json")
    json.dump(out, open(dst, "w"), indent=2)
    print(json.dumps(out, indent=2))
    print(f"\nwrote {dst}")
