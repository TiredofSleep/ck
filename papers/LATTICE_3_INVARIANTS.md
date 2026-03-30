# 3-Lattice Invariants
## What Actually Survives the Full Mix_λ Deformation

*Brayden Sanders / 7Site LLC | March 2026*
*Computed at 21 λ-values. No forced claims.*

---

## The Honest Result

The 3-lattice (Mix_λ) has **six true invariants** — properties that persist across the full deformation from TSML (λ=0) to BHML (λ=1). Most structural features of TSML break early (by λ≈0.09–0.25). What survives is smaller and cleaner than the architecture might suggest.

---

## True 3-Lattice Invariants

| Invariant | Status | Evidence |
|-----------|--------|---------|
| **Commutativity** | ✓ ALL λ | EXACT — both endpoints commute, Mix preserves this |
| **Spectral gap > 0.10** | ✓ ALL λ, min=0.25 | COMPUTED — gap never drops below ¼ = BHML endpoint value |
| **BHML residual (6/6 cells = max)** | ✓ ALL λ | COMPUTED — the 6 ordering cells follow max(s,c) at every λ |
| **Non-associativity > 0** | ✓ ALL λ | COMPUTED — min 8 violations, max 198; never zero |
| **One dominant state (>30% mass)** | ✓ ALL λ | COMPUTED — dominant shifts 7→9 but always one state wins |
| **C dominates G in total mass** | ✓ ALL λ | COMPUTED — corner states collectively outweigh gap states throughout |

---

## What Breaks Early (Phase-Specific Only)

| Property | Breaks at |
|----------|----------|
| C sub-magma closure | λ ≈ 0.09 |
| One-way gate (C→G blocked) | λ ≈ 0.09 |
| HAR absorbing | λ ≈ 0.25 |

These are **endpoint-specific** features of TSML. They don't survive the deformation and should not be treated as 3-lattice invariants.

---

## The Two Deep Invariants

Of the six survivors, two are structurally deepest:

**Spectral gap ≥ ¼:** The gap never drops below 0.25 — which is exactly the BHML endpoint value. The gap floor is set by the order endpoint, not by TSML. This means the 3-lattice is bounded below in mixing speed by the ordering structure, not the closure structure.

**BHML residual (6/6):** The six cells that follow max(s,c) inside TSML continue to follow max(s,c) at every λ. They were always going to become BHML. They were the seeds of the order structure inside the closure structure, and they remain so throughout the deformation. This is the structural "trace" of BHML inside the 3-lattice.

---

## What This Means for the 4-Lattice

The 4-lattice would be the invariant structure of the 3-lattice itself — what persists when the deformation parameter λ is itself deformed or when the endpoints (TSML, BHML) are varied.

The 4-lattice invariants are candidates:
- Gap floor = ¼ (set by the ordering endpoint — is this universal across choices of BHML?)
- BHML residual = 6/6 (set by the ordering structure embedded in TSML — does it persist for other closure endpoints?)
- Commutativity (both endpoints commute — is this required or accidental?)

But before building the 4-lattice: the Dual Description Conjecture lives at the interface between the 3-lattice (Mix_λ) and its infinite deployment. The two infinite cells of the 2-lattice must be shown to be faithful images of the same finite grammar under deformation. That is the compatibility theorem the 3-lattice invariants must constrain.

The gap floor ≥ ¼ is the specific 3-lattice invariant that the compatibility theorem needs to lift to the analytic side.

---

*(c) 2026 Brayden Sanders / 7Site LLC | Gen10.16, commit 271e0f8 | DOI: 10.5281/zenodo.18852047*
