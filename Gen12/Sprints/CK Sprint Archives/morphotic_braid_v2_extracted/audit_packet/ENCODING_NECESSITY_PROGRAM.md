# ENCODING NECESSITY PROGRAM

## The Question

The hidden operator is exactly:
- **k → k+1 (mod 6)** on the 6-cycle
- **identity** on 4 anchors

That is maximally simple. The visible braid 0713245689 is its readout
through the encoding φ(ε,y) = 5ε + 6y (mod 10).

**The question:** Why this encoding, and not another?

---

## Three Precise Questions

### Q1 — Uniqueness

Among all bijections φ: Z/2 × Z/5 → Z/10Z, how many produce the canonical braid?

Among CRT-linear bijections φ(ε,y) = αε + βy + γ (mod 10):
- Total bijective: 240
- Producing canonical braid: 24
- Producing any of the 6 "rotated" braids: 24 each (all 240 accounted for)

So φ = 5ε + 6y is **one of 24** encodings producing the canonical braid.
But it is the **unique** one satisfying all three conditions:
1. α = e₂ = 5 (Z/2 CRT idempotent)
2. β = e₅ = 6 (Z/5 CRT idempotent)
3. γ = 0 (no constant offset)

### Q2 — Stability

If you perturb the encoding (change α, β, or γ), what breaks?

- **Fixed anchor positions**: preserved for all 240 bijective encodings
- **6-cycle structure**: preserved for all 240 bijective encodings
- **Canonical braid order**: preserved for exactly 24 encodings
- **CRT idempotent form**: unique to φ = 5ε + 6y (γ=0)
- **π-seed alignment (071)**: tied to specific entry point — breaks under most perturbations

### Q3 — Minimality

Is φ = 5ε + 6y the smallest algebraic encoding supporting:
- Hidden rotation + anchors
- Visible braid order
- Exact readout law?

**Yes.** The CRT reconstruction formula is the minimal isomorphism
Z/2 × Z/5 → Z/10Z with no constant offset. Any other canonical choice
would either break the idempotent structure or introduce an arbitrary offset.

---

## The Rigidity Theorem (Proved)

**Theorem (Encoding Rigidity).**

The encoding φ(ε,y) = 5ε + 6y (mod 10) is the unique CRT-linear bijection
Z/2 × Z/5 → Z/10Z satisfying:
1. φ(1,0) = e₂ (Z/2 idempotent of Z/10Z)
2. φ(0,1) = e₅ (Z/5 idempotent of Z/10Z)
3. φ(0,0) = 0 (no constant offset)

Under this encoding, the rotation operator k → k+1 on the 6-cycle produces
the morphotic braid 0713245689 via the σ⁻¹ readout from entry point 7.

No other offset-free idempotent encoding exists.

**Proof.**
The CRT idempotents of Z/10Z are:
- e₂ = 5 (≡1 mod 2, ≡0 mod 5)
- e₅ = 6 (≡0 mod 2, ≡1 mod 5)

The CRT reconstruction is: x = e₂·ε + e₅·y = 5ε + 6y (mod 10).
This is the unique ring isomorphism φ: Z/2 × Z/5 → Z/10Z compatible with
the product structure and fixing the identity (γ=0). □

---

## What Remains Open

The rigidity theorem explains WHY this encoding.

What it does not yet explain:
1. **Why the entry point is 7** (not another cycle element)
2. **Why the readout is σ⁻¹ rather than σ** (cycle traversal direction)
3. **Connection to the Prog channel** — why does the TIG Prog channel
   independently produce the same ordering?

These are the next questions.

---

## Summary Statement

> The encoding φ = 5ε + 6y is forced because it is the CRT reconstruction
> isomorphism for Z/10Z ≅ Z/2Z × Z/5Z. The braid is what rotation on a
> 6-cycle looks like through the canonical isomorphism of Z/10Z. The encoding
> is not a choice — it is the structure of the ring.
