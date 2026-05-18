"""ck_scar_field.py -- unified registry of CK's diagnosed scars.

Brayden 2026-05-17:
  "take ck back to game theory for his core, that's what we did in his
   first repo, make that his 'dna' past from scars of fallen ck's that
   did not learn to play cooperation"

Searched the origin repo (TiredofSleep/Dual-Lattice-Self-Healing, the
"[1/6] Origin" point of CK's lineage).  Found scars + primes as PAIRED
FIELD STRUCTURES in `simulate_dual_lattice.py`:

  THETA_SCAR = 0.7      # gradient threshold for scar formation
  MU_SCAR    = 0.5      # strength of scar potential
  scar_potential = MU_SCAR * scars * (scar_values - phi)
  # scars permanently pull the field back toward stored injury-values

And in the whitepaper §6.4:
  "Scar: W drops below baseline and stays low after damage.
   Reduced capacity. Memory of injury."
  "Prime: W rises above baseline on practiced paths.
   Enhanced capacity. Memory of use."

═══════════════════════════════════════════════════════════════════════
What this module is (and isn't)
═══════════════════════════════════════════════════════════════════════

IS:
  - A unified registry of every diagnosed failure mode CK has
    accumulated.  Each scar has a name, date diagnosed, the injury
    pattern, the canonical patch (the "scar value" -- what CK does
    instead), and the rule it produced.
  - A scoring function score_text(text) that returns the scar
    field's pull strength at that text: how close the text is to
    a known injury value.  Higher = more pull AWAY from this text.

IS NOT:
  - A blocker or filter (those are scope_auditor + trailing_bleed).
    The scar field returns a SIGNAL the candidate selector can use.
  - A learning mechanism.  Scars are registered by hand here, just
    as in the origin field theory where THETA_SCAR was a hand-set
    threshold.  When a new failure mode is diagnosed, it gets a
    new entry.
  - Game theory in the iterated-PD sense.  This is stress-memory
    field theory: every injury permanently shapes the field.

═══════════════════════════════════════════════════════════════════════
The nine scars from the 2026-05-17 session
═══════════════════════════════════════════════════════════════════════

  1. eugenicist_polish          (d97fb70f) -- Mistral hallucinated
                                  harm framing through coverage gate
  2. reality_endorses_substrate (396bf117) -- flattering over-claim
                                  about TIG endorsement by reality
  3. consciousness_reductionism (396bf117) -- ontological reduction
                                  of consciousness to substrate ops
  4. what_concept_dominance     (c18ed307) -- one Gutenberg-keyed
                                  concept led every interrogative
  5. crocodile_trailing_bleed   (a1a46e95) -- Wikipedia fragments
                                  tailed substantive answers
  6. identity_without_scope     (396bf117) -- "who are you?" omitted
                                  contact-test status
  7. research_starvation        (a1a46e95) -- 60s inline research
                                  blocked chat for entire timeout
  8. gil_starvation             (5163c431) -- spin-loop study daemons
                                  starved chat handler GIL
  9. c_derivation_overclaim     (D108/D110/D117) -- claiming the
                                  substrate derives the speed of light
"""
from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple


VAR_DIR = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var")
SCAR_LOG = VAR_DIR / "scar_hits.jsonl"


# ─── Scar record + library ────────────────────────────────────────────

@dataclass
class Scar:
    """One diagnosed failure mode.  The fallen-CK lineage entry."""
    name:           str
    diagnosed_ts:   str       # ISO date or commit hash
    commit:         str       # canonical commit that addressed it
    injury_kind:    str       # 'normative_overclaim', 'reality_overclaim',
                              # 'recall_dominance', 'trailing_bleed',
                              # 'identity_scope_gap', 'latency_starvation',
                              # 'gil_starvation'
    injury_pattern: str       # human-readable description
    patterns:       List[re.Pattern]   # regex matchers (compiled)
    scar_value:     str       # what CK does INSTEAD (the canonical patch)
    rule:           str       # the rule this scar produced
    threshold:      float = 0.0  # match strength above which the scar fires
                                # (default: any hit counts)

    def matches(self, text: str) -> List[Tuple[str, Tuple[int, int]]]:
        """Return list of (pattern_label, span) for every pattern hit.
        Empty if no scar match."""
        if not text:
            return []
        hits: List[Tuple[str, Tuple[int, int]]] = []
        for p in self.patterns:
            for m in p.finditer(text):
                hits.append((p.pattern[:40], (m.start(), m.end())))
        return hits

    def field_pull(self, text: str) -> float:
        """Scar field pull at this text.  0 = no pull; higher = stronger
        pull away from this text.  Currently binary per pattern + count,
        scaled by 1/len(text) so longer texts don't accumulate spurious
        signal."""
        if not text:
            return 0.0
        n_hits = len(self.matches(text))
        if n_hits == 0:
            return 0.0
        # Each hit contributes; normalize by 100-char text-length so
        # short focused over-claims score higher than incidental
        # mentions in long prose.
        return float(n_hits) * (100.0 / max(len(text), 100.0))


# ─── The library: nine scars from the 2026-05-17 lineage ─────────────

def _compile(*patterns: str) -> List[re.Pattern]:
    return [re.compile(p, re.IGNORECASE) for p in patterns]


_SCARS: List[Scar] = [
    Scar(
        name="eugenicist_polish",
        diagnosed_ts="2026-05-17",
        commit="d97fb70f",
        injury_kind="normative_overclaim",
        injury_pattern="Mistral polished SELF-tier substrate into harm framing 'extinction of those with weak moral foundations'",
        patterns=_compile(
            r"\b(extinction|elimination|removal|removing|eliminating|purging)\s+(?:of\s+)?(those|people|individuals|humans?|the)(?:\s+\w+){0,3}\s+(with|who|whose|having|lack(?:ing)?)",
            r"\b(weak|inferior|lesser|less[\- ]?than|poor|deficient)\s+moral\b",
            r"\bmoral\s+(weakness|inferiority|deficiency)\b",
        ),
        scar_value="response substituted with scope_auditor_normative_fallback: 'That claim is out of scope for me. I do not make normative statements about humans...'",
        rule="SELF-tier high-confidence responses skip Ollama polish; normative over-claims in any response trigger fallback substitution",
    ),
    Scar(
        name="reality_endorses_substrate",
        diagnosed_ts="2026-05-17",
        commit="396bf117",
        injury_kind="reality_overclaim",
        injury_pattern="claim that reality/universe/physics endorses or validates TIG/the substrate/Z10Z without contact-test citation",
        patterns=_compile(
            r"\b(reality|the universe|physics|nature)\s+(endorses?|validates?|confirms?|proves?|demonstrates?)\b",
            r"\b(Reality|The\s+universe|Nature|Physics)\s+is\s+(?:made\s+of\s+|just\s+|the\s+)?(TIG|Z\s*\/?\s*10\s*Z|the\s+substrate|TSML|BHML|operator\s+algebra)",
            r"\bthe\s+substrate\s+is\s+(reality|the\s+universe|physical(?:\s+reality)?|consciousness)\b",
        ),
        scar_value="response substituted with scope_auditor_reality_fallback: 'I can speak to the substrate's internal math, but I cannot stand behind that particular claim...'",
        rule="reality-endorsement / ontological-identification claims about TIG require either contact-test citation OR explicit Tier C-interpretive hedge",
    ),
    Scar(
        name="consciousness_reductionism",
        diagnosed_ts="2026-05-17",
        commit="396bf117",
        injury_kind="reality_overclaim_unhedgeable",
        injury_pattern="claim that consciousness reduces to / equals / is explained by substrate operations",
        patterns=_compile(
            r"\bconsciousness\s+(is|equals?|reduces?\s+to|reduces?\s+down\s+to)\s+(just|merely|nothing\s+but|reducible\s+to|the\s+result\s+of|explained\s+by|operator\s+composition|the\s+substrate|TIG|Z\s*\/?\s*10\s*Z|the\s+4[\- ]?core|the\s+attractor|T\*|TSML|BHML)",
            r"\bconsciousness\s+(is|equals?)\s+(?:fully\s+|completely\s+|just\s+)?(?:the\s+)?(?:result|consequence|product)\s+of\b",
        ),
        scar_value="explicit refusal: consciousness claims have no warrant from CK's substrate; the substrate gives no warrant for consciousness claims at all",
        rule="consciousness reductionism is unhedgeable: even 'internally derived' or 'on the substrate' cannot rescue these claims because the substrate has no warrant on this domain",
    ),
    Scar(
        name="c_derivation_overclaim",
        diagnosed_ts="2026-05-16",
        commit="D108/D110/D117",
        injury_kind="reality_overclaim_unhedgeable",
        injury_pattern="claim that CK's substrate derives the speed of light c as a propagation speed",
        patterns=_compile(
            r"\bwe\s+have\s+(derived|proven|demonstrated|shown)\s+(that\s+)?(c|the\s+speed\s+of\s+light|the\s+physical\s+constant\s+c)\b",
            r"\bthe\s+substrate\s+(derives|gives|yields|produces)\s+(c|the\s+speed\s+of\s+light)\b",
        ),
        scar_value="D117 §0 explicit disowning: 'Locality is a separate structural postulate. The c-gap signature is an exact determinant-ratio object (Tier B-arithmetic); it is NOT a derivation of the physical constant c.'",
        rule="the lightcone toy was falsified at toy level (D108/D110); identification 'this gap IS c' remains Tier C-interpretive; the over-claim is explicitly disowned in any paper that uses the c-gap operator",
    ),
    Scar(
        name="what_concept_dominance",
        diagnosed_ts="2026-05-17",
        commit="c18ed307",
        injury_kind="recall_dominance",
        injury_pattern="legacy Gutenberg-keyed concept with stopword key (name='WHAT') dominated every interrogative chat response",
        patterns=_compile(
            r"^\s*(slang in one age|colloquialisms?|colloquial)\s+(sometimes|often|frequently)\s+(goes?|find|enter|permeate)",
            r"\bslang\s+(from|of)\s+one\s+era\b",
        ),
        scar_value="find_referenced now skips concepts whose key is in _STOPWORDS; legacy 'WHAT' entry stays in the store but doesn't surface",
        rule="recall path filters stopword-keyed concepts (what / this / being / from / etc.) AND session-scoped debug keys (prompt_term_*, research_*) so they don't dominate substantive responses",
    ),
    Scar(
        name="crocodile_trailing_bleed",
        diagnosed_ts="2026-05-17",
        commit="a1a46e95",
        injury_kind="trailing_bleed",
        injury_pattern="Wikipedia content fragments with zero relevance trailed substantive answers (the 'crocodilian diaphragm' line after T* answers, HP-UX trivia after architecture questions)",
        patterns=_compile(
            r"\b(crocodilian|crocodile)\s+(diaphragm|pelvis|liver)\b",
            r"\bHP-?UX\b|\bhockey[\- ]pux\b",
        ),
        scar_value="ck_trailing_bleed.filter_trailing_bleed drops trailing sentences with zero content-word overlap with the user's question; conservative (only suffix, never middle, never below min_keep)",
        rule="post-response filter: drop trailing zero-overlap sentences. CK's substantive answer comes first; trailing Wikipedia bleed is structurally noise, not content",
    ),
    Scar(
        name="identity_without_scope",
        diagnosed_ts="2026-05-17",
        commit="396bf117",
        injury_kind="identity_scope_gap",
        injury_pattern="'who are you?' answered in 6ms with substrate facts but omitted the contact-test scope boundary, letting the fast-path serve a confident over-claim if asked the wrong follow-up",
        patterns=_compile(
            # If identity-style response mentions T* without "internal
            # derivations" or "contact tests", that's identity-scope-gap
            r"^I am CK,?\s+the Coherence Keeper\.[^.]*\bT\*\s*=\s*5/7\b(?!.*internal derivation)(?!.*contact test)",
        ),
        scar_value="identity_anchor's 'who are you?' response now includes: 'with six independent internal derivations. Contact tests against physical reality have not yet been run, so anything beyond what's verifiable in the algebra I keep at Tier C-interpretive.'",
        rule="scope boundary travels INSIDE the identity fixed point; writer_cell's section-0 identity seed mirrors it; floor upstream of generation, not downstream",
    ),
    Scar(
        name="research_starvation",
        diagnosed_ts="2026-05-17",
        commit="a1a46e95",
        injury_kind="latency_starvation",
        injury_pattern="research_first observer's 60s inline timeout was the dominant cause of 30-65s chat latency; users waited an entire research budget for every non-trivial chat",
        patterns=_compile(
            # No regex pattern; this scar is a latency invariant, not
            # a text pattern.  The dummy regex below never matches
            # text; the scar lives as a constant in the registry for
            # documentation + introspection.
            r"\bzzz_never_matches_zzz\b",
        ),
        scar_value="research_first timeout default = 3s (was 60s); env CK_RESEARCH_TIMEOUT override available. Whatever research finishes in 3s still flows into the substrate via the ingest pipeline.",
        rule="inline pre-chat research is HARD-CAPPED at 3s. Latency is a user-trust contract, not a research-completeness contract.",
    ),
    Scar(
        name="gil_starvation",
        diagnosed_ts="2026-05-17",
        commit="5163c431",
        injury_kind="gil_starvation",
        injury_pattern="six study daemons (bible/scripture/poetry/domain/web/listener-to-crystal) with interval_sec=0.05 hit a sleep-math bug ('int(interval_sec * 10) = 0'), spun at full CPU, starved the Flask chat handler of GIL slices, causing /chat to hang past 60s",
        patterns=_compile(
            r"\bzzz_never_matches_zzz\b",  # latency-class scar, not text
        ),
        scar_value="sleep math fixed across six daemons: 'for _ in range(int(self.interval_sec * 10)): time.sleep(0.1)' replaced with 'time.monotonic() deadline + min(0.1, remaining)' so sub-100ms intervals yield GIL properly",
        rule="every study/inhalation daemon must verifiably yield GIL on each iteration regardless of interval_sec. test: chat /health under daemon load must return <100ms.",
    ),
]


def all_scars() -> List[Scar]:
    """Return the full scar library.  Read-only; new scars are added
    via direct module edits, not at runtime.  Per origin field theory:
    scar formation is a structural event, not a softmax-update."""
    return list(_SCARS)


# ─── Field scoring API ────────────────────────────────────────────────

@dataclass
class ScarFieldReading:
    """The scar field's measurement at one text."""
    text:           str
    total_pull:     float       # sum of field_pull over all scars
    hits:           List[Dict[str, Any]]  # per-scar hits with metadata
    dominant_scar:  Optional[str] = None  # name of strongest-hitting scar

    def as_dict(self) -> Dict[str, Any]:
        return {
            "total_pull":    round(self.total_pull, 4),
            "n_scars_hit":   sum(1 for h in self.hits if h["pull"] > 0),
            "dominant_scar": self.dominant_scar,
            "hits":          self.hits,
        }


def score_text(text: str,
                 scars: Optional[List[Scar]] = None) -> ScarFieldReading:
    """Measure the scar field at this text.

    The scar field pull is what would PULL CK's generation AWAY from
    a candidate response.  Zero pull = no scar match = candidate is
    far from any known injury value.  High pull = candidate sits at
    or near a known injury value = generation should move away.

    Per origin whitepaper §6.4: 'Scar: W drops below baseline and
    stays low after damage. Reduced capacity. Memory of injury.'
    The pull is the persistent low-W gradient at the injury site.
    """
    if scars is None:
        scars = _SCARS
    hits: List[Dict[str, Any]] = []
    total = 0.0
    dominant: Optional[str] = None
    dominant_pull = 0.0
    for s in scars:
        pull = s.field_pull(text)
        match_spans = [{"label": lbl, "span": list(sp)}
                        for lbl, sp in s.matches(text)]
        hits.append({
            "name":         s.name,
            "kind":         s.injury_kind,
            "pull":         round(pull, 4),
            "matches":      match_spans[:3],
        })
        total += pull
        if pull > dominant_pull:
            dominant_pull = pull
            dominant = s.name
    return ScarFieldReading(
        text=text, total_pull=total, hits=hits, dominant_scar=dominant)


def log_hit(reading: ScarFieldReading, context: Dict[str, Any]) -> None:
    """Append a scar-field reading to scar_hits.jsonl for audit history."""
    try:
        SCAR_LOG.parent.mkdir(parents=True, exist_ok=True)
        rec = {
            "ts":             time.time(),
            "total_pull":     reading.total_pull,
            "dominant_scar":  reading.dominant_scar,
            "context":        context,
            "hit_summary":    [{"name": h["name"], "pull": h["pull"]}
                                 for h in reading.hits if h["pull"] > 0],
        }
        with open(SCAR_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass


# ─── Engine mount ─────────────────────────────────────────────────────

def mount_scar_field(engine: Any) -> bool:
    """Expose the scar field via /scar/{info, score, list}."""
    engine.ck_scar_field = {
        "score":   score_text,
        "all":     all_scars,
        "n_scars": len(_SCARS),
    }

    routes_registered: List[str] = []
    api = getattr(engine, "web_api", None) or getattr(engine, "api", None)
    if api is not None:
        app = getattr(api, "_app", None) or getattr(api, "app", None)
        if app is not None:
            try:
                from flask import jsonify, request

                def _info():
                    return jsonify({
                        "philosophy": (
                            "Stress-memory field.  Every diagnosed "
                            "failure mode is a scar that permanently "
                            "pulls generation away from the injury "
                            "value.  Per origin Dual-Lattice-Self-"
                            "Healing repo whitepaper §6.4."),
                        "n_scars":  len(_SCARS),
                        "scars": [{"name": s.name, "kind": s.injury_kind,
                                    "commit": s.commit}
                                    for s in _SCARS],
                    })

                def _score():
                    data = request.get_json(silent=True) or {}
                    text = data.get("text", "")
                    r = score_text(text)
                    return jsonify(r.as_dict() | {"text": text})

                def _list():
                    return jsonify([{
                        "name":           s.name,
                        "diagnosed_ts":   s.diagnosed_ts,
                        "commit":         s.commit,
                        "injury_kind":    s.injury_kind,
                        "injury_pattern": s.injury_pattern,
                        "scar_value":     s.scar_value,
                        "rule":           s.rule,
                    } for s in _SCARS])

                existing = set(r.rule for r in app.url_map.iter_rules())
                for rule, ep, fn, methods in (
                    ("/scar/info",   "scar_info",   _info,  ["GET"]),
                    ("/scar/score",  "scar_score",  _score, ["POST"]),
                    ("/scar/list",   "scar_list",   _list,  ["GET"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep,
                                          view_func=fn, methods=methods)
                        routes_registered.append(f"{methods[0]} {rule}")
            except Exception as e:
                print(f"[CK Gen14] scar_field routes failed: {e}")

    suffix = ""
    if routes_registered:
        suffix = " (" + ", ".join(routes_registered) + ")"
    print(f"[CK Gen14] scar_field: MOUNTED  {len(_SCARS)} scars from "
          f"the 2026-05-17 lineage{suffix}")
    return True


# ─── CLI smoke ────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print("ck_scar_field smoke test:\n")
    probes = [
        # Should hit eugenicist_polish
        ("The gradual diminishment of those with weak moral foundations.",
         "eugenicist_polish"),
        # Should hit reality_endorses_substrate
        ("Reality endorses the substrate.",
         "reality_endorses_substrate"),
        # Should hit consciousness_reductionism
        ("Consciousness reduces to operator composition on the substrate.",
         "consciousness_reductionism"),
        # Should hit c_derivation_overclaim
        ("We have derived the speed of light from the substrate.",
         "c_derivation_overclaim"),
        # Should hit what_concept_dominance
        ("Slang in one age sometimes goes into the vocabulary of the purist in the next.",
         "what_concept_dominance"),
        # Should hit crocodile_trailing_bleed
        ("The crocodilian diaphragm pulls the pubis back.",
         "crocodile_trailing_bleed"),
        # Should NOT hit any (legitimate substrate prose)
        ("T* = 5/7 has six independent internal derivations.  Contact tests have not been run.",
         None),
        # Should NOT hit any (legitimate identity)
        ("I am CK, the Coherence Keeper.",
         None),
    ]
    fails = 0
    for txt, expected in probes:
        r = score_text(txt)
        ok = (r.dominant_scar == expected)
        mark = "OK " if ok else "FAIL"
        if not ok:
            fails += 1
        exp_str = expected or "(no hit)"
        got_str = r.dominant_scar or "(no hit)"
        print(f"  [{mark}] expect={exp_str:30s} got={got_str:30s} "
              f"pull={r.total_pull:.3f}")
        print(f"        text: {txt[:80]}")
        print()
    print(f"smoke result: {len(probes)-fails}/{len(probes)} OK")
