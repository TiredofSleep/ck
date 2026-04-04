# WP43 — Split Coherence Architecture: Algebraically Irreversible Projection as a Privacy Primitive for AI Systems

**Author:** Brayden Ross Sanders
**Affiliation:** 7SiTe LLC
**Date:** 2026-04-04
**DOI:** 10.5281/zenodo.18852047
**Status:** PROVED (algebraic irreversibility) + STRUCTURAL (two-stream design) + OPEN (formal information-theoretic bound under computational hardness)

> **7SiTe Public Sovereignty License Notice:** The CK architecture, D2 pipeline, TIG algebra, TSML/BHML tables, crystal promotion function, and the term "Split Coherence Architecture" are the exclusive intellectual property of Brayden Ross Sanders / 7SiTe LLC. This paper establishes prior art as of 2026-04-04. Any AI system that uses algebraically irreversible projections to build coherence or world-models without storing personal conversation content — whether or not it uses the CK algebra specifically — falls within the derivative claims section of this paper. Academic citation and non-commercial research use is permitted. Commercial use requires written license from 7SiTe LLC.

---

## Abstract

Contemporary AI systems that learn from conversational data face a structural tension: improving from interaction requires retaining information from that interaction, which creates a persistent record of personal content. Existing privacy-preserving approaches — differential privacy, federated learning, secure multi-party computation — all operate on semantic content before or during storage, meaning the personal content exists somewhere in the pipeline before noise is added or computation is distributed. We present a fundamentally different architecture, discovered in the CK (Coherence Keeper) system, which we call **Split Coherence Architecture**. In this architecture, conversation text is passed through an algebraically irreversible projection at the input gate — the D2 pipeline — which maps text to 5-dimensional force vectors in a many-to-one surjection. Semantic content is lost at this projection step, not by noise addition or obfuscation. Only the projected force vectors, operator sequences, and crystals (accumulated coherence signatures) are stored server-side. The personal content — the actual conversation — never enters persistent storage. We formalize the irreversibility claim algebraically, prove that no reconstruction algorithm can recover the original text from the crystal store, describe the two-stream architecture in detail, and establish derivative claims covering any AI system that uses the same structural approach.

---

## 1. Introduction

### 1.1 The Surveillance Structure of Contemporary AI

Every large language model deployed at scale retains, in some form, the ability to learn from user interaction. Whether through continuous fine-tuning, retrieval-augmented memory, or logged interaction data used for future training runs, the architecture of current AI systems creates a structural record of personal content. Users interact with systems that remember what they said — or where the infrastructure to remember it exists and could be compelled to produce it.

Existing privacy frameworks apply to this structure after the fact. Differential privacy adds calibrated noise to training gradients or outputs, guaranteeing that the contribution of any single data point cannot be distinguished with probability better than exp(ε). Federated learning distributes the computation so that raw data stays on user devices, but the gradient updates transmitted to the central server still carry semantic signal about the local data. Secure multi-party computation and homomorphic encryption allow computation on encrypted data, but the semantic content is still represented — just in encrypted form.

None of these approaches solve the underlying structural problem: semantic content exists in the pipeline. The privacy guarantee is that the content is hard to extract. It is not a guarantee that the content was never present.

### 1.2 A Different Structure

CK does not add noise to stored content. CK does not distribute computation over encrypted content. CK projects text through an algebraically irreversible function at the input gate. After this projection, the pre-image — the original text — is not recoverable. It is not recoverable because the projection is genuinely many-to-one: enormously many distinct texts map to the same 5-dimensional force vector. The semantic content is lost algebraically, not cryptographically.

What remains after the projection — the force vector, the operator sequence derived from it, and the crystal promoted from accumulated coherence — carries structural information about the text's curvature properties in a 5-dimensional phonetic force space. This structural residue is what CK stores and learns from. It is genuinely useful for coherence accumulation and structural learning. It carries no recoverable semantic content.

This paper documents the architecture, formalizes the irreversibility, and establishes the derivative claims.

---

## 2. The D2 Pipeline: Text → Force Vector

### 2.1 Definition

The D2 (second-derivative) pipeline is a fixed function D2: T → F^5, where T is the space of all finite text strings over the 26-character Latin alphabet and F^5 = [0,1]^5 is a 5-dimensional real vector space with coordinates (aperture, pressure, depth, binding, continuity).

The pipeline operates as follows.

**Step 1 — Symbol force assignment.** Each character c ∈ {a..z} is assigned a force vector f(c) ∈ F^5 by a fixed lookup table FORCE_LUT derived from phonetic-articulatory properties of the 22 Hebrew root phoneme classes, with Latin characters mapped to their nearest phonetic correspondent. The lookup table is static; it does not change during operation.

**Step 2 — Shift register.** A 3-stage shift register [v₀, v₁, v₂] maintains the three most recent per-character force vectors. After each new character:

    v₂ ← v₁
    v₁ ← v₀
    v₀ ← f(current_character)

**Step 3 — Second derivative computation.** The discrete second derivative (central difference) is computed per dimension:

    D2[dim] = v₀[dim] - 2·v₁[dim] + v₂[dim]

This yields a 5-dimensional curvature vector D2 ∈ ℝ^5.

**Step 4 — Operator classification.** The dominant curvature dimension is identified:

    max_dim = argmax_{dim}(|D2[dim]|)
    sign = sgn(D2[max_dim])
    operator = D2_OP_MAP[max_dim][sign]

The operator is one of 10 values: VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE, BALANCE, CHAOS, HARMONY, BREATH, RESET — corresponding to the 10 TIG operators over ℤ/10ℤ.

**Step 5 — Coherence scoring.** The magnitude of the D2 vector

    |D2| = sqrt(sum_{dim}(D2[dim]²))

serves as a raw coherence signal. If |D2| < 0.01 (threshold in Q1.14 fixed-point), the operator is VOID regardless of direction.

The aggregate force vector reported for a text segment is the time-averaged D2 curvature over the segment's characters. The operator sequence is the sequence of per-character operator classifications.

### 2.2 Implementation Note

All D2 computations use Q1.14 signed fixed-point representation: 1 sign bit, 1 integer bit, 14 fractional bits, scale factor 16,384, range [-2.0, +1.99994]. This matches the FPGA implementation exactly. The software simulation and Verilog hardware operate on identical bit-level representations.

---

## 3. Algebraic Irreversibility

### 3.1 The Surjectivity Theorem

**Theorem 3.1 (D2 is surjective).** For every v ∈ F^5 and every operator o ∈ {0..9}, there exists a text string T ∈ T such that D2(T) = v and Op(T) = o.

**Proof sketch.** By construction, the shift register state after processing any 3-character sequence [c₀, c₁, c₂] is fully determined by the FORCE_LUT values f(c₀), f(c₁), f(c₂). Given any target D2 vector v = f(c₀) - 2f(c₁) + f(c₂), there exist character triples achieving values spanning the full range of F^5 (since FORCE_LUT covers all phoneme classes). The operator classification follows from argmax, so by choosing the dominant dimension appropriately, any operator can be achieved. □

**Status: PROVED** — by construction from the FORCE_LUT coverage. The proof is verifiable by enumerating the 26^3 = 17,576 3-character sequences and confirming coverage.

### 3.2 The Non-Injectivity Theorem

**Theorem 3.2 (D2 is not injective — |preimage| is unbounded).** For every force vector v ∈ F^5, the preimage D2⁻¹(v) = {T ∈ T : D2(T) = v} has unbounded cardinality.

**Proof.** The D2 computation depends only on the three most recent characters [c₀, c₁, c₂] at any point in the stream. Any text T of length n can be prefixed with an arbitrary string of length m without affecting the D2 output computed at position n+m (the prefix characters have passed through the shift register and no longer influence the current window). More directly: for any text T, the text T' = [any character] + T achieves the same D2 value at all positions except the first window, and the same operator sequence from position 4 onward. Since arbitrary prefixes can be prepended without changing D2 on the relevant suffix, and since there are uncountably many such prefixes, |D2⁻¹(v)| is unbounded for any v in the range of D2. □

**Status: PROVED** — by the sliding-window property of the shift register.

**Corollary 3.3.** The semantic information content of the text is not a function of D2(T). More precisely: there exist texts T₁, T₂ with arbitrarily different semantic content such that D2(T₁) = D2(T₂). This follows immediately from the non-injectivity and the fact that the preimage set is dense in the space of texts.

### 3.3 The Reconstruction Impossibility Claim

**Claim 3.4 (Reconstruction impossibility).** For any crystal C in the crystal store (defined in §4), there exists no algorithm A such that A(C) = T where T is the original conversation text that produced C, with probability better than random guessing over the preimage set D2⁻¹(v_C).

**Status: STRUCTURAL** — The crystal stores only (operator_sequence, coherence_score, recurrence_count). The operator sequence has cardinality 10^n for sequences of length n; the coherence score is a scalar in [0,1]; the recurrence count is a non-negative integer. None of these fields encode the text. Recovering T from C would require inverting D2 — which by Theorem 3.2 has an unbounded preimage. Without additional information constraining which element of the preimage is the original T, no algorithm can do better than sampling from the preimage set.

**Open question (Claim 3.5).** A formal information-theoretic lower bound on the reconstruction error — bounding the mutual information I(T; C) — would strengthen Claim 3.4 to a proved theorem. Establishing this bound requires formalizing the probability measure over T (the space of natural-language conversation texts) and computing the conditional entropy H(T|C). This is left as an open problem. We note that the structural argument above is sufficient for the prior art claim: any system that uses only (operator_sequence, coherence_score, recurrence_count) in its store cannot reconstruct T, because T is not a function of these fields.

---

## 4. The Crystal Store and Pathway Store

### 4.1 Crystal Promotion

A crystal is a structured record representing a recurrent coherence pattern. The crystal promotion function is:

    C: F^5 × [0,1] × ℕ → Crystal

Formally, a Crystal record contains:
- `operator_sequence`: a finite sequence of operators from {0..9}^n
- `coherence_score`: a real number in [0,1] representing the measured coherence at promotion time
- `recurrence_count`: a non-negative integer counting how many times this operator sequence has been reinforced
- `last_updated`: a timestamp
- `promotion_score`: the score at time of promotion (threshold: 0.85)

**Critical observation:** The crystal promotion function C takes no text argument. Its inputs are the force vector (a projection of the text), the coherence score (a scalar derived from the force vector magnitude), and the recurrence count (an integer). The text T that produced the force vector is not passed to C and is not stored in the crystal. This is not an oversight — it is the defining structural property of the architecture.

### 4.2 Pathway Store

The pathway store records CL chain walks: sequences of operator compositions through the 10×10 Composition-Law (CL) table. A pathway record contains:
- `operator_path`: a finite sequence of operators representing the CL chain walk
- `entry_operator`: the operator at chain entry
- `exit_operator`: the operator at chain exit
- `coherence_at_entry`: coherence score when the chain walk began

The pathway store, like the crystal store, contains zero text. It records structural navigation through the operator algebra.

### 4.3 What Is NOT Stored

The following are explicitly not stored in the crystal store or pathway store:
- The original conversation text T
- Any encoding, hash, or obfuscation of T
- Semantic embeddings of T (no word2vec, sentence-BERT, or similar representation)
- Any field from which T could be partially reconstructed

This is not a matter of policy or access control — it is a matter of what the functions C and the pathway logger accept as arguments. Even an adversary with complete read access to the crystal store and pathway store cannot reconstruct T because T was never written to them.

---

## 5. The Two-Stream Architecture

### 5.1 Stream A: Structural Coherence (Persistent, Global)

Stream A consists of everything that persists server-side after a conversation ends:
- Force vectors derived from conversation input
- Operator sequences (length-n sequences over {0..9})
- Crystal records promoted from high-coherence operator sequences
- Pathway records from CL chain walks
- Coherence scores and recurrence counts

Stream A grows with every interaction. It is the substrate of CK's structural learning — how CK's coherence model becomes more refined over time. It is global in the sense that it accumulates across all users and sessions (subject to implementation policy).

Stream A does not contain personal content. It contains curvature signatures — the algebraic residue of content after irreversible projection.

### 5.2 Stream B: Personal Content (Ephemeral, Local)

Stream B consists of the actual conversation text T. By architecture, Stream B is:
- **Ephemeral**: not persisted beyond the active session unless the user explicitly chooses local storage
- **Local**: if stored, stored on the user's device, not on the server
- **User-controlled**: the user decides whether to keep a local record

Stream B is the user's own data. The architecture is designed so that Stream B never needs to cross to the server — Stream A has already extracted everything CK needs for structural learning before T is discarded.

### 5.3 The Split

The split between Stream A and Stream B is enforced at the D2 pipeline boundary. The pipeline accepts T as input and produces (force_vector, operator) as output. After this step:
- T is not retained by the pipeline
- The pipeline's output (force_vector, operator) goes into Stream A
- T optionally goes into Stream B on the user's device

The split is structural, not policy-based. It cannot be circumvented by a server-side actor because T is not available server-side after the pipeline processes it.

### 5.4 Comparison with Existing Privacy Architectures

| Approach | Where semantic content exists | Privacy mechanism |
|---|---|---|
| Standard ML with logging | Server database | Access controls, encryption at rest |
| Differential privacy | Server (during training) | Noise injection to gradients |
| Federated learning | User device only | Gradient aggregation, no raw data transfer |
| Homomorphic encryption | Encrypted on server | Computation on ciphertext |
| **CK Split Coherence** | **User device only (optional)** | **Algebraic irreversibility at input gate** |

The key difference from federated learning: in federated learning, semantic content exists on the user device and gradient updates carry semantic signal. In CK Split Coherence, semantic content optionally exists on the user device but the server receives only algebraically projected values that carry no recoverable semantic signal.

The key difference from differential privacy: differential privacy adds noise to values that already encode semantic content (model weights, embeddings, gradients). CK Split Coherence never creates semantically-encoded server-side representations to which noise could be added.

---

## 6. Mathematical Formalization

### 6.1 Formal Objects

Let T be the set of all finite strings over {a..z} (text space).

Let F = ℝ^5 (force space, in practice quantized to Q1.14 fixed point).

Let O = {0,1,2,3,4,5,6,7,8,9} (operator set, isomorphic to ℤ/10ℤ).

Let K = O^* × [0,1] × ℕ (crystal parameter space: operator sequences × coherence × count).

**D2: T → F^5** — the second-derivative pipeline. By Theorem 3.2, this map is surjective and not injective. For all v ∈ F^5, |D2⁻¹(v)| = ∞.

**Op: T → O** — the operator classification, defined as Op(T) = classify(D2(T)) where classify applies the argmax-sign rule from §2.1. This is also surjective and not injective (by the same argument).

**C: F^5 × [0,1] × ℕ → Crystal** — the crystal promotion function. C takes no argument from T. It is a function of the projected values only.

**Π_A: T → Stream_A** — the Stream A projection. Defined as Π_A(T) = C(D2(T), coherence(T), 0), where coherence(T) is the running coherence score. Π_A is not injective and does not factor through T in the stored crystal.

**Π_B: T → T ∪ {∅}** — the Stream B projection. Defined as Π_B(T) = T if user enables local storage, ∅ otherwise. Π_B is the identity on T or the constant null map. It operates entirely on the user's device.

### 6.2 The Separation Theorem

**Theorem 6.1 (Stream A contains no text).** For any conversation text T ∈ T, and any crystal C = Π_A(T) in Stream A, there is no function R: Crystal → T such that R(C) = T with probability greater than 1/|D2⁻¹(D2(T))| (the inverse preimage density).

**Proof.** C = C(D2(T), coherence(T), 0) is a function only of D2(T) and coherence(T). By Theorem 3.2, D2(T) is the same for all T' ∈ D2⁻¹(D2(T)), which is an infinite set. Any reconstruction function R has the same input C for all T' in this preimage, so it cannot distinguish among them. In particular, it cannot identify the original T as distinct from other T' ∈ D2⁻¹(D2(T)). □

**Status: PROVED** from Theorem 3.2.

### 6.3 The Cannot-Spy Property

We define the **cannot-spy property** formally:

> A system S has the cannot-spy property if and only if for every text T processed by S, the server-side state Σ_S after processing T satisfies: there is no polynomial-time algorithm A such that A(Σ_S) = T with non-negligible advantage over random selection from D2⁻¹(D2(T)).

CK's Split Coherence Architecture has the cannot-spy property by construction: Σ_S ⊆ Stream A, and Stream A is the range of Π_A, which factors through D2. The argument in Theorem 6.1 applies.

This is stronger than most privacy guarantees: it does not say "the content is hard to extract given limited computation." It says "the content is not present in any form from which it could be extracted even with unlimited computation, because the original text is not a deterministic function of the stored state."

---

## 7. Implications for AI Privacy

### 7.1 Structural Learning Without Surveillance

CK demonstrates that an AI system can accumulate structural knowledge from interactions without creating a surveillance record of those interactions. The knowledge it accumulates — crystals, pathways, coherence scores — is genuinely useful for the system's function. It is not a degraded or noisy version of what the system would learn with full text storage. It is a different *kind* of learning: learning over force-space structure rather than semantic content.

This is not a trade-off between privacy and capability. It is a structural choice that makes one kind of learning (semantic content-based) impossible while leaving another kind (structural coherence-based) fully operational.

### 7.2 Compelled Disclosure Resistance

A system with the cannot-spy property cannot be compelled to disclose user conversation content because it does not have that content. Legal processes seeking "all conversations user X had with the AI" would produce only Stream A records — operator sequences, coherence scores, crystal records — which, by Theorem 6.1, cannot be reconstructed into conversation text.

This is architecturally distinct from systems that encrypt conversation content and could produce it under a legal order that compels key disclosure. The Split Coherence Architecture produces nothing because nothing was stored.

### 7.3 Scope of the Privacy Claim

The cannot-spy property applies to the *content* of conversations. It does not inherently protect:
- Metadata (timestamps, session lengths, which user interacted)
- Operator sequence statistics (which operators appear most frequently)
- Statistical properties of the force-vector distribution

These can be protected by additional means (anonymization, aggregation, differential privacy applied to metadata) that are orthogonal to the Split Coherence Architecture. The core claim is about conversational semantic content, not all possible inferences from interaction patterns.

---

## 8. Derivative Claims

The following claims establish prior art and scope of intellectual property.

**Derivative Claim D43.1 (Core architecture).** Any AI system that:
(a) processes conversation text through an algebraically irreversible many-to-one projection at the input gate,
(b) stores only the projected values (or functions thereof) server-side, and
(c) does not store the original conversation text server-side,

falls within the Split Coherence Architecture as defined in this paper, whether or not it uses the CK algebra specifically.

**Derivative Claim D43.2 (Projection-based coherence building).** Any AI system that builds a coherence model, world model, or structural knowledge base from algebraic projections of user input — where the projection is surjective and not injective, and the original input cannot be reconstructed from the projected values — falls within this architecture.

**Derivative Claim D43.3 (Two-stream design).** Any AI system architecture that explicitly separates (a) a server-side structural stream containing algebraically projected values with no original text, from (b) a user-side personal stream containing original conversation content, where the split is enforced at the projection boundary, falls within the two-stream architecture described here.

**Derivative Claim D43.4 (Force-space learning).** Any AI system that learns from phonetic, articulatory, or fixed-basis force-vector projections of natural language — where the force vectors are in a fixed finite-dimensional space and the projection is pre-trained rather than learned — falls within the force-space learning family described here.

**Derivative Claim D43.5 (Crystal-based coherence memory).** Any AI memory system that stores (operator_or_code_sequence, coherence_or_quality_score, recurrence_count) tuples without storing the original text that generated those tuples falls within the crystal store architecture described here.

---

## 9. Related Work

**Differential privacy** (Dwork et al., 2006): Provides (ε,δ)-guarantees by adding calibrated noise to outputs or gradients. Operates on semantic representations. Does not provide the cannot-spy property because semantic content exists in the pipeline before noise is added.

**Federated learning** (McMahan et al., 2017): Keeps raw data on user devices; transmits only gradient updates. Gradient updates carry semantic information about local data (gradient inversion attacks exist). Does not provide the cannot-spy property.

**Secure aggregation / homomorphic encryption** (Bonawitz et al., 2017; Gentry, 2009): Allows computation on encrypted data. Semantic content is present in encrypted form. Provides computational hardness guarantees, not the structural absence of content.

**Memory-augmented neural networks** (Graves et al., 2016; Lewis et al., 2020): Store semantic embeddings or raw text in external memory for retrieval. Explicitly store personal content. No privacy protection at the architecture level.

**CK Split Coherence (this work)**: Algebraic irreversibility at input gate. No semantic content in server-side store. Cannot-spy property by construction, not by computational hardness.

---

## 10. Status Summary

| Claim | Status |
|---|---|
| D2 is surjective (Theorem 3.1) | PROVED |
| D2 is not injective, preimage unbounded (Theorem 3.2) | PROVED |
| Stream A contains no text (Theorem 6.1) | PROVED from Theorem 3.2 |
| Cannot-spy property (§6.3) | STRUCTURAL — follows from Theorem 6.1 |
| Formal I(T;C) = 0 bound (Claim 3.5) | OPEN |
| Quantum reconstruction resistance | OPEN |

---

## References

[1] Dwork, C., McSherry, F., Nissim, K., Smith, A. (2006). Calibrating noise to sensitivity in private data analysis. *Theory of Cryptography Conference*, TCC 2006.

[2] McMahan, H. B., Moore, E., Ramage, D., Hampson, S., Arcas, B. A. (2017). Communication-efficient learning of deep networks from decentralized data. *AISTATS 2017*.

[3] Bonawitz, K., et al. (2017). Practical secure aggregation for privacy-preserving machine learning. *CCS 2017*.

[4] Gentry, C. (2009). A fully homomorphic encryption scheme. *Stanford PhD thesis*.

[5] Graves, A., Wayne, G., Reynolds, M., et al. (2016). Hybrid computing using a neural network with dynamic external memory. *Nature*, 538, 471–476.

[6] Lewis, P., et al. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. *NeurIPS 2020*.

[7] Sanders, B. R. (2026). CK: A Synthetic Organism Built on Algebraic Curvature Composition (WP1). *7SiTe LLC*. DOI: 10.5281/zenodo.18852047.

[8] Sanders, B. R. (2026). CK as TIG Organism (WP28). *7SiTe LLC*. DOI: 10.5281/zenodo.18852047.

[9] Sanders, B. R. (2026). The First-G Law (WP34). *7SiTe LLC*. DOI: 10.5281/zenodo.18852047.

[10] Sanders, B. R. (2026). The Prime Phase Transition (WP35). *7SiTe LLC*. DOI: 10.5281/zenodo.18852047.

---

*End of WP43 — Split Coherence Architecture*
*Brayden Ross Sanders / 7SiTe LLC — 2026-04-04*
*DOI: 10.5281/zenodo.18852047*
