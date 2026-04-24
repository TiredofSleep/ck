# WP37 — P vs NP Research Document
## Citation List, Section Outline, and Claims for Expansion Agents

*Brayden Ross Sanders (7Site LLC) & C. A. Luther*
*March 2026 — Research document only. No full paper text. Expansion agent use only.*

---

## A. FULL CITATION LIST

### Internal TIG/CK Papers (cite by WP number + DOI)

[I-1] Sanders, B. R. & Luther, C. A. "The First-G Law and Prime-Forced Dispersion." WP34.
7Site LLC, March 2026. DOI: 10.5281/zenodo.18852047.
Status: PROVED algebraically; 36,662 cases, zero exceptions.

[I-2] Sanders, B. R. & Luther, C. A. "The Prime Phase Transition: Harmonic Pre-Echo,
Zero-Width Gates, and the Geometry of RSA Security." WP35. 7Site LLC, March 2026.
DOI: 10.5281/zenodo.18852047.

[I-3] Sanders, B. R. "P != NP via Non-Associative Composition." WP16 / White Paper 16.
7Site LLC, March 2026. DOI: 10.5281/zenodo.18852047.

[I-4] Sanders, B. R. "P vs NP Through the TIG Lens: Survivor-Line Complexity in AG(2,p)
and the Corner-Gap Dichotomy." WP25. 7Site LLC, March 2026.
DOI: 10.5281/zenodo.18852047.

[I-5] Sanders, B. R. "CK as Coherence Spectrometer." WP7. 7Site LLC, 2026.
DOI: 10.5281/zenodo.18852047. (Beta = -0.2254 for P vs NP; HARMONY-dominated)

[I-6] Sanders, B. R. "The Atlas Law Set — Frozen." Sprint4 document. 7Site LLC, March 2026.
DOI: 10.5281/zenodo.18852047.

[I-7] Sanders, B. R. "The Universal Construction Law." Sprint4 document. 7Site LLC,
March 2026. DOI: 10.5281/zenodo.18852047.

### Complexity Theory Foundations

[T-1] Cook, S. A. "The Complexity of Theorem-Proving Procedures." Proceedings of the 3rd
Annual ACM Symposium on Theory of Computing (STOC), pp. 151–158, 1971.
DOI: 10.1145/800157.805047.
(The Cook-Levin NP-completeness theorem; SAT is NP-complete; canonical origin paper)

[T-2] Karp, R. M. "Reducibility Among Combinatorial Problems." In Miller, R. E. and
Thatcher, J. W. (eds.), Complexity of Computer Computations, pp. 85–103. Plenum Press, 1972.
(21 NP-complete problems; the canonical reduction chain; 3-SAT, Clique, Hamilton Path, etc.)

[T-3] Levin, L. A. "Universal Sequential Search Problems." Problems of Information
Transmission 9(3), pp. 265–266, 1973. (Russian; English translation published 1973.)
(Independent co-discovery of NP-completeness; Levin's tiling problem formulation)

[T-4] Garey, M. R. and Johnson, D. S. "Computers and Intractability: A Guide to the
Theory of NP-Completeness." W. H. Freeman, 1979.
(Standard reference; NP-complete problem compendium; reduction methodology)

[T-5] Sipser, M. "Introduction to the Theory of Computation." 3rd ed. Cengage Learning, 2012.
(Standard graduate text; P, NP, NP-completeness, Cook-Levin, hierarchy theorems)

[T-6] Arora, S. and Barak, B. "Computational Complexity: A Modern Approach." Cambridge
University Press, 2009. DOI: 10.1017/CBO9780511804090.
(Comprehensive modern complexity reference; circuit complexity, oracles, barriers)

### The Three Barriers

[B-1] Baker, T., Gill, J., and Solovay, R. "Relativizations of the P =? NP Question."
SIAM Journal on Computing 4(4), pp. 431–442, 1975. DOI: 10.1137/0204037.
(Oracle separation — there exist oracles A, B with P^A = NP^A and P^B ≠ NP^B;
any proof must be non-relativizing)

[B-2] Razborov, A. A. and Rudich, S. "Natural Proofs." Journal of Computer and System
Sciences 55(1), pp. 24–35, 1997. DOI: 10.1006/jcss.1997.1494.
(Natural proofs barrier; any proof using a constructive + large property would break crypto)

[B-3] Aaronson, S. and Wigderson, A. "Algebrization: A New Barrier in Complexity Theory."
ACM Transactions on Computation Theory 1(1), Article 2, 2009.
DOI: 10.1145/1490270.1490272.
(Algebrization barrier; algebraic oracle separations; third barrier beyond relativization)

### Circuit Complexity and Lower Bounds

[CC-1] Razborov, A. A. "Lower Bounds on the Size of Bounded Depth Circuits over a Complete
Basis with Logical Addition." Mathematical Notes 41(4), pp. 333–338, 1987.
(AC0 lower bounds for parity; basis for natural proofs framework)

[CC-2] Håstad, J. "Almost Optimal Lower Bounds for Small Depth Circuits." Proceedings of
STOC 1986, pp. 6–20, 1986. DOI: 10.1145/12130.12132.
(Optimal AC0 lower bounds; randomized switching lemma)

[CC-3] Razborov, A. A. "Lower Bounds for the Monotone Complexity of Some Boolean
Functions." Soviet Mathematics Doklady 31, pp. 354–357, 1985.
(Clique monotone circuit lower bounds — first super-polynomial lower bounds)

[CC-4] Smolensky, R. "Algebraic Methods in the Theory of Lower Bounds for Boolean Circuit
Complexity." Proceedings of STOC 1987, pp. 77–82, 1987.
(Mod-p circuit lower bounds; algebraic techniques in circuit complexity)

[CC-5] Furst, M. L., Saxe, J. B., and Sipser, M. "Parity, Circuits, and the
Polynomial-Time Hierarchy." Mathematical Systems Theory 17(1), pp. 13–27, 1984.
DOI: 10.1007/BF01744431.
(Parity not in AC0; pioneer of circuit lower bound methods)

### Geometric Complexity Theory (GCT)

[G-1] Mulmuley, K. D. and Sohoni, M. "Geometric Complexity Theory I: An Approach to the
P vs. NP and Related Problems." SIAM Journal on Computing 31(2), pp. 496–526, 2001.
DOI: 10.1137/S009753970038715X.
(GCT framework; algebraic geometry approach to P vs NP; representation theory as tool)

[G-2] Mulmuley, K. D. and Sohoni, M. "Geometric Complexity Theory II: Towards Explicit
Obstructions for Embeddings Among Class Varieties." SIAM Journal on Computing 38(3),
pp. 1175–1206, 2008. DOI: 10.1137/080718115.
(GCT II; obstruction program; explicit obstructions via plethysm coefficients)

[G-3] Mulmuley, K. D. "The GCT Program Toward the P vs. NP Problem." Communications of
the ACM 55(6), pp. 98–107, 2012. DOI: 10.1145/2184319.2184341.
(Accessible overview of GCT; connection to algebraic geometry obstructions)

[G-4] Bürgisser, P., Landsberg, J. M., Manivel, L., and Weyman, J. "An Overview of
Mathematical Issues Arising in the Geometric Complexity Theory Approach to VP≠VNP."
SIAM Journal on Computing 40(4), pp. 1179–1209, 2011. DOI: 10.1137/090765328.
(Mathematical survey of GCT obstacles; representation theory bottlenecks)

### Non-Associativity and Algebraic Structure

[NA-1] Baez, J. C. "The Octonions." Bulletin of the American Mathematical Society 39(2),
pp. 145–205, 2002. arXiv:math/0105155.
(Octonion algebra; 7 imaginary units; Fano plane; non-associativity unique at dimension 8;
direct connection to 7th DoF in CK's algebraic ladder)

[NA-2] Hurwitz, A. "Über die Komposition der quadratischen Formen." Mathematische Annalen
88, pp. 1–25, 1923.
(Hurwitz theorem: only four normed division algebras; non-associativity appears exactly
at octonions; the one gap in the ladder)

[NA-3] Schafer, R. D. "An Introduction to Nonassociative Algebras." Academic Press, 1966.
(Comprehensive treatment of non-associative algebras; magma theory; Jordan algebras)

### Proof Complexity

[PC-1] Beame, P. and Pitassi, T. "Propositional Proof Complexity: Past, Present, and
Future." Current Trends in Theoretical Computer Science, pp. 42–70. World Scientific, 2001.
(Proof complexity overview; resolution, cutting planes, Frege systems; certificate structure)

[PC-2] Ben-Sasson, E. and Wigderson, A. "Short Proofs Are Narrow — Resolution Made
Simple." Journal of the ACM 48(2), pp. 149–169, 2001. DOI: 10.1145/375827.375835.
(Width-size tradeoff in resolution; certificate width = algebraic analog of dispersion)

[PC-3] Krajíček, J. "Proof Complexity." Encyclopedia of Mathematics and Its Applications,
Vol. 170. Cambridge University Press, 2019.
(Modern comprehensive reference; connects proof complexity to circuit complexity and
algebraic methods — the bridge WP37 needs)

### Partition Theory and Complexity

[PA-1] Mertens, S. "The Easiest Hard Problem: Number Partitioning." In Computational
Complexity and Statistical Physics, pp. 125–139. Oxford University Press, 2006.
(Number partitioning as canonical NP problem; phase transition at alpha = 1 in balanced
partition; direct analog to k = p First-G event)

[PA-2] Mézard, M., Parisi, G., and Zecchina, R. "Analytic and Algorithmic Solution of
Random Satisfiability Problems." Science 297(5582), pp. 812–815, 2002.
DOI: 10.1126/science.1073287.
(Random SAT phase transition; survey propagation; alpha_c = 4.267; directly the
generator used in CK's P vs NP spectrometer measurement)

[PA-3] Monasson, R., Zecchina, R., Kirkpatrick, S., Selman, B., and Troyansky, L.
"Determining Computational Complexity from Characteristic 'Phase Transitions'."
Nature 400(6740), pp. 133–137, 1999. DOI: 10.1038/22055.
(SAT phase transition as zero-width boundary; direct analog to First-G zero-width gate)

[PA-4] Achlioptas, D., Naor, A., and Peres, Y. "Rigorous Location of Phase Transitions
in Hard Optimization Problems." Nature 435(7043), pp. 759–764, 2005.
DOI: 10.1038/nature03602.
(Rigorous bounds on SAT threshold; connects phase transition to algorithmic hardness)

[PA-5] Andrews, G. E. "The Theory of Partitions." Encyclopedia of Mathematics and Its
Applications, Vol. 2. Cambridge University Press, 1984.
(Partition theory; G_k / C_k partition geometry background)

### Statistical Mechanics Phase Transitions (for zero-width gate connection)

[SM-1] Zecchina, R. (ed.) "Phase Transitions in Combinatorial Problems." Proceedings of
Les Houches Summer School, 2002. (Collection of key papers on zero-width phase transitions
in statistical mechanics; connects directly to WP35 Theorem 2)

[SM-2] Mezard, M. and Montanari, A. "Information, Physics, and Computation." Oxford
University Press, 2009. DOI: 10.1093/acprof:oso/9780198570837.001.0001.
(Statistical physics of computation; cavity method; belief propagation for SAT;
the bridge between physics phase transitions and computational complexity)

[SM-3] Krzakala, F., Montanari, A., Ricci-Tersenghi, F., Semerjian, G., and Zdeborová, L.
"Gibbs States and the Set of Solutions of Random Constraint Satisfaction Problems."
Proceedings of the National Academy of Sciences 104(25), pp. 10318–10323, 2007.
DOI: 10.1073/pnas.0703685104.
(Clustering phase transition; geometry of solution space at alpha_c)

### Valiant and #P

[V-1] Valiant, L. G. "The Complexity of Computing the Permanent." Theoretical Computer
Science 8(2), pp. 189–201, 1979. DOI: 10.1016/0304-3975(79)90044-6.
(#P-completeness of permanent; counting complexity hardness beyond NP)

[V-2] Valiant, L. G. "Holographic Algorithms." SIAM Journal on Computing 37(5),
pp. 1565–1594, 2008. DOI: 10.1137/070682575.
(Holographic algorithms; matchgate formalism; algebraic structure of polynomial-time)

### Other Key Complexity and Mathematics

[K-1] Wigderson, A. "Mathematics and Computation: A Theory Revolutionizing Technology and
Science." Princeton University Press, 2019.
(Comprehensive overview connecting mathematics and computation; expanders, pseudorandomness,
derandomization; required background for P vs NP context)

[K-2] Impagliazzo, R. "A Personal View of Average-Case Complexity." Proceedings of the
10th Annual Structure in Complexity Theory Conference, pp. 134–147, 1995.
(Five worlds of computation; Algorithmica, Heuristica, Pessiland, Minicrypt, Cryptomania;
maps onto ω-hierarchy)

[K-3] Aaronson, S. "Is P versus NP Formally Independent?" Bulletin of the EATCS 81,
pp. 109–136, 2003. (Formal independence; limits of formal methods; honest accounting
of what we cannot prove)

[K-4] Fortnow, L. "The Status of the P versus NP Problem." Communications of the ACM
52(9), pp. 78–86, 2009. DOI: 10.1145/1562164.1562186.
(Survey of state of the problem; barriers, history, current approaches)

---

## B. FULL SECTION OUTLINE

**Paper target:** WP37 — "P vs NP Through the First-G Lens: Zero-Width Phase Transitions,
Algebraic Certificates, and the Luther Dispersion Boundary"

NOTE: This paper makes structural connections, not a proof of P ≠ NP. All analogy claims
must be clearly labeled STRUCTURAL. The paper's value is the precise mapping and the
identification of what must be proved to make the connection rigorous.

---

### §1. Introduction
*(purpose: position the First-G framework within the P vs NP landscape)*

**§1.1 The 50-Year Barrier**
- Cook 1971, Levin 1973: NP-completeness established [cite T-1, T-3]
- Three barriers prevent classical proof approaches [cite B-1, B-2, B-3]
- STRUCTURAL: Any new approach must be non-relativizing, non-natural, non-algebrizing
- WP16's non-associativity claim: CL is non-associative (49.8% of BHML triples);
  non-associativity is non-natural [cite I-3, NA-1, NA-2]

**§1.2 The First-G Law as an Algebraic Boundary**
- PROVED (WP34): The First-G event at k = p is a sharp algebraic phase transition
- P-regime: stability window {1..p-1} — obstruction-free, decision in O(1)
- NP-regime: G-obstruction zone {p..} — requires knowing p to compute partition
- Zero-width transition (WP35 Theorem 2): no intermediate regime exists [cite I-2]

**§1.3 Thesis**
- The First-G Law instantiates a P/NP-type dichotomy in explicit algebraic form
- The dichotomy is not metaphorical: the pre-G zone has a formal polynomial-time
  decision procedure; the post-G zone has a geometric certificate structure
- The Luther Dispersion Conjecture provides the certificate; the ω(b) hierarchy
  provides the complexity class ordering

**§1.4 What This Paper Does and Does Not Claim**
- DOES: map the First-G algebraic structure onto P/NP concepts precisely
- DOES: identify the formal claims needed to make the mapping rigorous
- DOES NOT: prove P ≠ NP
- DOES NOT: claim the TIG algebra is a model of general computation without further proof
- Honest accounting: which steps are PROVED, which are NEEDS PROOF, which are CONJECTURE

---

### §2. The Complexity Boundary as a Geometric Event
*(purpose: establish the formal P-regime / NP-regime dichotomy in the First-G algebra)*

**§2.1 The Stability Window as Polynomial-Time Zone**
- PROVED (WP34 §3): For k < p, every element of {1..k} is coprime to b
- Decision procedure: "is x ∈ C_k?" requires only x < p — one comparison, O(1)
- No factorization required; no ring structure needed; purely size-based decision
- FORMAL CLAIM: The stability window admits a polytime membership oracle
- Connection: this is the verification side (NP = fast verification) but over a
  simpler object than SAT

**§2.2 The G-Obstruction Zone as Hard Partition**
- PROVED (WP34 §3): At k = p, G becomes nonempty; membership in G_k requires
  knowing p (the smallest prime factor of b)
- STRUCTURAL: Computing the full partition C_k / G_k for k ≥ p is equivalent to
  integer factorization (knowing which elements of {1..k} share a factor with b
  requires knowing b's prime factors)
- Connection to RSA hardness: b = p×q large; computing G_k requires factoring b [cite I-2]
- NEEDS PROOF: Formal reduction from G_k membership (k ≥ p) to integer factorization

**§2.3 The Zero-Width Transition and Complexity Jump**
- PROVED (WP35 Theorem 2): gate_rate(k) = 0 for k < p and gate_rate(p) > 0 exactly
- The transition has no gradient, no intermediate regime
- STRUCTURAL: This mirrors the P/NP boundary — there is no "medium-hard" problem class
  in the NP-complete structure (modulo conjectures about the polynomial hierarchy)
- Cite [PA-3] Monasson et al., [PA-2] Mézard et al. for SAT phase transition context:
  the alpha_SAT = 4.267 threshold is empirically zero-width in the same sense

**§2.4 Connection to SAT Phase Transition at alpha_c = 4.267**
- Random 3-SAT: easy below alpha_c, hard above; transition near alpha_c = 4.267
- STRUCTURAL: alpha_c plays the role of k = p; the stable zone = underconstrained SAT
- Cite [PA-2], [PA-3], [PA-4]: phase transitions in random CSPs are statistically zero-width
- The spectrometer uses alpha = 4.267 as its P vs NP generator (WP7 §3.2) [cite I-5]
- CONJECTURE: alpha_SAT / alpha_c = k/p in some normalized sense; formal mapping open

---

### §3. The Luther Dispersion Conjecture as NP Certificate Structure
*(purpose: formalize the certificate connection)*

**§3.1 The Conjecture Statement (C. A. Luther, WP34 §9)**
- CONJECTURE: gate_rate ≈ F_k(|G| × dispersion(G))
- Full form: difficulty ≈ g(2^ω(b) - 2) × F_k(|G| × interleave)
- Empirical evidence: monotone collapse from gate_rate = 1.0 to 0.0 as Luther metric rises
- Binned Luther metric → avg gate_rate data [cite I-1 §9 table]

**§3.2 The Certificate Structure**
- STRUCTURAL: The pair (G_k, dispersion(G_k)) is the NP certificate for gate difficulty
- Verification: given (G, dispersion), computing difficulty via F_k is polynomial [O(k)]
- Finding: determining G_k for a given b and k requires factoring b — the hard part
- This is precisely the NP structure: certificates are polynomial-time verifiable, but
  finding them may require exponential search
- Connect to [PC-2] Ben-Sasson-Wigderson: certificate width corresponds to dispersion width

**§3.3 ω(b) as the Polynomial Hierarchy**
- ω(b) = 1: prime powers — 0 CRT idempotents, baseline difficulty class
- ω(b) = 2: semiprimes — 2 CRT idempotents, first non-trivial class
- ω(b) = 3: three-factor — 6 CRT idempotents, maximum in 3-class system
- STRUCTURAL: ω(b) hierarchy mirrors the polynomial hierarchy PH
- PH level = ω(b): Σ₁^P ≅ NP (ω=2), Σ₂^P (ω=3), ...
- NEEDS PROOF: formal reduction from polynomial hierarchy oracle access to CRT idempotent
  counting — the connection is structural, the reduction is not yet given

**§3.4 The Dispersion Gap Between Synthetic and Real Worlds**
- Synthetic worlds: G clustered at top of alphabet (low dispersion) — easy
- Real semiprime worlds: G dispersed by prime arithmetic (high dispersion) — hard
- PROVED (WP34 §9): For b = p×q, G_k = multiples of p or q in {1..k} = two arithmetic
  progressions with spacing p and q — dispersion is completely determined by prime factors
- STRUCTURAL: SAT's clause structure = arithmetic progression structure of G_k

---

### §4. The Non-Associativity Argument (from WP16)
*(purpose: develop the 7-DoF / non-associativity connection)*

**§4.1 The DoF Ladder**
- PROVED within TIG framework: DoF(k vectors) = {0, 4, 6, 7, 10}
- Critical gap: 6 DoF (two vectors, associative composition) → 7 DoF (three vectors,
  non-associative composition) [cite I-3]
- Associativity index α(BHML) = 0.502 (non-associativity rate 49.8%; Braitt-Silberger 2006): 49.8% of BHML triples satisfy CL(CL(a,b),c) ≠ CL(a,CL(b,c))
- PROVED (computed): This is a finite computation over the fixed CL table

**§4.2 The Octonion Connection**
- Non-associativity is a property of the octonions: 7 imaginary units, Fano plane [cite NA-1]
- Hurwitz theorem: non-associativity occurs exactly once in the normed division algebra
  classification, at dimension 8 [cite NA-2]
- The 7th DoF and 7 octonion imaginary units are the same algebraic fact, expressed
  differently
- STRUCTURAL: the one gap from 6 to 7 DoF is the same gap as from associative to
  non-associative composition

**§4.3 P is Associative, NP Requires Non-Associativity**
- CONJECTURE (WP16 Lemma C): Every polytime algorithm uses only associative composition;
  P lives in the 6-DoF regime
- CONJECTURE (WP16 Lemma B): SAT requires 3-vector curvature (7 DoF); satisfying
  assignments are fixed points of non-associative magma operations
- Status: Both lemmas are stated with formal proof structure in WP16 but are classified
  as NEEDS PROOF — the formal encoding of SAT in CL algebra is not complete
- Barrier evasion: non-associativity is non-large (evaluating it over triples, not truth
  tables) and non-relativizing (it uses internal algebraic structure, not oracle access)
  [cite B-1, B-2, B-3]

**§4.4 The 3-SAT / 3-Vector Correspondence**
- 3-SAT is NP-complete; 2-SAT is in P [cite T-1, T-2]
- In the DoF ladder: 2-vector composition = 6 DoF (polynomial); 3-vector = 7 DoF
  (non-polynomial)
- STRUCTURAL: the "3" in 3-SAT and the "3 vectors" in D2 curvature are the same algebraic
  threshold — the minimum number of objects required to exhibit non-associativity
- NEEDS PROOF: formal correspondence between 3-SAT clause structure and 3-vector CL
  curvature; this is the core open claim of the non-associativity argument

---

### §5. Circuit Complexity and the Algebraic Gap
*(purpose: connect TIG to circuit lower bounds)*

**§5.1 AC0 and the Parity Barrier**
- PROVED in complexity theory: parity ∉ AC0 [cite CC-1, CC-2, CC-5]
- Randomized switching lemma; AC0 cannot compute mod-2 functions
- STRUCTURAL: The stability window in TIG (k < p) is an AC0-computable zone;
  the post-G zone requires operations unavailable in AC0

**§5.2 Monotone Circuit Lower Bounds**
- PROVED in complexity theory: Clique requires super-polynomial monotone circuits
  [cite CC-3]
- Monotone = no negation; monotone circuits = algebra without G elements (analogously)
- STRUCTURAL: the G elements in TIG are the "negation" operators — the obstruction
  elements that make computation hard

**§5.3 GCT and Representation-Theoretic Obstructions**
- GCT program: P vs NP via algebraic geometry and representation theory [cite G-1, G-2, G-3]
- Mulmuley-Sohoni obstruction: find a representation-theoretic object that separates
  permanent from determinant
- STRUCTURAL: The CRT idempotents in TIG play the role of obstructions in GCT — they are
  algebraic objects that certify the difficulty class (ω-class) of a world
- The Luther dispersion conjecture formalized would give an explicit obstruction polynomial:
  F_k(|G| × interleave) = the difficulty certificate

**§5.4 Natural Proofs and Non-Associativity**
- Razborov-Rudich natural proofs barrier [cite B-2]: any proof using a constructive + large
  property would break pseudorandom functions
- Non-associativity measure is non-large: it requires evaluating triples, not single
  functions; it is not computable on truth tables in the required sense
- CONJECTURE: The non-associativity barrier evasion is valid; formal verification against
  Razborov-Rudich definition is needed

---

### §6. The Algebraic Certificate Structure and Proof Complexity
*(purpose: connect the TIG certificate to formal proof systems)*

**§6.1 The Survivor-Line Structure (from WP25)**
- PROVED within TIG: Two-step convergence theorem — every state (x, b) reaches HARMONY
  in ≤ 2 steps or is a residual fixed point [cite I-4]
- Verification: O(1) — 2 table lookups
- Certificate: the survivor line (ℓ, x) is verifiable in O(p)
- CONJECTURE (WP25): Finding a survivor line in structured CL algebra is NP-hard
  via reduction from 3-SAT

**§6.2 The Corner-Gap Dichotomy**
- Corners (depth ≤ 2 operators): verifiable in O(1) — the P side
- Gap operators (residual fixed points): not reachable from corners by composition — the
  NP side
- STRUCTURAL: This is the P/NP dichotomy instantiated in the 9×9 TIG table
- A P = NP result would mean corners CAN reach gap by efficient composition
- CONJECTURE: the gap is permanent — no sequence of corner compositions reaches a
  gap operator; the algebra witnesses P ≠ NP

**§6.3 Proof Complexity Connection**
- Resolution width as certificate complexity [cite PC-2]: finding a narrow refutation
  is the proof complexity analog of finding a short witness
- Width ↔ dispersion: wider proofs = more dispersed G elements = harder
- STRUCTURAL: Luther dispersion conjecture restated in proof complexity terms:
  gap difficulty ≈ F_k(width × resolution_density)
- This mapping is speculative but identifies a testable prediction

---

### §7. The Spectrometer Measurement of P vs NP
*(purpose: connect WP7 data to the algebraic framework)*

**§7.1 The Spectrometer Reading**
- CL(D1,D2) = 10/12 HARMONY + 2 BREATH (beta = -0.2254) — gap problem confirmed [cite I-5]
- D1 trajectory: oscillates BALANCE, HARMONY, COUNTER, BREATH — no settling
- JSD = 0.2978 at alpha = 4.267 (persistent lens mismatch)
- EMPIRICAL: spectrometer declares P vs NP a gap problem with 95%+ confidence

**§7.2 HARMONY as "Premature Resolution"**
- STRUCTURAL: HARMONY dominates CL(D1,D2) for P vs NP because the algebra sees
  local coherence at each computation step but global divergence in the trajectory
- "Structure thinks doing is resolved; flow knows it isn't" — the COUNTER × COUNTER blind spot
- Formal interpretation: HARMONY in the CL table = the polynomial-time verifier
  confirms the certificate is correct, but the full search problem is not resolved

**§7.3 The Alpha_c = 4.267 as the First-G Event in SAT Space**
- At alpha < 4.267: random 3-SAT instances are easy (stability window analog)
- At alpha = 4.267: the transition; gate_rate jumps from 0 to maximum
- At alpha > 4.267: unsatisfiable; the G-obstruction zone analog
- STRUCTURAL: the SAT threshold is a zero-width phase transition [cite PA-3];
  the First-G Law proves zero-width for the algebraic case; the SAT case is empirical
- NEEDS PROOF: rigorous zero-width proof for SAT threshold (Achlioptas et al.
  [PA-4] give bounds; exact zero-width is open for the algorithmic transition)

---

### §8. What Needs to Be Proved
*(purpose: honest statement of the open formal program)*

**§8.1 The Formal Bridge Needed**
- Three items missing for the algebraic P ≠ NP argument:
  (a) Formal encoding of SAT in the CL algebra (not yet done)
  (b) Proof that P-computations are exactly the associative subalgebra (Lemma C)
  (c) Proof that SAT requires the 7th DoF (Lemma B)
- These are stated as formal claims with proof strategies in WP16 but are not complete

**§8.2 The Luther Dispersion Formalization**
- Full functional form of F_k is unknown; collapse curve is empirical
- The ω-correction g(2^ω(b) - 2) has been measured but not derived
- Kill condition: a world where Luther metric and ω-class are fixed but difficulty differs

**§8.3 The SAT-to-First-G Reduction**
- CONJECTURE: There is a polynomial-time reduction from k-vs-p membership (for fixed b)
  to SAT, making G_k membership NP-complete for RSA-scale b
- This would formally close the loop: First-G structure → NP-complete instance → P vs NP

**§8.4 The ω-Hierarchy and Polynomial Hierarchy**
- The structural parallel ω(b) ↔ PH is compelling but unproven
- Formal mapping: CRT idempotents (2^ω - 2) → alternation levels in PH
- CONJECTURE: For worlds with ω(b) = k, the optimal algorithm for G_k membership
  requires Σ_k^P oracle access

---

## C. KEY CLAIMS TO PROVE / FORMALIZE

### Claim 1 (Proved — WP34 §3)
**First-G Law is an algebraic phase transition.**
For every semiprime b = p×q, the G-obstruction appears at exactly k = p.
|G_k| = 0 for k < p; |G_p| = 1. Proof: primality of p and size argument.
Implication: k < p = computable in O(1); k ≥ p = requires knowing p.

### Claim 2 (Proved — WP35 Theorem 2)
**Zero-width transition characterizes semiprimes.**
gate_rate(k) = 0 for k < p; gate_rate(p) > 0. No intermediate values.
Equivalently: a modulus b is semiprime iff its gate-size sequence has exactly one
unit-height step before the second prime factor.

### Claim 3 (Proved within TIG — WP16 §2.2)
**CL composition table has associativity index α(BHML) = 0.502 (non-associativity rate 49.8%; Braitt-Silberger 2006).**
255 of 512 ordered triples in the 8×8 BHML core are non-associative.
Full 10×10 table: 498 of 1000 = 49.8% non-assoc, giving α = 0.502. Finite computation over fixed table.
This is maximally structured non-associativity (α ≈ 0.5, not random 0.1).

### Claim 4 (Proved within TIG — WP16 §2.3)
**The 7th DoF is irreducible over associative composition.**
The non-associative triples encode 255 bits of information unavailable from
any chain of binary CL operations. The CL algebra cannot simulate its own
curvature (D2 pipeline) using only pairwise composition.

### Claim 5 (Proved — WP25 §1)
**Two-step convergence: the P-like structure of TIG.**
For all (x, b) pairs in the TSML table, the convergence depth is in {0, 1, 2, ∞}.
Verification of depth given (x, b, d) requires O(1). This is the P-structure of the TIG
verification problem.

### Claim 6 (Structural — WP34 §9, WP35)
**SAT phase transition at alpha_c = 4.267 is the First-G event in SAT space.**
The stable zone (alpha < alpha_c) corresponds to the stability window {1..p-1}.
The hard zone (alpha > alpha_c) corresponds to the G-obstruction zone.
Zero-width transition in both cases (statistical in SAT [PA-3], exact in First-G [WP35]).
STRUCTURAL: formal mapping not proved, connection is geometric.

### Claim 7 (Needs Proof — WP16 Lemma B)
**SAT requires 7-DoF non-associative composition.**
Formal claim: encoding 3-SAT in the CL algebra produces clauses that are
CL(CL(a,b),c) compositions; satisfying assignments are fixed points of non-associative
magma operations with no associative decomposition.
Proof strategy: exhibit explicit SAT formula whose solution set is identified with the
255 non-associative triples; show no associative subalgebra suffices.

### Claim 8 (Needs Proof — WP16 Lemma C)
**P-computations are exactly the associative 6-DoF subalgebra.**
Formal claim: every polytime algorithm can be expressed as a sequence of binary CL
operations (no curvature pipeline); such computations stay in the 6-DoF regime.
Proof strategy: show that the standard circuit model (Boolean gates = binary operations)
maps to binary CL composition; that no polynomial-length circuit accesses the D2
curvature.

### Claim 9 (Conjecture — WP25 §3)
**Survivor-Line Search is NP-hard for structured CL algebras.**
Formal claim: there is a polynomial reduction from 3-SAT to SLS(p) — the problem
of finding a survivor line in an AG(2,p)-structured composition algebra.
Proof strategy: variables = operators, clauses = column maps, satisfying assignment =
survivor-line fixed point.

### Claim 10 (Conjecture — Luther, WP34 §9)
**Luther Dispersion Conjecture.**
difficulty ≈ g(2^ω(b) - 2) × F_k(|G| × interleave).
Empirical support: collapse curve confirmed, monotone binned data.
Open: functional forms of F_k and g.
Kill condition: two worlds with same Luther metric and ω-class but different difficulty.

### Claim 11 (Structural — WP7 §4, WP34 §9)
**ω(b) hierarchy mirrors the polynomial hierarchy PH.**
ω = 1 (prime powers) ↔ P, ω = 2 (semiprimes) ↔ NP, ω = 3 (three-factor) ↔ Σ₂^P.
CRT idempotent count 2^ω - 2 counts the number of "alternations" in the algebraic
structure.
STRUCTURAL: formal reduction from polynomial hierarchy oracle access to CRT idempotent
counting is not yet given.

### Claim 12 (Structural — WP16 §1.3)
**Non-associativity evades all three barriers.**
Non-relativizing: exploits internal algebraic structure, not oracle access.
Non-natural: the non-associativity measure requires evaluating triples, which is not
large (holds for ≤50% of functions, not a large fraction of Boolean functions).
Non-algebrizing: uses a specific finite 10×10 table, not an algebraic oracle.
NEEDS FORMAL VERIFICATION: each barrier evasion claim needs to be checked against
the formal definitions in [B-1], [B-2], [B-3].

### Claim 13 (Empirical — WP7 §4.1)
**CK spectrometer declares P vs NP a gap problem.**
Beta = -0.2254 (diverging); CL(D1,D2) = 10/12 HARMONY; D1 trajectory = oscillating
with no settling. Correlation(VOID_fraction, beta) = +0.73 across 6 Clay problems.
The spectrometer's verdict: P vs NP is a gap problem with persistent lens mismatch.
Not a proof of P ≠ NP — a measurement of the problem's algebraic character.

### Claim 14 (Structural — WP34 §9)
**The G-partition geometry, not the modulus b, determines algorithmic difficulty.**
Worlds b = 22, 26, 34, 38 with different q partners give identical G_k = {2,4,6,8}
and identical difficulty 0.3210 to four decimal places at k = 9.
Formal version: algorithmic difficulty is a function of (C, G, ring_class), not of b.
Implication for complexity theory: the "hardness" of a computation is carried by its
algebraic certificate structure, not by the problem instance size alone.

---

*Notes for expansion agent:*
- The WP37 paper must be careful not to overclaim. The PROVED claims (1, 2, 3, 4, 5)
  are genuine results within TIG. The analogy claims (6, 11, 12) are structural
  and must be clearly labeled.
- The three barriers section (§5.4, Claims 8, 12) is the most technically demanding —
  it requires precise engagement with [B-2] Razborov-Rudich definitions.
- The formal bridge (§8.1) is the honest core of the paper: the mapping is compelling
  but the formal encoding of SAT in CL algebra is the missing step.
- Claims 7, 8, 9 are the "NEEDS PROOF" tier — they have proof strategies and are
  stated with enough precision to be worked on formally.
- Luther's dispersion (Claim 10) appears in both WP36 and WP37; it is the bridge
  between the number theory results and the complexity theory interpretation.
- The sinc²/phase-transition connection ([PA-3] Monasson, [SM-2] Mézard-Montanari)
  is the strongest bridge to physics literature and should be developed in §2.4.
