# Referee Report: J40 / JMP

**Manuscript:** "The Bialynicki-Birula Bridge: Logarithmic Nonlinearity Forced by Separability"
**Authors:** B. R. Sanders, H. J. Johnson
**Submitted to:** Journal of Mathematical Physics
**Reviewer:** External referee (anonymous), fresh eyes
**Date:** 2026-05-07

---

## 1. Summary of the manuscript

The authors propose a structural reading of the Bialynicki-Birula--Mycielski (BB) uniqueness theorem [Bialynicki-Birula & Mycielski 1976, *Annals of Physics* **100**:62--93] as a *forcing principle*: any continuum lift of a discrete partition algebra that preserves separability of subsystems must — by BB's theorem — admit a logarithmic self-interaction. The paper has six substantive sections.

(C1) **The forcing reading (Theorem 2.1, §2.2).** BB's theorem is restated and re-interpreted: rather than as a constraint on admissible nonlinear QM, it is read as a uniqueness statement that controls *any* continuum lift of a separability-respecting discrete structure. The reading is the manuscript's principal new conceptual contribution.

(C2) **The discrete side (§3).** Composition algebras over $\mathbb{Z}/N\mathbb{Z}$ with non-associativity decay $\sigma(N) \le 2/N$ on squarefree $N$ (companion paper J01) are summarized, and the Crossing Lemma (companion J05) is cited as the discrete reading of "information generation = separability failure."

(C3) **The forced continuum lift (§4).** The lifted equation is asserted to be $\Box \Xi = \kappa(1 + \log \Xi)$, with action density $V(\Xi) = \kappa\,\Xi \log \Xi$, vacuum at $\Xi_0 = e^{-1}$, and fluctuation mass $m_\Xi^2 = \kappa e$. **Theorem 4.1** asserts global-in-time regularity for smooth positive initial data with the displayed bound

$$\|\Xi(t)\|_{H^s} \le \|\Xi(0)\|_{H^s}\,\exp\!\bigl(C_s\,t\,(1 + \log \|\Xi(0)\|_{H^s})\bigr).$$

The proof is given as a one-paragraph sketch citing Cazenave--Haraux (1980) and the Høegh-Krohn $\exp(\Phi)_2$ model.

(C4) **The Navier-Stokes application (§5).** The authors define a *separability defect* $\sigma(u; \{\Omega_i\})$ as the relative $H^1$-distance from $u$ to its orthogonal projection onto velocity fields decomposable on the partition $\{\Omega_i\}$, conjecture (Conjecture 5.2) that bounded $\sup_t \sigma(u(t)) < 1$ over the worst partition is equivalent to NS regularity, and invoke the existing logarithmic-improvement criteria [BKM84, KT00, LZ09, MS01] as evidence that "the gap between known regularity and potential blowup is exactly logarithmic." Three explicit Open Problems (the lift $\Phi_N$; the nonlinearity gap $\delta^*$; the separability bound) close the section.

(C5) **Status table (§6).** A clean tier table separates the proved (BB Theorem 2.1; Theorem 4.1; quadratic-NS-broken-separability), the structural (the Bridge Premise), the conjectural (Conjecture 5.2), and the open (NS regularity itself).

A companion verification script `proof_separability_bridge.py` (43/43 PASS, run independently below) verifies elementary numerical claims around $\Xi_0 = e^{-1}$, $V''(\Xi_0) = \kappa e$, the log-vs-quadratic ratio decay, and a toy "vortex tube" $\sigma$ proxy.

I have read the manuscript end-to-end and re-derived the key sub-steps; details in §5 below.

---

## 2. Decision recommendation

**Major revisions** (close to "Reject and resubmit as a comment / framework note" — the framework reading is intriguing and original, but the central technical theorem (Theorem 4.1) has a substantive gap in its proof sketch, the bridge premise is acknowledged-but-undefined, the $\sigma(u)$ definition is under-specified at the level needed to make Conjecture 5.2 a precise mathematical statement, and the BB-Bridge / NS section is more an interpretive essay than a JMP-style technical contribution).

The manuscript has real mathematical content (the BB theorem is real; the curvature $V''(e^{-1}) = \kappa e$ is real; the asymptotic ordering $\log \rho \ll \rho^\alpha$ for any $\alpha > 0$ at large $\rho$ is real). The forcing-principle reading is honest and clearly distinguishes proved-vs-structural-vs-conjectural — the §6 tier table is a model of intellectual honesty I wish were more common.

But several of the displayed assertions are not quite the theorems they look like. Specifically:

- **Theorem 4.1** is stated as a regularity theorem with a one-paragraph "follows from Cazenave-Haraux" proof sketch, but Cazenave-Haraux 1980 treats the *u*-multiplied logarithmic Schrödinger / Klein-Gordon equation $u_{tt} - \Delta u = u\,\log|u|^k$, where the nonlinearity *vanishes* at $u = 0$. The present equation $\Box \Xi = \kappa(1 + \log \Xi)$ has nonlinearity $f(\Xi) = 1 + \log \Xi$ which *diverges* to $-\infty$ as $\Xi \to 0^+$. The two cases are not interchangeable: Cazenave-Haraux's pivotal step (positivity is preserved because $u \cdot \log |u|^k \to 0$ at $u = 0$) does not apply here.

- **The Bridge Premise** ("Any continuum lift $\Phi_N$ … that preserves separability is forced to have logarithmic self-interaction") is the load-bearing connector between the discrete and continuous halves of the paper, and is acknowledged as Open Problem 1. But the manuscript also relies on it implicitly in §4, where Theorem 4.1 is asserted as the regularity of "the BB-lifted theory" without first establishing that the lift exists.

- **Conjecture 5.2** (Separability Regularity Criterion) is stated relative to "the partition that maximizes $\sigma$." But the optimization is over an unspecified class (all measurable partitions? all polyhedral? finite $N$ only? scale-bounded?), and the orthogonal projection $P_{\rm sep}$ is described as "onto the subspace of velocity fields decomposable as $u = \sum_i u_i$ with $\mathrm{supp}(u_i) \subset \Omega_i$" without addressing whether divergence-free is required (which it must be for NS), nor whether the projection lives in $H^1$ or in a divergence-free subspace.

- **Section 5 is structurally a framework essay**, not a derivation. The conclusion "blowup ⇔ $\sigma \to 1$" is an interpretation, not a theorem. The toy-model script "verification" of $\sigma \to 1$ uses $\sigma = \omega/(\omega + 1)$, which is *not* the $\sigma$ of Definition 5.1.

None of these concerns is by itself fatal — JMP does publish framework papers — but in the present form the paper is slightly below the JMP technical bar. With moderate-to-major revision, primarily focused on (a) shoring up Theorem 4.1's proof or downgrading it appropriately, and (b) tightening Definition 5.1 / Conjecture 5.2, the paper would be a fine JMP contribution.

**An alternative path** the editors might consider: the paper as written reads naturally as two papers — a clean note on the BB-forced log theory's regularity (which would benefit from a few extra pages of actual proof) and a separate framework essay on the NS connection (which would benefit from a few extra pages of structural development of $\sigma(u)$). Splitting may be the cleanest path forward.

---

## 3. Major comments

### M1. Theorem 4.1 has a substantive proof gap (CRITICAL)

**The displayed equation $\Box \Xi = \kappa(1 + \log \Xi)$ is singular at $\Xi = 0$.** The right-hand side $f(\Xi) = \kappa(1 + \log \Xi)$ tends to $-\infty$ as $\Xi \to 0^+$. The proof sketch (lines 88--92) cites Cazenave-Haraux 1980 to justify the regularity bound, but Cazenave-Haraux treats the equation $u_{tt} - \Delta u = u \log|u|^k$, where the nonlinearity is $u \cdot \log|u|^k$ — which *vanishes* at $u = 0$ (the factor of $u$ kills the logarithmic divergence). This is the Cazenave-Haraux pivot that allows the equation to be defined at and across $u = 0$, and that allows positivity to fail to be a constraint.

In the present manuscript, the singularity at $\Xi = 0$ is *not* tamed by a multiplicative factor of $\Xi$: the right-hand side is a bare $\log$ rather than $\Xi \log \Xi$. So the equation is well-defined only on the open set $\{\Xi > 0\}$, and **positivity preservation must be proved as a precondition**, not assumed. Without positivity, the regularity bound is vacuous (the equation is not defined). With positivity, we further need a uniform lower bound $\Xi(t,x) \ge \delta(t) > 0$ to get the log-Sobolev (Brezis-Gallouet) estimate

$$\|\log \Xi\|_{H^s} \lesssim (1 + \log(1 + \|\Xi\|_{H^s})) \cdot \frac{1}{\inf_x \Xi},$$

which is the actual machinery feeding the displayed Grönwall-type bound. The bound *as displayed* in Theorem 4.1 omits the $1/\inf_x \Xi$ factor, which is the load-bearing constant in any honest log-Sobolev bound.

**Internal inconsistency:** the proof sketch refers to a "double-exponential bound," but the displayed inequality is single-exponential at fixed initial data: $\exp(C_s t \cdot (1 + \log \|\Xi(0)\|_{H^s}))$ is, for fixed $\|\Xi(0)\|$, just an exponential in $t$ (with multiplicative prefactor depending on $\|\Xi(0)\|$). Either the statement should say "double-exponential" (and the proof sketch then needs to derive an iterated Grönwall structure that is not currently visible in the sketch), or the sketch should call this a "single-exponential at fixed data" estimate, which is what is displayed.

**Recommended fix.** Either (a) prove (i) global positivity preservation, (ii) a uniform lower bound $\inf_x \Xi(t,x) \ge \delta(\|\Xi(0)\|, t)$, and (iii) the Brezis-Gallouet bound on $\|\log \Xi\|_{H^s}$ — these are three theorems, and the appropriate reference is *not* Cazenave-Haraux but rather the Hölder / Brezis-Gallouet line for inverse-singularity field theories; or (b) downgrade Theorem 4.1 to "Conditional Theorem (assuming positivity preservation and lower bound, the log-Sobolev embedding gives the displayed estimate)" and elevate positivity preservation to Open Problem 0. The latter is actually defensible as a JMP framework contribution, but it must be done explicitly.

The Høegh-Krohn $\exp(\Phi)_2$ model cited in the proof sketch is the *Boltzmann-weight dual* of $V = \Xi \log \Xi$, not the dynamical equation $\Box \Xi = \kappa(1 + \log \Xi)$. The relationship is by Wick rotation and thermodynamic limit; using H-K to justify dynamical regularity in 4D Lorentzian signature is a non-trivial step that the manuscript skips. Either justify the use of H-K explicitly, or remove the citation in this context.

### M2. The Bridge Premise (§3.3) is the entire physical content of the paper, and is acknowledged as conjectural — but is treated as a theorem in §4

The Bridge Premise reads: "Any continuum lift $\Phi_N : \mathrm{CL}_N \to L^2(\Omega)$ of the discrete Crossing Lemma data that preserves separability of the partition is, by Theorem 2.1, forced to have logarithmic self-interaction in the limit $N \to \infty$." The premise is acknowledged as Open Problem 1, but in §4 the equation $\Box \Xi = \kappa(1 + \log \Xi)$ is asserted as "the BB-lifted theory" without conditional flagging. Theorem 4.1 then proves regularity *of the BB-lifted theory*, which exists only conditionally on the premise.

This is a stylistic issue more than a mathematical one — the manuscript can certainly study the equation $\Box \Xi = \kappa(1 + \log \Xi)$ on its own merits, independent of whether it actually arises from a discrete-to-continuum lift. But the manuscript should make this distinction clean: either drop the lift framing in §4 (and state Theorem 4.1 as a result about the equation $\Box \Xi = \kappa(1 + \log \Xi)$ in its own right), or carry the conditional through (and call Theorem 4.1 a "conditional theorem on the BB-lifted theory").

The statement of Theorem 2.1 itself (the BB theorem in §2.1) also has a notational issue: BB's theorem in its 1976 formulation is for the *Schrödinger* evolution in the nonrelativistic Hilbert-space framework, with nonlinearity $\hat F(\rho)$ multiplying $\Psi$ inside the time evolution. The manuscript silently extends to a Klein-Gordon or wave-equation framework without explicit justification. Whether the BB theorem extends to relativistic settings is a real question (see Bialynicki-Birula's later papers on relativistic log-Schrödinger; the answer is "yes, with modifications," but the modifications are not the displayed equation $\Box \Xi = \kappa(1 + \log \Xi)$). This needs to be either argued, or qualified as a heuristic.

**Recommended fix.** Add a §2.3 "Scope of the BB theorem" subsection that explicitly addresses (i) Schrödinger versus Klein-Gordon vs wave-equation extensions of BB, (ii) the meaning of "separability" in each framework, (iii) which extension supports the equation $\Box \Xi = \kappa(1 + \log \Xi)$ as the forced lift. Currently this is left implicit and the reader has to infer it.

### M3. Definition 5.1 ($\sigma(u)$) is under-specified

The separability defect is defined as

$$\sigma(u; \{\Omega_i\}) = \frac{\|u - P_{\rm sep}(u)\|_{H^1}}{\|u\|_{H^1}}$$

where $P_{\rm sep}$ is "the orthogonal projection onto the subspace of velocity fields decomposable as $u = \sum_i u_i$ with $\mathrm{supp}(u_i) \subset \Omega_i$." Several issues:

- **Divergence-free?** Velocity fields in NS are constrained to be divergence-free. Is $P_{\rm sep}$ projecting in the divergence-free subspace, or in the full $H^1$? The two give different answers, and the resulting $\sigma$ has different meanings.
- **Domain of $u_i$.** "$\mathrm{supp}(u_i) \subset \Omega_i$" is not preserved under $P_{\rm sep}$ if the partition $\{\Omega_i\}$ has interior boundaries: the orthogonal projection of $u$ in $H^1$ is generally not supported on $\Omega_i$ unless $u_i$ is required to vanish at $\partial \Omega_i$ and to live in a divergence-free $H^1_0$ class. This is a non-trivial functional-analytic condition not addressed in the manuscript.
- **Class of partitions.** Conjecture 5.2 references "the optimal partition (the one maximizing $\sigma$)." Over what class? If unrestricted measurable partitions, the supremum is generically 1 (any nonzero $u$ admits a partition into a fine atomization where projection of $u$ to disjoint supports has zero $H^1$ norm; equivalently, $\sigma \to 1$ over arbitrarily fine partitions, vacuously). So the supremum has to be over a restricted class — but the class is not specified.

The result is that Conjecture 5.2 is not currently a precise mathematical statement: the constants $0 < \sigma < 1$ depend on the unspecified partition class, and "blowup ⇔ $\sigma \to 1$" cannot be evaluated without that specification.

The manuscript also says (line 124) "As vorticity concentrates in a tube of radius $r$ with circulation $\Gamma$, $\omega \sim \Gamma/r^2$, and one verifies $\sigma \to 1$ as $r \to 0$." But there is no actual verification — no calculation of $\sigma$ via Definition 5.1 for a vortex-tube velocity field. The companion script computes $\sigma = \omega / (\omega + 1)$, a toy proxy that has nothing to do with the $H^1$ projection definition.

**Recommended fix.** Either (a) restrict to a tractable class of partitions (say, polyhedral with bounded geometry or diadic with uniform aspect ratio) and reformulate Definition 5.1 / Conjecture 5.2 within that class; or (b) replace Definition 5.1 with a more standard scale-conscious functional, e.g., a Besov-type seminorm or a Garsia-Rodemich-Rumsey-type modulus that captures "non-separability" without needing an explicit partition. The Cassels-Bernstein-style separability defect for Besov spaces would be a natural starting point.

### M4. The "logarithmic gap" interpretive paragraph (§5.4) overstates the inheritance

§5.4 argues that known NS criteria (BKM, Kozono-Taniuchi BMO, Lei-Zhou) "log-improve" over polynomial growth and that this is "exactly the gap forced by the Bialynicki-Birula theorem." This is a leap that the paper does not justify.

The Kozono-Taniuchi BMO criterion replaces $L^\infty$ in BKM by BMO; the improvement is *one log* (BMO is to $L^\infty$ what one logarithmic factor is to a sup). But: the BBM nonlinearity is *linear in log*, not "one log better than polynomial." Furthermore, the log-improvements in the NS literature are measured in different functional spaces from the BB log: BMO is a logarithmic improvement of $L^\infty$ in the $\dot W^{1,\infty}$-vs-$\dot W^{1,\rm BMO}$ sense; the BB log is in $V(\rho)$ vs $\rho^p$ at the level of pointwise potentials. These are not the same kind of "log."

The paper's interpretation that "NS regularity is a question about whether the quadratic nonlinearity ever exceeds this logarithmic ceiling" is a metaphor, not a mathematical statement. Open Problem 2's $\delta^*$ is at least a precise formulation, but nothing in the manuscript shows that $\delta^* < \infty$ would actually imply NS regularity in any rigorous sense.

**Recommended fix.** Either (a) make the "logarithmic gap" claim mathematically precise — pick a specific functional norm for which the BB log and the KT BMO improvement are comparable, and prove the comparison; or (b) downgrade §5.4 to "Heuristic interpretation" with explicit acknowledgment that this is interpretive prose, not a derivation.

### M5. The discrete side (§3) provides motivation, not load-bearing input

§3 cites the companion papers J01 (σ-rate) and J05 (Crossing Lemma), and implicitly suggests that the discrete-side $\sigma(N) \to 0$ rate "feeds into" the continuum side. But the continuum equation $\Box \Xi = \kappa(1 + \log \Xi)$ is independent of the rate $2/N$; the only ingredient that matters for §4 and §5 is "the lift exists and preserves separability." The rate $2/N$ is irrelevant to the BB forcing.

This is not a fatal issue, but the framing implies a tighter discrete-continuum bond than the paper actually establishes. The reader is led to expect that the rate $2/N$ controls some aspect of the regularity bound or the conjecture, but it does not appear anywhere in §§4--5.

**Recommended fix.** Either drop §3 entirely (the BB-lifted equation can be motivated abstractly without the discrete preamble), or add a §3.4 explaining what the rate $2/N$ buys you — perhaps as a discrete-information-generation rate that is intended to converge to a continuum entropy production rate in the limit. Currently the rate is dead weight in the bridge.

### M6. Citation of Bialynicki-Birula's 1976 paper is correct in the abstract but not verified in detail

BB 1976 (Annals of Physics 100, 62--93) is correctly cited as the source of the uniqueness theorem. The manuscript's Theorem 2.1 statement is consistent with BB's actual theorem. However, BB's theorem is for the *non-relativistic Schrödinger equation*, and the sign convention $-b \ln \rho$ vs. the manuscript's $\kappa \log \rho$ is a sign flip that is not reconciled in the manuscript. The sign convention determines whether the resulting potential is concave (with $b < 0$) or convex (with $b > 0$); the manuscript's statement "with positive curvature $V''(\Xi_0) > 0$" requires a specific sign choice that is not made explicit.

**Recommended fix.** State the sign convention in §2.1 explicitly: "We take $\kappa > 0$ in $V(\Xi) = \kappa \Xi \log \Xi$; this corresponds to the *convex* branch of BB's family, which is the branch with stable vacuum." Tie this to BB's original $b$ (their convention) so the reader can match.

---

## 4. Minor comments

### m1. Abstract length
The abstract is 1 paragraph at 18 lines and reads well, but the final sentence ("All proved statements are clearly distinguished from conjectural ones; the tier classification is explicit.") is meta-commentary that belongs in §6, not the abstract. Remove from abstract.

### m2. "Continuum lift" is undefined
The phrase "continuum lift" appears 11 times in the manuscript without a formal definition. The implicit definition appears to be a colimit $\lim_{N \to \infty}$ of finite-dimensional structures into a function space, but the relevant categorical / topological framework is not specified. Even informally, the manuscript should provide the equivalent of a definition: "By 'continuum lift' we mean any one-parameter family of maps $\Phi_N : \mathrm{CL}_N \to \mathrm{some\ continuum\ object}$ such that … converges in … to …."

### m3. "Separability" is overloaded
The word "separability" is used in three distinct senses across the manuscript:
- (BB sense) factorization of bipartite wave functions as $\Psi_{AB} = \Psi_A \otimes \Psi_B$;
- (CRT sense) decomposition of $\mathbb{Z}/N\mathbb{Z}$ as a product of prime-component rings;
- (NS sense) decomposability of velocity fields on a partition $\{\Omega_i\}$.

These are arguably the same idea at three levels of abstraction, but the manuscript should explicitly identify them as the same idea, or at least note the analogy. The reader otherwise finds the word changing meaning without notice.

### m4. The toy "vortex tube" computation in §5.2 is misleading
The companion script computes $\sigma = \omega / (\omega + 1)$ for $\omega \sim \Gamma/r^2$ and observes $\sigma \to 1$ as $r \to 0$. But this is *not* the $\sigma$ of Definition 5.1, and the test is uninformative about the actual quantity. Either remove this from the script, or replace with a real computation of Definition 5.1 $\sigma$ for a model vortex-tube velocity field. (If the latter, the answer is non-obvious and would itself be a small theorem.)

### m5. Verification script: §3 (YM) and §4 (RH) are out-of-scope
The companion script `proof_separability_bridge.py` includes Sections 3 (YM mass gap proportional to $e$) and 4 (RH spectral entropy of the $(R, R_2)$ partition), neither of which is in the present manuscript. These are leftover from a Sprint 14 broader script and should be excised from the J40-specific verification, or the verification should be split into multiple scripts. As is, the "43/43 PASS" headline is misleading because some of the tests are not relevant to J40.

### m6. The statement "$\xi_0$ and $T^*$ are NOT algebraically related" in the script (Section 6) is a non-result
The script tests $|T^* - \xi_0| > 0.3$ and reports this as evidence of independence. This is a non-test: any two unrelated rational/transcendental numbers will satisfy it. Either remove, or replace with a substantive statement (e.g., transcendence-degree statement: $\xi_0 = e^{-1}$ is transcendental, $T^* = 5/7$ is rational, so they are algebraically independent over $\mathbb{Q}$). The latter is a real fact and can be stated cleanly.

### m7. Cazenave-Haraux 1980 reference is incomplete
The manuscript cites "Cazenave, T., Haraux, A. (1980). *Ann. Fac. Sci. Toulouse*." without volume or page numbers. The actual reference is *Ann. Fac. Sci. Toulouse Math.* (5) **2** (1980), no. 1, 21--51 ("Equations d'évolution avec non linéarité logarithmique"). Add the full citation.

### m8. Høegh-Krohn 1971 is cited but the conclusion drawn is unclear
The reference to Høegh-Krohn $\exp(\Phi)_2$ is appropriate to the Boltzmann-weight side (the partition function $Z = \int e^{-V} = \int e^{-\kappa \Xi \log \Xi}$, which after change of variables is in the $\exp(\Phi)$ class). But this is a Euclidean / thermodynamic statement, not a dynamical regularity statement for the wave equation. The manuscript should clarify that H-K provides existence in the Euclidean theory, not regularity in Lorentzian dynamics; these are connected via Osterwalder-Schrader reconstruction, which holds in 2D and is partial in higher dimensions.

### m9. Open Problem 1 (the lift $\Phi_N$) lists four reference frameworks (wavelet RG, JKO, Maas, Chow-Huang-Li-Zhou)
This is appropriate. But the manuscript could be more concrete about which framework is most likely to succeed: JKO/Maas is the natural candidate for the entropic-flow side, while wavelet RG is the natural candidate for the lattice-Lorentzian side. A one-paragraph "expected route" sub-section would help readers understand whether this open problem is "weeks of work for an expert" or "decades."

### m10. Consider re-titling
"The Bialynicki-Birula Bridge: Logarithmic Nonlinearity Forced by Separability" is fine. But "Bridge" suggests a derivation in both directions; the actual content is "BB constrains continuum lifts to log nonlinearity, with NS as a non-example." A more precise title might be "Logarithmic Nonlinearity as a Forcing Principle: A BB-Theorem Reading and Its Limits for Navier-Stokes." Author's choice.

---

## 5. Specific verifications performed

I have verified the following by independent calculation:

(V1) $V(\Xi) = \kappa \Xi \log \Xi$ has $V'(\Xi) = \kappa(1 + \log \Xi)$, vanishing at $\Xi_0 = e^{-1}$. $V''(\Xi) = \kappa/\Xi$, evaluated at $\Xi_0 = e^{-1}$ gives $\kappa e \approx 2.718 \kappa$. Curvature is positive. ✓

(V2) The asymptotic $\log \rho \ll \rho^\alpha$ for any $\alpha > 0$ at large $\rho$ is correct. The script's tests at $\rho = 10^6, 10^9, 10^{12}$ with $\alpha \in \{0.25, 0.5\}$ confirm $\log \rho / \rho^\alpha$ small. ✓

(V3) Companion script `proof_separability_bridge.py`: 43/43 PASS on my machine, in $< 1$ s with `python3` + `math`. ✓ (But: 43/43 PASS includes Section 3 and Section 4 tests not relevant to J40; see m5 above.)

(V4) The Bialynicki-Birula 1976 paper (Annals of Physics 100, 62--93) does state the uniqueness of $-b \ln |\Psi|^2$ as the form of the nonlinearity preserving separability of the bipartite system, in the *non-relativistic Schrödinger* setting. ✓ (But: see M6 above on extending to wave-equation / Klein-Gordon settings.)

(V5) **Theorem 4.1 fails to be a complete proof on inspection.** The displayed bound

$$\|\Xi(t)\|_{H^s} \le \|\Xi(0)\|_{H^s}\,\exp(C_s\,t\,(1 + \log \|\Xi(0)\|_{H^s}))$$

is at fixed initial data a single-exponential bound in $t$. It is consistent with a Brezis-Gallouet log-Sobolev embedding $\|\log \Xi\|_{H^s} \lesssim (1 + \log(1 + \|\Xi\|_{H^s}))$, which holds for $\Xi$ uniformly bounded below. The required $\inf_x \Xi(t, x) > 0$ is *not* established by the manuscript, and the equation is singular at $\Xi = 0$. Hence the proof sketch as written does not establish global regularity; it establishes a conditional regularity given positivity preservation and uniform lower bound.

(V6) The "Cazenave-Haraux scheme" cited in the proof sketch applies to nonlinearities of the form $u \log |u|^k$ (vanishing at $u = 0$), not $1 + \log |u|$ (singular at $u = 0$). The reference does not carry the regularity claim through.

(V7) For the script's "vortex tube test": the toy $\sigma = \omega / (\omega + 1)$ verifies the toy claim and not Definition 5.1. ✓ (toy ✓; not the manuscript's $\sigma$.)

(V8) On a brief literature scan: I did not find a prior paper using the BB 1976 theorem as a "forcing principle for discrete-to-continuum lifts." The closest prior literature is the use of BB as a constraint on candidate nonlinear QM (Rosen, Zloshchastiev), which the manuscript correctly cites. The forcing-principle reading is, to my reading, novel.

---

## 6. Questions to the authors

Q1. **Is positivity of $\Xi$ preserved by the equation $\Box \Xi = \kappa(1 + \log \Xi)$?** What is the regularity status of solutions whose initial data has $\inf_x \Xi(0, x) = 0$? Are there explicit examples (constructive or numerical) of solutions that maintain $\Xi > 0$ globally? If positivity is preserved, please provide a proof or a precise reference.

Q2. **In what functional setting does the Bridge Premise hold?** The premise says any continuum lift preserving separability has logarithmic self-interaction. But what is the function space of lifts being considered, and what is the precise notion of "preserves separability"? A reader should be able, in principle, to construct a lift, check the separability condition, and verify the conclusion. Currently the path from premise to conclusion is too informal.

Q3. **What restricted class of partitions is implicit in Conjecture 5.2?** Without a class restriction, the supremum is generically 1.

Q4. **Is Theorem 4.1 the equation's regularity, or the BB-lifted theory's regularity?** If the latter, please add the conditional flag explicitly. If the former, please drop the lift framing in §4.

Q5. **The proof sketch of Theorem 4.1 says "double-exponential bound," but the displayed inequality is single-exponential at fixed initial data. Which is the intended bound?** If double-exponential is the actual bound, please show the iterated Grönwall structure that produces it.

Q6. **Have the authors verified the BB theorem extends from non-relativistic Schrödinger to the wave equation $\Box \Xi$?** The 1976 BB result is for $i \hbar \partial_t \Psi = (\ldots) \Psi$. The manuscript silently extends to $\Box$. Bialynicki-Birula's later relativistic-extension papers (e.g., the "relativistic logarithmic Klein-Gordon" line) discuss this; please cite the relevant follow-up papers.

Q7. **What is the role of the discrete rate $\sigma(N) \le 2/N$ from J01 in the present paper?** It is mentioned in §3 but does not appear in §§4--5. If it is not load-bearing, consider removing the framing.

---

## 7. Originality and significance for JMP

The forcing-principle reading of Bialynicki-Birula's 1976 theorem is, to the referee's knowledge, original: prior literature uses BB as a constraint on candidate nonlinear QM, not as a forcing principle for continuum lifts. JMP would be a natural venue for such a framework paper provided the technical content rises to JMP standard.

The §6 status table is a model of intellectual honesty in distinguishing proved-vs-structural-vs-conjectural claims; the manuscript is not over-claiming, and the tier-4 framework classification is appropriate. This is a positive feature of the submission and should be preserved through revisions.

The Conjecture 5.2 (Separability Regularity Criterion) is *potentially* a precise mathematical statement about NS regularity, but as currently written it is under-specified (see M3). With the partition class fixed, this conjecture becomes a candidate for serious mathematical investigation.

The connection to logarithmic improvements in the existing NS regularity literature (BKM, KT, LZ) is more interpretive than mathematical, but it is suggestive — and a JMP framework paper is allowed to be suggestive provided it identifies precise open problems. The three Open Problems are appropriate and clearly stated.

**Significance assessment.** If the technical issues in M1–M3 are resolved, this is a publishable JMP framework paper. If they are not, the paper is closer to a Letters in Mathematical Physics short note (a "research announcement" of the framework) than to a JMP technical contribution.

---

## 8. Reproducibility

The companion script `proof_separability_bridge.py` runs in under one second with `python3` + standard library only. 43/43 PASS reproduces on first run. The script is a reasonable verification of the elementary numerical claims (vacuum at $e^{-1}$, $V'' = \kappa e$, log-vs-quadratic asymptotic ordering).

**However, the script does not verify the load-bearing claims of the manuscript:** Theorem 4.1 (analytic regularity bound), Definition 5.1 ($\sigma(u)$ as projection-based functional), or Conjecture 5.2 (separability regularity criterion) are not testable by the script and are not addressed. The script verifies the *easy* claims; the *hard* claims are unverified.

The "43/43 PASS" headline is therefore consistent with the elementary numerical content of the manuscript but is misleading about the manuscript's principal mathematical content. Either rebrand the script as an "elementary numerical sanity check" or add tests that meaningfully exercise the harder claims (e.g., a rigorous numerical verification of Brezis-Gallouet for a sample $\Xi(0)$, or a calculation of Definition 5.1 $\sigma$ for a model velocity field).

The DOI `10.5281/zenodo.18852047` resolves to a verification-script archive that is accessible. ✓

---

Sincerely,
External Referee, JMP
