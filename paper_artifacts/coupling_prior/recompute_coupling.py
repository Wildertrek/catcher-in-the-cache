#!/usr/bin/env python3
"""
recompute_coupling.py -- verify the coupling-prior numbers from cached ratings ($0).

Reproduces the paper's coupling-prior result: rating 20 synthetic (out-of-corpus)
characters from their NAME ALONE yields a strongly fused r(H, A_HEX) ~ +0.83, while
rating them from their TEXT recovers the designed anti-correlation ~ -0.45.

Inputs (shipped): responses_holistic.csv  (rater_id, panel_id, condition, H, A_HEX)
                  panel_kind.json          (panel_id -> canonical|synthetic)
Usage: python recompute_coupling.py
"""
import csv, json, os
from collections import defaultdict
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(f"{HERE}/responses_holistic.csv")))
kind = json.load(open(f"{HERE}/panel_kind.json"))
cell = defaultdict(lambda: {"H": [], "A": []})
for r in rows:
    cell[(r["panel_id"], r["condition"])]["H"].append(float(r["H"]))
    cell[(r["panel_id"], r["condition"])]["A"].append(float(r["A_HEX"]))


def rci(ps, cond):
    H = np.array([np.mean(cell[(p, cond)]["H"]) for p in ps if cell[(p, cond)]["H"]])
    A = np.array([np.mean(cell[(p, cond)]["A"]) for p in ps if cell[(p, cond)]["A"]])
    r = np.corrcoef(H, A)[0, 1]
    idx = np.random.default_rng(1).integers(0, len(H), (4000, len(H)))
    xs, ys = H[idx], A[idx]
    xc, yc = xs - xs.mean(1, keepdims=True), ys - ys.mean(1, keepdims=True)
    den = np.sqrt((xc ** 2).sum(1) * (yc ** 2).sum(1))
    bs = np.divide((xc * yc).sum(1), den, out=np.full(4000, np.nan), where=den > 0)
    return r, np.nanpercentile(bs, 2.5), np.nanpercentile(bs, 97.5)


print(f"{'substrate':>10} | {'name_only':>18} | {'redacted':>18} | {'full':>18}")
for sub in ("canonical", "synthetic"):
    ps = [p for p in kind if kind[p] == sub]
    cols = []
    for cond in ("name_only", "redacted", "full"):
        r, lo, hi = rci(ps, cond)
        cols.append(f"{r:+.3f} [{lo:+.2f},{hi:+.2f}]")
    print(f"{sub:>10} | " + " | ".join(f"{c:>18}" for c in cols))
print("\nHeadline: synthetic name-only ~ +0.83 (fused prior, no text, characters that "
      "do not exist) vs synthetic-from-text ~ -0.45 (recovers the designed structure).")
