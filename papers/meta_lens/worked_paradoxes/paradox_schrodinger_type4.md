# Worked Template [O-2] — Schrödinger's Cat

**Classification: UOP Type IV — Time-Consistency Failure**
**Branch:** `paradox-classifier-2026-04-24`
**Lens match:** primary — wave mechanics / nonlinear PDE;
secondary — ergodic / transfer-operator theory (measurement as
projection onto a spectral basis).

---

## Slot 1 — Objects

`X = ` density-matrix states of the joint system

```
S = (unstable nucleus) ⊗ (trigger + vial) ⊗ (cat) ⊗ (box interior)
```

inside a hermetically sealed, thermally isolated box. Parameter:
time `t ∈ [0, Δt]`. Initial state `ρ(0) = |alive⟩⟨alive|` with the
nucleus unexcited. The Hilbert space is finite-dimensional for the
two observables of interest (`alive`, `dead`), but the full space
is whatever is needed to carry the nuclear decay dynamics.

## Slot 2 — Observables

Two time-indexed observables:

- `f_U : [0, Δt] → States`, the **unitary-evolution** observable,
  defined by `f_U(t) = e^{−iHt/ℏ} ρ(0) e^{+iHt/ℏ}`. Under this
  rule `f_U(Δt)` is (for suitable `H, Δt`) a macroscopic
  superposition `(|alive⟩ + |dead⟩)/√2` up to phases.

- `f_M : [0, Δt] → States`, the **measurement-postulate**
  observable, defined by: when the box is opened at `t = Δt`, the
  state projects onto `|alive⟩⟨alive|` with probability `|α|²`
  and onto `|dead⟩⟨dead|` with probability `|β|²`, where
  `α, β` are the Schrödinger amplitudes.

The joint observable is the **time-consistency check** `J(t) =
(f_U(t), f_M(t))`.

## Slot 3 — UOP verdict

**`J(t)` fails to be time-consistent at `t = Δt`.** The two rules
prescribe structurally incompatible futures:

- `f_U(Δt)` is an off-diagonal density matrix
  `ρ_U(Δt) = |α|²|alive⟩⟨alive| + |β|²|dead⟩⟨dead| + α β*|alive⟩⟨dead| + α* β|dead⟩⟨alive|`.
- `f_M(Δt)` is a diagonal, stochastically-selected pure state:
  either `|alive⟩⟨alive|` or `|dead⟩⟨dead|` with classical
  probabilities `|α|², |β|²`.

`f_U ≠ f_M` generically, and not by a phase: the off-diagonal
coherences `|alive⟩⟨dead|, |dead⟩⟨alive|` are destroyed in `f_M`.

This is **not** fixable by adding another static observable
(Type I): the two rules both read state at a single instant, so
no extra observable at that instant reconciles them. It is **not**
a missing r.e. invariant (Type II). The objects are perfectly
admissible (Type III). The failure is between **two evolution
laws** both claimed to apply to the same `(state, time)` pair.

This is the defining Type IV signature.

## Slot 4 — Type

**Type IV — Time-Consistency Failure.** Two dynamical rules
(unitary evolution vs. projection-on-measurement) are both
sanctioned by the formalism, but they produce different `ρ(Δt)`
from the same `ρ(0)`. The obstruction lives on the **time axis**,
in the composition of evolution operators, not in the state or
observable space.

## Slot 5 — Fix

Every live interpretation of quantum mechanics is, structurally, a
Type IV fix. Each picks a different way to make the evolution law
single-valued.

- **Decoherence + consistent histories (Zurek 2003).** Unitary
  evolution is kept exact; the cat-vial-nucleus subsystem is
  strongly coupled to environmental degrees of freedom. Tracing
  out the environment gives a reduced density matrix whose
  off-diagonal terms decay on timescale
  `τ_dec ≈ ℏ²/(2 m k_B T λ²_dB)`, extraordinarily fast for
  macroscopic bodies. `f_M` is recovered as an emergent classical
  limit of `f_U` once environment is accounted for. Does not
  solve the preferred-basis problem by itself — needs einselection.

- **Many-Worlds (Everett 1957).** There is no collapse. Only
  `f_U` is real. The "cat observer" becomes a branch label in the
  universal wavefunction, and `|alive⟩` and `|dead⟩` are both
  realized on different Everett branches. `f_M` is an epistemic
  artifact of being on one branch.

- **Objective collapse (GRW — Ghirardi, Rimini, Weber 1986).**
  Modify the Schrödinger equation itself by adding a stochastic
  nonlinear localization term. Microscopic systems evolve
  effectively unitarily; macroscopic ones collapse on short
  timescales. One law, stochastic — `f_U = f_M` by construction.

- **Pilot-wave / Bohmian mechanics (Bohm 1952, de Broglie 1927).**
  Keep the wavefunction, add a hidden particle trajectory guided
  by the quantum potential. Measurement outcomes are determined
  by the actual trajectory; `f_U` is the guiding field, `f_M` is
  the trajectory record. Single law, two variables.

- **QBism (Fuchs, Mermin, Schack 2014).** The state is an agent's
  personal probability assignment, not ontic. `f_U` is how the
  agent updates in the absence of new data; `f_M` is how they
  update on a personal outcome. Type IV dissolves because the
  "state" was never a third-person object.

- **Consistent histories (Griffiths 1984).** Restrict to
  "consistent" families of projections along the time axis. Only
  those families that obey a decoherence condition get
  probability assignments. The paradox is the artifact of mixing
  non-consistent families.

The Type IV structure is preserved across all these fixes: each
commits to a **single** evolution law by either (a) deriving
`f_M` from `f_U` plus environment (decoherence, MWI), (b)
modifying `f_U` to include collapse (GRW), or (c) reinterpreting
the state so only one rule was ever needed (QBism, Bohmian).

## Slot 6 — Cite

- **Schrödinger, E. (1935).** *Die gegenwärtige Situation in der
  Quantenmechanik.* Naturwissenschaften 23, 807–812, 823–828,
  844–849. The original cat thought-experiment.
- **Everett, H. (1957).** *"Relative State" Formulation of Quantum
  Mechanics.* Reviews of Modern Physics 29, 454–462. Many-worlds.
- **Bohm, D. (1952).** *A Suggested Interpretation of the Quantum
  Theory in Terms of "Hidden" Variables, I & II.* Physical Review
  85, 166–179, 180–193.
- **Ghirardi, G. C., Rimini, A., & Weber, T. (1986).** *Unified
  dynamics for microscopic and macroscopic systems.* Physical
  Review D 34, 470–491. GRW collapse.
- **Griffiths, R. B. (1984).** *Consistent histories and the
  interpretation of quantum mechanics.* Journal of Statistical
  Physics 36, 219–272.
- **Zurek, W. H. (2003).** *Decoherence, einselection, and the
  quantum origins of the classical.* Reviews of Modern Physics 75,
  715–775.
- **Fuchs, C. A., Mermin, N. D., & Schack, R. (2014).** *An
  introduction to QBism with an application to the locality of
  quantum mechanics.* American Journal of Physics 82, 749–754.

---

## Why this is cleanly Type IV and not Type I, II, or III

- **Not Type I (Injectivity Failure).** Adding a new static
  observable at `t = Δt` cannot reconcile `f_U` and `f_M`; they
  already disagree about what the state *is* at that instant.
  The defect is not in the observable algebra at a fixed time.
- **Not Type II (Missing Invariant).** No hidden structural
  invariant is missing from the single-time state space — the
  Hilbert space and its observables are complete. Hidden-variable
  interpretations (Bohm) *add* a dynamical variable to change the
  evolution law, which is a Type IV fix, not a Type II discovery.
- **Not Type III (Admissibility Failure).** The cat-in-box system
  is a legitimate physical system. The state `ρ(0)`, the
  Hamiltonian `H`, the projection operators all pass
  well-formedness. The two evolution rules are both admitted by
  standard QM — that is precisely the tension.
- **Type IV is the only remaining slot.** Two legitimate
  dynamical rules, two different `ρ(Δt)` from the same `ρ(0)`,
  obstruction living on the time axis.

## Connection to the PDE / wave-mechanics lens

The Schrödinger equation `iℏ ∂_t ψ = H ψ` is a linear evolution
PDE — perfectly Type-IV-clean on its own. The paradox arises only
when a **second, nonlinear** update rule (projection) is
conjoined. Nonlinear modifications like BB log (Bialynicki-Birula
& Mycielski 1976) or GRW live in exactly this region of the
atlas: single-valued evolution laws that reproduce measurement
statistics without a second update rule. The UOP Type IV cell
matches the mathematical-physics literature on objective-collapse
models almost directly.

## Connection to the ergodic / transfer-operator lens

Measurement-as-projection onto a spectral basis is a transfer
operator acting on states. In the absence of decoherence-induced
pointer basis selection, the basis is arbitrary. Zurek's
einselection is the transfer-operator argument that the
environment picks out a unique basis on a short timescale, making
`f_M` derivable from `f_U`. The two lenses speak the same
underlying mathematics here; this is one of the atlas's cleaner
cross-lens agreements.

## Connection to CK's live classifier

`coherencekeeper.com/paradox` currently hardcodes Schrödinger's
cat as Type IV with the short verdict: "Unitary evolution and
measurement projection disagree about `ρ(Δt)`." This template is
the expanded six-slot form of that hardcoded verdict.

---

**Runnable classifier target ([O-1]):** the template above is the
input schema for `classify_paradox.py` when it exists. A JSON
instance of this template feeds into the classifier and returns
`(type = IV, fix = "single-valued dynamics via decoherence / MWI / GRW / Bohm / QBism")`.
