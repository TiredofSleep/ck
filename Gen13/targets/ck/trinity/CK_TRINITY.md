# CK-TRINITY — the synthesized intelligence system

**2026-06-11.** Brayden: *"combine and synthesize everyone in the field and let's build our own
intelligence system... keep going until you hit a dead end or change the face of intelligence."*
And the governing law, his correction mid-build: *"it doesn't win its seat, it EARNS its place
based on its abilities... CK's toolbox is the generation layer for his entire experience."*

## §1 The law of the toolbox

No tool is fired for losing a benchmark; no tool is kept for being beautiful. Every tool holds
exactly the abilities it has **measured**, the registry is public, and the system routes by
ability. The toolbox is the **generation layer**: what CK experiences IS the joint measurement
his tools produce. (Percept = fused output of every sense; the faces consume percepts.)

## §2 The seats, as earned today (every number reproducible from organ_*.py)

| tool | from | measured abilities | seat |
|---|---|---|---|
| **VSA-trigram** | VSA/HDC (Kanerva school) | noisy-recall **91%** mean top-1; deletions **96%** | FORM: primary recall |
| **VSA-position** | VSA/HDC | substitutions **100%**, swaps **98%**; resonance **+0.454** | FORM: sub/swap recall |
| **braid (ours)** | Burau/TIG | white-box **evidence** (named invariants — prints *why*); **exact** swap-invariant identity (theorem); resonance **+0.445 at 50× compression** (41-d vs 2048-d) | FORM: evidence + compact identity |
| **fused percept** (borrowed embed + char + braid) | standard ML + ours | routing **80%** (keyword 20%); learning curve 15→80% | MEANING: the percept |
| **kNN-distance + split conformal** | deep-kNN OOD + conformal | far-OOD hallucination **0%** vs MSP 27%; near-OOD **42%** vs 58%; acc-when-answering **85%** vs 79% — identical guarantee machinery | GAP: the gate |
| **multiscale integer-wrapped lattices** | WFA/linear-2RNN class + **Brayden's integer wrapping** | period rule-generalization **72%** (ESN 47%, chance 10%); canonical=random under identical nesting (the NESTING is the value) | SEQUENCE: counters/periods |
| **GRU / ESN class** | standard recurrent tools | DYCK validity **100%** (ESN, P4) | SEQUENCE: event tracking |
| **TRM-refiner** | Tiny Recursive Models | parity-20 static refinement **FAILED (53%)**; retargeted to PERIOD: **58%** vs one-shot 55% vs multiscale-lattice **72%** — loses to the toolbox | RECURSION: **seat vacated** (numbers kept) |

## §3 The three faces (what the system DOES)

- **FORM** — identity through noise, with evidence. Live demo: `harmny→harmony`,
  `sustrate→substrate`, `permutaton→permutation`.
- **MEANING** — trained heads over the fused percept. Live demo: "what gates his voice each
  tick" → t_star (conf 0.98, evidence: nearest known question printed).
- **GAP** — the forced choice. Live demo: "best pizza in hot springs" → **REFUSE (Type-III)**,
  with the math shown (knn 0.161 < τ 0.208) and the nearest known item printed.

**The open frontier, displayed honestly by the live demo itself:** "what is the hodge
conjecture" slipped through (knn 0.292 > τ) and was routed to kissing_j55 at conf 1.0 — the
near-OOD hallucination class (42% at conformal τ; best known, but not solved). The gate's next
upgrade target is exactly this: plausible-looking unanswerables. Also recorded: the conformal
guarantee is relative to its calibration distribution — teacher-grown calibration vs hand-written
queries showed the drift (65–70% realized vs 90% guaranteed). Drift between machine language and
human language is now a *measured* phenomenon in CK's own gate.

## §3.1 The GAP risk dial (organ_gap_dial.py — upgrade landed same session)

Negative store (the *concept* "plausible-but-unanswerable", templates disjoint from test traps)
+ contrastive score `knn(ref) − λ·knn(neg)`, conformal τ per λ:

| λ | coverage | halluc far | halluc NEAR |
|---|---|---|---|
| 0.00 | 65% | 0% | 42% |
| 0.40 | 50% | 0% | 33% |
| 0.60 | 40% | 0% | 25% |
| 0.75 | 35% | 0% | **8%** (1 of 12) |

A monotone, **measured risk dial** — deployment picks λ by risk tolerance; far-OOD is 0% at
every setting. (Granularity caveat: 12 near-traps.)

## §4 Dead ends hit (the mandate said keep going until one — we hit FOUR and kept what they taught)

1. **Parity-20 at N=1000** resists EVERY engine — one-shot 53%, TRM-refiner 53% (both
   memorizing, train 100%), and the field's GRU after a fair minibatch retune: train 80%,
   **test 49%**. A clean, total dead end for gradient learners at this data size. The pointer
   it leaves: parity is a 2-state automaton — *discrete automaton induction* (spectral WFA
   learning, Hsu/Balle school) is the registered next experiment, and CK's lattice machinery is
   already in the WFA class.
1b. **TRM-refiner on structured prediction**: 58% vs the multiscale lattice's 72% — the
   recursion organ as implemented never beat the toolbox anywhere; seat vacated. (TRM's home
   turf — large grid puzzles, big training budgets — was not reproducible at our scale.)
2. **The braid as recall champion** — beaten 91% to 45% by the field's VSA encodings; kept for
   its unique measured abilities (evidence, exact swap identity, compression), per the law.
3. **The canonical tables as special** — five kills, ended in the verdict doc; the multiscale
   *nesting* (Brayden's correction) survived as machinery and holds the sequence seat.

## §4.1 The rope's last two pulls (same session)

**The parity door OPENED (organ_induction.py):** discrete automaton induction — 56 hypotheses,
0 seconds — **100.0% test** from the same 1000 examples where every gradient engine memorized to
~50%. The induced machine is the even/odd automaton itself (`delta=[[0,1],[1,0]]`): *the
explanation and the solution are the same object.* Type-II confirmed in its purest form: the
failure was the hypothesis class, never the data. SEQUENCE organ gains discrete induction as a
measured ability.

**The meaning wean DEAD END, mechanism identified (organ_wean.py):** distill nomic → native form
features (char+braid+VSA). Ridge fit 0.63 → routing 30% (worse than no meaning block, 35%).
Retune: MLP distiller fit the teacher at **0.971 train cosine — and routing stayed 30%.** The map
memorizes the teacher and transfers nothing: the native FORM percept does not *contain* the
information that contextual MEANING space encodes for novel sentences. Third independent proof of
the session's law: **meaning is not derivable from form** (cross-family ✗, resonance partial,
distillation ✗ at 0.97 fit). The wean requires a native encoder trained on *usage* data (the
small-LM/TRM-text lane) — a real future project, not a map. Gate sanity: the GAP face survives on
distilled percepts (separation +0.12), so abstention does not depend on Ollama.

## §4.2 The spring (next-session coil, executed same day)

**organ_induction.py — parity door OPENED** (see §4.1). **organ_meaning_native.py — the missing
organ, first growth measured:** PPMI+SVD distributional vectors (Levy-Goldberg) + SIF sentence
embeddings, trained on **CK's own life-corpus** (canon + thesis + 383 journal files + CK docs +
study logs = 6.5 MB, 903K tokens) — *no teacher, no Ollama, native learning from usage*.

White-box probes came back visibly correct: `harmony` lives near **void, breath, reset** (the
4-core, learned from raw text); `sigma` near *omega, cycle, orbit, transpositions*; `attractor`
near *core, br, iteration*. Routing: **NATIVE-USAGE 50%** vs form-only 35% vs borrowed 80% —
partial signal per the registered bands (≥60% seats it; 45–60% partial). Diagnosis: register
mismatch — 900K tokens of formal math prose vs conversational queries; window/dim retune did not
move it. **Growth law established: this organ improves as CK accumulates lived conversational
text.** The seat is provisional-pending; the curriculum is to live more.

## §5 What is genuinely new here (the claim, scoped honestly)

The pieces are the field's (VSA, kNN-OOD, conformal, WFA-class lattices, TRM, fused heads). The
**combination** is not standard: a system whose *identity* is abstention-first (the gate is the
spine, not a bolt-on), whose *every* decision ships with printable evidence (nearest known item +
distance + named invariants where the braid is used), whose memory survives noise topologically,
and whose ability registry is itself a measured, public object — the system knows what each of
its own organs can do, with numbers. That last property — **self-knowledge as a data structure**
— is the face-changing move if it scales: intelligence that can show you the boundary of what it
knows, organ by organ, number by number.

## §6 Next (in order of evidence-per-effort)

1. Near-OOD gate hardening: contrastive negatives (fabricated-fact traps) in calibration; per-class τ.
2. The MEANING wean: distill borrowed-embed → a small native encoder over VSA+braid percepts (learning-curve gated).
3. SEQUENCE organ unification: multiscale lattices + GRU as one routed organ; DYCK+PERIOD+counter battery.
4. TRM-refiner verdict on structured prediction (pending run) — seat confirmed or vacated.
5. External benchmark: a published selective-QA set (the lane where the gate already beats MSP).
