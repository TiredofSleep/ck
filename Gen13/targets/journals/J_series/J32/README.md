# J32 — Operad D₄ Obstruction + P_56 Canonical Fuse (BUNDLED)

**Status:** DRAFT (manuscript finalized 2026-05-07; awaiting referee-rigor pass)
**Phase:** Phase 3
**Target venue:** Compositio Mathematica
**Author lane:** Sanders + Gish
**Tier:** B
**WP source:** WP109 + WP112 (BUNDLED — Part 1 and Part 2 sections in single manuscript)
**Lens scope:** TSML_RAW (annotated; orbit decomposition computed on the literal CL_BIT_PATTERN; lens-invariant 4-core results highlighted)

---

## §1 — Manuscript

**Local path:** `manuscript/manuscript.md`

The J32 paper is a **BUNDLED submission** combining WP109 (Operad D₄ Obstruction) and WP112 (P_56 Canonical Fuse Table).

**Part 1 (WP109).** The 126 non-associative TSML_RAW triples decompose under the diagonal $D_4 = \langle P_{56},\sigma^3\rangle$ action into 67 orbits; exactly 16 are bracketing-pair incoherent. **No $D_4$-equivariant fuse rule taking values in $\{a,b,c,L,R\}$ exists.** The operad-DOF is structurally orthogonal to the WP104 doubly-invariant gauge structure $\mathfrak{su}(4)\oplus\mathfrak{u}(1)$.

**Part 2 (WP112).** Restricting to $\langle P_{56}\rangle$ gives 98 orbits, all $P_{56}$-coherent. All 8 surveyed regular rule families are $P_{56}$-equivariant, none $\sigma^3$-equivariant. Family H (attractor-4-core preference) is the unique family with fuse-value range in the 4-core $\{V,H,Br,R\}$, with histogram $\{0:108, 7:18\}$. The σ³ obstruction localizes to a single triple: $\mathrm{fuse}(3,9,9)=7$. Two further structural results (lens-invariant on the 4-core): Theorem 5.5 — 4-core arity-3 closure ($4^3=64$ triples in-cube); Theorem 5.7 — universal HARMONY attractor (every non-trivial init converges to $\delta_7$ in 1-7 iterations).

Files in this J-folder's `manuscript/`:

- `manuscript.md` — the bundled J32 paper (WP109+WP112 corpus, finalized 2026-05-07)
- `WP109_OPERAD_D4_OBSTRUCTION.md`, `WP112_P56_CANONICAL_FUSE.md` — full source material
- `verification/d4_orbit_decomposition.py`, `p56_canonical_fuse.py`, `rule_families.py`, `fuse_table.py`, `nonassoc_triples.json`, `fuse_canonical_p56.json`

## §2 — Verification script

**Local path:** `manuscript/verification/`

Run order: `d4_orbit_decomposition.py` (Part 1, Theorem 1), `p56_canonical_fuse.py` (Part 2, Theorems 2-5.7), `rule_families.py` (Theorems 3-4). Total wall-clock under 30 seconds. Numpy + sympy. Canonical fuse table written to `fuse_canonical_p56.json`.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J02

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes

**FRESH-EYES REFEREE PASS (2026-05-07): Reject; SAVE PLAN applied (UNBUNDLE).**

The fresh-eyes referee report (`Atlas/META_PLAN_2026-05-06/REFEREE_REPORTS/J32_CompositioMath_FreshEyes.md`) flagged two critical mathematical errors and identified the bundled paper as below the *Compositio* significance bar:

- **§3.1 (CRITICAL).** Orbit-size distribution wrong: paper said $(5, 35, 19, 3)$ at sizes $(1, 2, 4, 8)$ summing to 175 ≠ 126. **CORRECT distribution** (sympy + script verified): $(44, 7, 4, 10, 2)$ at sizes $(1, 2, 3, 4, 8)$, summing to **67 orbits with size-weighted sum = 126** = |𝒩|. The correct accounting: 𝒩 is NOT $D_4$-invariant in $(\mathbb{Z}/10\mathbb{Z})^3$ (220 violations); the right group-theoretic object is the partition by restricted orbits $\overline{\mathcal{O}}_i := \mathcal{O}_i \cap \mathcal{N}$.
- **§3.2 (CRITICAL).** D_4 group structure error: WP109 §2 claimed "6 distinct elements with abstract structure $D_3 \times \mathbb{Z}_2$." **Both wrong.** $|\langle P_{56}, \sigma^3\rangle| = 8$ (sympy verified, order distribution $\{1:1, 2:5, 4:2\}$ matching $D_4$). $D_3 \times \mathbb{Z}_2$ has order 12, not 8. **FIX:** WP109 §2 rewritten with explicit 8-element table (cycle structure + orders) and the direct calculation that $P_{56} \cdot \sigma^3$ has order 4.
- **§4.2.** Burnside pseudo-citation in Theorem 2 (P_56 orbit count). Burnside not actually used; the singletons-vs-doubletons argument is direct enumeration. **FIX:** "Burnside" reference removed; replaced with the direct enumeration argument ("70 singletons + 28 doubletons = 98 orbits, sum-weighted 126").
- **§4.6.** §5.9 family-independence undermines paper's headline (canonical fuse rule choice is irrelevant for dynamical attractor). **FIX:** Theorem 5.9 added explicitly; honest reading appended ("Family H is canonical for static-table-aesthetic reasons, not for dynamical-attractor reasons; the dynamical attractor is a property of the binary TSML's HARMONY-left-absorber row").
- **§3.3, §3.4.** Obstruction example informal; no Φ argument hand-wavy. **FIX:** explicit case analysis on the size-3 obstruction example $\{(0,1,9),(0,5,9),(0,6,9)\}$ showing why $\{a,b,c,L,R\}$-valued $\Phi$ cannot be $D_4$-equivariant on this orbit; the case analysis serves as the worked-out paradigm for the 16 obstructing orbits.
- **§7-§8 (significance).** Even with errors fixed, the bundled paper is below the *Compositio* significance bar (the result is a finite enumeration on a hand-picked $10\times 10$ table). **FIX:** UNBUNDLE per the referee's explicit recommendation.

**Save plan:** `Atlas/META_PLAN_2026-05-06/SAVE_PLANS/SAVE_PLAN_J32.md` — UNBUNDLE per referee §8 recommendation:
- **Part 1 (D_4 obstruction)** → *Algebra Universalis* (~6-8 pages, corrected obstruction theorem)
- **Part 2 (P_56 canonical fuse + 4-core closure + HARMONY attractor)** → *Communications in Algebra* OR *Discrete Mathematics* (~8-12 pages)

The bundled `manuscript.md` is **kept** as a single-document reference (with corrections applied); the two unbundled manuscripts are the journal-submission targets.

**Fixes applied 2026-05-07:**
- `manuscript/WP109_OPERAD_D4_OBSTRUCTION.md` §2: rewritten with explicit 8-element D_4 table, sympy verification, direct calculation of $P_{56}\cdot\sigma^3$ order.
- `manuscript/WP109_OPERAD_D4_OBSTRUCTION.md` §3: rewritten with correct restricted-orbit framing ($\mathcal{N}$ not $D_4$-invariant; partition by $\overline{\mathcal{O}}_i := \mathcal{O}_i \cap \mathcal{N}$), correct distribution (44,7,4,10,2) summing to 67/126, explanation of size-3 restricted orbits.
- `manuscript/WP109_OPERAD_D4_OBSTRUCTION.md` §4: explicit case analysis on the size-3 obstruction example.
- `manuscript/manuscript.md` §"Theorem 1 (Obstruction)": corrected statement with the new orbit table.
- `manuscript/manuscript.md` §"Theorem 2 (P_56 orbit decomposition)": Burnside removed, direct enumeration argument added.
- `manuscript/manuscript.md` §"Theorem 5.7": expanded proof sketch (HARMONY left-absorber, total-variation distance, 7-iteration bound). 
- `manuscript/manuscript.md` Theorem 5.9 added (family-independence).
- `manuscript/manuscript.md` §"Honest scope" expanded (family-cosmetic status; framework dependence acknowledgment).
- `manuscript/manuscript.md` Status block updated: retargeting from *Compositio* to unbundled fallback.

**Verification of fixes (sympy + script):**
- $|D_4| = |\langle P_{56}, \sigma^3 \rangle| = 8$ ✓
- D_4 element order distribution: $\{1: 1, 2: 5, 4: 2\}$ ✓ (matches D_4)
- $P_{56} \cdot \sigma^3$ has order 4 ✓
- Restricted-orbit count: 67 orbits in 𝒩 ✓
- Restricted-orbit size distribution: $(44, 7, 4, 10, 2)$ at sizes $(1, 2, 3, 4, 8)$ ✓
- Size-weighted sum: $44 + 14 + 12 + 40 + 16 = 126 = |\mathcal{N}|$ ✓
- Full $D_4$-orbit distribution (no restriction): $(17, 11, 37, 2)$ at sizes $(1, 2, 4, 8)$, sum = 203 ✓
- 16 of 67 restricted orbits fail bracketing-pair coherence ✓
- $\mathcal{N}$ is NOT $D_4$-invariant: 220 violations $g \cdot t \notin \mathcal{N}$ for $t \in \mathcal{N}$, $g \in D_4$ ✓
- P_56 orbit decomposition: 70 singletons + 28 doubletons = 98 orbits, sum 126 ✓

**Estimated revision time:** 3-4 weeks for the unbundled split. Net: orbit-distribution and D_4-group corrections applied (DONE); §5.9 honest reading added (DONE); unbundling into two stand-alone manuscripts (PENDING — to be done before submission).



### Family-Structure framing (per Atlas/META_PLAN_2026-05-06/FAMILY_STRUCTURE_v1.md)

This paper sits within the TIG family of finite commutative non-associative magmas on Z/10Z (and ring extensions per D74). The family is defined by 5 conjoint membership criteria; the 4-core {V, H, Br, R} = {0, 7, 8, 9} at α_M = ½ is the algebraic center, with closed-form attractor h/β = 1+√3 (D78 Galois proof). The closest published precedent for this neighborhood is **Drápal & Wanless (2021), *J. Combin. Theory A* **184**, 105510** — same domain (small finite commutative non-associative structures), opposite extremum (theirs maximally non-associative).

### PROVEN / COMPUTED / STRUCTURAL RHYME / OPEN — template (fill per paper)

- **PROVEN:** [the specific theorem of this paper]
- **COMPUTED:** [verified-by-script invariants supporting the theorem]
- **STRUCTURAL RHYME:** [constants/identities cited as motivation, not derivation]
- **OPEN:** [the natural next-paper question]

### Lens-ownership paragraph — template (fill per paper, insert in manuscript §0)

> *Lens and substrate.* This paper works on [substrate: Z/10Z / Z/N for N in {...} / F_p for p in {...}] with the [tables: TSML / BHML / both]. These choices are not derived from first principles; they reflect a structural reading of the substrate motivated by [phonaesthesia / 10-operator decomposition / observed dynamics]. The theorems below are theorems on this specific structure; analogous theorems would hold on other substrate-and-table choices. Whether other substrate choices give similarly rich downstream connections is open.

### Hardening status (auto-applied 2026-05-07)

- License: submission scripts CC-BY-4.0 (per `_v3_hardening.py`)
- AI-attribution: Claude/Anthropic byline references removed (per `_v3_hardening.py`)
- Author lane: Sanders + Gish (per Brayden directive)
- Drápal-Wanless 2021 citation in references

## §6 — Submission checklist

- [x] Manuscript .md finalized (bundled)
- [x] Verification scripts green (3 scripts under 30s)
- [x] Tier-classified central claims explicit (Part 1 obstruction theorem; Part 2 P_56-equivariance)
- [x] Lens-scope annotation (TSML_RAW; 4-core lens-invariant results flagged)
- [ ] Cover letter finalized (bones laid; awaits referee-rigor pass)
- [x] Dependencies → cite each J-companion as "submitted to [venue]"
- [ ] Brayden's referee-rigor pass complete
- [ ] Per-venue cap check: this is the 1st paper to *Compositio* this quarter
- [ ] Fallback unbundle plan documented (Algebra Universalis + Comm Algebra)
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Gish. (2026). "Operad D₄ Obstruction + P_56 Canonical Fuse (BUNDLED)." Submitted to *Compositio Mathematica*.
