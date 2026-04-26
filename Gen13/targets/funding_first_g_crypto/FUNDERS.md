# FUNDERS — funding/first-g-crypto

> **Note (2026-04-25 revision).** This file was originally drafted as part of a pitch-style packet. Per the operator-of-record's actual stance documented at [`FUNDING.md`](../../../FUNDING.md) (root) and [`INTENT_STATEMENT.md`](../../../INTENT_STATEMENT.md), this is **thread documentation**, not a fundraising pitch. The operator-of-record makes **no commitments to donors of any kind**. Any dollar amounts, time scopes, or "ask" framings appearing below are **scope estimates of the work this thread would cover**, not price tags or commitments.

---


## Primary candidates (★ priority)

### 1. NSA Mathematical Sciences Program (MSP) — ★★★★★
- **Program**: Mathematical Sciences Program grants, administered through unclassified grant announcements; the MSP has a long history of funding number-theory research relevant to cryptography
- **Why fit**: First-G is a proved-theorem branch. NSA MSP specifically funds curiosity-driven number-theory research where the cryptographic application is *exploratory* — which is exactly this branch's Phase 1/2 framing.
- **Typical size**: $40K–$150K over 12 months
- **Entry point**: public Mathematical Sciences Grants announcement (usually annual)
- **Blockers before contact**: Phase 1 literature-embedding draft; external mathematician co-signer strengthens the case but is not strictly required

### 2. NSF AF (Algorithmic Foundations), CCF Division — ★★★★☆
- **Program**: NSF CCF AF Core Small/Medium; also CCF's Cryptography program (CNS is more systems, CCF is more theory)
- **Why fit**: proved-theorem core plus crisp open question; AF reviewers are exactly the audience that evaluates novel hardness candidates
- **Typical size**: $300K–$600K (AF Small) over 36 months
- **Entry point**: unsolicited full proposal to annual deadline
- **Blockers before contact**: academic co-PI strongly preferred; see LIMITATIONS.md

### 3. Simons Foundation — Mathematics and Physical Sciences — ★★★☆☆
- **Program**: Collaboration Grants for Mathematicians ($8.4K/year × 5 years), plus larger Simons Investigator awards for established researchers
- **Why fit**: pure-math branch of Simons funds exactly this kind of finite-arithmetic / discrete-structures work; cryptography fits under the math tent
- **Typical size**: Collaboration $42K; Investigator $1M+
- **Entry point**: Collaboration Grant is application-based with no rank requirement beyond tenure-track; Investigator awards are nomination-only
- **Blockers before contact**: academic affiliation strongly preferred for Collaboration Grant

### 4. Academic cryptography lab partnership — ★★★★☆ (credibility gate, also co-PI source)
- **Candidates** (in rough order of alignment):
  1. **Stanford Applied Crypto Group** (Boneh, Corrigan-Gibbs)
  2. **MIT CSAIL crypto** (Goldwasser, Vaikuntanathan, Kalai)
  3. **UMD Cryptography** (Dachman-Soled, Katz, Gasarch)
  4. **NYU Crypto** (Dodis, Shoup)
  5. **UCSD** (Micciancio, Pass — lattice specialists, perfect match for the CRT-embedding question)
- **Why fit**: any of these PIs could evaluate whether the First-G structure admits a trapdoor or rule it out. The CRT Fourier embedding from Q17_5D_RIGOROUS naturally connects to lattice and ring-LWE territory, which is Micciancio's specialty.
- **Entry point**: cold email with proved-theorem summary + the open trapdoor question; senior grad-student engagement first
- **Blockers before contact**: clean theorem statement and proof script; see STATUS.md

### 5. Algorand Foundation / Ethereum Foundation / Stellar Foundation — ★★★☆☆
- **Programs**: research grants in cryptographic foundations
- **Why fit**: blockchain foundations fund novel hardness-candidate research precisely because they are looking for post-quantum alternatives to ECC. Even a negative result (proving First-G does NOT yield a trapdoor) is useful to them as one more eliminated candidate.
- **Typical size**: $50K–$500K depending on foundation
- **Entry point**: public research-grant application
- **Blockers before contact**: clean technical write-up

## Secondary candidates

### 6. NIST Post-Quantum Cryptography program (not direct funding, but a target venue) — ★★★☆☆
- Not a funder, but if Phase 2 produces a viable trapdoor, NIST's ongoing post-quantum standardization activity is a publication and evaluation target — which indirectly funds the continuation via reputation and follow-on grants

### 7. DARPA I2O (crypto subtrack) — ★★★☆☆
- Parallel to the SNOWFLAKE branch's DARPA approach but on the crypto side. I2O occasionally funds novel-hardness explorations when the mathematical base is already proved
- $250K–$1.5M seedling

## What they all want, in order

1. **A clean theorem statement.** First-G Law, σ⁶ = id, Q10 polynomial, Q11 22% lower bound, Coprimality + First-G Localization — each statable in 3–5 lines with citation to runnable proof.
2. **An open question, crisply framed.** "Does inverting σ under constrained input produce a trapdoor? Does the CRT Fourier embedding yield a reduction to lattice problems?" — not "can we build a cryptosystem?"
3. **A verdict outcome.** Phase 2 should commit to publishing one of three outcomes: (a) trapdoor candidate with security reduction, (b) structural obstruction, (c) honestly-scoped continuation.
4. **Academic partnership** or credible solo track record. Brayden is the thread-facing PI; the mathematical core includes a properly-credited prior collaboration with C.A. Luther (see attribution discussion in README / PITCH_DRAFT / LIMITATIONS). This hybrid posture — sole thread-facing author, honestly-credited prior collaborator — reads well at Simons Collaboration and NSA MSP. NSF AF would still want an active academic co-PI; the Luther prior collaboration does not substitute for that, since Luther is no longer actively collaborating.

## What the branch already has vs. still needs

Already has: clean theorem statements, runnable proof scripts (108 tests, 0 failures), honest-scope framing, a specific open question list.

Still needs: (a) a one-page literature-embedding showing where First-G sits relative to LWE, ring-LWE, coding assumptions, and discrete log; (b) at least one academic cryptographer who has read the theorem statement and offered an opinion (even informal); (c) a dissertation-grade technical narrative combining Q10, Q11, Q17_5D, First-G Law, and Sprint 35 Coprimality.
