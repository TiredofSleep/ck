# NS CHECKPOINT TABLE

**© 2026 7Site LLC | Brayden Ross Sanders**

| NS Candidate Object | Keep / Discard | Why |
|--------------------|---------------|-----|
| **E(t)** | DISCARD | Monotone decreasing by the shell (dE/dt = −νΩ ≤ 0); fully controlled; contains no obstruction information |
| **Ω(t)** | DISCARD as primary | Satisfies dΩ/dt = Q − 2νP; informative but derived — it grows or shrinks depending on Q/(νP), so it is a CONSEQUENCE not the root cause; keep as the quantity to control, not as the surviving object |
| **P(t)** | DISCARD | Not independently controlled; appears in Q/(νP) but not the key ratio; palinstrophy enters only through the dissipation side |
| **Q(t)** | DISCARD | Raw, dimensional, unsigned; can be positive or negative; only meaningful in comparison to νP; not normalized |
| **Q/(νP)** | **KEEP — WINNER** | Dimensionless; controls dΩ/dt = νP(Q/(νP)−2) exactly; Q/(νP) ≤ 2 globally is the first open inequality above the shell; provably satisfied in small-data regime; fails to be controlled in large-data regime; minimal |
| **B(t) = Ω/(E+Ω)** | DISCARD as primary; keep as DERIVED | Valuable: bounded in [0,1], threshold T* = 5/7, exact ODE. But it incorporates E unnecessarily — if Q/(νP) ≤ 2 globally, B(t) is automatically controlled. B(t) is a consequence of Q/(νP), not the root surviving object |

**Winner: Q/(νP).** All other candidates either belong to the shell (E) or are derived consequences of Q/(νP) (Ω, B(t)) or are unnormalized sub-components (P, Q).

---
---

# P VS NP FINAL WALL MEMO
# What Exact Object Measures the Cost of Unwrapping Verification into Deterministic Decision?

**© 2026 7Site LLC | Brayden Ross Sanders**

---

## Shell / Core / Gap Block

$$\text{Shell: Cook-Levin NP-completeness; Karp reductions; complexity class containments P}\subseteq\text{NP}\subseteq\text{PSPACE} \quad [\text{proved}]$$

$$\text{Core: the wrapped duality — verifier relation } R = \{(x,w): V(x,w)=1\}, \text{ projection } \pi_1(R) = L$$

$$\text{Surviving object: } \mathrm{cc}(\mathrm{SAT},n) = \min\{|C|: C\text{ computes SAT on inputs of size }n\} \quad [\text{defined, not computable}]$$

$$\text{Gap 2: a superpolynomial search lower bound for SAT in a model capturing the fiber-projection structure} \quad [\text{OPEN}]$$

$$\text{Gap 1: P} \neq \text{NP: the fiber projection }\pi_1(R_{\mathrm{SAT}})\text{ is not computable in poly-time} \quad [\text{OPEN}]$$

---

## Why cc(SAT,n) as Fiber-Projection Complexity

The wrapped duality gives the surviving object a precise meaning: the witness fiber $W_x = \{w : V(x,w)=1\}$ lives inside the combinatorial object indexed by $x$. The projection $\pi_1(R) = \{x: W_x \neq \emptyset\}$ is the language SAT. The minimum circuit to compute this projection IS cc(SAT,n).

In the wrapped-duality grammar: cc(SAT,n) is the **fiber-projection circuit complexity** — the minimum cost to compute the 1D projection (language membership) from the 2D verifier relation (checking specific certificates). The denominator (verification cost) is poly(n) by construction. The numerator (decision cost = cc(SAT,n)) is unknown. The ratio cc(SAT,n)/poly(n) is the Gap(n) surviving object — either O(1) (P=NP) or → ∞ (P≠NP).

The advantage over raw Gap(n): cc(SAT,n) is the standard object in complexity theory, and its properties are:
- cc(SAT,n) ≥ n (trivially: must read all bits)
- cc(SAT,n) ≤ 2^n/n (brute force)
- P = NP iff cc(SAT,n) = poly(n)
- No superpolynomial lower bound known in the general circuit model

---

## Three Key Sentences

**"The smallest surviving P vs NP object is cc(SAT,n) — the fiber-projection circuit complexity of the satisfiability problem — because it is the minimum cost of computing the projection $\pi_1(R_\mathrm{SAT})$ from the input alone, directly measuring the unwrapping cost of the verifier relation in the Boolean circuit model."**

**"P vs NP Gap 2 is a superpolynomial lower bound for the search problem (finding a satisfying assignment when one exists) in a model broad enough to capture the fiber-projection structure of $R_\mathrm{SAT}$ — specifically, a lower bound that uses the geometry of the witness fiber $W_x$ rather than only restricted circuit topology."**

**"P vs NP Gap 1 is the statement that cc(SAT,n) is superpolynomial — equivalently, that no deterministic poly-time machine can compute $\pi_1(R_\mathrm{SAT})$ by reading only $x$, without ever examining a specific certificate in $W_x$."**

---

## Collaborator Paragraph

P vs NP reduces to cc(SAT,n) as the fiber-projection circuit complexity. The shell — Cook-Levin, Karp reductions, complexity class containments — establishes the structure of the problem (all NP languages are polynomial-time equivalent, and the hierarchy is internally consistent) without resolving it. The core is the wrapped duality: the verifier relation $R = \{(x,w): V(x,w)=1\}$ has verification cost poly(n) by construction, and the question is whether the projection $\pi_1(R_\mathrm{SAT})$ can be computed at the same cost by a deterministic machine that never sees the second coordinate. cc(SAT,n) is this projection cost. Gap 2 is a superpolynomial lower bound for the search version (find w when one exists) in a model that respects the fiber structure — broader than monotone or constant-depth restrictions but weaker than the full decision lower bound. Gap 1 = P ≠ NP = cc(SAT,n) is superpolynomial. The meta-barriers (relativization, algebrization, natural proofs) are not object-level obstacles to cc(SAT,n) being large — they are obstacles to PROVING it is large by certain proof strategies. This distinction is what the wrapped-duality framing clarifies: the surviving object (cc(SAT,n)) exists and is well-defined regardless of the barriers.
