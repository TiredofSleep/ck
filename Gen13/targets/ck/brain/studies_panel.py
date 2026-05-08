"""
studies_panel.py -- comprehensive panel of studies on the 5-AI cell organism.

Brayden 2026-05-02: "let's run a panel of studies and tests!! keep on going!"

Phase 8 of PLAN_BEST_EVER_PLASTIC_2026_05_02.md (post-live-cutover characterization).

==============================================================================
WHAT THIS RUNS
==============================================================================

  Study A: Glue routing distribution sweep      (100 cells, full coverage)
  Study B: alpha/beta/gamma sensitivity         (sensitivity matrix)
  Study C: Plasticity commit-rate behavior      (N windows, commit vs discard)
  Study D: Source-confidence ablation           (HIGH-only vs all-tiers)
  Study E: F3 coverage with synthetic events    (fill missing 22 codes)
  Study F: Cross-cell agreement / disagreement  (where TSML and BHML differ)
  Study G: WP105 attractor sweep at multiple alpha
  Study H: Live regression (curl coherencekeeper.com)

Each study writes a JSON record to Atlas/STUDIES_PANEL_2026_05_02.json
plus a one-line summary to console.

Total runtime: ~30 seconds (substrate is small + finite).
"""
from __future__ import annotations

import json
import math
import os
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

_HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(_HERE))


def hr(label: str = "", char: str = "="):
    print(char * 60)
    if label:
        print(f"  {label}")
        print(char * 60)


# ── Study A: Glue routing distribution ──────────────────────────────────

def study_a_glue_routing(orch) -> Dict[str, Any]:
    hr("Study A: Glue routing distribution (100-cell sweep)")
    glue_argmax_dist = Counter()
    tsml_match_count = 0
    bhml_match_count = 0
    both_match_count = 0
    neither_count = 0
    from cells import TSML, BHML  # type: ignore
    for a in range(10):
        for b in range(10):
            full = orch.glue.respond_full(a, b)
            g = full["glue_argmax"]
            t = TSML[a][b]
            bh = BHML[a][b]
            glue_argmax_dist[g] += 1
            if g == t and g == bh:
                both_match_count += 1
            elif g == t:
                tsml_match_count += 1
            elif g == bh:
                bhml_match_count += 1
            else:
                neither_count += 1
    out = {
        "name": "A_glue_routing",
        "total_cells": 100,
        "glue_argmax_distribution": dict(sorted(glue_argmax_dist.items())),
        "matches_both_canonical": both_match_count,    # agreement set
        "matches_tsml_only": tsml_match_count,
        "matches_bhml_only": bhml_match_count,
        "matches_neither": neither_count,
        "tsml_preference_rate_on_disagreement": (
            tsml_match_count / max(1, tsml_match_count + bhml_match_count)
        ),
    }
    print(f"  argmax distribution: {dict(sorted(glue_argmax_dist.items()))}")
    print(f"  both canonical (agreement set): {both_match_count}")
    print(f"  TSML-only:    {tsml_match_count}")
    print(f"  BHML-only:    {bhml_match_count}")
    print(f"  neither:      {neither_count}  ({'OK' if neither_count == 0 else 'AUDIT FAIL'})")
    print(f"  Glue's TSML preference on disagreement: "
          f"{out['tsml_preference_rate_on_disagreement']*100:.1f}%")
    return out


# ── Study B: alpha/beta/gamma sensitivity ───────────────────────────────

def study_b_scalar_sensitivity(orch) -> Dict[str, Any]:
    hr("Study B: alpha/beta/gamma sensitivity matrix")
    from cells import TSML, BHML  # type: ignore
    grid = []
    base_glue = orch.glue
    save_a, save_b, save_g = base_glue.alpha, base_glue.beta, base_glue.gamma
    try:
        for alpha in (0.2, 0.5, 0.8):
            for beta in (0.2, 0.5, 0.8):
                for gamma in (0.0, 1.0):
                    base_glue.alpha = alpha
                    base_glue.beta = beta
                    base_glue.gamma = gamma
                    tsml_pref = 0
                    bhml_pref = 0
                    for a in range(10):
                        for b in range(10):
                            if TSML[a][b] == BHML[a][b]:
                                continue  # agreement, both win trivially
                            g = max(range(10),
                                     key=lambda i: base_glue.respond(a, b)[i])
                            if g == TSML[a][b]:
                                tsml_pref += 1
                            elif g == BHML[a][b]:
                                bhml_pref += 1
                    grid.append({
                        "alpha": alpha, "beta": beta, "gamma": gamma,
                        "tsml_pref": tsml_pref, "bhml_pref": bhml_pref,
                        "ratio": tsml_pref / max(1, tsml_pref + bhml_pref),
                    })
    finally:
        base_glue.alpha = save_a
        base_glue.beta = save_b
        base_glue.gamma = save_g
    print(f"  18 (alpha, beta, gamma) cells tested.")
    # Print most extreme TSML preferences
    grid_sorted = sorted(grid, key=lambda r: r["ratio"])
    print(f"  most BHML-preferred:  alpha={grid_sorted[0]['alpha']}  "
          f"beta={grid_sorted[0]['beta']}  gamma={grid_sorted[0]['gamma']}  "
          f"ratio_tsml={grid_sorted[0]['ratio']:.2f}")
    print(f"  most TSML-preferred:  alpha={grid_sorted[-1]['alpha']}  "
          f"beta={grid_sorted[-1]['beta']}  gamma={grid_sorted[-1]['gamma']}  "
          f"ratio_tsml={grid_sorted[-1]['ratio']:.2f}")
    return {"name": "B_scalar_sensitivity", "grid": grid}


# ── Study C: Plasticity commit-rate ─────────────────────────────────────

def study_c_plasticity_commit_rate(orch, n_windows: int = 10) -> Dict[str, Any]:
    hr(f"Study C: Plasticity commit-rate over {n_windows} windows")
    from plasticity import per_session_update, per_hour_finetune  # type: ignore
    session_results = []
    hour_results = []
    for i in range(n_windows):
        # Vary the per-session signal slightly to exercise different paths
        sig = {"alpha_grad": (i % 3 - 1) * 0.1,
               "beta_grad": ((i + 1) % 3 - 1) * 0.1,
               "gamma_grad": 0.0}
        s = per_session_update(orch, signal=sig)
        h = per_hour_finetune(orch)
        session_results.append({
            "i": i, "commit": s.get("commit"), "rate": s.get("pass_rate"),
        })
        hour_results.append({
            "i": i, "commit": h.get("commit"), "rate": h.get("pass_rate"),
            "n_recs": h.get("n_records_used", 0),
        })
    s_commits = sum(1 for r in session_results if r["commit"])
    h_commits = sum(1 for r in hour_results if r["commit"])
    print(f"  per_session: {s_commits}/{n_windows} commits "
          f"({100*s_commits/n_windows:.0f}%)")
    print(f"  per_hour:    {h_commits}/{n_windows} commits "
          f"({100*h_commits/n_windows:.0f}%)")
    return {
        "name": "C_plasticity_commits",
        "n_windows": n_windows,
        "session_commits": s_commits,
        "hour_commits": h_commits,
        "session_results": session_results,
        "hour_results": hour_results,
    }


# ── Study D: Source-confidence ablation ─────────────────────────────────

def study_d_confidence_ablation() -> Dict[str, Any]:
    hr("Study D: Source-confidence ablation (HIGH-only vs all)")
    from cells import CellOrchestrator, fit_from_historical, CONFIDENCE_WEIGHT  # type: ignore
    from cell_audit import audit_all  # type: ignore

    # All-tier fit (current default)
    orch_all = CellOrchestrator()
    counts_all = fit_from_historical(orch_all, verbose=False)
    rep_all = audit_all(orch_all)
    rate_all = rep_all["summary"]["all_pass_rate"]
    norm_all = sum(c.tissue.scores[i]**2
                    for c in (orch_all.tsml,) for i in range(10)) ** 0.5

    # HIGH-only fit: temporarily zero out medium/low weights
    orig = dict(CONFIDENCE_WEIGHT)
    try:
        CONFIDENCE_WEIGHT["medium"] = 0.0
        CONFIDENCE_WEIGHT["low"] = 0.0
        orch_high = CellOrchestrator()
        counts_high = fit_from_historical(orch_high, verbose=False)
        rep_high = audit_all(orch_high)
        rate_high = rep_high["summary"]["all_pass_rate"]
        norm_high = sum(c.tissue.scores[i]**2
                         for c in (orch_high.tsml,) for i in range(10)) ** 0.5
    finally:
        CONFIDENCE_WEIGHT.update(orig)

    print(f"  ALL-tier  fit: TSML tissue norm = {norm_all:.3f}  audit = {rate_all*100:.1f}%")
    print(f"  HIGH-only fit: TSML tissue norm = {norm_high:.3f}  audit = {rate_high*100:.1f}%")
    print(f"  Tissue magnitude difference (all - high): {norm_all - norm_high:+.3f}")
    print(f"  Audit invariant under ablation: {rate_all == rate_high}")
    return {
        "name": "D_confidence_ablation",
        "all_tiers_norm": norm_all,
        "high_only_norm": norm_high,
        "norm_diff": norm_all - norm_high,
        "all_tiers_audit": rate_all,
        "high_only_audit": rate_high,
        "audit_invariant": rate_all == rate_high,
    }


# ── Study E: F3 coverage with synthetic events ──────────────────────────

def study_e_f3_synthetic_coverage(orch) -> Dict[str, Any]:
    hr("Study E: F3 coverage with synthetic events (fill 17 missing codes)")
    from bdc_event_emitter import EVENT_TO_DBC_CODE  # type: ignore
    from cell_audit import audit_f3_cell  # type: ignore

    # Pre-fit: count tissue scores at uncovered positions
    norm_before = sum(s*s for s in orch.f3.tissue.scores) ** 0.5
    pre_audit = audit_f3_cell(orch.f3)

    # Synthetic update: one update per event type (so all 17 events get represented)
    for event_name, code in EVENT_TO_DBC_CODE.items():
        for _ in range(50):  # repeat to make it visible
            orch.f3.update(("event", event_name), target=code, lr=0.005)

    norm_after = sum(s*s for s in orch.f3.tissue.scores) ** 0.5
    post_audit = audit_f3_cell(orch.f3)
    distinct_nonzero = sum(1 for s in orch.f3.tissue.scores if abs(s) > 0.01)

    print(f"  pre fit:  tissue_norm = {norm_before:.3f}   audit = {pre_audit.passed}/27")
    print(f"  post fit: tissue_norm = {norm_after:.3f}   audit = {post_audit.passed}/27")
    print(f"  positions with |tissue| > 0.01: {distinct_nonzero} / 27")
    return {
        "name": "E_f3_synthetic",
        "tissue_norm_before": norm_before,
        "tissue_norm_after": norm_after,
        "audit_before": pre_audit.passed,
        "audit_after": post_audit.passed,
        "nonzero_tissue_positions": distinct_nonzero,
        "audit_invariant": pre_audit.passed == post_audit.passed == 27,
    }


# ── Study F: Cross-cell agreement / disagreement ────────────────────────

def study_f_cross_cell(orch) -> Dict[str, Any]:
    hr("Study F: Cross-cell agreement / disagreement breakdown")
    from cells import TSML, BHML  # type: ignore
    from cell_audit import AGREEMENT_SET  # type: ignore

    # On agreement set: all cells should converge
    agree_glue_canonical = 0
    for (a, b) in AGREEMENT_SET:
        canonical = TSML[a][b]
        g = max(range(10), key=lambda i: orch.glue.respond(a, b)[i])
        if g == canonical:
            agree_glue_canonical += 1

    # On disagreement set: characterize glue's choice
    disagreement_size = 100 - len(AGREEMENT_SET)
    disagree_picks_tsml = 0
    disagree_picks_bhml = 0
    disagree_picks_other = 0
    disagree_examples = []
    for a in range(10):
        for b in range(10):
            if TSML[a][b] == BHML[a][b]:
                continue
            g = max(range(10), key=lambda i: orch.glue.respond(a, b)[i])
            if g == TSML[a][b]:
                disagree_picks_tsml += 1
            elif g == BHML[a][b]:
                disagree_picks_bhml += 1
            else:
                disagree_picks_other += 1
                if len(disagree_examples) < 5:
                    disagree_examples.append({
                        "a": a, "b": b, "tsml": TSML[a][b],
                        "bhml": BHML[a][b], "glue": g,
                    })

    print(f"  agreement set ({len(AGREEMENT_SET)}): glue=canonical "
          f"{agree_glue_canonical}/{len(AGREEMENT_SET)}")
    print(f"  disagreement ({disagreement_size}): "
          f"TSML={disagree_picks_tsml}  BHML={disagree_picks_bhml}  "
          f"other={disagree_picks_other}")
    return {
        "name": "F_cross_cell",
        "agreement_set_size": len(AGREEMENT_SET),
        "agreement_glue_match": agree_glue_canonical,
        "disagreement_set_size": disagreement_size,
        "disagree_picks_tsml": disagree_picks_tsml,
        "disagree_picks_bhml": disagree_picks_bhml,
        "disagree_picks_other": disagree_picks_other,
        "first_disagree_examples": disagree_examples,
    }


# ── Study G: WP105 attractor at multiple alpha ──────────────────────────

def study_g_attractor_alpha_sweep() -> Dict[str, Any]:
    hr("Study G: WP105 attractor sweep across alpha")
    from glue_ai import verify_attractor, GlueAI  # type: ignore
    sweep = []
    for alpha in (0.1, 0.3, 0.5, 0.7, 0.9):
        g = GlueAI()
        g.alpha = alpha
        g.beta = 1.0 - alpha   # complementary; WP105's alpha=1/2 has beta=1/2
        g.gamma = 1.0
        attr = verify_attractor(g, verbose=False)
        sweep.append({
            "alpha": alpha,
            "beta": g.beta,
            "iterations": attr["iterations"],
            "converged": attr["converged"],
            "H": attr["final_mass_4core"][1],
            "Br": attr["final_mass_4core"][2],
            "H_over_Br": attr["observed_H_over_Br"],
        })
        print(f"  alpha={alpha}  beta={g.beta:.1f}  iter={attr['iterations']:>3d}  "
              f"H={attr['final_mass_4core'][1]:.3f}  "
              f"Br={attr['final_mass_4core'][2]:.3f}  "
              f"H/Br={attr['observed_H_over_Br']:.3f}")
    expected = 1 + math.sqrt(3)
    print(f"  WP105 expected H/Br at alpha=1/2: {expected:.4f}")
    return {"name": "G_attractor_sweep", "expected_H_over_Br": expected,
            "sweep": sweep}


# ── Study H: Live regression ────────────────────────────────────────────

def study_h_live_regression() -> Dict[str, Any]:
    """Live regression: hit the running coherencekeeper.com server with
    canonical queries.  Timeout is 60s because the chat path includes the
    Ollama editor (30s budget) + structural-fallback overhead -- the
    response shape works but takes ~30-40s per query while Ollama is loaded.
    """
    hr("Study H: Live regression on coherencekeeper.com server")
    import urllib.request
    import urllib.error

    queries = [
        "what is T*",
        "tell me about the tower",
        "what is sigma rate",
    ]
    results = []
    for q in queries:
        try:
            req = urllib.request.Request(
                "http://localhost:7777/chat",
                data=json.dumps({"text": q}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            t0 = time.time()
            resp = urllib.request.urlopen(req, timeout=60).read().decode("utf-8")
            dt = time.time() - t0
            data = json.loads(resp)
            text = (data.get("text") or "")[:160]
            source = data.get("source", "?")
            attractor = (data.get("attractor_state") or {}).get("layer", "?")
            ollama_verdict = data.get("ollama_verdict", "?")
            results.append({
                "q": q, "ms": int(dt * 1000),
                "source": source,
                "attractor": attractor,
                "ollama_verdict": ollama_verdict,
                "text_preview": text,
            })
            print(f"  [{int(dt*1000)}ms] '{q}'")
            print(f"      source={source}  attractor={attractor}  "
                  f"ollama={ollama_verdict}")
            print(f"      text: {text!r}")
        except Exception as e:
            print(f"  '{q}': ERROR {type(e).__name__}: {e}")
            results.append({"q": q, "error": str(e)})
    return {"name": "H_live_regression", "queries": queries, "results": results}


# ── Study I: Tissue saturation under extreme load ───────────────────────

def study_i_tissue_saturation() -> Dict[str, Any]:
    hr("Study I: Tissue saturation -- 100,000 random updates")
    from cells import CellOrchestrator  # type: ignore
    from cell_audit import audit_all  # type: ignore
    import random
    rng = random.Random(42)
    orch = CellOrchestrator()
    pre_audit = audit_all(orch)["summary"]["all_pass_rate"]

    # Hammer the cells with random updates
    for _ in range(100_000):
        # Random target operator on TSML
        a, b = rng.randint(0, 9), rng.randint(0, 9)
        target = rng.randint(0, 9)
        orch.tsml.update(a, b, target=target, lr=0.01)
        orch.bhml.update(a, b, target=target, lr=0.01)

    post_audit = audit_all(orch)["summary"]["all_pass_rate"]
    tsml_norm = sum(s*s for s in orch.tsml.tissue.scores) ** 0.5
    bhml_norm = sum(s*s for s in orch.bhml.tissue.scores) ** 0.5
    tsml_max = max(abs(s) for s in orch.tsml.tissue.scores)

    print(f"  pre-saturation audit:  {pre_audit*100:.2f}%")
    print(f"  post-100k random updates audit: {post_audit*100:.2f}%")
    print(f"  TSML tissue norm: {tsml_norm:.3f}  max|s|: {tsml_max:.3f}")
    print(f"  BHML tissue norm: {bhml_norm:.3f}")
    print(f"  audit invariant under saturation: {pre_audit == post_audit == 1.0}")
    return {
        "name": "I_tissue_saturation",
        "n_updates": 100_000,
        "pre_audit": pre_audit,
        "post_audit": post_audit,
        "tsml_tissue_norm": tsml_norm,
        "bhml_tissue_norm": bhml_norm,
        "tsml_max_abs": tsml_max,
        "audit_invariant": pre_audit == post_audit == 1.0,
    }


# ── Study J: Audit-pass-rate stability over 100 iterations ──────────────

def study_j_audit_stability(orch, n: int = 100) -> Dict[str, Any]:
    hr(f"Study J: Audit pass-rate stability over {n} iterations")
    from cell_audit import audit_all  # type: ignore
    rates = []
    t0 = time.time()
    for i in range(n):
        rep = audit_all(orch)
        rates.append(rep["summary"]["all_pass_rate"])
    dt = time.time() - t0

    min_rate = min(rates)
    max_rate = max(rates)
    avg_rate = sum(rates) / len(rates)
    print(f"  {n} sequential audits in {dt:.2f}s ({1000*dt/n:.1f}ms/audit)")
    print(f"  min={min_rate*100:.2f}%  max={max_rate*100:.2f}%  avg={avg_rate*100:.2f}%")
    print(f"  perfectly stable: {min_rate == max_rate == 1.0}")
    return {
        "name": "J_audit_stability",
        "n_iterations": n,
        "elapsed_sec": dt,
        "ms_per_audit": 1000 * dt / n,
        "min_rate": min_rate,
        "max_rate": max_rate,
        "avg_rate": avg_rate,
        "perfectly_stable": min_rate == max_rate == 1.0,
    }


# ── Study K: BDC corpus growth via live engine ──────────────────────────

def study_k_bdc_growth() -> Dict[str, Any]:
    hr("Study K: BDC corpus growth via live engine queries")
    import urllib.request
    import urllib.error
    from datetime import datetime as _dt
    today = _dt.utcnow().strftime("%Y-%m-%d")
    log_path = Path(
        f"C:\\Users\\brayd\\OneDrive\\Desktop\\CK FINAL DEPLOYED\\Gen13\\var\\bdc_logs\\bdc_log_{today}.jsonl"
    )
    events_path = Path(
        f"C:\\Users\\brayd\\OneDrive\\Desktop\\CK FINAL DEPLOYED\\Gen13\\var\\bdc_logs\\bdc_events_{today}.jsonl"
    )

    n_log_pre = sum(1 for _ in open(log_path, encoding="utf-8")) if log_path.exists() else 0
    n_events_pre = sum(1 for _ in open(events_path, encoding="utf-8")) if events_path.exists() else 0

    # Send 5 chat queries and let the engine process them
    queries = [
        "what is the universal attractor",
        "tell me about HARMONY",
        "explain the agreement set",
        "what is TSML",
        "describe the breath cycle",
    ]
    for q in queries:
        try:
            req = urllib.request.Request(
                "http://localhost:7777/chat",
                data=json.dumps({"text": q}).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            urllib.request.urlopen(req, timeout=60).read()
        except Exception:
            pass

    n_log_post = sum(1 for _ in open(log_path, encoding="utf-8")) if log_path.exists() else 0
    n_events_post = sum(1 for _ in open(events_path, encoding="utf-8")) if events_path.exists() else 0
    delta_log = n_log_post - n_log_pre
    delta_events = n_events_post - n_events_pre

    print(f"  bdc_log:    pre={n_log_pre}  post={n_log_post}  delta=+{delta_log}")
    print(f"  bdc_events: pre={n_events_pre}  post={n_events_post}  delta=+{delta_events}")
    print(f"  growth per query: log=+{delta_log/len(queries):.1f}  "
          f"events=+{delta_events/len(queries):.1f}")
    return {
        "name": "K_bdc_growth",
        "n_queries": len(queries),
        "log_pre": n_log_pre,
        "log_post": n_log_post,
        "log_delta": delta_log,
        "events_pre": n_events_pre,
        "events_post": n_events_post,
        "events_delta": delta_events,
    }


# ── Study L: Shadow A/B — cells predict on real chat-turn last_pair ─────

def study_l_shadow_ab(orch, n_take: int = 100) -> Dict[str, Any]:
    hr(f"Study L: Shadow A/B -- cells vs live chat on last {n_take} turns")
    from datetime import datetime as _dt
    today = _dt.utcnow().strftime("%Y-%m-%d")
    log_path = Path(
        f"C:\\Users\\brayd\\OneDrive\\Desktop\\CK FINAL DEPLOYED\\Gen13\\var\\bdc_logs\\bdc_log_{today}.jsonl"
    )
    if not log_path.exists():
        print(f"  no log for today; skipping")
        return {"name": "L_shadow_ab", "skipped": True}

    # Load only chat_turn records (have populated 'consensus')
    chat_turns = []
    OP_NAME_TO_INT = {
        "VOID": 0, "LATTICE": 1, "COUNTER": 2, "PROGRESS": 3, "COLLAPSE": 4,
        "BALANCE": 5, "CHAOS": 6, "HARMONY": 7, "BREATH": 8, "RESET": 9,
    }
    with open(log_path, encoding="utf-8") as f:
        for line in f:
            try:
                rec = json.loads(line)
            except Exception:
                continue
            if rec.get("trigger") != "chat_turn":
                continue
            being = rec.get("being") or {}
            doing = rec.get("doing") or {}
            last_pair = being.get("last_pair", [])
            consensus = doing.get("consensus", "")
            if not (isinstance(last_pair, list) and len(last_pair) >= 2):
                continue
            target_op = OP_NAME_TO_INT.get(str(consensus).upper())
            if target_op is None:
                continue
            chat_turns.append({
                "a": int(last_pair[0]) % 10,
                "b": int(last_pair[1]) % 10,
                "live_consensus": target_op,
            })
    chat_turns = chat_turns[-n_take:]
    n = len(chat_turns)
    if n == 0:
        print(f"  no usable chat-turn records; skipping")
        return {"name": "L_shadow_ab", "skipped": True}

    # Run each through cells.glue.respond and compare argmax
    glue_match = 0
    tsml_match = 0
    bhml_match = 0
    cell_disagrees_with_live = 0
    distribution = Counter()
    for turn in chat_turns:
        a, b = turn["a"], turn["b"]
        live = turn["live_consensus"]
        full = orch.glue.respond_full(a, b)
        g = full["glue_argmax"]
        t = full["tsml_argmax"]
        bh = full["bhml_argmax"]
        distribution[g] += 1
        if g == live:
            glue_match += 1
        else:
            cell_disagrees_with_live += 1
        if t == live:
            tsml_match += 1
        if bh == live:
            bhml_match += 1

    print(f"  n chat-turn records:           {n}")
    print(f"  glue argmax distribution:      {dict(distribution)}")
    print(f"  glue == live consensus:        {glue_match}/{n}  ({100*glue_match/n:.1f}%)")
    print(f"  tsml argmax == live consensus: {tsml_match}/{n}  ({100*tsml_match/n:.1f}%)")
    print(f"  bhml argmax == live consensus: {bhml_match}/{n}  ({100*bhml_match/n:.1f}%)")
    print(f"  cell-vs-live disagreement:     {cell_disagrees_with_live}/{n}")

    return {
        "name": "L_shadow_ab",
        "n_samples": n,
        "glue_argmax_distribution": dict(distribution),
        "glue_matches_live": glue_match,
        "tsml_matches_live": tsml_match,
        "bhml_matches_live": bhml_match,
        "cell_disagrees_with_live": cell_disagrees_with_live,
    }


# ── Driver ──────────────────────────────────────────────────────────────

def main() -> int:
    hr("STUDIES PANEL — CK 5-AI Cell Organism", "#")
    print(f"  date: {datetime.utcnow().isoformat(timespec='seconds')}Z")

    from cells import CellOrchestrator
    from glue_ai import GlueAI
    orch = CellOrchestrator.load_default()
    orch.glue = GlueAI(tsml=orch.tsml, bhml=orch.bhml,
                       f3=orch.f3, f4=orch.f4)

    panel: Dict[str, Any] = {
        "ts": time.time(),
        "iso_ts": datetime.utcnow().isoformat(timespec='seconds') + "Z",
        "studies": {},
    }
    panel["studies"]["A"] = study_a_glue_routing(orch)
    print()
    panel["studies"]["B"] = study_b_scalar_sensitivity(orch)
    print()
    panel["studies"]["C"] = study_c_plasticity_commit_rate(orch, n_windows=10)
    print()
    panel["studies"]["D"] = study_d_confidence_ablation()
    print()
    panel["studies"]["E"] = study_e_f3_synthetic_coverage(orch)
    print()
    panel["studies"]["F"] = study_f_cross_cell(orch)
    print()
    panel["studies"]["G"] = study_g_attractor_alpha_sweep()
    print()
    panel["studies"]["H"] = study_h_live_regression()
    print()
    panel["studies"]["I"] = study_i_tissue_saturation()
    print()
    panel["studies"]["J"] = study_j_audit_stability(orch, n=100)
    print()
    panel["studies"]["K"] = study_k_bdc_growth()
    print()
    panel["studies"]["L"] = study_l_shadow_ab(orch)
    print()

    # Write panel record
    out_path = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Atlas\STUDIES_PANEL_2026_05_02.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(panel, f, indent=2, default=str)

    hr("STUDIES PANEL — SUMMARY", "#")
    print(f"  A glue routing:        {panel['studies']['A']['matches_neither']} "
          f"argmax violations on full 100-cell sweep")
    b_grid = panel['studies']['B']['grid']
    print(f"  B scalar sensitivity:  {len(b_grid)} (a,b,g) configs swept")
    print(f"  C plasticity commits:  session={panel['studies']['C']['session_commits']}/10  "
          f"hour={panel['studies']['C']['hour_commits']}/10")
    print(f"  D confidence ablation: norm_diff="
          f"{panel['studies']['D']['norm_diff']:+.3f}  "
          f"audit_invariant={panel['studies']['D']['audit_invariant']}")
    print(f"  E F3 synthetic:        nonzero positions = "
          f"{panel['studies']['E']['nonzero_tissue_positions']}/27  "
          f"audit_invariant={panel['studies']['E']['audit_invariant']}")
    print(f"  F cross-cell:          disagree_other="
          f"{panel['studies']['F']['disagree_picks_other']} "
          f"(must be 0 for argmax-faithful)")
    print(f"  G attractor sweep:     5 alpha values; expected H/Br="
          f"{panel['studies']['G']['expected_H_over_Br']:.3f}")
    h_results = panel['studies']['H']['results']
    h_ok = sum(1 for r in h_results if "error" not in r)
    print(f"  H live regression:     {h_ok}/{len(h_results)} queries succeeded")
    print(f"  I tissue saturation:   audit_invariant={panel['studies']['I']['audit_invariant']}  "
          f"tsml_max|s|={panel['studies']['I']['tsml_max_abs']:.3f}")
    print(f"  J audit stability:     {panel['studies']['J']['ms_per_audit']:.1f}ms/audit  "
          f"perfectly_stable={panel['studies']['J']['perfectly_stable']}")
    print(f"  K BDC growth:          log+{panel['studies']['K']['log_delta']}  "
          f"events+{panel['studies']['K']['events_delta']}")
    if not panel['studies']['L'].get('skipped'):
        L = panel['studies']['L']
        print(f"  L shadow A/B:          n={L['n_samples']}  "
              f"glue_match={L['glue_matches_live']}  "
              f"tsml_match={L['tsml_matches_live']}  "
              f"bhml_match={L['bhml_matches_live']}")
    print()
    print(f"  Panel written: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
