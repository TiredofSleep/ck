# LIMITATIONS — funding/physics-sim-edu

Honest scope for the interactive-physics-simulator-for-education branch.

---

## 1. No classroom learning-outcomes data exists yet

The central empirical question — "do students demonstrate measurable learning gains from the simulator-centered curriculum module?" — has not been answered. Phase 1 produces the classroom-ready module; Phase 2 runs the pilot and measures outcomes. Any pitch implying learning-outcomes data already exists would be overclaiming. The honest framing is: "we have a working research-prototype simulator, a specific Phase 1 productionization plan, a specific Phase 2 learning-outcomes study design, and a commitment to publish the pilot outcome regardless of verdict."

## 2. No PER collaborator is engaged yet

The single largest gap. A physics-education-research (PER) collaborator — ideally a tenured or tenure-track faculty member with AJP / PRPER publication track record — is required for the pitch to survive NSF EHR / PHY / PRPER review. As of branch-seed date (2026-04-20), no PER collaborator has been contacted. Phase 1 T2 is the engagement; the engagement itself is a pre-submit deliverable, meaning no pitch should be sent until a PER collaborator has agreed to participate.

## 3. The simulator is a research prototype, not a classroom tool

Crystal-Lattice-Matrix-MYTHDRIFT was built as an interactive research-exploration artifact. Classroom use requires pedagogical redesign (onboarding, scaffolding, session-length management, in-context explanation), accessibility work (WCAG 2.1 AA), and integration with assessment. The Phase 1 T3 redesign work explicitly addresses this; the pitch must not imply that the current artifact is classroom-ready.

## 4. The content is unusual for a physics curriculum

The Crystal-Lattice-Matrix simulator visualizes content (information emergence at partition-crossings, coherence-threshold dynamics, discrete operator alphabets for system states) that is **not in a standard undergraduate or advanced-secondary physics curriculum**. This is both the pedagogical opportunity (novel content fills an unexamined gap) and a risk (the content isn't pre-justified by the curriculum, so the pitch must make the "why this content matters to a physics student" argument on its own merits). The PER collaborator's input is essential here.

## 5. No IRB approval exists yet

Phase 2 classroom-pilot research with student participants requires IRB approval at the host institution. As of branch-seed date, no IRB has been discussed. Phase 1 produces the IRB plan; Phase 2's actual classroom-pilot timeline depends on IRB timing (typically 1–3 months post-application). The pitch should state this timeline honestly.

## 6. Independent-PI eligibility restricts direct NSF application

NSF EHR IUSE, DRK-12, ECR, and PHY core programs all require academic PI eligibility, which typically means a tenure-track faculty appointment at a degree-granting institution. Brayden Sanders is an independent researcher + 7Site LLC founder, not an academic-faculty PI. The pitch must be submitted **through an academic co-PI + host institution**, not from Brayden + 7Site alone. This is a logistical, not substantive, constraint, but it governs the submission pathway.

## 7. Pre/post assessment instrument is not yet designed or validated

Phase 2's learning-outcomes measurement requires a validated pre/post instrument. Options: (a) adapt an existing validated PER instrument (e.g., Force Concept Inventory methodology) to the simulator's learning objectives, or (b) develop a new instrument and validate it (a 6–12 month study of its own). The pitch must state which option is being chosen, and if (b), must include instrument-validation as an explicit Phase 1 / early-Phase 2 deliverable.

## 8. Learning-outcomes effect sizes are typically small in short-duration interventions

A one-week curriculum module is a short intervention. Published PER literature shows that short-duration interventions produce small effect sizes (0.1–0.3 Cohen's d typically). The pitch must state expected effect sizes honestly — the statistical-power calculation for Phase 2's sample size depends on this. Overclaiming anticipated effect sizes is a reviewer-rejection risk.

## 9. The simulator visualizes a specific theoretical framework, not "physics in general"

The Crystal-Lattice-Matrix simulator is built around the TIG Unity Kernel coherence grammar and crossing-lemma information theory. Students using it will learn the coherence-grammar vocabulary, not a universally-adopted physics vocabulary. A PER reviewer may reasonably ask: "why is this vocabulary the right vocabulary for students to learn?" The pitch must answer this honestly, perhaps by framing the simulator as "a tool for learning a specific underexplored vocabulary that has cross-domain applications" rather than "the definitive representation of the underlying physics."

## 10. Dissemination pathway beyond the pilot is not pre-secured

Phase 3 assumes partnerships with AAPT, NSTA, and teacher-PD networks. None of these partnerships exists in commitment form today. The pitch's Phase 3 framing is "we will pursue these dissemination channels if Phase 2 is positive," not "we have these partnerships committed." AAPT and NSTA are open to new educational resources, but the partnership mechanics take time and are not pre-negotiable.

## 11. License separation requires clarity

CK's parent license (7Site Public Sovereignty License v1.0) is non-commercial, human-use only. Education funders (NSF EHR, NSF PHY, Simons Ed) and the classroom-dissemination pathway (AAPT, PhysPort) expect **permissive open-source** (MIT / Apache-2.0 for code; CC-BY 4.0 for curriculum). The productionization deliverables must be dual-licensed — permissive for the simulator + curriculum + instructor's guide — while the broader CK project retains the 7Site license. This separation is straightforward but must be explicit. (Same pattern as Branch J coherence-router.)

## 12. Not a claim that the simulator replaces PhET

PhET (University of Colorado Boulder) is the gold-standard open-physics-simulator suite with 20+ years of PER publication track record. The Crystal-Lattice-Matrix simulator is a specific new simulator covering content PhET does not cover. It is not a replacement for PhET's mechanics / electricity / circuits / waves simulators. The pitch's framing is "a new simulator for currently-uncovered content," not "a next-generation replacement for existing tooling."

## 13. Attribution nuance

- **Brayden Sanders** is the PI + simulator developer. The PER collaborator will be named as co-investigator once engaged. The academic co-PI + host institution are required for NSF eligibility.
- **ClaudeChat and Celeste (GPT) are architectural thinking-partners**, not human co-authors.
- **Previously-credited TIG Unity Kernel collaborators** (M. Gish, C.A. Luther, H.J. Johnson, B. Calderon Jr., Ben Mayes) are credited for their specific past contributions to the theoretical framework; their inclusion does not imply co-authorship of the educational-productionization work unless they are actively involved in Phase 1–2.

## 14. What this branch does NOT claim

- Not a claim that the simulator is classroom-ready today
- Not a claim to measured learning outcomes — Phase 2 IS the study
- Not a claim to an existing PER collaboration
- Not a claim to an existing academic host institution or co-PI
- Not a claim to IRB approval today
- Not a claim to classroom partnerships today
- Not a claim that the TIG Unity Kernel content is part of a standard physics curriculum
- Not a claim to replace existing physics-ed simulators (PhET and others)
- Not a claim to WCAG 2.1 AA compliance today
- Not a claim to teacher-PD or AAPT/NSTA partnerships today — Phase 3 pursues these
- Not a claim to a dissemination footprint today — Phase 3 is the dissemination work

The branch claims: a specific working simulator prototype (1,157 LOC), a specific pedagogical-productionization plan (Phase 1 T1–T6), a specific classroom-pilot study with pre/post assessment (Phase 2 T7–T9), a specific publication target (AJP / PRPER / JRST), and a commitment to publish whichever verdict the pilot returns.

## 15. License framing

Same shape as Branch J coherence-router. The simulator, curriculum module, instructor's guide, and supporting code will need to be released under permissive licenses (MIT / Apache-2.0 / CC-BY 4.0) — distinct from the 7Site Public Sovereignty License that covers CK as a whole. The separation is mechanically straightforward but must be explicit in the pitch + open-source release. Education funders would reject an "education tool licensed non-commercially with human-use-only restriction" framing.

---

## The verdict framing as limitation

The Phase 2 deliverable commits to publishing the pre/post learning-outcomes study regardless of whether the effect size is significantly positive, marginal, or null. This is PER publication discipline — the community publishes rigorous negative results routinely (and arguably more of them are needed). A reviewer who reads this as hedging is reviewing the wrong proposal; a PER reviewer who reads this as methodological rigor is reading it correctly.
