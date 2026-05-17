"""ck_domain_study.py -- CK studies all 341 subject domains in ck_library.

Brayden 2026-05-16:
  "yea, same for his studying mechanisms?  he is the fastest learning
   substrate on the planet cause he just needs to measure, store, and
   compare.. let him fly and learn to phd across domains!"

═══════════════════════════════════════════════════════════════════════
What this module is
═══════════════════════════════════════════════════════════════════════

`ck_library/` already contains 341 subject corpora -- each subject has
three pre-encoded chains files (`{subject}-inside`, `{subject}-outside`,
`{subject}-throughout`) at the standard format:

  meta.json:    {name, keywords[], op_signature[3], chain_count, created}
  chains.json:  {chains: [{text, ops, conv, trust, links, shp}, ...]}

The chains are ALREADY operator-encoded (`ops` field).  No further V2
work needed.  CK can ingest them at the speed of disk I/O + JSON parse
+ concept_learner.store -- microseconds per chain.

Total: ~85,000 chains across 341 subjects.  At his measured throughput
(~43K verses/sec on the simpler scripture-study path) the entire library
takes ~2-5 seconds to sweep on a quiet system.

═══════════════════════════════════════════════════════════════════════
What "PhD across domains" means here, concretely
═══════════════════════════════════════════════════════════════════════

For each subject, the daemon:

  1. MEASURE -- load the chains.json, extract every chain's (text, ops)
  2. STORE -- for each chain:
       - resonance score (same as D121/D122)
       - if resonance >= threshold: register as a *concept* in
         ck_concept_learner with tier=EXTERNAL (he's reading the world,
         not himself) and operator_signature = chain.ops
       - append to Gen13/var/domain_anchors.jsonl with subject + text +
         resonance + ops
  3. COMPARE -- via existing infrastructure:
       - ck_concept_learner cross-references via op_signature similarity
       - the listener_to_crystal daemon (D120) picks up new candidates
       - HER (hindsight) replays high-resonance entries

═══════════════════════════════════════════════════════════════════════
The 341 subjects (sample)
═══════════════════════════════════════════════════════════════════════

The library inventory is rich and broad:

  acoustics, aesthetics, algebra, artificial-intelligence, astronomy,
  biology, chemistry, computer-science, cryptography, economics, ...
  ... mathematics, philosophy, physics, programming, psychology, ...
  ... and 300+ more, each with inside/outside/throughout perspectives

Per-subject naming convention:
  -inside       : structural / mechanism-level chains
  -outside      : applications / context chains
  -throughout   : narrative / temporal chains

Plus "becoming-depth-*" and "becoming-languages-*" introspective sets.

═══════════════════════════════════════════════════════════════════════
Discipline (same as D118 / D119 / D120 / D121 / D122)
═══════════════════════════════════════════════════════════════════════

1. He reads.  We don't curate within a subject; we don't favor between
   subjects.  Sweep order is alphabetical across all 341.
2. He anchors only what resonates.  Threshold 0.55, same scorer as
   D121/D122 applied uniformly.
3. His anchors are HIS.  No subject is asserted "true"; CK picks
   whatever resonates with his current substrate state.
4. EXTERNAL tier, not SELF.  Domain knowledge enters at confidence
   ~0.27 baseline (D-identity tier-weighting), boosted to PROVED if
   he keeps re-encountering it across multiple subject angles.
"""
from __future__ import annotations

import json
import re
import sys
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))


def _library_dir() -> Path:
    """Path to ck_library/ at the repo root."""
    _root = HERE
    for _ in range(8):
        _root = _root.parent
        cand = _root / "ck_library"
        if cand.exists() and (cand / "_index.json").exists():
            return cand
    return HERE / "ck_library"


def _anchors_path() -> Path:
    _root = HERE
    for _ in range(8):
        _root = _root.parent
        if (_root / "Gen13" / "var").exists():
            return _root / "Gen13" / "var" / "domain_anchors.jsonl"
    return HERE.parent / "var" / "domain_anchors.jsonl"


def _state_path() -> Path:
    _root = HERE
    for _ in range(8):
        _root = _root.parent
        if (_root / "Gen13" / "var").exists():
            return _root / "Gen13" / "var" / "domain_study_state.json"
    return HERE.parent / "var" / "domain_study_state.json"


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


def _load_state() -> Dict[str, Any]:
    p = _state_path()
    if not p.exists():
        return {"subjects_swept": [],
                "chains_read":     0,
                "anchors_formed":  0,
                "initial_sweep_complete": False,
                "started_ts":      time.time()}
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"subjects_swept": [],
                "chains_read":     0,
                "anchors_formed":  0,
                "initial_sweep_complete": False,
                "started_ts":      time.time()}


def _save_state(state: Dict[str, Any]) -> None:
    try:
        p = _state_path()
        p.parent.mkdir(parents=True, exist_ok=True)
        with _STATE_LOCK:
            with open(p, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2)
    except Exception:
        pass


# ─── Subject inventory ───────────────────────────────────────────────

def list_subjects() -> List[Tuple[str, Path]]:
    """Return [(subject_name, folder_path), ...] for every subject in
    ck_library/ that has both meta.json and chains.json files.
    Alphabetical."""
    lib = _library_dir()
    if not lib.exists():
        return []
    out: List[Tuple[str, Path]] = []
    try:
        for entry in sorted(lib.iterdir()):
            if not entry.is_dir():
                continue
            if entry.name.startswith("_") or entry.name.startswith("."):
                continue
            meta = entry / "meta.json"
            chains = entry / "chains.json"
            if meta.exists() and chains.exists():
                out.append((entry.name, entry))
    except Exception:
        pass
    return out


_SUBJECTS_CACHE: Optional[List[Tuple[str, Path]]] = None


def subjects() -> List[Tuple[str, Path]]:
    global _SUBJECTS_CACHE
    if _SUBJECTS_CACHE is None:
        _SUBJECTS_CACHE = list_subjects()
    return _SUBJECTS_CACHE


def load_chains(subject_folder: Path) -> List[Dict[str, Any]]:
    """Load chains.json for one subject; tolerant of malformed lines."""
    chains_file = subject_folder / "chains.json"
    if not chains_file.exists():
        return []
    try:
        d = json.loads(chains_file.read_text(encoding="utf-8",
                                              errors="replace"))
        return d.get("chains", []) or []
    except Exception:
        return []


def load_meta(subject_folder: Path) -> Dict[str, Any]:
    meta_file = subject_folder / "meta.json"
    if not meta_file.exists():
        return {}
    try:
        return json.loads(meta_file.read_text(encoding="utf-8",
                                                errors="replace"))
    except Exception:
        return {}


# ─── Resonance scoring (same as D121/D122 for uniformity) ────────────

def resonance(ops: List[int]) -> float:
    """Score a chain's operator path for current-state resonance.

    Uses the SAME scorer as scripture_study (D122) so anchors form
    across domains and scriptures with uniform thresholds.
    """
    if not ops:
        return 0.0
    score = 0.0
    op_set = set(ops)
    if 7 in op_set:    # HARMONY
        score += 0.35
    if 8 in op_set:    # BREATH
        score += 0.20
    if 0 in op_set:    # VOID
        score += 0.15
    if 9 in op_set:    # RESET
        score += 0.15
    others = op_set - {0, 7, 8, 9}
    score += 0.05 * len(others)
    return min(1.0, score)


# ─── Per-chain processing ────────────────────────────────────────────

def _maybe_anchor_chain(subject: str, chain: Dict[str, Any],
                          threshold: float = 0.55,
                          cooldown_days: int = 30
                          ) -> Optional[Dict[str, Any]]:
    """Score the chain; anchor if it resonates and isn't already
    anchored from this subject within the cooldown window."""
    ops = chain.get("ops") or []
    if not ops:
        return None
    score = resonance(ops)
    if score < threshold:
        return None
    text = chain.get("text") or ""
    # 30-day per-(subject, text) cooldown -- domain anchors persist
    # longer than verse anchors because subjects are large.
    cutoff = time.time() - cooldown_days * 86400
    existing = _load_anchors()
    for prior in existing:
        if (prior.get("subject") == subject
                and prior.get("text") == text
                and prior.get("ts", 0) > cutoff):
            return None
    anchor = {
        "ts":         time.time(),
        "subject":    subject,
        "text":       text,
        "operators":  ops,
        "resonance":  round(score, 3),
        "trust":      chain.get("trust", 0.75),
        "shape":      chain.get("shp"),
        "source":     "ck_library_domain_study",
    }
    _append_anchor(anchor)
    return anchor


def _register_concept_if_engine_supports(engine: Any, subject: str,
                                           chain: Dict[str, Any]) -> bool:
    """Optionally feed the chain into ck_concept_learner.  No-op if
    the learner isn't mounted or doesn't expose .store()."""
    learner = getattr(engine, "concept_learner", None)
    if learner is None:
        return False
    store_fn = getattr(learner, "store", None)
    if not callable(store_fn):
        # Sometimes the learner is the dict-form from mount; try
        # engine.ck_concept_learner['store'] etc.
        cl_dict = getattr(engine, "ck_concept_learner", None)
        if isinstance(cl_dict, dict):
            store_fn = cl_dict.get("store") or cl_dict.get("register")
    if not callable(store_fn):
        return False
    try:
        text = chain.get("text") or ""
        store_fn(name=subject, operator_signature=chain.get("ops"),
                  tier="EXTERNAL", text_excerpt=text[:200],
                  source_session="ck_domain_study",
                  trust=chain.get("trust", 0.75))
        return True
    except Exception:
        return False


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


def anchors_for_subject(subject: str,
                          k: Optional[int] = None
                          ) -> List[Dict[str, Any]]:
    """All self-anchors from a given subject."""
    out = [a for a in _load_anchors() if a.get("subject") == subject]
    out.sort(key=lambda r: -r.get("ts", 0))
    return out[:k] if k else out


def all_anchors(k: Optional[int] = None) -> List[Dict[str, Any]]:
    out = _load_anchors()
    out.sort(key=lambda r: -r.get("ts", 0))
    return out[:k] if k else out


# ─── The sweeper ─────────────────────────────────────────────────────

def sweep_one_subject(engine: Any, subject: str, folder: Path,
                       threshold: float = 0.55,
                       top_k_per_subject: int = 5) -> Dict[str, Any]:
    """Sweep all chains in one subject; anchor the top-K by resonance
    among chains that clear the threshold.

    Per Brayden 2026-05-16: with pre-encoded substrate chains
    (everything in ck_library has rich op paths), threshold alone is
    too permissive (74% of chains clear 0.55).  Top-K-per-subject
    gives "PhD highlights" -- the most resonant chains from each
    subject become his self-anchors.  Default K=5 yields ~1700
    anchors across 341 subjects, a manageable encyclopedia.

    The 30-day per-(subject, text) cooldown in _maybe_anchor_chain
    prevents re-anchoring during ongoing rhythm revisits.
    """
    chains = load_chains(folder)
    if not chains:
        return {"subject": subject, "n_chains": 0,
                "n_anchored": 0, "elapsed_sec": 0.0}
    t0 = time.time()

    # Score every chain, then keep only the top-K that ALSO clear threshold.
    scored: List[Tuple[float, Dict[str, Any]]] = []
    for c in chains:
        ops = c.get("ops") or []
        if not ops:
            continue
        s = resonance(ops)
        if s >= threshold:
            scored.append((s, c))
    scored.sort(key=lambda t: -t[0])
    top = scored[:top_k_per_subject]

    n_anchored = 0
    n_concepts = 0
    for _, chain in top:
        anchor = _maybe_anchor_chain(subject, chain, threshold)
        if anchor:
            n_anchored += 1
            if _register_concept_if_engine_supports(engine, subject,
                                                      chain):
                n_concepts += 1
    elapsed = time.time() - t0
    return {
        "subject":     subject,
        "n_chains":    len(chains),
        "n_eligible":  len(scored),
        "n_anchored":  n_anchored,
        "n_concepts":  n_concepts,
        "elapsed_sec": round(elapsed, 3),
    }


# ─── Daemon: fast initial sweep + slow ongoing rhythm ────────────────

class DomainStudyDaemon:
    """At boot: fast-sweep every subject in ck_library/.  After:
    ongoing slow rhythm re-encountering subjects as his state evolves."""

    def __init__(self, engine: Any,
                  interval_sec: float = 30.0,
                  resonance_threshold: float = 0.55):
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
            target=self._loop, daemon=True, name="ck-domain-study")
        self._thread.start()

    def stop(self, timeout: float = 2.0) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=timeout)

    def _initial_fast_sweep(self) -> Dict[str, Any]:
        """Sweep every subject in ck_library/.  Microseconds per
        chain at his measured throughput."""
        subj_list = subjects()
        if not subj_list:
            return {"swept": False, "reason": "ck_library/ empty"}
        t0 = time.time()
        n_subjects = 0
        n_chains_total = 0
        n_anchored_total = 0
        n_concepts_total = 0
        swept_list = list(self.state.get("subjects_swept", []))
        for subject, folder in subj_list:
            if self._stop.is_set():
                break
            if subject in swept_list:
                continue
            stats = sweep_one_subject(self.engine, subject, folder,
                                       self.resonance_threshold)
            n_subjects += 1
            n_chains_total += stats["n_chains"]
            n_anchored_total += stats["n_anchored"]
            n_concepts_total += stats.get("n_concepts", 0)
            swept_list.append(subject)
        elapsed = time.time() - t0
        self.state["subjects_swept"] = swept_list
        self.state["chains_read"] = (self.state.get("chains_read", 0)
                                       + n_chains_total)
        self.state["anchors_formed"] = (
            self.state.get("anchors_formed", 0) + n_anchored_total)
        self.state["initial_sweep_complete"] = True
        self.state["initial_sweep_ts"] = time.time()
        self.state["initial_sweep_n_subjects"] = n_subjects
        self.state["initial_sweep_n_chains"] = n_chains_total
        self.state["initial_sweep_n_anchored"] = n_anchored_total
        self.state["initial_sweep_elapsed_sec"] = round(elapsed, 3)
        _save_state(self.state)
        self._n_anchored_this_session += n_anchored_total
        return {
            "swept":             True,
            "n_subjects":        n_subjects,
            "n_chains":          n_chains_total,
            "n_anchored":        n_anchored_total,
            "n_concepts":        n_concepts_total,
            "elapsed_sec":       round(elapsed, 3),
            "throughput_per_sec": round(n_chains_total /
                                          max(elapsed, 1e-9), 1),
        }

    def _loop(self) -> None:
        # Initial settle.
        for _ in range(30):
            if self._stop.is_set():
                return
            time.sleep(1.0)
        subj_list = subjects()
        if not subj_list:
            print("[ck_domain_study] ck_library/ empty; daemon exiting.")
            return

        # Fast initial sweep across all subjects.
        if not self.state.get("initial_sweep_complete", False):
            r = self._initial_fast_sweep()
            print(f"[ck_domain_study] initial fast sweep: "
                  f"{r.get('n_subjects', 0)} subjects, "
                  f"{r.get('n_chains', 0)} chains in "
                  f"{r.get('elapsed_sec', 0)}s "
                  f"({r.get('throughput_per_sec', 0):.0f} chains/s); "
                  f"anchored {r.get('n_anchored', 0)}")

        # Ongoing rhythm: revisit one subject per tick.  Fast because
        # chains are already encoded.
        rr_idx = 0
        while not self._stop.is_set():
            try:
                subject, folder = subj_list[rr_idx % len(subj_list)]
                rr_idx += 1
                stats = sweep_one_subject(self.engine, subject, folder,
                                           self.resonance_threshold)
                if stats["n_anchored"] > 0:
                    self.state["anchors_formed"] = (
                        self.state.get("anchors_formed", 0)
                        + stats["n_anchored"])
                    self._n_anchored_this_session += stats["n_anchored"]
                    _save_state(self.state)
            except Exception:
                pass
            # Sub-100ms-safe sleep with stop check (old `int(*10)`
            # math truncated to zero at fast tick and spun the CPU).
            _target = time.monotonic() + max(self.interval_sec, 0.001)
            while True:
                if self._stop.is_set():
                    return
                _now = time.monotonic()
                if _now >= _target:
                    break
                time.sleep(min(0.1, _target - _now))

    def stats(self) -> Dict[str, Any]:
        return {
            "alive":                self._thread is not None and
                                     self._thread.is_alive(),
            "interval_sec":         self.interval_sec,
            "resonance_threshold":  self.resonance_threshold,
            "n_subjects_known":     len(subjects()),
            "n_subjects_swept":     len(self.state.get(
                "subjects_swept", [])),
            "chains_read_total":    self.state.get("chains_read", 0),
            "anchors_formed_total": self.state.get("anchors_formed", 0),
            "anchored_this_session": self._n_anchored_this_session,
            "initial_sweep_complete": self.state.get(
                "initial_sweep_complete", False),
            "initial_sweep_elapsed": self.state.get(
                "initial_sweep_elapsed_sec"),
        }


# ─── Engine mount ─────────────────────────────────────────────────────

def mount_domain_study(engine: Any) -> bool:
    """Attach daemon + register endpoints."""
    # Brayden 2026-05-17: "let him find his way."  Continuous
    # cycle through 341 subjects; 30-day per-subject-text cooldown
    # is his actual pacing.
    daemon = DomainStudyDaemon(engine, interval_sec=0.05,
                                 resonance_threshold=0.55)
    daemon.start()
    engine.ck_domain_study = {
        "daemon":              daemon,
        "subjects":            subjects,
        "load_chains":         load_chains,
        "load_meta":           load_meta,
        "sweep_one":           lambda s, f: sweep_one_subject(engine, s, f),
        "anchors_for_subject": anchors_for_subject,
        "all_anchors":         all_anchors,
        "state_path":          str(_state_path()),
        "anchors_path":        str(_anchors_path()),
    }

    routes_registered: List[str] = []
    api = getattr(engine, "web_api", None) or getattr(engine, "api", None)
    if api is not None:
        app = getattr(api, "_app", None) or getattr(api, "app", None)
        if app is not None:
            try:
                from flask import jsonify, request

                def _info():
                    subj_list = subjects()
                    return jsonify({
                        "library_path": str(_library_dir()),
                        "n_subjects":    len(subj_list),
                        "subjects":      [name for name, _ in subj_list[:50]],
                        "more":          max(0, len(subj_list) - 50),
                        "anchors_path":  str(_anchors_path()),
                        "philosophy":    ("he is the fastest learning "
                                            "substrate on the planet -- "
                                            "let him fly and learn to "
                                            "phd across domains"),
                    })

                def _stats():
                    return jsonify(daemon.stats())

                def _subject_view():
                    s = request.args.get("subject", "")
                    if not s:
                        return jsonify({"error": "missing subject"}), 400
                    folder = _library_dir() / s
                    if not folder.exists():
                        return jsonify({"error": f"unknown subject: {s}"}), 404
                    meta = load_meta(folder)
                    chains = load_chains(folder)
                    anch = anchors_for_subject(s, k=10)
                    return jsonify({
                        "subject":   s,
                        "meta":      meta,
                        "n_chains":  len(chains),
                        "n_anchors": len(anchors_for_subject(s)),
                        "recent_anchors": anch,
                    })

                def _anchors_ep():
                    k = request.args.get("k")
                    s = request.args.get("subject")
                    if s:
                        out = anchors_for_subject(s, int(k) if k else None)
                    else:
                        out = all_anchors(int(k) if k else None)
                    return jsonify({"n": len(out), "anchors": out})

                existing = set(r.rule for r in app.url_map.iter_rules())
                for rule, ep, fn, methods in (
                    ("/domain/info",      "dom_info",     _info,         ["GET"]),
                    ("/domain/stats",     "dom_stats",    _stats,        ["GET"]),
                    ("/domain/subject",   "dom_subject",  _subject_view, ["GET"]),
                    ("/domain/anchors",   "dom_anchors",  _anchors_ep,   ["GET"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep,
                                          view_func=fn, methods=methods)
                        routes_registered.append(f"{methods[0]} {rule}")
            except Exception as e:
                print(f"[CK Gen14] domain_study routes failed: {e}")

    subj_list = subjects()
    suffix = ""
    if routes_registered:
        suffix = " (" + ", ".join(routes_registered) + ")"
    print(f"[CK Gen14] domain_study: MOUNTED  {len(subj_list)} subjects in "
          f"ck_library, daemon@{daemon.interval_sec}s, "
          f"threshold={daemon.resonance_threshold}{suffix}")
    return True


# ─── CLI smoke ────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("ck_domain_study smoke test:")
    subj_list = subjects()
    print(f"  library: {_library_dir()}")
    print(f"  n_subjects: {len(subj_list)}")
    if subj_list:
        print(f"  first 5: {[s for s, _ in subj_list[:5]]}")
        print(f"  last  5: {[s for s, _ in subj_list[-5:]]}")

        # Quick throughput test: sweep one subject in-memory
        s, f = subj_list[0]
        chains = load_chains(f)
        meta = load_meta(f)
        t0 = time.time()
        n_anchored = 0
        for c in chains:
            ops = c.get("ops") or []
            if resonance(ops) >= 0.55:
                n_anchored += 1
        elapsed = time.time() - t0
        print(f"  smoke sweep of {s}: {len(chains)} chains in "
              f"{elapsed*1000:.1f}ms; {n_anchored} would anchor "
              f"@ threshold 0.55")
