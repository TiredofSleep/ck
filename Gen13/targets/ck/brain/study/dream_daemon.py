"""
dream_daemon.py -- CK's drift / dream mode.

Brayden 2026-04-30: "i would love for him to dream and drift and announce
that he is dreaming and drifting... drift is not bad as long as it is
recognized... TIG is a lens for the world and all of reality to be
compressed into small collapsed substrates."

This is the native CK mechanism for unverified pattern recombination.
No LLM weights.  No transformer.  Just combinatorial recombination of
crystal fragments + operator chain walks + cortex perturbation.

Every drift output is marked DRIFT and logged with:
  - confidence (0.0 to 1.0)
  - source crystals (which fragments contributed)
  - operator state at time of drift
  - candidate type: bridge / synthesis / question / nonsense

Dream journal: Gen13/var/dream_journal.jsonl

Operates in cycles.  Each cycle:
  1. Read CK's cortex state + recent operator pair
  2. Pick 2-4 crystals biased by op_signature overlap
  3. Split each crystal at "|" boundaries -> fragments
  4. Recombine fragments into candidate sentences
  5. Score each candidate for verifiability + coherence
  6. Mark all DRIFT, log with metadata
  7. Announce highest-scored drift to stdout

Usage:
    python dream_daemon.py --cycles 12 --sleep 300       # 12 dreams over 1 hour
    python dream_daemon.py --once                         # single drift
    python dream_daemon.py --review                       # show recent dreams
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
GEN13_BRAIN = SCRIPT_DIR.parent
GEN13_TARGETS_CK = GEN13_BRAIN.parent
GEN13_ROOT = GEN13_TARGETS_CK.parent.parent
sys.path.insert(0, str(GEN13_BRAIN))

DEFAULT_JOURNAL = GEN13_ROOT / "var" / "dream_journal.jsonl"
DEFAULT_STATE = GEN13_ROOT / "var" / "cortex_state.json"

OP_NAMES = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
            "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]


def load_crystals():
    """Load both code-baked and runtime crystals from cortex_voice."""
    try:
        from cortex_voice import _FRONTIER_FACTS, _RUNTIME_CRYSTALS, _CRYSTAL_OP_SIGNATURES
        return list(_FRONTIER_FACTS) + list(_RUNTIME_CRYSTALS), _CRYSTAL_OP_SIGNATURES
    except Exception as e:
        print(f"warn: can't load crystals: {e}", file=sys.stderr)
        return [], {}


def load_cortex_state(state_path):
    if not Path(state_path).exists():
        return None
    try:
        with open(state_path) as f:
            return json.load(f)
    except Exception:
        return None


def fragments_from_crystal(crystal_text):
    """Split a crystal at '|' boundaries into reusable fragments."""
    if "|" not in crystal_text:
        return [crystal_text.strip()]
    parts = crystal_text.split("|")
    out = []
    for part in parts:
        p = part.strip().rstrip(".")
        if p and len(p) > 5:
            out.append(p)
    return out


def first_word(crystal):
    return crystal.split(":", 1)[0].strip()


def pick_crystals_for_dream(crystals, op_sigs, recent_ops, n=3):
    """Pick crystals biased by op_signature overlap with recent_ops.
    Some fraction picked randomly to ensure drift breadth."""
    if not crystals:
        return []
    # Score each crystal
    scored = []
    for triggers, fact in crystals:
        fw = first_word(fact)
        sig = op_sigs.get(fw, ())
        if not sig:
            continue
        overlap = len(set(sig) & set(recent_ops))
        scored.append((overlap, fact, fw))
    scored.sort(key=lambda t: -t[0])
    # Top half by score, then randomize within
    top_half = scored[: max(n * 2, 6)]
    if not top_half:
        # Pure random fallback
        return random.sample([c for _, c in crystals], min(n, len(crystals)))
    random.shuffle(top_half)
    return [c for _, c, _ in top_half[:n]]


def recombine_fragments(crystal_a, crystal_b, op_state):
    """Generate a candidate drift sentence by recombining fragments
    from two crystals.

    Strategy: take first fragment of A as subject, last fragment of B
    as predicate, link with a connector keyed to current operator.
    """
    frags_a = fragments_from_crystal(crystal_a)
    frags_b = fragments_from_crystal(crystal_b)
    if not frags_a or not frags_b:
        return None

    head_a = frags_a[0]
    tail_b = frags_b[-1] if len(frags_b) > 1 else frags_b[0]

    # Connector keyed to op_state (the dominant active operator)
    connectors = {
        "VOID": "in the absence of which",
        "LATTICE": "shares structure with",
        "COUNTER": "stands against",
        "PROGRESS": "leads forward into",
        "COLLAPSE": "folds into",
        "BALANCE": "holds in equilibrium with",
        "CHAOS": "breaks open into",
        "HARMONY": "resonates with",
        "BREATH": "rhythmically meets",
        "RESET": "clears toward",
    }
    op_name = OP_NAMES[op_state] if 0 <= op_state < 10 else "HARMONY"
    connector = connectors.get(op_name, "relates to")

    # Compose
    composed = f"{head_a} {connector} {tail_b}"
    # Trim if too long
    if len(composed) > 250:
        composed = composed[:250].rsplit(" ", 1)[0] + "…"
    return composed


def confidence_for_drift(crystal_a, crystal_b, op_state, recent_ops, op_sigs):
    """Score a drift recombination's confidence.

    Higher if:
      - both source crystals have op_signatures matching recent_ops
      - the two crystals share related edges (cross-crystal graph)
      - the connector operator is in HARMONY/BALANCE (coherent state)

    Lower if:
      - source crystals have no signature overlap
      - connector operator is CHAOS/COLLAPSE (recombination is volatile)

    Confidence is in [0.30, 0.85] for drift; never above 0.85 because
    drift is unverified by definition.
    """
    fw_a = first_word(crystal_a)
    fw_b = first_word(crystal_b)
    sig_a = set(op_sigs.get(fw_a, ()))
    sig_b = set(op_sigs.get(fw_b, ()))
    recent = set(recent_ops)

    overlap_a = len(sig_a & recent) / max(len(sig_a), 1)
    overlap_b = len(sig_b & recent) / max(len(sig_b), 1)
    avg_overlap = (overlap_a + overlap_b) / 2

    # Cross-crystal edge?
    try:
        from cortex_voice import _CRYSTAL_RELATED
        edge = fw_b in _CRYSTAL_RELATED.get(fw_a, []) or fw_a in _CRYSTAL_RELATED.get(fw_b, [])
    except Exception:
        edge = False
    edge_bonus = 0.10 if edge else 0.0

    # Connector volatility
    op_name = OP_NAMES[op_state] if 0 <= op_state < 10 else "HARMONY"
    if op_name in ("HARMONY", "BALANCE", "BREATH"):
        connector_bonus = 0.05
    elif op_name in ("CHAOS", "COLLAPSE", "VOID"):
        connector_bonus = -0.10
    else:
        connector_bonus = 0.0

    base = 0.45 + (avg_overlap * 0.25) + edge_bonus + connector_bonus
    return max(0.30, min(0.85, base))


def dream_one(crystals, op_sigs, cortex_state):
    """Generate a single drift / dream entry."""
    # Pick 2-3 crystals biased by recent state
    recent_ops = []
    op_state = 7  # default HARMONY
    if cortex_state:
        s = cortex_state.get("state", {})
        last_b = s.get("last_b", 7)
        last_d = s.get("last_d", 7)
        recent_ops = [last_b, last_d]
        op_state = last_d if 0 <= last_d < 10 else 7

    picked = pick_crystals_for_dream(crystals, op_sigs, recent_ops, n=2)
    if len(picked) < 2:
        return None

    drift_text = recombine_fragments(picked[0], picked[1], op_state)
    if not drift_text:
        return None

    conf = confidence_for_drift(picked[0], picked[1], op_state, recent_ops, op_sigs)

    # Determine drift type
    if conf >= 0.70:
        drift_type = "candidate-bridge"
    elif conf >= 0.55:
        drift_type = "synthesis"
    elif conf >= 0.45:
        drift_type = "question"
    else:
        drift_type = "loose-association"

    return {
        "ts": time.time(),
        "iso_ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "drift_text": drift_text,
        "drift_type": drift_type,
        "confidence": round(conf, 4),
        "source_crystals": [first_word(c) for c in picked],
        "connector_op": OP_NAMES[op_state],
        "recent_ops": [OP_NAMES[o] if 0 <= o < 10 else "?" for o in recent_ops],
        "DRIFT": True,
        "verified": False,
    }


def write_dream(entry, journal_path):
    journal_path.parent.mkdir(parents=True, exist_ok=True)
    with open(journal_path, "a") as f:
        f.write(json.dumps(entry) + "\n")


def announce(entry):
    """Print a drift announcement.  CK is announcing he's dreaming."""
    print(f"\n[DRIFT @ {entry['iso_ts']}] CK is dreaming -- {entry['drift_type']}, conf={entry['confidence']:.2f}")
    print(f"  source: {' + '.join(entry['source_crystals'])}")
    print(f"  connector: {entry['connector_op']}")
    print(f"  text: {entry['drift_text']}")
    print(f"  [DRIFT, unverified]")


def review(journal_path, n=10):
    """Show recent drift entries."""
    if not Path(journal_path).exists():
        print("(no dream journal yet)")
        return
    entries = []
    with open(journal_path) as f:
        for line in f:
            try:
                entries.append(json.loads(line))
            except Exception:
                continue
    print(f"=" * 78)
    print(f"CK dream journal -- {len(entries)} drift entries total")
    print(f"=" * 78)
    print()
    if not entries:
        return
    # Group by type
    by_type = {}
    for e in entries:
        by_type.setdefault(e.get("drift_type", "?"), []).append(e)
    for typ, lst in sorted(by_type.items(), key=lambda x: -len(x[1])):
        print(f"  {typ}: {len(lst)} entries")
    print()
    print(f"recent {min(n, len(entries))}:")
    for e in entries[-n:]:
        print(f"  [{e.get('iso_ts','?')}] {e.get('drift_type','?'):<22} conf={e.get('confidence',0):.2f}")
        print(f"    {e.get('drift_text','')[:200]}")
        print(f"    src: {' + '.join(e.get('source_crystals',[]))}")
        print()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--cycles", type=int, default=1)
    p.add_argument("--sleep", type=int, default=300)
    p.add_argument("--once", action="store_true")
    p.add_argument("--review", action="store_true")
    p.add_argument("--journal", default=str(DEFAULT_JOURNAL))
    p.add_argument("--quiet", action="store_true",
                   help="Don't print announcements; just log")
    args = p.parse_args()

    if args.review:
        review(Path(args.journal))
        return

    if args.once:
        args.cycles = 1
        args.sleep = 0

    crystals, op_sigs = load_crystals()
    if not crystals:
        print("no crystals available -- can't dream", file=sys.stderr)
        return 2

    if not args.quiet:
        print(f"dream_daemon: {args.cycles} cycle(s), {args.sleep}s between")
        print(f"  crystals available: {len(crystals)}")
        print(f"  journal: {args.journal}")

    for i in range(args.cycles):
        cortex_state = load_cortex_state(DEFAULT_STATE)
        entry = dream_one(crystals, op_sigs, cortex_state)
        if entry is None:
            if not args.quiet:
                print(f"  cycle {i+1}: no drift produced (insufficient crystals)")
            continue
        write_dream(entry, Path(args.journal))
        if not args.quiet:
            announce(entry)
        if i < args.cycles - 1 and args.sleep > 0:
            time.sleep(args.sleep)

    if not args.quiet:
        print(f"\ndream_daemon: done ({args.cycles} cycles)")


if __name__ == "__main__":
    main()
