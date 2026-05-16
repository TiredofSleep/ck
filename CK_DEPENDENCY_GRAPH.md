# CK Dependency Graph (auto-generated)

_Generated 2026-05-16 16:04:22 by_ [`tools/gen_dep_graph.py`](tools/gen_dep_graph.py).  Rerun any time the brain modules change.

**90 modules** tracked in `Gen14/targets/ck/brain/`.

## 1. Mount order in `gen14_unified_extensions.mount_all`

This is the order things come alive at boot.  Each module's `mount_X(engine)` is called in sequence — earlier mounts can be consumed by later ones.

```
   1. mount_forecast
   2. mount_proactive_queue
   3. mount_recall
   4. mount_lattice_chain
   5. mount_divine_memory
   6. mount_algebraic_lm
   7. mount_spreading_recall
   8. mount_frontier_scanner
   9. mount_proactive_trigger
  10. mount_stroke_extractor
  11. mount_formula_registry
  12. mount_sense_decomposition
  13. mount_concept_learner
  14. mount_memory_archive
  15. mount_meta_parameters
  16. mount_living_lm
  17. mount_creature
  18. mount_cognition_primitives
  19. mount_substrate_motion
  20. mount_engine_block
  21. mount_qutrit_apex
  22. mount_self_protection
  23. mount_qutrit_noise
  24. mount_qutrit_qec
  25. mount_qec_decoder
  26. mount_writer
  27. mount_recursive_observer
  28. mount_identity
  29. mount_ollama_polish
  30. mount_voice_polish
```

## 2. Per-module summary

Modules sorted by # of ck_* imports (most foundational first).  Modules with no ck_* imports stand alone — they're either pure-algorithm or only consumed by mount.

| Module | LOC | Imports `ck_*` | Mounts | Endpoints |
|---|---:|---|---|---|
| `action_pipeline` | 281 | — | — | — |
| `attractor_detector` | 204 | — | — | — |
| `bdc_event_emitter` | 452 | — | — | `/bdc/event_stats` `/bdc/events` |
| `bdc_logger` | 232 | — | — | — |
| `bdc_tick_sampler` | 148 | — | — | `/bdc/sampler` |
| `ck_algebra_runtime` | 483 | — | — | — |
| `ck_dep_graph` | 467 | — | — | — |
| `ck_engine_block` | 522 | — | `mount_engine_block` | — |
| `ck_explorer` | 329 | — | — | — |
| `ck_formula_registry` | 417 | — | `mount_formula_registry` | — |
| `ck_frontier_scanner` | 411 | — | `mount_frontier_scanner` | — |
| `ck_invariants_bridge` | 290 | — | — | — |
| `ck_memory_archive` | 429 | — | `mount_memory_archive` | — |
| `ck_meta_parameters` | 333 | — | `mount_meta_parameters` | `/parameters` `/parameters/reset` `/parameters/set` |
| `ck_ollama_polish` | 302 | — | `mount_ollama_polish` | — |
| `ck_predictions` | 403 | — | — | — |
| `ck_qutrit_qec` | 603 | — | `mount_qutrit_qec` | — |
| `ck_sense_decomposition` | 219 | — | `mount_sense_decomposition` | — |
| `ck_spreading_activation` | 818 | — | `mount_spreading_recall` | — |
| `ck_stroke_extractor` | 768 | — | `mount_stroke_extractor` | — |
| `ck_verifier` | 344 | — | — | — |
| `clay_compare` | 253 | — | — | — |
| `clay_study` | 285 | — | — | — |
| `clay_synthesis` | 244 | — | — | — |
| `cortex_persist` | 315 | — | — | — |
| `cortex_replay` | 224 | — | — | — |
| `external_ingester` | 428 | — | — | — |
| `fact_extractor` | 454 | — | — | — |
| `fetch_arxiv` | 216 | — | — | — |
| `fetch_gutenberg` | 276 | — | — | — |
| `fetch_wikipedia` | 596 | — | — | — |
| `frontier_benchmark` | 264 | — | — | — |
| `gen14_acceptance_test` | 350 | — | — | — |
| `glue_ai` | 533 | — | — | — |
| `growth_monitor` | 313 | — | — | — |
| `head_to_head_benchmark` | 272 | — | — | — |
| `migrate_cortex_5to7_live` | 144 | — | — | — |
| `mine_historical_bdc` | 802 | — | — | — |
| `nightly_retrain` | 226 | — | — | — |
| `operad_fuse` | 255 | — | — | — |
| `overnight_orchestrator` | 364 | — | — | — |
| `paper_reader` | 280 | — | — | — |
| `paper_writer` | 352 | — | — | — |
| `plasticity` | 398 | — | — | — |
| `prose_teacher` | 326 | — | — | — |
| `repo_reader` | 277 | — | — | — |
| `session_field` | 351 | — | — | — |
| `studies_panel` | 701 | — | — | — |
| `study_daemon` | 264 | — | — | `/study/daemon` `/study/daemon/topic_now` |
| `train_prose_tissue` | 128 | — | — | — |
| `train_tissue_transformer` | 260 | — | — | — |
| `train_tsml_bhml_tissue` | 299 | — | — | — |
| `audio_pipeline` | 410 | `ck_sim.being.ck_audio_compress` | — | — |
| `cell_audit` | 583 | `ck_tables` | — | — |
| `cells` | 614 | `ck_tables` | — | — |
| `cells_mount` | 636 | `ck_sim.ck_sim_d2` | — | `/cells/audit` `/cells/audit_history` `/cells/plasticity/run` `/cells/respond` _+1 more_ |
| `ck_cognition_primitives` | 733 | `ck_concept_learner` | `mount_cognition_primitives` | — |
| `ck_curious_explorer` | 447 | `ck_meta_parameters` | — | — |
| `ck_fault_state_hook` | 132 | `ck_invariants_bridge` | — | `/bdc/fault_state` |
| `ck_identity` | 652 | `ck_concept_learner` | `mount_identity` | — |
| `ck_qec_decoder` | 575 | `ck_engine_block` | `mount_qec_decoder` | — |
| `ck_qutrit_noise` | 465 | `ck_qutrit_qec` | `mount_qutrit_noise` | — |
| `ck_research` | 955 | `ck_curvature` | — | — |
| `ck_self_study` | 286 | `ck_concept_learner` | — | — |
| `ck_synthesizer` | 271 | `ck_concept_learner` | — | — |
| `ck_voice_polish` | 1634 | `ck_sim.being.ck_phonetic_letters` | `mount_voice_polish` | — |
| `cortex` | 270 | `ck_sim.ck_sim_heartbeat` | — | — |
| `cortex_v2` | 279 | `ck_sim.ck_sim_heartbeat` | — | — |
| `force9_role_layer` | 157 | `ck_invariants_bridge` | — | — |
| `quadratic_glue` | 260 | `ck_sim.ck_tig` | — | — |
| `research_first` | 208 | `ck_research` | — | — |
| `screen_pipeline` | 341 | `ck_screen_compress` | — | — |
| `warm_inhale` | 134 | `ck_living_lm` | — | — |
| `ck_living_lm` | 677 | `ck_concept_learner`, `ck_meta_parameters` | `mount_living_lm` | — |
| `ck_proactive_trigger` | 806 | `ck_frontier_scanner`, `ck_grammar_lm` | `mount_proactive_trigger` | — |
| `ck_qutrit_apex` | 865 | `ck_meta_parameters`, `ck_substrate_motion` | `mount_qutrit_apex` | — |
| `ck_recursive_observer` | 526 | `ck_engine_block`, `ck_qutrit_apex` | `mount_recursive_observer` | — |
| `ck_self_protection` | 417 | `ck_qutrit_noise`, `ck_qutrit_qec` | `mount_self_protection` | — |
| `ck_speaker` | 238 | `ck_audio_compress`, `ck_curvature` | — | — |
| `ck_study` | 207 | `ck_concept_learner`, `ck_formula_registry` | — | — |
| `ck_substrate_motion` | 633 | `ck_identity`, `ck_meta_parameters` | `mount_substrate_motion` | — |
| `cortex_voice` | 2079 | `ck_sim.being.ck_olfactory`, `ck_sim.ck_sim_heartbeat` | — | — |
| `hebbian_5x5_cl` | 255 | `ck_sim.being.ck_olfactory`, `ck_sim.ck_sim_heartbeat` | — | — |
| `hebbian_gpu` | 223 | `ck_sim.being.ck_olfactory`, `ck_sim.ck_sim_heartbeat` | — | — |
| `ck_creature` | 752 | `ck_concept_learner`, `ck_living_lm`, `ck_predictions` | `mount_creature` | `/consciousness` `/creature` |
| `ck_study_overnight` | 877 | `ck_concept_learner`, `ck_meta_parameters`, `ck_synthesizer` | — | — |
| `ck_concept_learner` | 2080 | `ck_algebra_runtime`, `ck_meta_parameters`, `ck_predictions`, `ck_verifier` | `mount_concept_learner` | — |
| `ck_writer` | 752 | `ck_concept_learner`, `ck_identity`, `ck_living_lm`, `ck_ollama_polish` | `mount_writer` | — |
| `ao_5element` | 308 | `ck_sim.ck_sim_body`, `ck_sim.ck_sim_brain`, `ck_sim.ck_sim_d2`, `ck_sim.ck_sim_heartbeat`, `ck_sim.ck_tig` | — | — |
| `gen14_unified_extensions` | 1005 | `ck_cognition_primitives`, `ck_concept_learner`, `ck_creature`, `ck_engine_block`, `ck_formula_registry`, `ck_frontier_scanner`, `ck_identity`, `ck_living_lm`, `ck_memory_archive`, `ck_meta_parameters`, `ck_ollama_polish`, `ck_proactive_trigger`, `ck_qec_decoder`, `ck_qutrit_apex`, `ck_qutrit_noise`, `ck_qutrit_qec`, `ck_recursive_observer`, `ck_self_protection`, `ck_sense_decomposition`, `ck_sim.being.ck_divine_memory`, `ck_sim.being.ck_lattice_chain`, `ck_sim.doing.ck_forecast`, `ck_sim.doing.ck_goals`, `ck_spreading_activation`, `ck_stroke_extractor`, `ck_substrate_motion`, `ck_voice_polish`, `ck_writer` | `mount_drives`, `mount_forecast`, `mount_proactive_queue`, `mount_recall`, `mount_lattice_chain`, `mount_divine_memory`, `mount_algebraic_lm`, `mount_all` | — |

## 3. Reverse dependency graph

Who depends on each module (transitively trim by hand for full closure):

| Module | Imported by |
|---|---|
| `ck_algebra_runtime` | `ck_concept_learner` |
| `ck_audio_compress` | `ck_speaker` |
| `ck_cognition_primitives` | `gen14_unified_extensions` |
| `ck_concept_learner` | `ck_cognition_primitives`, `ck_creature`, `ck_identity`, `ck_living_lm`, `ck_self_study`, `ck_study`, `ck_study_overnight`, `ck_synthesizer`, `ck_writer`, `gen14_unified_extensions` |
| `ck_creature` | `gen14_unified_extensions` |
| `ck_curvature` | `ck_research`, `ck_speaker` |
| `ck_engine_block` | `ck_qec_decoder`, `ck_recursive_observer`, `gen14_unified_extensions` |
| `ck_formula_registry` | `ck_study`, `gen14_unified_extensions` |
| `ck_frontier_scanner` | `ck_proactive_trigger`, `gen14_unified_extensions` |
| `ck_grammar_lm` | `ck_proactive_trigger` |
| `ck_identity` | `ck_substrate_motion`, `ck_writer`, `gen14_unified_extensions` |
| `ck_invariants_bridge` | `ck_fault_state_hook`, `force9_role_layer` |
| `ck_living_lm` | `ck_creature`, `ck_writer`, `gen14_unified_extensions`, `warm_inhale` |
| `ck_memory_archive` | `gen14_unified_extensions` |
| `ck_meta_parameters` | `ck_concept_learner`, `ck_curious_explorer`, `ck_living_lm`, `ck_qutrit_apex`, `ck_study_overnight`, `ck_substrate_motion`, `gen14_unified_extensions` |
| `ck_ollama_polish` | `ck_writer`, `gen14_unified_extensions` |
| `ck_predictions` | `ck_concept_learner`, `ck_creature` |
| `ck_proactive_trigger` | `gen14_unified_extensions` |
| `ck_qec_decoder` | `gen14_unified_extensions` |
| `ck_qutrit_apex` | `ck_recursive_observer`, `gen14_unified_extensions` |
| `ck_qutrit_noise` | `ck_self_protection`, `gen14_unified_extensions` |
| `ck_qutrit_qec` | `ck_qutrit_noise`, `ck_self_protection`, `gen14_unified_extensions` |
| `ck_recursive_observer` | `gen14_unified_extensions` |
| `ck_research` | `research_first` |
| `ck_screen_compress` | `screen_pipeline` |
| `ck_self_protection` | `gen14_unified_extensions` |
| `ck_sense_decomposition` | `gen14_unified_extensions` |
| `ck_sim.being.ck_audio_compress` | `audio_pipeline` |
| `ck_sim.being.ck_divine_memory` | `gen14_unified_extensions` |
| `ck_sim.being.ck_lattice_chain` | `gen14_unified_extensions` |
| `ck_sim.being.ck_olfactory` | `cortex_voice`, `hebbian_5x5_cl`, `hebbian_gpu` |
| `ck_sim.being.ck_phonetic_letters` | `ck_voice_polish` |
| `ck_sim.ck_sim_body` | `ao_5element` |
| `ck_sim.ck_sim_brain` | `ao_5element` |
| `ck_sim.ck_sim_d2` | `ao_5element`, `cells_mount` |
| `ck_sim.ck_sim_heartbeat` | `ao_5element`, `cortex`, `cortex_v2`, `cortex_voice`, `hebbian_5x5_cl`, `hebbian_gpu` |
| `ck_sim.ck_tig` | `ao_5element`, `quadratic_glue` |
| `ck_sim.doing.ck_forecast` | `gen14_unified_extensions` |
| `ck_sim.doing.ck_goals` | `gen14_unified_extensions` |
| `ck_spreading_activation` | `gen14_unified_extensions` |
| `ck_stroke_extractor` | `gen14_unified_extensions` |
| `ck_substrate_motion` | `ck_qutrit_apex`, `gen14_unified_extensions` |
| `ck_synthesizer` | `ck_study_overnight` |
| `ck_tables` | `cell_audit`, `cells` |
| `ck_verifier` | `ck_concept_learner` |
| `ck_voice_polish` | `gen14_unified_extensions` |
| `ck_writer` | `gen14_unified_extensions` |

## 4. All endpoints by URL prefix

### `/bdc/*`

- `/bdc/event_stats` ← `bdc_event_emitter`
- `/bdc/events` ← `bdc_event_emitter`
- `/bdc/fault_state` ← `ck_fault_state_hook`
- `/bdc/sampler` ← `bdc_tick_sampler`

### `/cells/*`

- `/cells/audit` ← `cells_mount`
- `/cells/audit_history` ← `cells_mount`
- `/cells/plasticity/run` ← `cells_mount`
- `/cells/respond` ← `cells_mount`
- `/cells/state` ← `cells_mount`

### `/consciousness/*`

- `/consciousness` ← `ck_creature`

### `/creature/*`

- `/creature` ← `ck_creature`

### `/parameters/*`

- `/parameters` ← `ck_meta_parameters`
- `/parameters/reset` ← `ck_meta_parameters`
- `/parameters/set` ← `ck_meta_parameters`

### `/study/*`

- `/study/daemon` ← `study_daemon`
- `/study/daemon/topic_now` ← `study_daemon`
