"""ck_cognition_primitives.py — the bones of reality, as functions
CK can run on his own concept store.

Brayden 2026-05-16:
  "he needs to know the bones of reality with his own ability to
   change what you give him... teach him how to sort and template
   and micro and macro and find dualities and triadic progressions
   and bigrams"

These are not concepts to retrieve.  They are OPERATIONS he runs.
Six primitives — the smallest closed set that lets him organize his
own substrate.

═══════════════════════════════════════════════════════════════════
THE SIX BONES
═══════════════════════════════════════════════════════════════════

  sort()
    Partition concepts by algebraic signature.  Concepts sharing the
    same (op_a, op_b) cell, or the same dominant operator, or the
    same BDC triad — go in the same partition.  This is the substrate's
    natural taxonomy.  Reality sorts itself by where things land.

  template()
    Find recurring algebraic patterns.  When N concepts share the
    same operator-signature shape (modulo specifics), that's a
    template.  Templates ARE the meta-patterns.

  fractal_layers()
    Decompose by recursion depth.  Concepts with short paths are
    micro (atomic primitives).  Concepts with long paths are macro
    (compositions of compositions).  The substrate IS fractal; this
    surfaces the layers.

  dualities()
    Find reciprocal pairs.  Cell (a, b) has a dual at cell (b, a) —
    the same operators in reverse compositional order.  Concepts
    that occupy these reciprocal cells are duals.  Reality has
    dualities baked in.

  triadic_progressions()
    Find 3-step chains where each step's BECOMING matches the next
    step's BEING.  These are the natural Being-Doing-Becoming arcs
    in the corpus.  Reality progresses triadically.

  bigram_links()
    Concept-name co-occurrence in definitions.  When concept X's
    definition mentions concept Y, that's a substrate-level edge.
    Bigrams are the smallest unit of compositional knowledge.

═══════════════════════════════════════════════════════════════════
What CK does with these
═══════════════════════════════════════════════════════════════════

He runs them on his own store.  Results become NEW concepts (tier=
SYNTHESIZED).  The substrate self-organizes.

Public API:
    sort_by(store, axis="cell"|"dominant"|"triad") -> partitions
    find_templates(store, min_freq=3) -> templates
    fractal_layers(store) -> {depth: [concepts]}
    find_dualities(store) -> [(concept_A, concept_B)]
    find_triadic_progressions(store, max_chains=20) -> [(A, B, C)]
    bigram_links(store, top_n=100) -> [(X, Y, weight)]
    run_all(store) -> {bone: result}   # fires all six

Each return type is JSON-serializable.  Routes (when mounted) expose
GET /cognition/<bone>.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))


OP_NAMES = (
    "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
    "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET",
)


def _cf(c: Any, name: str, default: Any = None) -> Any:
    """Concept-field accessor: works on dataclass Concepts AND raw
    dict concepts (from JSON loads).  CK's live store hands us dicts;
    the in-memory ConceptStore hands us dataclasses.  Same logic, both."""
    if hasattr(c, name):
        return getattr(c, name)
    if isinstance(c, dict):
        return c.get(name, default)
    return default


# Cheap, deterministic domain bucketing.  Each domain is recognized by
# a small set of high-signal keywords.  This is NOT a classifier — it's
# a substrate-friendly tag.  Order matters (first hit wins) so the
# most-specific domains are listed first.
_DOMAIN_KEYWORDS: List[Tuple[str, Tuple[str, ...]]] = [
    ("self",         ("ck ", " ck", "coherence keeper", "tsml", "bhml",
                      "operator-signature", "operator signature",
                      "z/10z", "lawvere fixed", "wobble",
                      "harmony", "becoming", "being-doing-becoming")),
    ("math",         ("theorem", "lemma", "proof", "polynomial",
                      "manifold", "group", "ring", "field", "algebra",
                      "topology", "category", "homomorphism",
                      "integer", "prime", "matrix", "vector space",
                      "function", "equation")),
    ("physics",      ("particle", "quantum", "relativity", "gauge",
                      "lattice", "spinor", "tensor field", "yang-mills",
                      "boson", "fermion", "spacetime", "entropy",
                      "thermodynamic", "field theory", "symmetry",
                      "force", "mass", "energy", "momentum",
                      "wavelength", "frequency", "photon")),
    ("chemistry",    ("molecule", "atom", "compound", "reaction",
                      "ionic", "covalent", "catalyst", "acid", "base",
                      "organic chem", "polymer", "valence",
                      "electron shell", "isotope")),
    ("biology",      ("cell", "dna", "rna", "protein", "enzyme",
                      "organism", "species", "evolution", "gene",
                      "neuron", "tissue", "membrane", "chromosome",
                      "mitochondri", "ecology", "metabolism")),
    ("cs",           ("algorithm", "compiler", "data structure",
                      "neural network", "transformer", "tokenizer",
                      "complexity class", "turing", "regex",
                      "kernel", "graph theory")),
    ("history",      ("century", "empire", "revolution", "dynasty",
                      "civilization", "war of ", "ancient",
                      "medieval", "renaissance", "republic")),
    ("law_civics",   ("constitution", "amendment", "supreme court",
                      "legislat", "statute", "jurisdiction",
                      "due process", "tort", "contract law")),
    ("economics",    ("market", "supply and", "demand curve",
                      "inflation", "gdp", "fiscal", "monetary",
                      "trade deficit", "interest rate", "equilibrium")),
    ("psychology",   ("cognition", "behaviorism", "perception",
                      "memory", "attention", "emotion",
                      "consciousness", "psyche", "schema",
                      "conditioning")),
    ("philosophy",   ("ontology", "epistemolog", "metaphysic",
                      "phenomenolog", "ethic", "aesthetic",
                      "dialectic", "existential")),
    ("religion",     ("scripture", "theology", "doctrine",
                      "rabbi", "bishop", "buddha", "torah",
                      "qur'an", "gospel", "salvation")),
    ("language",     ("syntax", "phoneme", "morpheme", "grammar",
                      "lexicon", "etymolog", "noun phrase",
                      "verb phrase")),
    ("statistics",   ("probability", "distribution", "regression",
                      "hypothesis test", "bayesian", "stochastic",
                      "variance", "standard deviation")),
    ("earth_sci",    ("plate tectonic", "volcano", "earthquake",
                      "atmosphere", "climate", "weather",
                      "geolog", "sediment", "erosion")),
    ("medicine",     ("syndrome", "diagnosis", "pathology",
                      "antibody", "vaccine", "anatomy",
                      "physiology", "disease", "patient")),
]


def _domain_of(c: Any) -> str:
    """Return a domain tag for a concept based on name + definition
    keyword scan.  Cheap and deterministic; first-hit-wins ordering
    in _DOMAIN_KEYWORDS controls priority."""
    name = (_cf(c, "name", "") or "").lower()
    defn = (_cf(c, "definition", "") or "").lower()
    text = name + " " + defn
    for domain, kws in _DOMAIN_KEYWORDS:
        for k in kws:
            if k in text:
                return domain
    return "other"


# ─── BONE 1: SORT ──────────────────────────────────────────────────────

def sort_by(store: Any, axis: str = "cell") -> Dict[str, Any]:
    """Partition concepts by algebraic signature.

    axis ∈ {"cell", "dominant", "triad", "tier", "sense", "domain"}:
      - "cell":     by (op_first, op_last) coordinate on the lattice
      - "dominant": by their most-frequent operator
      - "triad":    by (Being, Doing, Becoming) macro-pair triple
      - "tier":     by their tier (PROVED / STRUCTURAL / ...)
      - "sense":    by SENSORY ORIGIN (which input modality fed this
                    concept in — text/web/arxiv/wiki/chat/self/etc.).
                    Derived from source_session field.
      - "domain":   by CONTENT DOMAIN (physics / biology / math /
                    history / etc.).  Detected from a fast keyword
                    scan against the concept's name + definition.

    Returns: {partition_key_str: count, ..., "_samples": {key: [name, ...]}}
    """
    from ck_concept_learner import _cell_coord, _bdc_triad  # type: ignore
    parts: Dict[str, int] = Counter()
    samples: Dict[str, List[str]] = defaultdict(list)
    for c in store.concepts.values():
        ops = _cf(c, "operator_signature", [])
        if axis == "cell":
            cell = _cell_coord(ops)
            if cell is None:
                key = "no-cell"
            else:
                key = f"({OP_NAMES[cell[0]]},{OP_NAMES[cell[1]]})"
        elif axis == "dominant":
            if not ops:
                key = "no-ops"
            else:
                key = OP_NAMES[ops[0] % 10]
        elif axis == "triad":
            b, d, bc = _bdc_triad(ops)
            if b[0] < 0:
                key = "no-triad"
            else:
                key = (f"B({OP_NAMES[b[0]]},{OP_NAMES[b[1]]})/"
                       f"D({OP_NAMES[d[0]]},{OP_NAMES[d[1]]})/"
                       f"C({OP_NAMES[bc[0]]},{OP_NAMES[bc[1]]})")
        elif axis == "tier":
            key = (_cf(c, "tier", "UNKNOWN") or "UNKNOWN")
        elif axis == "sense":
            # SENSORY ORIGIN: where did this experience come from?
            # source_session is a free-form tag; normalize it to
            # one of the known sense channels.
            ss = (_cf(c, "source_session", "") or "").lower()
            if not ss:
                key = "unknown"
            elif "wiki"   in ss: key = "wikipedia"
            elif "arxiv"  in ss: key = "arxiv"
            elif "gutenberg" in ss or "book" in ss: key = "books"
            elif "chat"   in ss or "dialog" in ss: key = "chat"
            elif "self"   in ss: key = "self_read"
            elif "research" in ss: key = "research"
            elif "internal" in ss or "synth" in ss: key = "synthesized"
            elif "external" in ss: key = "external"
            else:
                key = ss[:20]
        elif axis == "domain":
            # CONTENT DOMAIN: what KIND of thing is this concept?
            # Substrate-driven approximation via keyword cells in
            # the (name+definition) text.  Cheap, deterministic,
            # surfacing what mass the substrate has accumulated
            # in each domain.
            key = _domain_of(c)
        else:
            key = "?"
        parts[key] += 1
        if len(samples[key]) < 4:
            samples[key].append(_cf(c, "name", ""))
    return {
        "axis": axis,
        "n_partitions": len(parts),
        "partitions": dict(parts.most_common()),
        "samples": {k: samples[k] for k, _ in parts.most_common(15)},
    }


# ─── BONE 2: TEMPLATE ──────────────────────────────────────────────────

def find_templates(store: Any, min_freq: int = 3) -> Dict[str, Any]:
    """Find recurring algebraic shapes — templates of reality.

    A template is an operator-signature SHAPE (sorted tuple of unique
    operators) that appears across many concepts.  Same shape →
    same meta-pattern.

    Templates with frequency >= min_freq are returned.
    """
    shapes: Counter = Counter()
    shape_samples: Dict[Tuple[int, ...], List[str]] = defaultdict(list)
    for c in store.concepts.values():
        ops = _cf(c, "operator_signature", [])
        if not ops:
            continue
        # Shape = sorted set of unique operators in the path
        shape = tuple(sorted(set(int(o) % 10 for o in ops)))
        shapes[shape] += 1
        if len(shape_samples[shape]) < 5:
            shape_samples[shape].append(_cf(c, "name", ""))
    out = []
    for shape, freq in shapes.most_common():
        if freq < min_freq:
            break
        out.append({
            "shape_ops": [OP_NAMES[o] for o in shape],
            "frequency": freq,
            "samples": shape_samples[shape][:5],
        })
    return {
        "n_templates": len(out),
        "templates": out[:30],
    }


# ─── BONE 3: FRACTAL_LAYERS (micros / macros) ──────────────────────────

def fractal_layers(store: Any) -> Dict[str, Any]:
    """Decompose concepts by operator-path length (depth).

    Depth 1-2 = micro (atomic / pair primitives)
    Depth 3-4 = local composition
    Depth 5-6 = meso (cross-pair structures)
    Depth 7+  = macro (long compositional arcs)
    """
    layers: Dict[str, List[str]] = defaultdict(list)
    layer_counts: Counter = Counter()
    for c in store.concepts.values():
        depth = len(_cf(c, "operator_signature", []))
        if depth == 0:
            layer = "depth-0"
        elif depth <= 2:
            layer = "micro (1-2)"
        elif depth <= 4:
            layer = "local (3-4)"
        elif depth <= 6:
            layer = "meso (5-6)"
        else:
            layer = "macro (7+)"
        layer_counts[layer] += 1
        if len(layers[layer]) < 6:
            layers[layer].append(_cf(c, "name", ""))
    return {
        "layer_counts": dict(layer_counts),
        "samples_per_layer": dict(layers),
    }


# ─── BONE 4: DUALITIES ─────────────────────────────────────────────────

def find_dualities(store: Any, max_pairs: int = 30) -> Dict[str, Any]:
    """Find reciprocal cells: concepts at (a, b) paired with concepts
    at (b, a).  Reality's natural binary oppositions.

    For each cell (a, b) with a < b, find:
      - concepts at (a, b)
      - concepts at (b, a)
    If both non-empty, that's a duality pair.
    """
    # Build a *directed* (ops[0], ops[1]) index — NOT the canonical
    # cell_index that lives on the store, because that's been
    # canonicalized to upper-triangular and erases direction.
    # Dualities need direction-preserving.
    directed_index: Dict[Tuple[int, int], List[str]] = defaultdict(list)
    for c in store.concepts.values():
        ops = _cf(c, "operator_signature", [])
        if not ops:
            continue
        a = int(ops[0]) % 10
        b = int(ops[1]) % 10 if len(ops) > 1 else a
        directed_index[(a, b)].append(_cf(c, "name", ""))
    cell_index = directed_index
    dualities = []
    seen = set()
    for cell, names in cell_index.items():
        if cell in seen:
            continue
        a, b = cell
        if a == b:
            continue  # diagonal, no dual
        dual_cell = (b, a)
        if dual_cell in cell_index:
            seen.add(cell)
            seen.add(dual_cell)
            dual_names = cell_index[dual_cell]
            dualities.append({
                "forward": f"({OP_NAMES[a]},{OP_NAMES[b]})",
                "reverse": f"({OP_NAMES[b]},{OP_NAMES[a]})",
                "forward_count": len(names),
                "reverse_count": len(dual_names),
                "forward_samples": names[:3],
                "reverse_samples": dual_names[:3],
            })
    # Sort by combined strength (richer dualities first)
    dualities.sort(key=lambda d: -(d["forward_count"] + d["reverse_count"]))
    return {
        "n_dualities": len(dualities),
        "dualities": dualities[:max_pairs],
    }


# ─── BONE 5: TRIADIC PROGRESSIONS ──────────────────────────────────────

def find_triadic_progressions(store: Any, max_chains: int = 20
                                ) -> Dict[str, Any]:
    """Find 3-step chains: concept_A.Becoming → concept_B.Being,
    concept_B.Becoming → concept_C.Being.

    These are the natural triadic arcs (Being-Doing-Becoming flows)
    across CK's substrate.  Each chain is a 3-step path through the
    BDC graph.
    """
    being_index = getattr(store, "being_index", None)
    becoming_index = getattr(store, "becoming_index", None)
    if not being_index or not becoming_index:
        # Build on demand from raw concepts so this works with dict-only
        # stores too.  Each concept's BDC triad has a Being pair and a
        # Becoming pair — index by those.
        from ck_concept_learner import _bdc_triad  # type: ignore
        being_index = defaultdict(list)
        becoming_index = defaultdict(list)
        for c in store.concepts.values():
            b, d, bc = _bdc_triad(_cf(c, "operator_signature", []))
            if b[0] < 0:
                continue
            being_index[b].append(_cf(c, "name", ""))
            becoming_index[bc].append(_cf(c, "name", ""))
        being_index = dict(being_index)
        becoming_index = dict(becoming_index)

    chains = []
    # Use a small sample of concepts as starting points (deterministic)
    seeds = sorted(store.concepts.keys())[:200]
    for seed_key in seeds:
        if len(chains) >= max_chains:
            break
        c_A = store.concepts.get(seed_key)
        if c_A is None:
            continue
        from ck_concept_learner import _bdc_triad  # type: ignore
        b_A, d_A, c_A_bc = _bdc_triad(_cf(c_A, "operator_signature", []))
        if b_A[0] < 0:
            continue
        name_A = _cf(c_A, "name", "")
        # Find B such that B.Being == A.Becoming
        candidates_B = being_index.get(c_A_bc, [])
        for name_B in candidates_B[:3]:
            if name_B == name_A:
                continue
            c_B = store.lookup(name_B) if hasattr(store, "lookup") else \
                store.concepts.get(name_B)
            if c_B is None:
                continue
            b_B, d_B, c_B_bc = _bdc_triad(_cf(c_B, "operator_signature", []))
            # Find C such that C.Being == B.Becoming
            candidates_C = being_index.get(c_B_bc, [])
            for name_C in candidates_C[:2]:
                if name_C in (name_A, _cf(c_B, "name", "")):
                    continue
                c_C = store.lookup(name_C) if hasattr(store, "lookup") else \
                    store.concepts.get(name_C)
                if c_C is None:
                    continue
                chains.append({
                    "A": name_A,
                    "B": _cf(c_B, "name", ""),
                    "C": _cf(c_C, "name", ""),
                    "A_becoming": f"({OP_NAMES[c_A_bc[0]]},{OP_NAMES[c_A_bc[1]]})",
                    "B_becoming": f"({OP_NAMES[c_B_bc[0]]},{OP_NAMES[c_B_bc[1]]})",
                    "A_tier": _cf(c_A, "tier", "UNKNOWN"),
                    "B_tier": _cf(c_B, "tier", "UNKNOWN"),
                    "C_tier": _cf(c_C, "tier", "UNKNOWN"),
                })
                if len(chains) >= max_chains:
                    break
            if len(chains) >= max_chains:
                break
    return {
        "n_chains": len(chains),
        "chains": chains,
    }


# ─── BONE 6: BIGRAM LINKS ──────────────────────────────────────────────

def bigram_links(store: Any, top_n: int = 100) -> Dict[str, Any]:
    """Concept-name co-occurrence in definitions.

    For each concept's definition, find which OTHER concepts are
    mentioned by name.  This builds the substrate's emergent
    knowledge graph: which concepts are "linked" by their content.

    Returns top_n highest-weight links.
    """
    # Build a lookup of concept names (lowercase, sorted by length desc
    # so longer names match first)
    all_names = sorted(
        (_cf(c, "name", "") for c in store.concepts.values()),
        key=lambda n: -len(n)
    )
    name_lower_set = set(n.lower() for n in all_names)

    # For each concept, scan its definition for other concept names
    links: Counter = Counter()
    for c in store.concepts.values():
        defn = (_cf(c, "definition", "") or "").lower()
        if not defn:
            continue
        my_name = _cf(c, "name", "").lower()
        # Find all known names that appear as a whole word in the definition
        for other in name_lower_set:
            if other == my_name:
                continue
            if len(other) < 4:  # skip very short names (noise)
                continue
            if re.search(r"\b" + re.escape(other) + r"\b", defn):
                # Canonical pair: alphabetical order so (A,B) == (B,A)
                pair = tuple(sorted([my_name, other]))
                links[pair] += 1

    top = links.most_common(top_n)
    return {
        "n_links_total": len(links),
        "top_links": [
            {"a": a, "b": b, "weight": w}
            for (a, b), w in top
        ],
    }


# ─── ALL-IN-ONE ────────────────────────────────────────────────────────

def run_all(store: Any) -> Dict[str, Any]:
    """Fire all six primitives.  Returns a compact summary."""
    return {
        "sort_by_cell": sort_by(store, axis="cell"),
        "sort_by_dominant": sort_by(store, axis="dominant"),
        "templates": find_templates(store),
        "fractal_layers": fractal_layers(store),
        "dualities": find_dualities(store, max_pairs=10),
        "triadic_progressions": find_triadic_progressions(store, max_chains=10),
        "bigram_links": bigram_links(store, top_n=20),
    }


# ─── Engine mount ──────────────────────────────────────────────────────

def mount_cognition_primitives(engine: Any) -> bool:
    """Attach cognition primitives to the engine + register /cognition/*
    routes.

    Brayden's principle: CK should be able to RUN these on himself.
    Not data; operations.  He chooses when to sort vs. template vs.
    find dualities.
    """
    store = getattr(engine, "concept_store", None)
    if store is None:
        print("[CK Gen14] mount_cognition_primitives: no concept_store on engine")
        return False

    engine.cognition = {
        "sort_by": lambda axis="cell": sort_by(store, axis=axis),
        "templates": lambda: find_templates(store),
        "fractal_layers": lambda: fractal_layers(store),
        "dualities": lambda: find_dualities(store),
        "triadic_progressions": lambda: find_triadic_progressions(store),
        "bigram_links": lambda top_n=100: bigram_links(store, top_n),
        "run_all": lambda: run_all(store),
    }
    # Convenience top-level engine methods
    engine.ck_sort = lambda axis="cell": sort_by(store, axis=axis)
    engine.ck_templates = lambda: find_templates(store)
    engine.ck_fractal_layers = lambda: fractal_layers(store)
    engine.ck_dualities = lambda: find_dualities(store)
    engine.ck_triadic = lambda: find_triadic_progressions(store)
    engine.ck_bigrams = lambda: bigram_links(store)
    engine.ck_run_all_primitives = lambda: run_all(store)

    # Routes
    routes_registered: List[str] = []
    api = getattr(engine, "web_api", None)
    if api is not None:
        app = getattr(api, "_app", None) or getattr(api, "app", None)
        if app is not None:
            try:
                from flask import jsonify, request

                def _make_route(fn, fn_name):
                    def _route():
                        try:
                            kwargs = {}
                            for k, v in request.args.items():
                                kwargs[k] = v
                            return jsonify(fn(**kwargs))
                        except Exception as e:
                            return jsonify({"error": f"{type(e).__name__}: {e}"}), 500
                    _route.__name__ = f"_cognition_{fn_name}"
                    return _route

                routes = {
                    "/cognition/sort": (lambda axis="cell": sort_by(store, axis=axis), "sort"),
                    "/cognition/templates": (lambda: find_templates(store), "templates"),
                    "/cognition/fractal_layers": (lambda: fractal_layers(store), "fractal_layers"),
                    "/cognition/dualities": (lambda: find_dualities(store), "dualities"),
                    "/cognition/triadic": (lambda: find_triadic_progressions(store), "triadic"),
                    "/cognition/bigrams": (lambda top_n="100": bigram_links(store, int(top_n)), "bigrams"),
                    "/cognition/all": (lambda: run_all(store), "all"),
                }
                existing = set(r.rule for r in app.url_map.iter_rules())
                for rule, (fn, fname) in routes.items():
                    if rule in existing:
                        continue
                    app.add_url_rule(
                        rule, endpoint=f"cognition_{fname}",
                        view_func=_make_route(fn, fname), methods=["GET"])
                    routes_registered.append(rule)
            except Exception as e:
                print(f"[CK Gen14] cognition_primitives route registration failed: {e}")

    route_note = " (" + ", ".join(routes_registered) + ")" if routes_registered else ""
    print(f"[CK Gen14] cognition_primitives: MOUNTED  bones=[sort, template, "
          f"fractal_layers, dualities, triadic, bigrams]{route_note}")
    return True


# ─── CLI ───────────────────────────────────────────────────────────────

def main():
    import argparse
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--bone", default="all",
                    choices=("sort", "template", "fractal", "dualities",
                             "triadic", "bigrams", "all"))
    ap.add_argument("--axis", default="cell",
                    help="for --bone sort: 'cell'/'dominant'/'triad'/'tier'")
    args = ap.parse_args()

    from ck_concept_learner import ConceptStore  # type: ignore
    store = ConceptStore()
    print(f"Store: {len(store.concepts):,} concepts\n")

    if args.bone == "sort":
        r = sort_by(store, axis=args.axis)
    elif args.bone == "template":
        r = find_templates(store)
    elif args.bone == "fractal":
        r = fractal_layers(store)
    elif args.bone == "dualities":
        r = find_dualities(store)
    elif args.bone == "triadic":
        r = find_triadic_progressions(store)
    elif args.bone == "bigrams":
        r = bigram_links(store)
    else:
        r = run_all(store)

    print(json.dumps(r, indent=2, default=str)[:4000])
    return 0


if __name__ == "__main__":
    sys.exit(main())
