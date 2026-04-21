# FUNDERS — funding/self-healing

## Primary candidates (★ priority)

### 1. AFRL (Air Force Research Laboratory) — Autonomy Capability Team — ★★★★★
- **Program**: AFRL RQ (Aerospace Systems) autonomy programs; AFRL RI (Information) resilient-systems programs; Young Investigator Program (YIP) for eligible PIs
- **Why fit**: AFRL funds autonomous-systems work with closed-loop damage recovery as an explicit interest. Dual-lattice self-healing's coherence-matching + repair-action-vocabulary is exactly the kind of "novel substrate for resilience" AFRL evaluates
- **Typical size**: $100K–$150K/year for YIP (3 years); $500K–$2M for full programs
- **Entry point**: white paper to a program manager; AFRL has rolling evaluation
- **Blockers before contact**: architectural writeup; named benchmark domain

### 2. NASA JPL — NIAC (NASA Innovative Advanced Concepts) — ★★★★☆
- **Program**: NIAC Phase I ($175K / 9 months) and Phase II ($600K / 2 years) for advanced spacecraft concepts
- **Why fit**: spacecraft operate for years without human repair; self-healing autonomy is directly relevant. NIAC specifically funds unconventional approaches with rigorous feasibility gate
- **Typical size**: Phase I $175K, Phase II $600K
- **Entry point**: annual NIAC solicitation (usually January)
- **Blockers before contact**: feasibility study + named spacecraft-subsystem target for the demonstration

### 3. ONR (Office of Naval Research) — Autonomy and Counter-Autonomy — ★★★★☆
- **Program**: ONR Codes 341 (Autonomous Systems) and 311 (Information); BAAs covering autonomy, resilience, and cyber-resilience
- **Why fit**: Navy platforms operate autonomously at long range with limited repair access; self-healing is a Navy-operational concern
- **Typical size**: $500K–$3M over 36 months
- **Entry point**: BAA response (annual N0001425SB001 and successor)
- **Blockers before contact**: Phase 1 complete; architectural writeup; measurement plan

### 4. NSF CISE RI (Robotics and Intelligent Systems) — ★★★☆☆
- **Program**: NSF CISE IIS Robust Intelligence; also RI Core Small/Medium
- **Why fit**: academic robotics / autonomous-systems research funds algorithmic approaches to resilience; dual-lattice fits
- **Typical size**: $300K–$600K (Small), $600K–$1.2M (Medium) over 36–48 months
- **Entry point**: annual deadline, full proposal
- **Blockers before contact**: academic co-PI required

### 5. DARPA resilient-autonomy programs (various) — ★★★☆☆
- **Programs**: DARPA has recurring interest in resilient autonomy — e.g., programs descending from RADICS (power grid) and REMA (autonomy for missile-defense); check current I2O / TTO portfolios
- **Why fit**: DARPA funds high-risk architectural bets on resilience; dual-lattice's closed-loop is their architectural register
- **Typical size**: $1M–$10M
- **Entry point**: seedling or BAA

## Secondary candidates

### 6. Industrial partners — ★★★☆☆
- **Semiconductor fabs**: self-healing is a real concern for fab uptime; companies like TSMC, Samsung, Intel have internal research budgets for process-fault-recovery
- **Cloud providers**: AWS, Google Cloud, Azure have internal teams on self-healing distributed systems (some of these also show up in Branch A's funder list)
- **Grid operators**: ERCOT, ISO-NE, PJM have resilience budgets
- These are collaboration / applied-research paths, not direct grants

### 7. Moore Foundation (Data-Driven Discovery / Symbiotic Science) — ★★☆☆☆
- Long shot: Moore occasionally funds ambitious resilience / complexity-science work at foundation scale
- $500K–$2M
- Invitation-dependent

## What they all want, in order

1. **A named target domain**. "Self-healing in general" is too broad. "Self-healing for distributed-fault-tolerant compute fabric under asymmetric node-failure" or "self-healing for spacecraft attitude-control degradation" is fundable.
2. **A closed-loop demonstration plan**. Detection without repair is insufficient; repair without detection is hand-waving. The pitch must describe both and the loop that closes them.
3. **A safety envelope**. What guardrails prevent the self-healing loop from making the system worse (e.g., oscillating repair actions, cascading compensations)? This is especially important for AFRL / NASA / ONR where operational safety is mission-critical.
4. **Falsifiability**. What outcome on the Phase 2 benchmark would cause the PI to conclude dual-lattice self-healing does not work in that domain?
5. **Relationship to existing self-healing literature**. Fault-tolerant distributed systems, model-based fault detection and identification (FDI), autonomous spacecraft fault management (e.g., NASA Mission Data System), soft-robotics morphological repair. Where does dual-lattice sit relative to these?

## What the branch already has vs. still needs

Has: the external repo with architectural sketches, the TIG Unity simulator substrate, the TSML/BHML vocabulary, the coherence-gate pattern.

Needs: (a) integration + architectural writeup, (b) target domain selection, (c) named benchmark, (d) safety-envelope specification, (e) literature-positioning section comparing to FDI, autonomous spacecraft fault management, soft-robotics morphological repair, (f) academic or industrial collaborator who can evaluate.
