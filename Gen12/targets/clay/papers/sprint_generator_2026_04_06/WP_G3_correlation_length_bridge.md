Done. The paper is written and saved at:

`C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen12\targets\clay\papers\sprint10_flatness_2026_04_06\WP-G3_CORRELATION_LENGTH_UOP_BRIDGE.md`

Here is what was produced:

**Structure (10 sections + appendix)**

- **§2 Transfer Matrix**: Full derivation of T, exact eigenvalues λ₊ = 2cosh(βJ) and λ₋ = 2sinh(βJ), partition function for general n and explicit n=4 case (with two-temperature sanity checks), free energy per site with finite-n corrections. All marked [PROVED].

- **§3 Two-Point Correlator**: Complete transfer matrix proof using the spin operator Σ in the eigenbasis. Exact formula ⟨σ₀σⱼ⟩ = (r^{n-j} + rʲ)/(1+rⁿ) with r = tanh(βJ), plus two independent derivations of the thermodynamic limit. Both marked [PROVED].

- **§4 Correlation Length**: ξ = −1/ln(tanh βJ), both limiting behaviors with derivations, physical interpretation. [PROVED].

- **§5 Bridge Conjecture**: Precise formal definition of the window map f_w, the UOP score via conditional entropy, and the information radius r_θ. The conjecture states r_θ ~ C(θ)·ξ with C(θ) = |ln(1−θ)| explicit. Marked [STRUCTURAL ANALOGY].

- **§6 Evidence For**: Three independent threads — exponential decay rate match, the eigenvalue ratio tanh(βJ) as common ground for both objects, geometric score decay.

- **§7 Caveats**: Four precise obstacles — the combinatorial/analytic interface gap, boundary effects for finite n, discreteness of |R(f_w)| vs continuity of ξ, absence of a phase transition threshold.

- **§8 What Constitutes a Proof**: Lemma 8.1 (entropy = UOP score), Theorem 8.2 (exponential decay of |R(f_w)|), and the single Clinching Lemma that would close everything.

- **§9 T* Connection**: The formula r_{T*} = ξ·ln(7/2) ≈ 1.253·ξ is derived explicitly; whether T* = 5/7 is distinguished in the Ising spectrum is left [OPEN] with five specific sub-questions.

- **Appendix A Python**: Computes ξ(β) table, correlation decay table (with Fibonacci separation values), ASCII bar-chart of ⟨σ₀σⱼ⟩ at β=1.0, finite-size comparison (exact vs n→∞), and the UOP information radius table with the T* = 5/7 column highlighted. Summary claim table at the end classifies every statement.