"""Consensus runner (multi-provider trait inference).

Invokes multiple LLM providers to infer OCEAN traits from character evidence
(quotes in temporal order), then aggregates per-character outputs via median
or trimmed mean.

Ported from the private research repository's aperture_pillar1_consensus.py
(v3 prompt). Trimmed to three providers (OpenAI, Anthropic, Google) for
ease of reproduction; add more by extending ``PROVIDER_CALLERS`` below.

Expected input shape (``evidence`` argument to ``build_prompt``):
    {
        "character_name": str,
        "quotes": [
            {"quote_text": str, "quote_start": int | str},
            ...
        ],
    }

API keys are read from environment variables (or a ``.env`` file loaded via
``python-dotenv`` at import time):
    OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from statistics import median
from typing import Any, Callable

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:  # python-dotenv optional; env vars still work
    pass

TRAIT_KEYS = ["O", "C", "E", "A", "N"]


# ---------------------------------------------------------------------------
# Prompt construction (v3 refined framing)
# ---------------------------------------------------------------------------

def build_prompt(evidence: dict[str, Any]) -> str:
    """Build the OCEAN consensus prompt from an evidence pack.

    Uses the v3 refined framing (evidence-first, balanced facet guidance,
    full bidirectional range). Scale is [-1, +1] per trait.
    """
    character = evidence.get("character_name", "Unknown")
    quotes = evidence.get("quotes", []) or []

    quote_lines = []
    for idx, q in enumerate(quotes[:100], start=1):
        text = q.get("quote_text", "")
        if not text:
            continue
        start = q.get("quote_start", "")
        marker = f"[token {start}] " if start != "" else ""
        quote_lines.append(f"{idx}. {marker}{text}")
    quotes_block = "\n".join(quote_lines)

    return (
        "You are an expert personality psychologist scoring character traits "
        "from literary evidence.\n\n"
        "TASK: Rate the Big Five (OCEAN) personality traits on a scale from "
        "-1 to +1 based on the character's behavior and dialogue.\n"
        "Return JSON only with this exact schema:\n"
        '{ "O": float, "C": float, "E": float, "A": float, "N": float, '
        '"rationale": "brief 1-2 sentence summary" }\n\n'
        "PERSONALITY TRAITS (Bidirectional Scale):\n"
        "- O (Openness): Imaginative/curious/artistic (+1) vs Conventional/practical/simple (-1)\n"
        "- C (Conscientiousness): Organized/disciplined/reliable (+1) vs Careless/impulsive/disorganized (-1)\n"
        "- E (Extraversion): Outgoing/talkative/energetic (+1) vs Reserved/solitary/withdrawn (-1)\n"
        "- A (Agreeableness): Compassionate/kind/trusting (+1) vs Antagonistic/suspicious/cold (-1)\n"
        "- N (Neuroticism): Anxious/volatile/hot-tempered (+1) vs Calm/stable/even-tempered (-1)\n\n"
        "GUIDELINES:\n"
        "- Let the evidence guide your assessment; use negative scores for low traits.\n"
        "- Distinguish C Deliberation (plans ahead) from N Impulsiveness (emotionally volatile). "
        "A character can be calm (low N) yet spontaneous (low C), or anxious (high N) yet organized (high C).\n"
        "- Use the full range [-1, +1] to differentiate characters; avoid clustering around 0 unless truly neutral.\n"
        "- If traits evolve over time, weight later evidence more heavily and mention the change in the rationale.\n\n"
        f"CHARACTER: {character}\n\n"
        "EVIDENCE (Character quotes in temporal order):\n"
        f"{quotes_block}\n\n"
        "Return only valid JSON matching the schema above.\n"
    )


# ---------------------------------------------------------------------------
# Output parsing
# ---------------------------------------------------------------------------

def _extract_json(text: str) -> dict[str, Any] | None:
    """Pull the outermost JSON object from a model response string."""
    if not text:
        return None
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end <= start:
        return None
    try:
        return json.loads(text[start:end + 1])
    except json.JSONDecodeError:
        return None


def _normalize_vector(payload: dict[str, Any]) -> dict[str, float] | None:
    """Clamp a parsed payload to a 5-trait OCEAN vector in [-1, 1]."""
    if not payload:
        return None
    out: dict[str, float] = {}
    for key in TRAIT_KEYS:
        if key not in payload:
            return None
        try:
            value = float(payload[key])
        except (TypeError, ValueError):
            return None
        out[key] = max(-1.0, min(1.0, value))
    return out


# ---------------------------------------------------------------------------
# Provider callers
# ---------------------------------------------------------------------------

def _call_openai(model_id: str, api_key: str, prompt: str) -> str | None:
    try:
        from openai import OpenAI
    except ImportError:
        return None
    client = OpenAI(api_key=api_key)
    try:
        resp = client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=400,
        )
        if not resp.choices:
            return None
        return resp.choices[0].message.content
    except Exception:
        try:
            resp = client.responses.create(
                model=model_id,
                input=prompt,
                max_output_tokens=1200,
                reasoning={"effort": "minimal"},
            )
            return getattr(resp, "output_text", None)
        except Exception:
            return None


def _call_anthropic(model_id: str, api_key: str, prompt: str) -> str | None:
    try:
        import anthropic
    except ImportError:
        return None
    try:
        client = anthropic.Anthropic(api_key=api_key)
        resp = client.messages.create(
            model=model_id,
            max_tokens=400,
            temperature=0,
            messages=[{"role": "user", "content": prompt}],
        )
        if not resp.content:
            return None
        return resp.content[0].text
    except Exception:
        return None


def _call_google(model_id: str, api_key: str, prompt: str) -> str | None:
    try:
        import google.generativeai as genai
    except ImportError:
        return None
    try:
        genai.configure(api_key=api_key)
        full = model_id if model_id.startswith("models/") else f"models/{model_id}"
        model = genai.GenerativeModel(full)
        resp = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(temperature=0),
            request_options={"timeout": 120},
        )
        return getattr(resp, "text", None)
    except Exception:
        return None


PROVIDER_CALLERS: dict[str, tuple[str, Callable[[str, str, str], str | None]]] = {
    "openai": ("OPENAI_API_KEY", _call_openai),
    "anthropic": ("ANTHROPIC_API_KEY", _call_anthropic),
    "google": ("GOOGLE_API_KEY", _call_google),
}


def fetch_trait_vector(
    provider: str, model_id: str, prompt: str,
) -> dict[str, Any] | None:
    """Call a single provider and return a parsed trait vector (or None)."""
    if provider not in PROVIDER_CALLERS:
        raise ValueError(f"Unknown provider: {provider!r}. "
                         f"Known: {sorted(PROVIDER_CALLERS)}")
    env_key, caller = PROVIDER_CALLERS[provider]
    api_key = os.getenv(env_key)
    if not api_key:
        return None
    raw = caller(model_id, api_key, prompt)
    payload = _extract_json(raw or "")
    vector = _normalize_vector(payload) if payload else None
    if not vector:
        return None
    return {"provider": provider, "model": model_id, "vector": vector, "raw": raw}


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------

def aggregate_vectors(
    vectors: list[dict[str, Any]],
    method: str = "median",
) -> dict[str, float] | None:
    """Aggregate provider vectors into a single OCEAN vector.

    Args:
        vectors: Output of per-provider ``fetch_trait_vector`` calls (with
            ``None`` entries filtered out).
        method: ``"median"`` (default), ``"mean"``, or ``"trimmed_mean"``
            (drops one high and one low value when >= 3 providers are present).

    Returns a 5-key OCEAN dict, or ``None`` if any trait has no values.
    """
    if not vectors:
        return None
    valid = [v for v in vectors if v and v.get("vector")]
    if not valid:
        return None
    out: dict[str, float] = {}
    for key in TRAIT_KEYS:
        vals = [v["vector"][key] for v in valid if key in v["vector"]]
        if not vals:
            return None
        if method == "trimmed_mean" and len(vals) >= 3:
            vals = sorted(vals)[1:-1]
            out[key] = sum(vals) / len(vals)
        elif method == "mean":
            out[key] = sum(vals) / len(vals)
        else:
            out[key] = float(median(vals))
    return out


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

# Pinned to dated snapshots for run reproducibility (Invariant I7).
# The `*-latest` aliases would drift as providers rotate them; dated
# snapshots are the only way to guarantee the same model is invoked at
# reproduction time. The reference paper run used these specific
# snapshots; users overriding via `models=` should pass dated IDs too.
DEFAULT_MODELS: dict[str, str] = {
    "openai": "gpt-4o-mini-2024-07-18",
    "anthropic": "claude-3-5-haiku-20241022",
    "google": "gemini-1.5-flash-002",
}


def run_consensus(
    evidence_packs: list[dict[str, Any]],
    providers: list[str] | None = None,
    models: dict[str, str] | None = None,
    aggregation: str = "median",
    out_path: Path | str | None = None,
) -> dict[str, Any]:
    """Run consensus across providers for a list of characters.

    Args:
        evidence_packs: One dict per character, each with ``character_name``,
            ``coref_id`` (optional), and ``quotes``.
        providers: Provider names to query (default: all three).
        models: Per-provider model id override (default: ``DEFAULT_MODELS``).
        aggregation: ``"median"``, ``"mean"``, or ``"trimmed_mean"``.
        out_path: If given, write the run JSON to this path.

    Returns a run record::

        {
            "run_id": "...",
            "created_at": "ISO8601",
            "providers": [...],
            "models": {...},
            "aggregation": "...",
            "characters": [
                {
                    "character_name": "...",
                    "coref_id": "...",
                    "vectors": [{provider, model, vector, raw}, ...],
                    "consensus": {O, C, E, A, N},
                },
                ...
            ],
        }
    """
    providers = providers or list(PROVIDER_CALLERS)
    models = {**DEFAULT_MODELS, **(models or {})}

    unknown = [p for p in providers if p not in PROVIDER_CALLERS]
    if unknown:
        raise ValueError(f"Unknown provider(s): {unknown}. "
                         f"Known: {sorted(PROVIDER_CALLERS)}")

    characters_out: list[dict[str, Any]] = []
    for pack in evidence_packs:
        prompt = build_prompt(pack)
        vectors: list[dict[str, Any]] = []
        for provider in providers:
            result = fetch_trait_vector(provider, models[provider], prompt)
            if result is not None:
                vectors.append(result)
        consensus = aggregate_vectors(vectors, method=aggregation)
        characters_out.append({
            "character_name": pack.get("character_name"),
            "coref_id": pack.get("coref_id"),
            "vectors": vectors,
            "consensus": consensus,
        })

    now = datetime.now(timezone.utc)
    record: dict[str, Any] = {
        "run_id": now.strftime("run_%Y%m%dT%H%M%SZ"),
        "created_at": now.isoformat(),
        "providers": providers,
        "models": {p: models[p] for p in providers},
        "aggregation": aggregation,
        "characters": characters_out,
    }

    if out_path:
        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w") as f:
            json.dump(record, f, indent=2)

    return record
