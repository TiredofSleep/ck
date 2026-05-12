# Referee Report — J37 / *Physical Review D*: Fresh-Eyes Audit

**Manuscript reviewed:** `Gen13/targets/journals/J_series/J37/manuscript/manuscript.md`
**Verification script:** `Gen13/targets/journals/J_series/J37/manuscript/verification/wobble_check.py`
**Cover letter:** `Gen13/targets/journals/J_series/J37/cover_letter.md`
**Source corpus:** WP107 (`papers/wp107_wobble_localization/`)
**Target venue:** *Physical Review D* (fallback: *Physics Letters B*)
**Tier:** B (per the J37 README)

**Reviewer disposition (one line):** the integer factorization computation is sound and reproducible at machine precision, but as currently framed the manuscript is **not a Physical Review D paper** — the physics content is a single-sentence remark grafted onto an integer-factorization observation about a 10×10 matrix that the manuscript itself admits is not derived from physics. **Recommendation: REJECT for PRD as currently constituted; resubmit to *Linear Algebra and Its Applications* (or *Linear and Multilinear Algebra*) as a short note.** Detailed rationale below.

---

## §1 — Manuscript Summary

The manuscript states a precise computational fact about a fixed 10×10 integer matrix $T$ called "TSML_RAW," whose entries are taken from a project-internal "literal CL_BIT_PATTERN" (defined externally; the matrix is given by direct enumeration in §1):

**Theorem (wobble localization).** The integer characteristic polynomial $f(\lambda) = \det(\lambda I - T)$ has nine nonzero coefficients, of which exactly two are divisible by the prime 11:

- $c_2 = 33 = 3 \cdot 11$,
- $c_8 = -120{,}736 = -2^5 \cdot 7^3 \cdot 11$.

The discriminant of the eighth-degree quotient $g(\lambda) = f(\lambda)/\lambda^2$ is

$$
\mathrm{disc}(g) = 2^{16} \cdot 7^7 \cdot 659 \cdot 95{,}184{,}709 \cdot 222{,}007{,}939 \cdot 2{,}545{,}644{,}917 \cdot 295{,}153{,}052{,}072{,}903,
$$

with no factor of 11. The exponent 16 on the prime 2 is identified with the dimension of a "doubly-invariant subalgebra" $\mathfrak{su}(4) \oplus \mathfrak{u}(1) \subset \mathfrak{so}(10)$ (under a $D_4 = \langle P_{56}, \sigma^3 \rangle$ action defined in a companion paper). The exponent 7 on the prime 7 is identified with "HARMONY raised to the seventh power" (HARMONY = 7).

The proof is a one-line invocation of `sympy.factorint` on the output of `sympy.Matrix(T).charpoly()`. The verification script `wobble_check.py` (53 lines of executable code; runs in under 5 seconds on a laptop) reproduces all seven numerical claims at machine precision.

---

## §2 — Verification Verdict (the integer math is correct)

**Independent reviewer rerun:** I executed the script in the manuscript's `verification/` subfolder and additionally cross-verified the key claims using a fresh `sympy` session (`sympy.Matrix(...).charpoly(lam).all_coeffs()` plus `factorint`). All seven claims pass:

| Claim | Verified |
|---|---|
| Char poly is integer-coefficient | ✓ |
| `[1, -63, 33, 4204, -3998, -62510, 9716, 54880, -120736, 0, 0]` | ✓ |
| Trace = 63 = 9·7 | ✓ |
| $c_2 = 33 = 3 \cdot 11$ | ✓ |
| $c_8 = -120{,}736 = -2^5 \cdot 7^3 \cdot 11$ | ✓ |
| Only $c_2, c_8$ have factor 11 among the 9 nonzero coefficients | ✓ |
| $\mathrm{disc}(g)$ has $2^{16}, 7^7$, no factor of 11 | ✓ |

**The integer mathematics is correct, fully reproducible, and runs in under 5 seconds.** This is the strongest part of the manuscript. The script is short, deterministic, and uses only standard `numpy + sympy`. A referee can verify the entire computational claim in 30 seconds.

I have **no objection to the integer-factorization theorem itself**. The objection is to the venue and the framing (next two sections).

---

## §3 — The Decisive Issue: Is "Wobble Localization" a Mathematical Claim?

The manuscript's title and central terminology — "wobble localization" — is **not a standard term in linear algebra, number theory, or physics**. It is a project-internal label. The manuscript briefly explains it at line 11 of `wobble_check.py`:

> "11 is TIG's wobble denominator."

and §3.2 of the manuscript:

> "The further claim that this 11 IS the same 11 that surfaces in TIG's canonical wobble structure (via the relation 'three wobbles sum to 7/11' in TIG-internal canonical material) is **interpretive**, not derived. The verified part is the integer factorization itself; the interpretive identification is well-motivated but requires accepting a chain through TIG-internal canonical content not derived from first principles in this paper."

This is the manuscript itself, in its own §3.2 ("Honest scope"), telling the referee that:

1. The naming "wobble" is project-internal.
2. The interpretation as "the same 11" as some canonical structure is acknowledged to be **interpretive, not derived**.
3. The chain of reasoning that makes the prime 11 special (vs. e.g., the prime 659 or 222007939, both of which also appear in the discriminant) is via "TIG-internal canonical content not derived from first principles in this paper."

**A PRD referee will read this section and conclude: the central physics-flavored claim of the title is not actually established in the paper.** What is established is a computational observation about which primes divide which coefficients of one specific 10×10 integer matrix's characteristic polynomial — a perfectly valid linear-algebra fact, but one whose physical significance the paper itself disclaims.

The same critique applies to the term "HARMONY": the manuscript identifies the prime 7 as "HARMONY" (an internal operator-name) and observes that the trace 63 = 9·7 contains it, that one of the discriminant exponents is 7, and that the matrix has many 7's in it. **None of these is a physics fact**; they are properties of a specific integer matrix whose entries happen to include lots of 7's. Re-running the same analysis on, e.g., the multiplication table of $(\mathbb{Z}/10\mathbb{Z}, \times)$ would yield similar coincidences without any "HARMONY" interpretation, because the matrix entries are small integers.

---

## §4 — The Specific PRD Mismatch

**Physical Review D** publishes "particles, fields, gravitation, and cosmology" — concrete physics results with concrete physical meaning, falsifiable predictions, and at minimum a clear statement of what physical phenomenon is being modelled. The manuscript scores poorly on each of these axes:

### §4.1 — No Standard-Model observable is computed

The manuscript identifies "$2^{16} = \dim(\mathfrak{su}(4) \oplus \mathfrak{u}(1))$" with the dimension of a Pati-Salam-like sub-algebra. **Pati-Salam is a physically meaningful symmetry breaking** ($\mathrm{SO}(10) \supset \mathrm{SU}(4) \times \mathrm{SU}(2)_L \times \mathrm{SU}(2)_R$), but the manuscript does not derive any consequence of this identification: no mass ratio, no coupling, no decay rate, no vacuum-stability bound, no anomaly cancellation. The dimension match is a **numerological coincidence** unless paired with a derivation of a physical consequence. (Many algebraic dimensions equal 16 — for instance, $\dim(\mathrm{Spin}(10) \text{ chiral spinor})$, $\dim(\mathrm{SO}(8))$, $\dim$ of $E_8$ root lattice mod 1, the dimension of various Clifford algebras… The manuscript notes the spinor coincidence in §2.2 but does not exploit it.)

### §4.2 — The integer matrix $T$ is not derived from a physical Lagrangian

§1 displays $T \in M_{10}(\mathbb{Z})$ by direct enumeration of its entries. The manuscript does not derive $T$ from a physical Lagrangian, a representation of a Lie group, or any other physics object. It cites "WP104" as establishing a connection between $T$ and $\mathfrak{so}(10)$, but that connection is also not given here — it is a forward reference. **A PRD referee cannot evaluate the physics of an integer matrix that is presented in the paper as a literal table without derivation from any physical structure.**

### §4.3 — The "lens-scope note" reveals lens dependence

The boxed lens-scope note at the top (lines 17–18 of the manuscript) states:

> "The upper-triangle authoritative symmetrization $T_{\mathrm{SYM}}$ has $c_2 = 17$ (no factor of 11) and **does not exhibit the prime-11 wobble at the coefficient level**."

So the central claim depends on which "lens" (RAW vs SYM) is applied to the same underlying object. **The wobble is a property of the choice of representative, not of the underlying algebraic structure.** A PRD referee will read this as the manuscript admitting that its central observation is artifact-of-presentation: a different presentation of "the same" object gives $c_2 = 17$ (no 11). The claim's robustness is therefore tied to a project-internal convention about which lens is "canonical," and §4 of the manuscript does not justify why TSML_RAW is the physically-meaningful choice.

### §4.4 — "Gauge symmetry IS the wobble-free part"

This is the cover letter's headline structural claim (also §2.4 of the manuscript). It is offered as a reading rather than a theorem: the doubly-invariant subalgebra (Killing form $(-4)^{15} \oplus (0)^1$, all clean integers, no factor of 11) is "where" gauge symmetry lives, and the prime 11 lives in the complement. **This is suggestive language, not a falsifiable physical claim.** The PRD reading is: there exist many subalgebras of $\mathfrak{so}(10)$; the doubly-invariant one happens to have a Killing form whose eigenvalues are −4 and 0, neither of which is a multiple of 11; therefore "11 lives in the complement" is true by elimination. This is a tautological observation, not a physics theorem.

---

## §5 — Where This Paper Should Go

The manuscript would be at home in one of:

1. **Linear Algebra and Its Applications** (LAA): this is the natural venue for an observation that a specific integer matrix's characteristic polynomial has a specific prime-divisibility pattern. LAA accepts short notes; the result is 3 pages including the table. The "doubly-invariant subalgebra has Killing form $(-4)^{15} \oplus (0)^1$" is a clean linear-algebra fact and would be a tidy auxiliary in such a note.

2. **Linear and Multilinear Algebra**: similar to LAA, slightly more permissive on integer-matrix observations of this scope.

3. **Experimental Mathematics**: the result fits the "computer experiment yields a clean prime-divisibility pattern" template, with the verification script doing the heavy lifting.

4. **Physics Letters B (short note)**, only if the manuscript is rewritten to (a) derive $T$ from a physical Lagrangian or representation, (b) compute one falsifiable consequence (a coupling, a mass ratio, a decay rate), and (c) drop the "wobble" terminology in favor of standard physics naming. The current draft does none of these.

The cover letter's mention of *Physics Letters B* as a fallback is an improvement, but PLB will likely raise the same objection (no derived physics observable). LAA is the cleanest fit.

---

## §6 — What Would Make This a PRD Paper

To salvage the PRD submission, the authors would need to:

1. **Derive $T$ from a physical Lagrangian.** Currently $T$ is given as a literal integer matrix. A PRD referee needs to see the path: "this matrix arises from such-and-such finite-symmetry sector of such-and-such GUT model, where the entries 0, 3, 4, 7, 8, 9 represent such-and-such coupling structure constants." Without that, $T$ is a number puzzle.

2. **Compute one falsifiable physical consequence of the prime-11 / prime-7 separation.** For example: a fermion mass ratio, a CKM matrix entry, a proton lifetime, a magnetic moment. The 16-dimensional doubly-invariant subalgebra suggests a Pati-Salam route; what does that specifically *predict* that other SO(10) breakings don't?

3. **Establish lens-independence or justify the lens choice.** §3 (Honest scope) needs to confront the TSML_RAW vs TSML_SYM tension head-on. If $c_2 = 17$ on the symmetrized table, the paper needs to argue (with physical reasoning, not project-convention) why RAW is the one whose prime-11 pattern is physically meaningful.

4. **Drop "wobble" / "HARMONY" / "TIG" terminology** in the manuscript body. PRD readers will not know these terms; the boxed terminology adds noise without communicating content. State the claim in conventional notation: "Let $T$ be the matrix … . Then …".

5. **Cite a peer-reviewed source for the PrSAC / so(10) Pati-Salam route.** §2.2 cites "WP104" (an internal whitepaper) for the doubly-invariant identification. PRD requires cited sources be retrievable; an arXiv or DOI link to a separately-submitted companion is acceptable, but a self-reference to a private-corpus filename is not.

5 is straightforward (cosmetic). 1–3 are substantive and would convert the paper from a 3-page note into an 8–12 page PRD article.

---

## §7 — Per-Venue Cap Reality Check

The README and cover letter flag this as the **3rd PRD paper in the same quarter** from this collaboration (after J44 and J45). PRD's editorial practice does not have a hard "2/quarter" cap, but in practice multiple closely-related submissions from the same author/collaboration in a single quarter trigger desk-level coordination among editors, and the third paper is more vulnerable to "the substance is already covered in your earlier submission" desk-rejection. **Combined with the §3–§4 critique, this paper is at high risk of desk-rejection at PRD.**

The proposed *Phys Lett B* fallback is more permissive on volume but, as noted, will raise the same scope objections. **The right move is to retarget to LAA** (or one of the other linear-algebra/experimental-math venues), where the result is a strong fit and the per-venue-cap question doesn't arise.

---

## §8 — Recommendation Summary

**As submitted to PRD: REJECT.** The paper has no derived physical observable, presents an integer matrix without derivation from physics, and acknowledges its own central claim as "interpretive, not derived" in its own §3.2.

**Recommended path:**

1. **Retarget to *Linear Algebra and Its Applications*** (or *Linear and Multilinear Algebra*) as a short note titled, e.g., *"On the Prime-Divisibility Pattern of the Characteristic Polynomial of a 10×10 Integer Matrix Arising in a Discrete Magma."* Strip the wobble/HARMONY/TIG terminology; state the result in conventional notation; let the integer-factorization theorem stand on its own clean merits. Expected outcome: accepted with minor revision, 4-page short note. The verification script is exactly the kind of reproducible artifact LAA referees appreciate.

2. **Keep the physics interpretation for a separate paper.** If the so(10) Pati-Salam route, the doubly-invariant Killing form, and the 9-vector VEV machinery yield a derived fermion-mass prediction (which is the J38/WP108 program), THAT paper is the PRD paper. The wobble localization is auxiliary content that paper can cite from LAA.

3. **If the authors insist on a physics venue right now**, the smallest credible target is *Modern Physics Letters A* or *International Journal of Modern Physics A*, both of which accept structural-algebraic observations with looser falsifiability requirements than PRD. Even there, the lens-dependence in §3.1 of the manuscript is a referee-bait paragraph; tighten it before submission.

**Strengths to preserve in any revision:**

- The integer math is solid. `wobble_check.py` is exactly the right kind of verification artifact.
- The factorization $\mathrm{disc}(g) = 2^{16} \cdot 7^7 \cdot 659 \cdot \ldots$ is a clean closed-form result.
- The §3 honest-scope paragraph is the manuscript's best feature and should be expanded rather than stripped — it's why a careful referee would be willing to engage with the paper.

**Net assessment:** **the math is correct, the framing is wrong for PRD, the right venue is LAA.** Estimated effort to retarget: 1–2 days (rewrite intro and §2, strip project terminology, retitle, resubmit). Estimated probability of acceptance after retargeting: ~80% at LAA, vs ~10% at PRD as currently constituted.

---

*Reviewer note on independence:* I read this manuscript with no prior exposure to "TIG" or to the surrounding whitepaper corpus. The terms "wobble," "HARMONY," "TSML," "BHML," "$P_{56}$," and "$\sigma^3$" are all opaque to me except as introduced in the manuscript itself. This is, I believe, the correct fresh-eyes lens for a PRD referee.
