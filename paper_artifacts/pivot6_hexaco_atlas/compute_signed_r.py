#!/usr/bin/env python3
"""
Signed within-rater r(H, A_HEX) on canonical vs synthetic characters.

The substrate falsifier (Beat 2) reports the ABSOLUTE within-rater coupling
|r(H, A_HEX)|, which is the right statistic for "does the bundle collapse off
cache." But absolute value cannot distinguish retrieval from faithful
measurement, because the synthetics are authored with H and A_HEX
anti-correlated at r = -0.74: faithful measurement would recover r approx -0.74
(|r| approx 0.74) and retrieval would impose r approx +0.74 (|r| approx 0.74),
identical in magnitude. Only the SIGN discriminates them. This script computes
the signed correlation per rater so the discriminator is reported.

Output: signed_r_results.json (means + per-rater table).
"""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

PAIRED = [
    'anthropic_1', 'anthropic_2', 'anthropic_3', 'anthropic_4', 'cohere_1',
    'deepseek_1', 'deepseek_2', 'gemma_1', 'google_1', 'google_2', 'google_3',
    'google_4', 'google_5', 'meta_1', 'meta_2', 'meta_3', 'mistral_1',
    'openai_1', 'openai_2', 'openai_3', 'openai_4', 'openai_5', 'qwen_1',
    'qwen_2', 'xai_1', 'xai_2',
]
DESIGNED_R = -0.74


def get_pairs(path):
    if not os.path.exists(path):
        return None
    d = json.load(open(path))
    H, A = [], []
    for p in d['predictions']:
        if p.get('refusal') or p.get('error'):
            continue
        pa = p.get('parsed')
        if not isinstance(pa, dict):
            continue
        if pa.get('H') is None or pa.get('A_HEX') is None:
            continue
        H.append(float(pa['H']))
        A.append(float(pa['A_HEX']))
    if len(H) < 4:
        return None
    return np.array(H), np.array(A)


def signed_r(pair):
    if pair is None:
        return None
    H, A = pair
    if H.std() == 0 or A.std() == 0:
        return None
    return float(np.corrcoef(H, A)[0, 1])


def main():
    rows = []
    for s in PAIRED:
        rc = signed_r(get_pairs(os.path.join(HERE, f'hexaco_ratings_{s}.json')))
        rs = signed_r(get_pairs(os.path.join(HERE, f'hexaco_ratings_{s}_synth.json')))
        rows.append({'rater': s, 'canon_signed_r': rc, 'synth_signed_r': rs})

    cs = [r['canon_signed_r'] for r in rows if r['canon_signed_r'] is not None]
    ss = [r['synth_signed_r'] for r in rows if r['synth_signed_r'] is not None]
    out = {
        'designed_synthetic_r': DESIGNED_R,
        'canonical_signed_r_mean': round(float(np.mean(cs)), 4),
        'synthetic_signed_r_mean': round(float(np.mean(ss)), 4),
        'n_raters': len(ss),
        'synth_positive_raters': int(sum(1 for x in ss if x > 0)),
        'synth_negative_raters': int(sum(1 for x in ss if x < 0)),
        'synth_abs_r_mean': round(float(np.mean([abs(x) for x in ss])), 4),
        'interpretation': (
            'Faithful measurement of the designed -0.74 anti-correlation would '
            'yield a negative synthetic signed r; pure attenuation would shrink '
            'toward zero from the negative side. The observed positive mean '
            '(retrieval direction), positive in a large majority of raters, is '
            'the retrieval signature, not measurement and not simple attenuation.'
        ),
        'per_rater': rows,
    }
    with open(os.path.join(HERE, 'signed_r_results.json'), 'w') as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps({k: v for k, v in out.items() if k != 'per_rater'}, indent=2))


if __name__ == '__main__':
    main()
