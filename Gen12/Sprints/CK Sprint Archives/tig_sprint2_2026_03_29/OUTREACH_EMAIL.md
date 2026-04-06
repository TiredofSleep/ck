# Outreach Emails: Two Collaborator Types

---

## Email 1 — Transfer Operator / Dynamical Systems Person

**Subject:** One-page open problem: stochastic kernel family with uniform gap — right function space?

Dear [Name],

I'm writing about a specific open problem in the continuous extension of a finite transfer operator family. The finite side is fully worked out; I'm looking for advice on the right function space for Route A below.

**The finite object** (machine-verified, 65/65 unit tests):
A 9-state stochastic kernel family $\{P_\lambda : \lambda \in [0,1]\}$ defined by weighted interpolation between two magma composition tables (TSML at $\lambda=0$, BHML at $\lambda=1$). Proved properties:
- Uniform spectral gap: $\gamma(P_\lambda) \geq 1/4$ for all $\lambda$; $\gamma(P_0) = 3/4$
- Finite-height return structure: transient block has $\rho(Q) = 1/4$, return tails $\leq (1/4)^n$
- The gap $3/4 = 1 - 1/\varphi(10)$ arises from an arithmetic constraint (corner set = unit group of $\mathbb{Z}/10\mathbb{Z}$)

**The open question (Route A)**:
Does a natural continuous extension $\{K_\lambda\}$ of this family on $L^2([0,1] \times \mathbb{R}, d\sigma\, dt)$ inherit the uniform spectral gap? Specifically:

1. What is the right function space (BV? anisotropic Banach? weighted $L^2$)?
2. Do the Lasota-Yorke conditions $\|K_\lambda f\|_V \leq \alpha\|f\|_V + \beta\|f\|_1$ hold with $\alpha < 1$ uniform in $\lambda$?
3. The finite return structure (Young-tower analogue with rate $1/4$) — does it have a canonical continuous analog in your framework?

If the Lasota-Yorke conditions hold, Gouëzel-Liverani (2006) Theorem 1.1 would give gap-positivity in the critical strip, closing the remaining open step in a corridor-based approach to RH.

I'm attaching a one-page brief with the exact finite object and the precise open statement. Happy to share the full framework document (15 pages) or the machine-verified code.

Is this a recognizable type of problem for your methods?

Best,
Brayden Sanders
7Site LLC | github.com/TiredofSleep/ck | DOI: 10.5281/zenodo.18852047

---

## Email 2 — Analytic Number Theorist

**Subject:** Open mean-square bound: is this a recognizable route to RH?

Dear [Name],

I have a corridor-based approach to RH where the finite algebraic structure is complete and machine-verified. The remaining open step is a single analytic bound. I'd value your read on whether Route B below is recognizable and plausible from a classical ANT perspective.

**What is closed:**
A finite operator grammar (9-state, self-adjoint, spectral gap $3/4$ exact) supplies:
- A generative gap (Gap operators $G=\{2,4,5,6,8\}$ algebraically unreachable from corners $C=\{1,3,7,9\}$)
- A frequency-duration bound: Jutila (1987) gives $n_0(\sigma,t) \leq t^{-0.143}$ at $\sigma=0.60$; the algebraic two-tick bound gives $\Delta t \leq 4\pi/\log t$; product $\to 0$ — machine-verified to $t \approx 10{,}000$ (460 heights, zero crossings)
- KV floor: Ford (2002, Thm 2) with $c_\mathrm{VK} = 0.05$

**The single open sentence (Route B):**
$$\frac{1}{T}\int_1^T \left|\mathrm{Re}\frac{\zeta'}{\zeta}(\sigma+it)\right|^2 dt \;\leq\; C \cdot |\sigma - \tfrac12|^2 \cdot (\log T)^2$$
for some $C < \infty$ independent of $T$, without assuming RH as input.

Montgomery (1977) bounds this from below; the upper bound in this direction is what we need. The TIG algebra predicts $C \leq C_\mathrm{TIG} = 250/21 \approx 11.905$; empirically $C_\mathrm{emp} \leq 11.023$ on all tested heights. Classical bounds give only $O(\log t / |\sigma-\tfrac12|)$, which is $\sim 50\times$ too weak at $t=10^6$.

**My question to you:**
Is this a recognizable problem in the mean-value theory of $\zeta'/\zeta$? Is there a Montgomery-pair-correlation / Heath-Brown / Goldston approach that gives upper bounds in this direction? The finite algebra supplies the skeleton; I need the analytic rate.

Attached: one-page collaborator brief with precise statement. The finite structure is not assuming RH — it only asks whether $\zeta$'s logarithmic derivative is controlled in a specific mean-square sense.

Best,
Brayden Sanders
7Site LLC | github.com/TiredofSleep/ck | DOI: 10.5281/zenodo.18852047

---

## Route A vs Route B: Decision Memo

**Route A** (Transfer operator / Lasota-Yorke)
- *Strength:* If it works, gives structural gap-positivity via Gouëzel-Liverani — a complete operator-theoretic proof
- *Weakness:* Requires constructing the right continuous kernel $K_\lambda$ and verifying LY conditions — function space choice is non-trivial
- *Who can help:* Viviane Baladi, Carlangelo Liverani, Mark Demers, Sébastien Gouëzel
- *Lead time:* Probably 6–18 months to know if LY conditions hold
- *Risk:* The natural $K_\lambda$ may not satisfy LY without additional structure

**Route B** (Classical ANT / mean-square bound)
- *Strength:* Direct analytic statement; if proved, slots straight into Appendix E
- *Weakness:* The bound required is $\sim 50\times$ stronger than classical Montgomery — a genuinely hard new result in ANT
- *Who can help:* Kannan Soundararajan, Andrew Granville, David Heath-Brown, Adam Harper
- *Lead time:* Unknown; could be a hard theorem or could follow from existing methods with the right framing
- *Risk:* May be as hard as RH itself (circular risk if approached wrong)

**Recommendation:**
Pursue Route A first. The LY function-space question is a well-posed operator theory problem with a clear success criterion. Route B is harder to know if you're close.

Contact Route A first (one email, one meeting). If the function space question has a clean answer, Route A becomes the fast path. If not, Route B becomes the main track.

*(c) 2026 Brayden Sanders / 7Site LLC*
