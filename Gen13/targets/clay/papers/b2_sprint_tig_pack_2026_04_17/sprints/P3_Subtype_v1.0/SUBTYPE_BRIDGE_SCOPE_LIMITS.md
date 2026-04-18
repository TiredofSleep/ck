# What the Subtype Bridge Can Prove, and What It Still Cannot Prove
## Short Note

---

## What a PASS Would Prove

A PASS on the subtype bridge would support one specific sentence:

> On the same Path 2 carrier family where P3-BridgeA-Prime established topology-family resemblance, the MAX/ADD partition of planted-recovery seams also transports: per-carrier subtype count vectors cluster near Z/10's 75%/25% MAX/ADD proportion, edge subtype placement in the seam graph follows Z/10's pattern by graph role, and these patterns are significantly different from a null that scrambles subtype labels on the same graphs.

Three things that claim explicitly includes:

1. **The MAX/ADD vocabulary transports as labels.** The rule-type distinction that the theorem uses to classify its seam cells — MAX rules on six cells, ADD rules on two — is not an arbitrary bookkeeping choice. It identifies a real partition that reappears on other carriers under the same extension algorithm.

2. **The proportion is preserved, not just the partition.** Path 2 artifacts don't just have some MAX edges and some ADD edges; they have them in roughly the same ratio as Z/10. Variation within a tolerance band is expected; but the family distribution is centered near Z/10's 75/25.

3. **Placement is not random.** MAX edges and ADD edges are not uniformly distributed throughout the seam graph. On Z/10, ADD edges connect the identity vertex (1) to the adjacent vertex (2); MAX edges link the chain structure. On Path 2, under a transport of this placement logic, ADD edges should appear in predictable roles relative to the chain and the attractor-involution pair.

Those three claims together constitute a finer bridge than P3AP's coarse topology PASS, and they would earn the sentence above.

---

## What a PASS Would NOT Prove

Even a strong subtype PASS leaves several things unestablished:

**It does not prove rule-type identity.** A MAX-like edge on Z/14 has value $\max(c_i, c_{i+1})$ for the $i$-th chain pair — a specific numerical value. A MAX-like edge on Z/10 has a different numerical value (e.g., $\max(2, 4) = 4$). Both are "MAX-type" in the sense that the modal empirical value equals the max-of-coordinates. The rule-type label transports; the specific values do not correspond across carriers. Subtype bridge is about labels, not values.

**It does not prove that MAX and ADD are the only legitimate subtypes.** They are the subtypes the theorem uses. A richer taxonomy (MAX, ADD, ABS-DIFFERENCE, XOR, LATTICE-MEET, etc.) might classify the same data more informatively. Subtype bridge tests whether the theorem's two-class partition transports; it does not test whether two classes are the right resolution.

**It does not promote the overlay-extension algorithm.** The doubling-chain + identity-edge + attractor-involution rule remains a heuristic, frozen as the spec's generator. A subtype PASS would say that under this heuristic, subtypes transport. It would not say the heuristic is canonical. A different overlay rule might produce different subtype patterns.

**It does not extend any Path 1 theorem.** The theorem remains proven only on Z/10, with $h_\text{thm} = 7$. All Path 2 artifacts tested here are planted-recovery artifacts under the extension algorithm, not theorems.

**It does not prove hub-and-spokes transport.** P3AP's diagnostic showed that Path 2 artifacts under this extension have chain topology, not hub-and-spokes. Subtype placement within a chain is different from subtype placement within a hub-and-spokes tree. A subtype PASS could hold even if the two paths have different coarse shapes, because subtype is measured against each path's own topology. The hub-vs-chain question remains open after this sprint regardless of verdict.

**It does not establish any physical, ontological, or real-world claim.** Scope stays within the taxonomic bridge work.

---

## What a FAIL Would Prove

A FAIL, depending on which sub-condition breaks, teaches something specific:

**If subtype count vectors diverge significantly across paths:** the MAX/ADD proportion on Z/10 is not a universal family property. Z/10's 75/25 split is carrier-specific. This closes a bridge claim but leaves topology-family preservation (P3AP) intact.

**If subtype counts match but placement by role differs:** the rule-type labels transport, but the arrangement of rule types within the seam is carrier-specific. This is a more subtle negative result: the vocabulary moves but the grammar does not. It would suggest that subtype-structural bridges require a richer specification than simply "MAX edges go in MAX positions."

**If subtype adjacency patterns fail under null comparison but counts and role placement pass:** edges' relationships to each other (MAX-next-to-ADD vs MAX-next-to-MAX) are random-looking across paths despite the individual counts transporting. Very different from the first two failure modes.

The spec distinguishes these possibilities by having three separable sub-conditions.

---

## What the Limit Cases Look Like

**Bright-line PASS:** every carrier has between 65% and 85% MAX-like edges, ADD edges appear predominantly as leaf-attached edges on the vertex 1 (or its structural analog), MAX-next-to-ADD adjacency exceeds the random-relabeling null by ≥2σ.

**Bright-line FAIL (any of):**
- Some carriers have <50% MAX-like edges or >95% MAX-like edges.
- ADD edges on Path 2 appear predominantly in internal-chain positions rather than in leaf/hub-adjacent positions.
- Subtype adjacency pattern matches random relabeling within 1σ.

**Honest intermediate:** counts transport, placement is weakly preserved. A marginal UNCLEAR with explicit report of what was observed. Useful input to a followup sprint.

---

## Why This Matters for the Program's Overall Claim

The program's deepest implicit claim is that "structure transports" in some meaningful sense — that the theorem's internal grammar (not just its rough shape) has analogs across carriers. P3AP tested the shape level and passed. The subtype bridge tests whether the *grammar's vocabulary* transports under the same conditions. A PASS would be the first evidence that the program's implicit grammatical claims are operationalizable. A FAIL would be strong evidence that the program's vocabulary is Z/10-specific and that genuine transport operates at a coarser level only.

Either outcome is informative. The subtype sprint is exactly the kind of narrow question whose answer materially changes how the program thinks about the cross-carrier question.

---

## Scope Discipline Reminder

The subtype bridge stays within the P3AP object class. It adds metrics, not generators. It tests a specific finer question raised by P3AP's diagnostic. It does not attempt to resolve the hub-vs-chain question, which requires a different overlay rule and would be a separate sprint.

Staying narrow is the point. Large claims are earned by accumulating narrow results, not by asking broad questions and hoping data supports broad conclusions. The program has proved this discipline works: seven sprints, two PASSes, each with clean attribution. Subtype is the next narrow question whose answer will tell us something specific.
