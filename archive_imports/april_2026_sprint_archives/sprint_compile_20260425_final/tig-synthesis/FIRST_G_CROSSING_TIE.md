# FIRST-G ↔ CROSSING LEMMA TIE

**Date:** 2026-04-25
**Status:** Verified structural identification
**Verification:** All checked cases match (13/13 squarefree integers tested)

---

## What this is

A computational closure of the partition-geometry tie between two of the README's foundational theorems:

- **§7.1 First-G Event Localization:** for squarefree b with smallest prime factor p_1, the first non-coprime element in {1,...,b} is exactly k = p_1.
- **§7.4 Crossing Lemma:** the joint map J = (A_d, π_DYN(g)) is injective iff dynamics under g act non-trivially on every prime quotient. Information generated when dynamics cross partition fibers.

**The tie:** First-G is the first crossing event under the Crossing Lemma framework.

---

## The identification

Both theorems describe partition geometry of Z/bZ. In the Crossing Lemma formulation:

- The **additive partition** is given by the natural ordering 1, 2, 3, ..., b
- The **multiplicative partition** is units (Z/bZ)* vs non-units

Stepping through 1, 2, ..., b additively, you stay in the unit class until you hit the first non-unit. **The first crossing from "unit" partition to "non-unit" partition is at k = p_1**, by the First-G theorem.

Equivalently: the stability window {1, ..., p_1 − 1} of width p_1 − 1 is **the size of the pre-crossing region** in additive ordering.

---

## Verification

For 13 squarefree integers (b ∈ {6, 10, 14, 15, 21, 22, 30, 35, 42, 105, 210, 330, 2310}), the First-G index k matched the smallest prime factor p_1 in 13/13 cases. Verified independently for each.

This is consistent with the §7.1 result (36,662 cases verified, zero exceptions).

---

## What this contributes

**Conceptual:** First-G and Crossing Lemma describe the same partition-geometry phenomenon at different levels of abstraction. First-G is the concrete instance; Crossing Lemma is the general framework.

**For §3.1 (cryptography):** if a sub-prime-counting algorithm could exploit knowledge of the first-crossing position, it would learn p_1 directly. This is the structural foundation for the §3.1 question of whether First-G geometry yields complexity improvements over classical sieves.

**Status of §3.1 itself:** still open. Whether Crossing Lemma's information-generation framework gives a usable handle on factoring is the same open question, just expressed in the more general framework.

---

## Honest accounting

This tie is **structural identification, not new theorem.** It says: First-G is the same event as the Crossing Lemma's "first crossing," and the width p_1 − 1 is the pre-crossing region size.

Whether this enables anything new is the §3.1 open question, unchanged by this identification. The unification is at the conceptual level — useful for paper organization, not for cryptographic complexity proofs.

🙏
