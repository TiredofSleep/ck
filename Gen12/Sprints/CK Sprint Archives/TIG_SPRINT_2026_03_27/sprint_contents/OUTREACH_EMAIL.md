# Outreach Email — Analytic Number Theorist

**Subject:** New dissipative flow for ζ(s) — seeking feedback on inner-collar bound

---

Dear [Name],

I have been developing a TIG (Trinity Infinity Geometry) operator algebra
framework and have found what appears to be a new geometric restatement
of the Riemann Hypothesis. I am writing to ask whether you can spot a
path toward the one remaining analytic step.

**The setup in one paragraph.** Define the scalar flow

```
dσ/dt = −(σ − 1/2)|ζ(σ + it₀)|²
```

on the critical strip. I prove (Halving Lemma, Grönwall) that on any
zero-free vertical segment the flow converges exponentially to σ = 1/2
at rate m(t₀) = min|ζ(σ+it₀)|² > 0. Korobov–Vinogradov gives this
unconditionally for σ ≥ σ_KV(t₀) ≈ 0.999. The Riemann Hypothesis is
equivalent to m(t₀) > 0 for *every* zero-free vertical, all the way
down to σ = 1/2.

**The open analytic question (one line):**

> Does there exist c > 0 such that for every t₀ with no zero on
> {σ + it₀ : 0 ≤ σ ≤ 1},
> min|ζ(σ+it₀)| ≥ exp(−c(log t₀)^{2/3}(log log t₀)^{1/3})?

If yes, the Halving Lemma closes immediately and RH follows. If no,
the explicit failure height t₀ identifies precisely where the flow
picture must be refined.

**Why I am writing to you.** The paper's Appendix C surveys what the
existing tools give:

- Korobov–Vinogradov: covers σ ≥ 0.999, leaves the inner collar open
- Huxley density estimates: averaged over t, not pointwise per t₀
- Bourgain sub-convexity: upper bound on |ζ|, not a lower bound
- Heath-Brown mean values: averaged |ζ|^{2k}, pointwise still missing

The common gap is averaged vs pointwise. Do you know of any technique
that produces a pointwise lower bound on |ζ(σ+it₀)| for individual t₀
values in the range 1/2 < σ < σ_KV?

I attach the 7-page draft. The relevant material is the Introduction
(the boxed open problem on p. 2) and Appendix C (the tool survey).

**The TIG side.** For context: in the discrete TIG algebra, the
analogous statement is proved algebraically — residuals persist only
in their anchor columns, and everything else collapses in ≤ 2 steps.
The flow is the continuous analog of this absorption structure. The
paper is honest that the algebraic proof does not transfer to ζ —
it only provides the framework and the correct open problem.

Any feedback on the feasibility of the pointwise lower bound — or
pointers to relevant existing results — would be greatly appreciated.

Best regards,
Brayden Sanders
7Site LLC | coherencekeeper.com
DOI: 10.5281/zenodo.18852047

---

*Attachments: WP19_HALVING_LEMMA_final.pdf, COLLAB_MEMO_KV.md*
