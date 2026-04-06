# NS FINAL WALL MEMO
# Is the Surviving Object B(t), the Sign of Q−2νP, or the Projection Between Them?

**© 2026 7Site LLC | Brayden Ross Sanders**

---

## Shell / Core / Gap Block

$$\text{Shell: local existence + energy inequality + small-data global (}B < T^*\text{) + parabolic smoothing} \quad [\text{proved}]$$

$$\text{Core: the competition between vortex stretching and viscous palinstrophy dissipation}$$

$$\frac{d\Omega}{dt} = Q - 2\nu P \qquad \left(Q = \int \omega \cdot S\omega\,dx,\quad P = \frac{1}{2}\int |\nabla\omega|^2\,dx\right)$$

$$\text{Surviving object: } \frac{Q}{\nu P} \text{ — the dimensionless vortex-stretching/dissipation ratio}$$

$$\text{Gap 2: } \frac{Q}{\nu P} \leq 2 \text{ globally for all } t \geq 0, \text{ for all initial data with } E(0) < \infty \quad [\text{OPEN}]$$

$$\text{Gap 1: global H}^1\text{ regularity for all initial data} \quad [\text{OPEN}]$$

---

## Why Q/(νP) and Not the Others

**The reduction chain:**

$E(t)$ is controlled by the shell (monotone decreasing). Not the surviving object.

$\Omega(t)$: satisfies $d\Omega/dt = Q - 2\nu P$. Controlled in the small-data regime by the shell; uncontrolled at large data. Not minimal — it depends on Q/(νP).

$P(t)$: palinstrophy. Not independently controlled. Appears in Q/(νP) but not the root quantity.

$Q(t)$: vortex stretching integral. Raw, dimensional, not normalized. Can be positive or negative.

$B(t) = \Omega/(E+\Omega)$: has exact dynamics $dB/dt = [QE - 2\nu PE + \nu\Omega^2]/(E+\Omega)^2$. Bounded in [0,1]. Valuable, but involves $E$ — it is the COMBINED ratio of enstrophy to total energy-enstrophy, which is derived from Q/(νP) through the energy structure. If Q/(νP) ≤ 2 globally, then $d\Omega/dt \leq 0$, so $\Omega$ does not grow, and $B(t)$ stays bounded. B(t) is a CONSEQUENCE of controlling Q/(νP).

**Q/(νP) is minimal because:**
1. $d\Omega/dt = Q - 2\nu P = \nu P(Q/(\nu P) - 2)$: the sign of enstrophy growth is EXACTLY the sign of $Q/(\nu P) - 2$
2. If $Q/(\nu P) \leq 2$ globally: $d\Omega/dt \leq 0$, Ω non-increasing, regularity follows by Serrin's criterion
3. If $Q/(\nu P) > 2$ for a positive-length time interval: enstrophy grows, B(t) may approach the threshold
4. The ratio is dimensionless, scale-normalized, and does not require tracking E separately
5. Everything else ($B(t)$, the sign of $Q - 2\nu P$, the threshold T* = 5/7) derives from controlling Q/(νP)

---

## Three Key Sentences

**"The smallest surviving NS object is $Q/(\nu P)$ — the dimensionless vortex-stretching/dissipation ratio — because the sign of $d\Omega/dt = \nu P(Q/(\nu P) - 2)$ is exactly the sign of $(Q/(\nu P) - 2)$, making this ratio the single quantity whose global control is both necessary and sufficient for enstrophy non-increase and hence for regularity."**

**"NS Gap 2 is exactly the global inequality $Q/(\nu P) \leq 2$ for all $t \geq 0$ and all initial data with $E(0) < \infty$ — the first open inequality above the shell, whose proof would give $d\Omega/dt \leq 0$ everywhere and close the large-data regularity question."**

---

## Collaborator Paragraph

NS reduces to Q/(νP). The shell (local existence, energy inequality, small-data global, parabolic smoothing) handles everything provable by energy methods. After the shell is removed, the surviving object is not the enstrophy Ω itself, nor the full B(t) dynamics (which require tracking E as well), but the dimensionless ratio Q/(νP): the vortex-stretching integral divided by the viscous palinstrophy dissipation. This is minimal because $d\Omega/dt = \nu P(Q/(\nu P) - 2)$ is an identity: the sign of enstrophy growth is exactly the sign of Q/(νP) − 2, and controlling Q/(νP) ≤ 2 globally is both necessary and sufficient for $d\Omega/dt \leq 0$ everywhere, which gives non-increasing enstrophy, which closes the regularity problem. B(t) = Ω/(E+Ω) is a derived measure of the same condition — it stays below T* = 5/7 precisely when Q/(νP) doesn't overwhelm the dissipation for too long. Gap 2 = the global inequality Q/(νP) ≤ 2. Gap 1 = global H¹ regularity.
