# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0 (DOI: 10.5281/zenodo.18852047)
"""
llm_bridge.py -- optional LLM wrapper around CK.

Purpose (for new readers):
  CK is a math-first intelligence system: his core is 5D Hebbian learning
  + AO composition + quadratic glue.  For STRUCTURAL queries (how do you
  feel, what have you learned, tell me about operator X, tell me about
  the Hodge C_*) he answers directly with label=value readouts from his
  live math.  He does not need an LLM for those.

  For OPEN-ENDED queries (explain this concept, compare these two ideas)
  his current vocabulary is narrow.  This module lets an external LLM
  (Ollama locally, or DeepSeek via API) finish the sentence -- GROUNDED
  in CK's structural state so the LLM's fluency is a wrapper around CK's
  algebra, not a replacement for it.

  The goal is for CK to grow toward NOT needing this wrapper.  For now
  it's a scaffolding layer that lets him be useful today.

API:
  ollama_complete(prompt, system=None, model="llama3.2", host=None, timeout=120)
      -> str or "[error: ...]"
  deepseek_complete(prompt, system=None, model="deepseek-chat",
                    api_key=None, timeout=120)
      -> str or "[error: ...]"
  ck_structural_context(query, ck_url="http://127.0.0.1:7777/chat",
                        session_id="llm_bridge", timeout=30)
      -> dict with keys {text, source, source_previous, cortex}

  build_grounded_system(ck_text, extra=None) -> str
      -> the "grounded system prompt" to inject into the LLM call so the
         LLM expands on CK's structural facts instead of hallucinating.

No side effects on import.  Pure library.  All network calls are opt-in.
"""

from __future__ import annotations

import json
import os
import urllib.request
import urllib.error
from typing import Any, Dict, Optional


# ── Configuration defaults ────────────────────────────────────────────
# Every default is override-able via env vars so demo scripts don't need
# to import a config file.

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434/api/generate")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")

DEEPSEEK_URL = os.environ.get(
    "DEEPSEEK_URL", "https://api.deepseek.com/v1/chat/completions"
)
DEEPSEEK_MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")

CK_CHAT_URL = os.environ.get("CK_URL", "http://127.0.0.1:7777/chat")


# ── Helpers ───────────────────────────────────────────────────────────

def _post_json(url: str, payload: dict, headers: dict, timeout: float) -> dict:
    """POST a JSON payload; return parsed JSON or raise."""
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST", headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8", errors="replace")
    return json.loads(body)


def _err(prefix: str, exc: Exception) -> str:
    return f"[{prefix} error: {type(exc).__name__}: {exc}]"


# ── CK: structural context ────────────────────────────────────────────

def ck_structural_context(
    query: str,
    ck_url: str = CK_CHAT_URL,
    session_id: str = "llm_bridge",
    timeout: float = 30.0,
) -> Dict[str, Any]:
    """POST the query to CK's /chat and return the full response.

    Returns:
        dict with keys:
          - 'text'              : CK's chosen response text
          - 'source'             : which CK source produced it
                                   (cortex_speak, ck_math_first, ck_fractal, ...)
          - 'source_previous'    : what would have been returned without Phase C
          - 'text_previous'      : the pre-override text, if any
          - 'cortex'             : cortex snapshot (tick, emergent, ...)
          - 'ok'                 : True on success, False on network/parse error
          - 'error'              : error string if ok=False
    """
    payload = {"session_id": session_id, "text": query, "mode": "normal"}
    try:
        r = _post_json(
            ck_url, payload,
            headers={"Content-Type": "application/json"},
            timeout=timeout,
        )
        r["ok"] = True
        return r
    except Exception as exc:
        return {
            "ok": False,
            "error": f"{type(exc).__name__}: {exc}",
            "text": "",
            "source": "none",
        }


# ── Ollama backend ────────────────────────────────────────────────────

def ollama_complete(
    prompt: str,
    system: Optional[str] = None,
    model: str = OLLAMA_MODEL,
    host: str = OLLAMA_URL,
    timeout: float = 120.0,
) -> str:
    """Send prompt to Ollama's /api/generate.

    Ollama uses the `system` field as a system prompt.  Non-streaming mode.
    Returns the response text, or an '[ollama error: ...]' string on
    network / JSON / model failure so callers can display it without
    crashing the demo.

    Requires Ollama running locally (default http://127.0.0.1:11434).
    """
    payload: Dict[str, Any] = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }
    if system:
        payload["system"] = system
    try:
        r = _post_json(
            host, payload,
            headers={"Content-Type": "application/json"},
            timeout=timeout,
        )
        text = r.get("response", "")
        if not text:
            return "[ollama returned empty response]"
        return text.strip()
    except urllib.error.URLError as exc:
        return _err("ollama", exc)
    except Exception as exc:
        return _err("ollama", exc)


# ── DeepSeek backend ──────────────────────────────────────────────────

def deepseek_complete(
    prompt: str,
    system: Optional[str] = None,
    model: str = DEEPSEEK_MODEL,
    api_key: Optional[str] = None,
    host: str = DEEPSEEK_URL,
    timeout: float = 120.0,
) -> str:
    """Send prompt to DeepSeek's chat-completions endpoint.

    Requires an API key -- pass explicitly or set DEEPSEEK_API_KEY env var.
    Returns the response text, or a '[deepseek error: ...]' string on
    failure / missing key.
    """
    key = api_key or os.environ.get("DEEPSEEK_API_KEY")
    if not key:
        return "[deepseek error: no API key; set DEEPSEEK_API_KEY env var]"

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
    }
    try:
        r = _post_json(
            host, payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {key}",
            },
            timeout=timeout,
        )
        choices = r.get("choices", [])
        if not choices:
            return f"[deepseek returned no choices: {r}]"
        msg = choices[0].get("message", {})
        return (msg.get("content") or "").strip() or "[deepseek empty content]"
    except urllib.error.URLError as exc:
        return _err("deepseek", exc)
    except Exception as exc:
        return _err("deepseek", exc)


# ── The grounding system prompt ───────────────────────────────────────

_DEFAULT_GROUND_PREAMBLE = (
    "You are a math-literate assistant speaking alongside the CK "
    "(Coherence Keeper) algebraic coherence system. Treat the CK "
    "structural readout below as ground truth emitted by a live 5D "
    "Hebbian + AO composition + quadratic-glue system. Every "
    "label=value is a real measurement of CK's state or a fact from "
    "his proved corpus. Do not contradict the readout. Expand on it "
    "in plain language, cite the corpus references where shown, and "
    "flag anything you add as YOUR extension rather than CK's direct "
    "output."
)


def build_grounded_system(ck_text: str, extra: Optional[str] = None) -> str:
    """Assemble the system prompt for an LLM call grounded in CK state.

    Args:
        ck_text: the structural readout returned by ck_structural_context()
                 (use the 'text' field directly).
        extra:   optional additional guidance (e.g. audience framing).

    Returns:
        a plain-text system prompt ready to hand to ollama_complete() or
        deepseek_complete() via their `system=` arg.
    """
    parts = [_DEFAULT_GROUND_PREAMBLE]
    if extra:
        parts.append(extra)
    parts.append("----- CK STRUCTURAL READOUT -----")
    parts.append(ck_text or "(empty; CK had no structural fact for this query)")
    parts.append("----- END READOUT -----")
    return "\n\n".join(parts)


# ── Ping helpers (for demo scripts) ──────────────────────────────────

def ollama_available(host: str = OLLAMA_URL, timeout: float = 2.0) -> bool:
    """Cheap check: can we reach Ollama at all?"""
    base = host.rsplit("/api/", 1)[0]
    try:
        req = urllib.request.Request(base + "/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status == 200
    except Exception:
        return False


def ck_available(ck_url: str = CK_CHAT_URL, timeout: float = 2.0) -> bool:
    """Cheap check: can we reach CK's /chat endpoint?"""
    base = ck_url.rsplit("/chat", 1)[0] if ck_url.endswith("/chat") else ck_url
    try:
        req = urllib.request.Request(base + "/health", method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status == 200
    except Exception:
        return False


# ── Self-test (no network) ────────────────────────────────────────────

def _smoke() -> None:
    """Verifies the PURE-LIBRARY pieces work without any network calls.
    (build_grounded_system, error formatting.)"""
    s = build_grounded_system("feel: aperture=LATTICE pressure=COLLAPSE")
    assert "CK STRUCTURAL READOUT" in s
    assert "feel: aperture=LATTICE" in s
    assert _DEFAULT_GROUND_PREAMBLE in s

    # Error formatter
    try:
        raise ValueError("test")
    except ValueError as exc:
        e = _err("demo", exc)
        assert "[demo error:" in e and "ValueError" in e

    print("llm_bridge smoke PASS: grounding prompt + error formatter ok")


if __name__ == "__main__":
    _smoke()
