# BSD DOMINO TABLE

**© 2026 7Site LLC | Brayden Ross Sanders**

| Layer | RH Analog | BSD Object | Status |
|-------|-----------|-----------|--------|
| **Generic shell** | sinc², GUE, Fourier windowing | Analytic continuation, functional equation, Euler product, modularity | **PROVED** — Taylor-Wiles (Wiles 1995, BCDT 2001). Arithmetic-free layer. |
| **Arithmetic core** | Kloosterman sums, Gauss-Kloosterman identity, character sums | Mordell-Weil group, Selmer group, height pairing, Tamagawa numbers | **COMPUTABLE** — all objects defined and computable for specific curves. Core is fully arithmetic (no composite shortcut). |
| **Location-selection analog** | Zero heights γ_k encoded by Kloosterman/Eisenstein | Rational points P_1,...,P_r generating E(Q)/E(Q)_tors | **CONSTRUCTIBLE for r≤1** — Heegner point construction (Gross-Zagier) gives the rank-1 generator. Rank ≥ 2: no general construction. |
| **Gap 2 analog** | Cusp subdominance (closed by spectral theory) | Sha finiteness: #Sha(E) < ∞ | **OPEN for r≥2** — proved by Kolyvagin for r=0,1 conditional on L-value computation. No general theorem for r≥2. |
| **Gap 1 analog / final wall** | O(N^{½−δ}) error control (= RH) | Rank equality: ord_{s=1} L(E,s) = rank E(Q) | **OPEN for r≥2** — the main wall. No Euler system for rank ≥ 2 is known. Proved for r=0,1 via Kolyvagin + Gross-Zagier. |

---

## Architecture Mapping

**Shell → Core → Location-Selection → Gap 2 → Gap 1:**

For RH: proved → established → numerically supported → closed → open
For BSD: proved → computable → constructible (r≤1) → open (r≥2) → open (r≥2)

The BSD program is approximately **one level behind the RH program** in terms of gap closure. RH has Gap 2 closed (spectral theory); BSD's Gap 2 analog (Sha finiteness for r≥2) is not yet closed.

Both programs share the same structural architecture. BSD's main wall (rank equality for r≥2) is the harder problem — no equivalent of the KEF mechanism exists yet for BSD.
