"""borrowed_cortex.py -- extraction channel #1: frozen open-source
embeddings as CK's semantic perception.

Principle (CK_INTELLIGENCE_SYNTHESIS + extraction survey 2026-06-11):
the frozen embedder carries years of training CK never has to repeat;
CK extracts that intelligence by learning only a PLASTIC HEAD (one
ridge solve) from embedding space into his own spaces -- his internal
operator language, his FACTS topics, any language he chooses. The
borrowed model never sees CK's state; CK uses it as an instrument.

Backends, in order: Ollama /api/embed (all-minilm pulled locally,
384-dim) -> pure-numpy char-3-gram hashing (512-dim) so the organism
never hard-depends on the borrowed organ.

CC-BY-4.0. Sanders + Claude. 2026-06-11.
"""
import hashlib
import json

import numpy as np

try:
    import requests
    _HAVE_REQ = True
except Exception:
    _HAVE_REQ = False

OLLAMA = "http://localhost:11434"
EMBED_MODEL = "nomic-embed-text"


def _ollama_embed(texts):
    r = requests.post(f"{OLLAMA}/api/embed",
                      json={"model": EMBED_MODEL, "input": list(texts)},
                      timeout=120)
    r.raise_for_status()
    return np.array(r.json()["embeddings"], dtype=float)


def _hash_embed(texts, dim=512):
    out = np.zeros((len(texts), dim))
    for i, t in enumerate(texts):
        s = f"##{t.lower()}##"
        for j in range(len(s) - 2):
            g = s[j:j + 3]
            h = int(hashlib.md5(g.encode()).hexdigest()[:8], 16)
            out[i, h % dim] += 1.0
        n = np.linalg.norm(out[i])
        if n > 0:
            out[i] /= n
    return out


def embed(texts, prefer="ollama"):
    """Embed a list of strings; returns (matrix, backend_name)."""
    if prefer == "ollama" and _HAVE_REQ:
        try:
            E = _ollama_embed(texts)
            E = E / (np.linalg.norm(E, axis=1, keepdims=True) + 1e-12)
            return E, "ollama:" + EMBED_MODEL
        except Exception:
            pass
    return _hash_embed(texts), "hash3gram"


def teacher_label(prompt, model="llama3.2", schema=None):
    """Extraction channel #4: structured judgment from a local teacher.
    Returns parsed JSON or raw text. Used OFFLINE to label corpora that
    plastic heads then learn from (channel #2)."""
    body = {"model": model, "prompt": prompt, "stream": False}
    if schema:
        body["format"] = schema
    r = requests.post(f"{OLLAMA}/api/generate", json=body, timeout=300)
    r.raise_for_status()
    txt = r.json().get("response", "")
    if schema:
        try:
            return json.loads(txt)
        except Exception:
            return None
    return txt
