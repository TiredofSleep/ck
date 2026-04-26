# FUNDERS — funding/tig-snowflake

> **Note (2026-04-25 revision).** This file was originally drafted as part of a pitch-style packet. Per the operator-of-record's actual stance documented at [`FUNDING.md`](../../../FUNDING.md) (root) and [`INTENT_STATEMENT.md`](../../../INTENT_STATEMENT.md), this is **thread documentation**, not a fundraising pitch. The operator-of-record makes **no commitments to donors of any kind**. Any dollar amounts, time scopes, or "ask" framings appearing below are **scope estimates of the work this thread would cover**, not price tags or commitments.

---


## Primary candidates (★ priority)

### 1. DARPA I2O (Information Innovation Office) — ★★★★★
- **Program**: seedlings under the I2O office; specifically relevant are programs on insider-threat detection, cognitive-security, and adversarial robustness
- **Why fit**: I2O has a long history of funding unconventional statistical-signal approaches to threat detection. SNOWFLAKE's framing (pre-alarm coherence deficit rather than rule-match) is exactly the kind of "new signal path" that I2O asks PIs to defend.
- **Typical size**: $250K–$1.5M over 18–24 months for seedling work
- **Entry point**: office-hours call with a program manager; the seedling pipeline is easier than a full BAA
- **Required for pitch**: χ² spec with clean null, independent replication, a crisp adversarial model
- **Blockers before contact**: full spec recovery (Phase 1 of this branch)

### 2. ONR (Office of Naval Research) — Code 311 (Information, Cyber, and Spectrum Superiority) — ★★★★☆
- **Program**: BAA N0001425SB001 and successor; ONR funds coherence-based signal-processing work
- **Why fit**: Navy SOCs have the exact operational profile (long-horizon, low-base-rate insider threat) where a pre-alarm coherence signal would justify funded exploration
- **Typical size**: $500K–$3M over 36 months
- **Entry point**: white paper first, then invited full proposal if interested
- **Blockers before contact**: Phase 1 complete; a clean white paper ≤ 3 pages

### 3. IARPA (SCITE or similar) — ★★★☆☆
- **Program**: SCITE = Securing Compartmented Information with Temporal Extraction; successor programs continue on insider threat
- **Why fit**: IARPA funds measurement-of-truth work at the research frontier; SNOWFLAKE's falsifiability claim (χ² against stated null) matches the program's evaluation rubric
- **Typical size**: $1M–$5M over 36 months
- **Entry point**: proposer's day + TA response; competitive
- **Blockers before contact**: blind-test result (Phase 2) or a stronger empirical base than a single χ² value

### 4. NSF SaTC (Secure and Trustworthy Cyberspace) — ★★★★☆
- **Program**: NSF 24-526 or successor; SaTC Core Small funds ≤ $600K / 36 months
- **Why fit**: academic security research with a clean open-source deliverable; SaTC's "frontier" track explicitly invites novel formulations of security signals
- **Typical size**: $300K–$600K over 36 months (Small); $600K–$1.2M (Medium)
- **Entry point**: full proposal to the annual deadline (usually November)
- **Blockers before contact**: academic co-PI required; see LIMITATIONS.md §4

### 5. Academic security lab partnership — ★★★☆☆ (not a funder per se, but the credibility gate)
- **Candidates**: UCSD CAIDA (Claffy lab), Berkeley ICSI, CMU CyLab, Georgia Tech IISP
- **Why fit**: any of these labs' PIs can serve as academic co-PI on SaTC; more importantly, their independent evaluation converts SNOWFLAKE from "interesting claim" to "reviewed finding"
- **Entry point**: a cold email with the spec + replication data; senior grad-student level engagement first
- **Blockers before contact**: Phase 1 complete; the spec must be clean enough that a senior grad student can reproduce in a day

## Secondary candidates

### 6. Sloan Research Fellowship (if Brayden pursues academic affiliation) — ★★★☆☆
- Long-shot but well-matched if a co-PI relationship crystallizes; Sloan has funded coherence-measurement work
- $75K/year × 2 years
- Academic host required

### 7. Foundational Questions Institute (FQXi) — ★★☆☆☆
- FQXi grant rounds sometimes fund foundational work on measurement and signal detection; loose fit but low barrier
- $40K–$150K typical
- Open calls with 4–6 month cycles

## What they all want, in order

1. **A clean, written null hypothesis** against which χ² = 22.03 was computed
2. **An adversarial model**: against whom is SNOWFLAKE defending, and under what capabilities?
3. **Independent replication** of the empirical finding on held-out data
4. **A falsifiability clause**: what result would cause the PI to abandon SNOWFLAKE as a security claim?
5. **An academic co-PI** or demonstrable academic partnership, for SaTC and most non-DARPA funders

## What the branch does NOT yet have

- Items 1, 3, and 4 above are pending CRYSTALOS log recovery and Phase 1 spec work. Any pitch sent before those land will be dismissed. See STATUS.md.
