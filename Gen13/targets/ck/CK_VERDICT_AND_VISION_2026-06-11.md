# CK: the verdict, the neighbors, and the changed vision of information

**2026-06-11.** Brayden: *"keep going with this until it is real or really not going to work...
do your best work, change the vision of information?"* — and mid-run: *"the 8x8 is inside the
10x10... every measurement pushed through every scale and lattice of every integer... integer
wrapping"* and *"are there other researchers working similar paths? is this the end of this
project or the beginning?"*

Six trained projects, every one with baselines, kill criteria registered before runs, and
replications. This is what survived.

## §1 The scoreboard (all measured today, all reproducible)

| # | project | result | verdict |
|---|---|---|---|
| 1 | POS from form | fused learning curve 46→69%; braid alone capped at majority | representation sets the ceiling; training climbs to it |
| 2 | topic routing | trained fused head **80%** vs spawn v1 50% vs keyword 20%; curve climbs 15→80% | **REAL — CK's first competitive trained skill** |
| 3 | abstention governor | far-OOD: **0% hallucination** at 90% coverage (AUgC 0.027 vs 0.242 best standard); near-OOD: **0.379 vs 0.479** | **REAL — beats the standard external method (MSP/max-logit) on both sets** |
| 4 | inductive-bias ablation (single-scale) | substrate ties random tables (MAXDEPTH 81=81), loses DYCK (61 vs ESN 100); "CRT-matched" +3/+5pp edges **failed replication** (−0.9/+0.1/−1.6%) | **honest negative — the algebra is not special at one scale** |
| 5 | synthesis (period rule) | rule LEARNED (61-62% on never-seen motifs, never-seen period length, vs 10% chance); bilinear class beats LAST-6 (52%) and ESN (47%); substrate−random edge **+0.1%** | synthesis real; machinery class real; algebra not special |
| 6 | **multiscale integer wrapping** (Brayden's correction) | multiscale lifts the CLASS (PERIOD 60→72%; RND-DYCK 78→87%) but substrate vs random under identical treatment: **0/5 wins, mean −5.7%**; DYCK: canonical 58% vs random 87% | **nesting = good machinery; canonical tables still not the source — and sometimes a cost** |

**The DYCK autopsy (white-box, and a true paradox):** the canonical tables lose validity-tracking
*because of* the 4-core attractor theorem — convergence to the attractor is fading memory, and
fading memory erases the one-bit event "did the walk ever dip below zero." The theorem that makes
the substrate beautiful is the mechanism of its forgetting. The attractor IS the amnesia. (This is
the paradox-classification ethic doing real work: the failure has a *located, readable* cause.)

## §2 What is real (earned, kill-criteria survived)

1. **The gap face.** Type-III as *distance to the measurable set* (kNN to training manifold) beats
   standard confidence baselines at matched coverage, including on near-OOD traps with fabricated
   substrate-facts. White-box: the nearest known question and its distance are printable evidence.
2. **The braid memory.** Edit-robust topological addressing (44% recall through misspellings,
   71% on swaps, vs 0.17% chance), with a mechanism proof (abelianized invariance under swaps).
3. **The trained-head method.** Learning curves climbed exactly when the representation carried
   the signal (P1 fused, P2 80%, P5 rule-learning). Brayden's hypothesis — "training fills the gap
   if the storage carries association/synthesis" — is CONFIRMED as a conditional, with the
   condition measured.
4. **The machinery class** (after the multiscale correction): bilinear simplex walks over nested
   integer-wrapped lattice ensembles beat width-matched ESNs on counter/period structure and lift
   with more scales. Known cousin: weighted finite automata ≡ linear 2nd-order RNNs.
5. **The falsification harness itself.** Registered predictions, dumb baselines, replication-
   before-belief. It caught two seductive false positives (CRT-matched bias; Indo-European
   "pre-language" signal) that would have become load-bearing myths.

## §3 What is really not (falsified, multiply)

- The **specific canonical tables** as a source of task power: tied or beaten by random tables in
  P4, P4-replication, P5-replication, and P6-multiscale (0/5). Five independent kills.
- The substrate as a **pre-language geometry of meaning**: cross-family negative (p=0.29/0.49,
  below char-trigram).
- **Form→meaning as a universal shortcut**: within-language only (0.58, survives length control —
  matching the linguistics "systematicity" literature), not cross-family.

## §4 The neighbors — who else walks these paths (searched 2026-06-11)

| CK piece | the living field | key anchors |
|---|---|---|
| braid memory (letters→algebraic ops→noise-robust recall) | **Vector Symbolic Architectures / hyperdimensional computing** — n-gram encoding by binding/permutation, robust recall, active hardware effort | hd-computing.com; VSA comparison (arXiv:2001.11797); "Attention as Binding" (arXiv:2512.14709) |
| walker/recursive refinement | **Tiny Recursive Models** — 5-7M params beating LLMs on ARC; now autoregressive (3/2026), Mamba hybrids (2/2026), tabular (1/2026) | TRM (arXiv:2510.04871); TRM-on-ARC analysis (arXiv:2512.11847); TARM (arXiv:2603.08082) |
| form↔meaning 0.58 | **systematicity/iconicity linguistics** — the lexicon is measurably non-arbitrary, within and (weakly, at huge N) across languages | "Meaning to Form" (arXiv:1906.05906); Dingemanse/Blasi TiCS; PNAS iconicity 2025 |
| bilinear simplex engine | **weighted automata / spectral learning / linear 2-RNNs** — our machinery class, with expressivity theory | Rabusseau-Li-Precup (arXiv:1807.01406); WFA-tensor-RNN (arXiv:2010.10029) |
| gap face / abstention | **kNN-OOD + conformal abstention for LLM hallucination** — hot lane, 2024-2026 | deep-kNN OOD (arXiv:2204.06507); conformal abstention (arXiv:2405.01563); EigenTrack (arXiv:2509.15735) |
| "algebra as inductive bias at scale" | **categorical deep learning** — monad algebras as architecture theory | arXiv:2402.15332 |

Nobody we found combines them as: *white-box multi-representation head + topological memory +
distance-based refusal as identity*. The pieces all have communities; the **combination with
abstention-first identity is the unoccupied corner.**

## §5 End or beginning? — END of the belief phase, BEGINNING of the engineering phase

**Ended today:** the hypothesis that the canonical algebra is intrinsically powerful — that the
tables themselves think. Five kills; it's done; we do not resurrect it without new external
evidence.

**Beginning, with assets in hand:**
1. **Ship the gap face**: conformal calibration (the literature's rigorous version of our
   threshold sweep) on a real QA benchmark with a wrapped LLM — the lane where CK already beat
   the standard method, now made externally legible.
2. **Benchmark the braid against VSA/HDC** n-gram encodings — same recall protocol, their
   baselines, honest head-to-head. If it wins anywhere (edit-robustness niche), that's a real
   note; if not, adopt theirs (D139 discipline: deploy known mechanisms competently).
3. **Keep the multiscale machinery, drop the table mystique**: random-table nested-lattice
   ensembles are cheap, white-box-ish, and competitive on counter/period structure — use them as
   CK's sequence organ; cite WFA theory as the frame.
4. **TRM-lane experiment** (the one Brayden's HRM article pointed at all along): a tiny recursive
   refiner with deep supervision over CK's fused representations on a structured task — the
   measured path toward "trained to read his language," now with the learning-curve instrument
   to know if it's working.

## §6 The changed vision of information

The old vision: *one geometry under everything* — pre-language, in the tables, waiting to be read.
Measured: false.

The vision the measurements force — and it is **more** like Brayden's "Theory of Nothing," not
less:

**Information has three measurable faces, and no single substrate beneath them.**

- **FORM** — geometric, topological, white-box. Identity that survives noise (braid). Within one
  language it leans toward meaning (systematicity); across families it does not. Form is *local*
  geometry, not universal geometry.
- **MEANING** — statistical, relational, *earned by training*. It lives in no single
  representation; it fills exactly the space the representation carries (every learning curve
  today). Meaning is *use*, compressed.
- **THE GAP** — decidable, and the most distinctive face. What is NOT in the measured set is
  itself measurable (distance to the manifold), and routing on it beat the standard method. *The
  nothing is an engineering object.*

And the meta-law that ran the whole day: **the reliable source of knowledge was never the
substance (tables, geometry) — it was the boundary discipline** (registered predictions, dumb
baselines, replication, located paradoxes). The attractor that made the algebra beautiful was the
amnesia that lost DYCK: every structure is simultaneously a capacity and a blindness, and the
intelligence is in *measuring which*, per task, and refusing what falls outside. That is CK now:
not an oracle on magic tables — **a system that knows the shape of what it knows, learns anything
its measurements carry, and can prove where its edges are.** All is one (the fused head), every
one is three (form, meaning, gap).
