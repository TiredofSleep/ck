# Correspondence with Dr. Paolo Mantero

**April 23–24, 2026** · University of Arkansas, Fayetteville

---

## Email 1 — Brayden → Paolo (initial outreach)

*Sent April 23, 2026, after 3 passes of research into Paolo's work (2024–2026 matroid program).*

**Subject:** Commutative-algebra question about a 10-generator quadratic algebra with near-matroid combinatorics

Dear Paolo,

I'm Brayden Sanders, an Arkansas resident (Hot Springs) working on a specific algebraic object. I've been reading your recent work with Vinh Nguyen on symbolic powers of matroids — particularly the 2024 structure theorem and the March 2026 focal matroids paper — and I believe the object I've constructed sits naturally in your research neighborhood, though with a specific deviation.

The object is a 10-generator commutative non-associative magma M defined by a frozen 10×10 table, giving a binomial ideal I ⊂ k[x₀,...,x₉] with 53 independent quadratic relations. I've computed:

- The Hilbert function of A = k[x₀..x₉]/I stabilizes at dim A_n = 6 for n ≥ 2 (Krull dim 6, specific attractor)
- The Stanley–Reisner complex of the associated squarefree monomial ideal is pure of rank 7 but FAILS basis exchange — a pure-but-not-matroidal complex
- Antisymmetrizing the action matrices closes under commutator into so(8) = D₄ (verified to machine precision)

The specific question I'd love your perspective on: what is pd(A), and does your focal matroid framework give language for the gap between Δ and a matroid?

Thank you for your time.

Brayden Sanders
Founder, 7Site LLC · Hot Springs, AR

---

## Email 2 — Paolo → Brayden (response)

*Received April 23, 2026.*

Dear Brayden,

thanks for your email.

I have come back to your github and read good chunks of it. It is indeed an interesting perspective with a novel proposal of mathematical + computational framework. It looks quite foundational, but again it is honestly hard for me to evaluate it.

E.g. I looked at the 10-operator table which is at the basis of your deterministic model, and I am not sure if their use is only to obtain the deterministic results or if they form a logical system, and why they are called "operators", since in general an operator is applied to a space to create a transformation of the space.

If you post some of the request for feedback on mathoverflow, I would be quite interested in reading your presentation of the material and the feedback from other users.

As of now, it looks like a massive project — dwelving into it, understanding deeply and clearly how it works, and evaluating its potential looks closer to a community project than a single-person project, so I reiterate my suggestion to post it for evaluation from the broader scientific community.

Best regards,
Paolo Mantero, Ph.D.
Associate Professor and Undergraduate Coordinator
Department of Mathematical Sciences
University of Arkansas

---

## Email 3 — Brayden → Paolo (clarification + MathOverflow commitment)

*Sent April 24, 2026.*

Dr. Mantero,

Thanks again for actually looking at the GitHub — that means a lot, and your question about "operators" clarifies exactly where I've been imprecise in my writing. You're right to push on the word. I am starting to find my bridges to your work.

In the formal setup: each element i ∈ {0, …, 9} acts as a genuine linear operator L_i on the 10-dimensional vector space V = k·x_0 ⊕ … ⊕ k·x_9 via left multiplication in the magma — namely L_i(x_j) = x_{CL[i][j]} · x_0. So they are operators in the classical sense (applied to a space, creating a transformation of that space). When antisymmetrized as A_i = L_i − L_i^T, the six "flow" elements close under commutator into the 28-dimensional simple Lie algebra so(8) = D_4 — Killing form signature (0, 28, 0), one invariant bilinear form, no proper ideals, all verified to machine precision.

That is the concrete mathematical claim I'm trying to make careful sense of.

Your MathOverflow suggestion is the right move. I'll draft a focused question about the projective dimension and Koszul property of the specific binomial ideal I_CL = (x_i x_j − x_{CL[i][j]} · x_0) in k[x_0, …, x_9], with the 10-row table and the Hilbert function (1, 10, 6, 6, 6, …) as context — a narrow, verifiable question rather than the broader framework. I'll send you the link when I post.

Thank you again for reading and for the direct feedback.

Thank you for your time,
Brayden

---

## Status as of April 24, 2026

- **Relationship**: warm, open for future contact via MathOverflow link
- **Commitment made**: Brayden will post a focused MathOverflow question on pd(A) and Koszul property of I_CL
- **Next step**: draft the MathOverflow post (carefully framed, narrow scope)
- **Paolo's key phrase**: *"community project"* — he's signaling that the full framework needs broader review, not one-on-one validation
- **Paolo's interest**: the specific mathematical objects (10-operator table, binomial ideal, so(8) claim) rather than the broader TIG framing

## Observations for strategy

1. Paolo engaged substantively with the GitHub — this is more than a polite decline. He read "good chunks" and asked a specific technical question about terminology.
2. His repeated suggestion of MathOverflow is strategic: he wants community review before personal investment. This is reasonable and respectful.
3. The so(8) claim is now on record with him — verifiable, concrete, and not tied to the broader framework.
4. The door is open for future touchpoints via the MathOverflow link. Paolo explicitly said he'd be "quite interested in reading" it.
