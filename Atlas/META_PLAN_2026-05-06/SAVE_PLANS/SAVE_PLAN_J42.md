# SAVE PLAN — J42 (Discrete sinc² Identity in Finite-Dimensional QM)

**Date:** 2026-05-07
**Status:** SAVABLE with mechanical revisions; ARITHMETIC ERROR confirmed
**Target venue (revised):** *Letters in Mathematical Physics* (per referee + per-venue-cap)
**Verdict:** Keep. Math is correct; one number was mistyped; framing needs honesty about Fejér priority.

---

## §1 — What the referee caught

| # | Issue | Severity | Action |
|---|-------|----------|--------|
| 1 | Numerical value `sinc²(1/10) ≈ 0.9355` is wrong | MECHANICAL | Replace with `≈ 0.9675`. The closed form `25(√5-1)²/(4π²)` is correct. |
| 2 | Theorem 3.1 is the Fejér kernel (1900) | FRAMING | Acknowledge directly; reframe as "Fejér-kernel application to cyclic-group QM." |
| 3 | Corollary 4.2 prime restriction unnecessary | OVER-RESTRICTION | Generalize: first zero of R(·,f) is at k=f for any f≥2. |
| 4 | Proposition 4.1 mis-interprets overlap as probability mass | INTERPRETIVE | Restate as squared transition amplitude / overlap; remove "probability mass" language. |
| 5 | Per-venue cap (3rd JMP target this quarter) | LOGISTICS | Submit to LMP instead. Already documented in cover letter §6.3. |

---

## §2 — Independent verification (this referee-rigor pass)

Direct computation in Python:

```python
import numpy as np
from sympy import sqrt, pi, N

# Closed-form symbolic
val_sym = 25 * (sqrt(5) - 1)**2 / (4 * pi**2)
val = float(val_sym)
# = 0.9675312093

# Direct: sinc²(1/10) = sin²(π/10) / (π/10)²
direct = np.sin(np.pi/10)**2 / (np.pi/10)**2
# = 0.9675312093
```

**Step-by-step:**
- `(√5 - 1)² = 6 - 2√5 ≈ 1.5278640`
- `25 · 1.5278640 = 38.196601`
- `4π² = 39.478418`
- `38.196601 / 39.478418 = 0.967531`

**Conclusion:** The closed form is correct. The numerical value `0.9355` in the manuscript is a transcription error — the correct value is **`0.9675`** (or `0.9676` if rounded after more digits).

---

## §3 — Why this is salvageable

The error is *not* a logic error. The closed form `25(√5-1)²/(4π²)` is correctly derived from `sin(π/10) = (√5-1)/4` (Ptolemy's identity for the regular pentagon). The closed form when evaluated correctly gives `0.9675`. Someone wrote down the wrong decimal digits in §4.3.

After the corrections in §4 below, the paper is:
1. A clean LMP-style short note (5-8 pages).
2. A correctly-attributed Fejér-kernel application to QM-on-cyclic-group.
3. Free of the over-restriction in Corollary 4.2.
4. Honest about the Proposition 4.1 interpretive scope.

The note is **not novel as a closed-form identity** (Fejér 1900) but **is novel as a unified QM-on-Z/N-with-arithmetic-bridge presentation**. That's an LMP-appropriate contribution.

---

## §4 — Concrete edits to the manuscript

### Edit 1 — Fix §4.3 numerical value (CRITICAL)

In `manuscript/J15_DiscreteSinc2_QM_JMathPhys.md` line 103:

```
$$\sinc^2(1/2) = 4/\pi^2 \approx 0.4053, \qquad \sinc^2(1/10) = \frac{25(\sqrt{5}-1)^2}{4\pi^2} \approx 0.9355.$$
```

**Replace with:**

```
$$\sinc^2(1/2) = 4/\pi^2 \approx 0.4053, \qquad \sinc^2(1/10) = \frac{25(\sqrt{5}-1)^2}{4\pi^2} \approx 0.9675.$$
```

(The closed form `25(√5-1)²/(4π²)` is correct; only the decimal needs fixing.)

### Edit 2 — Acknowledge Fejér kernel in §3 proof (FRAMING)

Add a one-line acknowledgement after Theorem 3.1's proof:

> *Remark.* The kernel $R(k, f)$ is the **Fejér kernel** [Fejér 1900] evaluated at $\theta = 2\pi/f$ and $n = k$, normalized so that $\sum_k R(k,f)$ approximates $\sinc^2$ in the continuum limit. The closed form is therefore not new; the contribution of this note is the QM interpretation on the cyclic Hilbert space and the arithmetic-bridge synchronization (§5).

### Edit 3 — Generalize Corollary 4.2 (OVER-RESTRICTION)

In §4.2, replace the prime restriction with the unrestricted statement:

```
**Corollary 4.2 (First zero of R).** For every $f \ge 2$ and every $k \in \{1, \dots, f-1\}$, $R(k, f) > 0$. At $k = f$, $R(f, f) = 0$. Hence the first integer zero of $R(\cdot, f)$ in $\mathbb{Z}_{\ge 1}$ is exactly $k = f$.

*Proof.* For $1 \le k \le f-1$, $f \nmid k$ (since $k < f$ and $k \ne 0$), so $\sin(\pi k/f) \ne 0$. At $k = f$, $\sin(\pi f/f) = 0$. The prime structure of $f$ is not used. $\qed$
```

The prime structure is needed only at Proposition 5.1 (the synchronization), where one needs `gcd(k, b) = 1` for `1 ≤ k < p₁`. Move that argument to §5 where it actually plays a role.

### Edit 4 — Reformulate Proposition 4.1 (INTERPRETIVE)

In §4.1, replace the "position-space probability mass" language with the squared overlap interpretation:

```
**Proposition 4.1 (Squared overlap with normalized window).** *The squared transition amplitude between a momentum eigenstate $|\hat p\rangle$ ($\hat p = N/f$, $f \mid N$) and the normalized rectangular position window $|w_k\rangle = k^{-1/2}\sum_{j=1}^k |j\rangle$ is*
$$|\langle \hat p | w_k\rangle|^2 = \frac{k}{N} \cdot R(k,f) = \frac{1}{N} \cdot \frac{\sin^2(\pi k/f)}{\sin^2(\pi/f)}.$$
*The continuum limit $N, f \to \infty$ with $k/f \to t$ recovers the standard $\sinc^2(t)/N$ scaling.*
```

Drop the "probability mass" language. The actual probability of finding `|p̂⟩` in `{1,...,k}` under position measurement is `k/N` (uniform marginal); `R(k,f)` is the *fidelity* / *overlap* with the window state, which is a different object and is the kernel of practical interest.

### Edit 5 — Add a 10-line verification script

Create `manuscript/verify_J42_sinc2.py`:

```python
"""J42 verification: discrete sinc² identity at machine precision."""
import numpy as np
from sympy import sqrt, pi, N as snum

def R_geom(k, f):
    j = np.arange(1, k+1)
    s = np.sum(np.exp(2j * np.pi * j / f))
    return abs(s)**2 / k**2

def R_closed(k, f):
    return np.sin(np.pi*k/f)**2 / (k**2 * np.sin(np.pi/f)**2)

def main():
    # Theorem 3.1: closed form matches geometric sum
    max_dev = 0.0
    for f in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 17, 19, 23]:
        for k in range(1, f+2):
            dev = abs(R_geom(k, f) - R_closed(k, f))
            max_dev = max(max_dev, dev)
    print(f"Theorem 3.1 max deviation across f in [3..23], k in [1..f+1]: {max_dev:.2e}")
    assert max_dev < 1e-12, "Closed form fails"

    # Corollary 4.2 (unrestricted): first zero at k=f for all f >= 2
    for f in [2, 3, 4, 5, 6, 8, 9, 10, 12, 15]:
        for k in range(1, f):
            assert R_closed(k, f) > 0, f"Unexpected zero at f={f}, k={k}"
        assert abs(R_closed(f, f)) < 1e-12, f"Expected zero at k=f={f}"
    print("Corollary 4.2 (unrestricted): first zero at k=f confirmed for f in [2..15]")

    # Special value sinc^2(1/10) = 25(sqrt(5)-1)^2/(4*pi^2) = 0.9675...
    closed_sym = 25 * (sqrt(5) - 1)**2 / (4 * pi**2)
    val = float(closed_sym)
    direct = np.sin(np.pi/10)**2 / (np.pi/10)**2
    print(f"sinc^2(1/10) closed form: {val:.10f}")
    print(f"sinc^2(1/10) direct     : {direct:.10f}")
    assert abs(val - 0.9675312093) < 1e-9, "sinc^2(1/10) value wrong"
    print("Special value sinc^2(1/10) ≈ 0.9675 confirmed")

if __name__ == "__main__":
    main()
```

### Edit 6 — Title and §1 reframe (OPTIONAL)

Title is acceptable as-is. If a stronger reframe is wanted: "*The Fejér Kernel on Cyclic-Group Quantum Mechanics: A Closed Form, a First-Zero Theorem, and an Arithmetic Bridge*."

---

## §5 — What this paper is *now* (after corrections)

**PROVEN:**
- Theorem 3.1 (closed form for R(k,f) — the Fejér kernel; cited correctly).
- Corollary 4.2 (first zero at k=f for any f≥2).
- Theorem 4.3 (continuum limit to sinc²(t)).
- Proposition 5.1 (synchronization with First-G event for f = spf(b)).

**COMPUTED:**
- Machine-precision verification across f ∈ {3,4,5,...,23}, k ∈ {1,...,f+1}.
- Special value sinc²(1/10) = 25(√5-1)²/(4π²) ≈ 0.9675.

**STRUCTURAL RHYME:**
- The First-G event (companion paper J04) and the discrete sinc² zero coincide at k = spf(b) for any squarefree b > 1.

**OPEN:**
- Whether the deeper synchronization extends to multi-prime structure: does R(k, f) for f ranging over the prime factors of b encode the full coprimality structure?

---

## §6 — Recommended action

1. Apply Edits 1-5 to `manuscript/J15_DiscreteSinc2_QM_JMathPhys.md`.
2. Add `manuscript/verify_J42_sinc2.py` (Edit 5).
3. Update README §5 to reflect the Fejér-attribution reframe and the LMP venue path (concur with cover letter §6.3 fallback).
4. Submit to *Letters in Mathematical Physics* (preferred fallback per cover letter; per-venue cap acknowledged).

**Estimated revision effort:** 1-2 hours of editing. No new mathematics required.

**Verdict:** SAVE. Math is correct; one number was mistyped; framing needs Fejér acknowledgement and venue swap.
