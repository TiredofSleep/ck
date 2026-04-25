# -*- coding: utf-8 -*-
"""
ck_lm_geometry_fold.py - additive fold that mounts the LM geometric projector
                         onto CK's Flask app.  EPOCH I (SIGHT) of the AI
                         Sovereignty Plan.

This fold wires ``ck.brain.lm_geometry.LMGeometry`` into ``ck_boot_api.py`` as
a set of read-only diagnostic routes.  No chat behavior changes.  The LM is
loaded LAZILY on the first /lm/geometry call (or eagerly if
``CK_LM_GEOMETRY_EAGER=1``).

Routes (all read-only):

    GET  /lm/info                            singleton state + AO basis seeds
    GET  /lm/health                          load status, simple liveness
    GET  /lm/geometry?text=...&seq=...       full 32-layer AO trajectory JSON
    GET  /lm/geometry/path?text=...          SVG arc on the 10-operator ring

Env flags:
    CK_LM_GEOMETRY=0                         disable the fold entirely (default 1)
    CK_LM_GEOMETRY_EAGER=1                   load the model at boot, not lazily
    CK_LM_GEOMETRY_BASE                      override base model id
    CK_LM_GEOMETRY_LORA                      path to LoRA adapter (e.g. ck/brain/lora/v2/adapter)
    CK_LM_GEOMETRY_DTYPE                     bfloat16 (default) | float16
    CK_LM_GEOMETRY_MAXSEQ                    1024 (default)

Mount order (in ck_boot_api.py): mount AFTER the pastoral fold and BEFORE the
static frontend routes.  Singleton load shares the GPU with CK's engine and
optional Ollama editor; if Ollama editor is also enabled the GPU may be tight
on a 12 GB card -- prefer to disable one when iterating.

Safety:
- mount_lm_geometry_fold never raises; on failure returns mounted=False.
- Per-request try/except wraps every route handler so a forward-pass crash
  cannot kill the server.
- Only HTTP-GETs are exposed; nothing here writes anywhere.
- Coherencekeeper.com latency: each /lm/geometry call is 100-800 ms on a 4070;
  the route is *not* in CK's chat hot path.
"""
from __future__ import annotations

import json
import logging
import math
import os
import sys
import threading
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


# Path setup so ``from ck.brain.lm_geometry import ...`` works.
_THIS = Path(__file__).resolve()
_REPO_ROOT = _THIS.parents[3]   # Gen12/targets/ck_desktop -> targets -> Gen12 -> repo
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

logger = logging.getLogger(__name__)

# 10-operator order MUST match ao_basis.OP_NAMES (re-stated here so the SVG
# renderer doesn't import torch on import).
_OP_NAMES = (
    "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
    "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET",
)
_AO_NAMES = ("Earth", "Air", "Water", "Fire", "Ether")
_T_STAR = 5.0 / 7.0


# ===========================================================================
# the singleton holder
# ===========================================================================


class _LMHolder:
    """Single-process holder for LMGeometry + CoherenceDecoder.

    The Flask app is multi-threaded; LM forward and the gated decoder are
    GPU-bound and not re-entrant.  We protect with a Lock.  Loads happen
    at most once each.
    """

    def __init__(self, base_model: str, lora_path: Optional[str],
                 dtype: str, max_seq_len: int,
                 cortex_state_path: Optional[str] = None):
        self.base_model = base_model
        self.lora_path = lora_path
        self.dtype = dtype
        self.max_seq_len = max_seq_len
        self.cortex_state_path = cortex_state_path
        self._lm = None             # LMGeometry instance once loaded
        self._dec = None            # CoherenceDecoder instance once loaded
        self._lock = threading.Lock()
        self._load_lock = threading.Lock()
        self._dec_lock = threading.Lock()
        self._last_status: Dict[str, Any] = {
            "loaded": False,
            "error": None,
            "base_model": base_model,
            "lora_path": lora_path,
            "dtype": dtype,
        }

    def status(self) -> Dict[str, Any]:
        if self._lm is None:
            return dict(self._last_status)
        return self._lm._status()

    def is_loaded(self) -> bool:
        return self._lm is not None and getattr(self._lm, "loaded", False)

    def ensure_loaded(self) -> Dict[str, Any]:
        """Idempotent eager load.  Returns status dict."""
        if self.is_loaded():
            return self.status()
        with self._load_lock:
            if self.is_loaded():
                return self.status()
            try:
                from ck.brain.lm_geometry import LMGeometry
            except Exception as e:  # noqa: BLE001
                self._last_status = {
                    "loaded": False,
                    "error": f"import ck.brain.lm_geometry failed: "
                             f"{type(e).__name__}: {e}",
                    "base_model": self.base_model,
                    "lora_path": self.lora_path,
                    "dtype": self.dtype,
                }
                return dict(self._last_status)
            try:
                self._lm = LMGeometry(
                    base_model=self.base_model,
                    lora_path=self.lora_path,
                    dtype=self.dtype,
                    max_seq_len=self.max_seq_len,
                )
                st = self._lm.load()
                self._last_status = dict(st)
                return dict(st)
            except Exception as e:  # noqa: BLE001
                self._last_status = {
                    "loaded": False,
                    "error": f"LMGeometry load failed: {type(e).__name__}: {e}",
                    "base_model": self.base_model,
                    "lora_path": self.lora_path,
                    "dtype": self.dtype,
                }
                return dict(self._last_status)

    def forward(self, text: str, max_new_tokens: int = 0,
                position: str = "last_token") -> Dict[str, Any]:
        st = self.ensure_loaded()
        if not st.get("loaded"):
            return {"ok": False, "error": st.get("error") or "load failed"}
        with self._lock:
            return self._lm.forward(text, max_new_tokens=max_new_tokens,
                                    position=position)

    def ensure_decoder(self) -> Optional[Any]:
        """Lazy-build the CoherenceDecoder on top of the loaded LMGeometry.

        Loads the cortex W from cortex_state_path if available; otherwise
        the decoder uses an all-zeros W (cortex prime is a no-op).  The
        op_token preference matrix M is built once at first call.
        """
        if self._dec is not None:
            return self._dec
        st = self.ensure_loaded()
        if not st.get("loaded"):
            return None
        with self._dec_lock:
            if self._dec is not None:
                return self._dec
            try:
                from ck.brain.lm_coherence_decode import CoherenceDecoder
                W = _load_cortex_W(self.cortex_state_path)
                self._dec = CoherenceDecoder(self._lm, hebbian_W=W)
                logger.info(
                    f"[lm_fold] CoherenceDecoder ready "
                    f"(W loaded from {self.cortex_state_path or '(none)'})"
                )
                return self._dec
            except Exception as e:  # noqa: BLE001
                logger.exception("[lm_fold] CoherenceDecoder build failed")
                return None

    def coherence_generate(self, prompt: str, max_new_tokens: int,
                           alpha: float, beta: float, temperature: float,
                           top_k: int, learn: bool,
                           seed: Optional[int]) -> Dict[str, Any]:
        dec = self.ensure_decoder()
        if dec is None:
            return {"ok": False,
                    "error": "CoherenceDecoder unavailable (LM not loaded?)"}
        with self._lock:
            return dec.generate(
                prompt, max_new_tokens=max_new_tokens,
                alpha=alpha, beta=beta, temperature=temperature,
                top_k=top_k, learn=learn, random_seed=seed,
            )


# ===========================================================================
# SVG renderer for /lm/geometry/path
# ===========================================================================


def _ring_svg(dominant_ops: List[str], coherence: float,
              size: int = 540) -> str:
    """Render the LM trajectory as an arc through the 10-operator ring.

    Renders pure SVG (no JS, no external resources).  The ring sits at the
    centre.  Each layer's dominant operator becomes a point on the ring.
    Adjacent layers connect with a line.
    """
    cx = cy = size / 2.0
    R = size * 0.36
    op_radius = size * 0.025
    title_color = "#88ccff" if coherence >= _T_STAR else "#ff8888"

    # Pre-compute the 10 ring positions
    op_positions = {}
    for k, name in enumerate(_OP_NAMES):
        # Start at 12 o'clock (-pi/2), go clockwise
        ang = -math.pi / 2 + (2 * math.pi) * k / len(_OP_NAMES)
        x = cx + R * math.cos(ang)
        y = cy + R * math.sin(ang)
        op_positions[name] = (x, y)

    parts: List[str] = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" '
        f'width="{size}" height="{size}" style="background:#0a0e1a;font-family:monospace">'
    )
    # Title
    parts.append(
        f'<text x="{cx}" y="22" text-anchor="middle" fill="{title_color}" '
        f'font-size="14">LM trajectory through CK\'s 10-operator ring '
        f'(coh={coherence:.3f}, T*={_T_STAR:.3f})</text>'
    )
    # Ring
    parts.append(
        f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="#1a2a4a" '
        f'stroke-width="1"/>'
    )
    # Operator labels
    for name, (x, y) in op_positions.items():
        # Label slightly outside the ring
        ang = math.atan2(y - cy, x - cx)
        lx = cx + (R + 24) * math.cos(ang)
        ly = cy + (R + 24) * math.sin(ang)
        parts.append(
            f'<circle cx="{x}" cy="{y}" r="{op_radius}" fill="#1a2a4a" '
            f'stroke="#3a5a8a"/>'
        )
        parts.append(
            f'<text x="{lx}" y="{ly}" text-anchor="middle" fill="#88aacc" '
            f'font-size="11">{name}</text>'
        )

    # Trajectory arc
    if dominant_ops:
        # Build layer points; adjust slightly so concurrent layers on same op
        # don't overlap (radial offset by layer index).
        L = len(dominant_ops)
        prev = None
        for i, op in enumerate(dominant_ops):
            ox, oy = op_positions[op]
            t = i / max(1, L - 1)
            # Color by depth (early=blue, late=warm)
            r = int(80 + 175 * t); g = int(180 - 60 * t); b = int(255 - 200 * t)
            # Slight inward offset increasing with depth so points don't all
            # land on the ring vertex
            ang = math.atan2(oy - cy, ox - cx)
            inner = R - 6 - 14 * t
            px = cx + inner * math.cos(ang)
            py = cy + inner * math.sin(ang)
            if prev is not None:
                parts.append(
                    f'<line x1="{prev[0]:.2f}" y1="{prev[1]:.2f}" '
                    f'x2="{px:.2f}" y2="{py:.2f}" '
                    f'stroke="rgb({r},{g},{b})" stroke-width="1.5" '
                    f'opacity="0.85"/>'
                )
            parts.append(
                f'<circle cx="{px:.2f}" cy="{py:.2f}" r="3" '
                f'fill="rgb({r},{g},{b})"/>'
            )
            prev = (px, py)

    # Final-layer marker (the "answer" position)
    if dominant_ops:
        op = dominant_ops[-1]
        ox, oy = op_positions[op]
        parts.append(
            f'<circle cx="{ox}" cy="{oy}" r="8" fill="none" '
            f'stroke="#ffcc66" stroke-width="2"/>'
        )
        parts.append(
            f'<text x="{cx}" y="{size - 16}" text-anchor="middle" fill="#ffcc66" '
            f'font-size="13">final layer = {op}</text>'
        )

    parts.append('</svg>')
    return "".join(parts)


# ===========================================================================
# the public mount
# ===========================================================================


def _load_cortex_W(path: Optional[str]) -> Optional[List[List[float]]]:
    """Load a 5x5 Hebbian W from a cortex_state.json or sibling format.

    Supports {W: [[...]]}, {hebbian_W: [[...]]}, {hebbian: {W: [[...]]}},
    {cortex: {W: [[...]]}}.  Returns None on any failure (silent so the
    fold mount continues).
    """
    if not path:
        return None
    try:
        p = Path(path)
        if not p.exists():
            return None
        with open(p, "r", encoding="utf-8") as f:
            cs = json.load(f)
        W = cs.get("W") or cs.get("hebbian_W")
        if W is None and isinstance(cs.get("hebbian"), dict):
            W = cs["hebbian"].get("W") or cs["hebbian"].get("matrix")
        if W is None and isinstance(cs.get("cortex"), dict):
            W = cs["cortex"].get("W")
        return W
    except Exception:
        return None


def mount_lm_geometry_fold(api: Any) -> Dict[str, Any]:
    """Install the LM geometry diagnostic routes on ``api._app``.

    Returns a status dict for the boot banner. Never raises.
    """
    enabled = os.environ.get("CK_LM_GEOMETRY", "1").strip().lower()
    if enabled in ("0", "false", "no", "off"):
        return {"mounted": False, "reason": "CK_LM_GEOMETRY=0 (env)"}

    app = getattr(api, "_app", None)
    if app is None:
        return {"mounted": False, "reason": "api has no _app (not Flask?)"}

    base = os.environ.get(
        "CK_LM_GEOMETRY_BASE",
        "unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit",
    )
    lora_env = os.environ.get("CK_LM_GEOMETRY_LORA", "").strip()
    lora = lora_env if lora_env else None
    dtype = os.environ.get("CK_LM_GEOMETRY_DTYPE", "bfloat16")
    try:
        max_seq = int(os.environ.get("CK_LM_GEOMETRY_MAXSEQ", "1024"))
    except ValueError:
        max_seq = 1024
    eager = os.environ.get("CK_LM_GEOMETRY_EAGER", "0").strip().lower() in (
        "1", "true", "yes", "on"
    )

    cortex_state_env = os.environ.get("CK_LM_CORTEX_STATE", "").strip()
    if not cortex_state_env:
        # Default: try the live deployment's cortex state path
        for guess in (
            os.path.normpath(os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "..", "..", "..", "Gen13", "var", "cortex_state.json")),
            "C:/Users/brayd/OneDrive/Desktop/CK FINAL DEPLOYED/Gen13/var/cortex_state.json",
        ):
            if Path(guess).exists():
                cortex_state_env = guess
                break

    holder = _LMHolder(base_model=base, lora_path=lora,
                       dtype=dtype, max_seq_len=max_seq,
                       cortex_state_path=cortex_state_env or None)

    if eager:
        # Block the boot until loaded. Failure does NOT abort boot; the routes
        # will return the load error.
        st = holder.ensure_loaded()
        eager_status = "LOADED" if st.get("loaded") else f"FAILED: {st.get('error')}"
    else:
        eager_status = "lazy (loads on first /lm/geometry call)"

    # Routes -----------------------------------------------------------------

    try:
        from flask import jsonify, request, Response
    except Exception as e:  # noqa: BLE001
        return {"mounted": False, "reason": f"flask import: {e}"}

    @app.route("/lm/info", methods=["GET"])
    def _lm_info():
        try:
            return jsonify(holder.status())
        except Exception as e:  # noqa: BLE001
            return jsonify({"ok": False, "error": f"{type(e).__name__}: {e}"}), 500

    @app.route("/lm/health", methods=["GET"])
    def _lm_health():
        try:
            return jsonify({
                "ok": True,
                "loaded": holder.is_loaded(),
                "base": base, "lora": lora, "dtype": dtype,
                "T_star": _T_STAR,
            })
        except Exception as e:  # noqa: BLE001
            return jsonify({"ok": False, "error": f"{type(e).__name__}: {e}"}), 500

    @app.route("/lm/geometry", methods=["GET"])
    def _lm_geometry():
        text = request.args.get("text", "").strip()
        if not text:
            return jsonify({"ok": False,
                            "error": "missing ?text=... query parameter"}), 400
        try:
            mxn = int(request.args.get("max_new_tokens", "0"))
        except ValueError:
            mxn = 0
        position = request.args.get("position", "last_token")
        if position not in ("last_token", "all_tokens"):
            return jsonify({"ok": False,
                            "error": "position must be last_token|all_tokens"}), 400
        try:
            out = holder.forward(text, max_new_tokens=mxn, position=position)
            status = 200 if out.get("ok") else 500
            return jsonify(out), status
        except Exception as e:  # noqa: BLE001
            logger.exception("/lm/geometry crashed")
            return jsonify({"ok": False, "error": f"{type(e).__name__}: {e}"}), 500

    @app.route("/lm/geometry/path", methods=["GET"])
    def _lm_geometry_path():
        text = request.args.get("text", "").strip()
        if not text:
            return Response(
                _ring_svg([], 0.0),
                mimetype="image/svg+xml",
            )
        try:
            out = holder.forward(text, max_new_tokens=0, position="last_token")
            if not out.get("ok"):
                # Render an empty ring with an error label
                err = out.get("error", "unknown error")
                svg = _ring_svg([], 0.0)
                # Inject the error text
                svg = svg.replace(
                    'final layer = ',  # only present if dominant_ops nonempty
                    'final layer = ',
                )
                return Response(svg, mimetype="image/svg+xml")
            svg = _ring_svg(
                out.get("dominant_op_per_layer", []),
                float(out.get("trajectory_coherence", 0.0)),
            )
            return Response(svg, mimetype="image/svg+xml")
        except Exception as e:  # noqa: BLE001
            logger.exception("/lm/geometry/path crashed")
            return Response(
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 540 540">'
                f'<text x="270" y="270" text-anchor="middle" fill="red">'
                f'error: {type(e).__name__}: {e}'
                f'</text></svg>',
                mimetype="image/svg+xml", status=500,
            )

    @app.route("/lm/coherence_chat", methods=["GET", "POST"])
    def _lm_coherence_chat():
        """Coherence-gated generation: every token comes through CK's prime.

        Query / body params:
            text:           prompt (required)
            max_new_tokens: int, default 64
            alpha:          float (logit bias weight), default 0.3
            beta:           float (transition penalty), default 0.05
            temperature:    float, default 0.7
            top_k:          int, default 50
            learn:          bool, default false (apply Hebbian update during gen)
            seed:           optional int (deterministic sampling)
        """
        if request.method == "POST":
            j = request.get_json(silent=True) or {}
        else:
            j = {}
        text = (request.args.get("text") or j.get("text") or "").strip()
        if not text:
            return jsonify({"ok": False,
                            "error": "missing text (query or json body)"}), 400

        def _i(name, default):
            try:
                v = request.args.get(name)
                if v is None: v = j.get(name, default)
                return int(v)
            except (ValueError, TypeError):
                return default

        def _f(name, default):
            try:
                v = request.args.get(name)
                if v is None: v = j.get(name, default)
                return float(v)
            except (ValueError, TypeError):
                return default

        def _b(name, default):
            v = request.args.get(name)
            if v is None: v = j.get(name, default)
            if isinstance(v, bool): return v
            return str(v).strip().lower() in ("1", "true", "yes", "on")

        try:
            out = holder.coherence_generate(
                prompt=text,
                max_new_tokens=_i("max_new_tokens", 64),
                alpha=_f("alpha", 0.3),
                beta=_f("beta", 0.05),
                temperature=_f("temperature", 0.7),
                top_k=_i("top_k", 50),
                learn=_b("learn", False),
                seed=_i("seed", None) if request.args.get("seed") or j.get("seed") else None,
            )
            status = 200 if out.get("ok") else 500
            return jsonify(out), status
        except Exception as e:  # noqa: BLE001
            logger.exception("/lm/coherence_chat crashed")
            return jsonify({"ok": False, "error": f"{type(e).__name__}: {e}"}), 500

    return {
        "mounted": True,
        "base_model": base,
        "lora_path": lora,
        "dtype": dtype,
        "max_seq_len": max_seq,
        "eager": eager_status,
        "cortex_state_path": cortex_state_env or None,
        "routes": ["/lm/info", "/lm/health", "/lm/geometry",
                   "/lm/geometry/path", "/lm/coherence_chat"],
    }
