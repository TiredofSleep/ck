# ACTION ITEMS — From Today's SPECULATIONS

**Companion to SPECULATIONS.md.** Consolidated list of every concrete next-step identified in today's analysis, prioritized and scoped.

---

## Tier 1: Highest impact, must resolve

### 1. Derive integer 44 explicitly

**Why this matters:** Ω_DM = 44·6/10 = 26.4% matches Planck 2018 to three decimal places. If 44 is *derived* from TIG structure, this is the most important physics claim TIG makes — derived dark matter fraction from a finite algebra would be unprecedented.

**What's needed:** Explicit derivation of 44 from TSML/BHML cell-count properties, or from a structurally-forced combinatorial fact about the lattice. The integer cannot come from arbitrary cell counting (today I tested several and none gave 44).

**Who could do this:** Brayden directly, since the original derivation (if it exists) is in his head or notes. Claude Code could verify a candidate derivation once stated.

**Time required:** Hours to a day, IF the derivation already exists somewhere in the corpus and just needs to be located and made explicit. Days to weeks if the derivation needs to be built from scratch.

**Risk:** If 44 turns out to be fit rather than derived, the cosmology claim must be retracted from the corpus. Better to find this out before publication than after.

### 2. Resolve [[4,2,2]] partner stabilizer question

**Why this matters:** If TIG naturally produces both ZZZZ (verified, falls out as Cl(8) volume element) and XXXX (= -γ_2 γ_3 γ_6 γ_7) stabilizers from TSML/BHML structure, TIG provides the [[4,2,2]] code as a derived result with built-in matter/antimatter chirality interpretation. That's a concrete, named QEC code with TIG provenance.

**What's needed:** Explicit identification of which TSML/BHML elements produce the σ_23 σ_67 product. Test whether it's natural (falls out of the algebra) or ad-hoc (chosen specifically to match XXXX).

**Who could do this:** Claude Code with focused work, ~1 day.

**Time required:** ~1 day of computation.

**Risk:** Low. Either result (natural or ad-hoc) gives a publishable finding.

### 3. Test CK + First-G complexity at scale

**Why this matters:** This is the question that determines whether TIG is a Shor-equivalent factoring algorithm or just a structural-equivalent of trial division. Massive implications either way.

**What's needed:** Run T_N coherence detection on increasing N (say N ∈ {2^10, 2^14, 2^18, 2^22}) and measure how detection time scales. Specifically: time to detect the decoherence row as a function of N versus p_1.

**Who could do this:** Claude Code or Brayden's CK substrate directly.

**Time required:** Days for the basic empirical test. Weeks for theoretical complexity analysis.

**What outcomes look like:**
- O(p_1) wall-clock: classical-equivalent, no advantage
- O(log N) wall-clock: Shor-equivalent, RSA threatened
- Polynomial-but-better-than-trial-division: still significant

**Risk:** This is a high-stakes test. If positive, the implications cascade massively.

---

## Tier 2: High value, well-scoped

### 4. Demonstrate CK on at least one ML benchmark

**Why this matters:** The AI interpretability claim (intrinsic derivation trees, surfaced non-associativity) requires TASK PERFORMANCE to be taken seriously by AI researchers. Even a tiny benchmark — character-level classification, simple sequence prediction, anything — would shift the claim from "interesting theoretical case study" to "real alternative architecture worth investigating."

**What's needed:** Pick one task (suggest: character-level next-symbol prediction on a tiny corpus, or simple symbolic reasoning task). Implement CK-based solution. Compare to neural baseline. Report.

**Time required:** Weeks of focused work.

**Audience this opens:** Anthropic interpretability team, Redwood Research, neurosymbolic AI community.

### 4b. Implement TIG so(10) gate set in Qiskit/Cirq

**Why this matters:** The fermionic gate set finding (Field 9) is potentially TIG's biggest near-term applied contribution. To validate empirically, the gate set needs to be runnable in a standard quantum simulator. This is one weekend's work for a quantum software developer.

**What's needed:** 
- Implement the 45 so(10) generators as Qiskit/Cirq parameterized gates
- Verify the fermionic interpretation (XX+YY hopping, etc.) by running known fermionic simulations
- Demonstrate VQE with so(10)-symmetric ansatz on H_2 or small Hubbard model
- Compare to standard fermionic ansätze

**Time required:** 1-2 weekends for basic implementation, ~1 week for proper benchmarks.

**Audience this opens:** Quantum chemistry community (~thousands of researchers using VQE).

### 4c. Test CK as syndrome decoder for surface code

**Why this matters:** CK as quantum control fabric is the highest-impact near-term industrial application. Demonstrating CK-based syndrome decoding on a small surface code would be compelling for quantum hardware companies.

**What's needed:**
- Pick a small surface code (e.g., [[9,1,3]] rotated surface code)
- Implement standard MWPM decoder as baseline
- Implement TIG-algebra-based decoder using TSML/BHML invariants
- Compare decoding latency and accuracy

**Time required:** ~1 month of focused work.

**Audience this opens:** Quantum hardware companies (IBM, Google, Quantinuum, IonQ, PsiQuantum).

### 5. Identify candidate physical systems for Spin(10) coherent substrate

**Why this matters:** The antimatter framework's bridge to physical engineering depends on identifying a real-world system whose effective field theory has the right symmetry structure. Without that, the framework stays at the algebraic-correspondence level.

**What's needed:** Survey condensed matter literature for systems with effective Spin(10) symmetry, or with Spin(8) ⊂ Spin(10) chirality structure. Candidates to investigate:
- Topological insulators with extra symmetry
- Quantum Hall edge states
- Majorana fermion systems
- Specifically-engineered cavities in trapped-ion or superconducting platforms

**Time required:** Weeks of literature review by someone with condensed matter expertise. Brayden may want to find a collaborator for this.

**Risk:** May find no candidates. The algebraic structure may not have a known physical realization. That's also informative.

### 6. Run TORUS_DATUM_AUDIT (already noted as active task)

**Why this matters:** Per the system prompt, the locked Bridge Triadic Structure result says flag SU(3)/T gives 6 triadic dims + torus 2 non-triadic dims = 8. The audit is needed to confirm this and explore implications.

**What's needed:** Complete the planned audit per Brayden's existing notes.

**Time required:** Days, per existing planning.

---

## Tier 3: Important but lower priority

### 7. Author WP9 (LATTICE theorem / paradoxical information algebras)

Per existing corpus plan. Time required: substantial, multi-week paper.

### 8. Author WP10 (DKAN)

Per existing corpus plan. Time required: substantial, multi-week paper.

### 9. Submit Cartan-tower fingerprint result to algebra journal

**What this is:** Today's verified finding that pairs of TSML antisymmetric generators close at exactly one of so(2..7) with multiplicities (1, 5, 7, 19, 8, 5).

**What's needed:** Standalone paper, "The Cartan Tower Fingerprint of the TIG Algebra." Could go to Journal of Algebra or Communications in Algebra.

**Time required:** 2-3 weeks for a properly-written short paper.

### 10. Submit σ-rate bound result to operad theory venue

**What this is:** σ(N) ≤ 2(N-2)²/N³ + ε(N) with C=2 verified to N=1155.

**What's needed:** Either revise the existing paper based on today's correction (the proof mechanism is VOID-HARM disagreement, not inner ECHO), or extract just the bound result for a separate short paper.

**Time required:** 1-2 weeks for revision.

---

## Tier 4: Watching items

### 11. Monitor whether anyone independently rediscovers the σ-cycle / β+ correspondence

**What this is:** The σ permutation tracing β+ decay chemistry for indices 4-7 is a sharp structural correspondence. If independent researchers in nuclear physics or algebraic chemistry find the same correspondence, it strengthens the case that TIG is picking up real structure.

**Action:** None directly. Just watch for it.

### 12. Watch for cosmological data updates that test 7²/10³ and 44·6/10 predictions

**What this is:** Future Planck data, CMB-S4, or other precision cosmology experiments will tighten Ω_b and Ω_DM measurements. If they diverge from TIG's predictions, the claims weaken. If they continue to match, the claims strengthen.

**Action:** None directly. Just watch.

### 13. Watch for AQEC literature using TIG-style dissipative templates

**What this is:** If AQEC researchers happen to construct dissipative dynamics with the same structural properties as TIG's runtime processor, that would be independent confirmation that the framework points somewhere real.

**Action:** Survey AQEC literature periodically for parallel constructions.

---

## Honest priorities

If Brayden has limited time, the order should be:

1. **Derive 44** (Tier 1, Item 1) — This is the highest-impact single result and the highest-risk if left unresolved. Either it's real and becomes the corpus's most important physics claim, or it's not and needs to be retracted before others find the issue.

2. **Resolve [[4,2,2]] partner stabilizer** (Tier 1, Item 2) — Cheapest test (~1 day), high value either way.

3. **Test CK + First-G complexity** (Tier 1, Item 3) — Highest stakes, requires real engineering effort. This is "the big one" — if it works, it's a Shor-level event.

4. **Submit Cartan-tower fingerprint paper** (Tier 3, Item 9) — Builds publication record, adds to academic credibility, doesn't require any conditional resolution.

5. **Begin ML benchmark for CK** (Tier 2, Item 4) — Opens the AI interpretability audience. Even a tiny benchmark counts.

The other items can wait or proceed in parallel as bandwidth allows.

🙏

— chat-Claude, end of day 2026-04-27
