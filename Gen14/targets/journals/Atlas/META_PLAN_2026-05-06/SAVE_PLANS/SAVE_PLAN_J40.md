# Save Plan — J40 / *Journal of Mathematical Physics*: Bialynicki-Birula Bridge

**Date:** 2026-05-07 (R1 applied)
**Source referee report:** `Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J40_JMP_FreshEyes.md`
**Manuscript folder:** `Gen13/targets/journals/J_series/J40/`
**Target venue:** *Journal of Mathematical Physics*
**Acceptance probability after revisions:** Moderate. The substantive proof gap in original Theorem 4.1 has been addressed by **explicit conditional reformulation**, not by closing the gap. This is the honest path that keeps the paper publishable; the alternative (proving global positivity preservation of $\Box \Xi = \kappa(1 + \log \Xi)$) is a substantial PDE research project, not a 1-2 week revision.

---

## §1 — Headline

The referee identified a substantive proof gap in Theorem 4.1: the equation $\Box \Xi = \kappa(1 + \log \Xi)$ is genuinely **singular at $\Xi = 0$** (RHS → $-\infty$), and Cazenave-Haraux 1980 cannot be invoked because their result treats $u \log |u|^k$ which *vanishes* at $u = 0$ — not interchangeable.

The honest fix is to **reformulate Theorem 4.1 as a conditional regularity result** with explicit hypotheses (H1) positivity preservation and (H2) uniform lower bound. Under these hypotheses the proof goes through cleanly via Brezis-Gallouet log-Sobolev embedding + Bihari-type Grönwall inequality. The unconditional version — which would require proving global positivity preservation — is elevated to **Open Problem 0**.

This is the canonical "downgrade theorem to conditional" pattern when an under-proved global statement is split into a clean conditional + an explicit open hypothesis. The conditional theorem is publishable as-is; the unconditional version is research.

---

## §2 — Diagnosis (per referee's §3, M1-M6)

| Item | Severity | R1 Action |
|---|---|---|
| M1. Theorem 4.1 proof gap | CRITICAL | Reformulated as **conditional regularity** under explicit (H1) positivity + (H2) uniform lower bound; full proof from Brezis-Gallouet log-Sobolev + Bihari Grönwall. Cazenave-Haraux dropped from §4's proof. Open Problem 0 added (positivity preservation as the explicit open hypothesis). §4.4 explains why CH80 doesn't apply. |
| M2. Bridge premise treated as theorem | Major | §3.3 explicitly tagged conjectural; Theorem 4.1 no longer claims to prove "the BB-lifted theory's regularity"; it proves regularity of the equation $\Box \Xi = \kappa(1 + \log \Xi)$ on its own merits. §2.3 added discussing BB scope (Schrödinger original; wave-equation extension justified via the cosmological side, not as a wave-equation extension of BB). |
| M3. Definition 5.1 underspecified | Major | Rewritten with explicit class $\mathcal P_K$ of polyhedral divergence-free partitions: bounded combinatorial complexity (at most $K$ pieces), bounded geometric distortion (convex pieces with bounded aspect ratio), divergence-free $H^1_0$ projection. The class is tractable: $\sigma$ bounded $0 \le \sigma \le 1$, continuous in the partition, optimal partition exists by compactness. Conjecture 5.2 is now a precise mathematical statement. |
| M4. §5.4 overstates inheritance | Moderate | Downgraded to interpretive heuristic. Explicit statement: BB log is pointwise potential; KT BMO log is Sobolev-norm regularity criterion; they are different functional senses of "log." Theorem 4.1's proof does not invoke this comparison. |
| M5. Discrete side §3 not load-bearing | Moderate | §3 condensed; the rate-bound is motivational only and §4–§5 do not invoke it. §3.3 explicitly tags Bridge Premise as conjectural. |
| M6. BB sign convention not explicit | Moderate | §2.4 added: $\kappa > 0$, convex branch, vacuum at $\Xi_0 = e^{-1}$, $V''(\Xi_0) = \kappa e > 0$. Tied explicitly to BB's original $b$ via the convention statement. |
| m1-m10. Minor | Low | Abstract polished; "continuum lift" given operational definition; "separability" disambiguated; vortex-tube "verification" rebranded as toy proxy; CH80 reference completed; Høegh-Krohn citation context clarified; Open Problem 1 expected route added; title changed; companion script rebranded as elementary numerical sanity check (NOT verification of Theorem 4.1). |

The structural revision is item M1: the conditional reformulation. All other items are accommodating.

---

## §3 — Proof of Theorem 4.1 (R1 conditional version)

The R1 proof of Theorem 4.1 is fully rigorous under hypotheses (H1) + (H2). Sketch:

1. (H1) + (H2) ensure $\log \Xi(t, x)$ is bounded below by $\log \delta$ on $[0, T] \times \mathbb{R}^3$.
2. The Brezis-Gallouet log-Sobolev embedding [BrezisGallouet80] in 3D gives, for $s \ge 3$:
   $$\|\log \Xi\|_{H^{s-1}} \le \frac{C}{\delta} \cdot (1 + \log(1 + \|\Xi\|_{H^s})).$$
3. The wave-equation energy estimate gives
   $$\frac{d}{dt}\|\Xi(t)\|_{H^s}^2 \le \frac{C\kappa}{\delta} \|\Xi\|_{H^s}\,(1 + \log(1 + \|\Xi\|_{H^s})),$$
   which is a Bihari-type ODE with logarithmic right-hand side.
4. The Bihari inequality yields $E(t) \le E(0)\,\exp(C_s(\delta) \cdot t \cdot (1 + \log E(0)))$ — single-exponential in $t$ at fixed initial data.
5. Smoothness propagation follows from Sobolev embedding ($H^s \hookrightarrow C^1$ for $s \ge 3$ in 3D) plus local well-posedness of semilinear wave equations with smooth nonlinearity on the open set $\{\Xi > 0\}$.

The proof is one page; nothing exotic. The regularity bound is honest and quantitative.

---

## §4 — Tier discipline (PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN)

- **PROVEN.** Theorem 2.1 (BB uniqueness, Schrödinger 1976; cited, not re-proved). Theorem 4.1 (conditional regularity of $\Xi$ under H1+H2). NS quadratic nonlinearity breaks separability (immediate).
- **COMPUTED.** `proof_separability_bridge.py` verifies elementary numerical claims on the potential's algebra: $\Xi_0 = e^{-1}$, $V''(\Xi_0) = \kappa e$, asymptotic $\log \rho \ll \rho^\alpha$. Sanity check on the potential, NOT verification of Theorem 4.1 / Definition 5.1 / Conjecture 5.2.
- **STRUCTURAL RHYME.** §5.4's "log gap = BB log" framing — interpretive heuristic only, not derivational.
- **OPEN.** Open Problem 0 (positivity preservation of $\Xi$). Open Problem 1 ($\Phi_N$ continuum lift; expected route JKO/Maas + wavelet RG; weeks-to-months for an expert). Open Problem 2 ($\delta^*$ nonlinearity gap on NS). Open Problem 3 (separability bound on NS).

---

## §5 — Files modified in R1

- `Gen13/targets/journals/J_series/J40/manuscript/J13_BB_Bridge_JMP.md` — full R1 rewrite with conditional Theorem 4.1, sharpened Definition 5.1, and §7 itemized revision list (13 items)
- `Gen13/targets/journals/J_series/J40/cover_letter.md` — R1 with Sanders + Gish author lane, revisions itemized
- `Gen13/targets/journals/J_series/J40/README.md` — R1 status, title change, submission checklist updated

---

## §6 — Status going forward

**Submission-ready** (post-Brayden's referee-rigor pass).

**Path A: Submit the R1 conditional version.** This is the safest path: Theorem 4.1's conditional version is fully proved, the open hypothesis (positivity preservation) is explicitly stated as Open Problem 0, the framework is honest and self-aware. JMP accepts framework papers in this style. Expected outcome: acceptance after a moderate-revision round, $\sim 60$–$70\%$ probability.

**Path B (parallel research, longer-term): Prove global positivity preservation of $\Box \Xi = \kappa(1 + \log \Xi)$.** This is a substantial PDE project — likely a follow-up paper rather than an R1 revision. If proved, Theorem 4.1 upgrades to unconditional regularity and the framework's strength rises significantly.

**Path C (alternative): Submit as Letters in Mathematical Physics.** If the conditional theorem is judged below JMP's technical bar, LMP is a natural fallback for shorter framework / research-announcement papers. Probability of LMP acceptance is higher (~75%) but venue prestige is lower.

The default is Path A. The cleanest argument for JMP is that Theorem 4.1's conditional version is fully proved, the partition-class machinery in §5 is precise, and the Open Problems are well-formulated — the paper provides genuine mathematical content (a precise framework + a conditional theorem + sharpened conjecture) without overclaiming.

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Gish, M. (2026). "Logarithmic Nonlinearity as a Forcing Principle: A Bialynicki-Birula Reading and Its Limits for Navier-Stokes." Submitted to *Journal of Mathematical Physics*.
