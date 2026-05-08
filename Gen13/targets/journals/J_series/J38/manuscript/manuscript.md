# WP108 — Yukawa Scaffolding from the 9-vector VEV

**Status:** scaffolding paper; sets up the computation, does not complete it.
**Authors:** Anthropic Code session, 2026-04-25 late evening
**Position:** WP100s tier; sister to WP104 (which identifies the 9-vector Higgs direction); follows-on to F1 from `Atlas/FRONTIERS_2026_04_25.md`.
**MSC 2020:** 81R40 (symmetry breaking), 81V22 (unified field theories), 11R32 (Galois theory in the relevant field), 17B81 (applications to physics).

---

## Abstract

WP104 / Path A established that BHML's $\sigma_\mathrm{outer}$-breaking content lives 100 % in the symmetric-traceless **54** irrep of $\mathfrak{so}(10)$, with an explicit 9-vector direction in the $\mathfrak{so}(9)$-vector subspace. The 9-vector has six components at $-1/\sqrt{2}$ on $\{V, L, C, P, X, H\}$, two zeros at BREATH and RESET, and one component at $-1/2$ on the symmetric pair $(B + S)/\sqrt{2}$. Squared norm $\|v\|^2 = 13/4$ exactly.

This paper sets up the Yukawa-coupling computation that follows from this VEV pattern, under the (load-bearing) hypothesis that TIG's so(10) is identified with the SO(10) GUT gauge algebra. We lay out:

* The standard SO(10) Yukawa structure: which Yukawa coupling matrices arise from which Higgs irreps, and which fermion bilinears they connect.
* The constraint imposed by a **54-dimensional Higgs VEV**: 54-Higgs couplings are NOT directly in the standard $16 \otimes 16$ Yukawa terms (the 54 doesn't appear in $16 \otimes 16$), but it appears at second order via mixing with 10 and 126 Higgs irreps that DO couple directly to fermions.
* The constraint imposed by **BREATH and RESET being zeros**: certain components of the resulting effective Yukawa matrix are forced to zero or to specific patterns determined by the unbroken $\mathrm{so}(7)$ subgroup of the broken $\mathrm{so}(9)$.
* The expected effective Yukawa pattern at energies below the symmetry-breaking scale.
* Open questions and the path to a falsifiable phenomenological prediction.

This paper does **not** complete the Yukawa computation. That requires committing to a specific Higgs sector (which combinations of 10, 54, 126 are present), running RG flows from the GUT scale to the electroweak scale, and comparing to observed mass hierarchies. Each of those is substantial work. This paper sets up the framework and identifies where the Yukawa calculation engages with TIG's specific structural input.

---

## §1 Standard SO(10) Yukawa structure (textbook background)

### §1.1 Fermion content

In SO(10) GUT, one generation of Standard Model fermions plus a right-handed neutrino fits into a single **16-dimensional spinor irrep** of $\mathrm{Spin}(10)$. Three generations means three copies of the **16**.

Under the Pati-Salam reduction $\mathrm{SO}(10) \to \mathrm{SU}(4) \times \mathrm{SU}(2)_L \times \mathrm{SU}(2)_R$, the 16 decomposes as:

$$
\mathbf{16} \;=\; (\mathbf{4}, \mathbf{2}, \mathbf{1}) \;\oplus\; (\bar{\mathbf{4}}, \mathbf{1}, \mathbf{2})
$$

The first piece contains the left-handed quarks and leptons; the second contains the right-handed quarks and leptons. The $\mathbf{4}$ of $\mathrm{SU}(4)_c$ contains the 3 quark colors plus lepton number ("lepton as the fourth color," Pati-Salam 1974).

### §1.2 Yukawa irrep structure

Yukawa couplings come from terms $\bar{\psi} \Phi \psi$ where $\psi$ is a fermion field (here, the **16**) and $\Phi$ is a Higgs field. The relevant tensor product is:

$$
\mathbf{16} \otimes \mathbf{16} \;=\; \mathbf{10} \oplus \mathbf{120} \oplus \overline{\mathbf{126}}
$$

So the standard Higgs irreps that **directly** generate Yukawa couplings to the 16 are:

* The **10**: a vector Higgs. Generates symmetric Yukawa couplings $\bar{16} \cdot \mathbf{10} \cdot 16$.
* The **120**: a 3-form Higgs. Generates antisymmetric Yukawa couplings.
* The **$\overline{\mathbf{126}}$**: a self-dual 5-form Higgs. Generates symmetric Yukawa couplings + Majorana neutrino masses (the canonical see-saw mechanism).

**The 54 does NOT appear in this list.** The 54 of SO(10) does not couple directly to $\bar{16} \cdot 16$ at the renormalizable level; it appears in $16 \otimes \overline{16}$ (the adjoint-style terms) and in higher-order operators.

### §1.3 The 54-Higgs role: symmetry breaking, not direct Yukawa

The 54 of SO(10) is the **symmetric-traceless** representation. A VEV in the 54 breaks $\mathrm{SO}(10) \to \mathrm{SO}(p) \times \mathrm{SO}(q)$ for some $p + q = 10$. The specific decomposition depends on which direction within the 54 the VEV points.

**The 9-vector direction inside the 54 (WP104's result) breaks $\mathrm{SO}(10) \to \mathrm{SO}(9)$**, with the 9-vector parametrizing the orthogonal direction. The next stage of breaking — from $\mathrm{SO}(9)$ to a smaller subgroup — depends on additional VEVs in the 9 of $\mathrm{so}(9)$ or in other Higgs sectors.

So: the 54-Higgs VEV from WP104 is a **first-stage symmetry-breaker**. It breaks SO(10) → SO(9). The resulting fermion mass spectrum at this stage depends on what couplings the 16 of SO(10) inherits from the 16 of $\mathrm{Spin}(9)$.

Under $\mathrm{SO}(10) \to \mathrm{SO}(9)$, the 16 of $\mathrm{Spin}(10)$ decomposes as $\mathbf{16} = \mathbf{16}$ of $\mathrm{Spin}(9)$ (it stays as a single 16-spinor of the smaller group). So no direct fermion-mass effect at this breaking stage; the 16 of $\mathrm{Spin}(10)$ remains an irreducible spinor of $\mathrm{Spin}(9)$.

**Consequence:** the 54-VEV breaking that WP104 identifies is *upstream* of fermion mass generation. Mass terms come from subsequent symmetry breaking in Higgs sectors that DO couple directly to $\bar{16} \cdot 16$ — namely the 10, 120, and 126.

---

## §2 What WP104's 9-vector contributes to Yukawa structure

### §2.1 The constraint: BREATH and RESET unbroken

The 9-vector VEV has $v_8 = v_9 = 0$ in TIG's labelling — the BREATH and RESET components are zero. Translating to physics-side language: the breaking $\mathrm{SO}(10) \to \mathrm{SO}(9)$ proceeds along a direction with two **specific** components zero in the orthogonal 9-vector.

In the standard SO(10) parameterization, the 9-vector lives in the orthogonal complement of $\mathrm{SO}(9)$ inside $\mathrm{SO}(10)$. Under $\mathrm{SO}(10) \to \mathrm{SO}(9)$ breaking by a 9-vector VEV $v$, the unbroken subgroup is $\mathrm{SO}(8) \subset \mathrm{SO}(9)$ when the VEV doesn't fully break SO(9), or $\mathrm{SO}(9)$ itself when the VEV is "minimal" (along a fixed direction). For our specific 9-vector $v$, the unbroken subgroup at this stage is $\mathrm{SO}(7)$ — the stabilizer of the two-zero direction $(\hat{e}_8, \hat{e}_9)$ inside $\mathrm{SO}(9)$.

**Reading:** WP104's 9-vector breaks SO(10) all the way down to **SO(7)** in one step (because two of the nine 54-irrep components are zero, leaving 7 active directions for $\mathrm{SO}(9) \to \mathrm{SO}(7)$ breaking via the same VEV).

This is a much more aggressive symmetry breaking than is typical in the literature: most SO(10) GUT models use a 54 VEV that breaks SO(10) → SO(6) × SO(4) (Pati-Salam) directly, which requires the 9-vector to point in a specific direction *that doesn't have BREATH and RESET zero*. Our 9-vector, with BREATH=RESET=0, instead breaks via the SO(9) intermediate.

### §2.2 Implication for the fermion sector

If the symmetry breaking goes $\mathrm{SO}(10) \to \mathrm{SO}(9) \to \mathrm{SO}(7)$, the 16 of $\mathrm{Spin}(10)$ decomposes as:

$$
\mathbf{16} \xrightarrow{\mathrm{SO}(10) \to \mathrm{SO}(9)} \mathbf{16} \xrightarrow{\mathrm{SO}(9) \to \mathrm{SO}(7)} \mathbf{8}_s + \mathbf{8}_c
$$

(The 16 of $\mathrm{Spin}(9)$ decomposes under $\mathrm{Spin}(7) \subset \mathrm{Spin}(9)$ as $\mathbf{8}_s + \mathbf{8}_c$, the two distinct 8-dim spinors of $\mathrm{Spin}(7)$.)

This is **not** the Pati-Salam decomposition (which would have given $(\mathbf{4}, \mathbf{2}, \mathbf{1}) + (\bar{\mathbf{4}}, \mathbf{1}, \mathbf{2})$ under $\mathrm{SU}(4) \times \mathrm{SU}(2) \times \mathrm{SU}(2)$). The two 8-dim spinors of $\mathrm{Spin}(7)$ are instead the natural decomposition under triality of $\mathrm{Spin}(7) \subset \mathrm{Spin}(8)$.

**Tension with Path B.** WP104's Path B identifies the **doubly-invariant subalgebra under $D_4 = \langle P_{56}, \sigma^3 \rangle$** as $\mathfrak{su}(4) \oplus \mathfrak{u}(1)$ — the Pati-Salam $\oplus$ B−L gauge content. This expects a Pati-Salam decomposition of the 16, not an $\mathrm{Spin}(7)$ decomposition. The two paths point at the same target (Pati-Salam $\subset$ SO(10)) but appear to disagree on the *route*: Path A's 9-vector with BREATH=RESET=0 breaks via SO(9), not directly to Pati-Salam.

Resolving this tension is the **first concrete open question** in WP108: is the SO(7) intermediate compatible with the doubly-invariant Pati-Salam structure? Or does the 9-vector need to be reinterpreted (perhaps the BREATH=RESET=0 constraint fixes the symmetric-traceless tensor in a way that's actually equivalent to Pati-Salam under some basis change)?

### §2.3 The integer 13 in $\|v\|^2 = 13/4$

The squared norm of the 9-vector is $13/4 = 26/8$, where 26 is the count of $\sigma_\mathrm{outer}$-asymmetric BHML cells (D33). The integer 13 also appears in $\kappa_\xi = 13/(4e)$ (D35, the inflaton coupling). It does NOT appear directly in standard SO(10) Yukawa literature — there's no "magic 13" in the textbook treatment.

**This is the structural fingerprint.** If TIG's so(10) really is the SO(10) GUT gauge algebra, then the integer 13 should show up in the eventual phenomenological predictions — perhaps as a specific overall scale, or as a count of degrees of freedom involved in a coupling. If it doesn't, that's a falsification of the identification: the 13 is structurally TIG, not structurally physics.

---

## §3 The Yukawa computation — what would have to be done

To convert WP104's structural alignment into a falsifiable phenomenological prediction:

### §3.1 Commit to a Higgs sector

The 54 alone breaks SO(10) → SO(9) (via our 9-vector); it does NOT generate fermion masses. Mass generation requires additional Higgs irreps from $\{10, 120, 126\}$. The minimal viable sector for SO(10) GUT phenomenology is **10 + 126** (or sometimes 10 + 120 + 126).

A complete TIG-derivation would need to identify which additional Higgs irreps are forced or strongly suggested by TIG's structure. Currently, only the 54 is identified by WP104. The 10 and 126 (or 120) are additional input.

### §3.2 Resolve the SO(9) vs Pati-Salam route

Per §2.2 above, the 9-vector with BREATH=RESET=0 breaks SO(10) → SO(7) via the SO(9) intermediate, while Path B's doubly-invariant subalgebra suggests a Pati-Salam reduction. The two routes can be reconciled by identifying a basis transformation OR by accepting that Path B is structural (the gauge content) while Path A is dynamical (the breaking route), and they decouple.

### §3.3 Compute the Yukawa matrix

For the chosen Higgs sector, compute the 3 × 3 Yukawa matrices $Y_u$, $Y_d$, $Y_e$, $Y_\nu$ allowed by the symmetry-broken theory. The TIG-specific input is the BREATH=RESET=0 zero-direction: certain matrix entries are forced to zero by the symmetry, others are free parameters that the Higgs VEV fixes.

This is standard SO(10) GUT computation; the textbook treatments (Slansky 1981, Mohapatra-Pal) provide the framework.

### §3.4 RG-run from GUT scale to electroweak scale

Standard renormalization-group running of the Yukawa matrices from the GUT scale ($\sim 10^{16}$ GeV) to the electroweak scale ($\sim 10^2$ GeV). This requires choosing the GUT scale, which in turn requires the TIG ↔ Planck scale-fixing that's open per F2 in `FRONTIERS.md`.

### §3.5 Compare to Standard Model masses

The endpoint: do the predicted masses and mixing angles (CKM matrix; PMNS matrix; mass ratios $m_u : m_c : m_t$, $m_d : m_s : m_b$, $m_e : m_\mu : m_\tau$) match observation? **This is the falsification test.** If yes, the 54-Higgs route is a viable physics prediction. If no, the so(10) ↔ SO(10)-GUT identification fails.

---

## §4 Computational scaffold (what the tractable next steps look like)

### §4.1 Symbolic decomposition of the 9-vector

Encode the 9-vector in `papers/wp108_yukawa_scaffolding/verification/` (folder to be created when this work resumes). Components:

```python
v_9 = [
    -1/sqrt(2),   # e_0 = VOID
    -1/sqrt(2),   # e_1 = LATTICE
    -1/sqrt(2),   # e_2 = COUNTER
    -1/sqrt(2),   # e_3 = PROGRESS
    -1/sqrt(2),   # e_4 = COLLAPSE
    -1/2,         # e_5+e_6 symmetric (BALANCE+CHAOS)/sqrt(2)
    -1/sqrt(2),   # e_7 = HARMONY
    0,            # e_8 = BREATH
    0,            # e_9 = RESET
]
```

Embed this as a 9 × 9 symmetric-traceless tensor in the 54 of SO(10). Verify: it preserves the SO(7) stabilizer subgroup (the 7 nonzero components form an SO(7)-invariant subspace of the 9).

### §4.2 16-spinor decomposition under the breaking

Compute the decomposition $\mathbf{16}_\mathrm{Spin(10)} \to \mathbf{16}_\mathrm{Spin(9)} \to \mathbf{8}_s + \mathbf{8}_c$ of $\mathrm{Spin}(7)$ explicitly. Verify the spinor reps via the Clifford algebra decomposition (this is standard; Slansky 1981 has the tables).

### §4.3 Test for Pati-Salam compatibility

For the 9-vector with BREATH=RESET=0, check whether the residual gauge group at the breaking endpoint contains the Pati-Salam group $\mathrm{SU}(4) \times \mathrm{SU}(2) \times \mathrm{SU}(2)$ as a sub-quotient or as a transverse structure. This addresses §2.2's tension between Path A and Path B.

### §4.4 Yukawa matrix structure

For a minimal 10 + 126 Higgs sector with the 54-VEV pattern fixed, write the symbolic form of the Yukawa matrices $Y_u, Y_d, Y_e, Y_\nu$. Identify which entries are forced to zero by the BREATH=RESET=0 constraint, which entries are nonzero, and what the relations among the nonzero entries are.

### §4.5 Phenomenological prediction (the endpoint)

If all of §4.1–§4.4 lands cleanly, the result is a parametrized prediction for the SM mass hierarchy. Compare to observed values; either the prediction matches (so(10) ↔ SO(10)-GUT survives this test) or it doesn't (so(10) is "abstractly" $\mathfrak{so}(10)$ but not the SO(10)-GUT gauge algebra in the physical sense).

---

## §5 Honest scope (what this paper does NOT do)

This paper is **scaffolding**. It does not:

* Complete any Yukawa coupling computation. The calculations above are sketched but not performed.
* Predict any mass ratio, mixing angle, or specific phenomenological observable.
* Resolve the §2.2 tension between Path A's SO(9) intermediate and Path B's Pati-Salam doubly-invariant content.
* Commit to a specific additional Higgs sector beyond the 54 (the 10, 120, 126 choices remain open).
* Address the TIG ↔ Planck scale fixing required for any quantitative prediction (F2 in FRONTIERS, decade-class).

What it DOES is set up the computational structure and identify the specific places where TIG's structural input (the 9-vector with BREATH=RESET=0; the integer 13 in $\|v\|^2 = 13/4$; the doubly-invariant Pati-Salam ⊕ B−L gauge content) engages with the standard SO(10) Yukawa machinery.

The natural next sprint: §4.1 through §4.4, in order. Each is a few-hundred-LOC computational task with literature lookup. §4.5 is the substantial phenomenology task.

---

## §6 References

* **Standard SO(10) GUT:**
  * Fritzsch, H., Minkowski, P. *Unified interactions of leptons and hadrons.* Ann. Phys. 93 (1975), 193.
  * Georgi, H. *The state of the art — gauge theories.* AIP Conf. Proc. 23 (1975), 575.
  * Pati, J. C., Salam, A. *Lepton number as the fourth color.* Phys. Rev. D 10 (1974), 275.
  * Slansky, R. *Group theory for unified model building.* Phys. Rep. 79 (1981), 1.
  * Mohapatra, R. N. *Unification and Supersymmetry: The Frontiers of Quark-Lepton Physics.* Springer, 3rd ed., 2003.
* **SO(10) Higgs sector:**
  * Aulakh, C. S., Mohapatra, R. N. *Implications of supersymmetric SO(10) grand unification.* Phys. Rev. D 28 (1983), 217.
  * Buccella, F., Ruegg, H., Savoy, C. A. *Patterns of symmetry breaking in SU(5) and SO(10).* Phys. Lett. B 94 (1980), 491.
  * Bertolini, S., Schwetz, T., Malinský, M. *Fermion masses and mixings in SO(10) models and the neutrino challenge to SUSY GUTs.* Phys. Rev. D 73 (2006), 115012.
* **Pati-Salam phenomenology:**
  * King, S. F., Maliński, M. *Towards a complete theory of fermion masses and mixings with $SO(3)$ family symmetry and $5D$ SO(10) unification.* JHEP 11 (2006), 071.
  * Bajc, B., Melfo, A., Senjanović, G., Vissani, F. *The minimal supersymmetric grand unified theory.* Phys. Lett. B 588 (2004), 196.
* **TIG-side prerequisites:**
  * Sanders, B.R., Gish, M. *WP103 — TSML+BHML's so(10) = D₅ closure.* 2026-04-24.
  * Sanders, B.R., Gish, M. *WP104 — Two Roads to Pati-Salam from TIG's so(10).* 2026-04-25.
  * Sanders, B.R., Gish, M. *Sprint: the unmistakable truth — su(4) ⊕ u(1) doubly-invariant subalgebra.* 2026-04-25.

---

## §7 Citation

```bibtex
@misc{sanders2026wp108,
  author       = {Sanders, Brayden Ross and Anthropic Code session},
  title        = {{WP108} --- Yukawa Scaffolding from the 9-vector {VEV}},
  year         = {2026},
  month        = {apr},
  doi          = {10.5281/zenodo.18852047},
  howpublished = {\url{https://github.com/TiredofSleep/ck/tree/tig-synthesis/papers/wp108_yukawa_scaffolding}},
  note         = {Scaffolding paper: sets up the SO(10) Yukawa-coupling computation that follows from {WP104}'s 9-vector {VEV} (with BREATH and RESET as zeros), identifies the {SO(9)} intermediate and the SO(7) endpoint of the symmetry-breaking route, and lists the computational steps required to reach a falsifiable phenomenological prediction. Does not complete the computation.}
}
```

🙏

— Anthropic Code session, 2026-04-25 late evening
