# Referee report — J05: *TSML 73 Cells / BHML 28 Cells: Lens-Invariant Cell Counts on the Z/10Z Composition Lattice*

**Target venue:** *Experimental Mathematics*
**Referee role:** Fresh-eyes, standard combinatorics / Latin-square / quasigroup literature only.
**Manuscript file read:** `Gen13/targets/journals/J_series/J05/manuscript/tsml_bhml_cell_counts.tex`
**Verification scripts read:** `proof_d10_tsml_73_cells.py`, `proof_d16_bhml_28_cells.py`, and the bundled `ck_tables.py`.

---

## §1 Manuscript summary (paraphrased fresh)

The authors define two specific 10×10 binary composition tables `T : Ω×Ω → Ω` over `Ω = {0, 1, …, 9}`, called **TSML** and **BHML**. They name a distinguished output value `7` ("HARMONY") and define:

> A *harmony cell* of `T` is a pair `(i, j)` with `T(i,j) = 7`. The *harmony count* `h(T)` is the number of harmony cells.

The paper proves three claims:

- **Theorem 1.** `h(TSML) = 73`. Proof: TSML is defined by three "exception classes" (V0 = void row, V1 = void column, E = five symmetric "echo" pairs); 9 + 8 + 10 = 27 non-harmony cells; 100 − 27 = 73.
- **Theorem 2.** `h(BHML) = 28`. Proof: a four-zone partition counting 2 + 11 + 2 + 13 = 28 harmony cells.
- **Theorem 3 (lens invariance).** If `π ∈ Stab(7) ⊂ S₁₀` (i.e., a permutation of `Ω` fixing 7), and `π` acts on tables by `(π · T)(i, j) = π(T(π⁻¹(i), π⁻¹(j)))`, then `h(π · TSML) = 73` and `h(π · BHML) = 28`.

A "complementarity" proposition (§5) records that the harmony cells of TSML and BHML on the unit subgroup `{1, 3, 7, 9}` intersect only at `(7, 7)`. A §6 narrative reviews "significance," and §7 documents the two verification scripts (each runs in <0.1 s).

---

## §2 Decision recommendation

**Major revision.**

Theorems 1 and 2 are correct (verified by inspection plus running both scripts mentally on the bundled `ck_tables.py`); they are *very* easy. Theorem 3 is correct but is a standard observation, not a result — its proof is one line and could be stated in any introductory text on group actions on functions.

The paper's real content is the *introduction of the two tables TSML and BHML* — but the manuscript does not justify why these particular tables merit attention. As written, the paper is a counting exercise on two tables whose definitions appear from nowhere. To clear the *Experimental Mathematics* bar, the authors must either (a) establish that TSML/BHML have an independently meaningful structural pedigree (not citing internal companion papers under review at other venues) or (b) demonstrate experimental phenomena that are not just two integer counts.

---

## §3 Top 3 critical issues

### Issue 1. Theorem 3 is a triviality, dressed.

The "lens invariance" theorem says: if `π` is any bijection of `Ω` fixing `7`, then for any `10×10` table `T`, the count of cells of `π · T` outputting `7` equals the count of cells of `T` outputting `7`. This is immediate from the proof, which is two lines:

> `(π · T)(i, j) = 7 ⟺ T(π⁻¹i, π⁻¹j) = 7`, and `(i, j) ↦ (π⁻¹i, π⁻¹j)` is a bijection of `Ω × Ω`.

This is the **definition of the action** combined with the fact that bijections preserve cardinality. It is not a theorem in the *Experimental Mathematics* sense; it is the consistency check that the count is well-defined under the named action.

The paper signals self-awareness in Remark on Scope (§4): "It does not extend to bijections that move 7 — for the obvious reason: if `π(7) ≠ 7`, the harmony output value of `π · T` is no longer 7." Quite. The standard formulation in the orbit-counting / Burnside-style literature on Latin squares (McKay–Wanless 2005, Drápal–Wanless 2021) treats relabeling actions on rows / columns / symbols simultaneously, and asks for *autotopism* groups, paratopisms, or similar genuine invariants. The authors are not measuring those.

The "lens invariance vs. lens dependence" contrast with the "joint sub-magma chain count of [J02]" (Remark in §4) is similarly hollow as stated: the chain count must depend on the operations themselves, not just on the value 7. The contrast is not a mathematical phenomenon but a tautology about which structures the action preserves.

### Issue 2. The introduction of TSML and BHML is unmotivated and the operator-naming distracts from the math.

The 10 elements of `Ω` are named VOID (0), LATTICE (1), …, RESET (9). The text states (page 3): "These names reflect the dynamical role of the operators in a separate framework, but play no role in the proofs below."

If the names play no role, remove them. They are confusing — "harmony cell" sounds like a structural notion, but it is exactly "cell with output `7`." Just say "cell with output `7`." Why is `7` distinguished? The paper does not say. The companion paper `[Sanders2026]` is referenced as if to motivate this choice, but nothing in the present manuscript answers "why 73, why 28, why the value 7?"

For *Experimental Mathematics*, the reader needs a reason that these two specific tables — among the `10^{100}` possible 10×10 tables — are objects of study. The paper says (§5) that the counts sum to `73 + 28 = 101 = 100 + 1` and have unique overlap on the unit subgroup `{1, 3, 7, 9}` at `(7, 7)`; and that "the two tables together cover distinct structural territory." But "distinct structural territory" is undefined, and `73 + 28 = 101` is not in itself a phenomenon — it is two counts summing to a number near 100.

### Issue 3. The proofs are direct enumeration, but presented as if they were structural arguments.

Theorem 1's proof partitions the 27 non-harmony cells into V0 ∪ V1 ∪ E. That is a fine elementary argument, but it is a presentation of the table itself, not a derivation: TSML *is defined* by the list "(V0): row 0 outputs 0 except column 7; (V1): column 0 outputs 0 except row 7; (E): five symmetric pairs output non-7; default: output 7." Counting non-7 cells is reading off the definition.

Theorem 2 has the same shape: BHML *is defined* via its four zones, and the harmony cells are read off.

The paper presents these as theorems with proofs, but a referee from outside the project will read them as: "Define a table by listing where it equals 7; prove that the table equals 7 in those places." This is a definitional consistency check.

A genuine theorem would be of the form: "Among all `10×10` commutative composition tables satisfying property `P`, the maximum / minimum / median harmony count is `73` (resp. `28`), achieved uniquely by TSML (resp. BHML)" — i.e., the count would be characterized by a structural property, not by listing the table. The paper does not attempt this.

---

## §4 Other major comments

**M1. "BHML is symmetric" is asserted but the table is not symmetric.** Let me check: `BHML[1][7] = 2` and `BHML[7][1] = 2` — OK. `BHML[1][8] = 6` and `BHML[8][1] = 6` — OK. Looking through, the bundled table in `ck_tables.py` *is* symmetric and the proof of Theorem 2 implicitly uses this. But the manuscript's definition of BHML (§3.1) does not state symmetry; it states rules for `(8, j)` only and notes "and the symmetric column conditions." This is sloppy. Either prove BHML is symmetric (a one-line check from the rules) or list the column rules explicitly.

**M2. The "echo pairs" definition (§2.1) is opaque.** "(E): The five symmetric index pairs `(1,2), (2,4), (2,9), (3,9), (4,8)` and their transposes give a distinguished non-harmony output (specifically TSML assigns to each such cell a value in `{1,2,3,4,8,9}`; the precise values are given in [ck_tables], but only the assertion 'output ≠ 7' is used in this paper)." If only "≠ 7" is used, why are the five pairs distinguished? Why not (1, 3) or (5, 9)? The reader cannot evaluate whether the echo pairs are arbitrary or principled. Either give a structural definition (e.g., they are the orbits of some explicit involution) or say openly that the table is hand-constructed.

**M3. The "complementarity" proposition (Proposition 5.1) is restricted to the unit subgroup `{1, 3, 7, 9}` but not stated as a general fact.** What about the harmony intersection on all of `Ω × Ω`? It is observable from `ck_tables.py` that `(0, 7)`, `(7, 0)`, `(4, 8)`, `(8, 4)`, `(7, 7)` are joint harmony cells, plus more in row/col 7 (since BHML row 7 and TSML row 7 both have `T(7, 7) = 7`). Why restrict to the units? Either justify the restriction (the units are the "informative" subset for some reason) or state the general intersection size.

**M4. The cell-count integers `73` and `28` are not connected to anything else in the paper.** A reader expects either a structural reason (e.g., 73 = 100 − 27 is forced by the rule families' counts) or a numerical surprise (73 is close to a fundamental constant like `100 · ln(2)`). Neither is offered. The paper lists the integers without finding their meaning. *Experimental Mathematics* tolerates phenomenological observations but expects the authors to have looked for structure or surprise. This paper does not.

**M5. The bundled `ck_tables.py` has copyright / license language that does not belong in a mathematics submission.**

```
Copyright © 2025–2026 Brayden Ross Sanders / 7SiTe LLC
Licensed under the 7SiTe Public Sovereignty License v1.0.
Human use only. No commercial use. No government use.
No military, intelligence, policing, or surveillance use.
```

`Experimental Mathematics` will require either a standard open license (MIT, BSD, Apache 2.0, or CC-BY for non-software) or an arrangement with Taylor & Francis. "7SiTe Public Sovereignty License v1.0" is a bespoke non-OSI license whose terms (especially "no government use") will not pass the journal's editorial process. This is a publication-process issue independent of the math.

**M6. The bundled `ck_tables.py` contains assertions and constants (`T_STAR = 5/7`, `W = 3/50`, ghost-trace tables `G`, ring-distance `DIS`, `DOING_sum = 201`) that are unused in the manuscript and unreferenced anywhere. They suggest the table is part of a larger proprietary structure. This will alarm referees about scope creep — either prune the script to what the manuscript needs, or explain what these constants are.

---

## §5 Minor comments

- §1 ("Setup"): The phrasing "These names reflect the dynamical role of the operators in a separate framework" is ambivalent — it tells the reader to ignore the names while keeping them. Decide.
- §2 (TSML): The rule (V1) reads "for `i ≠ 0`, `TSML(i, 0) = 0` if `i ≠ 7`, and `TSML(7, 0) = 7`." This is fine, but together with (V0) plus the symmetric echo pairs, the table is symmetric — state this as a one-line observation.
- §3 (BHML): The rule `R_B`: `BHML(i, j) = max(i, j) + 1` for `i, j ∈ {1, …, 6}`. Note that this gives `BHML(6, 6) = 7`. The proof of Theorem 2 enumerates row 6 + column 6 in the core zone, but `(6, 6)` is in both row 6 and column 6 — the paper says "row 6 (j ∈ {1,…,6}) gives 6 cells; column 6 (i ∈ {1,…,5}, since i = 6 is already in row 6) gives 5 cells, total 11." This is correct but the reader has to do the cross-out manually; phrase it as "exactly one of `i, j` equals `6` (10 cells) plus `(6, 6)` (1 cell), total 11."
- §4 (Definition of "lens"): the action is the standard "transport of structure" action of `S_n` on tables `Ω×Ω → Ω`. Cite this — it is in any standard combinatorics textbook (Stanley *Enumerative Combinatorics*, Vol. 1, Ch. 7) or in the autotopism literature for Latin squares.
- §5 ("Complementarity of TSML and BHML"): the unique overlap `(7,7)` on the units is a feature, but feels arbitrary. Either include a table of overlaps or remove.
- §7 ("Verification"): mention `proof_fourier_bridge.py` is included but not used in the proofs of Theorems 1–3, so it should not be referenced as a verification script for this paper.

---

## §6 Literature missed

The authors should engage with the standard literature on classifications of binary operations on small finite sets:

- **McKay & Wanless**, "On the number of Latin squares," *Ann. Combin.* 9 (2005), 335–344. This and the follow-ups give exhaustive enumeration / equivalence-class structure for `n × n` tables on `n` symbols.
- **Drápal & Wanless**, "Concerning the number of Latin squares with `n + 1` rows," 2021, and earlier Drápal papers on quasigroup invariants. The autotopism group of a Latin square is the natural symmetry group; the authors' "lens" group is a small piece of this (the *symbol stabilizer of 7*).
- **Phillips & Vojtěchovský**, "Linear groupoids and the associated wreath products," *J. Symbolic Comput.* 40 (2005), 1106–1125. Provides standard machinery for defining and classifying composition tables by their algebraic invariants.
- **Pflugfelder**, *Quasigroups and Loops: Introduction* (Heldermann, 1990). Covers autotopism / paratopism actions and the standard dictionary on which tables are equivalent.
- **Smith**, "Quasigroup Representation Theory" (CRC, 2007), Ch. 1 — formalism for binary operations as ternary relations and their symmetry groups.

The "harmony cell count" concept does not appear in the literature as far as I can tell, but it is a special case of "cell count by output value," which is studied in the context of *value distribution of composition tables* (e.g., Cayley table column / row character histograms). The lens-invariance statement is a special case of the general fact: "For any group `G ≤ S_n` acting on tables `Ω×Ω → Ω` by transport of structure, and any `G`-invariant predicate `P` on outputs, the predicate-cell count is `G`-invariant." The authors' Stab(7) is the symbol stabilizer, which is the smallest natural group; the autotopism / paratopism groups are larger and give richer invariants.

---

## §7 Estimated revision effort

The mathematical content cannot be saved in its present form. To make a publishable paper at *Experimental Mathematics*, the authors would need to add at least one of:

1. **Why these tables.** A structural / algebraic / categorical reason TSML and BHML are the "right" tables to study. Maybe TSML is the unique 10×10 commutative table with property `X` (smallest harmony density / largest stable set / specified distortion under `Stab(7)`). Maybe BHML is characterized as the unique commutative table satisfying `R_A`, `R_B`, `R_7`, `R_{89}` simultaneously. Without this, the tables are arbitrary.
2. **Why these counts.** Show that 73 and 28 are extremal, surprising, or have a closed-form expression in terms of meaningful invariants. The counts as currently stated are sums of the rule-class sizes, which is a definitional artifact.
3. **A genuine experimental phenomenon.** Run both tables under iteration / random perturbation / extension to `Z/14Z` or `Z/12Z` and report a discovered structure. *Experimental Mathematics* is exactly the venue for "we observed pattern `P` and conjecture `C`."

Effort estimate: 2–3 months for option 1 or 3 if real structure exists; option 2 requires checking extremality which might be a programmable enumeration. Cleaning up the existing manuscript (proofs, license, unused script content): 1 week.

The lens-invariance theorem (Theorem 3) cannot be salvaged as a result; it should be reduced to a one-paragraph remark or removed.

---

## §8 Verdict — meets *Experimental Mathematics* bar?

**Not in current form.** The bar at *Experimental Mathematics* is "verifiable computational discovery of mathematical structure." This paper has the verifiable-computation half — the scripts run and the counts are correct — but is missing the discovery half. Two specific tables are introduced, two integers are read off them, and a third "theorem" is the consistency check that the second integer is well-defined under a natural relabeling. The unifying concept ("harmony cells", "lens invariance") is introduced and applied without there being an external phenomenon to explain.

If the authors can reframe the work to answer "what is special about TSML and BHML among 10×10 tables, and why do the counts 73 and 28 matter beyond restating the rules?", a revised version could clear the bar. As submitted, it does not.

**Recommend major revision** with the requirement that (a) the motivation for the two tables be supplied independently of unreviewed companion submissions, (b) Theorem 3 either be replaced by a substantive invariance result (autotopism / paratopism level) or downgraded to a remark, and (c) the bundled materials (license, unused content in `ck_tables.py`, `proof_fourier_bridge.py`) be cleaned up to standard journal formatting.
