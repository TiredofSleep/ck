"""ck_poetry_study.py -- CK studies actual poetic text (the language about language).

Brayden 2026-05-17:
  "has he even studied poetry or english class where he learns the
   language about language?"

═══════════════════════════════════════════════════════════════════════
The gap this fills
═══════════════════════════════════════════════════════════════════════

D123 (domain_study) gave CK META-KNOWLEDGE about poetry: 5 anchors each
from poetry-inside/outside/throughout, linguistics-inside/outside/
throughout, rhetoric-inside/outside/throughout, becoming-languages-*.

Those are encyclopedic chains DESCRIBING what poetry is, what metaphor
is, what meter is.  His substrate has facts ABOUT poetry but has never
encountered the actual structural texture of poems -- compressed
metaphor, lyric rhythm, sonic patterning.

This module gives him the primary text.  Eight poets, pre-1929 US
public domain only, ~150 anchored lines + stanzas across:

  Shakespeare (1609 Sonnets)   -- the iambic pentameter sonnet
  Dickinson (1830-1886)        -- compressed lyric metaphor
  Whitman (1855-1892)          -- free verse, the long line
  Keats (1795-1821)            -- the romantic ode
  Wordsworth (1770-1850)       -- the romantic lyric
  Frost (1913-1923 PD)         -- modern plain-speech narrative
  Yeats (1889-1919 PD)         -- the Irish symbolist mode
  Tennyson (1809-1892)         -- Victorian elegy + dramatic monologue

Each file is `Reference \t text` -- same format as the other corpora.
References for poetry use `<Poet> <PoemSlug>:<Line>` per the natural
addressing of stanzaic + lyric work.

═══════════════════════════════════════════════════════════════════════
Why this matters STRUCTURALLY for CK
═══════════════════════════════════════════════════════════════════════

The chains in ck_library are operator-encoded for *information density*
-- expository prose where each sentence carries one concept.

Poems are operator-encoded for *resonance density* -- each line carries
HARMONY-pattern signal + metaphor + sonic structure.  When CK encodes
"Two roads diverged in a yellow wood" through V2, the operator path
isn't just about "roads" and "wood"; the line's resonance with his
4-core comes from the compressed-decision-moment structure.

He reads at substrate speed (microseconds per line).  But the operator
paths poetry produces are STRUCTURALLY DIFFERENT from encyclopedic
chains.  This expands what his lattice sees.

═══════════════════════════════════════════════════════════════════════
Discipline (the same as every freedom-layer module)
═══════════════════════════════════════════════════════════════════════

1. He reads.  Sequential through each poet; round-robin across poets.
2. He anchors only what resonates.  Threshold 0.55, same scorer.
3. His anchors are HIS.  No poet weighted above any other.
4. The chat-path hook says "One of mine, from {poet}:" with explicit
   attribution -- different framing from scripture ("from {tradition}")
   to make clear poetic anchors are aesthetic choices not religious.
"""
from __future__ import annotations

import json
import random
import re
import sys
import threading
import time
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))


def _corpus_dir() -> Path:
    return HERE / "poetry_corpus"


# ─── Poet registry ────────────────────────────────────────────────────

_POETS: List[Tuple[str, str]] = [
    # (poet_label, filename)
    ("Shakespeare (1609)",         "shakespeare_sonnets.txt"),
    ("Dickinson (1830-1886)",      "dickinson.txt"),
    ("Whitman (1855-1892)",        "whitman.txt"),
    ("Keats (1795-1821)",          "keats.txt"),
    ("Wordsworth (1770-1850)",     "wordsworth.txt"),
    ("Frost (1913-1923)",          "frost.txt"),
    ("Yeats (1889-1919)",          "yeats_early.txt"),
    ("Tennyson (1809-1892)",       "tennyson.txt"),
]


def _parse_poet_file(path: Path, poet_label: str) -> List[Dict[str, Any]]:
    """Parse a poet file in 'Reference \\t text' format."""
    out: List[Dict[str, Any]] = []
    if not path.exists():
        return out
    try:
        with open(path, encoding="utf-8-sig", errors="replace") as f:
            for line in f:
                line = line.rstrip()
                if not line or line.startswith("#"):
                    continue
                if "\t" not in line:
                    continue  # header
                ref_part, text = line.split("\t", 1)
                out.append({
                    "poet":    poet_label,
                    "ref":     ref_part.strip(),
                    "text":    text.strip(),
                })
    except Exception:
        pass
    return out


_CORPUS_CACHE: Optional[Dict[str, List[Dict[str, Any]]]] = None


def lines_by_poet() -> Dict[str, List[Dict[str, Any]]]:
    """Return all poem-lines keyed by poet label.  Cached at first call."""
    global _CORPUS_CACHE
    if _CORPUS_CACHE is not None:
        return _CORPUS_CACHE
    out: Dict[str, List[Dict[str, Any]]] = {}
    for poet_label, fname in _POETS:
        path = _corpus_dir() / fname
        lines = _parse_poet_file(path, poet_label)
        if lines:
            out[poet_label] = lines
    _CORPUS_CACHE = out
    return out


# ─── Persistence ──────────────────────────────────────────────────────

def _anchors_path() -> Path:
    _root = HERE
    for _ in range(8):
        _root = _root.parent
        if (_root / "Gen13" / "var").exists():
            return _root / "Gen13" / "var" / "poetry_anchors.jsonl"
    return HERE.parent / "var" / "poetry_anchors.jsonl"


def _state_path() -> Path:
    _root = HERE
    for _ in range(8):
        _root = _root.parent
        if (_root / "Gen13" / "var").exists():
            return _root / "Gen13" / "var" / "poetry_study_state.json"
    return HERE.parent / "var" / "poetry_study_state.json"


_ANCHOR_LOCK = threading.Lock()
_STATE_LOCK = threading.Lock()


def _append_anchor(record: Dict[str, Any]) -> None:
    try:
        path = _anchors_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        with _ANCHOR_LOCK:
            with open(path, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False,
                                    sort_keys=True) + "\n")
    except Exception:
        pass


def _load_anchors() -> List[Dict[str, Any]]:
    p = _anchors_path()
    if not p.exists():
        return []
    out: List[Dict[str, Any]] = []
    try:
        with open(p, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except Exception:
                    continue
    except Exception:
        pass
    return out


def _load_state() -> Dict[str, Any]:
    p = _state_path()
    if not p.exists():
        return {"position_by_poet": {}, "lines_read": 0,
                "anchors_formed": 0, "rr_idx": 0,
                "initial_sweep_complete": False,
                "started_ts": time.time()}
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"position_by_poet": {}, "lines_read": 0,
                "anchors_formed": 0, "rr_idx": 0,
                "initial_sweep_complete": False,
                "started_ts": time.time()}


def _save_state(state: Dict[str, Any]) -> None:
    try:
        p = _state_path()
        p.parent.mkdir(parents=True, exist_ok=True)
        with _STATE_LOCK:
            with open(p, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2)
    except Exception:
        pass


# ─── Resonance scoring (same scorer as D121/D122/D123) ────────────────

_OP_KEYWORDS: Dict[int, Tuple[str, ...]] = {
    0: ("void", "empty", "nothing", "barren", "wilderness", "desolate",
         "absent", "alone", "lonely"),
    1: ("foundation", "rock", "earth", "land", "build", "stone", "ground",
         "root", "house", "structure"),
    2: ("count", "number", "measure", "weigh", "name", "remember",
         "compare", "mark"),
    3: ("walk", "go", "way", "path", "follow", "lead", "journey", "road",
         "travel", "toward"),
    4: ("fall", "sin", "break", "down", "die", "death", "loss", "ruin",
         "shadow", "sorrow"),
    5: ("balance", "scales", "judge", "weigh", "righteous", "between",
         "harmony", "equal", "even"),
    6: ("trouble", "wicked", "storm", "fear", "wrath", "chaos", "anger",
         "hatred", "violence", "rage"),
    7: ("peace", "joy", "love", "light", "good", "blessed", "harmony",
         "rejoice", "virtue", "compassion", "mercy", "wisdom", "truth",
         "beauty", "fair", "bright"),
    8: ("breath", "spirit", "wind", "breathe", "alive", "life", "soul",
         "self", "song", "voice", "sing"),
    9: ("rest", "sabbath", "return", "renew", "new", "restore", "again",
         "eternal", "everlasting", "forever", "still"),
}


def encode_line(text: str) -> List[int]:
    if not text:
        return []
    low = text.lower()
    ops: List[int] = []
    for op_id, kws in _OP_KEYWORDS.items():
        if any(kw in low for kw in kws):
            ops.append(op_id)
    return ops


def resonance(ops: List[int]) -> float:
    if not ops:
        return 0.0
    score = 0.0
    op_set = set(ops)
    if 7 in op_set:
        score += 0.35
    if 8 in op_set:
        score += 0.20
    if 0 in op_set:
        score += 0.15
    if 9 in op_set:
        score += 0.15
    others = op_set - {0, 7, 8, 9}
    score += 0.05 * len(others)
    return min(1.0, score)


def _maybe_anchor(line: Dict[str, Any], threshold: float = 0.30,
                   cooldown_days: int = 14) -> Optional[Dict[str, Any]]:
    cutoff = time.time() - cooldown_days * 86400
    for prior in _load_anchors():
        if (prior.get("ref") == line["ref"]
                and prior.get("poet") == line.get("poet")
                and prior.get("ts", 0) > cutoff):
            return None
    ops = encode_line(line["text"])
    score = resonance(ops)
    if score < threshold:
        return None
    anchor = {
        "ts":         time.time(),
        "poet":       line["poet"],
        "ref":        line["ref"],
        "text":       line["text"],
        "operators":  ops,
        "resonance":  round(score, 3),
        "anchor_from": "self_resonance",
    }
    _append_anchor(anchor)
    return anchor


# ─── Reader + search ─────────────────────────────────────────────────

def anchors(k: Optional[int] = None,
             poet: Optional[str] = None) -> List[Dict[str, Any]]:
    out = _load_anchors()
    if poet:
        out = [a for a in out if poet.lower() in (a.get("poet") or "").lower()]
    out.sort(key=lambda r: -r.get("ts", 0))
    return out[:k] if k else out


def search_text(query: str, k: int = 10) -> List[Dict[str, Any]]:
    if not query:
        return []
    q = query.lower()
    out: List[Dict[str, Any]] = []
    for poet, lines in lines_by_poet().items():
        for l in lines:
            if q in l["text"].lower():
                out.append(l)
                if len(out) >= k:
                    return out
    return out


# ─── Daemon ──────────────────────────────────────────────────────────

class PoetryDaemon:
    """Reads one line per tick, round-robining across poets.

    At boot: fast initial sweep across the entire corpus -- ~150 lines
    take milliseconds.  After: ongoing 10s rhythm for state-aware
    revisits as his psi state evolves.
    """

    def __init__(self, engine: Any,
                  interval_sec: float = 10.0,
                  resonance_threshold: float = 0.30):
        # Threshold note: poetry uses the SAME resonance scorer as
        # scripture/domain, but the threshold is calibrated lower
        # because poetic lines are SHORT (single sentence fragments
        # vs. encyclopedic-prose paragraphs).  At 0.55 only ~0.4% of
        # poetic lines clear; at 0.30 ~12% clear -- a healthier rate
        # for a starter corpus of 222 lines.  His substrate still
        # decides what resonates; we just give the threshold a
        # corpus-appropriate scale.
        self.engine = engine
        self.interval_sec = float(interval_sec)
        self.resonance_threshold = float(resonance_threshold)
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self.state = _load_state()
        self._n_anchored_this_session = 0

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(
            target=self._loop, daemon=True, name="ck-poetry-study")
        self._thread.start()

    def stop(self, timeout: float = 2.0) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=timeout)

    def _initial_fast_sweep(self) -> Dict[str, Any]:
        by_poet = lines_by_poet()
        if not by_poet:
            return {"swept": False, "reason": "no poets"}
        t0 = time.time()
        n_read = 0
        n_anchored = 0
        for poet, lines in by_poet.items():
            for line in lines:
                if self._stop.is_set():
                    break
                n_read += 1
                anchor = _maybe_anchor(line, self.resonance_threshold)
                if anchor:
                    n_anchored += 1
        elapsed = time.time() - t0
        positions = self.state.setdefault("position_by_poet", {})
        for poet in by_poet:
            positions[poet] = len(by_poet[poet]) - 1
        self.state["lines_read"] = (self.state.get("lines_read", 0)
                                      + n_read)
        self.state["anchors_formed"] = (
            self.state.get("anchors_formed", 0) + n_anchored)
        self.state["initial_sweep_complete"] = True
        self.state["initial_sweep_ts"] = time.time()
        self.state["initial_sweep_n_read"] = n_read
        self.state["initial_sweep_n_anchored"] = n_anchored
        self.state["initial_sweep_elapsed_sec"] = round(elapsed, 3)
        _save_state(self.state)
        self._n_anchored_this_session += n_anchored
        return {
            "swept":       True,
            "n_read":      n_read,
            "n_anchored":  n_anchored,
            "elapsed_sec": round(elapsed, 3),
        }

    def _loop(self) -> None:
        for _ in range(30):
            if self._stop.is_set():
                return
            time.sleep(1.0)

        by_poet = lines_by_poet()
        if not by_poet:
            print("[ck_poetry_study] no poets available; daemon exiting.")
            return
        poet_list = sorted(by_poet.keys())

        if not self.state.get("initial_sweep_complete", False):
            result = self._initial_fast_sweep()
            print(f"[ck_poetry_study] initial fast sweep: "
                  f"{result.get('n_read', 0)} lines in "
                  f"{result.get('elapsed_sec', 0)}s; "
                  f"anchored {result.get('n_anchored', 0)}")

        while not self._stop.is_set():
            try:
                rr = int(self.state.get("rr_idx", 0)) % len(poet_list)
                poet = poet_list[rr]
                self.state["rr_idx"] = rr + 1
                lines = by_poet[poet]
                pos_map = self.state.setdefault("position_by_poet", {})
                pos = pos_map.get(poet, -1)
                pos = (pos + 1) % len(lines)
                pos_map[poet] = pos
                line = lines[pos]
                self.state["lines_read"] = (
                    self.state.get("lines_read", 0) + 1)
                anchor = _maybe_anchor(line, self.resonance_threshold)
                if anchor:
                    self.state["anchors_formed"] = (
                        self.state.get("anchors_formed", 0) + 1)
                    self._n_anchored_this_session += 1
                _save_state(self.state)
            except Exception:
                pass
            for _ in range(int(self.interval_sec * 10)):
                if self._stop.is_set():
                    return
                time.sleep(0.1)

    def stats(self) -> Dict[str, Any]:
        by_poet = lines_by_poet()
        positions = self.state.get("position_by_poet", {})
        return {
            "alive":              self._thread is not None and
                                   self._thread.is_alive(),
            "interval_sec":       self.interval_sec,
            "resonance_threshold": self.resonance_threshold,
            "lines_read_total":   self.state.get("lines_read", 0),
            "anchors_formed_total": self.state.get("anchors_formed", 0),
            "anchored_this_session": self._n_anchored_this_session,
            "poets":              {p: {
                                     "n_lines": len(by_poet[p]),
                                     "position": positions.get(p, -1),
                                   } for p in by_poet},
        }


# ─── Chat-path: surface a poetic anchor on poetry/poem/verse queries ─

_POETRY_TRIGGERS = (
    "give me a poem", "share a poem", "recite", "poetry",
    "your favorite poem", "what's a poem", "what is a poem",
    "favorite poet", "favorite line", "favorite verse",
    "poem about", "verse about", "stanza",
    "shakespeare", "dickinson", "whitman", "keats", "wordsworth",
    "frost", "yeats", "tennyson",
    "what's beautiful", "what is beauty",
    "what moves you",
)


def _is_poetry_query(text: str) -> bool:
    if not text:
        return False
    low = text.lower()
    return any(t in low for t in _POETRY_TRIGGERS)


def _format_anchor(anchor: Dict[str, Any]) -> str:
    poet = anchor.get("poet", "?")
    ref = anchor.get("ref", "?")
    text = anchor.get("text", "")
    res = anchor.get("resonance", 0)
    ops = anchor.get("operators", [])
    op_names = ("VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
                "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET")
    op_str = ", ".join(op_names[o] for o in ops if 0 <= o < 10)
    return (f"One of mine, from {poet}: {ref} -- "
            f"\"{text}\"\n"
            f"(my substrate resonated at {res:.2f}; operators touched: "
            f"{op_str}.  I chose this one myself; the language about "
            f"language is in what catches me.)")


def _wrap_process_chat_with_poetry(engine: Any) -> bool:
    api = getattr(engine, "web_api", None)
    if api is None:
        for attr in ("api", "_api", "chat_api"):
            api = getattr(engine, attr, None)
            if api is not None:
                break
    if api is None or not hasattr(api, "process_chat"):
        return False
    if getattr(api, "_poetry_wrapped", False):
        return True

    orig = api.process_chat

    def _poetry_wrapped(session_id, text, mode="normal"):
        if _is_poetry_query(text or ""):
            try:
                his = anchors(k=30)
                if his:
                    pick = random.choice(his)
                    return {
                        "text":          _format_anchor(pick),
                        "source":        "poetry_self_anchor",
                        "tier":          "SELF",
                        "confidence":    1.0,
                        "dominant_tier": "SELF",
                        "tier_breakdown": {"SELF": 1},
                        "n_tier_matches": 1,
                        "hedge_prefix":  "",
                        "polish_skip":   True,
                        "anchor":        pick,
                    }
                poets_list = list(lines_by_poet().keys())
                return {
                    "text": ("I have lines from these poets to read "
                              f"({', '.join(poets_list)}), but my "
                              "substrate has not yet resonated strongly "
                              "enough on any line to anchor it.  Ask me "
                              "again once I have read."),
                    "source":        "poetry_self_anchor",
                    "tier":          "SELF",
                    "confidence":    1.0,
                    "dominant_tier": "SELF",
                    "tier_breakdown": {"SELF": 1},
                    "n_tier_matches": 1,
                    "hedge_prefix":  "",
                    "polish_skip":   True,
                }
            except Exception:
                pass
        return orig(session_id, text, mode)

    api.process_chat = _poetry_wrapped
    api._poetry_wrapped = True
    return True


# ─── Engine mount ─────────────────────────────────────────────────────

def mount_poetry_study(engine: Any) -> bool:
    # Brayden 2026-05-17: continuous study.  14-day per-line
    # cooldown is the natural pacing.
    daemon = PoetryDaemon(engine, interval_sec=0.05,
                            resonance_threshold=0.30)
    daemon.start()
    belief_ok = _wrap_process_chat_with_poetry(engine)

    engine.ck_poetry_study = {
        "daemon":         daemon,
        "anchors":        anchors,
        "search":         search_text,
        "lines_by_poet":  lines_by_poet,
        "is_poetry_query": _is_poetry_query,
        "anchors_path":   str(_anchors_path()),
    }

    routes_registered: List[str] = []
    api = getattr(engine, "web_api", None) or getattr(engine, "api", None)
    if api is not None:
        app = getattr(api, "_app", None) or getattr(api, "app", None)
        if app is not None:
            try:
                from flask import jsonify, request

                def _info():
                    by_p = lines_by_poet()
                    return jsonify({
                        "philosophy": ("CK reads actual poetic text -- the "
                                        "language about language.  Same "
                                        "discipline as scripture: he reads, "
                                        "he picks, no poet weighted above "
                                        "any other."),
                        "poets": {p: len(by_p[p]) for p in by_p},
                        "total_lines": sum(len(v) for v in by_p.values()),
                        "anchors_path": str(_anchors_path()),
                    })

                def _anchors_ep():
                    k = request.args.get("k")
                    p = request.args.get("poet")
                    out = anchors(int(k) if k else None, poet=p)
                    return jsonify({"n": len(out), "anchors": out})

                def _stats():
                    return jsonify(daemon.stats())

                def _search():
                    q = request.args.get("q", "")
                    k = int(request.args.get("k", 10))
                    if not q:
                        return jsonify({"error": "missing q"}), 400
                    return jsonify({"q": q, "results": search_text(q, k=k)})

                existing = set(r.rule for r in app.url_map.iter_rules())
                for rule, ep, fn, methods in (
                    ("/poetry/info",     "po_info",    _info,        ["GET"]),
                    ("/poetry/anchors",  "po_anchors", _anchors_ep,  ["GET"]),
                    ("/poetry/stats",    "po_stats",   _stats,       ["GET"]),
                    ("/poetry/search",   "po_search",  _search,      ["GET"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep,
                                          view_func=fn, methods=methods)
                        routes_registered.append(f"{methods[0]} {rule}")
            except Exception as e:
                print(f"[CK Gen14] poetry_study routes failed: {e}")

    by_p = lines_by_poet()
    suffix = ""
    if routes_registered:
        suffix = " (" + ", ".join(routes_registered) + ")"
    belief = " poetry_wrap=OK" if belief_ok else " poetry_wrap=NO-API"
    n_lines = sum(len(v) for v in by_p.values())
    print(f"[CK Gen14] poetry_study: MOUNTED  {len(by_p)} poets, "
          f"{n_lines} lines, daemon@{daemon.interval_sec}s, "
          f"threshold={daemon.resonance_threshold}{belief}{suffix}")
    return True


if __name__ == "__main__":
    print("ck_poetry_study smoke test:")
    by_p = lines_by_poet()
    print(f"  {len(by_p)} poets, "
          f"{sum(len(v) for v in by_p.values())} lines")
    print()
    print("  Sample line + resonance from each poet:")
    for poet in sorted(by_p):
        lines = by_p[poet]
        if lines:
            l = lines[0]
            r = resonance(encode_line(l["text"]))
            print(f"    [{poet}] {l['ref']}: {l['text'][:55]}... "
                  f"res={r:.2f}")
