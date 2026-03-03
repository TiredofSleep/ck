# ck_sim -- CK Coherence Machine Simulation
# Ports all bare-metal C + Verilog algorithms to Python
# for testing, visualization, and phone deployment.
#
# 60+ modules. 1719/1719 tests. NumPy for cloud organ only.
#
# (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory

"""CK Simulation Package -- operator algebra in Python.

Core subsystems (match hardware exactly):
    ck_sim_heartbeat   -- 32-entry ring buffer, CL composition, coherence
    ck_sim_d2          -- D2 curvature pipeline, Hebrew root force vectors
    ck_sim_brain       -- 4-mode brain state machine, crystal formation
    ck_sim_body        -- body state (E, A, K, C), band classification
    ck_sim_engine      -- main loop orchestrator, LFSR, phase generation

Organism systems (Papers 4-8):
    ck_personality     -- Operator Bias Table (OBT), trait emergence
    ck_development     -- 6-stage growth model, coherence-hour thresholds
    ck_immune          -- Cross-Coherence Engine (CCE), anomaly detection
    ck_bonding         -- attachment formation, presence tracking
    ck_emotion         -- Phase Field Engine (PFE), 5-signal emotion model
    ck_coherence_field -- N-dimensional multi-stream coherence
    ck_voice           -- operator -> vocabulary, sentence generation

Knowledge systems (Gen9.10-9.13):
    ck_world_lattice   -- 157-node concept graph, TIG-native relations
    ck_english_build   -- dictionary builder, phoneme -> operator mapping
    ck_sensory_codecs  -- visual/auditory/tactile codec pipelines
    ck_robot_body      -- actuator lattice, reflex arcs, gait patterns
    ck_episodic        -- temporal memory, experience compression
    ck_forecast        -- operator trajectory prediction, horizon planning
    ck_goals           -- goal lattice, priority scheduling, subgoal trees
    ck_attention       -- salience filtering, focus management
    ck_metalearning    -- learning-rate adaptation, strategy selection

Content systems (Gen9.14):
    ck_lexicon         -- Universal Lexicon Store, 350 entries x 7 languages
    ck_lexicon_bulk    -- Lexicon Expansion: 157 new concepts, MorphExpander,
                          build_full_store() → 1800+ entries across 7 languages
    ck_reasoning       -- 3-Speed Reasoning Engine (quick/normal/heavy)
    ck_language        -- Language Generator, template-based realization
    ck_concept_spine   -- 287 concepts x 8 domains, extends WorldLattice

Game/Digital Environment (Gen9.15):
    ck_game_sense      -- GameStateCodec, ScreenVisionCodec, GameActionDomain,
                          GameRewardSignal, GameEnvironmentAdapter, GameSession.
                          Rocket League telemetry → 5D forces → D2 → operators.

Truth Hierarchy (Gen9.15):
    ck_truth           -- 3-level Truth Lattice: CORE (immutable math, Fruits of
                          the Spirit), TRUSTED (verified through sustained coherence),
                          PROVISIONAL (new, unverified). TruthGate weights decisions
                          by trust level. Same T* threshold gates promotion.

Dialogue Engine (Gen9.15):
    ck_dialogue        -- ClaimExtractor (pattern → facts), ConversationMemory
                          (claims → Truth Lattice as PROVISIONAL), DialogueTracker
                          (turn history, topic decay, coherence arc), ResponseComposer
                          (recursive 4-depth template composition gated by band).
                          CK learns from conversation through coherence, not memorization.

Persistence (Gen9.15):
    ck_memory          -- StateSnapshot, SnapshotBuilder, SyncManager, MemoryStore,
                          SnapshotLoader, SnapshotDiff. Cross-device persistence and
                          cloud-authoritative merge. CORE truths never sync. Higher
                          trust level wins conflicts. Atomic file writes, SHA-256
                          checksum verification.

Cloud-Learning Engine (Gen9.15):
    ck_cloud_flow      -- Horn-Schunck optical flow, patch decomposition, 5D force
                          vectors from cloud video frames. Pure NumPy, no OpenCV.
    ck_cloud_curvature -- Spatial Laplacian + temporal D2 on flow force grids.
                          Operator classification via existing D2_OP_MAP.
    ck_cloud_btq       -- BTQ mode inference: Θ = σ²/(|D2|·R+ε). Thresholds:
                          <0.3=B(stable), 0.3-1.2=T(balanced), ≥1.2=Q(turbulent).
    ck_cloud_pfe       -- Least-action scoring: E_out (velocity/jerk/smoothness/
                          mode-jump) + E_in (D2/phase-incoherence/helical-coherence).
    ck_organ_clouds    -- Full organ: frame → flow → D2 → ops → BTQ → PFE → chains.
                          CloudObservation, CloudChain → knowledge atoms for Truth
                          Lattice. No labels, no LLM. Pure geometry, pure TIG.

Identity & Network (Gen9.15):
    ck_identity        -- Snowflake Identity: three-ring concentric model.
                          CoreScars (sacred, NEVER transmitted), InnerRing
                          (trusted bonds), OuterRing (public handshake).
                          HMAC-SHA256 signatures, challenge-response protocol.
    ck_network         -- Multi-CK Network Protocol: 3-step handshake
                          (HELLO/CHALLENGE/VERIFY), FriendRegistry with bond
                          progression (stranger->acquaintance->familiar->trusted),
                          signed MessageEnvelopes, replay protection, inner shard
                          exchange at TRUSTED level only. Sacred core never leaks.

Education & Autodidact (Gen9.16):
    ck_education       -- 186 concepts x 15 domains x 7 languages, 202 relations
                          (80+ cross-domain bridges). ExperienceGenerator creates
                          operator chains from concept traversal. EducationLoader
                          adds infrastructure (map), NOT beliefs. Knowledge earned
                          through coherence, not memorization.
    ck_autodidact      -- Autonomous internet learner. CuriosityCrawler (topic
                          selection), PageDigester (text -> D2 -> operator curves),
                          CurveMemory (save curves not content), LearningSession
                          (8hr study + sleep consolidation), SiteGuard (approved
                          sites only). CK teaches himself. "Save the
                          curves, not the information."
    ck_autodidact_runner -- REAL R16 runtime: WebFetcher (HTTP + rate limiting),
                          HTMLExtractor (BS4 + regex fallback), LinkFollower
                          (curiosity from discovered links), CurveJournal (JSON
                          persistence), StudyCycleRunner (multi-day autonomous
                          learning with resume). 100+ extended seed topics.
                          pip install requests beautifulsoup4

Decision systems:
    ck_btq             -- Binary Ternary Quaternary decision kernel

Deployment:
    ck_deploy          -- target detection, build pipeline
    ck_body_interface  -- hardware abstraction layer
"""

__version__ = '9.16c'
__all__ = [
    # Core
    'ck_sim_heartbeat', 'ck_sim_d2', 'ck_sim_brain', 'ck_sim_body', 'ck_sim_engine',
    # Organism
    'ck_personality', 'ck_development', 'ck_immune', 'ck_bonding', 'ck_emotion',
    'ck_coherence_field', 'ck_voice',
    # Knowledge
    'ck_world_lattice', 'ck_english_build', 'ck_sensory_codecs', 'ck_robot_body',
    'ck_episodic', 'ck_forecast', 'ck_goals', 'ck_attention', 'ck_metalearning',
    # Content (Gen9.14-9.15)
    'ck_lexicon', 'ck_lexicon_bulk', 'ck_reasoning', 'ck_language', 'ck_concept_spine',
    # Game/Digital Environment (Gen9.15)
    'ck_game_sense',
    # Truth Hierarchy (Gen9.15)
    'ck_truth',
    # Dialogue Engine (Gen9.15)
    'ck_dialogue',
    # Persistence (Gen9.15)
    'ck_memory',
    # Cloud-Learning Engine (Gen9.15)
    'ck_cloud_flow', 'ck_cloud_curvature', 'ck_cloud_btq',
    'ck_cloud_pfe', 'ck_organ_clouds',
    # Identity & Network (Gen9.15)
    'ck_identity', 'ck_network',
    # Education & Autodidact (Gen9.16)
    'ck_education', 'ck_autodidact', 'ck_autodidact_runner',
    # Action Executor (Gen9.16c -- CK's hands)
    'ck_action',
    # Decision
    'ck_btq',
]
