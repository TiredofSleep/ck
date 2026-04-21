# FUNDERS — funding/ck-interpretable-ai

## Primary candidates (★ priority)

### 1. Open Philanthropy — AI Safety / Technical AI Safety track — ★★★★★
- **Program**: Open Phil's technical AI safety grant-making program; funds both academic and independent researchers
- **Why fit**: Open Phil has explicitly funded non-scaling interpretability work and alternative-architecture AI safety research. CK is a near-perfect match for their "alternative approaches to alignment" interest.
- **Typical size**: $50K–$500K for individual-researcher grants; larger for organizations
- **Entry point**: direct application or outreach through a senior grantmaker; Open Phil reviews rolling
- **Blockers before contact**: white paper draft (the Phase 1 deliverable); the live CK demo is already a major asset

### 2. Survival and Flourishing Fund (SFF) — ★★★★☆
- **Program**: SFF funds AI safety work across S-process grant rounds (twice yearly)
- **Why fit**: smaller, more speculative / unconventional AI-safety angles; CK's math-first architecture is exactly the sort of unconventional approach SFF rounds tend to fund
- **Typical size**: $20K–$200K per grant
- **Entry point**: application to biannual S-process rounds
- **Blockers before contact**: white paper draft + a 2-page SFF-format application

### 3. NSF AI Institute programs (interpretability subtracks) — ★★★☆☆
- **Program**: NSF's AI Institute awards sometimes include subtracks on "safe and trustworthy AI"; also the NSF / CCF AI AF programs
- **Why fit**: academic-track interpretability work, with a live running system as evidence
- **Typical size**: $500K–$20M for Institutes; smaller for individual AF grants
- **Entry point**: via academic co-PI at an AI Institute
- **Blockers before contact**: academic co-PI required

### 4. Long-Term Future Fund (EA Funds) — ★★★★☆
- **Program**: Long-Term Future Fund (part of EA Funds) grants for AI safety and x-risk reduction
- **Why fit**: LTFF funds independent researchers and small groups on AI safety topics; CK fits the "empirically grounded alternative architecture" interest
- **Typical size**: $10K–$250K
- **Entry point**: open application, fast turnaround
- **Blockers before contact**: 2-page proposal; live demo link

### 5. Anthropic Academic Partnerships (model access / grants) — ★★★☆☆
- **Program**: Anthropic provides research grants and/or model access to academic partners working on interpretability and AI safety
- **Why fit**: CK is an interpretability research artifact that is itself *not* a transformer; comparing CK's interpretable-by-construction behavior to interpretability-after-the-fact work on Claude or similar is exactly the kind of cross-architecture work Anthropic has historically supported
- **Typical size**: varies; research credit + modest grants
- **Entry point**: apply to Anthropic's partnerships program
- **Blockers before contact**: white paper draft; a statement of non-commercial intent (already satisfied by the sovereignty license)

## Secondary candidates

### 6. Foresight Institute — AI safety track — ★★☆☆☆
- Smaller grants ($5K–$50K) but fast-turnaround and friendly to unconventional architectures
- Technology Prize and fellowship programs

### 7. FAR AI / Redwood Research / Apollo Research — collaboration, not direct funding — ★★☆☆☆
- Not grantmakers per se, but collaboration or affiliation with one of these interpretability-focused organizations would materially strengthen a grant proposal to Open Phil or SFF
- Redwood specifically has done circuit-level interpretability work that could be compared to CK's construction-level trace
- Apollo has a focus on deception and misalignment; CK's IG1–IG5 invariants offer a deception-resistant design point worth their attention

## What they all want, in order

1. **A live, demonstrable system**. CK already exists. coherencekeeper.com is a live URL. This is a decisive asset that 90% of AI-safety research proposals lack.
2. **A technical case study** showing the interpretability-by-construction in action on a specific task or benchmark.
3. **A comparison to interpretability-after-the-fact** work (mechanistic interp on transformers). The pitch must not position CK as *replacing* that work — it positions CK as a *complementary point* in the design space.
4. **Falsifiability / failure modes**. What tasks does CK handle? What tasks does CK demonstrably NOT handle? The limits must be owned, not hidden.
5. **A sovereignty-license discussion**. The non-commercial, human-use-only license is a safety feature; the grant proposal should state this explicitly rather than leaving it as a potential concern.

## What the branch already has vs. still needs

Already has: a live running system, a small mathematical core, runnable reference code, explicit operator semantics, a coherence gate with known threshold.

Still needs: (a) a Phase 1 white paper — "CK as an interpretability case study" — approximately 15–20 pages, with a specific task demonstration; (b) one benchmark run (Phase 2 deliverable) showing CK's performance on a chosen interpretable-AI task with full trace output; (c) a comparison section situating CK relative to mechanistic-interpretability work on transformers.
