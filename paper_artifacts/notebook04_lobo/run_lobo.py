"""Compute LOBO-CV MAE using cached 3072-dim embeddings → 1536d slice.

For Notebook 04 to be self-contained at public release, we need cached
embeddings + a LOBO loop that runs offline. The private research repository's
`model_scores.json` per book already contains `mean_embedding` (3072d)
and ground-truth `consensus_ocean`. We:
  1. Aggregate (embedding, gt_ocean) pairs across all books with both
  2. Slice 3072d -> 1536d (Matryoshka head; text-embedding-3-large is
     trained for this)
  3. For each book held out, train an RF regressor on the remainder
     and predict on the held-out book
  4. Compute per-book MAE and overall mean

Output: paper_artifacts/notebook04_lobo/lobo_results.json
"""
from __future__ import annotations
import json, glob
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor

REPO = Path(".")
OUT = Path("paper_artifacts/notebook04_lobo")
OUT.mkdir(parents=True, exist_ok=True)
TRAITS = ["O", "C", "E", "A", "N"]
EMBED_SLICE = 1536  # Matryoshka slice from 3072d native

# Load (embedding, gt_ocean, book, name) per character
records = []
for ms_path in sorted(glob.glob(str(REPO / "rag_indices/*/pillar1/model_scores.json"))):
    book = ms_path.split("/")[-3]
    gt_path = REPO / f"rag_indices/{book}/pillar1/ground_truth.json"
    if not gt_path.exists():
        continue
    try:
        ms = json.loads(Path(ms_path).read_text())
        gt = json.loads(gt_path.read_text())
    except Exception:
        continue
    # GT is keyed by character_name or coref_id depending on schema
    gt_chars = gt.get("characters", [])
    gt_by_id = {}
    for c in gt_chars:
        cid = str(c.get("coref_id", ""))
        if not cid:
            continue
        # Prefer consensus_ocean (v3 schema), fall back to traits
        ocean = c.get("consensus_ocean") or c.get("traits") or {}
        if not all(t in ocean for t in TRAITS):
            continue
        gt_by_id[cid] = {t: float(ocean[t]) for t in TRAITS}

    ms_chars = ms.get("characters", {})
    for cid, char in ms_chars.items():
        gt = gt_by_id.get(str(cid))
        if not gt:
            continue
        emb = char.get("mean_embedding")
        if not emb or len(emb) < EMBED_SLICE:
            continue
        records.append({
            "book": book,
            "name": char.get("character_name", ""),
            "coref_id": cid,
            "embedding": np.array(emb[:EMBED_SLICE], dtype=np.float32),
            "gt": np.array([gt[t] for t in TRAITS], dtype=np.float32),
        })

n = len(records)
books = sorted(set(r["book"] for r in records))
print(f"Loaded {n} (embedding, gt) records across {len(books)} books.")
print(f"Embedding dim: {EMBED_SLICE} (sliced from 3072 native)")

# LOBO
print(f"\nRunning leave-one-book-out CV ({len(books)} books)...")
per_book_mae = {}
all_residuals = []
for held_book in books:
    train = [r for r in records if r["book"] != held_book]
    test  = [r for r in records if r["book"] == held_book]
    if not test:
        continue
    X_train = np.stack([r["embedding"] for r in train])
    y_train = np.stack([r["gt"] for r in train])
    X_test  = np.stack([r["embedding"] for r in test])
    y_test  = np.stack([r["gt"] for r in test])
    rf = RandomForestRegressor(n_estimators=300, max_depth=15,
                                 random_state=20260427, n_jobs=-1)
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)
    char_maes = np.mean(np.abs(y_pred - y_test), axis=1)
    per_book_mae[held_book] = {
        "n": len(test),
        "mae": float(char_maes.mean()),
        "char_maes": char_maes.tolist(),
    }
    all_residuals.extend(char_maes.tolist())
    print(f"  {held_book[:35]:<35} n={len(test):<4} MAE={char_maes.mean():.4f}")

# Overall
overall_mean = float(np.mean(all_residuals))
overall_sd = float(np.std(all_residuals))
n_total = len(all_residuals)
# Bootstrap CI
rng = np.random.default_rng(20260427)
boots = [np.mean(rng.choice(all_residuals, size=n_total, replace=True))
         for _ in range(2000)]
ci_lo, ci_hi = float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))

print(f"\n{'='*60}")
print(f"LOBO-CV summary (n={n_total} chars across {len(books)} books)")
print(f"{'='*60}")
print(f"  Mean MAE: {overall_mean:.4f}")
print(f"  SD:       {overall_sd:.4f}")
print(f"  95% CI (bootstrap, n=2000): [{ci_lo:.4f}, {ci_hi:.4f}]")
print(f"  distillation baseline: 0.309 [0.303, 0.316] (28 novels)")

# Save
out = {
    "lobo_date": "2026-04-27",
    "n_records": n_total,
    "n_books": len(books),
    "embedding_dim": EMBED_SLICE,
    "regressor": {
        "type": "RandomForestRegressor",
        "n_estimators": 300,
        "max_depth": 15,
        "random_state": 20260427,
    },
    "summary": {
        "mean_mae": overall_mean,
        "sd_mae": overall_sd,
        "ci_95_low": ci_lo,
        "ci_95_high": ci_hi,
    },
    "per_book": per_book_mae,
    "distillation_baseline": {
        "mae": 0.309,
        "ci_95": [0.303, 0.316],
        "n_books": 28,
    },
}
out_path = OUT / "lobo_results.json"
out_path.write_text(json.dumps(out, indent=2) + "\n")
print(f"\nSaved {out_path}")
