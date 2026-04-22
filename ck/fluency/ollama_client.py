# -*- coding: utf-8 -*-
"""
ollama_client.py — minimal wrapper around the Ollama HTTP API.

Contract per OLLAMA_LEARN_LOOP.md §2.5:

    "thin wrapper around /api/generate"

Design:
- Uses only the Python standard library (urllib) — no extra deps.  Ollama
  ships with its own client libraries but those pull in transitive
  dependencies we don't need for Option A.
- Default endpoint is ``http://localhost:11434`` (Ollama's loopback default).
  **Never** configured to point at a remote host — this is a local-only
  learn-loop.
- Connection errors are returned as structured ``dict`` results, never
  raised.  The fluency server treats "ollama offline" as a data point,
  not a crash.
- Streaming is disabled (``"stream": false``) so we get one response blob
  per request.  The learn-loop is turn-based; streaming adds complexity
  the correction layer can't use.

Reference: https://github.com/ollama/ollama/blob/main/docs/api.md
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


# ----------------------------------------------------------------------------
# config
# ----------------------------------------------------------------------------

DEFAULT_HOST = "http://localhost:11434"
DEFAULT_MODEL = "llama3.1:8b"
DEFAULT_TIMEOUT_SEC = 120  # generation can be slow on CPU
DEFAULT_TEMPERATURE = 0.7


# ----------------------------------------------------------------------------
# result container
# ----------------------------------------------------------------------------

@dataclass
class OllamaResult:
    """What /api/generate returned, or a structured error."""
    ok: bool
    text: str = ""
    model: str = ""
    error: str = ""
    elapsed_ms: int = 0
    raw: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ok": self.ok,
            "text": self.text,
            "model": self.model,
            "error": self.error,
            "elapsed_ms": self.elapsed_ms,
            # the raw API response is kept around for auditing but not
            # re-serialized into every log entry
        }


# ----------------------------------------------------------------------------
# client
# ----------------------------------------------------------------------------

class OllamaClient:
    """Local Ollama HTTP client.  Loopback only."""

    def __init__(
        self,
        host: str = DEFAULT_HOST,
        model: str = DEFAULT_MODEL,
        timeout_sec: int = DEFAULT_TIMEOUT_SEC,
    ) -> None:
        # refuse non-loopback hosts -- the learn-loop is local-only
        if not host.startswith(("http://localhost", "http://127.0.0.1")):
            raise ValueError(
                f"ollama_client: host must be loopback; got {host!r}. "
                f"The learn-loop is local-only per CK_UNIFIED_ARCHITECTURE.md §3.4."
            )
        self.host = host.rstrip("/")
        self.model = model
        self.timeout_sec = timeout_sec

    # ---- generate ----

    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = DEFAULT_TEMPERATURE,
        system: Optional[str] = None,
    ) -> OllamaResult:
        """POST /api/generate; return OllamaResult (never raises)."""
        model_tag = model or self.model
        payload: Dict[str, Any] = {
            "model": model_tag,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": float(temperature)},
        }
        if system:
            payload["system"] = system

        url = f"{self.host}/api/generate"
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        t0 = time.perf_counter()
        try:
            with urllib.request.urlopen(req, timeout=self.timeout_sec) as resp:
                raw = json.loads(resp.read().decode("utf-8"))
        except urllib.error.URLError as e:
            return OllamaResult(
                ok=False,
                model=model_tag,
                error=f"ollama-unreachable: {e.reason}",
                elapsed_ms=int((time.perf_counter() - t0) * 1000),
            )
        except json.JSONDecodeError as e:
            return OllamaResult(
                ok=False,
                model=model_tag,
                error=f"ollama-bad-json: {e}",
                elapsed_ms=int((time.perf_counter() - t0) * 1000),
            )
        except Exception as e:  # pragma: no cover -- never crash the server
            return OllamaResult(
                ok=False,
                model=model_tag,
                error=f"ollama-unexpected: {type(e).__name__}: {e}",
                elapsed_ms=int((time.perf_counter() - t0) * 1000),
            )

        elapsed_ms = int((time.perf_counter() - t0) * 1000)
        text = str(raw.get("response", "")).strip()
        return OllamaResult(
            ok=True,
            text=text,
            model=str(raw.get("model", model_tag)),
            elapsed_ms=elapsed_ms,
            raw=raw,
        )

    # ---- health ----

    def is_reachable(self) -> bool:
        """Quick GET /api/tags; true iff Ollama answers."""
        try:
            req = urllib.request.Request(f"{self.host}/api/tags", method="GET")
            with urllib.request.urlopen(req, timeout=2) as resp:
                return resp.status == 200
        except Exception:
            return False


# ----------------------------------------------------------------------------
# self-test (prints without requiring Ollama to be running)
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    c = OllamaClient()
    reachable = c.is_reachable()
    print(f"[ollama_client] host={c.host} model={c.model} reachable={reachable}")
    if reachable:
        r = c.generate("Say 'pong' and nothing else.", temperature=0.0)
        print(f"[ollama_client] ok={r.ok} elapsed={r.elapsed_ms}ms")
        print(f"[ollama_client] text={r.text!r}")
    else:
        print("[ollama_client] Ollama not running on loopback; skipping generate probe.")
        print("[ollama_client] This is expected if you haven't started 'ollama serve'.")
