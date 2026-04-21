# FUNDERS — funding/civilization-coherence

## Primary candidates (★ priority)

### 1. Santa Fe Institute — External Faculty / Research Fellowship — ★★★★★
- **Program**: SFI External Faculty affiliations, research fellowships, and short-term resident programs; SFI has a 40-year track record of funding exactly this kind of civilizational-scale complexity modeling (think Turchin, Arthur, Ostrom)
- **Why fit**: the coherence-grammar civilization simulator is a natural SFI topic — complex adaptive systems, emergent dynamics, tractable-but-nontrivial models. Empirical comparison with Seshat (which SFI hosts) is a natural Phase 2 path.
- **Typical size**: External Faculty is affiliation not funding; short-term fellowships ~$10K–$50K; longer programs $100K–$300K
- **Entry point**: contact an existing SFI faculty member (Turchin, Flack, DeDeo, Bettencourt) about short visit / working group; SFI working-group proposals are a fast path
- **Blockers before contact**: clean simulator documentation; one-page summary of the research question

### 2. NSF SBE — DISES (Dynamics of Integrated Socio-Environmental Systems) — ★★★★☆
- **Program**: NSF SBE/BCS DISES funds computational-social-science work at the intersection of social dynamics and environmental / institutional dynamics
- **Why fit**: the R-σ-Λ-H civilizational state vector fits DISES's "integrated system dynamics" framing; empirical comparison with V-Dem or WVS is a standard DISES deliverable
- **Typical size**: $300K–$1.6M over 3 years
- **Entry point**: annual DISES solicitation
- **Blockers before contact**: academic co-PI; integrated-systems framing in the proposal

### 3. John Templeton Foundation — ★★★★☆
- **Programs**: Templeton funds foundational-questions work including computational approaches to social dynamics, cohesion, trust, institutional integrity
- **Why fit**: the civilization-coherence simulator aligns with Templeton's "big questions with tractable computational form" funding pattern
- **Typical size**: $150K–$1M for individual-investigator; larger for consortium projects
- **Entry point**: online letter of inquiry (LOI) → full proposal on invitation
- **Blockers before contact**: clean empirical-fit specification; academic affiliation preferred

### 4. Schmidt Futures — AI for Social Good / Novel Methods — ★★★☆☆
- **Programs**: Schmidt Futures funds ambitious, cross-disciplinary computational-social-science work
- **Why fit**: a coherence-based civilization simulator with explicit empirical-comparison plan fits Schmidt's "novel methods for persistent problems" interest
- **Typical size**: $100K–$5M depending on program
- **Entry point**: invitation-dependent; connections through academic hosts or existing Schmidt fellows
- **Blockers before contact**: invitation or academic institutional host

### 5. Paul Allen Family Foundation — Integrative Science — ★★★☆☆
- **Programs**: Allen Family's integrative-science grants
- **Why fit**: cross-disciplinary computational work is within their scope
- **Typical size**: $100K–$750K
- **Entry point**: typically invitation-based; LOI for some programs
- **Blockers before contact**: institutional host; invitation pathway

## Secondary candidates

### 6. Omidyar Network / Open Philanthropy (social-dynamics subtracks) — ★★☆☆☆
- Occasional funding for institutional-trust and social-cohesion modeling; not dedicated computational-social-science pipelines but worth exploring
- $50K–$500K

### 7. Seshat Global History Databank consortium — ★★★☆☆ (collaboration, not direct funding)
- Turchin-led Seshat consortium is a natural empirical-comparison partner; affiliation with Seshat grants data access and academic co-authorship pipeline
- Entry: cold email to Seshat PI or affiliate

## What they all want, in order

1. **Strict-scope framing**. The pitch must not sound like futurism. It must sound like computational social science: here is a model, here is the specific empirical comparison, here is the pass/fail criterion.
2. **An empirical benchmark**. What dataset (WVS, V-Dem, Seshat, ANES) does the simulator output get compared to? What is the comparison metric? What result means the simulator fits / doesn't fit?
3. **Honest verdicts**. The deliverable commits to publishing *whatever result comes out*, positive, negative, or mixed. No cherry-picking.
4. **Academic co-PI** or institutional host for non-foundation paths (NSF DISES especially requires academic affiliation).
5. **Strip consciousness-anchored language**. Any reference to V20 or related framings from the Jan 2026 Trifecta must be re-framed in computational-social-science terms before a reviewer sees them. This is critical — a "consciousness-anchored" framing will get the pitch dismissed by sociology reviewers on arrival.

## What the branch has vs. needs

Has: runnable simulators (tig_civilization_v5.py, v7.py, 1,340 LOC combined), the TIME-FOR-HELP repo clone, the R-σ-Λ-H state variables.

Needs: (a) simulator documentation for reader who has not seen the code, (b) empirical-fit specification naming dataset + metric + pass/fail, (c) SFI / academic co-PI engagement, (d) literature-positioning against existing comp-soc-sci (Axelrod, Schelling, Acemoglu-Robinson, Turchin cliodynamics, Bak-Sneppen coevolution), (e) framing cleanup removing consciousness-anchored language.
