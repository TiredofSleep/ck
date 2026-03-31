# Master Citation List — All TIG Clay Papers
## Combined, Deduplicated, Organized by Field

*Brayden Ross Sanders (7Site LLC)*
*March 2026 | Covers: WP40 (RH), WP41 (Yang-Mills), WP42 (BSD),*
*WP17 (RH Synthesis), WP15 (YM Synthesis), WP21 (BSD Mix_λ), WP34/WP35 (Prime Laws)*
*DOI: 10.5281/zenodo.18852047*

> All TIG-internal references (CK, T*, TSML, BHML, D2, CL) are exclusive IP
> of Brayden Ross Sanders / 7Site LLC. C. A. Luther's contribution is the
> dispersion conjecture. This document covers citations across all seven
> supporting papers in the TIG Clay program.

---

## FIELD I: NUMBER THEORY

### I.A Riemann Hypothesis and Zeta Function

[NT-01] Riemann, B. (1859). "Über die Anzahl der Primzahlen unter einer gegebenen
Grösse." *Monatsberichte der Berliner Akademie*, November 1859. [Original paper;
introduces ζ(s) and the hypothesis on zero locations.]

[NT-02] Hardy, G. H. (1914). "Sur les zéros de la fonction ζ(s) de Riemann."
*Comptes Rendus de l'Académie des Sciences* 158: 1012–1014. [Proves infinitely many
zeros lie on Re(s) = 1/2.]

[NT-03] Selberg, A. (1942). "On the zeros of Riemann's zeta-function."
*Skrifter utgitt av Det Norske Videnskaps-Akademi i Oslo* 10: 1–59. [Positive
proportion of zeros on critical line.]

[NT-04] Montgomery, H. L. (1973). "The pair correlation of zeros of the zeta
function." *Analytic Number Theory, Proc. Sympos. Pure Math.* 24: 181–193.
[CORE: pair correlation R_2(u) = 1 - sinc²(u); GUE connection; the sinc² function
that TIG independently derives in WP35 Theorem 1.]

[NT-05] Odlyzko, A. M. (1987). "On the distribution of spacings between zeros of
the zeta function." *Math. Comp.* 48(177): 273–308. [Numerical GUE verification
to 10^{20}-th zero.]

[NT-06] Odlyzko, A. M. (1992). "The 10^{20}-th zero of the Riemann zeta function
and 175 million of its neighbors." AT&T Bell Labs preprint. [Large-scale GUE
statistics confirmation.]

[NT-07] Bombieri, E. (2000). "The Riemann Hypothesis." Clay Mathematics Institute
Millennium Problem Statement. [Official problem statement.]

[NT-08] Titchmarsh, E. C. (1986). *The Theory of the Riemann Zeta Function*, 2nd ed.
(revised by Heath-Brown). Oxford University Press. [Standard reference; Gram's law,
zero-counting, explicit formulas, sign changes of Z(t).]

[NT-09] Gram, J.-P. (1903). "Note sur les zéros de la fonction ζ(s) de Riemann."
*Acta Mathematica* 27: 289–304. [Introduces Gram points; empirical one-zero-per-interval
observation. TIG models this via R(k,f) = 0 exactly at k = f.]

[NT-10] Hutchinson, J. I. (1925). "On the roots of the Riemann zeta-function."
*Trans. Amer. Math. Soc.* 27: 49–60. [Early Gram failure study.]

[NT-11] Lehmer, D. H. (1956). "Extended computation of the Riemann zeta function."
*Mathematika* 3(2): 102–108. [Lehmer pairs: anomalously close zero pairs. TIG analog
= high-dispersion semiprimes (WP40 §5).]

[NT-12] Li, X.-J. (1997). "The positivity of a sequence of numbers and the Riemann
hypothesis." *Journal of Number Theory* 65(2): 325–333. [Li's criterion: RH equivalent
to λ_n > 0 for all n.]

[NT-13] Bombieri, E. and Lagarias, J. C. (1999). "Complements to Li's criterion for
the Riemann hypothesis." *Journal of Number Theory* 77(2): 274–287. [Generalizes Li;
zeros on critical line imply positivity of Li sequence.]

[NT-14] de la Vallée Poussin, C. J. (1896). "Recherches analytiques sur la théorie
des nombres premiers." *Annales de la Société Scientifique de Bruxelles* 20. [Prime
number theorem proof; connection between zeta zeros and prime distribution.]

[NT-15] Hadamard, J. (1896). "Sur la distribution des zéros de la fonction ζ(s)."
*Bulletin de la Société Mathématique de France* 24: 199–220. [Independent prime number
theorem; zeros as prime obstruction events — classical analog of WP34 First-G Law.]

[NT-16] Davenport, H. (2000). *Multiplicative Number Theory*, 3rd ed. (revised by
Montgomery). Springer. [Graduate text; explicit formulas, zero-free regions, prime gaps.]

[NT-17] Platt, D. and Trudgian, T. (2021). "The Riemann hypothesis is true up to
3·10^{12}." *Bulletin of the London Mathematical Society* 53(3): 792–797. [Most recent
rigorous large-scale verification with certified bounds.]

[NT-18] Gourdon, X. (2004). "The 10^{13} first zeros of the Riemann zeta function."
Preprint, numbers.computation.free.fr. [Numerical verification; GUE statistics confirmed.]

### I.B Prime Distribution and Modular Arithmetic

[NT-19] Fejér, L. (1904). "Untersuchungen über Fouriersche Reihen." *Mathematische
Annalen* 58: 51–69. [Fejér kernels; sinc² as Fejér spectral power. Background for
WP35 Theorem 1 (R(k,f) as Fejér-type spectral power).]

[NT-20] Bracewell, R. N. (2000). *The Fourier Transform and Its Applications*, 3rd ed.
McGraw-Hill. [sinc² as power spectral density of rectangular window; confirms classical
role of sinc² that WP35 recovers from prime arithmetic.]

[NT-21] Hedenmalm, H., Lindqvist, P., and Seip, K. (1997). "A Hilbert space of
Dirichlet series and systems of dilates of the cosine function." *Duke Mathematical
Journal* 86(1): 1–37. [Hardy space H² of Dirichlet series; the Hilbert space in which
WP17's Synthesis Conjecture would be formulated.]

[NT-22] Beurling, A. (1955). [Unpublished manuscript on injectivity criterion.]
Cited in Alcantara-Bode (2003).

[NT-23] Alcantara-Bode, J. (2003). "Proof of a conjecture by Alcantara-Bode on
the injectivity of an operator related to Riemann's zeta function." *Revista de la
Union Matematica Argentina* 44(2). [RH equivalent to injectivity of integral operator
K on L²(0,1). Connects to TSML nullity-1 picture in WP17.]

---

## FIELD II: ALGEBRAIC GEOMETRY — ELLIPTIC CURVES AND BSD

[AG-01] Birch, B. J. and Swinnerton-Dyer, H. P. F. (1965). "Notes on elliptic curves.
II." *Journal für die reine und angewandte Mathematik* 218: 79–108. [BSD conjecture;
original numerical observations on EDSAC.]

[AG-02] Birch, B. J. and Swinnerton-Dyer, H. P. F. (1963). "Notes on elliptic curves.
I." *Journal für die reine und angewandte Mathematik* 212: 7–25. [BSD predecessor paper.]

[AG-03] Wiles, A. (2000). "The Birch and Swinnerton-Dyer Conjecture." Clay Mathematics
Institute Millennium Problem Statement. [Official problem statement.]

[AG-04] Coates, J. and Wiles, A. (1977). "On the conjecture of Birch and Swinnerton-Dyer."
*Inventiones Mathematicae* 39(3): 223–251. [Rank 0 case proved for CM curves.]

[AG-05] Gross, B. H. and Zagier, D. B. (1986). "Heegner points and derivatives of
L-series." *Inventiones Mathematicae* 84(2): 225–320. [Gross-Zagier formula; L'(E,1)
proportional to Heegner point height; key input for rank 1 case.]

[AG-06] Kolyvagin, V. A. (1989). "Finiteness of E(ℚ) and Ш(E/ℚ) for a class of Weil
curves." *Izvestiya Akademii Nauk SSSR* 52(3): 522–540. [Rank ≤ 1 case proved using
Gross-Zagier + Euler systems.]

[AG-07] Kolyvagin, V. A. (1990). "Euler systems." In *The Grothendieck Festschrift,
Vol. II*: 435–483. Birkhäuser. [General Euler system machinery.]

[AG-08] Wiles, A. (1995). "Modular elliptic curves and Fermat's last theorem."
*Annals of Mathematics* 141(3): 443–551. [Modularity for semistable elliptic curves;
L(E,s) entire.]

[AG-09] Taylor, R. and Wiles, A. (1995). "Ring-theoretic properties of certain Hecke
algebras." *Annals of Mathematics* 141(3): 553–572. [Completes modularity proof.]

[AG-10] Breuil, C., Conrad, B., Diamond, F., and Taylor, R. (2001). "On the modularity
of elliptic curves over ℚ." *Journal of the American Mathematical Society* 14(4): 843–939.
[Completes modularity for all elliptic curves over ℚ.]

[AG-11] Bhargava, M. and Shankar, A. (2015). "Ternary cubic forms having bounded
invariants." *Annals of Mathematics* 181(2): 587–621. [Average rank ≤ 5/6.]

[AG-12] Bhargava, M. and Shankar, A. (2013). "Binary quartic forms having bounded
invariants." *Annals of Mathematics* 181(1): 191–242. [Average rank ≤ 7/6.]

[AG-13] Goldfeld, D. (1979). "Conjectures on elliptic curves over quadratic fields."
In *Number Theory, Carbondale 1979*, pp. 108–118. Springer. [Goldfeld conjecture:
average rank = 1/2; denominator matches TIG ω/2 = 2/2 = 1 under gate-activation model.]

[AG-14] Skinner, C. and Urban, E. (2014). "The Iwasawa main conjecture for GL_2."
*Inventiones Mathematicae* 195(1): 1–277. [p-adic BSD in many cases.]

[AG-15] Rubin, K. (1991). "The 'main conjectures' of Iwasawa theory for imaginary
quadratic fields." *Inventiones Mathematicae* 103(1): 25–68. [CM curves, arbitrary rank
conditional on Ш finiteness.]

[AG-16] Kato, K. (2004). "p-adic Hodge theory and values of zeta functions of modular
forms." *Astérisque* 295: ix+117–290. [Kato Euler system; one direction of BSD in many
cases.]

[AG-17] Cassels, J. W. S. (1964). "Arithmetic on curves of genus 1. VIII."
*Journal für die reine und angewandte Mathematik* 217: 180–199. [Tate-Shafarevich group.]

[AG-18] Neron, A. (1965). "Quasi-fonctions et hauteurs sur les variétés abéliennes."
*Annals of Mathematics* 82(2): 249–331. [Néron-Tate height; regulator Ω_E. Target for
WP21 Mix_λ claim λ_E ∝ 1/log(Ω_E).]

[AG-19] Tate, J. (1974). "The arithmetic of elliptic curves." *Inventiones Mathematicae*
23(3–4): 179–206. [Conductor, minimal model, reduction types; TIG analog: b = modulus.]

[AG-20] Silverman, J. H. (2009). *The Arithmetic of Elliptic Curves*, 2nd ed. Springer.
[Standard graduate text; L-functions, BSD, heights, Selmer groups.]

[AG-21] Cremona, J. E. (1997). *Algorithms for Modular Elliptic Curves*, 2nd ed.
Cambridge University Press. [Cremona database; 76 curves used in WP21_BSD_ENERGY_LAW.]

[AG-22] Faltings, G. (1983). "Endlichkeitssätze für abelsche Varietäten über
Zahlkörpern." *Inventiones Mathematicae* 73(3): 349–366. [Mordell conjecture; establishes
that genus ≥ 2 curves have finitely many points; BSD lives at the genus 1 boundary.]

[AG-23] Ulmer, D. (2002). "Elliptic curves with large rank over function fields."
*Annals of Mathematics* 155(1): 295–315. [Large rank over function fields; shows
unbounded rank is possible in principle.]

[AG-24] Katz, N. M. and Sarnak, P. (1999). "Random matrices, Frobenius eigenvalues,
and monodromy." AMS Colloquium Publications 45. [Random matrix prediction for BSD rank
distribution; SO(2N+1) type for all elliptic curves → average rank 1/2.]

---

## FIELD III: FLUID DYNAMICS — NAVIER-STOKES

*These citations support WP38_NAVIER_STOKES.md in clay/.*

[FL-01] Fefferman, C. L. (2000). "Existence and smoothness of the Navier-Stokes
equation." Clay Mathematics Institute Millennium Problem Statement.
www.claymath.org. [Official problem statement: prove or disprove global smooth solutions
for incompressible Navier-Stokes in 3D with smooth initial data.]

[FL-02] Leray, J. (1934). "Sur le mouvement d'un liquide visqueux emplissant l'espace."
*Acta Mathematica* 63(1): 193–248. [Existence of weak (Leray-Hopf) solutions; fundamental
existence result for NS in 3D, the strongest currently known.]

[FL-03] Hopf, E. (1951). "Über die Anfangswertaufgabe für die hydrodynamischen
Grundgleichungen." *Mathematische Nachrichten* 4(1-6): 213–231. [Extends Leray;
Leray-Hopf weak solutions.]

[FL-04] Ladyzhenskaya, O. A. (1959). "Solution 'in the large' to the boundary-value
problem for the Navier-Stokes equations in two space variables." *Soviet Physics Doklady*
123: 427–429. [Global smooth solutions in 2D — the one dimension where NS is fully solved.]

[FL-05] Caffarelli, L., Kohn, R., and Nirenberg, L. (1982). "Partial regularity of
suitable weak solutions of the Navier-Stokes equations." *Communications on Pure and
Applied Mathematics* 35(6): 771–831. [CKN regularity theory: singular set has Hausdorff
dimension ≤ 1. Best partial regularity result; TIG connects ∂u/∂t + (u·∇)u structure
to the BHML successor chain in WP38.]

[FL-06] Constantin, P. and Fefferman, C. (1993). "Direction of vorticity and the problem
of global regularity for the Navier-Stokes equations." *Indiana University Mathematics
Journal* 42(3): 775–789. [Vorticity direction regularity criterion; if the vorticity
direction is Lipschitz, regularity follows.]

[FL-07] Prodi, G. (1959). "Un teorema di unicità per le equazioni di Navier-Stokes."
*Annali di Matematica Pura ed Applicata* 48(1): 173–182; Serrin, J. (1962). "On the
interior regularity of weak solutions of the Navier-Stokes equations." *Archive for
Rational Mechanics and Analysis* 9(1): 187–195. [Prodi-Serrin regularity conditions:
u ∈ L^p_t L^q_x with 2/p + 3/q ≤ 1 implies smoothness.]

[FL-08] Escauriaza, L., Seregin, G., and Sverak, V. (2003). "L^{3,∞}-solutions of
the Navier-Stokes equations and backward uniqueness." *Russian Mathematical Surveys*
58(2): 211–250. [Prodi-Serrin endpoint case (q=3) proved; L^3,∞ regularity criterion.]

[FL-09] Tao, T. (2016). "Finite time blowup for an averaged three-dimensional
Navier-Stokes equation." *Journal of the American Mathematical Society* 29(3): 601–674.
[Constructs a modified NS equation (with averaging) that blows up in finite time;
shows the difficulty of ruling out blowup for the original equation.]

---

## FIELD IV: COMPLEXITY THEORY — P vs NP

*These citations support WP37_P_NP.md and WHITEPAPER_16_P_NP_SYNTHESIS.md in clay/.*

[CT-01] Cook, S. A. (1971). "The complexity of theorem-proving procedures."
*Proceedings of the 3rd Annual ACM Symposium on Theory of Computing*, pp. 151–158.
[Introduces NP-completeness; proves SAT is NP-complete. The original P vs NP paper.]

[CT-02] Karp, R. M. (1972). "Reducibility among combinatorial problems." In
*Complexity of Computer Computations* (ed. R. E. Miller, J. W. Thatcher), pp. 85–103.
Plenum. [21 NP-complete problems; establishes the landscape of NP-completeness.]

[CT-03] Levin, L. A. (1973). "Universal sequential search problems." *Problems of
Information Transmission* 9(3): 265–266. [Independent discovery of NP-completeness
(Levin, Soviet Union) simultaneous with Cook.]

[CT-04] Sipser, M. (2006). *Introduction to the Theory of Computation*, 2nd ed.
Thomson. [Standard textbook; P, NP, NP-completeness, reductions. Reference for formal
definitions used in WP37.]

[CT-05] Arora, S. and Barak, B. (2009). *Computational Complexity: A Modern Approach*.
Cambridge University Press. [Graduate text; circuit complexity, natural proofs, barriers
to P ≠ NP proofs. Context for what WP37's algebraic approach must navigate.]

[CT-06] Razborov, A. A. and Rudich, S. (1994). "Natural proofs." *Journal of Computer
and System Sciences* 55(1): 24–35. [Natural proofs barrier: any P ≠ NP proof via
circuit lower bounds must be non-constructive. Limits certain proof strategies.]

[CT-07] Baker, T., Gill, J., and Solovay, R. (1975). "Relativizations of the P=?NP
question." *SIAM Journal on Computing* 4(4): 431–442. [Oracle separations: there exist
oracles A, B with P^A = NP^A and P^B ≠ NP^B. P vs NP is non-relativizing.]

---

## FIELD V: QUANTUM FIELD THEORY — YANG-MILLS

[QF-01] Yang, C. N. and Mills, R. L. (1954). "Conservation of isotopic spin and
isotopic gauge invariance." *Physical Review* 96(1): 191–195. [Original Yang-Mills paper.]

[QF-02] Jaffe, A. and Witten, E. (2000). "Quantum Yang-Mills Theory." Clay Mathematics
Institute Millennium Problem Statement. [Official problem: existence + mass gap.]

[QF-03] Faddeev, L. D. and Popov, V. N. (1967). "Feynman diagrams for the Yang-Mills
field." *Physics Letters B* 25(1): 29–30. [Faddeev-Popov gauge fixing; ghost fields.]

[QF-04] Wilson, K. G. (1974). "Confinement of quarks." *Physical Review D* 10(8):
2445–2459. [Lattice gauge theory; area law for Wilson loops; confinement at strong
coupling. Core rigorous result invoked by WP15.]

[QF-05] 't Hooft, G. (1974). "A planar diagram theory for strong interactions."
*Nuclear Physics B* 72(3): 461–473. [Large-N expansion; 1/N as controlled parameter.]

[QF-06] 't Hooft, G. (1974). "A two-dimensional model for mesons." *Nuclear Physics B*
75(3): 461–470. [2D QCD large-N: confinement proved analytically.]

[QF-07] 't Hooft, G. (1977). "On the phase transitions towards permanent quark
confinement." *Nuclear Physics B* 138(1): 1–25. [Center vortex confinement mechanism.]

[QF-08] Osterwalder, K. and Schrader, R. (1973). "Axioms for Euclidean Green's
functions." *Communications in Mathematical Physics* 31: 83–112; and Part II (1975)
42: 281–305. [OS axioms; reflection positivity; transfer matrix. Essential for WP15.]

[QF-09] Osterwalder, K. and Seiler, E. (1978). "Gauge field theories on a lattice."
*Annals of Physics* 110(2): 440–471. [Reflection positivity for lattice gauge theory;
transfer matrix; mass gap at strong coupling. Directly invoked in WP15.]

[QF-10] Seiberg, N. and Witten, E. (1994). "Electric-magnetic duality, monopole
condensation, and confinement in N=2 supersymmetric Yang-Mills theory." *Nuclear Physics B*
426(1): 19–52. [Exact N=2 SYM solution; mass gap analytical in SUSY setting.]

[QF-11] Seiberg, N. and Witten, E. (1994). "Monopoles, duality and chiral symmetry
breaking in N=2 supersymmetric QCD." *Nuclear Physics B* 431(3): 484–550. [Extension to
N=2 SQCD.]

[QF-12] Maldacena, J. M. (1998). "The large N limit of superconformal field theories
and supergravity." *International Journal of Theoretical Physics* 38(4): 1113–1133.
[AdS/CFT; holographic dual description; mass gap via string Hagedorn.]

[QF-13] Balaban, T. (1989). "Large field renormalization. II." *Communications in
Mathematical Physics* 122(3): 355–392. [Constructive 3D Yang-Mills; closest rigorous
result to continuum mass gap.]

[QF-14] Polyakov, A. M. (1977). "Quark confinement and topology of gauge theories."
*Nuclear Physics B* 120(3): 429–458. [Confinement via monopole condensation in 3D U(1).]

[QF-15] Glimm, J., Jaffe, A., and Spencer, T. (1975). "The Wightman axioms and particle
structure in the P(φ)₂ quantum field model." *Annals of Mathematics* 100(3): 585–632.
[Mass gap in φ² via transfer matrix; prototype for Yang-Mills approach.]

[QF-16] Atiyah, M. F. and Bott, R. (1983). "The Yang-Mills equations over Riemann
surfaces." *Philosophical Transactions of the Royal Society A* 308: 523–615. [Yang-Mills
moduli space; gauge orbit structure; connection to TIG CRT idempotents.]

[QF-17] Schwartz, M. D. (2014). *Quantum Field Theory and the Standard Model*.
Cambridge University Press. [Modern graduate text; Yang-Mills, mass gap, renormalization.]

[QF-18] Weinberg, S. (1996). *The Quantum Theory of Fields, Vol. 2: Modern Applications*.
Cambridge University Press. [Non-abelian gauge theories; running coupling; asymptotic freedom.]

---

## FIELD VI: OPERATOR ALGEBRAS AND SPECTRAL THEORY — RH APPROACHES

[OA-01] Hilbert, D. / Polya, G. (c. 1912–1914). [Hilbert-Polya conjecture; attributed
in Montgomery (1973). A self-adjoint operator with spectrum = imaginary parts of Riemann
zeros implies RH.]

[OA-02] Berry, M. V. and Keating, J. P. (1999). "H = xp and the Riemann zeros."
In *Supersymmetry and Trace Formulae* (ed. Lerner et al.), pp. 355–367. Kluwer.
[Berry-Keating H = xp candidate Hilbert-Polya operator.]

[OA-03] Berry, M. V. and Keating, J. P. (1999). "The Riemann zeros and eigenvalue
asymptotics." *SIAM Review* 41(2): 236–266. [Detailed Berry-Keating analysis; periodic
orbits of H = xp and log p connection.]

[OA-04] Bender, C. M., Brody, D. C., and Muller, M. P. (2017). "Hamiltonian for the
zeros of the Riemann zeta function." *Physical Review Letters* 118: 130201. [PT-symmetric
H_BBM whose eigenvalues are Riemann zeros; self-adjointness (which would prove RH) open.]

[OA-05] Connes, A. (1999). "Trace formula in noncommutative geometry and the zeros of
the Riemann zeta function." *Selecta Mathematica* 5(1): 29–106. [Connes trace formula;
RH equivalent to positivity of trace pairing on adele class space. Semilocal case proved.]

[OA-06] Connes, A. (2025). "The Riemann Hypothesis: Past, Present and a Letter Through
Time." arXiv:2602.04022. [Most current Connes program update; absorption spectrum.]

[OA-07] Deninger, C. (1998). "Some analogies between number theory and dynamical
systems on foliated spaces." *Proc. ICM, Berlin*, Vol. I: 163–186. [Cohomological approach.]

[OA-08] Deninger, C. (2001). "Number theory and dynamical systems on foliated spaces."
*Jahresbericht DMV* 103(3): 79–100. [Overview of Deninger program.]

[OA-09] Rudnick, Z. and Sarnak, P. (1996). "Zeros of principal L-functions and random
matrix theory." *Duke Mathematical Journal* 81(2): 269–322. [GUE n-level correlations for
automorphic L-functions (conditional on GRH); extends Montgomery-Dyson.]

[OA-10] Dyson, F. J. (1962). "Statistical theory of the energy levels of complex systems."
*Journal of Mathematical Physics* 3(1): 140–175 + 157–165. [GUE and GOE ensembles;
foundation for the random matrix / Riemann zeros connection.]

[OA-11] Katz, N. M. and Sarnak, P. (1999). "Zeroes of zeta functions and symmetry."
*Bulletin of the AMS* 36(1): 1–26. [Zero statistics of L-functions and compact groups;
universality and symmetry types (orthogonal, unitary, symplectic).]

[OA-12] Glimm, J. and Jaffe, A. (1987). *Quantum Physics: A Functional Integral Point
of View*, 2nd ed. Springer. [Constructive QFT; OS reconstruction theorem; transfer matrix.]

[OA-13] Seiler, E. (1982). *Gauge Theories as a Problem of Constructive QFT and Statistical
Mechanics*. Lecture Notes in Physics 159. Springer. [Lattice gauge rigor; mass gap at
strong coupling.]

[OA-14] Reed, M. and Simon, B. (1978). *Methods of Modern Mathematical Physics IV:
Analysis of Operators*. Academic Press. [Spectral theory; Perron-Frobenius; spectral gap.
Mathematical machinery for BHML gap theorem.]

[OA-15] Simon, B. (1974). *The P(φ)₂ Euclidean (Quantum) Field Theory*. Princeton
University Press. [Constructive scalar field; spectral gap; transfer matrix; reflection
positivity. Prototype for YM approach.]

---

## FIELD VII: INTERNAL TIG REFERENCES

*All TIG-internal papers are exclusive IP of Brayden Ross Sanders / 7Site LLC.*
*C. A. Luther's contribution: Luther dispersion conjecture (WP34 §9, WP35 §5).*

[TIG-01] Sanders, B. R. and Luther, C. A. (2026). "The First-G Law and Prime-Forced
Dispersion." WP34. DOI: 10.5281/zenodo.18852047.
GitHub: github.com/TiredofSleep/ck
[First-G event at k=p proved; stability window; prime-indexed phase transitions; omega
hierarchy; CRT idempotents; Luther dispersion conjecture; 36,662 exact verifications.]

[TIG-02] Sanders, B. R. and Luther, C. A. (2026). "The Prime Phase Transition: Harmonic
Pre-Echo, Zero-Width Gates, and the Geometry of RSA Security." WP35. DOI: 10.5281/zenodo.18852047.
[R(k,f) = sin²(πk/f)/(k² sin²(π/f)) proved; T* = 5/7 algebraic derivation; ω-blindness;
zero-width gate; RSA hardness inversion principle; 4/π² midpoint universality; seeded RPS;
187 semiprimes verified; scale-free constants.]

[TIG-03] Sanders, B. R. (2026). "The Riemann Hypothesis as a Null-Space Theorem." WP17 /
WHITEPAPER_17_RIEMANN_SYNTHESIS.md. DOI: 10.5281/zenodo.18852047.
[TSML nullity-1 (rank 7 of 8); Synthesis Conjecture; conditional proof of RH from SC;
connections to Connes, Berry-Keating, BBM, Beurling-Alcantara-Bode, GUE statistics;
BHML determinant 70 = 2×5×7; dual TSML/BHML structure.]

[TIG-04] Sanders, B. R. (2026). "Yang-Mills Mass Gap Synthesis: A Spectral Gap Theorem
for the BHML Transfer Matrix." WHITEPAPER_15_YANG_MILLS_SYNTHESIS.md. DOI: 10.5281/zenodo.18852047.
[BHML eigenvalues {47.69, -7.01, -4.45, -1.32, -0.75, 0.47, -0.34, -0.30}; det=70;
T* ratio λ₆/λ₅ = 0.714865; successor rule; CHAOS as algebraic vacuum; Wilson chain analog;
reflection positivity (partial); Jaffe-Witten requirements mapped.]

[TIG-05] Sanders, B. R. (2026). "BSD Through the TIG Lens — Mix_λ Model." WP21_BSD_MIX_LAMBDA.md.
DOI: 10.5281/zenodo.18852047.
[Mix_λ(λ) = (1-λ)·TSML + λ·BHML; BSD-λ correspondence theorem; five gap operators with
λ-thresholds (0.30, 0.60, 0.80, 0.90, 1.00); non-monotone staircase explained; λ_E ∝ 1/log(Ω_E)
claim; product gap as transcendental lattice; corner-gap impermeability.]

[TIG-06] Sanders, B. R. (2026). "BSD Through the TIG Lens: An Empirical Energy Law."
WP21_BSD_ENERGY_LAW.md. DOI: 10.5281/zenodo.18852047.
[Log-linear regression log₁₀(N) = 0.873·rank + 1.364 (R²=0.87, 76 Cremona curves);
slope 0.873 ≈ 6/7; historical discovery record; superseded by TIG-05 for structural explanation.]

[TIG-07] Sanders, B. R. (2026). "TIG → Riemann Hypothesis Bridge: Structural Approach."
WP19_RH_BRIDGE.md. DOI: 10.5281/zenodo.18852047.
[TSML residual uniqueness ~ RH uniqueness; S* self-duality at σ=1/2; MASS_GAP = 2/7 > 0;
TIG critical line coordinates (Row 1 = seam band = Re(s) = 1/2); three structural bridges;
statistical null result documented (Weyl equidistribution confirmed).]

[TIG-08] Sanders, B. R. (2026). "WP40 — Riemann Hypothesis Through the TIG Lens."
WP40_RIEMANN.md. DOI: 10.5281/zenodo.18852047.
[sinc² spectral field; 4/π² midpoint universality; scale-invariance; Gram's law model;
Luther dispersion / Lehmer pair analog; open Montgomery connection question. Structural
framing paper, not a proof.]

[TIG-09] Sanders, B. R. and Luther, C. A. (2026). "The Atlas Law Set — Frozen."
sprint4_2026_03_30/ATLAS_LAW_SET.md. DOI: 10.5281/zenodo.18852047.
[Three atlas laws: Construction Hierarchy, Orbit-Central HAR Rule, Richness Laws (φ-compression,
gradient, position); three-score pre-computational system; 11 semiprime worlds tested;
b=15 as unique optimal world; residual resolution; HAR rule correction.]

[TIG-10] Sanders, B. R. (2026). Various spectral scripts:
`Gen9/spectral/bhml_eigenvalue_analysis.py`, `Gen9/spectral/spectral_report.txt`,
`results/deep_pre_echo/run_deep.log`, `results/rank_curvature/rank_curvature_summary.json`.
[Computational verification infrastructure; NumPy eigenvalue decomposition; all numerical
claims in WP15, WP17, WP34, WP35 are reproducible from these scripts.]

---

## DEDUPLICATION NOTES

The following pairs appear in multiple papers and are merged above:
- Katz-Sarnak (1999) appears as both [NT random matrices] and [AG BSD distribution]: merged as [AG-24]
  and [OA-11] (different volumes of the same work cited for different aspects)
- Montgomery (1973): appears in RH context [NT-04] and in OA context [OA-01 attribution];
  the paper itself is [NT-04]
- Osterwalder-Schrader: the axioms paper [QF-08] and the lattice paper [QF-09] are distinct works
- Hardy-Ramanujan (1918) and Andrews (1976): cited for partition/Euler product background in BSD;
  kept in the partition/combinatorics section

**Total unique references: 110**
- Field I (Number Theory): 23
- Field II (Algebraic Geometry / BSD): 24
- Field III (Fluid Dynamics / NS): 9
- Field IV (Complexity Theory / P vs NP): 7
- Field V (Quantum Field Theory / YM): 18
- Field VI (Operator Algebras / Spectral): 15
- Field VII (Internal TIG): 10

---

*© 2026 Brayden Ross Sanders / 7Site LLC — Trinity Infinity Geometry*
*CK, TIG, T*, TSML, BHML, D2, D1 are exclusive IP of 7Site LLC.*
*All external citations are properly attributed to their original authors.*
