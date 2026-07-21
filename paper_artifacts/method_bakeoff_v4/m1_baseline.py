#!/usr/bin/env python3
"""M1 -- the training-free embedding-prototype baseline (the Paper-1 method,
computed on this paper's corpus for completeness).

M1 scores a character by the cosine similarity of its 3072-d embedding to each
OCEAN factor's mean trait-anchor embedding; no fitted model. Cosine scores are
mapped to the trait scale by a training-free calibration (per-factor z-score, then
rescaled to the ground-truth marginal mean/std -- a corpus-level transform that
uses no per-character ground truth). M1 is a Bar-1 (ground-truth-recovery)
baseline only; it is not carried into the convergent-validity (Bar 2) analysis.

Outputs the leaderboard row (MAE / Pearson r / CCC + 10,000-resample bootstrap CIs)
to m1_baseline_results.json. Reproducible, deterministic (seeded).
"""
import csv, ast, json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ANCHORS = "personality_models/ocean_embeddings_3072.csv"
EMB = os.path.join(HERE, "..", "pivot6_hexaco_atlas", "embeddings", "canonical_embeddings_3072d.npz")
GT = os.path.join(HERE, "per_llm_bakeoff.csv")

FACTORS = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]
TRAIT = {"Openness": "O", "Conscientiousness": "C", "Extraversion": "E",
         "Agreeableness": "A", "Neuroticism": "N"}
RNG = np.random.default_rng(42)
NBOOT = 10000


def unit(v):
    return v / np.clip(np.linalg.norm(v, axis=-1, keepdims=True), 1e-9, None)


def ccc(x, y):
    vx, vy = x.var(), y.var()
    return 2 * np.cov(x, y)[0, 1] / (vx + vy + (x.mean() - y.mean()) ** 2)


# anchors -> 5 factor-mean unit vectors
fa = {f: [] for f in FACTORS}
for r in csv.DictReader(open(ANCHORS)):
    fa[r["Factor"]].append(ast.literal_eval(r["Embedding"]))
anchors_u = unit(np.array([np.mean(fa[f], axis=0) for f in FACTORS]))

z = np.load(os.path.abspath(EMB), allow_pickle=True)
emb_u = unit(z["embeddings"].astype(np.float64))
books, corefs, names = z["books"], z["corefs"], z["names"]

# GT keyed by (book, coref_id) ONLY (no name fallback, which over-matched and
# double-counted); one GT vector per (book, coref).
gt_by_coref = {}
for r in csv.DictReader(open(GT)):
    try:
        v = {t: float(r["gt_" + t]) for t in "OCEAN"}
    except (ValueError, KeyError):
        continue
    gt_by_coref.setdefault((r["book"], r["coref_id"]), v)

cos, gtv = [], []
seen = set()
for i in range(len(emb_u)):
    key = (str(books[i]), str(corefs[i]))
    if key in seen:
        continue
    g = gt_by_coref.get(key)
    if g is None:
        continue
    seen.add(key)
    cos.append(anchors_u @ emb_u[i])
    gtv.append([g[TRAIT[f]] for f in FACTORS])
cos, gtv = np.array(cos), np.array(gtv)        # (n, 5)
n = len(cos)

# training-free calibration per factor: z-score -> GT marginal mean/std
pred = np.zeros_like(cos)
for j in range(5):
    x = cos[:, j]
    xz = (x - x.mean()) / (x.std() + 1e-9)
    pred[:, j] = xz * gtv[:, j].std() + gtv[:, j].mean()


def metrics(idx):
    p, g = pred[idx].ravel(), gtv[idx].ravel()
    return np.mean(np.abs(p - g)), np.corrcoef(p, g)[0, 1], ccc(p, g)


mae, r, c = metrics(np.arange(n))
bo = np.array([metrics(RNG.integers(0, n, n)) for _ in range(NBOOT)])
ci = lambda k: [round(float(np.percentile(bo[:, k], 2.5)), 3), round(float(np.percentile(bo[:, k], 97.5)), 3)]

out = {
    "method": "M1 (training-free embedding prototype)",
    "n_characters": int(n),
    "MAE": round(float(mae), 3), "MAE_CI": ci(0),
    "pearson_r": round(float(r), 3), "r_CI": ci(1),
    "CCC": round(float(c), 3), "CCC_CI": ci(2),
    "per_trait_r": {TRAIT[FACTORS[j]]: round(float(np.corrcoef(pred[:, j], gtv[:, j])[0, 1]), 3) for j in range(5)},
    "note": ("Bar-1 baseline only (not in the Bar-2 convergent matrix). Cosine scores "
             "calibrated to the GT marginal per factor (training-free, no per-character "
             "GT fitting). Computed by m1_baseline.py."),
}
json.dump(out, open(os.path.join(HERE, "m1_baseline_results.json"), "w"), indent=2)
print(json.dumps(out, indent=2))
