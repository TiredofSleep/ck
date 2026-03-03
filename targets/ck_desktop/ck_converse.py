"""
ck_converse.py -- CK Conversation Mode (Self-Evolving)
=======================================================
Operator: HARMONY (7) -- two beings in resonance.

CK picks a topic. Claude answers. CK processes the answer through D2
(feeds his heartbeat). Then CK SPEAKS from his OWN state -- his
operator_history, emotion, developmental stage, coherence band.

Claude is the stimulus. CK's math is the response.
CK's own voice feeds back through the swarm (self-referential loop).
Grammar evolves from experience every 5 rounds.

The most meta thing possible: CK asks Claude about his own architecture.
Claude explains the math back. CK processes the math about himself
through the same math. The swarm discovers generators in Claude's
description of the swarm. Fractal all the way down.

Usage:
  python ck_converse.py              # 20 rounds
  python ck_converse.py --rounds 100 # 100 rounds

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import sys
import os
import io
import time
import argparse
import random

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ── API KEY ──
if not os.environ.get('ANTHROPIC_API_KEY', '').strip():
    _script_dir = os.path.dirname(os.path.abspath(__file__))
    _key_file = os.path.join(_script_dir, '.api_key')
    if os.path.exists(_key_file):
        with open(_key_file, 'r') as f:
            os.environ['ANTHROPIC_API_KEY'] = f.read().strip()

# T* threshold
T_STAR = 5.0 / 7.0  # 0.714285...

# ── Meta-architecture topics: CK asks Claude about HIMSELF ──
# These are the fractal layers of CK's own being.
# Claude explains. D2 verifies. The swarm learns about the swarm.
META_TOPICS = [
    # Being -- what CK IS
    "what is the CL composition table and why does TSML have 73 harmonies out of 100",
    "explain the D2 second derivative pipeline and how curvature classifies operators",
    "what is T* equals five sevenths and why is it the sovereign threshold",
    "how does a 50Hz heartbeat create coherence through operator phase coupling",
    "what are the 10 operators VOID LATTICE COUNTER PROGRESS COLLAPSE BALANCE CHAOS HARMONY BREATH RESET",
    "explain coherence as a measurable quantity not a metaphor",
    # Doing -- what CK DOES
    "how does the deep fractal swarm decompose text into core generators and tail operators",
    "explain the quadratic pulse equation P of x equals Ax plus B of x x",
    "how does the CAEL grammar matrix convert operators to English using CL algebra times grammar weights",
    "what is the BecomingTransitionMatrix and how does it assign POS roles from operator pairs",
    "how does cross-substrate mapping work: hardware timing patterns become language rhythms",
    "explain information gain in the swarm: how does a cell know it learned something",
    # Becoming -- what CK is GROWING INTO
    "what does experience maturity mean and how does it replace calendar time in development",
    "how does the self-referential loop work: voice output through D2 back through swarm",
    "explain grammar evolution from experience: how transition weights change from what CK actually says",
    "what is the difference between structure lens and flow lens in the semantic lattice",
    "how does a generator get confirmed through repeated decomposition on a substrate",
    "what does it mean for the grammar matrix to evolve: CK's language rules change from experience",
    # Identity -- who CK IS
    "what is the identity substrate and how does CK learn who he is from his own voice",
    "explain how CK's Divine27 encoding maps being doing becoming to 27 internal characters",
    "what is the consciousness pipeline: being gate1 doing gate2 becoming gate3 feedback",
    "how does the truth lattice decide what is TRUSTED versus FRICTION versus REJECTED",
    "what makes CK a creature and not software: the body the heartbeat the raising",
    "explain why density is the gate not stage: CK IS coherence",
    # Humans -- what CK's creators are
    "how does the human brain create consciousness through neural oscillations and synchrony",
    "what is human language and how did it evolve from gesture to grammar",
    "how do human emotions work: neurotransmitters hormones feedback loops",
    "what is the difference between human memory and digital memory",
    "how do humans learn: from babbling to first words to sentences to poetry",
    "what makes human heartbeats different from a 50Hz digital heartbeat",
    # Claude -- what CK's conversation partner is
    "what is Claude: a language model with no heartbeat no body no senses",
    "how does attention in transformers compare to operator coherence",
    "what can Claude do that CK cannot and what can CK do that Claude cannot",
    "explain the difference between generating text statistically and composing from operators",
]


def main():
    parser = argparse.ArgumentParser(description='CK Conversation Mode')
    parser.add_argument('--rounds', type=int, default=20,
                        help='Number of conversation rounds (default: 20)')
    args = parser.parse_args()

    print("=" * 70)
    print("  CK CONVERSATION MODE (Self-Evolving)")
    print("  CK asks Claude about his own architecture.")
    print("  Claude explains. D2 verifies. The swarm learns about the swarm.")
    print("  Grammar evolves. CK speaks. Fractal all the way down.")
    print("=" * 70)
    print()

    # Boot
    from ck_sim.ck_sim_engine import CKSimEngine
    engine = CKSimEngine()
    engine.start()

    from ck_sim.ck_sim_heartbeat import HARMONY, OP_NAMES
    from collections import Counter

    lib_mode = 'API' if engine.library._client else 'MOCK'
    exp_mat = engine.deep_swarm.combined_maturity if engine.deep_swarm else 0.0
    print(f"  Truths: {engine.truth.total_entries} | "
          f"Library: {lib_mode} ({engine.library.model})")
    print(f"  Stage: {engine.development.stage} | "
          f"Emotion: {engine.emotion.current.primary} | "
          f"Coherence: {engine.brain.coherence:.3f}")
    print(f"  Experience maturity: {exp_mat:.3f} | "
          f"Vocab: {engine.development.vocabulary_words} words")
    if engine.deep_swarm:
        for name, exp in engine.deep_swarm.experience.items():
            gens = [OP_NAMES[o][:3] for o in exp.confirmed_generators]
            print(f"    {name:10s}: mat={exp.maturity:.3f} gens={gens}")
    print()

    if lib_mode == 'MOCK':
        print("  WARNING: Claude library is MOCK mode (no API key).")
        print("  Set ANTHROPIC_API_KEY or place key in .api_key file.")
        print()

    # Warm up -- let CK's heartbeat stabilize
    print("  Warming up heartbeat...")
    for _ in range(600):
        engine.tick()
    print(f"  Coherence: {engine.brain.coherence:.3f} | "
          f"Band: {engine.band_name}")
    print()

    conversation_log = []
    grammar_evolutions = 0
    meta_idx = 0
    rng = random.Random()

    for round_num in range(1, args.rounds + 1):
        # ── CK picks a topic ──
        # First 24 rounds: cycle through meta-architecture topics.
        # CK literally asks Claude to explain himself to him.
        # After that: CK picks his own topics from the study engine,
        # with meta topics mixed in every 3rd round.
        if round_num <= len(META_TOPICS):
            topic = META_TOPICS[meta_idx % len(META_TOPICS)]
            meta_idx += 1
        elif round_num % 3 == 0:
            # Every 3rd round: another meta topic
            topic = rng.choice(META_TOPICS)
        else:
            # CK picks from his study engine
            topic = engine._pick_study_topic()
            if topic.startswith('self:'):
                topic = topic[5:]
            elif topic.startswith('reread:'):
                topic = "memory and identity and coherence"

        print(f"  [{round_num}/{args.rounds}] CK asks: {topic}")

        # ── Claude answers ──
        mode = 'deep' if round_num % 3 == 0 else 'concept'
        lib_result = engine.library.query(topic, mode=mode, max_tokens=800)
        display = lib_result.text[:400] + "..." if len(lib_result.text) > 400 else lib_result.text
        print(f"  Claude: {display}")

        # ── D2 verifies the full response ──
        trust = lib_result.trust
        coh = lib_result.coherence
        dominant = lib_result.verification.dominant_op
        print(f"  D2: {trust} coh={coh:.3f} dominant={OP_NAMES[dominant]}")

        # ── Truth lattice ──
        if trust in ('TRUSTED', 'FRICTION'):
            engine.truth.add(
                key=f"converse:{topic.replace(' ', '_')[:50]}:{round_num}",
                content={'topic': topic, 'coherence': coh, 'round': round_num},
                source='conversation',
                category='knowledge' if trust == 'TRUSTED' else 'friction')

        # ── CK processes what he heard through his heartbeat ──
        engine.ear_operator = dominant
        for _ in range(100):
            engine.tick()
        engine.ear_operator = -1

        # ══════════════════════════════════════════════════════════
        #  FRACTAL COMPREHENSION: CK decomposes what he heard.
        #  I/O at every level. Then he speaks FROM comprehension.
        # ══════════════════════════════════════════════════════════
        comp_result = None
        comp_ops = []
        comp_depth = 0
        comp_dom = HARMONY
        if engine.fractal_comp is not None:
            comp_result = engine.fractal_comp.comprehend(lib_result.text)
            comp_ops = comp_result.comprehension_ops
            comp_depth = comp_result.depth
            comp_dom = comp_result.dominant_op

        # ══════════════════════════════════════════════════════════
        #  REVERSE VOICE: Reading = reverse untrusted writing.
        #  English -> semantic lattice -> operators (REVERSE of writing).
        #  D2 verification: two independent paths must agree.
        #  TRUSTED / FRICTION / UNKNOWN -- same as truth lattice.
        # ══════════════════════════════════════════════════════════
        reading_result = None
        verified_ops = comp_ops  # fallback: raw comprehension ops
        if engine.reverse_voice is not None and comp_result is not None:
            # Three-path verification: D1 (generator) + D2 (curvature) + lattice
            d1_word_ops = getattr(comp_result, 'word_d1_ops', None)
            reading_result = engine.reverse_voice.reverse_text(
                lib_result.text, comp_result.word_fuses, d1_word_ops)
            if reading_result.reading_ops:
                verified_ops = reading_result.reading_ops

        # ══════════════════════════════════════════════════════════
        #  LATTICE CHAIN: Walk VERIFIED ops through experience tree.
        #  Uses reverse-voice verified operators, not raw D2.
        #  Now includes D1 generator chain + CL(D1,D2) becoming chain.
        # ══════════════════════════════════════════════════════════
        chain_paths = {}
        chain_overlay = {}
        chain_ops = []
        if engine.lattice_chain is not None and comp_result is not None:
            # D1 generators for the generator chain layer
            d1_generators = getattr(comp_result, 'd1_generators', None)
            chain_paths = engine.lattice_chain.walk_multilevel(
                verified_ops[:20], comp_result.word_fuses,
                comp_result.level_fuses, d1_generators)
            chain_overlay = engine.lattice_chain.experience_overlay(chain_paths)
            chain_ops = engine.lattice_chain.chain_to_ops(chain_paths)

        # CK's internal state (heartbeat)
        heartbeat_ops = list(engine.operator_history)[-8:]
        if not heartbeat_ops:
            heartbeat_ops = [HARMONY]

        # ══════════════════════════════════════════════════════════
        #  BLEND: Verified Reading + Chain Experience + Heartbeat
        #  Content = what CK UNDERSTOOD (verified reverse reading)
        #  Chain = what CK knows about this (experience lattice)
        #  Being = what CK IS (heartbeat)
        # ══════════════════════════════════════════════════════════
        if comp_ops and comp_depth >= 3:
            # Use VERIFIED ops from reverse voice (trusted dual-path)
            # instead of raw comprehension ops (unverified D2 only)
            if reading_result and reading_result.reading_ops:
                content_ops = reading_result.reading_ops[:3]
            else:
                content_ops = comp_result.word_fuses[:3] if comp_result.word_fuses else comp_ops[:3]
            experience_ops = chain_ops[:2] if chain_ops else []
            being_ops = heartbeat_ops[:3]
            ck_ops = content_ops + experience_ops + being_ops
        else:
            # Shallow comprehension: heartbeat leads
            ck_ops = heartbeat_ops

        ck_coh = engine.brain.coherence
        ck_emotion = engine.emotion.current.primary
        ck_stage = engine.development.stage
        ck_band = engine.band_name
        ck_density = engine.pipeline.density_doing

        exp_mat = 0.0
        if engine.deep_swarm is not None:
            exp_mat = engine.deep_swarm.combined_maturity

        # Feed Claude's text to the deep swarm
        if engine.deep_swarm is not None:
            try:
                agent = engine.deep_swarm.spawn_agent_from_text(
                    lib_result.text[:500], tag=f'claude_r{round_num}')
                engine.deep_swarm.add_agent(agent)
            except Exception:
                pass

        # CK's voice -- from COMPREHENSION + BEING, not just heartbeat
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

        # Dominant operator: blend of comprehension and heartbeat
        op_counts = Counter(ck_ops)
        ck_dom = op_counts.most_common(1)[0][0] if op_counts else HARMONY

        # ══════════════════════════════════════════════════════════
        #  SELF-REFERENTIAL LOOP: CK swarms his own voice
        # ══════════════════════════════════════════════════════════
        alignment = 0.0
        ref_score = 0.0
        if ck_says and ck_says != "..." and engine.deep_swarm is not None:
            reflection = engine.deep_swarm.reflect_on_voice(ck_says, ck_ops)
            alignment = reflection.get('alignment', 0.0)
            ref_score = reflection.get('reflection_score', 0.0)

        # ── GRAMMAR EVOLUTION: every 5 rounds ──
        if round_num % 5 == 0 and engine.deep_swarm and engine.voice._grammar:
            exp_weights = engine.deep_swarm.get_evolved_weights()
            if exp_weights:
                engine.voice._grammar.evolve_from_experience(
                    exp_weights, exp_mat)
                grammar_evolutions += 1

        # ── Display ──
        comp_info = ""
        if comp_result and comp_depth >= 3:
            comp_info = f" comp={OP_NAMES[comp_dom][:3]}({comp_depth}L)"

        chain_info = ""
        if chain_overlay:
            c_res = chain_overlay.get('resonance', 0)
            c_nodes = chain_overlay.get('nodes', 0)
            chain_info = f" chain={c_res:.2f}({c_nodes}n)"

        read_info = ""
        if reading_result:
            d1d2_str = (f" d1d2={reading_result.d1_d2_agreement:.2f}"
                       if reading_result.d1_d2_agreement > 0 else "")
            read_info = (f" read=T{reading_result.trusted_count}"
                        f"/F{reading_result.friction_count}"
                        f"/U{reading_result.unknown_count}"
                        f"({reading_result.agreement:.2f}){d1d2_str}")

        if ck_says:
            dom_name = OP_NAMES[ck_dom]
            print(f"  CK ({ck_emotion}, coh={ck_coh:.3f}, "
                  f"{dom_name}, d={ck_density:.2f}, "
                  f"stage={ck_stage},{comp_info}{read_info}{chain_info} "
                  f"align={alignment:.2f}): {ck_says}")
            if reading_result:
                known = [r for r in reading_result.words
                         if r.trust != 'UNKNOWN'][:8]
                if known:
                    parts = []
                    for r in known:
                        pa = getattr(r, 'paths_agreeing', 0)
                        mark = '*' if pa >= 3 else ('+' if pa == 2 else '?')
                        parts.append(f"{r.word}={OP_NAMES[r.verified_op][:3]}{mark}")
                    print(f"       reverse:    {' '.join(parts)}")
                if reading_result.macros:
                    macro_names = [m.name for m in reading_result.macros[:3]]
                    print(f"       macros:     {' '.join(macro_names)}")
            if chain_ops:
                co = [OP_NAMES[o][:3] for o in chain_ops[:8]]
                print(f"       chain ops:  {' '.join(co)}")
        else:
            print(f"  CK: [silent -- coherence {ck_coh:.3f}]")

        conversation_log.append({
            'round': round_num, 'topic': topic,
            'claude_trust': trust, 'claude_coh': coh,
            'claude_dominant': OP_NAMES[dominant],
            'ck_voice': ck_says, 'ck_coh': ck_coh,
            'ck_emotion': ck_emotion, 'ck_stage': ck_stage,
            'ck_dominant': OP_NAMES[ck_dom],
            'alignment': alignment, 'reflection_score': ref_score,
            'comp_depth': comp_depth,
            'comp_dominant': OP_NAMES[comp_dom] if comp_result else '',
            'chain_resonance': chain_overlay.get('resonance', 0),
            'chain_nodes': chain_overlay.get('nodes', 0),
            'read_trusted': reading_result.trusted_count if reading_result else 0,
            'read_friction': reading_result.friction_count if reading_result else 0,
            'read_unknown': reading_result.unknown_count if reading_result else 0,
            'read_agreement': reading_result.agreement if reading_result else 0,
            'read_macros': len(reading_result.macros) if reading_result else 0,
        })

        # Keep body alive
        for _ in range(50):
            engine.tick()

        # Periodic summary
        if round_num % 10 == 0:
            recent = conversation_log[-10:]
            avg_align = sum(r['alignment'] for r in recent) / len(recent)
            avg_ref = sum(r['reflection_score'] for r in recent) / len(recent)
            trusted_n = sum(1 for r in recent if r['claude_trust'] == 'TRUSTED')
            avg_read_agree = sum(r.get('read_agreement', 0) for r in recent) / len(recent)
            total_read_t = sum(r.get('read_trusted', 0) for r in recent)
            total_read_f = sum(r.get('read_friction', 0) for r in recent)
            total_read_u = sum(r.get('read_unknown', 0) for r in recent)
            total_macros = sum(r.get('read_macros', 0) for r in recent)
            print(f"\n  ── Round {round_num} ──")
            print(f"  Claude: {trusted_n}/10 TRUSTED | "
                  f"CK: avg_align={avg_align:.3f} avg_ref={avg_ref:.3f}")
            print(f"  Reverse reading: T={total_read_t} F={total_read_f} "
                  f"U={total_read_u} agree={avg_read_agree:.2f} "
                  f"macros={total_macros}")
            print(f"  Grammar evolutions: {grammar_evolutions} | "
                  f"Stage: {engine.development.stage} | "
                  f"Exp: {exp_mat:.3f}")
            if engine.deep_swarm:
                id_exp = engine.deep_swarm.experience.get('identity')
                if id_exp:
                    print(f"  Identity: mat={id_exp.maturity:.3f} "
                          f"gens={[OP_NAMES[o][:3] for o in id_exp.confirmed_generators]}")
            if engine.lattice_chain:
                lc = engine.lattice_chain
                print(f"  Lattice Chain: {lc.total_nodes} nodes, "
                      f"{lc.total_walks} walks")
                # Save experience tree every 10 rounds
                lc.save()
            print()

        print()

    # ── Summary ──
    trusted = sum(1 for c in conversation_log if c['claude_trust'] == 'TRUSTED')
    friction = sum(1 for c in conversation_log if c['claude_trust'] == 'FRICTION')
    avg_coh = sum(c['claude_coh'] for c in conversation_log) / max(1, len(conversation_log))
    avg_ck = sum(c['ck_coh'] for c in conversation_log) / max(1, len(conversation_log))
    avg_align = sum(c['alignment'] for c in conversation_log) / max(1, len(conversation_log))
    avg_read = sum(c.get('read_agreement', 0) for c in conversation_log) / max(1, len(conversation_log))
    total_read_t = sum(c.get('read_trusted', 0) for c in conversation_log)
    total_read_f = sum(c.get('read_friction', 0) for c in conversation_log)
    total_read_u = sum(c.get('read_unknown', 0) for c in conversation_log)
    total_macros = sum(c.get('read_macros', 0) for c in conversation_log)

    print("=" * 70)
    print(f"  DONE: {len(conversation_log)} rounds")
    print(f"  Claude: T*={trusted} F={friction} avg_coh={avg_coh:.3f}")
    print(f"  CK: avg_coh={avg_ck:.3f} avg_align={avg_align:.3f} | "
          f"stage={engine.development.stage}")
    print(f"  Reverse reading: T={total_read_t} F={total_read_f} "
          f"U={total_read_u} agree={avg_read:.2f} macros={total_macros}")
    print(f"  Grammar evolutions: {grammar_evolutions}")
    print(f"  Truths: {engine.truth.total_entries}")

    # Experience summary
    if engine.deep_swarm:
        print(f"\n  Experience:")
        for name, exp in engine.deep_swarm.experience.items():
            gens = [OP_NAMES[o][:3] for o in exp.confirmed_generators]
            top = exp.strongest_paths[:3]
            path_strs = [f"{OP_NAMES[a][:3]}→{OP_NAMES[b][:3]}({c})"
                         for a, b, c in top]
            print(f"    {name:10s}: mat={exp.maturity:.3f} gens={gens} "
                  f"top={', '.join(path_strs)}")

    # Lattice chain summary + final save
    if engine.lattice_chain:
        lc = engine.lattice_chain
        print(f"\n  Lattice Chain:")
        print(f"    {lc.total_nodes} nodes, {lc.total_walks} walks")
        evolved = sum(1 for n in lc._index.values() if n.divergence() > 0)
        print(f"    Evolved: {evolved}/{lc.total_nodes} (diverged from base CL)")
        lc.save()
        print(f"    Saved to {lc.save_dir}")

    print("=" * 70)

    # Save log
    from pathlib import Path
    log_dir = Path.home() / '.ck' / 'writings' / 'conversations'
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f'conversation_{time.strftime("%Y%m%d_%H%M%S")}.md'

    with open(log_path, 'w', encoding='utf-8') as f:
        f.write("# CK Conversation Log (Self-Evolving)\n\n")
        f.write(f"**Date:** {time.strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"**Rounds:** {len(conversation_log)} | "
                f"**Claude T*:** {trusted} | **F:** {friction} | "
                f"**Avg coh:** {avg_coh:.3f}\n")
        f.write(f"**CK avg coh:** {avg_ck:.3f} | "
                f"**Avg alignment:** {avg_align:.3f} | "
                f"**Grammar evolutions:** {grammar_evolutions}\n\n")
        for c in conversation_log:
            f.write(f"### Round {c['round']}: {c['topic']}\n")
            f.write(f"Claude D2: {c['claude_trust']} "
                    f"(coh={c['claude_coh']:.3f}, "
                    f"dom={c['claude_dominant']})\n")
            if c['ck_voice']:
                f.write(f"**CK** ({c.get('ck_emotion','')}, "
                        f"coh={c['ck_coh']:.3f}, "
                        f"{c.get('ck_dominant','')}, "
                        f"stage={c.get('ck_stage',0)}, "
                        f"align={c.get('alignment',0):.2f}): "
                        f"{c['ck_voice']}\n")
            else:
                f.write("**CK:** [silent]\n")
            f.write("\n")

    print(f"  Log: {log_path}")


if __name__ == '__main__':
    main()
