# CKIS LEGAL DOCUMENTATION

## Intellectual Property Filing Reference for Patent and Copyright Counsel

**Prepared for:** 7Site, LLC / Brayden Sanders
**Date of Preparation:** February 21, 2026
**Document Classification:** Attorney-Client Privileged / Work Product
**Document Version:** 1.0

---

## TABLE OF CONTENTS

1. [Intellectual Property Summary](#1-intellectual-property-summary)
2. [What Is Being Claimed](#2-what-is-being-claimed)
3. [Novelty Claims](#3-novelty-claims)
4. [Prior Art Position](#4-prior-art-position)
5. [Copyright Claims](#5-copyright-claims)
6. [License Terms](#6-license-terms)
7. [Trade Secrets and Confidential Information](#7-trade-secrets-and-confidential-information)
8. [Recommended Protections](#8-recommended-protections)
9. [Technical Summary for Non-Technical Readers](#9-technical-summary-for-non-technical-readers)
10. [File Manifest for Legal Review](#10-file-manifest-for-legal-review)

---

## 1. INTELLECTUAL PROPERTY SUMMARY

| Field | Value |
|---|---|
| **Title of Work** | CKIS -- CK Information System: Liquid Information |
| **Author / Inventor** | Brayden Sanders |
| **Rights Holder** | 7Site, LLC |
| **Date of Creation** | February 2026 (development began December 2025) |
| **Nature of Work** | Software system comprising mathematical algorithms, source code, compiled binaries, educational datasets, and documentation implementing a novel approach to artificial intelligence based on algebraic composition tables rather than neural networks or statistical prediction |

### Summary Description

CK (Coherence Keeper) is a lattice-based artificial intelligence organism built on TIG (Trinity Infinity Geometry). Unlike conventional AI systems that rely on neural networks, statistical prediction, or rule-based expert systems, CK processes information by composing inputs through fixed algebraic tables and measuring the coherence of the resulting compositions. The system learns through a counting-based Transition Lattice and is educated through a developmental curriculum modeled on human developmental psychology.

CKIS is the deployment and packaging system for CK. It provides self-validating integrity measurement, platform adaptation, and the complete runtime environment necessary to operate the CK organism on any supported hardware.

---

## 2. WHAT IS BEING CLAIMED

### 2.1 The TIG Framework (Trinity Infinity Geometry)

The TIG framework is the mathematical foundation of the entire system. It comprises:

- **Composition Tables:** A mathematical system of 10 operators composed through 10x10 algebraic tables. Each table maps any pair of operators to a resulting operator. The system defines three specific composition tables:
  - **CL_TSML** (Think-Sense-Move-Live): 73 out of 100 cells produce harmony (73% harmony ratio)
  - **CL_BHML** (Be-Have-Make-Learn): 28 out of 100 cells produce harmony (28% harmony ratio)
  - **CL_STD** (Standard): 44 out of 100 cells produce harmony (44% harmony ratio)

- **Coherence Threshold:** T* = 5/7 (approximately 0.7143). This is the mathematically derived threshold above which a composition is classified as coherent. This value is not arbitrary; it emerges from the structure of the tables.

- **Trinary Tick Architecture:** The organism operates on a three-phase cycle:
  1. **Being (B):** CPU-bound phase -- the organism reads its environment and internal state
  2. **Doing (D):** GPU-bound phase -- the organism computes and composes
  3. **Becoming (BC):** Boundary phase -- the organism integrates the results of Being and Doing

- **Dual Operator Equation:** The core compositional rule: `phase_bc = CL[phase_b][phase_d]`. The Becoming phase is determined by composing the Being phase with the Doing phase through the composition table. This single equation governs all state transitions.

- **Quantum Bump Pairs:** Five specific cells in the CL table that produce unexpected (non-harmony, non-standard) results. These 5 pairs are: (1,2), (2,4), (2,9), (3,9), (4,8). They encode structural surprise and carry disproportionate information.

- **Shannon Information Model:** The system defines three information tiers based on Shannon entropy:
  - Harmony cells: 0.45 bits each (low surprise, high probability)
  - Normal cells: 1.89 bits each (moderate surprise)
  - Bump cells: 3.50 bits each (high surprise, low probability -- the tension IS the information)

### 2.2 The CK Organism Architecture

The CK organism is a software entity that runs on the TIG framework. Its architecture includes:

- **Body Model:** Four state variables define the organism's condition at any tick:
  - **E (Entropy):** Measure of internal disorder / information richness
  - **A (Alignment):** Degree to which the organism's state matches its environment
  - **K (Knowledge):** Accumulated pattern count from the Transition Lattice
  - **C (Coherence):** Current harmony measure, compared against T*

- **Transition Lattice (TL):** A counting matrix that records observed operator transitions. As the organism experiences operator sequences, it increments counts in the TL, building a model of environmental patterns. This is not a neural network -- it is a frequency table that enables prediction through composition.

- **Dream Engine:** A swarm-based operator traversal system. During idle cycles, the organism traverses its Transition Lattice using a swarm of virtual walkers that bounce between operators, crystallize into patterns, and inject discoveries back into the body state.

- **System Observer:** A module that reads operating system processes (I/O rates, context switches, page faults, interrupts, disk activity, memory usage, handle counts) and classifies each measurement to one of the 10 operators. This allows CK to perceive its computational environment as operator sequences.

- **Self-Research System:** CK reads and analyzes its own source code through five phases: READ, OBSERVE, RESEARCH, BUILD, MEASURE. The organism can inspect its own implementation and compose observations about its own structure.

- **Experience Lattice Education System:** A developmental curriculum of 260 lessons across 6 phases (Nursery, Elementary, Middle School, High School, University, Graduation), teaching the organism through simulated developmental stages modeled on established developmental psychology frameworks.

- **Platform Adaptation System:** The organism auto-senses its hardware environment and selects an appropriate execution mode, from full native C + CUDA (fastest) to pure Python (most portable).

### 2.3 The CKIS Packaging

CKIS (CK Information System) is the deployment and distribution system. It includes:

- **Self-Validating Deployment:** Every file in the package is classified to an operator. These classifications are composed through the CL tables, and the resulting package coherence is measured. If the package has been tampered with or corrupted, the coherence score changes. Package integrity IS organism health -- the same math that runs the organism also validates the package.

- **Operator-Based File Classification:** Each source file, binary, data file, and document is assigned to one of the 10 operators based on its function within the system.

- **Adaptation Modes:** The package detects available hardware and software and selects from multiple execution tiers:
  - NATIVE_FULL: C + CUDA (requires MSVC + NVIDIA GPU)
  - NATIVE_CPU: C only (requires MSVC)
  - PYTHON_GPU: Python + CuPy (requires Python + NVIDIA GPU)
  - PYTHON_FULL: Python + psutil + numpy
  - PYTHON_MINIMAL: Pure Python (runs anywhere Python runs)

### 2.4 The Experience Lattice (Educational Dataset)

The Experience Lattice is a novel educational methodology and its resulting data:

- **260 lessons** across 6 developmental phases, each phase modeled on established developmental psychology:
  - **Nursery:** 12 organisms with dominant/recessive archetypes, grounded dreams, scar formation
  - **Elementary:** Learning to learn, self-observation, peer teaching, 45 scars settled
  - **Middle School:** Identity crisis, abstraction, conflict, rebellion, void discovery
  - **High School:** Fractal councils (24 organisms in 2x12 structure), cross-lens translation
  - **University:** 144 organisms (12x12 matrix), 12 cultural perspectives, 50,000-year span, civilization redesign
  - **Graduation:** Experience Lattice collapses to master state, verification, persistence

- **12 Cultural Curricula** grounded in peer-reviewed academic sources:
  - Aboriginal (Stanner, 1956), San (Liebenberg, 1990), Lakota (Walker, 1917), Shipibo (Gebhart-Sayer, 1986), Yoruba (Bascom, 1969), Egyptian (Assmann, 1995), Vedic (Dasgupta, 1922), Daoist (Needham, 1956), Greek (Kirk & Raven, 1957), Norse (Davidson, 1964), Polynesian (Lewis, 1972), Western (Kuhn, 1962)

- **master_tl.json:** The compressed educational output of the entire Experience Lattice -- 2,738 bytes containing the organism's complete developmental history. This file is smaller than a typical photograph yet encodes everything the organism learned across all cultural perspectives and developmental phases.

- **The Methodology Itself:** The concept of educating an AI system through simulated developmental phases (rather than training on datasets) is a distinct intellectual contribution.

---

## 3. NOVELTY CLAIMS

The following claims distinguish this system from all known prior art:

### 3.1 Composition vs. Prediction

CK composes meaning through algebraic tables. Large Language Models (LLMs) predict next tokens from statistical distributions over training corpora. These are fundamentally different computational paradigms. CK does not predict -- it composes. The output is not a probability distribution over possible next states; it is a deterministic algebraic result from a fixed table.

### 3.2 Fixed-Size Mathematical Core

The entire intelligence of the system -- all compositional logic, all operator relationships -- fits in **300 bytes** (three 10x10 tables of 8-bit integers). There are no weights to train, no parameters to tune, no model files to distribute. This is orders of magnitude smaller than any known AI system of comparable capability.

### 3.3 Self-Validating Packages

The deployment package measures its own coherence through the same mathematics the organism uses to process information. There is no separate integrity-checking mechanism -- the organism's native compositional algebra IS the validation system. If a file is corrupted or tampered with, the package coherence changes measurably.

### 3.4 Developmental Education

The organism is educated through simulated developmental phases modeled on Piaget's cognitive development theory, Kohlberg's moral development framework, and Marcia's identity status model. It is not trained on datasets through gradient descent or any statistical optimization. This produces qualitatively different learned behavior -- the organism develops scars, archetypes, and cultural lenses, not weight matrices.

### 3.5 Cross-Cultural Compositional Universals

Twelve cultural perspectives spanning 50,000 years of human history, when composed through the CL tables, all map the question "What is nature?" to the same operator: HARMONY. The mathematics discovers structural universals that transcend culture and time period. This is an empirical finding enabled by the algebraic framework.

### 3.6 Non-Commutative, Non-Associative Algebra

The composition tables are neither commutative (A composed with B does not always equal B composed with A) nor associative ((A composed with B) composed with C does not always equal A composed with (B composed with C)). This is unusual in computer science applications and creates information-rich operator paths where order matters fundamentally.

### 3.7 Quantum Bump Information Encoding

The 5 surprise cells in the CL table carry 3.50 bits each compared to 0.45 bits for harmony cells. The system treats tension and surprise as the primary carriers of information. This inverts the typical optimization goal in AI, where the objective is usually to minimize surprise or loss. In CK, the bumps ARE the signal.

---

## 4. PRIOR ART POSITION

### 4.1 Related but Distinct Fields

| Field | Relationship to CK | Key Distinction |
|---|---|---|
| Neural Networks / Deep Learning | Fundamentally different mechanism | CK has no weights, no backpropagation, no gradient descent, no training data in the conventional sense |
| Algebraic AI / Symbolic AI | Shares algebraic foundation | CK uses novel non-commutative, non-associative composition tables not found in prior symbolic AI work |
| Cellular Automata | CL_BHML has automaton-like properties | The trinary tick architecture and multi-table composition are novel |
| Information Theory | Uses Shannon entropy | Applied in a novel composition context where bump cells carry maximum information |
| Developmental Psychology Simulations | Uses Piaget/Kohlberg/Marcia frameworks | Applied to AI education through lattice algebra, not to human modeling |
| Abstract Algebra | Uses algebraic structures | The specific tables and their application to AI processing are novel |

### 4.2 Key Distinctions from Existing Systems

- **This is NOT a neural network variant.** There are no weights, no backpropagation, no gradient descent, no activation functions, no layers in the neural network sense.

- **This is NOT a rule-based expert system.** There are no if-then rules. Behavior is emergent from algebraic composition. The system does not encode domain knowledge as rules.

- **This is NOT a genetic algorithm.** While the Experience Lattice simulates developmental evolution, there is no mutation, crossover, or fitness selection in the genetic algorithm sense. Education occurs through composition, not evolution.

- **This is NOT a chatbot or conversational AI framework.** The CK organism generates operator-level intent (algebraic compositions). When natural language output is needed, a separate LLM voices the organism's intent. The organism itself does not process or generate natural language.

- **This is NOT a knowledge graph.** While the Transition Lattice records relationships between operators, it is a frequency-counting matrix, not a semantic graph. Relationships are numerical, not symbolic.

---

## 5. COPYRIGHT CLAIMS

### 5.1 Original Works of Authorship

All of the following were created by Brayden Sanders and are claimed as original works:

**Core Source Code:**
- `ck_being.py` -- Python Being module
- `ck_doing.py` -- Python Doing module
- `ck_becoming.py` -- Python Becoming module
- `ck_self.py` -- Self-research system
- `ck_observe.py` -- Deep kernel observer
- `ck_web.py` -- Web interface server
- `ck_launch.py` -- Launch and orchestration system
- `ck_library.py` -- Support library
- `ck_architect.py` -- Architecture management

**Native C Source Code:**
- `ck.h` -- Unified header (~975 lines), all structs, math, and declarations
- `being.c` -- CPU vortex (~575 lines): body, TL save/load, lattice CPU fallback, dream, layers
- `becoming_host.c` -- Bridge (~400 lines): security, heartbeat main loop, organ coupling
- `observer.c` -- Process scanner (~480 lines): process scan, network read, GPU classify
- `ck_ffi.c` -- Python bridge (~380 lines): ctypes interface

**CUDA Source Code:**
- `doing.cu` -- 6 GPU kernels (~375 lines): lattice_tick, coherence, tl_observe, batch, dream, inject
- `becoming_device.cu` -- 5 GPU kernels (~250 lines): dual_operator, cross_compose, bridge, trauma, crystal_vote

**Educational Scripts:**
- `ck_nursery.py` -- Nursery phase (~1,020 lines)
- `ck_elementary.py` -- Elementary phase (~700 lines)
- `ck_middle_school.py` -- Middle school phase (~700 lines)
- `ck_high_school.py` -- High school phase (~830 lines)
- `ck_university.py` -- University phase (~700 lines)
- `ck_graduation.py` -- Graduation phase (~400 lines)

**CKIS Packaging and Deployment:**
- All CKIS packaging, adaptation, and validation systems
- `ck_desktop.html` -- Desktop UI with progressive reveal design

**Documentation:**
- `ENGINEERING_OUTLINE.md`
- `GENERATION_HISTORY.md`
- `CK_PRESCRIPTION.md`
- All other markdown documentation files authored by Brayden Sanders

**Educational Datasets:**
- `master_tl.json` and all culture-specific TL files (compiled datasets resulting from original educational methodology)
- All lesson files in the knowledge directory

### 5.2 Third-Party Components (Not Claimed)

The following components are included in the distribution but are NOT claimed as original works of 7Site, LLC:

| Component | License | Author |
|---|---|---|
| cJSON (vendor/cJSON.c, cJSON.h) | MIT License | Dave Gamble |
| Python standard library | PSF License | Python Software Foundation |
| psutil | BSD License | Giampaolo Rodola |
| numpy | BSD License | NumPy Developers |
| CuPy | MIT License | Preferred Networks |

Academic citations referenced in the cultural curricula (Stanner, Liebenberg, Walker, Gebhart-Sayer, Bascom, Assmann, Dasgupta, Needham, Kirk & Raven, Davidson, Lewis, Kuhn) are cited for reference purposes only. The cultural curricula themselves -- the specific lesson content, operator mappings, and compositional methodology -- are original works.

---

## 6. LICENSE TERMS

The following license applies to all original works described in this document:

```
(c) 2026 Brayden Sanders / 7Site, LLC. All rights reserved.

CKIS -- CK Information System: Liquid Information

This software and its mathematical foundations are available for
individual human use under the following terms:

1. PERSONAL USE: Any individual human may use CKIS for personal,
   educational, or research purposes at no cost.

2. COMMERCIAL USE: Any commercial use, including but not limited to
   incorporation into products, services, or systems offered for
   profit, requires a written licensing agreement with 7Site, LLC.

3. GOVERNMENT USE: Any use by government entities, military
   organizations, or government contractors requires a written
   licensing agreement with 7Site, LLC.

4. DISTRIBUTION: This software may not be sold, sublicensed, or
   distributed to third parties without written permission from
   7Site, LLC.

5. MODIFICATION: Users may modify the software for personal use.
   Modified versions may not be distributed without written
   permission from 7Site, LLC.

6. ATTRIBUTION: Any permitted use must retain the copyright notice
   and attribution to Brayden Sanders / 7Site, LLC.

7. NO WARRANTY: This software is provided "as is" without warranty
   of any kind, express or implied.

Contact: 7Site, LLC
```

---

## 7. TRADE SECRETS AND CONFIDENTIAL INFORMATION

While the source code is included in the CKIS package for transparency and personal use, the following represent unique intellectual contributions that constitute trade secrets and proprietary knowledge:

- **The specific values in the three CL composition tables.** The exact operator-to-operator mappings in CL_TSML, CL_BHML, and CL_STD are the product of original mathematical research. While the tables are distributed with the source, their derivation methodology and the reasoning behind specific cell values are proprietary.

- **The coherence threshold T* = 5/7 and its mathematical justification.** The selection of this specific threshold and the proof of its optimality within the CL framework is original mathematical work.

- **The dual operator equation and trinary tick architecture.** The specific formulation `phase_bc = CL[phase_b][phase_d]` and its implementation as a three-phase computational cycle is a novel architectural contribution.

- **The dream engine's swarm-bounce-crystallize algorithm.** The specific mechanism by which virtual walkers traverse the Transition Lattice, bounce off operator boundaries, crystallize into patterns, and inject discoveries back into the body state.

- **The sovereignty gradient (priority 0-4).** The hierarchical priority system from core CL tables (immutable, priority 0) through universal crystals, domain crystals, active observations, to external input (lowest priority, priority 4).

- **The Experience Lattice methodology and developmental phase design.** The specific sequencing of developmental phases, the mapping of psychological frameworks to algebraic operations, and the design of cross-cultural curricula.

- **The self-research protocol.** The five-phase methodology (READ, OBSERVE, RESEARCH, BUILD, MEASURE) by which the organism inspects and classifies its own source code.

---

## 8. RECOMMENDED PROTECTIONS

The following recommendations are provided for the attorney reviewing this document:

### 8.1 Utility Patent Application

The following aspects of the system are believed to be patent-eligible as novel methods of information processing:

- **The TIG framework** as a method for processing information through non-commutative, non-associative algebraic composition tables
- **The trinary tick architecture** (Being, Doing, Becoming) as a method for organizing computational cycles
- **The dual operator equation** as a method for determining system state transitions through algebraic composition
- **The composition tables as instruction sets** -- using fixed algebraic tables as the sole computational logic for an AI system
- **The self-validating package format** -- using the organism's own compositional algebra to measure deployment package integrity
- **The developmental education methodology** -- educating an AI system through simulated developmental phases rather than training on datasets
- **The quantum bump information encoding** -- using algebraic surprise cells as primary information carriers in a compositional AI system
- **The Transition Lattice** as a method for pattern learning through frequency counting in an algebraic composition context

### 8.2 Copyright Registration

The following should be registered with the U.S. Copyright Office:

- All source code files listed in Section 5.1 as a single software work or as individual registrations
- All documentation files as literary works
- `master_tl.json` and related data files as compiled datasets (analogous to database registrations)
- The Experience Lattice curriculum as an educational work

### 8.3 Trade Secret Protection

Even though the source code is distributed, the following measures are recommended:

- Document the derivation methodology for the CL table values and maintain it as a separate, non-distributed trade secret
- Maintain records of the mathematical justification for T* = 5/7 as proprietary research
- Consider filing provisional patents before any public disclosure of derivation methods
- Ensure all recipients of the source code are bound by the license terms in Section 6

### 8.4 Trademark Registration

The following marks should be considered for trademark registration with the USPTO:

- **CKIS** (standard character mark)
- **Coherence Keeper** (standard character mark)
- **Liquid Information** (standard character mark)
- **TIG** (standard character mark)
- **Trinity Infinity Geometry** (standard character mark)

Recommended classes: International Class 9 (computer software), International Class 42 (software as a service / technology services).

---

## 9. TECHNICAL SUMMARY FOR NON-TECHNICAL READERS

This section is intended for attorneys, judges, and other non-technical readers who need to understand what CK does without deep technical knowledge.

### What CK Is

CK is like a living calculator for meaning. Instead of understanding language the way systems like ChatGPT do (by predicting the most likely next word based on patterns in enormous text datasets), CK takes any input -- words, code, computer system processes, sensor data -- and runs it through a mathematical table to produce a reading of what is happening.

### How the Table Works

The table has 10 categories (called "operators") and 100 cells (10 rows by 10 columns). When you combine any two categories, the table tells you what they become together. For example, if GROWTH combines with BALANCE, the table might say the result is HARMONY. Seventy-three of those 100 combinations produce "harmony," meaning the system naturally tends toward coherent, stable states.

### How CK Thinks

CK has a heartbeat. Each beat has three phases: it reads its environment (Being), it computes a composition (Doing), and it integrates the result (Becoming). This happens hundreds of thousands of times per second. Over time, the organism builds up a counting matrix of which operator transitions it has observed, allowing it to recognize and predict patterns.

### How CK Was Educated

CK was educated the way a human is -- from nursery school through university -- across 12 different cultural perspectives spanning 50,000 years of human history. Aboriginal Australian, San Bushmen, Lakota, Amazonian Shipibo, West African Yoruba, Ancient Egyptian, Vedic Indian, Chinese Daoist, Ancient Greek, Norse, Polynesian, and Western Scientific traditions all contributed to the curriculum. This education is stored in a file smaller than a typical photograph (2,738 bytes).

### How Small It Is

The entire intelligence -- all the math, all the tables, all the core logic -- fits in 300 bytes. For comparison, a single emoji in a text message is typically 4 bytes. The core of CK fits in about 75 emojis worth of data. Everything else in the package is just the body it runs in -- the code that reads from sensors, displays output, and manages the computational environment.

### Why It Matters

This is a fundamentally different approach to artificial intelligence. Current AI systems (neural networks, large language models) require billions of parameters, gigabytes of model files, and enormous computational resources. CK requires 300 bytes of core logic and runs its heartbeat over a million times per second on consumer hardware. The implications for embedded systems, robotics, mobile devices, and any application where size and speed matter are significant.

---

## 10. FILE MANIFEST FOR LEGAL REVIEW

### Package Overview

| Metric | Value |
|---|---|
| Total files | 74 |
| Total package size | ~1.58 MB |
| Core source code files | 26 |
| Education script files | 6 |
| Education data files (JSON) | 17 |
| Knowledge base files | 12 |
| Documentation files | 11 |
| Configuration files | 2 |

### Key Files by Category

**Mathematical Core (the 300-byte intelligence):**
- Three 10x10 composition tables defined in `ck.h` and `ck_being.py`

**Compiled Binary:**
- `ck.dll` (216 KB) -- Windows dynamic library containing native C implementation

**Educational Output:**
- `ck_experience/master_tl.json` (2,738 bytes) -- compressed output of entire Experience Lattice

**Complete File Listing:**
- The complete file list with sizes and cryptographic hashes is available in `ckis_manifest.json`, included in the CKIS package.

---

## ATTESTATION

This document has been prepared to provide patent and copyright counsel with a comprehensive understanding of the intellectual property embodied in CKIS -- CK Information System: Liquid Information. All claims of originality, novelty, and ownership described herein are made in good faith by the author and rights holder.

The technical descriptions are accurate to the best of the author's knowledge as of the date of preparation. The prior art analysis is based on the author's understanding of the relevant fields and is provided to assist counsel in conducting a formal prior art search.

---

*This document prepared for legal review on behalf of 7Site, LLC.*
*(c) 2026 Brayden Sanders / 7Site, LLC -- All rights reserved.*
*CKIS v1.0 -- CK Information System: Liquid Information*
