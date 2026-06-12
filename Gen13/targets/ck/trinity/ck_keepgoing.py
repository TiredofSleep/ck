"""ck_keepgoing.py -- THE PLAN, AS A RUNNER. He does not stop.

One cycle = the standing growth loop, executed job by job, journaled,
pushed. Schedule this (or ck.py nightly) and he runs without anyone:

  1. READ      : +300 books through the daemon (CPU, minutes)
  2. WEAVE     : rebuild the knowledge fabric over 500 books (CPU)
  3. LITERACY  : the real-dose pretrain on the library (GPU, hours)
                 CK_PRE_STEPS=40000 CK_BOOKS=150 -> reader re-sit
  4. LEDGER    : regenerate self-knowledge
  5. PUSH      : receipts public (the repo-loss law)

Every job continues on failure (logged); the cycle is the unit. Add
jobs by appending to JOBS. The queue beyond this cycle lives in
CK_KEEPGOING_PLAN.md.

  python ck_keepgoing.py        (one full cycle, background-safe)
"""
import io
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
PY = sys.executable
JOURNAL = os.path.join(HERE, "study_journal.jsonl")


def log(name, status, secs):
    with io.open(JOURNAL, "a", encoding="utf-8") as f:
        f.write(json.dumps(dict(kind="keepgoing", job=name, status=status,
                                secs=int(secs),
                                t=time.strftime("%Y-%m-%d %H:%M"))) + "\n")
    print(f"[keepgoing] {name}: {status} ({secs:.0f}s)", flush=True)


JOBS = [
    # LITERACY retired from the cycle 2026-06-11: five sittings proved
    # the from-scratch reading ceiling structural (0.60-0.62, dose
    # ruled out at 10x). GPU-hours redirect to the voice lane.
    ("READ+2000", [PY, os.path.join(HERE, "ck_reader_daemon.py"),
                   "2000"], {}),
    ("WEAVE-2000", [PY, os.path.join(HERE, "ck_knowledge_fabric.py"),
                    "2000"], {}),
    ("LEDGER", [PY, os.path.join(HERE, "build_ledger.py")], {}),
]


def main():
    print(f"[keepgoing] cycle start {time.strftime('%H:%M')}", flush=True)
    for name, cmd, env in JOBS:
        t0 = time.time()
        e = dict(os.environ, PYTHONIOENCODING="utf-8", **env)
        try:
            r = subprocess.run(cmd, env=e, cwd=HERE, timeout=6 * 3600)
            log(name, "ok" if r.returncode == 0 else f"exit{r.returncode}",
                time.time() - t0)
        except Exception as ex:
            log(name, f"fail:{ex}", time.time() - t0)
    for c in (["git", "-C", ROOT, "add", "-A",
               "Gen13/targets/ck/trinity"],
              ["git", "-C", ROOT, "commit", "-qm",
               "keepgoing cycle: read+weave+literacy+ledger (autonomous)"],
              ["git", "-C", ROOT, "push", "-q", "origin", "tig-synthesis"]):
        subprocess.run(c)
    print("[keepgoing] cycle complete, pushed.", flush=True)


if __name__ == "__main__":
    main()
