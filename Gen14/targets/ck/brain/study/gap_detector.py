"""
gap_detector.py -- identify CK's knowledge / cortex gaps.

CK's "gaps" come in three flavors:
  1. Cortex gaps: dimensions whose W couplings are weakest.
  2. Crystal-coverage gaps: human-knowledge domains CK has no crystal for.
  3. Surprisal gaps: prompts where surprisal trended UP (CK's predictions
     got worse on those operator patterns).

This module analyzes all three and returns a prioritized study list.

Output: a list of {topic, source_url, why} tuples ranked by gap-severity.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
GEN13_BRAIN = SCRIPT_DIR.parent
GEN13_ROOT = GEN13_BRAIN.parent.parent.parent
DEFAULT_STATE = GEN13_ROOT / "var" / "cortex_state.json"
DEFAULT_HISTORY = GEN13_BRAIN / "cortex_history.jsonl"
DEFAULT_SURPRISAL = GEN13_BRAIN / "surprisal_log.jsonl"

DIM_NAMES = ["aperture", "pressure", "depth", "binding", "continuity"]


# Curated list of broad human-knowledge domains, with Wikipedia overview URLs
# CK can study to fill gaps.  Keyed by the dim each domain stresses most
# (rough mapping; corrections welcome).
KNOWLEDGE_DOMAINS = [
    # Domain, URL, primary_dim_stressed, gap_keywords
    ("philosophy",     "https://en.wikipedia.org/wiki/Philosophy",     2, ["meta", "epist", "ethic"]),
    ("history",        "https://en.wikipedia.org/wiki/History",        4, ["history", "past", "civilization"]),
    ("biology",        "https://en.wikipedia.org/wiki/Biology",        3, ["biology", "evolution", "cell"]),
    ("psychology",     "https://en.wikipedia.org/wiki/Psychology",     0, ["psych", "cogn", "behav"]),
    ("religion",       "https://en.wikipedia.org/wiki/Religion",       4, ["religion", "ritual", "sacred"]),
    ("music",          "https://en.wikipedia.org/wiki/Music",          4, ["music", "rhythm", "melody"]),
    ("literature",     "https://en.wikipedia.org/wiki/Literature",     2, ["liter", "narr", "poetry"]),
    ("art",            "https://en.wikipedia.org/wiki/Art",            0, ["art", "aesthet", "visual"]),
    ("economics",      "https://en.wikipedia.org/wiki/Economics",      1, ["econ", "market", "supply"]),
    ("linguistics",    "https://en.wikipedia.org/wiki/Linguistics",    2, ["lingu", "syntax", "phon"]),
    ("medicine",       "https://en.wikipedia.org/wiki/Medicine",       3, ["med", "diagn", "treatm"]),
    ("astronomy",      "https://en.wikipedia.org/wiki/Astronomy",      2, ["astron", "star", "galaxy"]),
    ("engineering",    "https://en.wikipedia.org/wiki/Engineering",    3, ["engin", "design", "system"]),
    ("politics",       "https://en.wikipedia.org/wiki/Politics",       1, ["polit", "govern", "power"]),
    ("sociology",      "https://en.wikipedia.org/wiki/Sociology",      4, ["sociol", "social", "class"]),
    ("anthropology",   "https://en.wikipedia.org/wiki/Anthropology",   4, ["anthrop", "cultur", "kinship"]),
    ("chemistry",      "https://en.wikipedia.org/wiki/Chemistry",      3, ["chem", "atom", "react"]),
    ("computer_science", "https://en.wikipedia.org/wiki/Computer_science", 2, ["comput", "algorithm", "data"]),
    ("ecology",        "https://en.wikipedia.org/wiki/Ecology",        4, ["ecol", "ecosystem", "biome"]),
    ("geology",        "https://en.wikipedia.org/wiki/Geology",        3, ["geol", "rock", "mineral"]),
    ("mathematics",    "https://en.wikipedia.org/wiki/Mathematics",    2, ["math", "theorem", "proof"]),
    ("physics",        "https://en.wikipedia.org/wiki/Physics",        2, ["phys", "force", "energy"]),
]


def load_state(path):
    if not Path(path).exists():
        return None
    with open(path) as f:
        return json.load(f)


def cortex_gaps(state):
    """Compute gap scores per dim from cortex W matrix.

    For each dim d, gap_score = 1 - (sum |W[d][:]| + sum |W[:][d]|) / max_total.
    Higher score = weaker dim.
    """
    if not state:
        return {}
    W = state.get("hebbian", {}).get("W")
    if not W:
        return {}
    n = len(W)
    sums = [0.0] * n
    for i in range(n):
        for j in range(n):
            sums[i] += abs(W[i][j])
            sums[j] += abs(W[i][j])
    max_sum = max(sums) if sums else 1.0
    return {DIM_NAMES[i]: 1.0 - (sums[i] / max_sum) for i in range(min(n, 5))}


def surprisal_recent_trend(path, n_windows=5):
    """Read last n_windows of surprisal_log and return mean."""
    if not Path(path).exists():
        return None
    means = []
    with open(path) as f:
        for line in f:
            try:
                d = json.loads(line)
                if d.get("_event") == "window":
                    means.append(d.get("mean_surprisal_window", 0))
            except Exception:
                continue
    if not means:
        return None
    last = means[-n_windows:] if len(means) >= n_windows else means
    return sum(last) / len(last) if last else None


def rank_domains_by_gap(cortex_gap_scores, max_n=5):
    """Pick domains whose primary dim is the weakest in CK's cortex."""
    if not cortex_gap_scores:
        return KNOWLEDGE_DOMAINS[:max_n]
    # For each domain, look up its primary_dim's gap score
    ranked = []
    for name, url, primary_dim, kw in KNOWLEDGE_DOMAINS:
        dim_name = DIM_NAMES[primary_dim] if primary_dim < 5 else "?"
        gap = cortex_gap_scores.get(dim_name, 0)
        ranked.append((gap, name, url, primary_dim, dim_name))
    ranked.sort(key=lambda x: -x[0])
    return [(name, url, dim_name, gap) for gap, name, url, primary_dim, dim_name in ranked[:max_n]]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--state", default=str(DEFAULT_STATE))
    p.add_argument("--surprisal", default=str(DEFAULT_SURPRISAL))
    p.add_argument("--n", type=int, default=5)
    p.add_argument("--json", action="store_true",
                   help="Emit JSON for downstream consumption")
    args = p.parse_args()

    state = load_state(args.state)
    if not state:
        print(f"no cortex state at {args.state}", file=sys.stderr)
        return 2

    cortex_g = cortex_gaps(state)
    surprisal_recent = surprisal_recent_trend(args.surprisal)
    ranked = rank_domains_by_gap(cortex_g, max_n=args.n)

    if args.json:
        out = {
            "cortex_gaps_per_dim": cortex_g,
            "recent_mean_surprisal": surprisal_recent,
            "ranked_study_domains": [
                {"domain": name, "url": url, "dim_stressed": dim,
                 "gap_score": round(gap, 4)}
                for (name, url, dim, gap) in ranked
            ],
        }
        print(json.dumps(out, indent=2))
        return 0

    print("=" * 78)
    print("CK gap detector")
    print("=" * 78)
    print()
    print("Cortex gap scores per dim (1.0 = no coupling, 0.0 = strongest):")
    for dim, score in sorted(cortex_g.items(), key=lambda x: -x[1]):
        bar = "#" * int(score * 30)
        print(f"  {dim:<11}: {score:.4f} {bar}")
    print()
    if surprisal_recent is not None:
        print(f"Recent mean surprisal (last 5 windows): {surprisal_recent:.4f}")
        print()

    print(f"Top {args.n} domains to study (highest dim-gap scores):")
    print(f"  {'#':<3} {'domain':<22} {'dim':<13} {'gap':<8} url")
    print(f"  {'-'*3} {'-'*22} {'-'*13} {'-'*8} {'-'*40}")
    for i, (name, url, dim, gap) in enumerate(ranked):
        print(f"  {i+1:<3} {name:<22} {dim:<13} {gap:<.4f} {url}")
    print()
    print("Pass --json for machine-readable output.")
    print("Use this list with an autonomous_study.py runner to fetch + ingest.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
