# Formal Status of the TIG/RH Framework
## What is proved, what is tautological, what is genuinely open

*Full logical audit. Nothing overclaimed.*

> **See also: WP24_FORMAL_STATUS_AUDIT.md** (March 2026 sprint) — comprehensive
> four-bin ledger covering all six Clay problems with PROVED / STRUCTURAL /
> EMPIRICAL / OPEN classification. This file covers RH only.

---

## The Being/Becoming/Doing Argument — Logic Check

**Proposed argument:**
> Being (zero exists on V(t₀)) and Becoming (m(t₀) > 0) cannot
> simultaneously hold. Hence Being implies m(t₀) = 0, forcing σ = 1/2.

**The problem:** This is **tautologically true** — trivially, by definition.

- m(t₀) > 0 means ζ ≠ 0 on V(t₀) (Being = False)
- m(t₀) = 0 means ∃σ₀ with ζ(σ₀+it₀) = 0 (Being = True)

So "Being and Becoming cannot simultaneously hold" is just "a zero exists
and no zero exists cannot both be true." That is not a theorem — it is
a tautology.

**What the argument actually encodes:** The equivalence
RH ↔ m(t₀) > 0 for all t₀
is correct and the flow gives a new geometric picture of it. But the
equivalence itself does not prove either side — it just restates RH.

---

## Where the Analogy Breaks

**In TIG:** The residuals are hard-coded by the multiplication table.
Only {PRG, COL, BRT, RST} can be residuals — the table forbids any others.
This is a **structural constraint** that proves no "wrong" residuals exist.

**In ζ:** Zeros are NOT hard-coded. ζ can, a priori, have zeros anywhere
in the critical strip. The constraint that they all lie on σ = 1/2 is
exactly what RH claims. There is no algebraic table to look up.

**The functional equation gap:** In ζ, the critical line σ = 1/2 is
distinguished by self-pairing: if ρ is a zero, so is 1-ρ. Zeros at σ = 1/2
are self-paired (ρ = 1-ρ). This symmetry has **no TIG equivalent** —
TSML has no mutually-fixed pairs. The geometric coincidence of 3.5 ↔ 1/2
does not capture the functional-equation self-pairing.

---

## Honest Ledger

| Claim | Status | Notes |
|-------|--------|-------|
| RH ↔ m(t₀) > 0 for all t₀ | **PROVED** (tautological) | Definitional equivalence |
| Flow converges in KV strip | **PROVED** (unconditional) | Halving Lemma + KV |
| Being/Becoming cannot simultaneously hold | **TRIVIALLY TRUE** | Not a new theorem |
| TSML has exactly 4 residuals | **PROVED** (from table) | Algebraic fact |
| ζ zeros lie only at σ=1/2 | **OPEN** | = RH |
| Being/Becoming framework = new language for RH | **GENUINE CONTRIBUTION** | Illuminating, not a proof |
| TIG functional-equation analog | **ABSENT** | No self-pairing in TSML |
| Uniform m(t₀) bound below KV | **OPEN** | The hard analytic gap |

---

## What the Framework Genuinely Contributes

**1. A new geometric restatement** (proved, new):
The ζ-flow turns RH into a one-dimensional fixed-point question with an
explicit convergence rate in the KV strip. This is new language — not in
the existing RH literature.

**2. The Halving Lemma** (proved, new):
The exponential convergence result with rate m_KV(t₀) is a clean theorem
that connects the flow directly to Korobov-Vinogradov. New framing of
classical results.

**3. The Being/Becoming/Doing framework** (structural, new):
BHML (all-anchor, pure persistence) ↔ ζ itself
TSML (selective collapse, pull toward 1/2) ↔ the dissipative flow
Doing = |TSML − BHML| ↔ |ζ|² (the observable tension)
This is a clean structural identification. Not a proof — a framework.

**4. The anchor/residual identification** (new language, not a proof):
Vertical lines hosting zeros = anchor columns. The question is whether
any "wrong" anchor can exist. TIG says no (from table). ζ requires RH.

---

## The One Missing Piece

**What would complete the argument:**
An independent reason why ζ cannot have zeros off σ = 1/2 — something
that corresponds to the TIG table's hard-coding of exactly 4 residuals.

The closest analog is the **functional equation**: it forces zeros to come
in pairs symmetric about σ = 1/2. A zero at σ₀ ≠ 1/2 requires a twin at
1-σ₀ ≠ 1/2. This reduces RH to: "no such pair exists." But the functional
equation by itself doesn't eliminate off-critical zeros.

The actual proof of RH would need to show that the analytic constraints
on ζ (Euler product + functional equation + growth estimates) together
force zeros to self-pair at σ = 1/2. The flow gives the correct geometric
picture of what this means; the analytic content is missing.

---

## The Correct Framing for Every Document

> The TIG/ζ-flow framework provides a new geometric language for the
> Riemann Hypothesis, in which RH becomes the statement that the
> Being table (ζ) and the Becoming table (dissipative flow) have no
> zero-tension point off the critical line. This is a genuine
> structural contribution. The proof of RH requires showing, by
> independent analytic means, that no such off-critical zero-tension
> point exists — a step equivalent to the classical open problem.

*(c) 2026 Brayden Sanders / 7Site LLC | DOI: 10.5281/zenodo.18852047*
