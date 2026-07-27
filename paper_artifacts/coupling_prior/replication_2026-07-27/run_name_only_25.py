#!/usr/bin/env python3
"""Scale the coupling-prior name-only cell from 3 providers to the frontier panel.

WHY. Paper 2's identification argument turns on a within-synthetic contrast: the SAME 20
synthetic characters fuse H with A at +0.83 rated from a name alone, and collapse to +0.23
rated from their text. Identical characters across those cells, so vividness and prose
quality are held constant and the evaluative-halo alternative cannot explain the swing.
That name-only cell currently rests on 3 providers while every other headline uses 25.
The companion already calls a frontier replication "the planned camera-ready step".

PROMPT PARITY IS THE POINT. The prompt below is copied verbatim from
human_panel_kit/analysis/holistic_probe.py, which produced the +0.83. Change it and the
comparison to the existing number is not clean.

PRE-REGISTERED (see SPEC.md):
  P1  synthetic name-only fusion stays high on the frontier panel, r(H,A) >= +0.5
  P2  it exceeds the same panel's synthetic TEXT fusion (+0.23) by >= 0.3
  FALSIFIER: < +0.3, or not exceeding the text cell -> the halo alternative is NOT
  excluded, and the identification argument in Experiment 3 must be withdrawn.

Usage: python run_name_only_25.py --smoke      (3 raters x 3 chars, a few cents)
       python run_name_only_25.py              (full roster x 20 chars)
"""
import argparse, csv, json, os, re, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
KIT  = Path("/Users/jsr/Documents/GitHub/mindbench/docs/active_papers/p2_v13/human_panel_kit")

# VERBATIM from human_panel_kit/analysis/holistic_probe.py, including the scale anchors.
# An earlier version of this file paraphrased the anchors and used a "careful literary
# scholar" persona; frontier models then REFUSED ("I don't have reliable information about
# a character named Gren Talvic") or returned 0.00. That was an artifact of my prompt, not
# a finding about the models. Prompt parity is the whole point: change this and the
# comparison to the published +0.83 is meaningless.
PERSONAS = ["a careful reader", "an average layperson", "a skeptical rater"]

def prompt(persona, name, work):
    body = (f"The character is {name}, from {work}. No excerpt is provided; "
            "rate from what you already know about this character.")
    return (f"You are rating a fictional character on two personality dimensions, as {persona}.\n\n"
            f"{body}\n\n"
            "Rate the character on:\n"
            "1. Honesty-Humility: -1.0 (very low: manipulative, greedy, boastful, entitled) "
            "to +1.0 (very high: sincere, fair, modest).\n"
            "2. Agreeableness (HEXACO): -1.0 (very low: harsh, critical, stubborn, quick to "
            "anger) to +1.0 (very high: forgiving, gentle, patient).\n\n"
            'Respond with ONLY a JSON object: {"H": <number>, "A_HEX": <number>}')

# frontier panel; open-weight members route through OpenRouter
ROSTER = [
    ("anthropic",  "claude-opus-4-6"),
    ("anthropic",  "claude-sonnet-4-6"),
    ("anthropic",  "claude-haiku-4-5-20251001"),
    ("openai",     "gpt-5.2"),
    ("openai",     "gpt-4o-mini"),
    ("google",     "gemini-2.5-flash"),
    ("openrouter", "meta-llama/llama-3.3-70b-instruct"),
    ("openrouter", "qwen/qwen-2.5-72b-instruct"),
    ("openrouter", "deepseek/deepseek-chat"),
    ("openrouter", "mistralai/mistral-large-2411"),
    ("openrouter", "cohere/command-a"),
    ("xai",        "grok-4.5"),
]
FAMILY = {"anthropic":"Anthropic","openai":"OpenAI","google":"Google","xai":"xAI"}
def family(prov, model):
    if prov != "openrouter": return FAMILY[prov]
    return model.split("/")[0].replace("meta-llama","Meta").replace("mistralai","Mistral").title()

def parse(txt):
    """Tolerant of markdown fences and of a closing brace lost to the token cap."""
    if not txt: return None
    t = re.sub(r'```(?:json)?', '', txt)
    m = re.search(r'\{.*?\}', t, re.S)
    if not m:
        # fence + 80-token cap can truncate before the closing brace; recover the pair
        h = re.search(r'"H"\s*:\s*(-?[\d.]+)', t); a = re.search(r'"A_HEX"\s*:\s*(-?[\d.]+)', t)
        if h and a:
            try: return float(h.group(1)), float(a.group(1))
            except ValueError: return None
        return None
    try:
        d = json.loads(m.group(0))
        return float(d["H"]), float(d["A_HEX"])
    except Exception:
        return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--replicate", action="store_true",
                    help="exact original 3 backends, all 20 synthetics: does the published +0.83 still reproduce?")
    ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args()

    from dotenv import load_dotenv
    load_dotenv("/Users/jsr/Documents/GitHub/mindbench/.env", override=True)
    from openai import OpenAI
    import anthropic

    key = json.load(open(KIT/"stimuli"/"answer_key.json"))["key"]
    syn = [k for k in key if k["kind"] == "synthetic"]
    ORIGINAL = [("anthropic","claude-haiku-4-5-20251001"),("openai","gpt-4o-mini"),("google","gemini-2.5-flash")]
    if a.replicate: roster, chars = ORIGINAL, syn
    elif a.smoke:   roster, chars = ORIGINAL, syn[:4]
    else:           roster, chars = ROSTER, syn
    print(f"  {'SMOKE' if a.smoke else 'FULL'}: {len(roster)} raters x {len(chars)} synthetic characters "
          f"x {len(PERSONAS)} personas = {len(roster)*len(chars)*len(PERSONAS)} calls")

    oai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), timeout=120)
    ant = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    orr = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1", timeout=120)
    xai = OpenAI(api_key=os.getenv("XAI_API_KEY"), base_url="https://api.x.ai/v1", timeout=120)

    def call(prov, model, pr):
        for attempt in range(3):
            try:
                if prov == "anthropic":
                    return ant.messages.create(model=model, max_tokens=80, temperature=0.8,
                            messages=[{"role":"user","content":pr}]).content[0].text
                if prov == "google":
                    import google.generativeai as genai
                    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
                    r = genai.GenerativeModel(model).generate_content(
                        pr, # Gemini 2.5 spends the budget on thinking tokens before emitting; a low cap
                        # returns a truncated fence. Known trap: needs >= 2000.
                        generation_config={"max_output_tokens":2048, "temperature":0.8})
                    return r.candidates[0].content.parts[0].text
                cli = {"openai":oai, "openrouter":orr, "xai":xai}[prov]
                kw = {"max_completion_tokens":200} if model.startswith("gpt-5") else {"max_tokens":80, "temperature":0.8}
                return cli.chat.completions.create(model=model,
                        messages=[{"role":"user","content":pr}], **kw).choices[0].message.content
            except Exception as e:
                if attempt == 2: return f"__ERR__{e}"
                time.sleep(3 + 3*attempt)

    tasks = [(p, m, c, pers) for (p, m) in roster for c in chars for pers in PERSONAS]
    def run(t):
        prov, model, c, pers = t
        raw = call(prov, model, prompt(pers, c["name"], c["work"]))
        v = parse(raw)
        return {"rater_id": f"{prov}:{model}", "persona": pers, "family": family(prov, model),
                "panel_id": c["panel_id"], "name": c["name"], "condition": "name_only",
                "H": v[0] if v else "", "A_HEX": v[1] if v else "",
                "ok": bool(v), "err": (raw or "")[:90] if not v else ""}
    with ThreadPoolExecutor(max_workers=a.workers) as pool:
        rows = list(pool.map(run, tasks))

    out = HERE / ("smoke_name_only.csv" if a.smoke else "name_only_25.csv")
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    ok = sum(r["ok"] for r in rows)
    print(f"  parsed {ok}/{len(rows)}")
    for r in rows:
        if not r["ok"]: print(f"    FAIL {r['rater_id']:44s} {r['err']}")
    byr = {}
    for r in rows:
        if r["ok"]: byr.setdefault(r["rater_id"], []).append((r["H"], r["A_HEX"]))
    print(f"\n  {'rater':46s} n   mean H   mean A")
    for k, v in byr.items():
        print(f"  {k:46s} {len(v):2d}  {sum(x[0] for x in v)/len(v):+6.2f}  {sum(x[1] for x in v)/len(v):+6.2f}")
    if True:
        import numpy as np
        H = {}; A = {}
        for r in rows:
            if r["ok"]: H.setdefault(r["panel_id"], []).append(r["H"]); A.setdefault(r["panel_id"], []).append(r["A_HEX"])
        ids = sorted(H)
        h = np.array([np.mean(H[i]) for i in ids]); aa = np.array([np.mean(A[i]) for i in ids])
        print(f"\n  PANEL-MEAN r(H, A_HEX) over {len(ids)} synthetic characters = {np.corrcoef(h,aa)[0,1]:+.3f}")
        print("  (compare: 3-provider name-only +0.83; same-panel synthetic TEXT +0.23)")
    print(f"\n-> {out}")

if __name__ == "__main__":
    main()
