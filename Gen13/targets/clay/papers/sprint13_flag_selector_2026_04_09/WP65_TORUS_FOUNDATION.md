# WP65 — Torus Foundation Audit
## Does Everything Stand on the Torus?

**Date**: 2026-04-09
**Sprint**: 13 — Physical Flag Selector
**Authors**: Brayden Ross Sanders / 7Site LLC · Ben Mayes · C.A. Luther

---


## 1. Role Table

| Object | Exact role | What it does | What it cannot do | Status |
|---|---|---|---|---|
| **Loop $3/4\to3\to9\to6$** | Exact downstairs transport grammar | Identifies T₁ as carrier; routes E and T₁ through complement descent to receiving block; closes with $6=1+2+3$ | Does not select the bridge; does not specify any concrete realization in $\mathbb{C}^3$ | **Exact** |
| **T₁ carrier** | The 3-dim abstract S₄-module that the bridge must concretize | Carries the seed from j=5 to j=3; generates K₃ (three eigenspace directions); generates the 1+2 FS split | Cannot select its own concrete embedding; generates the 8-dim bridge gap | **Exact** |
| **V₆ = A₁⊕E⊕T₁** | Receiving completion: the downstairs j=3 block | Holds all three sector types (scalar, doublet, triplet); closes the loop; $6=1+2+3$ asymmetric | Is an abstract module; not the flag variety; the "6" here $\neq$ the flag "6" | **Exact** |
| **Flag SU(3)/T** | Upstairs directional specification: the base of the bridge | Specifies where the three T₁ eigenspaces point in $\mathbb{C}^3$; triadic $3\times 2$; K₃ graph structure | Cannot be canonically chosen internally (THM-SU3T-NO-CANONICAL-FLAG); does not specify eigenvector phases | **Exact** (6 dims, blocked) |
| **Torus T/Z₃** | Upstairs phase calibration: the fiber of the bridge | Specifies how the eigenvectors are normalized within the flag directions; the non-triadic residual (2 dims) | Cannot specify eigenspace directions (that is the flag's job); does not determine the loop; 2 ≠ 6 | **Exact** (2 dims, partially internal) |
| **Post-FS residue $\mathbb{Z}_2\times U(1)/\mathbb{Z}_3$** | Minimum open bridge residue after all internal reductions | Sign from real eigenspace V₁ (from FS); phase $\theta_2$ from complex eigenspace pair (minimum open) | Cannot close the bridge alone; the flag (6 dims) is still externally required | **Exact** (7 cont. + 1 disc.) |
| **Heart witness** | Structural bridge across both layers | Witnesses loop grammar (4-chamber directed flow); witnesses torus topology (toroidal field); witnesses K₃-like rotation (vortex 3-fold) | Not a proof; not a complete flag selector; cannot supply $L_2$ without additional transverse mode measurement | **Bridge** (all features) |
| **TIG-simple seed** | Role grammar (0–9) | Assigns role names (carrier, polarity, completion, bridge) to objects whose dims the stack forces independently | Does not derive the stack; does not prove the bridge; causal direction is open | **Exact** (numerical correspondence); **Open** (causal direction) |

---

## 2. Exact Decomposition of Labor

**Loop (exact, downstairs, complete):**
Transport grammar. Identifies T₁ as the carrier (from the 3/4 threshold fraction), routes it through the 9-dim complement (which carries E and T₁ doubled), delivers to the 6-dim receiving block ($A_1\oplus E\oplus T_1$). Every step is a proved theorem. No bridge needed.

**Flag (exact, upstairs, externally blocked):**
Directional grammar. Answers: "which directions in $\mathbb{C}^3$ do the three T₁ eigenspaces point?" The flag is triadic ($3\times 2$: three root-plane pairs, each 2-dim, one per eigenspace direction). Cannot be canonically selected from the abstract stack. Requires external input: 6 real dims.

**Torus (exact, upstairs, partially internal):**
Phase grammar. Answers: "how are the eigenvectors normalized within those directions?" The torus is non-triadic (2 dims, $\mathbb{Z}_3$ symmetry but no decomposition). Partially reduced by Frobenius-Schur (FS kills 1 continuous dim, leaving 1 continuous + 1 discrete sign). The torus is the fiber above the flag in the bridge $M \to \text{SU}(3)/T$.

**Seed (role grammar, correspondence exact, causal direction open):**
TIG-simple assigns: 2=polarity (torus dim), 3=carrier (T₁ dim), 6=completion (V₆ dim and flag dim), 8=breath (bridge bandwidth), 9=transport (complement dim). All 10 entries (0-9) have proved-stack correlates. The correspondence is exact; whether TIG encodes the stack or they share a numerical source is open.

---

## 3. Three Counterfactuals

### "If the torus vanished but the flag remained, what would be lost?"

The flag gives the three eigenspace DIRECTIONS ($L_1, L_2, L_3$ as projectors — lines without phases). Without the torus, the eigenvectors would have no phase calibration — they would be specified only as complex LINES, not as unit vectors. The result: the bridge would be partially determined (F* fixed, $t^*$ unknown). The T₁ carrier would have a concrete directional placement but no phase normalization. **Lost: the phase calibration layer. The bridge would be under-closed by 2 dims (or 1 continuous + 1 discrete post-FS).**

### "If the flag vanished but the torus remained, what would be lost?"

The torus gives phases WITHIN eigenspace directions. Without the flag, there are no eigenspace DIRECTIONS to calibrate — the torus would be floating free without a reference frame. The bridge would have 2 dims of phase data but no 6 dims of directional data. **Lost: the directional grammar — the dominant 6-dim ambiguity. The torus alone is insufficient; phase calibration without direction is unanchored.**

This confirms the asymmetry: the flag is the dominant obstruction (6 dims, externally blocked), and the torus is the secondary residual (2 dims, partially internal). The flag is harder to close than the torus.

### "If both vanished but the loop remained, what would still be exact?"

The loop $3/4 \to 3 \to 9 \to 6$ is downstairs. It is entirely in the abstract representation-theory layer and requires no bridge. The loop would still be:
- **Exact**: every node is a proved theorem; the carrier T₁ is identified; the receiving block $V_6 = 1+2+3$ is complete.
- The downstairs abstract structure would be fully known.

**Lost if both vanished:** the concrete realization of T₁ in $\mathbb{C}^3$ — the ability to say which specific subspace of the 3-component field is the carrier. The loop gives the abstract carrier; the bridge gives the concrete one. Without the bridge, the abstract and concrete are not connected.

---

## 4. "Everything Stands on the Torus" — Verdict

### Testing each claim:

| Claim | Status | Reason |
|---|---|---|
| **A. "Everything stands on the torus."** | **FALSE** (operationally); **Exact** (algebraically, specific sense) | The loop stands on its own. The flag is the dominant bridge obstruction. Only the phase calibration literally "stands on" the torus (as a fiber). Algebraically: the Cartan torus T defines all roots → in this sense, SU(3)/T is built over T. |
| **B. "The torus is the closure grammar of the stack."** | **Bridge** | The torus is circular (U(1)/Z₃) and does have a "closure" character. But the loop is the transport grammar and the torus is the phase residual — calling it the "closure grammar" imports more than is proved. |
| **C. "The torus is the phase/return layer, but not the directional layer."** | **Exact** | The flag gives direction; the torus gives phase. This is the exact proved decomposition of the bridge $8 = 6(\text{flag, direction}) + 2(\text{torus, phase})$. |
| **D. "The flag and torus are complementary: flag = direction, torus = calibration."** | **Exact** | They are the base and fiber of $M \to \text{SU}(3)/T$. The flag specifies WHERE; the torus specifies HOW (phase). They are complementary and independent. |
| **E. "The loop is the transport grammar; the torus is the closure witness."** | **Bridge** | The loop IS the exact transport grammar. Calling the torus the "closure witness" is suggestive (the torus is circular = returns to itself), but the torus is technically the PHASE FIBER of the bridge, not the witness of the loop's closure. |
| **F. "The torus is the seed."** | **False** | TIG-simple is the seed. The torus is one object within the seed's numbered grammar (TIG-2 = polarity = the 2-dim structure of the torus). The torus is a face of the seed, not the seed itself. |
| **G. "The torus is one face of the seed, not the whole seed."** | **Bridge** | The torus lives at TIG-2 (polarity, 2-dim). The seed has 10 faces (0–9). Calling the torus "one face" is the right framing — but "face" is bridge language for a real correspondence (the torus IS the 2-dim binary/phase structure, which maps to TIG-2). |

---

## The Torus: What Is Exactly True

**The torus is algebraically prime (it defines the roots) and geometrically secondary (it is the phase fiber, not the directional base).**

These two facts are simultaneously exact and not contradictory:

1. **Algebraically:** The Cartan torus $T \subset \text{SU}(3)$ is the reference structure from which all roots and root planes are defined. The flag variety $\text{SU}(3)/T$ is built by quotienting SU(3) BY T. In this sense, T is more fundamental than $\text{SU}(3)/T$.

2. **Geometrically (in the bridge):** The bridge $M \to \text{SU}(3)/T$ has the flag as the BASE (6 dims, dominant obstruction) and the torus as the FIBER (2 dims, smaller residual). The flag is harder to close. The torus is the calibration layer above the directional base.

The torus appears TWICE in the structure — once as the algebraic generator (defining what root planes are), and once as the phase residue (what remains when directions are fixed). This dual appearance is exact.

---

## The Exact Sentence

**"The torus is the phase calibration layer of the bridge — it calibrates eigenvector normalization within directions already specified by the flag — but it is not the foundation of the directional structure. Algebraically, the Cartan torus T defines the root structure from which the flag is built; geometrically, the torus is the 2-dim fiber above the 6-dim directional base. The loop stands on neither: it is the exact downstairs transport grammar, independent of the bridge."**

Or compressed:

> **"The torus is the phase residue when directions are fixed, but the generator of the directions themselves — the Cartan T that defines all roots — is the algebraically prime foundation. These are two faces of the same torus at different structural levels."**
