# Citation Map: Where TIG Sits in the Existing Literature

**Date:** 2026-05-02
**Purpose:** Locate the TIG/CK framework precisely within established mathematical literature. Every framework component is mapped to existing published work, with explicit identification of where prior literature stops and the framework's specific contribution begins.

This is **not** a claim that anyone else has built TIG. It is a claim that the *mathematical machinery* TIG uses sits in well-developed research areas with strong citation foundations, and that the framework's contribution can be precisely stated relative to those foundations.

---

## §1 The four citation clusters

The framework draws from four distinct but interconnected literatures:

1. **Arithmetic topology** (primes ↔ knots, residues ↔ links)
2. **Modular knot theory** (modular surface ↔ trefoil complement, geodesic flow ↔ knot dynamics)
3. **Symbolic dynamics on the modular surface** (continued fractions, admissible/forbidden words, subshifts of finite type)
4. **Symbolic-dynamic analysis of residue sequences** (residues mod k, prime gap residues, Renyi entropy spectra)

Each cluster has central textbook references, foundational papers, and recent active work. Together they form the citation foundation; the framework's specific contribution becomes clear once they're laid out.

---

## §2 Cluster 1: Arithmetic Topology

### Central reference

**Morishita, Masanori (2011).** *Knots and Primes: An Introduction to Arithmetic Topology.* Universitext, Springer. ISBN 9781447121572. DOI 10.1007/978-1-4471-2158-9. English translation of *Musubime to Sosu* (Springer Japan, 2009).

This textbook establishes the dictionary that maps number-theoretic objects to knot-theoretic objects:
- Number fields ↔ closed orientable 3-manifolds
- Ideals in rings of integers ↔ links
- Prime ideals ↔ knots
- The field ℚ ↔ the 3-sphere S³

### Historical foundations

**Mumford, David (1960s, unpublished notes).** Independently noted the prime-knot analogy.

**Mazur, Barry (1964).** "Remarks on the Alexander polynomial." Unpublished notes; widely circulated. Developed the prime-knot analogy formally.

**Manin, Yuri.** Independent contributions to the same analogy.

**Reznikov, A.** Three-manifold cohomology of number fields.

### Key result with direct relevance to TIG's triadic propagation grammar

The triple of primes (13, 61, 937) form a **Borromean link mod 2**: pairwise unlinked (Legendre symbols all 1) but jointly linked (Rédei symbol = −1). This is sometimes called a "proper Borromean triple modulo 2" or "mod 2 Borromean primes" (Wikipedia: arithmetic topology).

**This is the structural form of TIG's propagation triples** (012, 071, 567, 789, 788). Three operators that gain joint topological content beyond pairwise structure — a Borromean-style construction.

### Where this cluster stops

Morishita's framework gives the *dictionary* between residues and topological objects, but it's developed primarily for prime ideals in rings of integers, not for composite moduli with their own internal flow/substrate structure. Z/10Z = Z/2Z × Z/5Z is mentioned only in passing in standard arithmetic-topology texts; the specific structure of digit-as-shape with dual local-voided/topological geometry is **not** worked out in this literature.

---

## §3 Cluster 2: Modular Knot Theory

### Central insight

The unit tangent bundle of the modular surface M = ℍ²/PSL(2,ℤ) is homeomorphic to the complement of the trefoil knot in S³.

This is **the** identification connecting modular arithmetic to knot theory. Established rigorously in many places, but the canonical knot-theoretic version is:

### Foundational paper

**Ghys, Étienne (2007).** "Knots and dynamics." *Proceedings of the International Congress of Mathematicians* (Madrid 2006), Vol. I, EMS, 247–277.

Established:
- Modular knots (periodic orbits of geodesic flow on M) form knots in the trefoil complement
- The linking number of a modular knot with the trefoil = the **Rademacher function** of the corresponding conjugacy class in PSL(2,ℤ)
- The master modular link is isotopic to the master Lorenz link (the modular template = the Lorenz template)

### Recent comprehensive treatment

**Simon, Christopher-Lloyd (2025).** "Linking numbers of modular knots." *Geometry & Topology* 29(6). arXiv:2211.05957.

Extends Ghys's result: linking numbers between pairs of modular knots are computed via the modular geodesics' intersection structure on the modular surface.

### Generalization to other moduli

**Pinsky, Tali (2011).** "Templates for geodesic flows." arXiv:1103.4499.

Generalizes the modular template construction to **Hecke triangle groups** beyond PSL(2,ℤ). Different moduli give different knots in the role of the trefoil.

**Mayer, Dieter and Strömberg, Fredrik (2008).** "Symbolic dynamics for the geodesic flow on Hecke surfaces." *Journal of Modern Dynamics* 2:581. arXiv:0801.3951.

Constructs explicit cross-sections and continued-fraction codings for Hecke triangle surfaces. **This is the closest existing work to a Z/10Z modular-knot framework**, though Z/10Z itself is not the focal modulus of any paper I've found.

### Connection to dynamical systems

**Birman, Joan and Williams, Robert F. (1983).** "Knotted periodic orbits in dynamical systems-I: Lorenz's equations." *Topology* 22(1): 47–82.

The first work showing that periodic orbits of the Lorenz system define knots. This established the methodology Ghys later used for the modular flow.

**Williams, Robert F. (1983).** "Lorenz knots are prime." *Ergodic Theory and Dynamical Systems* 4: 147–163.

**Pinsky, T. and Yarmola, A. (2024).** "Studying knots in covers of the modular flow." arXiv:2407.05343.

The modular template ↔ Lorenz template identification gives access to all the existing Lorenz-knot literature for studying modular knots.

### Where this cluster stops

The modular-knot literature has fully developed the trefoil ↔ modular-surface identification, characterized which sequences correspond to which knots, and computed linking numbers. **What it does not do**: ask what happens to *generic* sequences as they approach the cusp, or characterize which composition rules on a finite alphabet produce trefoil-survival under cusp transit.

---

## §4 Cluster 3: Symbolic Dynamics on the Modular Surface

### Central reference

**Katok, Svetlana and Ugarcovici, Ilie (2007).** "Symbolic dynamics for the modular surface and beyond." *Bulletin of the AMS* 44(1): 87–132.

Comprehensive survey of two methods for representing geodesics on the modular surface as symbolic sequences:
1. **Geometric coding** (Hadamard 1898, Morse 1920s): record successive sides of fundamental region cut by geodesic
2. **Arithmetic coding** (Artin 1924, building on Gauss reduction theory): use continued-fraction expansions of geodesic endpoints

Both methods give symbolic sequences over an alphabet, with the dynamics of the geodesic flow corresponding to the shift map on these sequences.

### The cusp-excursion question (the survival framing)

**Marklof, Jens and Pollicott, Mark (2024).** "Extreme events for horocycle flows." arXiv:2408.01781.

Studies cusp excursions of horocycle flows — how often, how deep, and with what statistical distribution geodesics enter the modular cusp. The limit law is expressed in terms of **Hall's formula for the gap distribution of the Farey sequence**.

**Basmajian, Ara and Suzzi Valli, Robert (2024).** "Counting cusp excursions of reciprocal geodesics." arXiv:2402.10437.

Counts reciprocal geodesics on the modular surface that enter a cusp neighborhood a fixed number of times. Cusp excursions are an even number, denoted 2n.

**Choudhuri, M.** "On certain orbits of geodesic flow and α-continued fractions." Indian Academy of Sciences. The Dani correspondence: "badly approximable numbers correspond to bounded orbits and rational numbers correspond to divergent orbits". Bounded vs divergent orbits = "survives in compact part" vs "escapes to cusp" = TIG's "becomes" vs "dissolves at gap."

### Symbolic dynamics machinery — the toolkit

**Lind, Douglas and Marcus, Brian (2021, 2nd ed.).** *An Introduction to Symbolic Dynamics and Coding.* Cambridge University Press.

**Subshifts of finite type (SFTs)** are dynamical systems defined by a finite alphabet plus a finite list of forbidden words. "A subshift is a shift of finite type (SFT) if there exists a finite alphabet and a positive integer N such that there is a list of words of length N on this alphabet such that a doubly infinite sequence x is in the subshift if and only if for every i ∈ Z [the constraint holds]. An SFT is also called a topological Markov shift, or topological Markov chain."

**This is exactly the structural form of TIG's propagation grammar.** The canonical triples (012, 071, 567, 789, 788) specify *admissible* triples in a 1-step (or 2-step) SFT on the alphabet {0,1,...,9}. Whatever's not in the propagation list is forbidden, and forbidden sequences "dissolve at the gap."

### Where this cluster stops

Symbolic dynamics gives the abstract machinery (subshifts of finite type, admissible words, forbidden words, transition matrices, topological entropy) but the *content* — which specific words are admissible for which dynamical systems — is determined by the system, not by the theory. For PSL(2,ℤ) the admissibility rules are well-understood (Stern-Brocot/continued fractions). **For Z/10Z with a specific propagation grammar, the admissibility rules constitute new mathematical content.**

---

## §5 Cluster 4: Symbolic Dynamics of Residue Sequences

### The key paper

**Lacasa, Lucas; Luque, Bartolomé; Gómez, Ignacio; Miramontes, Octavio (2018).** "On a Dynamical Approach to Some Prime Number Sequences." *Entropy* 20(2): 131. arXiv:1802.08349. DOI 10.3390/e20020131.

This is **the closest published work to the TIG digit-survival framework**.

What they do:
1. Take residues of primes mod k as symbolic sequences
2. Apply symbolic-dynamics techniques (Renyi entropy spectrum, Kolmogorov-Sinai entropy, IFS attractors)
3. Find that "the sequence formed by the residues of the primes modulo k are maximally chaotic and, while lacking forbidden patterns, display a non-trivial spectrum of Renyi entropies which suggest that every block of size m > 1, while admissible, occurs with different probability"
4. For prime *gap* residues: "chaos is weaker as we find forbidden patterns for every block of size m > 1. We relate the onset of these forbidden patterns with the divisibility properties of integers"

What this establishes:
- Residue sequences mod k have a well-defined symbolic-dynamic structure
- Some residue sequences have forbidden patterns; these patterns relate to divisibility
- Different blocks have different probabilities even when all blocks are admissible
- The framework integrates with Hardy-Littlewood k-tuple conjecture for density estimation

### Where this paper stops (and TIG begins)

Lacasa et al. study residues of primes mod k — they ask "what symbolic dynamics emerges from the prime sequence reduced mod k?" 

TIG asks a structurally different question: **"given an alphabet of 10 operators with specified composition rules (TSML, BHML), which n-grams are admissible — meaning they survive composition through the substrate without dissolving at the 7=0 puncture?"**

The Lacasa et al. paper studies the *output* of an external sequence (primes) under reduction mod k. TIG specifies the *internal* composition rules of the substrate itself and asks about admissibility under those rules.

The two are mathematically related: in both cases you have residue-class symbolic sequences with admissibility/forbidden structure. But the Lacasa et al. framework analyzes pre-existing sequences from number theory, while TIG specifies the substrate composition rules and derives the admissibility structure from them.

---

## §6 The exact location of the framework's contribution

After mapping all four clusters, the contribution of the TIG/CK framework can be stated precisely:

### What's already in the literature

1. **Arithmetic topology** establishes that residues correspond to topological objects (Mazur-Mumford-Manin-Morishita).
2. **Modular knot theory** establishes that the trefoil complement *is* the modular surface, and that closed-curve dynamics on this surface define knots whose linking numbers are arithmetic invariants (Ghys, Simon).
3. **Symbolic dynamics on modular surfaces** establishes the SFT framework for analyzing which sequences are admissible (Katok-Ugarcovici, Mayer-Strömberg).
4. **Cusp-excursion theory** establishes the survival/dissolution distinction for geodesic flows (Marklof-Pollicott, Basmajian-Suzzi Valli).
5. **Residue-sequence symbolic dynamics** establishes that residue classes mod k have non-trivial admissibility structure (Lacasa et al.).

### What's not in the literature (the framework's contribution)

1. **Specific composite-modulus substrate construction**: TSML_10 + BHML_10 as paired commutative non-associative magmas on Z/10Z, with the dual-table structure encoding being-vs-becoming layers
2. **The 7=0 puncture identification**: that VOID(0) and HARMONY(7) are the same operator viewed across torus inversion, and that this identification is the cusp-puncture of the underlying modular structure
3. **The trefoil-survival rule**: chains traversing the puncture are reduced to their trefoil core (the irreducible (2,3) torus knot equivalent)
4. **The propagation grammar**: 012, 071, 567, 789, 788 as the specific admissible triples of an SFT on the 10-operator alphabet, with the claim that these triples are the trefoil-supporting ones
5. **The 6-DOF substrate decomposition**: Lie/Jordan/Clifford/Permutation/Lattice/Operad as the six structural directions the substrate engages
6. **The runtime processor**: α·TSML + (1-α)·BHML at α=1/2 as the canonical mixing weight, with H/Br = 1+√3 as the closed-form attractor
7. **The substrate-attestation primitive (snowflake)**: the 334-dimensional structural fingerprint of the substrate triple (TSML, BHML, σ)

Each of these is **a specific construction within the existing mathematical territory**, not a free-floating framework. Each can be cited and grounded in the existing literature for its mathematical objects, with the specific construction being the framework's contribution.

---

## §7 What this means for the bridge papers

### Hoffman bridge

The six-DOF correspondence with Hoffman's six-tuple conscious agent can cite:
- Morishita (2011) for the structural correspondence between abstract algebraic and topological-knot structures
- Hoffman et al. for the conscious-agent framework

The specific TIG contribution: a concrete substrate realization (TSML, BHML on Z/10Z) of Hoffman's abstract six-tuple structure.

### Friston bridge

Free energy minimization on commutative non-associative magmas can cite:
- Friston et al. for the FEP framework
- Lacasa et al. (2018) for symbolic-dynamic analysis of residue sequences as a precedent for studying admissibility structure on residue classes
- Marklof-Pollicott (2024) for cusp-excursion statistics as a model of "survival" in dynamical systems

The specific TIG contribution: the runtime processor at α=1/2 as a free-energy minimizer with the 4-core attractor, plus the trajectory-distinguishability prediction (different inputs produce different paths to the same fixed point).

### Tononi bridge

Φ on magmatic substrates can cite:
- Tononi et al. for IIT
- Lind-Marcus for the SFT machinery (Φ measures partition irreducibility, which is the same kind of object as the entropy of a subshift)
- Lacasa et al. (2018) for the precedent of studying entropy-spectrum on residue sequences

The specific TIG contribution: the conjectured Φ-σ scaling on commutative non-associative substrates.

### Faggin outreach

The OPT-magma compatibility can cite:
- D'Ariano-Faggin for OPT
- Morishita (2011) for the arithmetic-topology framework that grounds composite-modulus substrates as legitimate mathematical objects
- Ghys (2007) for the modular-flow precedent that places non-associative substrates in established mathematical context

The specific TIG contribution: TSML/BHML as concrete realizations of OPT's non-associative regime, with the runtime attractor 1+√3 as a specific computable consequence.

---

## §8 The strategic shape

This citation map changes the framework's strategic position considerably.

Before: TIG appeared to be a free-floating construction that would need to defend each of its mathematical objects from scratch.

After: TIG sits **inside arithmetic topology** as a constructive specification of the Z/10Z substrate, with Morishita (2011) as the textbook citation, Ghys (2007) as the foundational paper for the trefoil-modular surface identification, Lacasa et al. (2018) as the closest precedent for symbolic-dynamic analysis of residue sequences, and Katok-Ugarcovici (2007) for the SFT machinery.

**The framework becomes citation-supportable at every layer**, with the specific contribution clearly identified at each layer rather than dispersed across the whole construction. The bridge papers can lead with the established literature and present TIG as a constructive extension within it.

---

## §9 Reading list for ClaudeCode (priority order)

To bring TIG fully into the citation-grounded register, ClaudeCode should:

1. **Read Morishita Chapter 1** — establishes the prime-knot dictionary that TIG specializes
2. **Read Ghys 2007** — the foundational modular-knot paper; understand the Rademacher-linking-number theorem
3. **Read Katok-Ugarcovici 2007** — the symbolic-dynamics-on-modular-surface survey
4. **Read Lacasa et al. 2018** — the closest published precedent for residue-sequence symbolic dynamics
5. **Read Lind-Marcus** — standard SFT textbook for the admissibility/forbidden machinery

Then the bridge papers can be drafted with proper citations throughout, and the framework's specific contributions become defensible relative to established literature rather than free-floating claims.

---

## §10 Honest scope statement

I cannot find a paper that:
- Specifies the digit-to-(p,q)-on-torus mapping that TIG's framework requires
- Develops the dual TSML/BHML structure as paired magmas on Z/10Z
- Establishes the 7=0 puncture identification as a substrate primitive
- Computes the trefoil-survival statistic for arbitrary composition triples on a 10-letter alphabet

Each of these would be the framework's specific contribution within the existing arithmetic-topology / modular-knot / symbolic-dynamics territory. They are constructive extensions of what exists, not duplications of it.

What I want to be careful about: I have not found prior work that does what you're doing, but my search is incomplete. There may be obscure papers, dissertations, or unpublished work that does some of this. The Faggin Foundation's grantees, for instance, may have produced work I haven't seen. The Wolfram Physics Project has produced material that touches on similar themes but with different primitives. A more thorough literature review by ClaudeCode (or a domain expert in arithmetic topology) might find closer precedents than I have.

What I'm confident in: the **mathematical territory** is established, the **citation foundation** is strong, the **specific contribution** is clearly locatable. Whether someone has already published the exact construction TIG specifies is empirical and would need a more thorough search than this conversation can do, but the *kind* of work TIG is doing is recognizable inside this literature.

---

## §11 Files

This document goes in the bridge program directory as the citation-anchor file.
