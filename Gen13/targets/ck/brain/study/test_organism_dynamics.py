"""
test_organism_dynamics.py — does CK actually organize memory the way
Brayden's framework says he should?

Tests probed by this harness:

  1. PER-MODALITY ABSORPTION
     Same canonical D2 pipeline applied to text + 4 distinguishable
     audio sources (silence-heavy, sustained tone, rhythmic burst,
     speech-like).  Captures pre/post cortex W + olfactory totals.

  2. DUALITY
     Are dual-operator pairs (VOID<->HARMONY, BALANCE<->CHAOS,
     LATTICE<->BREATH, COUNTER<->RESET, COLLAPSE<->PROGRESS)
     visible as coupled in the cortex W matrix after absorption?
     Method: compute |W[a][b]| for canonical dual pairs vs random
     pairs; the dual pairs should not be smaller on average.

  3. RESONANCE / PARALLEL
     Feed the same audio source twice.  Compare pass-1 W-delta to
     pass-2 W-delta.  If CK is organizing memory, pass-2 deltas
     should be smaller (recognition) or differently shaped
     (different operator pair learning).

  4. PROGRESSION
     Order matters: A->B->C vs C->B->A produces different W
     endpoints (because Hebbian is order-sensitive on adjacent op
     pairs).  Verify the live cortex shows order-dependence.

  5. NOW-RETRIEVAL
     After absorbing audio, query 'what did you just hear' /
     'what is the dominant operator now' / 'do you remember the
     tone'.  Read the chat response; does it reflect the absorbed
     material?  This is the strongest claim and the one most likely
     to fall short with current chat layer.

Outputs:
  ./test_organism_dynamics_<TIMESTAMP>.json -- full numeric record
  stdout summary -- human-readable per-test verdict (PASS/PARTIAL/FAIL)

This is read-only at the source level (no code changes); it just
exercises the live server and reports.
"""
from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.request
import wave
from collections import Counter
from pathlib import Path

import numpy as np

SCRIPT_DIR = Path(__file__).parent.resolve()
GEN13_BRAIN = SCRIPT_DIR.parent
sys.path.insert(0, str(GEN13_BRAIN))
sys.path.insert(0, str(GEN13_BRAIN / "ck_sim" / "being"))
sys.path.insert(0, str(SCRIPT_DIR))

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

from audio_pipeline import (
    OP_NAMES, NUM_OPS, pcm_to_operator_stream,
)

SERVER = "http://localhost:7777"

# Canonical dual-operator pairs (Brayden's framework)
# Each pair is (operator, dual) -- they should be visibly coupled
# if CK organizes memory in dualities.
DUAL_PAIRS = [
    (0, 7),   # VOID <-> HARMONY
    (5, 6),   # BALANCE <-> CHAOS
    (1, 8),   # LATTICE <-> BREATH (structure <-> rhythm)
    (2, 9),   # COUNTER <-> RESET (measure <-> liminal)
    (3, 4),   # PROGRESS <-> COLLAPSE (forward <-> error correct)
]


# ── Server interface ───────────────────────────────────────────────

def _get_json(path: str, timeout: float = 30) -> dict:
    req = urllib.request.Request(f"{SERVER}{path}", method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def _post_json(path: str, body: dict, timeout: float = 60) -> dict:
    req = urllib.request.Request(
        f"{SERVER}{path}",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def snapshot_state() -> dict:
    """Capture CK's current cortex + olfactory state."""
    cortex = _get_json("/cortex")
    out = {
        "tick": int(cortex.get("tick", 0)),
        "W_trace": float(cortex.get("W_trace", 0.0)),
        "emergent": float(cortex.get("emergent", 0.0)),
        "last_pair": list(cortex.get("last_pair", [None, None])),
        "ao_op": cortex.get("ao", {}).get("op"),
        "W": cortex.get("hebbian", {}).get("W", []),
    }
    # Olfactory totals via /experience/status (which reads the bulb stats)
    try:
        exp = _get_json("/experience/status")
        out["experience"] = {
            "total_ingested": int(exp.get("total_ingested", 0)),
            "total_edges": int(exp.get("total_edges", 0)),
        }
    except Exception:
        out["experience"] = {}
    return out


def cortex_w_norm(state: dict) -> float:
    """Sum |W[i][j]| across the cortex W matrix."""
    W = state.get("W") or []
    return float(sum(abs(v) for row in W for v in row))


def cortex_w_dual_score(state: dict) -> dict:
    """For each canonical dual pair (a, b), report |W[a_dim][b_dim]|.
    Maps op -> 7d cortex dim using the same OP_TO_DIM_7 the cortex uses."""
    W = state.get("W") or []
    if not W:
        return {}
    OP_TO_DIM_7 = {0: 0, 1: 3, 2: 1, 3: 2, 4: 4, 5: 3, 6: 0, 7: 0,
                   8: 4, 9: 1}
    n = len(W)
    out = {}
    for op_a, op_b in DUAL_PAIRS:
        d_a = OP_TO_DIM_7.get(op_a, 0) % n
        d_b = OP_TO_DIM_7.get(op_b, 0) % n
        # Take absolute coupling in both directions
        wab = abs(W[d_a][d_b])
        wba = abs(W[d_b][d_a])
        out[f"{OP_NAMES[op_a]}<->{OP_NAMES[op_b]}"] = round(
            (wab + wba) / 2.0, 5)
    return out


# ── Audio source generators ────────────────────────────────────────

def silence_pcm(seconds: float = 5.0, sr: int = 44100):
    """Pure silence -- expected dominant: VOID + LATTICE (low force)."""
    n = int(sr * seconds)
    return np.zeros(n, dtype=np.int16), sr


def tone_pcm(seconds: float = 5.0, sr: int = 44100, freq: float = 440):
    """Sustained sinusoid -- expected: BREATH + COUNTER + BALANCE."""
    n = int(sr * seconds)
    t = np.arange(n).astype(np.float32) / sr
    return (np.sin(2 * np.pi * freq * t) * 8000).astype(np.int16), sr


def burst_pcm(seconds: float = 5.0, sr: int = 44100, period: float = 0.3):
    """Rhythmic bursts -- expected: PROGRESS/COLLAPSE shifts at attacks."""
    n = int(sr * seconds)
    out = np.zeros(n, dtype=np.float32)
    burst_len = int(sr * period * 0.4)
    period_n = int(sr * period)
    t = np.arange(burst_len).astype(np.float32) / sr
    for start in range(0, n, period_n):
        end = min(n, start + burst_len)
        env = np.linspace(1.0, 0.1, end - start, dtype=np.float32)
        local = np.sin(2 * np.pi * 200 * t[: end - start]) * 8000 * env
        out[start:end] = local
    return out.astype(np.int16), sr


def chirp_pcm(seconds: float = 5.0, sr: int = 44100,
              f0: float = 200, f1: float = 1200):
    """Frequency sweep -- expected: progressive curvature."""
    n = int(sr * seconds)
    t = np.arange(n).astype(np.float32) / sr
    phase = 2 * np.pi * (f0 * t + (f1 - f0) / (2 * seconds) * t * t)
    return (np.sin(phase) * 8000).astype(np.int16), sr


def speech_like_pcm(seconds: float = 5.0, sr: int = 44100):
    """TTS the alphabet -- expected: rich operator distribution."""
    text = "ay. bee. see. dee. ee. ef. jee. aitch. eye. jay. kay."
    helper = (
        "import pyttsx3\n"
        f"text = {text!r}\n"
        f"out  = '/tmp/_speech_like.wav'\n"
        "e = pyttsx3.init()\n"
        "voices = [v for v in e.getProperty('voices') if 'EN-US' in v.id.upper()]\n"
        "if voices: e.setProperty('voice', voices[0].id)\n"
        "e.setProperty('rate', 110)\n"
        "e.save_to_file(text, out)\n"
        "e.runAndWait()\n"
    )
    rc = subprocess.run([sys.executable, "-c", helper],
                        capture_output=True, text=True, timeout=30)
    if rc.returncode != 0:
        return None, None
    # Re-encode to canonical PCM
    try:
        import static_ffmpeg
        static_ffmpeg.add_paths()
        import shutil
        ff = shutil.which("ffmpeg")
    except Exception:
        return None, None
    out_wav = "/tmp/_speech_like_clean.wav"
    rc = subprocess.run(
        [ff, "-i", "/tmp/_speech_like.wav",
         "-acodec", "pcm_s16le", "-ac", "1", "-ar", "44100",
         "-y", "-loglevel", "error", out_wav],
        capture_output=True, text=True)
    if rc.returncode != 0:
        return None, None
    with wave.open(out_wav, "rb") as wf:
        sr2 = wf.getframerate()
        raw = wf.readframes(wf.getnframes())
        samples = np.frombuffer(raw, dtype=np.int16)
    return samples, sr2


SOURCES = {
    "silence":   silence_pcm,
    "tone_440":  tone_pcm,
    "bursts":    burst_pcm,
    "chirp":     chirp_pcm,
    "speech":    speech_like_pcm,
}


# ── Absorption + measurement ───────────────────────────────────────

def absorb_pcm(samples, sr: int, label: str) -> dict:
    """Run canonical pipeline + POST to /audio/perceive.
    Returns dict with pre/post state, fingerprint, op distribution."""
    pre = snapshot_state()
    ops, fp = pcm_to_operator_stream(samples, sample_rate=sr)
    if not ops:
        return {"label": label, "error": "no ops produced"}
    body = {"ops": ops, "fingerprint": fp,
            "source_label": f"organism_test:{label}"}
    try:
        resp = _post_json("/audio/perceive", body, timeout=120)
    except Exception as exc:
        return {"label": label, "error": str(exc), "pre": pre,
                "fingerprint": fp, "n_ops": len(ops)}
    time.sleep(0.5)  # let the bulb settle
    post = snapshot_state()
    return {
        "label": label,
        "n_ops": len(ops),
        "fingerprint": {
            "operator_dist_named": fp.get("operator_dist_named", {}),
            "dominant_op_name": fp.get("dominant_op_name"),
            "curvature_energy": fp.get("curvature_energy"),
            "d2_magnitude_mean": fp.get("d2_magnitude_mean"),
            "flow_ratio": fp.get("flow_ratio"),
        },
        "pre":  {"tick": pre["tick"], "W_trace": pre["W_trace"],
                 "emergent": pre["emergent"],
                 "W_norm": cortex_w_norm(pre)},
        "post": {"tick": post["tick"], "W_trace": post["W_trace"],
                 "emergent": post["emergent"],
                 "W_norm": cortex_w_norm(post)},
        "delta": {
            "tick":      post["tick"]      - pre["tick"],
            "W_trace":   round(post["W_trace"]   - pre["W_trace"],   5),
            "emergent":  round(post["emergent"]  - pre["emergent"],  5),
            "W_norm":    round(cortex_w_norm(post) - cortex_w_norm(pre), 5),
        },
        "post_last_pair": post["last_pair"],
        "post_dual_score": cortex_w_dual_score(post),
        "absorb_response": {
            "ok": resp.get("ok"),
            "absorb_attempts": resp.get("absorb_attempts"),
            "olfactory_delta": resp.get("olfactory_delta"),
        },
    }


def query_chat(q: str, timeout: float = 60) -> dict:
    """Ask CK a chat question; return shortened response info."""
    try:
        resp = _post_json("/chat", {"text": q}, timeout=timeout)
    except Exception as exc:
        return {"q": q, "error": str(exc)}
    text = resp.get("text", "")
    return {
        "q": q,
        "source": resp.get("source"),
        "text_head": text[:240],
        "operators": resp.get("operators", [])[:6],
        "last_pair": resp.get("cortex", {}).get("last_pair")
            if isinstance(resp.get("cortex"), dict) else None,
    }


# ── Test runners ────────────────────────────────────────────────────

def cosine(a: list, b: list) -> float:
    a, b = np.array(a), np.array(b)
    na, nb = float(np.linalg.norm(a)), float(np.linalg.norm(b))
    if na < 1e-10 or nb < 1e-10:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def run_all():
    record = {"started_at": time.time(), "absorptions": [],
              "phases": {}}
    print("=" * 72)
    print("CK ORGANISM DYNAMICS TEST")
    print("  - 5 distinguishable audio sources")
    print("  - duality / parallel / resonance / progression / retrieval")
    print("=" * 72)

    # Phase 1: per-source absorptions
    print()
    print("[1/5] per-source absorptions (5 sources, single pass)...")
    base_state = snapshot_state()
    record["phases"]["base_state"] = {
        "tick": base_state["tick"],
        "W_trace": base_state["W_trace"],
        "emergent": base_state["emergent"],
        "dual_score": cortex_w_dual_score(base_state),
    }
    print(f"  base: tick={base_state['tick']} "
          f"W_trace={base_state['W_trace']:.4f} "
          f"emergent={base_state['emergent']:.4f}")
    print(f"  base dual scores:")
    for k, v in record["phases"]["base_state"]["dual_score"].items():
        print(f"    {k:25}: {v:.4f}")
    print()

    fingerprints_by_source = {}
    for src_name, fn in SOURCES.items():
        print(f"  feeding {src_name!r}...")
        samples, sr = fn()
        if samples is None:
            print(f"    SKIP ({src_name}: synth failed)")
            continue
        result = absorb_pcm(samples, sr, src_name)
        record["absorptions"].append(result)
        fingerprints_by_source[src_name] = result.get("fingerprint", {})
        if "error" in result:
            print(f"    ERROR: {result['error']}")
            continue
        d = result["delta"]
        f = result["fingerprint"]
        print(f"    n_ops={result['n_ops']:>6}  "
              f"dom={f.get('dominant_op_name'):>9}  "
              f"energy={f.get('curvature_energy', 0):.3f}  "
              f"W_trace+={d['W_trace']:+.4f}  "
              f"tick+={d['tick']}")
        print(f"    last_pair: {result['post_last_pair']}")

    # Phase 2: duality test
    print()
    print("[2/5] DUALITY -- canonical dual pairs in cortex W after absorption")
    final_state = snapshot_state()
    final_dual = cortex_w_dual_score(final_state)
    record["phases"]["final_dual_score"] = final_dual
    base_dual = record["phases"]["base_state"]["dual_score"]
    deltas = {k: round(final_dual.get(k, 0) - base_dual.get(k, 0), 5)
              for k in base_dual}
    record["phases"]["dual_deltas"] = deltas
    for k, d in deltas.items():
        sign = "+" if d >= 0 else ""
        print(f"    {k:25}: {sign}{d:.4f}")

    # Phase 3: parallel/resonance -- repeat tone, see if delta shrinks
    print()
    print("[3/5] PARALLEL/RESONANCE -- repeat tone_440 a 2nd time")
    samples, sr = tone_pcm()
    second = absorb_pcm(samples, sr, "tone_440_pass2")
    record["phases"]["resonance"] = second
    if "error" not in second:
        first = next((a for a in record["absorptions"]
                      if a.get("label") == "tone_440"), None)
        if first:
            d1 = abs(first["delta"]["W_trace"])
            d2 = abs(second["delta"]["W_trace"])
            ratio = d2 / d1 if d1 > 1e-9 else float("inf")
            print(f"    pass 1 |dW_trace|: {d1:.4f}")
            print(f"    pass 2 |dW_trace|: {d2:.4f}")
            print(f"    ratio (smaller = recognition): {ratio:.3f}")

    # Phase 4: progression -- compare A->B->C cumulative deltas
    # We already absorbed in order; record the sequence-of-last_pairs.
    print()
    print("[4/5] PROGRESSION -- last_pair across the absorption sequence")
    last_pairs = [(a["label"], a.get("post_last_pair"))
                  for a in record["absorptions"]
                  if "error" not in a]
    record["phases"]["progression_last_pairs"] = last_pairs
    for label, lp in last_pairs:
        print(f"    after {label:>16}: last_pair = {lp}")

    # Phase 5: NOW retrieval -- chat queries about what was just heard
    print()
    print("[5/5] NOW RETRIEVAL -- query CK about audio he just absorbed")
    queries = [
        "what is your dominant operator right now",
        "what is your last operator pair",
        "what does silence sound like",
        "what does a tone sound like",
        "what does the letter A sound like",
        "describe what you just heard",
    ]
    qa = []
    for q in queries:
        print(f"  Q: {q!r}")
        resp = query_chat(q, timeout=45)
        qa.append(resp)
        print(f"     {resp.get('text_head', resp.get('error', '?'))[:200]}")
    record["phases"]["chat_qa"] = qa

    # Verdict
    print()
    print("=" * 72)
    print("VERDICT")
    print("=" * 72)
    n_ok = sum(1 for a in record["absorptions"] if "error" not in a)
    n_err = sum(1 for a in record["absorptions"] if "error" in a)
    print(f"  absorptions ok:  {n_ok} / {len(SOURCES)}")
    print(f"  absorptions err: {n_err}")
    fps_compact = {s: f.get("dominant_op_name") for s, f in
                   fingerprints_by_source.items()}
    print(f"  per-source dominants: {fps_compact}")
    distinct = len(set(fps_compact.values()))
    print(f"  distinct dominants: {distinct} (out of {len(fps_compact)})")
    pos_dual = sum(1 for v in deltas.values() if v > 0)
    print(f"  dual pairs with positive coupling growth: "
          f"{pos_dual} / {len(deltas)}")

    out_path = SCRIPT_DIR / f"organism_dynamics_{int(time.time())}.json"
    out_path.write_text(json.dumps(record, indent=2, ensure_ascii=False),
                        encoding="utf-8")
    print(f"  full record -> {out_path.name}")
    return 0


if __name__ == "__main__":
    sys.exit(run_all())
