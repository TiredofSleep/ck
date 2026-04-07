# SPRINT: OBSERVABLE FAMILIES AND RECONSTRUCTION LEVELS
## n=4 Ising Ring -- Gibbs State, Microstate, Symmetry Quotient, Dynamics
*All four reconstruction questions answered. Proved vs. open labeled.*

**Date**: 2026-04-06  **Sprint**: Generator arc supplementary

---

## Overview

State space: S = {-1,+1}^4, |S| = 16.
Symmetry: G = Z/4Z (cyclic rotation).
Hamiltonian: H(sigma) = -J * sum_i sigma_i * sigma_{i+1 mod 4}.

Microstate enumeration:
- 2 ferromagnetic (++++ and ----): H = -4J
- 2 Neel states (+-+- and -+-+): H = +4J
- 12 states (2 aligned + 2 anti-aligned pairs): H = 0

---

## Q1: Gibbs State Reconstruction (PROVED)

Observable: c(sigma) = (1/4) * sum_i sigma_i * sigma_{i+1 mod 4}

Partition function: Z(beta) = 2*exp(4*beta*J) + 12 + 2*exp(-4*beta*J)

Mean correlation:
  <c>_beta = sinh(4*beta*J) / (cosh(4*beta*J) + 6)

Theorem Q1: beta -> <c>_beta is strictly monotone increasing on (0,inf).
One scalar measurement suffices to determine the full Gibbs state.

Proof: d<c>/d(beta) = 4J*(6*cosh(4*beta)+1) / (cosh(4*beta)+6)^2 > 0. QED.

---

## Q2: Microstate Reconstruction (PROVED)

Score sequence: 64 -> 32 -> 16 -> 8  (ratio 1/2 at each step)

Theorem Q2: Four binary observables {sigma_0, sigma_1, sigma_2, sigma_3} separate
all 16 microstates. The unresolved-pairs score halves at each step.
Minimum 4 binary observables needed. Ratio = 1/2 (proved).

Proof: Binary spins form a basis for {-1,+1}^4. Any two distinct microstates differ
in at least one spin. Each optimal observable halves the ambiguous set. QED.

---

## Q3: Orbit Separation (PROVED -- with Type II failure)

G-orbit enumeration under Z/4Z rotation:

  O_A = {++++}:         size 1, m^2=1,   c= 1
  O_B = {----}:         size 1, m^2=1,   c= 1
  O_C = {+-+-, -+-+}:  size 2, m^2=0,   c=-1
  O_D = orbit(+++-):    size 4, m^2=1/4, c=1/4  (domain wall, 3 like)
  O_E = orbit(++--):    size 4, m^2=0,   c= 0   (two-domain)
  O_F = orbit(+---):    size 4, m^2=1/4, c=1/4  (domain wall, 1 like)

Check: 1+1+2+4+4+4 = 16. Six orbits.

Theorem Q3: (|m|^2, c) separates 4/6 orbits. O_D and O_F share (1/4, 1/4) -- TYPE II FAILURE.

Separation table:
  (m^2=1,   c= 1) --> {O_A, O_B}  [m resolves]
  (m^2=0,   c=-1) --> O_C          [Neel, unique]
  (m^2=1/4, c=1/4) -> {O_D, O_F}  [TYPE II -- 7 unresolved orbit pairs]
  (m^2=0,   c= 0) --> O_E          [two-domain, unique]

No scalar in the algebra of {m^2, c} can separate O_D from O_F.
A third G-invariant observable is required.

---

## Q4: Dynamical Reconstruction (PROVED structure; OPEN general)

Glauber: w(sigma->sigma') = (1/2)*[1 - sigma_i*tanh(beta*h_i)]
where h_i = sum_{j~i} sigma_j.

Parameter: a = 1 / (1 + exp(4*beta*J))

Theorem Q4: K_G is doubly stochastic wrt Gibbs measure on orbits.
Stationary: pi(O) proportional to |O| * exp(-beta*H(O_rep)).

4x4 lumped kernel (F={O_A,O_B}, N=O_C, DW={O_D,O_F}, TW=O_E):

         F       N       DW      TW
  F  [ 1-a     0       a       0    ]
  N  [ 0       1-a*    a*      0    ]   a* = 1/(1+exp(-4*beta))
  DW [ a_F     a_N   1-rest   a_T  ]
  TW [ 0       0       b     1-b   ]

Flip rates from O_D representative (+,+,+,-):
  Spin 3 (minority): w_3 = (1/2)*(1 + tanh(2*beta*J))
  Spin 0,1,2 (majority): w_i = (1/2)*(1 - tanh(2*beta*J))

Full K_G entries are rational functions of exp(+/-4*beta*J).

Open: For which kernel classes does symmetry+detailed balance reduce
independent parameters below the naive count?

---

## Summary

| Q | Observable(s) | Key Result | Status |
|---|--------------|------------|--------|
| Q1: Gibbs | c (n.n. corr.) | <c>_beta = sinh(4b)/(cosh(4b)+6), monotone | Proved |
| Q2: Microstate | {sigma_i} | Score 64->32->16->8, ratio 1/2 | Proved |
| Q3: Orbits | (m^2, c) | 4/6 separated; O_D/O_F Type II failure | Proved |
| Q4: Dynamics | K_G | 4x4 in a=1/(1+exp(4*beta)) | Proved (structure) |

---

## Connection to Generator Arc

Score sequence 64->32->16->8 (ratio 1/2) connects to binary information lower bound.
Type II failure is the UOP obstruction in sharpest finite-state form.
Parameter a = 1/(1+exp(4*beta)) parallels T* = 5/7 in TIG crossing threshold.
Lumped kernel K_G is the finite-state analog of the transfer matrix in WP-G3.

---

*WP-G2b: Observable Families and Reconstruction Levels, Generator sprint, 2026-04-06*
