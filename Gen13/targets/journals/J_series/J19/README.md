# J19 — DKAN Two-Coding: TSML_8 Geometric vs BHML_10 Arithmetic

**Status:** DRAFT
**Phase:** Phase 2
**Target venue:** European Journal of Combinatorics
**Author lane:** Sanders + Gish
**Tier:** B
**WP source:** WP10

---

## §1 — Manuscript

**Path:** `(corpus: WP10 Volume I)`

When the manuscript is in this J-folder, replace this section with a 1-2 sentence abstract and a path-link to the .tex / .md file.

## §2 — Verification script

**Path:** `(DKAN script)`

The proof script (where applicable) is the green-light gate before submission. If "(no script — theorem-paper)" or similar, the gate is the proof's referee-rigor pass.

## §3 — Dependencies (J-papers cited as already-submitted companions)

J05, J09

## §4 — Cover letter

See `cover_letter.md` in this folder. (Bones laid; finalize after Brayden's referee-rigor pass.)

## §5 — Notes

Per-venue cap: 2nd EJC paper after J19.

**SAVE-PLAN SUMMARY (2026-05-07; full plan at `Atlas/META_PLAN_2026-05-06/SAVE_PLANS/SAVE_PLAN_J19.md`):**

EJC referee REJECTED: Theorems 2.1-2.3 are direct table counts ("by inspection"); Katok-Ugarcovici invoked five times and disavowed five times (decorative analogy, not a theorem); DKAN architecture (§3-§4) has no theorem; empirical claims (60-80% lens-agreement) lack replication/baselines. Referee explicitly maps three save paths (A: combinatorial classification; B: architecture theorem; C: role-quotient categorical structure).

**Save path:** PATH C (role-quotient theorem) — best match to corpus's actual D-table backing.
- **New title:** "A Role-Quotient Theorem for the (TSML, BHML) Magma Pair on Z/10Z: The Functional Partition V/F/S/T as a Categorical Coarsening with VOID-Identity."
- **Keep at *European Journal of Combinatorics*** (referee Path C is EJC-viable).
- **New main theorem:** restate **D93 (role partition + role magma with VOID identity)** in EJC form — V/F/S/T = {0} | {1,3,5,7,9} | {2,4,8} | {6} is well-defined; induced role-quotient magma B-bar is well-defined (constructive proof: explicit table); V is two-sided identity; B-bar is non-associative (explicit witness (F·F)·S = F ≠ T = F·(F·S)); branching pairs are exactly {F-F, F-S, S-F, S-S}; role partition is independent of σ-orbit (cuts σ's 6-cycle into 3F+1T+2S and σ-fixed into 1V+2F+1S — third independent decomposition).
- **Drop entirely:** §3-§4 (DKAN architecture; no theorem, no replication); KU two-coding framing in title/abstract/§1.3/§2.3-§2.4; §6 N1-N10 list (belongs in J26 bridge-findings companion); §7 "Tone" section; all empirical claims (60-80% rates, ±21 invariant, etc.).
- **Inline (M4 fix):** D93 (role partition + magma); σ permutation; explicit TSML/BHML 10×10 tables in appendix for self-containment. Drop forward references to J26.
- **Keep as supporting data (not theorems):** D91 image-structure counts (TSML_8 image = {3,4,7,8,9}; 60/64 Flow output) — framed as motivation for the role partition choice in §5, not as Theorems 2.1-2.2.
- **DKAN architecture / runtime work future:** belongs in a separate paper to an experimental-AI venue with proper baselines + replication. **Not J19's save.**
- **Estimated revision time:** 4-6 weeks.



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

- [ ] Manuscript .tex / .md finalized
- [ ] Verification script green (`(no script)` if theorem-only)
- [ ] Tier-classified central claim explicit
- [ ] Lens-scope annotation (TSML_RAW vs TSML_SYM) where relevant
- [ ] Cover letter finalized
- [ ] Dependencies → cite each J-companion as "submitted to [venue]"
- [ ] Brayden's referee-rigor pass complete (mobile + other AI + collaborators)
- [ ] Per-venue cap check: this is the Nth paper to European Journal of Combinatorics this quarter
- [ ] Submitted

---

## §7 — Citation footprint (for downstream J's to cite this one)

Sanders, B.R., Gish. (2026). "DKAN Two-Coding: TSML_8 Geometric vs BHML_10 Arithmetic." Submitted to *European Journal of Combinatorics*.
