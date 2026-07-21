"""Consensus metrics: PA, TD, CMC, RCS.

Ported from the parent research repository's scripts/compute_pillar1_metrics.py.
Self-contained: reads ground-truth JSON files in the v3 multi-source schema
(with graceful fallback to older v2 / legacy formats) and consensus-run JSON
files produced by `consensus_runner.run_consensus`.
"""
from __future__ import annotations

import json
import math
from itertools import combinations
from pathlib import Path
from statistics import mean
from typing import Any

TRAITS = ["O", "C", "E", "A", "N"]


# ---------------------------------------------------------------------------
# Ground-truth loading
# ---------------------------------------------------------------------------

def load_ground_truth(path: Path | str) -> dict[str, dict[str, float]]:
    """Load a ground-truth JSON file and return {coref_id: {trait: score}}.

    Handles v3 multi-source, v2 framework-aware, and legacy flat schemas.
    """
    with open(path) as f:
        data = json.load(f)
    out: dict[str, dict[str, float]] = {}
    for char in data.get("characters", []):
        scores = _extract_scholarly_scores(char)
        if scores:
            key = char.get("coref_id") or char.get("canonical_name") or char.get("character_name")
            if key:
                out[key] = scores
    return out


def _extract_scholarly_scores(gt_char: dict[str, Any]) -> dict[str, float]:
    """Extract OCEAN scores from a ground-truth character record.

    Priority (matches parent-repo behavior): v3 consensus_ocean,
    v2 ocean_scores, traits dict, bare top-level OCEAN, per-source fallback.
    """
    scores: dict[str, float] = {}

    if gt_char.get("consensus_ocean"):
        for t in TRAITS:
            v = gt_char["consensus_ocean"].get(t)
            if isinstance(v, (int, float)):
                scores[t] = float(v)

    if not scores and gt_char.get("ocean_scores"):
        for t in TRAITS:
            entry = gt_char["ocean_scores"].get(t, {}) or {}
            if entry.get("score") is not None:
                scores[t] = float(entry["score"])

    if not scores and "traits" in gt_char:
        for t in TRAITS:
            v = gt_char["traits"].get(t)
            if isinstance(v, (int, float)):
                scores[t] = float(v)

    if not scores:
        for t in TRAITS:
            v = gt_char.get(t)
            if isinstance(v, (int, float)):
                scores[t] = float(v)

    if not scores and gt_char.get("sources"):
        for src in gt_char["sources"]:
            if src.get("ocean"):
                for t in TRAITS:
                    v = src["ocean"].get(t)
                    if isinstance(v, (int, float)):
                        scores[t] = float(v)
            if scores:
                break
            osv2 = src.get("ocean_scores_v2") or {}
            for t in TRAITS:
                entry = osv2.get(t, {}) or {}
                if entry.get("score") is not None:
                    scores[t] = float(entry["score"])
            if scores:
                break

    return scores


# ---------------------------------------------------------------------------
# PA, Profile Accuracy
# ---------------------------------------------------------------------------

def compute_pa_mae(
    consensus: dict[str, float],
    scholarly: dict[str, float],
) -> tuple[float | None, dict[str, float]]:
    """Profile Accuracy as mean absolute error. Lower is better.

    Returns (mean_error, per_trait_errors). `None` if no shared traits.
    """
    shared = [t for t in TRAITS if t in consensus and t in scholarly]
    if not shared:
        return None, {}
    errors = {t: abs(consensus[t] - scholarly[t]) for t in shared}
    return mean(errors.values()), errors


def compute_pa_pearson(
    consensus: dict[str, float],
    scholarly: dict[str, float],
) -> float | None:
    """Profile Accuracy as Pearson correlation. Higher is better.

    Requires at least 3 shared traits. Returns `None` otherwise or on
    zero-variance vectors.
    """
    shared = [t for t in TRAITS if t in consensus and t in scholarly]
    if len(shared) < 3:
        return None
    c = [consensus[t] for t in shared]
    s = [scholarly[t] for t in shared]
    cm, sm = mean(c), mean(s)
    num = sum((ci - cm) * (si - sm) for ci, si in zip(c, s))
    den_c = math.sqrt(sum((ci - cm) ** 2 for ci in c))
    den_s = math.sqrt(sum((si - sm) ** 2 for si in s))
    if den_c == 0 or den_s == 0:
        return None
    return num / (den_c * den_s)


# ---------------------------------------------------------------------------
# TD, Trait Distinctiveness
# ---------------------------------------------------------------------------

def _euclidean(v1: dict[str, float], v2: dict[str, float]) -> float:
    return math.sqrt(sum((v1.get(t, 0.0) - v2.get(t, 0.0)) ** 2 for t in TRAITS))


def compute_td(
    consensus_vectors: list[tuple[int, str, dict[str, float]]],
) -> dict[str, Any]:
    """Trait Distinctiveness via mean pairwise Euclidean distance.

    Args:
        consensus_vectors: List of ``(index, character_name, trait_vector)``.

    Returns dict with mean/median/min/max distances, pair count, and the
    three most-similar and three most-distinct character pairs.
    """
    distances: list[float] = []
    pairs: list[tuple[str, str, float]] = []
    for (_, n1, v1), (_, n2, v2) in combinations(consensus_vectors, 2):
        d = _euclidean(v1, v2)
        distances.append(d)
        pairs.append((n1, n2, d))
    if not distances:
        return {"mean": 0.0, "median": 0.0, "min": 0.0, "max": 0.0, "n_pairs": 0,
                "most_similar": [], "most_distinct": []}
    pairs.sort(key=lambda x: x[2])
    sorted_d = sorted(distances)
    return {
        "mean": mean(distances),
        "median": sorted_d[len(sorted_d) // 2],
        "min": min(distances),
        "max": max(distances),
        "n_pairs": len(distances),
        "most_similar": pairs[:3],
        "most_distinct": pairs[-3:],
    }


# ---------------------------------------------------------------------------
# CMC, Cross-Model Consistency
# ---------------------------------------------------------------------------

def compute_cmc(characters_data: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Cross-Model Consistency: ``1 - mean(trait variance across providers)``.

    Args:
        characters_data: Per character, a dict with keys:
            - ``character_name``
            - ``vectors``: list of per-provider records, each with a
              ``vector`` dict holding OCEAN scores.

    Returns a mapping ``{character_name: {cmc, trait_variances, n_providers}}``.
    Characters with fewer than two providers are skipped.
    """
    results: dict[str, dict[str, Any]] = {}
    for char in characters_data:
        name = char.get("character_name")
        vectors = char.get("vectors", [])
        if not name or len(vectors) < 2:
            continue
        trait_vars: dict[str, float] = {}
        for t in TRAITS:
            vals = [v["vector"].get(t) for v in vectors if v.get("vector", {}).get(t) is not None]
            if len(vals) >= 2:
                m = mean(vals)
                trait_vars[t] = mean((x - m) ** 2 for x in vals)
        if trait_vars:
            results[name] = {
                "cmc": 1.0 - mean(trait_vars.values()),
                "trait_variances": {t: round(v, 4) for t, v in trait_vars.items()},
                "n_providers": len(vectors),
            }
    return results


# ---------------------------------------------------------------------------
# RCS, Repeat Consistency Score
# ---------------------------------------------------------------------------

def compute_rcs(runs: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Repeat Consistency Score across multiple consensus runs.

    Args:
        runs: List of run records, each with a ``characters`` list whose
            entries carry a ``consensus`` dict of aggregated OCEAN scores.

    Returns a per-character mapping ``{name: {rcs, trait_variances, n_runs}}``.
    Characters appearing in fewer than two runs are skipped.
    """
    grouped: dict[str, list[tuple[str, dict[str, float]]]] = {}
    for run in runs:
        for char in run.get("characters", []):
            key = char.get("coref_id") or char.get("character_name")
            cons = char.get("consensus") or {}
            if key and cons:
                grouped.setdefault(key, []).append(
                    (char.get("character_name", key), cons)
                )

    results: dict[str, dict[str, Any]] = {}
    for key, entries in grouped.items():
        if len(entries) < 2:
            continue
        name = entries[0][0]
        consensuses = [c for _, c in entries]
        trait_vars: dict[str, float] = {}
        for t in TRAITS:
            vals = [c.get(t) for c in consensuses if c.get(t) is not None]
            if len(vals) >= 2:
                m = mean(vals)
                trait_vars[t] = mean((x - m) ** 2 for x in vals)
        if trait_vars:
            results[name] = {
                "rcs": 1.0 - mean(trait_vars.values()),
                "trait_variances": {t: round(v, 4) for t, v in trait_vars.items()},
                "n_runs": len(entries),
            }
    return results
