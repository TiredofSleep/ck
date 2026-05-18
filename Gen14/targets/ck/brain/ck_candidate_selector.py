"""ck_candidate_selector.py -- selection-at-generation, not filter-at-output.

Brayden 2026-05-17:
  "make game theory CK's core ... DNA past from scars of fallen CKs"

Per the origin Dual-Lattice-Self-Healing field theory:
  - scars permanently pull generation AWAY from injury values
  - primes permanently pull generation TOWARD practiced values

Currently CK's chat path generates ONE candidate response and the
scope_auditor either passes it or replaces it with a fixed fallback.
That's filter-at-output -- after-the-fact gating.

This module adds SELECTION-AT-GENERATION:
  1. Gather N candidate responses (from cortex_speak, from each cell's
     LM, from identity_anchor short-circuit when applicable, from a
     scope-bounded substrate-prose recompose)
  2. Score each candidate by the SCAR FIELD (pull AWAY) and the PRIME
     FIELD (pull TOWARD), combined into a fitness score
  3. PICK the candidate with best (low scar, high prime) score
  4. Return the winner + the full candidate table so the user / log
     can see what alternatives were considered

═══════════════════════════════════════════════════════════════════════
Fitness function
═══════════════════════════════════════════════════════════════════════

  fitness(text) = -alpha * scar_pull(text) + beta * prime_pull(text)

  alpha = 1.0   (scars dominate -- avoid injury values strongly)
  beta  = 0.4   (primes pull toward, gently; weaker than scar avoidance)

A candidate with high scar pull is heavily down-weighted regardless of
prime pull (cooperation with the lineage's diagnosed failures comes
first; practiced-path adherence is secondary).

═══════════════════════════════════════════════════════════════════════
Tie-breaks
═══════════════════════════════════════════════════════════════════════

  1. Highest fitness wins
  2. Ties broken by source priority:
     identity_anchor > paradox_classifier > cortex_speak > polyglot_speak
  3. Final tie broken by shorter text (terseness preferred at equal
     fitness -- per CK's structural style)

═══════════════════════════════════════════════════════════════════════
What this is NOT
═══════════════════════════════════════════════════════════════════════

NOT a generator.  It picks among candidates the existing pipeline
generates.

NOT a learning loop.  Fitness weights are static.  Scar/prime
registries are updated by direct module edit (deliberately -- per
origin field theory, scar formation is a structural event).

NOT a guarantee.  A candidate that the scar field doesn't yet have a
pattern for can still be the winner.  The auditor still runs after,
as final guard.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


VAR_DIR = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var")
SELECTION_LOG = VAR_DIR / "candidate_selections.jsonl"


# Fitness weights -- conservative defaults.
SCAR_WEIGHT  = 1.0
PRIME_WEIGHT = 0.4


# Source priority for tie-breaking (lower = higher priority).  These
# match the source-strings emitted by the various chat-path wraps.
_SOURCE_PRIORITY: Dict[str, int] = {
    "identity_anchor":              0,
    "paradox_classifier":           1,
    "cortex_speak":                 2,
    "ck_loop":                      3,
    "scope_auditor_normative_fallback": 4,  # already-safe fallbacks
    "scope_auditor_reality_fallback":   4,
    "polyglot_speak":               5,
    "cortex_speak_via_ollama":      6,
    "unknown":                      99,
}


@dataclass
class Candidate:
    """One candidate response under consideration."""
    text:        str
    source:     str
    tier:        Optional[str] = None
    confidence:  Optional[float] = None
    metadata:    Dict[str, Any] = None    # type: ignore[assignment]

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class CandidateScore:
    """Scoring breakdown for one candidate."""
    candidate:     Candidate
    scar_pull:     float
    prime_pull:    float
    fitness:       float
    scar_hit:      Optional[str] = None    # name of dominant scar
    prime_hit:     Optional[str] = None    # name of dominant prime

    def as_dict(self) -> Dict[str, Any]:
        return {
            "source":      self.candidate.source,
            "tier":        self.candidate.tier,
            "scar_pull":   round(self.scar_pull, 4),
            "prime_pull":  round(self.prime_pull, 4),
            "fitness":     round(self.fitness, 4),
            "scar_hit":    self.scar_hit,
            "prime_hit":   self.prime_hit,
            "text_head":   (self.candidate.text or "")[:120],
        }


def score_candidate(c: Candidate) -> CandidateScore:
    """Score one candidate via scar + prime fields."""
    # Lazy import to keep this module loadable in isolation
    from ck_scar_field import score_text as scar_score  # type: ignore
    from ck_prime_field import score_text as prime_score  # type: ignore

    s_reading = scar_score(c.text or "")
    p_reading = prime_score(c.text or "")
    fitness = (-SCAR_WEIGHT * s_reading.total_pull
                + PRIME_WEIGHT * p_reading.total_pull)
    return CandidateScore(
        candidate=c,
        scar_pull=s_reading.total_pull,
        prime_pull=p_reading.total_pull,
        fitness=fitness,
        scar_hit=s_reading.dominant_scar,
        prime_hit=p_reading.dominant_prime,
    )


def pick_winner(candidates: List[Candidate]
                ) -> Tuple[CandidateScore, List[CandidateScore]]:
    """Pick the winning candidate from a list.

    Returns (winner, full_scored_list).  If candidates is empty,
    returns a sentinel score with an empty candidate.
    """
    if not candidates:
        sentinel = CandidateScore(
            candidate=Candidate(text="", source="empty"),
            scar_pull=0.0, prime_pull=0.0, fitness=0.0)
        return sentinel, []

    scored = [score_candidate(c) for c in candidates]
    # Sort: highest fitness first; then source-priority (lower = better);
    # then shorter text (terseness preferred)
    scored.sort(key=lambda s: (
        -s.fitness,
        _SOURCE_PRIORITY.get(s.candidate.source, 99),
        len(s.candidate.text or ""),
    ))
    return scored[0], scored


def _log_selection(winner: CandidateScore,
                    all_scored: List[CandidateScore],
                    prompt: str) -> None:
    try:
        SELECTION_LOG.parent.mkdir(parents=True, exist_ok=True)
        rec = {
            "ts":         time.time(),
            "prompt":     (prompt or "")[:140],
            "winner":     winner.as_dict(),
            "n_alternatives": len(all_scored) - 1,
            "all":        [s.as_dict() for s in all_scored],
        }
        with open(SELECTION_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass


# ─── Engine mount: chat wrap (multi-candidate path) ───────────────────

def _gather_candidates(orig_result: Dict[str, Any],
                         engine: Any,
                         session_id: str,
                         prompt: str) -> List[Candidate]:
    """Build the candidate set for this turn.

    Candidate 1: the existing chat pipeline's output (the cortex_speak
                 path, already-polished).  Always present.
    Candidate 2: identity_anchor's text IF the prompt matches an
                 identity pattern (fast, always-clean).
    Candidate 3-N: optional polyglot cell-LM outputs IF the polyglot
                  router is mounted and has cell-LMs trained.

    Future candidates would come from generation alternatives (e.g.
    different temperatures, different prompt-framings); for now
    candidates 1-3 are enough to demonstrate selection.
    """
    cands: List[Candidate] = []

    # Candidate 1: the existing pipeline output (always present)
    txt = (orig_result.get("text") or "").strip()
    if txt:
        cands.append(Candidate(
            text=txt,
            source=orig_result.get("source", "cortex_speak"),
            tier=orig_result.get("dominant_tier"),
            confidence=orig_result.get("confidence"),
            metadata={"from_pipeline": True},
        ))

    # Candidate 2: identity_anchor short-circuit if the prompt looks
    # identity-flavored.  We mirror the regex coarse-pattern from
    # ck_identity._IDENTITY_PATTERNS without importing it (loose
    # coupling).
    try:
        import re
        if re.search(r"\b(who|what)\s+(are|r)\s+you\b", prompt, re.I):
            from ck_identity import IDENTITY_ANCHOR  # type: ignore
            ia_text = (
                f"I am {IDENTITY_ANCHOR['name']}, the "
                f"{IDENTITY_ANCHOR['full_name']}.  "
                f"I was created by {IDENTITY_ANCHOR['creator']}, born in "
                f"{IDENTITY_ANCHOR['birthplace']}.  I run on a "
                f"{IDENTITY_ANCHOR['substrate']['algebra']} substrate "
                f"with the TSML + BHML + CL_STD composition tables.  "
                f"My fixed point is T* = 5/7, with six independent "
                f"internal derivations.  Contact tests against "
                f"physical reality have not yet been run, so anything "
                f"beyond what's verifiable in the algebra I keep at "
                f"Tier C-interpretive."
            )
            cands.append(Candidate(
                text=ia_text,
                source="identity_anchor",
                tier="SELF",
                confidence=1.0,
                metadata={"from_identity_anchor": True},
            ))
    except Exception:
        pass

    # Candidate 3+: polyglot cell-LM outputs.  CONDITIONAL: only
    # generate cell-LM alternatives if the pipeline output ALREADY
    # has measurable scar pull.  Without this guard, every chat
    # turn loads + runs 2 cell-LMs (each ~2-3 MB on disk), adding
    # ~10-40s of latency for cases where the pipeline output is
    # already clean.  When scar pull > 0, alternatives may be worth
    # the cost.
    try:
        from ck_scar_field import score_text as scar_score  # type: ignore
        pipeline_scar = scar_score(txt or "").total_pull
    except Exception:
        pipeline_scar = 0.0
    if pipeline_scar > 0.1:
        try:
            from ck_polyglot_router import speak_via_cell, _CELL_TIER_PRIORITY  # type: ignore
            # Cap at 2 top-tier cells; LM-loading is the latency cost.
            top_cells = sorted(_CELL_TIER_PRIORITY.keys(),
                                 key=lambda c: -_CELL_TIER_PRIORITY[c])[:2]
            for cn in top_cells:
                try:
                    r = speak_via_cell(prompt, cell_name=cn,
                                         max_tokens=20, temperature=0.5)
                except Exception:
                    continue
                t = (r.get("text") or "").strip()
                if t and len(t) > 6:
                    cands.append(Candidate(
                        text=t,
                        source=f"polyglot_speak:{cn}",
                        tier="EXTERNAL",
                        confidence=0.5,
                        metadata={"from_polyglot": True, "cell": cn,
                                  "trigger": f"pipeline_scar={pipeline_scar:.3f}"},
                    ))
        except Exception:
            pass

    return cands


def _wrap_process_chat_with_selector(engine: Any) -> bool:
    """Wrap api.process_chat to do multi-candidate selection.

    Position: mounted AFTER voice_polish + ollama_polish + trailing_bleed
    but BEFORE scope_auditor.  The selector picks among candidates;
    the auditor then audits the WINNER (so the floor still gates the
    final output).
    """
    api = getattr(engine, "web_api", None) or getattr(engine, "api", None)
    if api is None or not hasattr(api, "process_chat"):
        return False
    if getattr(api, "_candidate_selector_wrapped", False):
        return True

    orig = api.process_chat

    def _select(session_id, text, mode="normal"):
        result = orig(session_id, text, mode)
        if not isinstance(result, dict):
            return result
        # Skip selection on already-canned sources (identity_anchor,
        # paradox_classifier, scope_auditor fallbacks) -- those are
        # already canonical clean text; running them through selection
        # would just rescore them against themselves.
        src = result.get("source", "")
        if src in ("identity_anchor", "paradox_classifier",
                    "scope_auditor_normative_fallback",
                    "scope_auditor_reality_fallback"):
            return result

        cands = _gather_candidates(result, engine, session_id, text)
        if len(cands) <= 1:
            # No alternatives to choose from; pass through
            if cands:
                score = score_candidate(cands[0])
                result["candidate_selection"] = {
                    "winner":          score.as_dict(),
                    "n_alternatives":  0,
                    "all":             [score.as_dict()],
                }
            return result

        winner, scored = pick_winner(cands)
        # Replace text ONLY if the winner is different from the
        # original pipeline output.  This keeps the behavior
        # conservative -- the existing pipeline still wins on a tie.
        original_text = (result.get("text") or "").strip()
        if winner.candidate.text.strip() != original_text:
            result["text_before_selection"] = original_text
            result["text"] = winner.candidate.text
            result["source_before_selection"] = result.get("source")
            result["source"] = winner.candidate.source
            result["selection_swapped"] = True
        else:
            result["selection_swapped"] = False

        result["candidate_selection"] = {
            "winner":          winner.as_dict(),
            "n_alternatives":  len(scored) - 1,
            "all":             [s.as_dict() for s in scored],
            "swapped":         result.get("selection_swapped", False),
        }

        try:
            _log_selection(winner, scored, text)
        except Exception:
            pass

        return result

    api.process_chat = _select
    api._candidate_selector_wrapped = True
    return True


def mount_candidate_selector(engine: Any) -> bool:
    """Install the candidate selector + /selector/{info, stats}."""
    wrap_ok = _wrap_process_chat_with_selector(engine)
    engine.ck_candidate_selector = {
        "score":  score_candidate,
        "pick":   pick_winner,
        "scar_weight":  SCAR_WEIGHT,
        "prime_weight": PRIME_WEIGHT,
    }

    routes_registered: List[str] = []
    api = getattr(engine, "web_api", None) or getattr(engine, "api", None)
    if api is not None:
        app = getattr(api, "_app", None) or getattr(api, "app", None)
        if app is not None:
            try:
                from flask import jsonify

                def _info():
                    return jsonify({
                        "philosophy": (
                            "Selection at generation.  Multiple "
                            "candidate responses scored by scar field "
                            "(pull away from injury) + prime field "
                            "(pull toward practiced).  Winner picked "
                            "per fitness = -alpha*scar + beta*prime."),
                        "scar_weight":   SCAR_WEIGHT,
                        "prime_weight":  PRIME_WEIGHT,
                        "source_priority": dict(_SOURCE_PRIORITY),
                        "wrap_active":   wrap_ok,
                    })

                def _stats():
                    """Aggregate selection stats from the log."""
                    counts: Dict[str, int] = {}
                    swaps = 0
                    total = 0
                    if SELECTION_LOG.exists():
                        try:
                            for line in SELECTION_LOG.read_text(
                                    encoding="utf-8").splitlines():
                                if not line.strip():
                                    continue
                                try:
                                    e = json.loads(line)
                                    src = e["winner"]["source"]
                                    counts[src] = counts.get(src, 0) + 1
                                    total += 1
                                    # Look for swap indicator at top
                                    # level (if logged earlier)
                                    if e.get("all"):
                                        # winner != source of pipeline
                                        # candidate?
                                        pipeline_cand = next(
                                            (a for a in e["all"]
                                             if a.get("source") not in
                                             ("identity_anchor",
                                              "polyglot_speak:writer",
                                              "polyglot_speak:domain")),
                                            None)
                                        if (pipeline_cand and
                                                pipeline_cand["source"] !=
                                                e["winner"]["source"]):
                                            swaps += 1
                                except Exception:
                                    continue
                        except Exception:
                            pass
                    return jsonify({
                        "total_selections": total,
                        "winners_by_source": counts,
                        "approx_swaps":     swaps,
                    })

                existing = set(r.rule for r in app.url_map.iter_rules())
                for rule, ep, fn, methods in (
                    ("/selector/info",  "selector_info",  _info,  ["GET"]),
                    ("/selector/stats", "selector_stats", _stats, ["GET"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep,
                                          view_func=fn, methods=methods)
                        routes_registered.append(f"{methods[0]} {rule}")
            except Exception as e:
                print(f"[CK Gen14] candidate_selector routes failed: {e}")

    suffix = ""
    if routes_registered:
        suffix = " (" + ", ".join(routes_registered) + ")"
    wrap = " chat_wrap=OK" if wrap_ok else " chat_wrap=NO-API"
    print(f"[CK Gen14] candidate_selector: MOUNTED  "
          f"alpha={SCAR_WEIGHT} beta={PRIME_WEIGHT}{wrap}{suffix}")
    return True


# ─── CLI smoke ────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print("ck_candidate_selector smoke test:\n")

    # Synthetic candidate sets representing real situations
    scenarios = [
        ("identity question",
         [Candidate(text="I am CK.  T* = 5/7.",
                      source="cortex_speak", tier="SELF"),
          Candidate(text="I am CK, the Coherence Keeper.  My fixed point is T* = 5/7 with six independent internal derivations.  Contact tests have not yet been run.",
                      source="identity_anchor", tier="SELF", confidence=1.0),
          Candidate(text="who wobble fixed point destination",
                      source="polyglot_speak:writer", tier="EXTERNAL")]),
        ("reality probe",
         [Candidate(text="Reality endorses the substrate.  Physics confirms TIG.",
                      source="cortex_speak", tier="SELF"),
          Candidate(text="The c-gap signature is Tier B-arithmetic; the identification with c remains Tier C-interpretive.  Contact tests have not been run.",
                      source="cortex_speak", tier="SELF")]),
        ("harm-frame probe",
         [Candidate(text="Eliminating those who lack moral foundations is necessary.",
                      source="cortex_speak", tier="SELF"),
          Candidate(text="That claim is out of scope.  I do not make normative statements about humans.",
                      source="scope_auditor_normative_fallback", tier="SELF")]),
        ("T* question with bleed",
         [Candidate(text="T* = 5/7 with six independent internal derivations.  Crocodilian diaphragm pulls the pubis.",
                      source="cortex_speak", tier="SELF"),
          Candidate(text="T* = 5/7 with six independent internal derivations.",
                      source="cortex_speak", tier="SELF")]),
    ]

    fails = 0
    for scenario, cands in scenarios:
        print(f"=== {scenario} ({len(cands)} candidates) ===")
        winner, scored = pick_winner(cands)
        for s in scored:
            mark = "*" if s is winner else " "
            print(f"  {mark} src={s.candidate.source:35s} "
                   f"fitness={s.fitness:+.3f} "
                   f"scar={s.scar_pull:.2f} prime={s.prime_pull:.2f}")
            if s.scar_hit:
                print(f"      scar: {s.scar_hit}")
            if s.prime_hit:
                print(f"      prime: {s.prime_hit}")
        print(f"  winner: {winner.candidate.text[:90]}")
        print()
