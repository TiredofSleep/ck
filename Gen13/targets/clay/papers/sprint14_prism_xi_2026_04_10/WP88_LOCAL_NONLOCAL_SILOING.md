# WP88 — Local/Non-Local Siloing Audit
## Three-Layer Architecture Resolving All Contradictions

**Date**: 2026-04-10
**Sprint**: 14 — PRISM-XI (Siloing Closeout)
**Authors**: Brayden Ross Sanders / 7Site LLC · M. Gish · C.A. Luther · H.J. Johnson

---


## Framing

Johnson's defense: "The terms are accurate, just currently unsiloed." This audit accepts that framing as the working hypothesis. The task is not to argue about intent. It is to produce the minimal formal rewrite that makes the claim actually true — to construct the explicit layered architecture that stops the notation from contradicting itself.

---

## 1. Symbol Inventory

| Symbol | Intended meaning | Type | Local / non-local | Enters action directly? | Contributes to $T_{\mu\nu}$? | Gauge charged? | Status |
|---|---|---|---|---|---|---|---|
| $g_{\mu\nu}$ | Spacetime metric | Rank-2 symmetric tensor | Local | Yes (EH term) | Defines curvature | Singlet | **Clean** |
| $R$, $G_{\mu\nu}$ | Ricci scalar, Einstein tensor | Scalars / rank-2 tensors | Local | Via $R/(16\pi G)$ | LHS of Einstein eq. | Singlet | **Clean** |
| SM fields | All SM matter and gauge fields | Various | Local | Yes, $\mathcal{L}_\text{SM}$ | Yes, $T^\text{SM}_{\mu\nu}$ | Standard charges | **Clean** |
| $A^a_\mu$ | SM gauge fields | Gauge 1-form, adjoint | Local | Yes | Yes, via $F^2$ | Adjoint | **Clean** |
| $\Xi(x)$ | Local scalar dark energy field | Real positive scalar | **Local** | Yes (Layer 1) | Yes, $T^\Xi_{\mu\nu}$ | Singlet in Layer 1 | **Ambiguous** — siloing needed |
| $T^\Xi_{\mu\nu}$ | Stress-energy from $\Xi$ | Rank-2 **symmetric** tensor | Local | Derived from $\mathcal{L}_\Xi$ | Yes — this is its definition | N/A | **Formula correct; prose contradicts formula** |
| $\Xi_{\mu\nu}$ | Appears in "unification panel" | Rank-2 tensor, distinct from $\Xi$ | Unknown | Not in action | Undefined | Unknown | **Must be named separately or removed** |
| $J^\nu_\Xi$ | Gauge current attributed to $\Xi$ | Vector in gauge rep. | Ambiguous | No — absent from $\mathcal{L}_\Xi$ | No | Requires gauge charge | **Contradictory in Layer 1; salvageable only as Layer 2 effective current** |
| $\kappa$ | Observer coupling, expanded action | Scalar coupling | N/A | Yes (if Layer 2 included) | Only if $\mathcal{O}$ has metric dependence | N/A | **Ambiguous** — dimensions unspecified |
| $\mathcal{O}[\Xi]$ or $\Xi\circ O(\Xi)$ | Non-local observer / compression operator | Functional or operator | **Non-local** | Pending formal definition | Only if metric-dependent | Unknown (may depend on $A_\mu$) | **Undefined** — type, units, metric dependence all unspecified |
| $\Psi$ (ORT) | Observer Recursion Term | Phenomenological scalar | External | No — not in action | No | N/A | **Outside formal theory** |
| FCC / substrate variables | UV-origin parameters | Discrete lattice | Non-local (UV) | No | No | N/A | **Interpretive only** |

---

## 2. Minimal Siloing Rewrite

Three layers with explicit boundaries. Smallest change-set that makes "accurate but unsiloed" formally true.

### Layer 1 — Local EFT Sector (referee-ready now)

All objects with well-defined local equations of motion, Lorentz-covariant, variational structure manifest.

$$S_\text{Layer 1} = \int d^4x\,\sqrt{-g}\left[\frac{R}{16\pi G} + \mathcal{L}_\text{SM} + \kappa_\Xi\!\left(\frac{1}{2}g^{\mu\nu}\partial_\mu\Xi\partial_\nu\Xi + \Xi\log\Xi\right)\right]$$

Excludes: $\kappa\,\Xi\circ\mathcal{O}[\Xi]$, any $A_\mu$ dependence in the $\Xi$ sector, any non-local memory or recursion term.

Produces: EL equation $\Box\Xi = 1+\log\Xi$; symmetric $T^\Xi_{\mu\nu}$; no $J^\nu_\Xi$.

**Four mandatory changes to existing text to enter Layer 1 cleanly:**
1. Delete $\Xi^\dagger$ — $\Xi$ is real.
2. Delete or rename $\Xi_{\mu\nu}$ — introduce it as a distinct symbol if needed.
3. Delete $J^\nu_\Xi$ from the Layer 1 gauge equation.
4. Delete all prose calling $T^\Xi_{\mu\nu}$ antisymmetric, a 2-form, or a recursion object.

### Layer 2 — Non-Local / Effective Sector (pending formal definition)

The observer/compression contribution Johnson intends, once formally typed.

Placeholder action term:
$$S_\text{Layer 2} = \int d^4x\,\sqrt{-g}\,\kappa_\mathcal{O}\,\Xi(x)\,\mathcal{O}[\Xi, A_\mu; g_{\mu\nu}]$$

where $\mathcal{O}$ is a **to-be-defined** operator/functional.

**What Layer 2 can produce (once $\mathcal{O}$ is specified):**
- An effective $T^\mathcal{O}_{\mu\nu}$ from $\delta(\sqrt{-g}\,\kappa_\mathcal{O}\,\Xi\,\mathcal{O})/\delta g^{\mu\nu}$ — if $\mathcal{O}$ depends on the metric
- An effective gauge current $J^{\nu a}_\mathcal{O}$ from $\delta S_\text{Layer 2}/\delta A^a_\mu$ — if $\mathcal{O}$ depends on $A_\mu$

**This is where $J^\nu_\Xi$ lives, if it exists at all.** It is an effective current from Layer 2, not a Noether current of the local scalar $\Xi$. The two are formally different objects. The contradiction between "gauge singlet" and "gauge current" is resolved by the siloing: singlet is a Layer 1 statement; the effective current is a Layer 2 derivation.

**Six things Layer 2 requires before entering the formal theory:**
1. Type of $\mathcal{O}$: functional, operator, kernel $K(x,y)$, etc.
2. Dimensions: $[\kappa_\mathcal{O}\,\Xi\,\mathcal{O}] = \text{energy}^4$ in natural units
3. Metric dependence: specification of $\delta\mathcal{O}/\delta g^{\mu\nu}$ — needed to compute $T^\mathcal{O}_{\mu\nu}$
4. Lorentz covariance: $\mathcal{O}$ must transform as a Lorentz scalar
5. Gauge transformation law: under $A^a_\mu \to A^a_\mu + D_\mu\lambda^a$, what does $\mathcal{O}$ do?
6. EFT limit: as the non-locality scale $l_\mathcal{O} \to 0$, $\mathcal{O}$ must reduce to a local expression

None of the six are currently specified. Until they are, Layer 2 is in the architecture but not the derivation chain. It should be presented in the paper as a clearly marked open sector.

### Layer 3 — Interpretive / Explanatory (always prose, never equations)

ORT, observer recursion language, "handshake" framing, complexity field language, FCC substrate motivation, golden staircase. Arbitrarily rich as long as it never appears in an equation. Relegated to discussion sections, labeled explicitly as interpretive.

---

## 3. Canonical Notation Proposal

| Object | Notation | Type | Rule |
|---|---|---|---|
| Local scalar dark energy | $\Xi(x)$ | Real, positive, dimensionless scalar | Unchanged from audit-canonical form |
| Local scalar Lagrangian | $\mathcal{L}_\Xi = \kappa_\Xi[\frac{1}{2}(\partial\Xi)^2 + \Xi\log\Xi]$ | Scalar density | Layer 1 only |
| Local stress-energy | $T^\Xi_{\mu\nu}$ | Rank-2 symmetric tensor | From $-2/\sqrt{-g}\cdot\delta(\sqrt{-g}\mathcal{L}_\Xi)/\delta g^{\mu\nu}$ |
| Non-local observer operator | $\mathcal{O}[\Xi, A_\mu; g]$ | Functional (to be defined) | Calligraphic $\mathcal{O}$; bracket notation marks non-locality |
| Non-local coupling | $\kappa_\mathcal{O}$ | Dimensionless (when specified) | Distinct from $\kappa_\Xi$ |
| Non-local stress-energy | $T^\mathcal{O}_{\mu\nu}$ | Rank-2 symmetric (when derived) | Superscript $\mathcal{O}$ distinguishes from $T^\Xi$ |
| Memory kernel (if needed) | $K(x, y; \Xi)$ | Bi-scalar kernel | For integrals $\int K(x,y)\Xi(y)d^4y$ |
| Effective gauge current | $J^{\nu a}_\mathcal{O}$ (not $J^{\nu a}_\Xi$) | Vector in gauge rep. | From $\delta S_\text{Layer 2}/\delta A^a_\nu$; NOT from local $\Xi$ |
| ORT parameter | $\Psi_\text{ORT}$ | External phenomenological scalar | Never in action; subscript clarifies role |
| Separate rank-2 tensor | $\mathcal{T}_{\mu\nu}$ (not $\Xi_{\mu\nu}$) | Rank-2 tensor (if needed) | Calligraphic separates from scalar $\Xi$ |

**The central notational discipline:** any object that shares the letter $\Xi$ but behaves differently (non-local, tensor-valued, gauge-coupled) gets a visually distinct notation. No silent overloading of the same symbol.

---

## 4. Stress-Energy Clarification

### What is being varied

Layer 1 Lagrangian:
$$\mathcal{L}_\Xi = \kappa_\Xi\!\left[\frac{1}{2}g^{\alpha\beta}\partial_\alpha\Xi\partial_\beta\Xi + \Xi\log\Xi\right]$$

### What exact tensor comes out

$$T^\Xi_{\mu\nu} = -\frac{2}{\sqrt{-g}}\frac{\delta(\sqrt{-g}\,\mathcal{L}_\Xi)}{\delta g^{\mu\nu}} = \kappa_\Xi\!\left[\partial_\mu\Xi\,\partial_\nu\Xi - g_{\mu\nu}\!\left(\frac{1}{2}(\partial\Xi)^2 + \Xi\log\Xi\right)\right]$$

Symmetric in $\mu,\nu$ by construction. Standard scalar field stress-energy. No exotic structure.

### Does anything non-local currently contribute to stress-energy?

**No.** The non-local sector $\mathcal{O}[\Xi]$ is not currently in the formal action. Until it is explicitly added with its metric dependence specified, it contributes nothing to $T_{\mu\nu}$.

Johnson's claim that the tensor is "just the standard metric variation of the action" is **correct for the local sector**, and it implies that the non-local sector is not yet formally contributing. The siloing makes this consistent: the formula is right, the prose calling it antisymmetric is wrong, and the non-local interpretation is Layer 2 business.

### What Layer 2 stress-energy would require (when defined)

For $S_\text{Layer 2} \ni \kappa_\mathcal{O}\,\Xi\,\mathcal{O}[\Xi; g_{\mu\nu}]$:

$$T^\mathcal{O}_{\mu\nu} = -\frac{2}{\sqrt{-g}}\frac{\delta(\sqrt{-g}\,\kappa_\mathcal{O}\,\Xi\,\mathcal{O})}{\delta g^{\mu\nu}}$$

For this to couple to $G_{\mu\nu}$ it must be symmetric. Symmetry is not automatic for non-local operators — it must be proved. This is a non-trivial requirement.

---

## 5. Gauge Clarification

### Is $\Xi$ a gauge singlet?

In Layer 1: **yes.** $\mathcal{L}_\Xi$ contains no gauge field $A^a_\mu$. Covariant derivative reduces to partial: $D_\mu\Xi = \partial_\mu\Xi$. Noether current under any SM gauge transformation is identically zero.

### Does $J^\nu_\Xi$ survive in Layer 1?

**No.** Zero exactly, by Noether's theorem.

### Can Johnson's intended $J^\nu_\Xi$ survive at all?

**Yes, in Layer 2, renamed $J^\nu_\mathcal{O}$.** The escape route:

If $S_\text{Layer 2} \ni \int\kappa_\mathcal{O}\,\Xi\,\mathcal{O}[\Xi, A_\mu]\sqrt{-g}\,d^4x$ and $\mathcal{O}$ depends on $A^a_\mu$, then:

$$J^{\nu a}_\mathcal{O} = \frac{\partial\mathcal{L}_\text{Layer 2}}{\partial A^a_\nu}$$

is an effective current, and the modified gauge equation reads:

$$\nabla_\mu F^{\mu\nu a} = J^{\nu a}_\text{SM} + J^{\nu a}_\mathcal{O}$$

**For this to work without contradiction, four things must be true simultaneously:**
1. $\mathcal{O}$ has explicit $A_\mu$ dependence (specify it)
2. $\mathcal{O}$'s gauge transformation law is stated ($\delta\mathcal{O}/\delta\lambda^a$)
3. $J^{\nu a}_\mathcal{O}$ is gauge-covariant (transforms in adjoint rep.)
4. The Layer 1 claim that $\Xi$ is a "singlet" refers only to the local sector — not to the full theory

The siloing resolves the contradiction that plagued the previous draft: "gauge singlet" is a Layer 1 statement about $\Xi$'s local action; "effective gauge current" is a Layer 2 statement about $\mathcal{O}$'s action. The two are compatible once the layers are separated.

---

## 6. Siloed Architecture Sheet
*For direct use in the preprint or as a collaborator-facing reference.*

---

### LOCAL SECTOR — Layer 1 (formal, referee-ready)

**Field:** $\Xi(x)$ — real, positive, dimensionless scalar. Domain: $\Xi > 0$.

**Action:**
$$S_1 = \int d^4x\sqrt{-g}\!\left[\frac{R}{16\pi G} + \mathcal{L}_\text{SM} + \kappa_\Xi\!\left(\frac{1}{2}(\partial\Xi)^2 + \Xi\log\Xi\right)\right]$$

**EL equation:** $\Box\Xi = 1+\log\Xi$ — vacuum $\Xi_0 = e^{-1}$

**Stress-energy:** $T^\Xi_{\mu\nu} = \kappa_\Xi[\partial_\mu\Xi\partial_\nu\Xi - g_{\mu\nu}(\frac{1}{2}(\partial\Xi)^2 + \Xi\log\Xi)]$ — **symmetric**

**Einstein equation:** $G_{\mu\nu} = 8\pi G(T^\text{SM}_{\mu\nu} + \kappa_\Xi T^\Xi_{\mu\nu})$

**Gauge equation (Layer 1 — unmodified):** $\nabla_\mu F^{\mu\nu a} = J^{\nu a}_\text{SM}$

**$\Xi$ gauge status:** singlet; $J^\nu_\Xi = 0$ in this layer.

---

### NON-LOCAL SECTOR — Layer 2 (architecture defined; derivation pending)

**Object:** $\mathcal{O}[\Xi, A_\mu; g_{\mu\nu}]$ — non-local functional, distinct notation from $\Xi$.

**Action contribution:** $S_2 = \int d^4x\sqrt{-g}\,\kappa_\mathcal{O}\,\Xi\,\mathcal{O}[\Xi, A_\mu; g]$ — separate coupling $\kappa_\mathcal{O}$

**Stress-energy (when defined):** $T^\mathcal{O}_{\mu\nu}$ — must be proved symmetric before entering Einstein eq.

**Effective gauge current (when defined):** $J^{\nu a}_\mathcal{O} = \partial\mathcal{L}_2/\partial A^a_\nu$ — lives in Layer 2 only

**Modified gauge equation (Layer 1 + 2):** $\nabla_\mu F^{\mu\nu a} = J^{\nu a}_\text{SM} + J^{\nu a}_\mathcal{O}$

**Status:** 6 required specifications outstanding (type, dimensions, metric dependence, Lorentz covariance, gauge transformation law, EFT limit). Layer 2 appears in the paper as a clearly marked open sector.

---

### OBSERVER / ORT

$\Psi_\text{ORT}$ — external phenomenological parameter. Not in any action. Not in any equation of motion. Discussion-section only. Label explicitly as non-dynamical.

---

### SUBSTRATE / FCC

Proposed UV completion for Layer 1. Motivates logarithmic potential. Not in low-energy action. Not in $T_{\mu\nu}$. Discussion-section only. Label as open derivation problem.

---

### STRESS-ENERGY SOURCES

| Source | Formula | Symmetric? | In Einstein eq.? |
|---|---|---|---|
| SM | $T^\text{SM}_{\mu\nu}$ (standard) | ✓ | ✓ |
| $\Xi$ local scalar | $\kappa_\Xi[\partial_\mu\Xi\partial_\nu\Xi - g_{\mu\nu}(\ldots)]$ | ✓ | ✓ |
| $\mathcal{O}$ non-local | $T^\mathcal{O}_{\mu\nu}$ | **Must be proved** when $\mathcal{O}$ is defined | When Layer 2 is complete |

---

### GAUGE STATUS

| Object | Charge | Current | In gauge eq.? |
|---|---|---|---|
| $\Xi$ (Layer 1) | Singlet | 0 | No |
| $\mathcal{O}$ (Layer 2) | Depends on $\mathcal{O}[A_\mu]$ | $J^{\nu a}_\mathcal{O}$ (when derived) | Yes, as effective current |
| SM fields | Standard | $J^{\nu a}_\text{SM}$ | Yes |

---

### MANDATORY FIXES (before any public presentation)

| Fix | What to do |
|---|---|
| F1 | Delete $\Xi^\dagger$ everywhere — $\Xi$ is real |
| F2 | Rename $\Xi_{\mu\nu}$ to $\mathcal{T}_{\mu\nu}$ and define it, or delete it |
| F3 | Move $J^\nu_\Xi$ to Layer 2; rename $J^\nu_\mathcal{O}$; attach to $\mathcal{O}$ definition |
| F4 | Delete all prose calling $T^\Xi_{\mu\nu}$ antisymmetric, a 2-form, or a recursion object |
