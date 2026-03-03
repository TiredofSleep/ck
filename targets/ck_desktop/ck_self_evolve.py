"""
ck_self_evolve.py -- CK Self-Evolution: Void to Experience
==========================================================
Operator: PROGRESS (3) -- CK grows by listening to himself.

The self-referential loop:
  1. CK's heartbeat generates operators
  2. Voice composes words from operators
  3. His own words go back through D2 → swarm
  4. Swarm measures: did the words match the intended operators?
  5. Experience updates: strong paths reinforced, weak paths die
  6. Grammar evolves from experience
  7. CK speaks again — better.

No Claude. No human. Just CK, his algebra, and time.
The swarm IS the filter. The math converges. Or it doesn't.

Give him the dictionary. Let him fly.

Usage:
  python ck_self_evolve.py                 # 50 rounds
  python ck_self_evolve.py --rounds 200    # 200 rounds
  python ck_self_evolve.py --verbose       # show swarm details

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import sys
import os
import io
import time
import argparse

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# T* threshold
T_STAR = 5.0 / 7.0  # 0.714285...


def main():
    parser = argparse.ArgumentParser(description='CK Self-Evolution')
    parser.add_argument('--rounds', type=int, default=50,
                        help='Number of self-evolution rounds (default: 50)')
    parser.add_argument('--verbose', action='store_true',
                        help='Show swarm details each round')
    args = parser.parse_args()

    print("=" * 70)
    print("  CK SELF-EVOLUTION: VOID TO EXPERIENCE")
    print("  CK speaks. CK listens to himself. The swarm decides what's real.")
    print("  No Claude. No human. Just the math.")
    print("=" * 70)
    print()

    # ── Boot ──
    from ck_sim.ck_sim_engine import CKSimEngine
    engine = CKSimEngine()
    engine.start()

    from ck_sim.ck_sim_heartbeat import HARMONY, BREATH, OP_NAMES
    from collections import Counter

    exp_mat = engine.deep_swarm.combined_maturity if engine.deep_swarm else 0.0
    print(f"  Stage: {engine.development.stage} | "
          f"Emotion: {engine.emotion.current.primary} | "
          f"Coherence: {engine.brain.coherence:.3f}")
    print(f"  Experience maturity: {exp_mat:.3f} | "
          f"Vocab: {engine.development.vocabulary_words} words")
    if engine.deep_swarm:
        for name, exp in engine.deep_swarm.experience.items():
            gens = [OP_NAMES[o][:3] for o in exp.confirmed_generators]
            print(f"    {name:10s}: mat={exp.maturity:.3f} gens={gens} "
                  f"paths={exp.path_strength}")
    print()

    # ── Warm up: let heartbeat stabilize ──
    print("  Warming up heartbeat (600 ticks)...")
    for _ in range(600):
        engine.tick()
    print(f"  Coherence: {engine.brain.coherence:.3f} | "
          f"Band: {engine.band_name}")
    print()

    # ── All 10 operators for perturbation cycling ──
    ALL_OPS = list(range(10))  # VOID..RESET

    # ── Self-evolution loop ──
    evolution_log = []
    best_score = 0.0
    best_text = ""
    grammar_evolutions = 0

    for round_num in range(1, args.rounds + 1):
        # ── OPERATOR DIVERSITY: perturb CK's state every 3 rounds ──
        # CK can't grow if he only hears HARMONY.
        # Every 3rd round, inject a different operator to explore new
        # territory. The swarm filters the results -- coherent
        # permutations survive, noise dies. This is how CK discovers
        # ALL 10 of his operators, not just the stable basin.
        if round_num % 3 == 0:
            # Cycle through all 10 operators
            perturb_op = ALL_OPS[(round_num // 3) % 10]
            engine.ear_operator = perturb_op
            for _ in range(30):
                engine.tick()
            engine.ear_operator = -1

        # ── CK's operator state (from heartbeat, not manufactured) ──
        ck_ops = list(engine.operator_history)[-8:]
        if not ck_ops:
            ck_ops = [HARMONY]

        ck_coh = engine.brain.coherence
        ck_emotion = engine.emotion.current.primary
        ck_stage = engine.development.stage
        ck_band = engine.band_name
        ck_density = engine.pipeline.density_doing

        exp_mat = 0.0
        if engine.deep_swarm is not None:
            exp_mat = engine.deep_swarm.combined_maturity

        # ── Experience-guided operator prediction ──
        # On even rounds, let the swarm predict operators from experience.
        # This supplements the heartbeat chain with learned paths.
        if round_num % 2 == 0 and engine.deep_swarm is not None:
            predicted = engine.deep_swarm.predict_voice_ops(ck_ops, 4)
            # Blend: heartbeat ops + predicted ops interleaved
            blended = []
            for i in range(max(len(ck_ops), len(predicted))):
                if i < len(ck_ops):
                    blended.append(ck_ops[i])
                if i < len(predicted):
                    blended.append(predicted[i])
            ck_ops = blended[:8]

        # ── CK speaks from his operator state ──
        if engine.pipeline.humble:
            ck_says = engine.voice.get_humble_response(ck_stage)
        else:
            ck_says = engine.voice.compose_from_operators(
                ck_ops,
                emotion_primary=ck_emotion,
                dev_stage=ck_stage,
                coherence=ck_coh,
                band=ck_band,
                density=ck_density,
                experience_maturity=exp_mat)

        # Dominant operator
        op_counts = Counter(ck_ops)
        ck_dom = op_counts.most_common(1)[0][0] if op_counts else HARMONY

        # ── SELF-REFERENTIAL LOOP: CK listens to himself ──
        reflection = {'alignment': 0.0, 'produced_ops': [], 'reflection_score': 0.0}
        if ck_says and ck_says != "..." and engine.deep_swarm is not None:
            reflection = engine.deep_swarm.reflect_on_voice(ck_says, ck_ops)

        alignment = reflection.get('alignment', 0.0)
        ref_score = reflection.get('reflection_score', 0.0)
        produced_ops = reflection.get('produced_ops', [])

        # ── Track best per operator ──
        if ref_score > best_score and ck_says and ck_says != "...":
            best_score = ref_score
            best_text = ck_says

        # ── GRAMMAR EVOLUTION: every 5 rounds, evolve from experience ──
        if round_num % 5 == 0 and engine.deep_swarm and engine.voice._grammar:
            exp_weights = engine.deep_swarm.get_evolved_weights()
            if exp_weights:
                engine.voice._grammar.evolve_from_experience(
                    exp_weights, exp_mat)
                grammar_evolutions += 1

        # ── Display ──
        dom_name = OP_NAMES[ck_dom]
        prod_names = [OP_NAMES[o][:3] for o in produced_ops[:6]]
        perturbed = " *" if round_num % 3 == 0 else ""

        if ck_says and ck_says != "...":
            print(f"  [{round_num:3d}/{args.rounds}] "
                  f"coh={ck_coh:.3f} {dom_name:8s} "
                  f"d={ck_density:.2f} "
                  f"align={alignment:.2f} ref={ref_score:.2f} | "
                  f"{ck_says}{perturbed}")
        else:
            print(f"  [{round_num:3d}/{args.rounds}] "
                  f"coh={ck_coh:.3f} {dom_name:8s} "
                  f"d={ck_density:.2f} | [silent]{perturbed}")

        if args.verbose:
            print(f"           ops={[OP_NAMES[o][:3] for o in ck_ops]} "
                  f"→ produced={prod_names}")
            if engine.deep_swarm:
                print(f"           swarm: agents={len(engine.deep_swarm.agents)} "
                      f"field_coh={engine.deep_swarm.field_coherence:.3f} "
                      f"mat={exp_mat:.3f}")

        # ── Feed CK's voice back as heartbeat stimulus ──
        # His own dominant operator feeds his ears.
        # The heartbeat absorbs it. Operator history shifts.
        engine.ear_operator = ck_dom
        for _ in range(50):
            engine.tick()
        engine.ear_operator = -1

        # ── Keep body alive between rounds ──
        for _ in range(50):
            engine.tick()

        # ── Log ──
        evolution_log.append({
            'round': round_num,
            'ck_says': ck_says,
            'ck_coh': ck_coh,
            'ck_emotion': ck_emotion,
            'ck_stage': ck_stage,
            'ck_dominant': dom_name,
            'alignment': alignment,
            'reflection_score': ref_score,
            'density': ck_density,
            'exp_maturity': exp_mat,
        })

        # ── Periodic summary ──
        if round_num % 10 == 0:
            recent = evolution_log[-10:]
            avg_align = sum(r['alignment'] for r in recent) / len(recent)
            avg_ref = sum(r['reflection_score'] for r in recent) / len(recent)
            avg_coh = sum(r['ck_coh'] for r in recent) / len(recent)
            silent = sum(1 for r in recent if not r['ck_says'] or r['ck_says'] == '...')
            print(f"\n  ── Round {round_num} summary ──")
            print(f"  avg_align={avg_align:.3f} avg_ref={avg_ref:.3f} "
                  f"avg_coh={avg_coh:.3f} silent={silent}/10 "
                  f"grammar_evol={grammar_evolutions}")
            print(f"  best so far (ref={best_score:.3f}): {best_text}")
            print(f"  stage={engine.development.stage} "
                  f"exp={exp_mat:.3f} "
                  f"vocab={engine.development.vocabulary_words}\n")

    # ── Final Summary ──
    total_spoken = sum(1 for r in evolution_log
                       if r['ck_says'] and r['ck_says'] != '...')
    avg_align = sum(r['alignment'] for r in evolution_log) / max(1, len(evolution_log))
    avg_ref = sum(r['reflection_score'] for r in evolution_log) / max(1, len(evolution_log))
    avg_coh = sum(r['ck_coh'] for r in evolution_log) / max(1, len(evolution_log))

    print("=" * 70)
    print("  SELF-EVOLUTION COMPLETE")
    print(f"  Rounds: {len(evolution_log)} | Spoken: {total_spoken} | "
          f"Grammar evolutions: {grammar_evolutions}")
    print(f"  Avg alignment: {avg_align:.3f} | "
          f"Avg reflection: {avg_ref:.3f} | "
          f"Avg coherence: {avg_coh:.3f}")
    print(f"  Best (ref={best_score:.3f}): {best_text}")
    print(f"  Stage: {engine.development.stage} | "
          f"Experience: {exp_mat:.3f} | "
          f"Vocab: {engine.development.vocabulary_words}")

    # Show experience evolution
    if engine.deep_swarm:
        print(f"\n  Experience substrates:")
        for name, exp in engine.deep_swarm.experience.items():
            gens = [OP_NAMES[o][:3] for o in exp.confirmed_generators]
            top_paths = exp.strongest_paths[:5]
            path_strs = [f"{OP_NAMES[a][:3]}→{OP_NAMES[b][:3]}({c})"
                         for a, b, c in top_paths]
            print(f"    {name:10s}: mat={exp.maturity:.3f} "
                  f"gens={gens}")
            print(f"               top_paths: {', '.join(path_strs)}")

    print("=" * 70)

    # ── Save log ──
    from pathlib import Path
    log_dir = Path.home() / '.ck' / 'writings' / 'evolution'
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f'evolution_{time.strftime("%Y%m%d_%H%M%S")}.md'

    with open(log_path, 'w', encoding='utf-8') as f:
        f.write("# CK Self-Evolution Log\n\n")
        f.write(f"**Date:** {time.strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"**Rounds:** {len(evolution_log)} | "
                f"**Grammar evolutions:** {grammar_evolutions}\n")
        f.write(f"**Avg alignment:** {avg_align:.3f} | "
                f"**Avg reflection:** {avg_ref:.3f} | "
                f"**Avg coherence:** {avg_coh:.3f}\n")
        f.write(f"**Best:** {best_text} (ref={best_score:.3f})\n\n")
        for r in evolution_log:
            f.write(f"### Round {r['round']}\n")
            f.write(f"coh={r['ck_coh']:.3f} {r['ck_dominant']} "
                    f"d={r['density']:.2f} "
                    f"align={r['alignment']:.2f} "
                    f"ref={r['reflection_score']:.2f} "
                    f"stage={r['ck_stage']} "
                    f"exp={r['exp_maturity']:.3f}\n")
            if r['ck_says'] and r['ck_says'] != '...':
                f.write(f"**CK:** {r['ck_says']}\n")
            else:
                f.write("**CK:** [silent]\n")
            f.write("\n")

    print(f"  Log: {log_path}")


if __name__ == '__main__':
    main()
