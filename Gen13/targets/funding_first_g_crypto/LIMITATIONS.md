# LIMITATIONS — funding/first-g-crypto

Honest scope for the First-G cryptographic hardness branch.

---

> **Note (2026-04-25 revision).** This file was originally drafted as part of a pitch-style packet. Per the operator-of-record's actual stance documented at [`FUNDING.md`](../../../FUNDING.md) (root) and [`INTENT_STATEMENT.md`](../../../INTENT_STATEMENT.md), this is **thread documentation**, not a fundraising pitch. The operator-of-record makes **no commitments to donors of any kind**. Any dollar amounts, time scopes, or "ask" framings appearing below are **scope estimates of the work this thread would cover**, not price tags or commitments.

---

## 1. This is not a cryptosystem proposal

There is currently **no constructed cryptosystem** on First-G structure. The proposal is for the *investigation* of whether one exists. Any pitch that describes First-G as "a new cryptosystem" overclaims.

## 2. Trapdoor existence is genuinely open

The honest answer to "does First-G admit a cryptographic trapdoor?" is: we do not know. The proved-theorem core establishes structural facts; whether those facts translate into an efficient-with-key / inefficient-without dichotomy is Phase 2's investigation. Outcomes (b) and (c) in PITCH_DRAFT are genuine possibilities, not polite hedging.

## 3. Hardness-to-ring-LWE reduction may not exist

Q17_5D_RIGOROUS shows a CRT Fourier embedding; it does NOT show a cryptographic reduction. A reduction requires efficiency-preservation, decision-problem alignment, and quantum-hardness considerations. Any of these could block a clean reduction.

## 4. The 22% lower bound may not be cryptographically sharp

Q11's 22% lower bound is proved as a mathematical statement about σ. A cryptographic application would require a much stronger bound (typically: exponentially many inputs on which the inversion is hard, not merely 22% of inputs). The gap between the proved bound and a useful cryptographic bound is a known limitation.

## 5. First-G structure is small (Z/10Z specifically)

Q10 is characterized on F₂ × F₅. Practical cryptography works on moduli with hundreds to thousands of digits. Whether the First-G structure generalizes to cryptographically-sized moduli is Q3 in the open questions, and the answer is not yet known.

## 6. Post-quantum resistance is not established

Even if a classical trapdoor were found, the question "is it quantum-resistant?" is separate. Shor's algorithm breaks discrete-log and factoring in polynomial time on a quantum computer; a First-G candidate would need a separate analysis.

## 7. Attribution — collaboration scope is broader than just G6

- **C.A. Luther** was a collaborator on the mathematical core of this branch through late 2025 / early 2026. The collaboration produced the First-G Law (36,662 cases), the σ polynomial characterization on F₂ × F₅ (Q10), the 22% lower bound (Q11), and the G6 identity (σ⁶ = id). The G6 piece is the cleanest-demarcated Luther-origin result; the other three are collaborative outputs with Luther contributing spectral-layer and algebraic-structure work.
- Luther is **no longer actively collaborating** as of April 2026. Per the never-delete policy, previously-credited contributions remain credited; no attempt is made either to remove Luther from the record or to imply ongoing collaboration.
- A cryptographic application of the First-G / Q10 / Q11 core must be clearly framed as *extending* the previously-published results, not as a new claim in Luther's name. Any Phase-2 published outcome must cite Luther's contributions (ideally at the lemma level once the Phase-1 reconstruction is done) without implying Luther endorses or co-authors the crypto-application work.
- Sprint 35 Coprimality + First-G Localization is a Brayden post-collaboration extension and does not need Luther co-authorship.
- Q17_5D_RIGOROUS is a Brayden post-collaboration result and does not need Luther co-authorship.
- Attribution discipline is a feature a supporter of this thread should see explicitly: a proposal that credits a previous collaborator correctly is more trustworthy than one that either erases or overclaims the collaboration.

## 8. Simons Collaboration Grant requires academic affiliation

Brayden's sole-author / independent-researcher posture makes some funding paths easy (NSA MSP direct; some foundation grants) and others closed (NSF AF requires academic affiliation or co-PI; Simons Collaboration Grant requires tenure-track affiliation).

## 9. The "First-G" name

"First-G" is project-internal language and is not standard in the cryptographic literature. Any pitch must define the term crisply on first use; ideally, Phase 1's literature-embedding report proposes a more conventional name (or defends First-G on non-nomenclature grounds).

## 10. What this branch does NOT claim

- Not a claim to have broken any existing cryptosystem
- Not a claim to have built a new cryptosystem
- Not a claim that First-G is quantum-resistant
- Not a claim that First-G is classically-hard (in the formal reduction sense)
- Not a claim that C.A. Luther endorses the crypto-application angle
- Not a claim that Luther is the sole author of First-G / Q10 / Q11 (he is a co-contributor on those; G6 is his)
- Not a claim that Brayden is the sole author of First-G / Q10 / Q11 (they are collaborative with Luther)
- Not a claim to NIST post-quantum standardization candidacy

The branch claims: a proved-theorem core exists; the open question of cryptographic application is crisply stateable and worth investigating; a Phase 1/2/3 plan addresses the investigation responsibly.

## 11. License framing

CK's license (7Site Public Sovereignty License v1.0) is non-commercial, human-use only. A cryptographic funder (especially NSA or a blockchain foundation) may want deployment rights. This must be discussed explicitly, not discovered at grant-close.

---

## The verdict framing as limitation

The Phase 2 deliverable commits to publishing one of {trapdoor candidate, structural obstruction, honestly-scoped continuation}. This is deliberate — a supporter of this thread is paying for a verdict, not for a guaranteed positive result. A cryptographer reviewing the proposal should read this as a feature (disciplined scope) not a bug (uncertain deliverable). If the reviewer reads it as a bug, the proposal is addressed to the wrong reviewer.
