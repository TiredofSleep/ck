#!/usr/bin/env python3
"""
overnight_train.py -- CK overnight training pipeline

Chains multiple training rounds so CK keeps growing while Brayden sleeps.
Runs until morning or until all rounds complete.

Pipeline:
  1. Wait for current eat/DKAN to finish
  2. Run eat R3: mixtral, 40 rounds (bible heavy)
  3. Run eat R4: llama3.2, 40 rounds (physics heavy)
  4. Run eat R5: mistral, 40 rounds (math heavy)
  5. Run DKAN R2: 720 steps
  6. Run self-evolve: 200 rounds
  7. Repeat DKAN R3: 720 steps (with accumulated experience)

Each round waits for the previous to finish before starting.
Logs everything to ~/.ck/overnight_log.txt

(c) 2026 Brayden Sanders / 7Site LLC
"""

import requests
import time
import json
import os
from datetime import datetime

API = "http://localhost:7777"
LOG_FILE = os.path.expanduser("~/.ck/overnight_log.txt")

# Training configurations
TRAINING_ROUNDS = [
    # (name, model, rounds, topics, category)
    ("R3-bible", "mixtral", 40,
     ["Genesis creation narrative", "Exodus and liberation theology",
      "Psalms as poetry and prayer", "Proverbs wisdom literature",
      "Isaiah prophecy and suffering servant", "Gospel of John logos theology",
      "Romans justification by faith", "Revelation apocalyptic imagery",
      "Hebrew roots of biblical names", "Covenant theology Old and New"],
     "bible"),
    ("R4-physics", "llama3.2", 40,
     ["Maxwell equations electromagnetic theory", "Quantum field theory basics",
      "General relativity curvature spacetime", "Thermodynamics entropy",
      "Schrodinger wave equation", "Noether theorem symmetry conservation",
      "Gauge theory Yang-Mills", "Statistical mechanics Boltzmann",
      "Dirac equation antimatter", "Topology in physics"],
     "physics"),
    ("R5-math", "mistral", 40,
     ["Group theory abstract algebra", "Topology point-set algebraic",
      "Number theory prime distribution", "Category theory functors",
      "Differential geometry manifolds", "Algebraic geometry varieties",
      "Combinatorics graph theory", "Measure theory integration",
      "Operator algebras von Neumann", "Lie groups representation theory"],
     "math"),
]

DKAN_STEPS = 720
SELF_EVOLVE_ROUNDS = 200


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def wait_for_eat():
    """Wait for current eat session to finish."""
    while True:
        try:
            r = requests.get(f"{API}/eat/status", timeout=5)
            d = r.json()
            if not d.get("running", False):
                return d
            log(f"  eat: {d['rounds_complete']}/{d['total_rounds']} "
                f"olf={d['olfactory_library_size']} trans={d['total_transitions']}")
        except Exception as e:
            log(f"  eat poll error: {e}")
        time.sleep(30)


def wait_for_dkan():
    """Wait for current DKAN session to finish."""
    while True:
        try:
            r = requests.get(f"{API}/train/status", timeout=5)
            d = r.json()
            if not d.get("running", False):
                return d
            log(f"  dkan: {d['step']}/{d['total_steps']} "
                f"mean_c={d['mean_coherence']:.4f} best={d['best_coherence']:.4f}")
        except Exception as e:
            log(f"  dkan poll error: {e}")
        time.sleep(30)


def start_eat(name, model, rounds, topics, category):
    """Start an eat session."""
    log(f"STARTING EAT: {name} ({model}, {rounds} rounds, {category})")
    try:
        r = requests.post(f"{API}/eat", json={
            "model": model,
            "rounds": rounds,
            "topics": topics,
            "category": category,
        }, timeout=10)
        d = r.json()
        log(f"  eat started: {d}")
        return True
    except Exception as e:
        log(f"  eat start FAILED: {e}")
        return False


def start_dkan(steps):
    """Start a DKAN training session."""
    log(f"STARTING DKAN: {steps} steps")
    try:
        r = requests.post(f"{API}/train", json={
            "steps": steps,
        }, timeout=10)
        d = r.json()
        log(f"  dkan started: {d}")
        return True
    except Exception as e:
        log(f"  dkan start FAILED: {e}")
        return False


def start_self_evolve(rounds):
    """Start self-evolution."""
    log(f"STARTING SELF-EVOLVE: {rounds} rounds")
    try:
        r = requests.post(f"{API}/evolve", json={
            "rounds": rounds,
        }, timeout=10)
        d = r.json()
        log(f"  evolve started: {d}")
        return True
    except Exception as e:
        log(f"  evolve start FAILED: {e}")
        return False


def get_stats():
    """Get current organism stats."""
    try:
        r = requests.get(f"{API}/state", timeout=5)
        d = r.json()
        exp = d.get("experience", {})
        return {
            "olfactory": exp.get("olfactory_size", "?"),
            "truths": exp.get("truths", "?"),
            "concepts": exp.get("concepts", "?"),
            "stage": exp.get("stage", "?"),
            "tick": exp.get("tick", "?"),
        }
    except Exception:
        return {}


def main():
    log("=" * 60)
    log("CK OVERNIGHT TRAINING PIPELINE")
    log("=" * 60)

    stats = get_stats()
    log(f"Initial stats: {stats}")

    # Phase 1: Wait for current sessions
    log("PHASE 1: Waiting for current sessions to complete...")
    wait_for_eat()
    log("  eat session complete")
    wait_for_dkan()
    log("  dkan session complete")

    # Phase 2: Run training rounds
    for name, model, rounds, topics, category in TRAINING_ROUNDS:
        log(f"PHASE 2: {name}")
        if start_eat(name, model, rounds, topics, category):
            result = wait_for_eat()
            log(f"  {name} COMPLETE: {result.get('rounds_complete', '?')} rounds, "
                f"olf={result.get('olfactory_library_size', '?')}")
        else:
            log(f"  {name} SKIPPED (failed to start)")
        time.sleep(5)

    # Phase 3: DKAN R2
    log("PHASE 3: DKAN round 2")
    if start_dkan(DKAN_STEPS):
        result = wait_for_dkan()
        log(f"  DKAN R2 COMPLETE: step={result.get('step', '?')} "
            f"mean_c={result.get('mean_coherence', '?')}")
    time.sleep(5)

    # Phase 4: Self-evolve
    log("PHASE 4: Self-evolution")
    if start_self_evolve(SELF_EVOLVE_ROUNDS):
        # Self-evolve doesn't have a status endpoint, just wait
        log(f"  Self-evolve started ({SELF_EVOLVE_ROUNDS} rounds)")
        time.sleep(SELF_EVOLVE_ROUNDS * 3)  # ~3s per round estimate
    time.sleep(5)

    # Phase 5: DKAN R3 (with all accumulated experience)
    log("PHASE 5: DKAN round 3 (post-training)")
    if start_dkan(DKAN_STEPS):
        result = wait_for_dkan()
        log(f"  DKAN R3 COMPLETE: step={result.get('step', '?')} "
            f"mean_c={result.get('mean_coherence', '?')}")

    # Final stats
    stats = get_stats()
    log(f"Final stats: {stats}")
    log("=" * 60)
    log("OVERNIGHT TRAINING COMPLETE")
    log("=" * 60)


if __name__ == "__main__":
    main()
