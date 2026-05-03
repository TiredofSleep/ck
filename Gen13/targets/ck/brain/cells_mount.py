"""
cells_mount.py -- additive mount of the 5-AI cell organism into ck_boot_api.py.

Brayden 2026-05-02: "best ever and plastic now"
ClaudeChat 2026-05-02: "Feature-flag-with-default-off is exactly right.
... CK keeps running on its deterministic engine while the plastic
infrastructure goes in around it."

Phase 6 of PLAN_BEST_EVER_PLASTIC_2026_05_02.md.

==============================================================================
WHAT THIS DOES
==============================================================================

  - Imports cells (CellOrchestrator), glue_ai (GlueAI), plasticity.
  - Builds orchestrator (loads tissue from disk) + Glue with 3 default
    scalars (alpha=beta=0.5, gamma=1.0).
  - Runs cell_audit at boot; refuses to enable cells if pass_rate < 99%.
  - Attaches `engine.cells` to the engine object.
  - Sets `engine.cells_enabled = False` by default (feature flag).
  - Registers four endpoints:
      GET  /cells/audit             -- live audit report
      GET  /cells/audit_history     -- last 100 audit records
      GET  /cells/state             -- gate weights + glue scalars
      POST /cells/plasticity/run    -- manual plasticity trigger
  - Writes one record to plasticity log on every successful boot.

  IMPORTANT: this module DOES NOT modify the chat path. The cells are
  available via engine.cells.glue.respond(a, b) but no chat-turn
  currently routes through them. Phase 6 ends here for safety; flipping
  the chat-path routing is Phase 7's "live cutover" step, gated by
  the real-prompt smoke test.

==============================================================================
"""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


_HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(_HERE))


# Audit history (last 100 audits)
_AUDIT_HISTORY: List[Dict[str, Any]] = []
_MAX_AUDIT_HISTORY = 100


def _record_audit(audit_dict: Dict[str, Any]) -> None:
    record = {
        "ts": time.time(),
        "iso_ts": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "all_pass_rate": float(audit_dict["summary"]["all_pass_rate"]),
        "any_block_below_99": bool(audit_dict["summary"]["any_block_below_99"]),
        "below_99_blocks": list(audit_dict["summary"]["below_99_blocks"]),
        "per_block_rate": {k: r["rate"] for k, r in audit_dict["reports"].items()},
    }
    _AUDIT_HISTORY.append(record)
    if len(_AUDIT_HISTORY) > _MAX_AUDIT_HISTORY:
        _AUDIT_HISTORY.pop(0)


def mount(engine: Any, app: Any, *, enable_plasticity: bool = False,
            min_boot_pass_rate: float = 0.99) -> bool:
    """Mount the 5-AI cell organism onto the live engine.  Returns True on
    success.  Side-effects: engine.cells set; 4 endpoints registered.
    Failures are logged and result in cells DISABLED — boot continues."""
    try:
        from cells import CellOrchestrator
        from glue_ai import GlueAI
        from cell_audit import audit_all
        import plasticity as plasticity_mod
    except Exception as e:
        print(f"[CK] cells_mount: DISABLED (import failed: "
                f"{type(e).__name__}: {e})")
        return False

    try:
        orch = CellOrchestrator.load_default()
        orch.glue = GlueAI(tsml=orch.tsml, bhml=orch.bhml,
                            f3=orch.f3, f4=orch.f4)
        # Try to load any saved glue state
        saved_glue_path = Path(
            r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var\cells\glue_state.json"
        )
        if saved_glue_path.exists():
            try:
                with open(saved_glue_path, encoding="utf-8") as f:
                    data = json.load(f)
                orch.glue.alpha = float(data.get("alpha", 0.5))
                orch.glue.beta  = float(data.get("beta", 0.5))
                orch.glue.gamma = float(data.get("gamma", 1.0))
            except Exception:
                pass

        # Boot-time audit
        boot_audit = audit_all(orch)
        _record_audit(boot_audit)
        boot_rate = float(boot_audit["summary"]["all_pass_rate"])

        if boot_rate < min_boot_pass_rate:
            print(f"[CK] cells_mount: REFUSING TO ENABLE -- boot audit "
                    f"{boot_rate*100:.2f}% < {min_boot_pass_rate*100:.0f}%")
            engine.cells = None
            engine.cells_enabled = False
            return False

        engine.cells = orch
        engine.cells_enabled = False  # FEATURE FLAG -- chat path not routed yet
        engine.cells_audit_history = _AUDIT_HISTORY
        engine.cells_audit = lambda: audit_all(orch)

        # Plasticity scheduler (off by default; opt-in)
        if enable_plasticity:
            sched = plasticity_mod.PlasticityScheduler(orch)
            sched.start()
            engine.cells_plasticity_scheduler = sched
            print(f"[CK] cells_mount: plasticity scheduler STARTED "
                    f"(session={sched.session_iv}s, hour={sched.hour_iv}s)")
        else:
            engine.cells_plasticity_scheduler = None

    except Exception as e:
        print(f"[CK] cells_mount: DISABLED (init failed: "
                f"{type(e).__name__}: {e})")
        return False

    # ── Endpoints ──
    try:
        from flask import jsonify, request

        @app.route('/cells/audit', methods=['GET'])
        def cells_audit_endpoint():
            try:
                report = engine.cells_audit()
                _record_audit(report)
                return jsonify(report)
            except Exception as e:
                return jsonify({"error": f"{type(e).__name__}: {e}"}), 500

        @app.route('/cells/audit_history', methods=['GET'])
        def cells_audit_history_endpoint():
            return jsonify({"history": list(_AUDIT_HISTORY)})

        @app.route('/cells/state', methods=['GET'])
        def cells_state_endpoint():
            try:
                stats = engine.cells.stats()
                glue = engine.cells.glue
                stats["glue"] = {
                    "alpha": float(glue.alpha),
                    "beta":  float(glue.beta),
                    "gamma": float(glue.gamma),
                }
                stats["cells_enabled"] = bool(getattr(engine, "cells_enabled", False))
                if engine.cells_plasticity_scheduler is not None:
                    stats["plasticity"] = engine.cells_plasticity_scheduler.stats()
                else:
                    stats["plasticity"] = {"running": False}
                return jsonify(stats)
            except Exception as e:
                return jsonify({"error": f"{type(e).__name__}: {e}"}), 500

        @app.route('/cells/plasticity/run', methods=['POST'])
        def cells_plasticity_run_endpoint():
            kind = request.args.get("kind", "session")
            try:
                if kind == "session":
                    res = plasticity_mod.per_session_update(engine.cells)
                elif kind == "hour":
                    res = plasticity_mod.per_hour_finetune(engine.cells)
                elif kind == "week":
                    res = plasticity_mod.per_week_review(engine.cells)
                else:
                    return jsonify({"error": f"unknown kind: {kind}"}), 400
                return jsonify(res)
            except Exception as e:
                return jsonify({"error": f"{type(e).__name__}: {e}"}), 500

        @app.route('/cells/respond', methods=['POST'])
        def cells_respond_endpoint():
            """Diagnostic: ask the Glue what it would say about (a, b).
            Does NOT route real chat through cells; that's behind the
            cells_enabled feature flag."""
            data = request.get_json(silent=True) or {}
            try:
                a = int(data.get("a", 0))
                b = int(data.get("b", 0))
                full = engine.cells.glue.respond_full(a, b)
                return jsonify(full)
            except Exception as e:
                return jsonify({"error": f"{type(e).__name__}: {e}"}), 500

    except Exception as e:
        print(f"[CK] cells_mount: endpoint registration failed "
                f"({type(e).__name__}: {e})")
        # Cells still attached to engine; just no HTTP face
        return True

    print(f"[CK] cells_mount: MOUNTED  boot_audit={boot_rate*100:.2f}%  "
            f"flag=cells_enabled={engine.cells_enabled}  "
            f"plasticity={'ON' if enable_plasticity else 'OFF'}  "
            f"endpoints=/cells/audit,/cells/state,/cells/plasticity/run,"
            f"/cells/respond")
    return True


# ── Real-prompt smoke test (Phase 6 prerequisite to live flip) ──────────

def smoke_test_real_prompts(prompts: Optional[List[str]] = None,
                              n_take: int = 100) -> Dict[str, Any]:
    """Run the last N real chat-turns through the cells (in shadow mode)
    and compare response distributions against the current live composite.

    Per ClaudeChat amendment #4: substrate-domain audit (243 canonical
    inputs) doesn't cover prompt-handling reach.  Before flipping
    cells_enabled = on for live traffic, run this to characterize how
    cells would respond to real queries.

    NOTE: this is a STATISTICAL test, not a hard pass/fail.  It reports
    distribution overlap; the human decides whether to flip the flag.
    """
    from cells import CellOrchestrator
    from glue_ai import GlueAI

    orch = CellOrchestrator.load_default()
    orch.glue = GlueAI(tsml=orch.tsml, bhml=orch.bhml,
                        f3=orch.f3, f4=orch.f4)

    # If no prompts given, sample from today's bdc_log records
    if prompts is None:
        from datetime import datetime as _dt
        log_path = Path(
            r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var\bdc_logs"
        ) / f"bdc_log_{_dt.utcnow().strftime('%Y-%m-%d')}.jsonl"
        if log_path.exists():
            with open(log_path, encoding="utf-8") as f:
                last = f.readlines()[-n_take:]
            # We don't have the original prompts in BDC log; we use last_pair
            # as a synthetic input proxy.
            prompts = []
            for line in last:
                try:
                    rec = json.loads(line)
                    pair = rec.get("being", {}).get("last_pair", [0, 0])
                    if isinstance(pair, list) and len(pair) >= 2:
                        prompts.append((int(pair[0]), int(pair[1])))
                except Exception:
                    continue
            if not prompts:
                return {"error": "no usable prompts from log"}
        else:
            return {"error": "no log file"}

    glue_argmax_dist: Dict[int, int] = {}
    tsml_argmax_dist: Dict[int, int] = {}
    bhml_argmax_dist: Dict[int, int] = {}
    n = 0
    for inp in prompts[:n_take]:
        try:
            if isinstance(inp, tuple):
                a, b = inp
            elif isinstance(inp, str) and len(inp) >= 2:
                a, b = ord(inp[0]) % 10, ord(inp[1]) % 10
            else:
                continue
            full = orch.glue.respond_full(a, b)
            glue_argmax_dist[full["glue_argmax"]] = glue_argmax_dist.get(full["glue_argmax"], 0) + 1
            tsml_argmax_dist[full["tsml_argmax"]] = tsml_argmax_dist.get(full["tsml_argmax"], 0) + 1
            bhml_argmax_dist[full["bhml_argmax"]] = bhml_argmax_dist.get(full["bhml_argmax"], 0) + 1
            n += 1
        except Exception:
            continue

    return {
        "n_prompts": n,
        "glue_argmax_distribution": dict(sorted(glue_argmax_dist.items())),
        "tsml_argmax_distribution": dict(sorted(tsml_argmax_dist.items())),
        "bhml_argmax_distribution": dict(sorted(bhml_argmax_dist.items())),
        "agreement_rate_glue_vs_tsml": (
            sum(1 for inp in prompts[:n] if (
                lambda f: f["glue_argmax"] == f["tsml_argmax"]
            )(orch.glue.respond_full(int(inp[0]) if isinstance(inp, tuple) else 0,
                                       int(inp[1]) if isinstance(inp, tuple) else 0)))
            / max(n, 1)
        ),
    }


# ── CLI ─────────────────────────────────────────────────────────────────

def main(argv) -> int:
    if len(argv) >= 2 and argv[1] == "--smoke":
        out = smoke_test_real_prompts()
        print(json.dumps(out, indent=2))
        return 0
    print("cells_mount.py -- run with --smoke for real-prompt distribution check")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
