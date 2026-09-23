"""
BENCH -- Resolution-Graded Disclosure (RGD) vs e-Differential Privacy
        vs k-Anonymity, on the privacy-utility frontier.

PRE-REGISTERED DECISION RULE (per BENCH_SPEC_RESOLUTION_DISCLOSURE §7):
  D-PRIV CONFIRMED if, on >=1 of the 3 datasets, the RGD frontier
  touches or dominates the better of the DP and k-anon frontiers at
  >=1 operating point (equal-or-better utility at equal-or-better
  privacy).
  D-PRIV FALSE if RGD's frontier is strictly dominated by both
  incumbents on all 3 datasets at all operating points.

HONEST PRIOR (per BENCH_SPEC §8):
  Most likely outcome -- RGD is dominated on tabular re-identification
  but competitive on streaming-telemetry, where its multi-resolution
  structure is best matched.

DATA REQUIREMENT (CRITICAL):
  This script needs REAL public benchmark data:
    [tabular]    UCI Adult (Census Income), arff or csv form
    [streaming]  a public smart-meter / wearable-sensor dataset
    [histogram]  a public query-log / trip-count dataset
  Set the three paths via env vars or CLI:
    --tabular   path/to/adult.csv
    --stream    path/to/telemetry.csv  (single numeric column per
                                        timestamp, sorted by time)
    --hist      path/to/histogram.csv  (categorical column with high
                                        cardinality)
  If any path is missing the script generates a SMOKE-TEST synthetic
  set with a LOUD warning -- the smoke result is NOT the bench
  verdict.  The verdict requires real data.

OUTPUTS:
  bench_results.jsonl -- one line per (dataset, method, knob, attacker,
                         utility) operating point
  bench_verdict.md    -- the pre-registered decision applied to
                         the frontier data

Copyright (c) 2026 Brayden Ross Sanders / 7SiTe LLC.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import random
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field, asdict
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Tuple

HERE = os.path.dirname(__file__)
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "Gen13", "targets"))

from foundations.lens_family import CHAIN_SUBMAGMAS  # noqa: E402
from ck_tables import BHML  # noqa: E402


# =====================================================================
# Pre-registered decision rule (DO NOT MODIFY)
# =====================================================================
PRE_REGISTERED = {
    "rule": "Pareto-touch-or-dominate on >=1 dataset at >=1 operating point",
    "datasets_required": 3,
    "real_data_required": True,
    "no_post_hoc_tuning": True,
    "honest_prior": "streaming-telemetry is the predicted win zone if any",
    "claim_under_test": "D-PRIV",
    "decision_irrevocable_once_run": True,
}


# =====================================================================
# Data adapters (REAL or SYNTHETIC-smoke)
# =====================================================================
_ADULT_COLUMNS = [
    "age", "workclass", "fnlwgt", "education", "education-num",
    "marital-status", "occupation", "relationship", "race", "sex",
    "capital-gain", "capital-loss", "hours-per-week", "native-country",
    "income",
]
# Quasi-identifiers per UCI Adult k-anonymity literature: age, race,
# sex, marital-status, native-country.  Sensitive: income.
_ADULT_QID = ["age", "race", "sex", "marital-status", "native-country"]
_ADULT_SENSITIVE = "income"


def load_tabular(path: Optional[str]) -> Tuple[List[List[str]], List[str], List[str], str]:
    """
    Returns (rows, quasi_id_cols, sensitive_col_name, source_note)
    Auto-detects UCI Adult format (no header, 15 comma-space columns).
    """
    if path and os.path.exists(path):
        rows: List[List[str]] = []
        is_adult = path.endswith("adult.data") or "adult" in path.lower()
        if is_adult:
            # UCI Adult: comma-space-separated, no header, 15 columns,
            # the last column is the sensitive (income) attribute.
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip().rstrip(".")
                    if not line:
                        continue
                    parts = [p.strip() for p in line.split(",")]
                    if len(parts) != 15:
                        continue
                    # Filter rows with missing values ("?")
                    if "?" in parts:
                        continue
                    # Bucket age into decades so QID matching is meaningful
                    try:
                        age = int(parts[0])
                        parts[0] = f"{(age // 10) * 10}s"
                    except ValueError:
                        continue
                    # Project to (QID-cols, sensitive)
                    qid_vals = [parts[_ADULT_COLUMNS.index(c)] for c in _ADULT_QID]
                    rows.append(qid_vals + [parts[_ADULT_COLUMNS.index(_ADULT_SENSITIVE)]])
            return rows, _ADULT_QID, _ADULT_SENSITIVE, f"real:{path} (UCI Adult)"
        # Generic CSV-with-header path
        with open(path, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = [r for r in reader if r and len(r) == len(header)]
        return rows, header[:-1], header[-1], f"real:{path}"
    return _synth_tabular()


def _synth_tabular() -> Tuple[List[List[str]], List[str], List[str], str]:
    """LOUD warning: synthetic smoke data."""
    print("[WARN] synthetic tabular data (no --tabular path); SMOKE TEST only", file=sys.stderr)
    rng = random.Random(42)
    rows = []
    for _ in range(2000):
        age = str(rng.randint(20, 80))
        edu = rng.choice(["HS", "BA", "MA", "PhD"])
        race = rng.choice(["W", "B", "A", "H", "O"])
        sex = rng.choice(["M", "F"])
        # sensitive: income > 50k roughly correlated with education
        prob = {"HS": 0.10, "BA": 0.30, "MA": 0.55, "PhD": 0.75}[edu]
        income = ">50K" if rng.random() < prob else "<=50K"
        rows.append([age, edu, race, sex, income])
    return rows, ["age", "education", "race", "sex"], "income", "synthetic:tabular_smoke"


def load_stream(path: Optional[str], max_rows: Optional[int] = None) -> Tuple[List[float], str]:
    """
    Load a numeric streaming dataset.  Auto-detects UCI Power
    Consumption format (semicolon-separated; first useful numeric is
    Global_active_power in column 3).
    """
    if path and os.path.exists(path):
        vals: List[float] = []
        is_power = "household_power" in path or "power_consumption" in path
        with open(path, "r", newline="", encoding="utf-8") as f:
            header = f.readline()  # discard header
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if is_power:
                    parts = line.split(";")
                    if len(parts) < 3:
                        continue
                    try:
                        vals.append(float(parts[2]))  # Global_active_power
                    except ValueError:
                        continue
                else:
                    try:
                        vals.append(float(line.split(",")[-1]))
                    except ValueError:
                        continue
                if max_rows is not None and len(vals) >= max_rows:
                    break
        return vals, f"real:{path}"
    return _synth_stream()


def _synth_stream() -> Tuple[List[float], str]:
    print("[WARN] synthetic streaming data (no --stream path); SMOKE TEST only", file=sys.stderr)
    rng = random.Random(43)
    vals = []
    base = 0.0
    for t in range(5000):
        # daily cycle + drift + noise + occasional events
        cyc = 5 * math.sin(2 * math.pi * t / 200)
        drift = 0.001 * t
        noise = rng.gauss(0, 1)
        event = 8.0 if (rng.random() < 0.01) else 0.0
        vals.append(base + cyc + drift + noise + event)
    return vals, "synthetic:stream_smoke"


def load_histogram(path: Optional[str], max_rows: Optional[int] = None) -> Tuple[List[str], str]:
    """
    Load a categorical histogram dataset.  Auto-detects UCI KOS
    bag-of-words format (3-line header: n_docs / vocab / nnz; then
    'docID wordID count' triples -- we expand to a flat list of word
    occurrences keyed by 'w{wordID}', so the cardinality and
    Zipf-distributed frequency are real).
    """
    if path and os.path.exists(path):
        items: List[str] = []
        is_kos = "docword" in path or "kos" in path.lower()
        with open(path, "r", encoding="utf-8") as f:
            if is_kos:
                # skip 3-line header
                _ = f.readline(); _ = f.readline(); _ = f.readline()
                for line in f:
                    parts = line.strip().split()
                    if len(parts) != 3:
                        continue
                    _, word_id, count = parts
                    try:
                        c = int(count)
                    except ValueError:
                        continue
                    items.extend([f"w{word_id}"] * min(c, 8))  # cap per-line repetition
                    if max_rows is not None and len(items) >= max_rows:
                        break
            else:
                for line in f:
                    t = line.strip()
                    if t:
                        items.append(t)
                    if max_rows is not None and len(items) >= max_rows:
                        break
        return items, f"real:{path}"
    return _synth_histogram()


def _synth_histogram() -> Tuple[List[str], str]:
    print("[WARN] synthetic histogram data (no --hist path); SMOKE TEST only", file=sys.stderr)
    rng = random.Random(44)
    # Zipf-ish distribution
    items = []
    for _ in range(5000):
        r = rng.random()
        if r < 0.3:
            items.append(f"q_{rng.randint(0, 9)}")
        elif r < 0.7:
            items.append(f"q_{rng.randint(0, 99)}")
        else:
            items.append(f"q_{rng.randint(0, 999)}")
    return items, "synthetic:histogram_smoke"


# =====================================================================
# Mechanisms
# =====================================================================

# --- RGD: D64 nested-resolution organizer, granted-depth knob ---------
def rgd_tabular(rows: List[List[str]], depth: int) -> List[List[str]]:
    """
    RGD on tabular: at depth d, expose values whose hash(value) % 10
    lies in the canonical D64 shell of size CHAIN_SUBMAGMAS[depth];
    suppress others to "*" (the wildcard).
    Higher depth -> larger shell -> more values pass through.
      d=1  shell={0}            -> ~10% of values exposed (max privacy)
      d=2  shell={0,7,8,9}      -> ~40%
      d=8  shell={0..9}         -> 100% (no privacy = full utility)
    Per-COLUMN shell is randomized so different columns suppress
    different value subsets (more realistic than global shell).
    """
    if depth < 1:
        depth = 1
    if depth > 8:
        depth = 8
    keymap = sorted(CHAIN_SUBMAGMAS.keys())
    target_size = keymap[min(depth - 1, len(keymap) - 1)]
    shell = sorted(CHAIN_SUBMAGMAS[target_size])
    shell_set = set(shell)
    out = []
    for row in rows:
        new_row = []
        for c, v in enumerate(row[:-1]):
            # use a column-salted hash so the shell partitions each
            # column's value-set independently
            h = (hash((c, v)) % 10 + 10) % 10
            if h in shell_set:
                new_row.append(v)  # PRESERVE the value
            else:
                new_row.append("*")
        new_row.append(row[-1])
        out.append(new_row)
    return out


def rgd_stream(vals: List[float], depth: int) -> List[float]:
    """RGD on streaming: depth-d sliding window mean of nested shell length."""
    if depth < 1:
        depth = 1
    if depth > 10:
        depth = 10
    keymap = sorted(CHAIN_SUBMAGMAS.keys())
    window = keymap[min(depth - 1, len(keymap) - 1)]
    out = []
    for i in range(len(vals)):
        start = max(0, i - window + 1)
        slice_ = vals[start: i + 1]
        out.append(sum(slice_) / len(slice_))
    return out


def rgd_histogram(items: List[str], depth: int) -> Counter:
    """
    RGD on histogram: at depth d, expose items whose hash(item) % 10
    lies in CHAIN_SUBMAGMAS[d]; suppress others under '*'.  Same
    suppress-style as rgd_tabular so attacker/utility compare against
    the SAME item-vocabulary (no schema mismatch).
    """
    if depth < 1:
        depth = 1
    if depth > 8:
        depth = 8
    keymap = sorted(CHAIN_SUBMAGMAS.keys())
    target_size = keymap[min(depth - 1, len(keymap) - 1)]
    shell = sorted(CHAIN_SUBMAGMAS[target_size])
    shell_set = set(shell)
    out: Counter = Counter()
    for v in items:
        h = (hash(v) % 10 + 10) % 10
        if h in shell_set:
            out[v] += 1
        else:
            out["*"] += 1
    return out


# --- e-DP: Laplace mechanism ------------------------------------------
def laplace(scale: float, rng: random.Random) -> float:
    u = rng.random() - 0.5
    return -scale * math.copysign(1.0, u) * math.log(1.0 - 2.0 * abs(u) + 1e-300)


def dp_tabular(rows: List[List[str]], epsilon: float, rng: random.Random) -> List[List[str]]:
    """DP on tabular: keep rows but randomly perturb each quasi-id column via Laplace-rounded indicators."""
    # collect value sets per column
    if not rows:
        return rows
    n_cols = len(rows[0]) - 1
    values = [list({r[c] for r in rows}) for c in range(n_cols)]
    out = []
    for row in rows:
        new_row = []
        for c in range(n_cols):
            true_idx = values[c].index(row[c])
            noisy_idx = int(round(true_idx + laplace(1.0 / max(epsilon, 1e-6), rng)))
            noisy_idx = max(0, min(len(values[c]) - 1, noisy_idx))
            new_row.append(values[c][noisy_idx])
        new_row.append(row[-1])
        out.append(new_row)
    return out


def dp_stream(vals: List[float], epsilon: float, rng: random.Random) -> List[float]:
    scale = 1.0 / max(epsilon, 1e-6)
    return [v + laplace(scale, rng) for v in vals]


def dp_histogram(items: List[str], epsilon: float, rng: random.Random) -> Counter:
    base: Counter = Counter(items)
    out: Counter = Counter()
    scale = 1.0 / max(epsilon, 1e-6)
    for k, v in base.items():
        out[k] = max(0.0, v + laplace(scale, rng))
    return out


# --- k-Anonymity: column generalization -------------------------------
def kanon_tabular(rows: List[List[str]], k: int) -> List[List[str]]:
    """Simple Mondrian-lite: partition by quasi-id prefix-bucket until groups >= k."""
    if not rows or k <= 1:
        return rows
    n_cols = len(rows[0]) - 1
    # group by full quasi-id; if any group < k, replace with "*" in last column
    groups: Dict[Tuple[str, ...], List[List[str]]] = defaultdict(list)
    for r in rows:
        groups[tuple(r[:n_cols])].append(r)
    out: List[List[str]] = []
    for qid, members in groups.items():
        if len(members) >= k:
            for r in members:
                out.append(list(r))
        else:
            # generalize: drop the rightmost column to "*"
            gen_qid = list(qid)
            for col in range(n_cols - 1, -1, -1):
                gen_qid[col] = "*"
                # re-bucket
                count = sum(1 for q in groups if all(
                    q[c] == gen_qid[c] or gen_qid[c] == "*" for c in range(n_cols)
                ))
                if count >= k:
                    break
            for r in members:
                out.append(gen_qid + [r[-1]])
    return out


# k-anon for stream / histogram = generalize equally
def kanon_stream(vals: List[float], k: int) -> List[float]:
    """Bin into k-sized bands of values."""
    if k <= 1 or not vals:
        return vals
    vmin, vmax = min(vals), max(vals)
    n_bands = max(2, len(vals) // max(k, 1))
    width = (vmax - vmin) / n_bands if vmax > vmin else 1.0
    out = []
    for v in vals:
        b = int((v - vmin) / width) if width > 0 else 0
        out.append(vmin + (b + 0.5) * width)
    return out


def kanon_histogram(items: List[str], k: int) -> Counter:
    base = Counter(items)
    out = Counter()
    for key, count in base.items():
        if count >= k:
            out[key] = count
        else:
            out["*"] += count
    return out


# =====================================================================
# Fixed attacker
# =====================================================================
def _qid_matches(priv_qid: Tuple[str, ...], orig_qid: Tuple[str, ...]) -> bool:
    """priv_qid matches orig_qid if every non-wildcard column equals."""
    for p, o in zip(priv_qid, orig_qid):
        if p != "*" and p != o:
            return False
    return True


def attacker_tabular(orig: List[List[str]], priv: List[List[str]]) -> float:
    """
    k-anonymity-style re-identification rate.  For each priv row,
    count how many orig rows are compatible with its QID (treating
    "*" as wildcard); attacker has 1/K probability per row.  Score
    = mean of 1/K across all priv rows.  Lower = better privacy.

    Optimization: pre-count orig QIDs in a hash table; exact lookups
    are O(1).  Wildcard lookups fall back to a full N-scan but only
    when "*" is present.
    """
    if not priv:
        return float("nan")
    orig_qid_counts: Dict[Tuple[str, ...], int] = defaultdict(int)
    for r in orig:
        orig_qid_counts[tuple(r[:-1])] += 1
    orig_qid_list = list(orig_qid_counts.keys())
    # Cache wildcard-lookup results so identical priv-QIDs reuse the count
    wild_cache: Dict[Tuple[str, ...], int] = {}
    total_p = 0.0
    for p in priv:
        qid_p = tuple(p[:-1])
        if "*" in qid_p:
            if qid_p in wild_cache:
                matches = wild_cache[qid_p]
            else:
                matches = sum(
                    orig_qid_counts[q] for q in orig_qid_list
                    if _qid_matches(qid_p, q)
                )
                wild_cache[qid_p] = matches
        else:
            matches = orig_qid_counts.get(qid_p, 0)
        if matches > 0:
            total_p += 1.0 / matches
    return total_p / max(len(priv), 1)


def attacker_stream(orig: List[float], priv: List[float]) -> float:
    """Reconstruction: 1 - normalized RMSE."""
    if len(orig) != len(priv):
        return float("nan")
    diffs = [(o - p) ** 2 for o, p in zip(orig, priv)]
    rmse = math.sqrt(sum(diffs) / max(len(diffs), 1))
    span = max(orig) - min(orig) if orig else 1.0
    if span == 0:
        return 0.0
    return max(0.0, 1.0 - rmse / span)


def attacker_histogram(orig: Counter, priv: Counter) -> float:
    """L1 closeness as proxy for reconstruction success."""
    total = sum(orig.values())
    if total == 0:
        return 0.0
    diff = 0.0
    for k in set(orig.keys()) | set(priv.keys()):
        diff += abs(orig[k] - priv[k])
    return max(0.0, 1.0 - diff / (2 * total))


# =====================================================================
# Utility
# =====================================================================
def utility_tabular(orig: List[List[str]], priv: List[List[str]]) -> float:
    """
    Predictive utility: train a majority-class predictor on priv
    (qid -> sensitive), evaluate accuracy on orig.  When priv-QID
    contains wildcards, match against orig via wildcard compatibility
    and take the wildest-compatible group's majority.  Compares to
    the overall priv majority baseline as the fallback.
    """
    if not priv:
        return 0.0
    # Group priv by QID -> sensitive distribution
    groups_priv: Dict[Tuple[str, ...], Counter] = defaultdict(Counter)
    overall: Counter = Counter()
    for r in priv:
        groups_priv[tuple(r[:-1])][r[-1]] += 1
        overall[r[-1]] += 1
    baseline_pred, _ = overall.most_common(1)[0] if overall else ("", 0)
    # If priv preserves QID values (RGD/k-anon style), we can match
    # orig QID directly OR via wildcard compatibility
    priv_qid_keys = list(groups_priv.keys())
    has_wild = any("*" in q for q in priv_qid_keys)
    correct = 0
    for r in orig:
        true = r[-1]
        qid = tuple(r[:-1])
        # exact match first
        if qid in groups_priv and groups_priv[qid]:
            pred, _ = groups_priv[qid].most_common(1)[0]
        elif has_wild:
            # search for compatible wildcarded priv groups
            combined: Counter = Counter()
            for pk, dist in groups_priv.items():
                if "*" in pk and _qid_matches(pk, qid):
                    combined.update(dist)
            if combined:
                pred, _ = combined.most_common(1)[0]
            else:
                pred = baseline_pred
        else:
            pred = baseline_pred
        if pred == true:
            correct += 1
    return correct / max(len(orig), 1)


def utility_stream(orig: List[float], priv: List[float]) -> float:
    """Anomaly preservation: correlation of |diff(orig)| with |diff(priv)|."""
    if len(orig) != len(priv) or len(orig) < 2:
        return 0.0
    da = [abs(orig[i] - orig[i - 1]) for i in range(1, len(orig))]
    dp = [abs(priv[i] - priv[i - 1]) for i in range(1, len(priv))]
    ma, mp = sum(da) / len(da), sum(dp) / len(dp)
    num = sum((a - ma) * (b - mp) for a, b in zip(da, dp))
    da_var = math.sqrt(sum((a - ma) ** 2 for a in da))
    dp_var = math.sqrt(sum((b - mp) ** 2 for b in dp))
    if da_var == 0 or dp_var == 0:
        return 0.0
    return max(0.0, num / (da_var * dp_var))


def utility_histogram(orig: Counter, priv: Counter) -> float:
    """Top-k overlap (k=10)."""
    top_o = {k for k, _ in orig.most_common(10)}
    top_p = {k for k, _ in priv.most_common(10)}
    if not top_o:
        return 0.0
    return len(top_o & top_p) / len(top_o)


# =====================================================================
# Frontier sweep
# =====================================================================
@dataclass
class Point:
    dataset: str
    method: str
    knob: str
    attacker_success: float
    utility: float
    source: str


def run_dataset(name: str, mode: str, data, knobs: Dict[str, List]) -> List[Point]:
    points: List[Point] = []
    rng = random.Random(1729)
    if mode == "tabular":
        orig, _, _, src = data
        # RGD
        for d in knobs["rgd"]:
            priv = rgd_tabular(orig, d)
            a = attacker_tabular(orig, priv)
            u = utility_tabular(orig, priv)
            points.append(Point(name, "RGD", f"d={d}", a, u, src))
        # DP
        for eps in knobs["dp"]:
            priv = dp_tabular(orig, eps, rng)
            a = attacker_tabular(orig, priv)
            u = utility_tabular(orig, priv)
            points.append(Point(name, "DP", f"eps={eps}", a, u, src))
        # k-anon
        for k in knobs["kanon"]:
            priv = kanon_tabular(orig, k)
            a = attacker_tabular(orig, priv)
            u = utility_tabular(orig, priv)
            points.append(Point(name, "k-anon", f"k={k}", a, u, src))
    elif mode == "stream":
        orig, src = data
        for d in knobs["rgd"]:
            priv = rgd_stream(orig, d)
            a = attacker_stream(orig, priv)
            u = utility_stream(orig, priv)
            points.append(Point(name, "RGD", f"d={d}", a, u, src))
        for eps in knobs["dp"]:
            priv = dp_stream(orig, eps, rng)
            a = attacker_stream(orig, priv)
            u = utility_stream(orig, priv)
            points.append(Point(name, "DP", f"eps={eps}", a, u, src))
        for k in knobs["kanon"]:
            priv = kanon_stream(orig, k)
            a = attacker_stream(orig, priv)
            u = utility_stream(orig, priv)
            points.append(Point(name, "k-anon", f"k={k}", a, u, src))
    elif mode == "histogram":
        items, src = data
        for d in knobs["rgd"]:
            priv = rgd_histogram(items, d)
            a = attacker_histogram(Counter(items), priv)
            u = utility_histogram(Counter(items), priv)
            points.append(Point(name, "RGD", f"d={d}", a, u, src))
        for eps in knobs["dp"]:
            priv = dp_histogram(items, eps, rng)
            a = attacker_histogram(Counter(items), priv)
            u = utility_histogram(Counter(items), priv)
            points.append(Point(name, "DP", f"eps={eps}", a, u, src))
        for k in knobs["kanon"]:
            priv = kanon_histogram(items, k)
            a = attacker_histogram(Counter(items), priv)
            u = utility_histogram(Counter(items), priv)
            points.append(Point(name, "k-anon", f"k={k}", a, u, src))
    return points


def pareto_frontier(points: List[Point]) -> List[Point]:
    """Privacy-utility frontier: low attacker_success + high utility = good.
       A point is Pareto-optimal if no other point in the same set has
       both lower attacker_success AND higher utility."""
    frontier: List[Point] = []
    for p in points:
        dominated = False
        for q in points:
            if q is p:
                continue
            if q.attacker_success <= p.attacker_success and q.utility >= p.utility and (
                q.attacker_success < p.attacker_success or q.utility > p.utility
            ):
                dominated = True
                break
        if not dominated:
            frontier.append(p)
    return frontier


def verdict(by_dataset: Dict[str, List[Point]]) -> Dict:
    """Apply the pre-registered decision rule."""
    dataset_verdicts = {}
    rgd_wins_anywhere = False
    for dataset, points in by_dataset.items():
        rgd_pts = [p for p in points if p.method == "RGD"]
        incumbent = [p for p in points if p.method in ("DP", "k-anon")]
        # frontier of incumbent
        incumbent_frontier = pareto_frontier(incumbent)
        # for each RGD point, ask: is it dominated by ALL incumbent points?
        rgd_pareto_wins = []
        for r in rgd_pts:
            dominated_by_any = False
            for q in incumbent_frontier:
                if q.attacker_success <= r.attacker_success and q.utility >= r.utility and (
                    q.attacker_success < r.attacker_success or q.utility > r.utility
                ):
                    dominated_by_any = True
                    break
            if not dominated_by_any:
                rgd_pareto_wins.append(r)
        won = len(rgd_pareto_wins) > 0
        rgd_wins_anywhere = rgd_wins_anywhere or won
        dataset_verdicts[dataset] = {
            "rgd_pareto_winning_points": [asdict(p) for p in rgd_pareto_wins],
            "rgd_won_or_tied": won,
        }
    return {
        "D_PRIV_CONFIRMED": rgd_wins_anywhere,
        "by_dataset": dataset_verdicts,
    }


# =====================================================================
# Main
# =====================================================================
def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description="RGD vs DP vs k-anon bench")
    parser.add_argument("--tabular", default=None)
    parser.add_argument("--stream", default=None)
    parser.add_argument("--hist", default=None)
    parser.add_argument("--out-jsonl", default="bench_results.jsonl")
    parser.add_argument("--out-md", default="bench_verdict.md")
    parser.add_argument("--max-rows", type=int, default=5000,
                        help="row cap per dataset for tractability (default 5000)")
    parser.add_argument("--max-hist-items", type=int, default=20000,
                        help="item cap for histogram (default 20000)")
    args = parser.parse_args(argv)

    print("=== BENCH -- RGD vs e-DP vs k-anonymity ===")
    print("    PRE-REGISTERED:", json.dumps(PRE_REGISTERED, indent=2))
    print(f"    sample caps: tabular={args.max_rows}, stream={args.max_rows}, "
          f"histogram={args.max_hist_items}")
    print()

    tabular = load_tabular(args.tabular)
    # Truncate tabular rows for tractability (~25M ops at 5000)
    if tabular[0] and len(tabular[0]) > args.max_rows:
        rows = tabular[0][:args.max_rows]
        tabular = (rows, tabular[1], tabular[2], tabular[3] + f" [first {args.max_rows} rows]")
    stream = load_stream(args.stream, max_rows=args.max_rows)
    hist = load_histogram(args.hist, max_rows=args.max_hist_items)

    real_data_count = sum(
        1 for src in [tabular[3], stream[1], hist[1]] if src.startswith("real:")
    )
    if real_data_count < 3:
        print(f"\n[!] WARNING: only {real_data_count}/3 datasets are REAL.")
        print("    The pre-registered bench requires 3 real datasets.")
        print("    This run produces SMOKE-TEST verdict only.\n")

    knobs = {
        "rgd": [1, 2, 3, 4, 5, 6],
        "dp": [0.1, 1.0, 10.0],
        "kanon": [5, 10, 25],
    }

    all_points: Dict[str, List[Point]] = {}
    all_points["tabular"] = run_dataset("tabular", "tabular", tabular, knobs)
    all_points["stream"] = run_dataset("stream", "stream", stream, knobs)
    all_points["histogram"] = run_dataset("histogram", "histogram", hist, knobs)

    # Print summary
    for ds_name, points in all_points.items():
        print(f"--- {ds_name} ---")
        for p in points:
            print(f"  {p.method:7s}  {p.knob:12s}  attacker_success={p.attacker_success:.4f}  utility={p.utility:.4f}")
        print()

    v = verdict(all_points)
    print("--- Decision (pre-registered rule) ---")
    print(f"D-PRIV confirmed: {v['D_PRIV_CONFIRMED']}")
    for ds_name, info in v["by_dataset"].items():
        wins = len(info["rgd_pareto_winning_points"])
        print(f"  {ds_name}: RGD Pareto-winning points = {wins}; rgd_won_or_tied = {info['rgd_won_or_tied']}")
    print()

    # Persist
    with open(args.out_jsonl, "w", encoding="utf-8") as f:
        for ds_name, points in all_points.items():
            for p in points:
                f.write(json.dumps(asdict(p)) + "\n")

    with open(args.out_md, "w", encoding="utf-8") as f:
        f.write("# Bench Verdict -- RGD vs e-DP vs k-anonymity\n\n")
        f.write(f"_Run at: {time.strftime('%Y-%m-%d %H:%M:%S')}_\n\n")
        f.write(f"**Real datasets used: {real_data_count}/3.**\n")
        if real_data_count < 3:
            f.write("> SMOKE-TEST verdict only.  Real-data run required for canon update.\n\n")
        f.write("## Pre-registered decision rule\n\n")
        f.write("```json\n" + json.dumps(PRE_REGISTERED, indent=2) + "\n```\n\n")
        f.write("## Verdict\n\n")
        f.write(f"**D-PRIV confirmed: {v['D_PRIV_CONFIRMED']}**\n\n")
        for ds_name, info in v["by_dataset"].items():
            wins = len(info["rgd_pareto_winning_points"])
            f.write(f"- **{ds_name}**: RGD Pareto-winning points = {wins}; "
                    f"`rgd_won_or_tied = {info['rgd_won_or_tied']}`\n")
        f.write("\n## Honest scope\n\n")
        if real_data_count < 3:
            f.write("This run was on SYNTHETIC smoke data; it cannot establish or retire D-PRIV.\n"
                    "To produce the bench-spec verdict, re-run with three REAL datasets via\n"
                    "--tabular / --stream / --hist.\n")
        else:
            f.write("Real-data run.  Pre-registered decision rule applied verbatim.\n"
                    "No post-hoc tuning permitted.\n")

    if real_data_count < 3:
        return 2  # smoke-only, not a real verdict
    return 0 if v["D_PRIV_CONFIRMED"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
