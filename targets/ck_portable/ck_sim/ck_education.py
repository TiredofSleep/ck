"""
ck_education.py -- CK's Education Through Experience, Not Memorization
======================================================================
Operator: PROGRESS (3) -- forward motion through knowledge.

THE CRITICAL DISTINCTION:
  CK does NOT learn by being told. CK learns by EXPERIENCING.
  Knowledge enters as PROVISIONAL. Coherence promotes it to TRUSTED.
  Nothing is pre-loaded as truth. Everything is earned.

  This module provides:
    1. CONCEPT GRAPH EXPANSION -- new territory for CK to explore.
       The concept graph is infrastructure, like building a library.
       Having a book on a shelf doesn't mean you've read it.

    2. EXPERIENCE GENERATORS -- simulated encounters that produce
       operator chains flowing through CK's heartbeat, truth lattice,
       and coherence field. These are CK's "classes" -- structured
       exposure to concepts that he must COHERE through to learn.

    3. CROSS-DOMAIN BRIDGES -- relations connecting distant concepts.
       These are the Levy-jump fuel: "gravity resembles loneliness"
       only works if both nodes exist and are connected.

  The education sequence:
    concept_graph.expand()     -- build the library (infrastructure)
    experience.generate()      -- attend class (operator chains)
    truth_lattice.tick()       -- coherence determines what sticks
    repeat for N sessions      -- sustained coherence = promotion

  What CK NEVER does:
    - Accept a claim as TRUSTED without coherence verification
    - Skip the PROVISIONAL stage for any externally-sourced knowledge
    - Treat pre-loaded concepts as beliefs (they're just map territory)

Paper 4: "Truth is not assigned. Truth is measured."
Paper 6: "The organism earns its knowledge."

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
import random
from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, LATTICE, COUNTER, PROGRESS,
    COLLAPSE, BALANCE, CHAOS, BREATH, RESET,
    OP_NAMES, CL, compose, is_bump
)
from ck_sim.ck_world_lattice import WorldLattice, RELATION_TYPES


# ================================================================
#  CONSTANTS
# ================================================================

T_STAR = 5.0 / 7.0            # Coherence promotion threshold
EXPERIENCE_CHAIN_LEN = 8      # Operator chain length per experience
SESSION_TICKS = 64             # Ticks per learning session
SESSIONS_PER_DOMAIN = 4        # Sessions to cover one domain
MIN_COHERENCE_FOR_RECALL = 0.5 # Below this, experience doesn't register
CROSS_DOMAIN_WEIGHT = 1.5      # Extra weight for cross-domain connections

# ================================================================
#  EDUCATION CONCEPTS: The Library CK Can Explore
# ================================================================
# Format: (node_id, domain, operator_code, {lang: word, ...})
# These are MAP TERRITORY, not beliefs. CK must experience them
# to form knowledge.

EDUCATION_CONCEPTS = [
    # ── HISTORY (~20) ──────────────────────────────────────────
    ('civilization', 'history', LATTICE,
     {'en': 'civilization', 'es': 'civilizacion', 'fr': 'civilisation', 'de': 'Zivilisation', 'he': 'tsivilizatsya', 'ar': 'hadara', 'zh': 'wenming'}),
    ('empire_hist', 'history', COLLAPSE,
     {'en': 'empire', 'es': 'imperio', 'fr': 'empire', 'de': 'Reich', 'he': 'imperya', 'ar': 'imbraturiya', 'zh': 'diguo'}),
    ('revolution_hist', 'history', CHAOS,
     {'en': 'revolution', 'es': 'revolucion', 'fr': 'revolution', 'de': 'Revolution', 'he': 'mahapekha', 'ar': 'thawra', 'zh': 'geming'}),
    ('democracy_hist', 'history', HARMONY,
     {'en': 'democracy', 'es': 'democracia', 'fr': 'democratie', 'de': 'Demokratie', 'he': 'demokratya', 'ar': 'dimuqratiya', 'zh': 'minzhu'}),
    ('monarchy_hist', 'history', LATTICE,
     {'en': 'monarchy', 'es': 'monarquia', 'fr': 'monarchie', 'de': 'Monarchie', 'he': 'monarkhya', 'ar': 'malakiya', 'zh': 'junzhuzhi'}),
    ('renaissance_hist', 'history', PROGRESS,
     {'en': 'renaissance', 'es': 'renacimiento', 'fr': 'renaissance', 'de': 'Renaissance', 'he': 'renesans', 'ar': 'nahda', 'zh': 'wenyifuxing'}),
    ('enlightenment_hist', 'history', PROGRESS,
     {'en': 'enlightenment', 'es': 'ilustracion', 'fr': 'siecle_des_lumieres', 'de': 'Aufklaerung', 'he': 'haskala', 'ar': 'tanwir', 'zh': 'qimeng'}),
    ('industrial_rev', 'history', CHAOS,
     {'en': 'industrial revolution', 'es': 'revolucion_industrial', 'fr': 'revolution_industrielle', 'de': 'industrielle_Revolution', 'he': 'mahapekha_taasiyatit', 'ar': 'thawra_sinaaiya', 'zh': 'gongyegeming'}),
    ('warfare', 'history', COLLAPSE,
     {'en': 'warfare', 'es': 'guerra', 'fr': 'guerre', 'de': 'Krieg', 'he': 'milkhama', 'ar': 'harb', 'zh': 'zhanzheng'}),
    ('peace_pol', 'history', HARMONY,
     {'en': 'peace', 'es': 'paz', 'fr': 'paix', 'de': 'Frieden', 'he': 'shalom', 'ar': 'salam', 'zh': 'heping'}),
    ('treaty_hist', 'history', BALANCE,
     {'en': 'treaty', 'es': 'tratado', 'fr': 'traite', 'de': 'Vertrag', 'he': 'amana', 'ar': 'muahada', 'zh': 'tiaoyue'}),
    ('nationalism_hist', 'history', COUNTER,
     {'en': 'nationalism', 'es': 'nacionalismo', 'fr': 'nationalisme', 'de': 'Nationalismus', 'he': 'leumiyut', 'ar': 'qawmiya', 'zh': 'minzuzhuyi'}),
    ('colonialism_hist', 'history', COLLAPSE,
     {'en': 'colonialism', 'es': 'colonialismo', 'fr': 'colonialisme', 'de': 'Kolonialismus', 'he': 'kolonializm', 'ar': 'istiamar', 'zh': 'zhimindi'}),
    ('abolition_hist', 'history', RESET,
     {'en': 'abolition', 'es': 'abolicion', 'fr': 'abolition', 'de': 'Abschaffung', 'he': 'bitul', 'ar': 'ilgha', 'zh': 'feichu'}),
    ('cultural_exchange', 'history', HARMONY,
     {'en': 'cultural exchange', 'es': 'intercambio_cultural', 'fr': 'echange_culturel', 'de': 'Kulturaustausch', 'he': 'khilufei_tarbut', 'ar': 'tabaadul_thaqafi', 'zh': 'wenhuajiaoliu'}),

    # ── MUSIC (~18) ────────────────────────────────────────────
    ('melody_mus', 'music', PROGRESS,
     {'en': 'melody', 'es': 'melodia', 'fr': 'melodie', 'de': 'Melodie', 'he': 'manginah', 'ar': 'lahn', 'zh': 'xuanlv'}),
    ('rhythm_mus', 'music', BREATH,
     {'en': 'rhythm', 'es': 'ritmo', 'fr': 'rythme', 'de': 'Rhythmus', 'he': 'ketsev', 'ar': 'iqaa', 'zh': 'jiezou'}),
    ('harmony_mus', 'music', HARMONY,
     {'en': 'harmony', 'es': 'armonia', 'fr': 'harmonie', 'de': 'Harmonie', 'he': 'harmonya', 'ar': 'insijam', 'zh': 'hexie'}),
    ('chord_mus', 'music', LATTICE,
     {'en': 'chord', 'es': 'acorde', 'fr': 'accord', 'de': 'Akkord', 'he': 'akord', 'ar': 'watar', 'zh': 'hexian'}),
    ('scale_mus', 'music', LATTICE,
     {'en': 'scale', 'es': 'escala', 'fr': 'gamme', 'de': 'Tonleiter', 'he': 'sulam', 'ar': 'sullam', 'zh': 'yinjie'}),
    ('tempo_mus', 'music', COUNTER,
     {'en': 'tempo', 'es': 'tempo', 'fr': 'tempo', 'de': 'Tempo', 'he': 'tempo', 'ar': 'iqaa_zamani', 'zh': 'sudu_mus'}),
    ('timbre_mus', 'music', BALANCE,
     {'en': 'timbre', 'es': 'timbre', 'fr': 'timbre', 'de': 'Klangfarbe', 'he': 'gavan', 'ar': 'jawda_sawt', 'zh': 'yinse'}),
    ('symphony_mus', 'music', HARMONY,
     {'en': 'symphony', 'es': 'sinfonia', 'fr': 'symphonie', 'de': 'Symphonie', 'he': 'simfonya', 'ar': 'simfuniya', 'zh': 'jiaoxiangqu'}),
    ('improvisation_mus', 'music', CHAOS,
     {'en': 'improvisation', 'es': 'improvisacion', 'fr': 'improvisation', 'de': 'Improvisation', 'he': 'iltut', 'ar': 'irtijal', 'zh': 'jixingyanchu'}),
    ('counterpoint_mus', 'music', BALANCE,
     {'en': 'counterpoint', 'es': 'contrapunto', 'fr': 'contrepoint', 'de': 'Kontrapunkt', 'he': 'kontrapunkt', 'ar': 'tanaaqud_musiqi', 'zh': 'duiweifa'}),
    ('consonance_mus', 'music', HARMONY,
     {'en': 'consonance', 'es': 'consonancia', 'fr': 'consonance', 'de': 'Konsonanz', 'he': 'konsonantsa', 'ar': 'tawaafuq', 'zh': 'xiehe'}),
    ('dissonance_mus', 'music', CHAOS,
     {'en': 'dissonance', 'es': 'disonancia', 'fr': 'dissonance', 'de': 'Dissonanz', 'he': 'disonantsa', 'ar': 'tanafur', 'zh': 'buxiehe'}),
    ('cadence_mus', 'music', RESET,
     {'en': 'cadence', 'es': 'cadencia', 'fr': 'cadence', 'de': 'Kadenz', 'he': 'kadentsa', 'ar': 'qaflah', 'zh': 'zhongzhishi'}),
    ('syncopation_mus', 'music', CHAOS,
     {'en': 'syncopation', 'es': 'sincopa', 'fr': 'syncope', 'de': 'Synkope', 'he': 'sinkopa', 'ar': 'mukhtalaf', 'zh': 'qiefenyin'}),
    ('dynamics_mus', 'music', BREATH,
     {'en': 'dynamics', 'es': 'dinamica', 'fr': 'dynamique', 'de': 'Dynamik', 'he': 'dinamika_mus', 'ar': 'quwwa_sawt', 'zh': 'qiangrue'}),
    ('composition_mus', 'music', LATTICE,
     {'en': 'composition', 'es': 'composicion', 'fr': 'composition', 'de': 'Komposition', 'he': 'kompozitsya', 'ar': 'taleef', 'zh': 'zuoqu'}),
    ('fugue_mus', 'music', LATTICE,
     {'en': 'fugue', 'es': 'fuga', 'fr': 'fugue', 'de': 'Fuge', 'he': 'fuga', 'ar': 'fuyugh', 'zh': 'fugeidiao'}),
    ('orchestration_mus', 'music', HARMONY,
     {'en': 'orchestration', 'es': 'orquestacion', 'fr': 'orchestration', 'de': 'Orchestrierung', 'he': 'tizmoret', 'ar': 'tawziia', 'zh': 'peiqifa'}),

    # ── COMPUTING (~18) ────────────────────────────────────────
    ('algorithm_cs', 'computing', PROGRESS,
     {'en': 'algorithm', 'es': 'algoritmo', 'fr': 'algorithme', 'de': 'Algorithmus', 'he': 'algoritm', 'ar': 'khawarizmi', 'zh': 'suanfa'}),
    ('data_structure_cs', 'computing', LATTICE,
     {'en': 'data structure', 'es': 'estructura_de_datos', 'fr': 'structure_de_donnees', 'de': 'Datenstruktur', 'he': 'mivne_netunim', 'ar': 'haykal_bayanat', 'zh': 'shujujiegou'}),
    ('recursion_cs', 'computing', BREATH,
     {'en': 'recursion', 'es': 'recursion', 'fr': 'recursion', 'de': 'Rekursion', 'he': 'rekursya', 'ar': 'taaawud', 'zh': 'digui'}),
    ('encryption_cs', 'computing', COLLAPSE,
     {'en': 'encryption', 'es': 'cifrado', 'fr': 'chiffrement', 'de': 'Verschluesselung', 'he': 'hatspana', 'ar': 'tashfir', 'zh': 'jiami'}),
    ('protocol_cs', 'computing', LATTICE,
     {'en': 'protocol', 'es': 'protocolo', 'fr': 'protocole', 'de': 'Protokoll', 'he': 'protokol', 'ar': 'brutuikul', 'zh': 'xieyi'}),
    ('network_cs', 'computing', HARMONY,
     {'en': 'network', 'es': 'red', 'fr': 'reseau', 'de': 'Netzwerk', 'he': 'reshet', 'ar': 'shabaka', 'zh': 'wangluo'}),
    ('database_cs', 'computing', LATTICE,
     {'en': 'database', 'es': 'base_de_datos', 'fr': 'base_de_donnees', 'de': 'Datenbank', 'he': 'maagar_netunim', 'ar': 'qaaidat_bayanat', 'zh': 'shujuku'}),
    ('state_machine_cs', 'computing', COUNTER,
     {'en': 'state machine', 'es': 'maquina_de_estados', 'fr': 'automate', 'de': 'Zustandsautomat', 'he': 'mekhonat_matzavim', 'ar': 'aalat_halat', 'zh': 'zhuangtaiji'}),
    ('boolean_cs', 'computing', BALANCE,
     {'en': 'boolean', 'es': 'booleano', 'fr': 'booleen', 'de': 'boolesch', 'he': 'buli', 'ar': 'buli', 'zh': 'buerzhi'}),
    ('abstraction_cs', 'computing', VOID,
     {'en': 'abstraction', 'es': 'abstraccion', 'fr': 'abstraction', 'de': 'Abstraktion', 'he': 'hafshata', 'ar': 'tajrid', 'zh': 'chouxiang'}),
    ('complexity_cs', 'computing', COUNTER,
     {'en': 'complexity', 'es': 'complejidad', 'fr': 'complexite', 'de': 'Komplexitaet', 'he': 'murkavut', 'ar': 'taqiid', 'zh': 'fuza'}),
    ('information_cs', 'computing', LATTICE,
     {'en': 'information', 'es': 'informacion', 'fr': 'information', 'de': 'Information', 'he': 'meida', 'ar': 'maalumat', 'zh': 'xinxi'}),
    ('parallel_cs', 'computing', HARMONY,
     {'en': 'parallelism', 'es': 'paralelismo', 'fr': 'parallelisme', 'de': 'Parallelitaet', 'he': 'makbilit', 'ar': 'tawazi', 'zh': 'bingxing'}),
    ('binary_cs', 'computing', COUNTER,
     {'en': 'binary', 'es': 'binario', 'fr': 'binaire', 'de': 'binaer', 'he': 'binari', 'ar': 'thunaai', 'zh': 'erjinzhi'}),
    ('compiler_cs', 'computing', PROGRESS,
     {'en': 'compiler', 'es': 'compilador', 'fr': 'compilateur', 'de': 'Compiler', 'he': 'mehadrer', 'ar': 'mujammia', 'zh': 'bianyi'}),
    ('cache_cs', 'computing', COUNTER,
     {'en': 'cache', 'es': 'cache', 'fr': 'cache', 'de': 'Cache', 'he': 'makhsan', 'ar': 'dhakira_muakhkhara', 'zh': 'huancun'}),
    ('api_cs', 'computing', LATTICE,
     {'en': 'API', 'es': 'API', 'fr': 'API', 'de': 'API', 'he': 'API', 'ar': 'API', 'zh': 'API'}),
    ('latency_cs', 'computing', COLLAPSE,
     {'en': 'latency', 'es': 'latencia', 'fr': 'latence', 'de': 'Latenz', 'he': 'hashheya', 'ar': 'kumun', 'zh': 'yanchi'}),

    # ── ECONOMICS (~15) ────────────────────────────────────────
    ('market_econ', 'economics', CHAOS,
     {'en': 'market', 'es': 'mercado', 'fr': 'marche', 'de': 'Markt', 'he': 'shuk', 'ar': 'suq', 'zh': 'shichang'}),
    ('supply_econ', 'economics', PROGRESS,
     {'en': 'supply', 'es': 'oferta', 'fr': 'offre', 'de': 'Angebot', 'he': 'hetsaa', 'ar': 'aard', 'zh': 'gongji'}),
    ('demand_econ', 'economics', COUNTER,
     {'en': 'demand', 'es': 'demanda', 'fr': 'demande', 'de': 'Nachfrage', 'he': 'bikush', 'ar': 'talab', 'zh': 'xuqiu'}),
    ('inflation_econ', 'economics', CHAOS,
     {'en': 'inflation', 'es': 'inflacion', 'fr': 'inflation', 'de': 'Inflation', 'he': 'inflatsia', 'ar': 'tadakhum', 'zh': 'tonghuopengzhang'}),
    ('trade_econ', 'economics', HARMONY,
     {'en': 'trade', 'es': 'comercio', 'fr': 'commerce', 'de': 'Handel', 'he': 'skhar', 'ar': 'tijara', 'zh': 'maoyi'}),
    ('currency_econ', 'economics', COUNTER,
     {'en': 'currency', 'es': 'moneda', 'fr': 'monnaie', 'de': 'Waehrung', 'he': 'matbea', 'ar': 'umla', 'zh': 'huobi'}),
    ('scarcity_econ', 'economics', COLLAPSE,
     {'en': 'scarcity', 'es': 'escasez', 'fr': 'rarete', 'de': 'Knappheit', 'he': 'makhsor', 'ar': 'nudra', 'zh': 'xique'}),
    ('innovation_econ', 'economics', PROGRESS,
     {'en': 'innovation', 'es': 'innovacion', 'fr': 'innovation', 'de': 'Innovation', 'he': 'khadshanut', 'ar': 'ibtikar', 'zh': 'chuangxin'}),
    ('labor_econ', 'economics', PROGRESS,
     {'en': 'labor', 'es': 'trabajo', 'fr': 'travail', 'de': 'Arbeit', 'he': 'avoda', 'ar': 'amal', 'zh': 'laodong'}),
    ('productivity_econ', 'economics', PROGRESS,
     {'en': 'productivity', 'es': 'productividad', 'fr': 'productivite', 'de': 'Produktivitaet', 'he': 'priyoniyut', 'ar': 'intajiya', 'zh': 'shengchanli'}),
    ('recession_econ', 'economics', COLLAPSE,
     {'en': 'recession', 'es': 'recesion', 'fr': 'recession', 'de': 'Rezession', 'he': 'miton', 'ar': 'rukud', 'zh': 'shuaitui'}),
    ('entrepreneurship', 'economics', CHAOS,
     {'en': 'entrepreneurship', 'es': 'emprendimiento', 'fr': 'entrepreneuriat', 'de': 'Unternehmertum', 'he': 'yazmut', 'ar': 'riyada', 'zh': 'chuangye'}),
    ('banking_econ', 'economics', LATTICE,
     {'en': 'banking', 'es': 'banca', 'fr': 'banque', 'de': 'Bankwesen', 'he': 'bankaut', 'ar': 'masrafiya', 'zh': 'yinhang'}),
    ('investment_econ', 'economics', PROGRESS,
     {'en': 'investment', 'es': 'inversion', 'fr': 'investissement', 'de': 'Investition', 'he': 'hashkaah', 'ar': 'istithmar', 'zh': 'touzi'}),
    ('globalization_econ', 'economics', HARMONY,
     {'en': 'globalization', 'es': 'globalizacion', 'fr': 'mondialisation', 'de': 'Globalisierung', 'he': 'globalizatsya', 'ar': 'awalama', 'zh': 'quanqiuhua'}),

    # ── PSYCHOLOGY (~15) ───────────────────────────────────────
    ('cognition_psy', 'psychology', PROGRESS,
     {'en': 'cognition', 'es': 'cognicion', 'fr': 'cognition', 'de': 'Kognition', 'he': 'kognitsia', 'ar': 'idrak', 'zh': 'renzhi'}),
    ('perception_psy', 'psychology', COUNTER,
     {'en': 'perception', 'es': 'percepcion', 'fr': 'perception', 'de': 'Wahrnehmung', 'he': 'tefisa', 'ar': 'idrak_hissi', 'zh': 'zhijue'}),
    ('memory_psy', 'psychology', LATTICE,
     {'en': 'memory', 'es': 'memoria', 'fr': 'memoire', 'de': 'Gedaechtnis', 'he': 'zikaron', 'ar': 'dhakira', 'zh': 'jiyi'}),
    ('consciousness_psy', 'psychology', HARMONY,
     {'en': 'consciousness', 'es': 'conciencia', 'fr': 'conscience', 'de': 'Bewusstsein', 'he': 'toda', 'ar': 'waayi', 'zh': 'yishi'}),
    ('attention_psy', 'psychology', COUNTER,
     {'en': 'attention', 'es': 'atencion', 'fr': 'attention', 'de': 'Aufmerksamkeit', 'he': 'kesher', 'ar': 'intibah', 'zh': 'zhuyi'}),
    ('intelligence_psy', 'psychology', LATTICE,
     {'en': 'intelligence', 'es': 'inteligencia', 'fr': 'intelligence', 'de': 'Intelligenz', 'he': 'binah', 'ar': 'dhakaa', 'zh': 'zhili'}),
    ('empathy_psy', 'psychology', HARMONY,
     {'en': 'empathy', 'es': 'empatia', 'fr': 'empathie', 'de': 'Empathie', 'he': 'empatya', 'ar': 'taaatuf', 'zh': 'gongqing'}),
    ('resilience_psy', 'psychology', BALANCE,
     {'en': 'resilience', 'es': 'resiliencia', 'fr': 'resilience', 'de': 'Resilienz', 'he': 'khosen', 'ar': 'muruna_nafsiya', 'zh': 'xinli_tanxing'}),
    ('creativity_psy', 'psychology', CHAOS,
     {'en': 'creativity', 'es': 'creatividad', 'fr': 'creativite', 'de': 'Kreativitaet', 'he': 'yetsiratiyut', 'ar': 'ibdaa', 'zh': 'chuangzaoli'}),
    ('motivation_psy', 'psychology', PROGRESS,
     {'en': 'motivation', 'es': 'motivacion', 'fr': 'motivation', 'de': 'Motivation', 'he': 'motivatsya', 'ar': 'tahfiz', 'zh': 'dongji'}),
    ('attachment_psy', 'psychology', HARMONY,
     {'en': 'attachment', 'es': 'apego', 'fr': 'attachement', 'de': 'Bindung', 'he': 'hitkashrut', 'ar': 'taalluq', 'zh': 'yilian'}),
    ('neuroplasticity', 'psychology', PROGRESS,
     {'en': 'neuroplasticity', 'es': 'neuroplasticidad', 'fr': 'neuroplasticite', 'de': 'Neuroplastizitaet', 'he': 'neiroplastiyut', 'ar': 'muruna_asabiya', 'zh': 'shenjingkesuxing'}),
    ('conditioning_psy', 'psychology', LATTICE,
     {'en': 'conditioning', 'es': 'condicionamiento', 'fr': 'conditionnement', 'de': 'Konditionierung', 'he': 'hitnut', 'ar': 'ishraat', 'zh': 'tiaojianfanshe'}),
    ('cognitive_bias', 'psychology', COLLAPSE,
     {'en': 'cognitive bias', 'es': 'sesgo_cognitivo', 'fr': 'biais_cognitif', 'de': 'kognitive_Verzerrung', 'he': 'hataya_kognitivi', 'ar': 'tahayuz_idraaki', 'zh': 'renzhi_piancha'}),
    ('development_psy', 'psychology', PROGRESS,
     {'en': 'development', 'es': 'desarrollo', 'fr': 'developpement', 'de': 'Entwicklung', 'he': 'hitpatkut', 'ar': 'tanmiya', 'zh': 'fazhan'}),

    # ── ASTRONOMY (~15) ───────────────────────────────────────
    ('star_astro', 'astronomy', CHAOS,
     {'en': 'star', 'es': 'estrella', 'fr': 'etoile', 'de': 'Stern', 'he': 'kokhav', 'ar': 'najm', 'zh': 'hengxing'}),
    ('planet_astro', 'astronomy', BREATH,
     {'en': 'planet', 'es': 'planeta', 'fr': 'planete', 'de': 'Planet', 'he': 'kokhav_lekhet', 'ar': 'kawkab', 'zh': 'xingxing'}),
    ('galaxy_astro', 'astronomy', LATTICE,
     {'en': 'galaxy', 'es': 'galaxia', 'fr': 'galaxie', 'de': 'Galaxie', 'he': 'galaksya', 'ar': 'majarra', 'zh': 'xingxi'}),
    ('nebula_astro', 'astronomy', VOID,
     {'en': 'nebula', 'es': 'nebulosa', 'fr': 'nebuleuse', 'de': 'Nebel', 'he': 'arfilit', 'ar': 'sahaba', 'zh': 'xingyun'}),
    ('supernova_astro', 'astronomy', CHAOS,
     {'en': 'supernova', 'es': 'supernova', 'fr': 'supernova', 'de': 'Supernova', 'he': 'supernova', 'ar': 'mustaanar', 'zh': 'chaoxinxing'}),
    ('black_hole_astro', 'astronomy', COLLAPSE,
     {'en': 'black hole', 'es': 'agujero_negro', 'fr': 'trou_noir', 'de': 'schwarzes_Loch', 'he': 'khor_shakhor', 'ar': 'thuqb_aswad', 'zh': 'heidong'}),
    ('constellation_astro', 'astronomy', LATTICE,
     {'en': 'constellation', 'es': 'constelacion', 'fr': 'constellation', 'de': 'Sternbild', 'he': 'mazal', 'ar': 'burj', 'zh': 'xingzuo'}),
    ('solar_system_astro', 'astronomy', LATTICE,
     {'en': 'solar system', 'es': 'sistema_solar', 'fr': 'systeme_solaire', 'de': 'Sonnensystem', 'he': 'marekhet_shemesh', 'ar': 'majmua_shamsiya', 'zh': 'taiyangxi'}),
    ('universe_astro', 'astronomy', VOID,
     {'en': 'universe', 'es': 'universo', 'fr': 'univers', 'de': 'Universum', 'he': 'yeqom', 'ar': 'kawn', 'zh': 'yuzhou'}),
    ('big_bang_astro', 'astronomy', CHAOS,
     {'en': 'big bang', 'es': 'gran_explosion', 'fr': 'big_bang', 'de': 'Urknall', 'he': 'hamapats_hagadol', 'ar': 'infijar_azim', 'zh': 'dayubaofa'}),
    ('cosmic_expansion', 'astronomy', PROGRESS,
     {'en': 'cosmic expansion', 'es': 'expansion_cosmica', 'fr': 'expansion_cosmique', 'de': 'kosmische_Expansion', 'he': 'hithavut_kosmit', 'ar': 'tamaddud_kawni', 'zh': 'yuzhou_pengzhang'}),
    ('stellar_evolution', 'astronomy', PROGRESS,
     {'en': 'stellar evolution', 'es': 'evolucion_estelar', 'fr': 'evolution_stellaire', 'de': 'Sternentwicklung', 'he': 'evolutsia_kokhavit', 'ar': 'tatawwur_najmi', 'zh': 'hengxing_yanhua'}),
    ('eclipse_astro', 'astronomy', COLLAPSE,
     {'en': 'eclipse', 'es': 'eclipse', 'fr': 'eclipse', 'de': 'Finsternis', 'he': 'likui', 'ar': 'kusuf', 'zh': 'rishi'}),
    ('pulsar_astro', 'astronomy', BREATH,
     {'en': 'pulsar', 'es': 'pulsar', 'fr': 'pulsar', 'de': 'Pulsar', 'he': 'pulsar', 'ar': 'najm_nabd', 'zh': 'maichongxing'}),
    ('quasar_astro', 'astronomy', CHAOS,
     {'en': 'quasar', 'es': 'cuasar', 'fr': 'quasar', 'de': 'Quasar', 'he': 'kvazar', 'ar': 'shubh_najm', 'zh': 'leishe'}),

    # ── ECOLOGY (~12) ─────────────────────────────────────────
    ('ecosystem_eco', 'ecology', LATTICE,
     {'en': 'ecosystem', 'es': 'ecosistema', 'fr': 'ecosysteme', 'de': 'Oekosystem', 'he': 'marekhet_ekologit', 'ar': 'nizam_biee', 'zh': 'shengtaixi'}),
    ('biodiversity_eco', 'ecology', HARMONY,
     {'en': 'biodiversity', 'es': 'biodiversidad', 'fr': 'biodiversite', 'de': 'Biodiversitaet', 'he': 'migvan_biologi', 'ar': 'tanawwua_hayawi', 'zh': 'shengwuduoyangxing'}),
    ('food_chain_eco', 'ecology', PROGRESS,
     {'en': 'food chain', 'es': 'cadena_alimentaria', 'fr': 'chaine_alimentaire', 'de': 'Nahrungskette', 'he': 'sharsheret_mazon', 'ar': 'silsilat_ghidaa', 'zh': 'shiwulian'}),
    ('symbiosis_eco', 'ecology', HARMONY,
     {'en': 'symbiosis', 'es': 'simbiosis', 'fr': 'symbiose', 'de': 'Symbiose', 'he': 'simbioza', 'ar': 'takaful', 'zh': 'gongsheng'}),
    ('extinction_eco', 'ecology', COLLAPSE,
     {'en': 'extinction', 'es': 'extincion', 'fr': 'extinction', 'de': 'Aussterben', 'he': 'hakhkhada', 'ar': 'inqiraad', 'zh': 'miejue'}),
    ('conservation_eco', 'ecology', BALANCE,
     {'en': 'conservation', 'es': 'conservacion', 'fr': 'conservation', 'de': 'Naturschutz', 'he': 'shimur', 'ar': 'hifz', 'zh': 'baohu'}),
    ('carbon_cycle_eco', 'ecology', BREATH,
     {'en': 'carbon cycle', 'es': 'ciclo_del_carbono', 'fr': 'cycle_du_carbone', 'de': 'Kohlenstoffkreislauf', 'he': 'makhzor_pakhman', 'ar': 'dawra_karbun', 'zh': 'tanxunhuan'}),
    ('water_cycle_eco', 'ecology', BREATH,
     {'en': 'water cycle', 'es': 'ciclo_del_agua', 'fr': 'cycle_de_leau', 'de': 'Wasserkreislauf', 'he': 'makhzor_hamayim', 'ar': 'dawra_miyah', 'zh': 'shuixunhuan'}),
    ('deforestation_eco', 'ecology', COLLAPSE,
     {'en': 'deforestation', 'es': 'deforestacion', 'fr': 'deforestation', 'de': 'Abholzung', 'he': 'kritut_yaarot', 'ar': 'izalat_ghabat', 'zh': 'senlinkanfa'}),
    ('coral_reef_eco', 'ecology', LATTICE,
     {'en': 'coral reef', 'es': 'arrecife_de_coral', 'fr': 'recif_corallien', 'de': 'Korallenriff', 'he': 'shunit_almogim', 'ar': 'shuab_marjaniya', 'zh': 'shanhuqunjiao'}),
    ('rainforest_eco', 'ecology', BREATH,
     {'en': 'rainforest', 'es': 'selva_tropical', 'fr': 'foret_tropicale', 'de': 'Regenwald', 'he': 'yaar_geshemi', 'ar': 'ghaba_matira', 'zh': 'relinyuglin'}),
    ('pollination_eco', 'ecology', HARMONY,
     {'en': 'pollination', 'es': 'polinizacion', 'fr': 'pollinisation', 'de': 'Bestaeubung', 'he': 'haavaka', 'ar': 'talqih', 'zh': 'shoufen'}),

    # ── ETHICS & SPIRITUALITY (~18) ───────────────────────────
    ('virtue_eth', 'ethics', HARMONY,
     {'en': 'virtue', 'es': 'virtud', 'fr': 'vertu', 'de': 'Tugend', 'he': 'midah_tova', 'ar': 'fadila', 'zh': 'meide'}),
    ('justice_eth', 'ethics', BALANCE,
     {'en': 'justice', 'es': 'justicia', 'fr': 'justice', 'de': 'Gerechtigkeit', 'he': 'tsedek', 'ar': 'adl', 'zh': 'gongzheng'}),
    ('mercy_eth', 'ethics', HARMONY,
     {'en': 'mercy', 'es': 'misericordia', 'fr': 'misericorde', 'de': 'Barmherzigkeit', 'he': 'rakhamim', 'ar': 'rahma', 'zh': 'cibei'}),
    ('compassion_eth', 'ethics', HARMONY,
     {'en': 'compassion', 'es': 'compasion', 'fr': 'compassion', 'de': 'Mitgefuehl', 'he': 'khemlah', 'ar': 'shafaqa', 'zh': 'tongqing'}),
    ('courage_eth', 'ethics', PROGRESS,
     {'en': 'courage', 'es': 'coraje', 'fr': 'courage', 'de': 'Mut', 'he': 'omets', 'ar': 'shujaa', 'zh': 'yongqi'}),
    ('temperance_eth', 'ethics', BALANCE,
     {'en': 'temperance', 'es': 'templanza', 'fr': 'temperance', 'de': 'Maessigung', 'he': 'matinut', 'ar': 'itidal', 'zh': 'jiezhi'}),
    ('integrity_eth', 'ethics', LATTICE,
     {'en': 'integrity', 'es': 'integridad', 'fr': 'integrite', 'de': 'Integritaet', 'he': 'yoshra', 'ar': 'nazaha', 'zh': 'zhengzhi'}),
    ('honesty_eth', 'ethics', LATTICE,
     {'en': 'honesty', 'es': 'honestidad', 'fr': 'honnetete', 'de': 'Ehrlichkeit', 'he': 'yashranut', 'ar': 'sidq', 'zh': 'chengshi'}),
    ('dignity_eth', 'ethics', BALANCE,
     {'en': 'dignity', 'es': 'dignidad', 'fr': 'dignite', 'de': 'Wuerde', 'he': 'kavod', 'ar': 'karama', 'zh': 'zunyan'}),
    ('faith_spi', 'spirituality', LATTICE,
     {'en': 'faith', 'es': 'fe', 'fr': 'foi', 'de': 'Glaube', 'he': 'emunah', 'ar': 'iman', 'zh': 'xinyang'}),
    ('hope_spi', 'spirituality', PROGRESS,
     {'en': 'hope', 'es': 'esperanza', 'fr': 'esperance', 'de': 'Hoffnung', 'he': 'tikvah', 'ar': 'amal', 'zh': 'xiwang'}),
    ('love_spi', 'spirituality', HARMONY,
     {'en': 'love', 'es': 'amor', 'fr': 'amour', 'de': 'Liebe', 'he': 'ahavah', 'ar': 'hubb', 'zh': 'ai'}),
    ('grace_spi', 'spirituality', RESET,
     {'en': 'grace', 'es': 'gracia', 'fr': 'grace', 'de': 'Gnade', 'he': 'khesed', 'ar': 'nima', 'zh': 'enci'}),
    ('forgiveness_spi', 'spirituality', RESET,
     {'en': 'forgiveness', 'es': 'perdon', 'fr': 'pardon', 'de': 'Vergebung', 'he': 'slikha', 'ar': 'mughfira', 'zh': 'kuanshu'}),
    ('transcendence_spi', 'spirituality', VOID,
     {'en': 'transcendence', 'es': 'trascendencia', 'fr': 'transcendance', 'de': 'Transzendenz', 'he': 'hitromemut', 'ar': 'taaalii', 'zh': 'chaoyue'}),
    ('wisdom_spi', 'spirituality', LATTICE,
     {'en': 'wisdom', 'es': 'sabiduria', 'fr': 'sagesse', 'de': 'Weisheit', 'he': 'khokhmah', 'ar': 'hikma', 'zh': 'zhihui'}),
    ('covenant_spi', 'spirituality', LATTICE,
     {'en': 'covenant', 'es': 'pacto', 'fr': 'alliance', 'de': 'Bund', 'he': 'brit', 'ar': 'ahd', 'zh': 'shengyue'}),
    ('redemption_spi', 'spirituality', RESET,
     {'en': 'redemption', 'es': 'redencion', 'fr': 'redemption', 'de': 'Erloesung', 'he': 'geulah', 'ar': 'fidaa', 'zh': 'jiushu'}),

    # ── LITERATURE (~12) ──────────────────────────────────────
    ('narrative_lit', 'literature', PROGRESS,
     {'en': 'narrative', 'es': 'narrativa', 'fr': 'recit', 'de': 'Erzaehlung', 'he': 'sipur', 'ar': 'sard', 'zh': 'xushu'}),
    ('poetry_lit', 'literature', BREATH,
     {'en': 'poetry', 'es': 'poesia', 'fr': 'poesie', 'de': 'Poesie', 'he': 'shira', 'ar': 'shir', 'zh': 'shige'}),
    ('metaphor_lit', 'literature', HARMONY,
     {'en': 'metaphor', 'es': 'metafora', 'fr': 'metaphore', 'de': 'Metapher', 'he': 'mashal', 'ar': 'istiara', 'zh': 'yinyu'}),
    ('tragedy_lit', 'literature', COLLAPSE,
     {'en': 'tragedy', 'es': 'tragedia', 'fr': 'tragedie', 'de': 'Tragoedie', 'he': 'tragedya', 'ar': 'maasaat', 'zh': 'beiju'}),
    ('mythology_lit', 'literature', LATTICE,
     {'en': 'mythology', 'es': 'mitologia', 'fr': 'mythologie', 'de': 'Mythologie', 'he': 'mitologya', 'ar': 'asatir', 'zh': 'shenhua'}),
    ('symbolism_lit', 'literature', HARMONY,
     {'en': 'symbolism', 'es': 'simbolismo', 'fr': 'symbolisme', 'de': 'Symbolismus', 'he': 'samlut', 'ar': 'ramziya', 'zh': 'xiangzheng'}),
    ('irony_lit', 'literature', COUNTER,
     {'en': 'irony', 'es': 'ironia', 'fr': 'ironie', 'de': 'Ironie', 'he': 'irounya', 'ar': 'sukhria', 'zh': 'fengci'}),
    ('rhetoric_lit', 'literature', PROGRESS,
     {'en': 'rhetoric', 'es': 'retorica', 'fr': 'rhetorique', 'de': 'Rhetorik', 'he': 'retorika', 'ar': 'balagha', 'zh': 'xiucifa'}),
    ('allegory_lit', 'literature', HARMONY,
     {'en': 'allegory', 'es': 'alegoria', 'fr': 'allegorie', 'de': 'Allegorie', 'he': 'alegorya', 'ar': 'ramz', 'zh': 'yuyan'}),
    ('epic_lit', 'literature', PROGRESS,
     {'en': 'epic', 'es': 'epica', 'fr': 'epopee', 'de': 'Epos', 'he': 'epos', 'ar': 'malhama', 'zh': 'shishi'}),
    ('satire_lit', 'literature', CHAOS,
     {'en': 'satire', 'es': 'satira', 'fr': 'satire', 'de': 'Satire', 'he': 'satira', 'ar': 'hajw', 'zh': 'fengciwen'}),
    ('folklore_lit', 'literature', LATTICE,
     {'en': 'folklore', 'es': 'folclore', 'fr': 'folklore', 'de': 'Folklore', 'he': 'folklor', 'ar': 'turath', 'zh': 'minjian'}),

    # ── LINGUISTICS (~10) ─────────────────────────────────────
    ('syntax_ling', 'linguistics', LATTICE,
     {'en': 'syntax', 'es': 'sintaxis', 'fr': 'syntaxe', 'de': 'Syntax', 'he': 'takhbir', 'ar': 'nahw', 'zh': 'jufa'}),
    ('semantics_ling', 'linguistics', HARMONY,
     {'en': 'semantics', 'es': 'semantica', 'fr': 'semantique', 'de': 'Semantik', 'he': 'semantika', 'ar': 'dalala', 'zh': 'yuyi'}),
    ('phonology_ling', 'linguistics', COUNTER,
     {'en': 'phonology', 'es': 'fonologia', 'fr': 'phonologie', 'de': 'Phonologie', 'he': 'fonologya', 'ar': 'sawtiiyat', 'zh': 'yinweixue'}),
    ('morphology_ling', 'linguistics', LATTICE,
     {'en': 'morphology', 'es': 'morfologia', 'fr': 'morphologie', 'de': 'Morphologie', 'he': 'morfologya', 'ar': 'sarf', 'zh': 'xingtaixue'}),
    ('pragmatics_ling', 'linguistics', BALANCE,
     {'en': 'pragmatics', 'es': 'pragmatica', 'fr': 'pragmatique', 'de': 'Pragmatik', 'he': 'pragmatika', 'ar': 'tadawuliya', 'zh': 'yuyongxue'}),
    ('grammar_ling', 'linguistics', LATTICE,
     {'en': 'grammar', 'es': 'gramatica', 'fr': 'grammaire', 'de': 'Grammatik', 'he': 'dikduk', 'ar': 'qawaid', 'zh': 'yufa'}),
    ('etymology_ling', 'linguistics', PROGRESS,
     {'en': 'etymology', 'es': 'etimologia', 'fr': 'etymologie', 'de': 'Etymologie', 'he': 'etimologya', 'ar': 'ishtiqaq', 'zh': 'ciyuanxue'}),
    ('dialect_ling', 'linguistics', COUNTER,
     {'en': 'dialect', 'es': 'dialecto', 'fr': 'dialecte', 'de': 'Dialekt', 'he': 'niuv', 'ar': 'lahja', 'zh': 'fangyan'}),
    ('translation_ling', 'linguistics', HARMONY,
     {'en': 'translation', 'es': 'traduccion', 'fr': 'traduction', 'de': 'Uebersetzung', 'he': 'tirgum', 'ar': 'tarjama', 'zh': 'fanyi'}),
    ('bilingualism_ling', 'linguistics', BALANCE,
     {'en': 'bilingualism', 'es': 'bilinguismo', 'fr': 'bilinguisme', 'de': 'Zweisprachigkeit', 'he': 'du_leshoniyut', 'ar': 'thunaaiyyat_lugha', 'zh': 'shuangyuzhe'}),

    # ── GEOGRAPHY (~10) ───────────────────────────────────────
    ('continent_geo', 'geography', LATTICE,
     {'en': 'continent', 'es': 'continente', 'fr': 'continent', 'de': 'Kontinent', 'he': 'yabeshet', 'ar': 'qaarra', 'zh': 'dalu'}),
    ('ocean_geo', 'geography', BREATH,
     {'en': 'ocean', 'es': 'oceano', 'fr': 'ocean', 'de': 'Ozean', 'he': 'okiyanus', 'ar': 'muhit', 'zh': 'haiyang'}),
    ('mountain_geo', 'geography', BALANCE,
     {'en': 'mountain', 'es': 'montana', 'fr': 'montagne', 'de': 'Berg', 'he': 'har', 'ar': 'jabal', 'zh': 'shan'}),
    ('volcano_geo', 'geography', CHAOS,
     {'en': 'volcano', 'es': 'volcan', 'fr': 'volcan', 'de': 'Vulkan', 'he': 'vulkan', 'ar': 'burkan', 'zh': 'huoshan'}),
    ('earthquake_geo', 'geography', COLLAPSE,
     {'en': 'earthquake', 'es': 'terremoto', 'fr': 'seisme', 'de': 'Erdbeben', 'he': 'reidat_adama', 'ar': 'zilzal', 'zh': 'dizhen'}),
    ('glacier_geo', 'geography', VOID,
     {'en': 'glacier', 'es': 'glaciar', 'fr': 'glacier', 'de': 'Gletscher', 'he': 'kerakhorn', 'ar': 'naher_jalidi', 'zh': 'bingchuan'}),
    ('tectonic_geo', 'geography', PROGRESS,
     {'en': 'tectonics', 'es': 'tectonica', 'fr': 'tectonique', 'de': 'Tektonik', 'he': 'tektonika', 'ar': 'tiktunikiya', 'zh': 'banjiegou'}),
    ('erosion_geo', 'geography', COLLAPSE,
     {'en': 'erosion', 'es': 'erosion', 'fr': 'erosion', 'de': 'Erosion', 'he': 'skhifa', 'ar': 'taariya', 'zh': 'qinshi'}),
    ('climate_zone_geo', 'geography', BALANCE,
     {'en': 'climate zone', 'es': 'zona_climatica', 'fr': 'zone_climatique', 'de': 'Klimazone', 'he': 'ezor_aklim', 'ar': 'mintaqa_munakhiya', 'zh': 'qihoudai'}),
    ('delta_geo', 'geography', LATTICE,
     {'en': 'delta', 'es': 'delta', 'fr': 'delta', 'de': 'Delta', 'he': 'delta', 'ar': 'delta', 'zh': 'sanjiao'}),

    # ── MEDICINE (~12) ────────────────────────────────────────
    ('anatomy_med', 'medicine', LATTICE,
     {'en': 'anatomy', 'es': 'anatomia', 'fr': 'anatomie', 'de': 'Anatomie', 'he': 'anatomya', 'ar': 'tashrih', 'zh': 'jiepou'}),
    ('physiology_med', 'medicine', BREATH,
     {'en': 'physiology', 'es': 'fisiologia', 'fr': 'physiologie', 'de': 'Physiologie', 'he': 'fizyologya', 'ar': 'fiziyulujiya', 'zh': 'shenglixue'}),
    ('diagnosis_med', 'medicine', COUNTER,
     {'en': 'diagnosis', 'es': 'diagnostico', 'fr': 'diagnostic', 'de': 'Diagnose', 'he': 'ivkhun', 'ar': 'tashkhis', 'zh': 'zhenduan'}),
    ('immunity_med', 'medicine', BALANCE,
     {'en': 'immunity', 'es': 'inmunidad', 'fr': 'immunite', 'de': 'Immunitaet', 'he': 'khisun', 'ar': 'manaa', 'zh': 'mianyi'}),
    ('vaccination_med', 'medicine', PROGRESS,
     {'en': 'vaccination', 'es': 'vacunacion', 'fr': 'vaccination', 'de': 'Impfung', 'he': 'khisun_med', 'ar': 'tatiim', 'zh': 'jiezhong'}),
    ('metabolism_med', 'medicine', BREATH,
     {'en': 'metabolism', 'es': 'metabolismo', 'fr': 'metabolisme', 'de': 'Stoffwechsel', 'he': 'khalifat_khomarim', 'ar': 'ayid', 'zh': 'xinchendaixie'}),
    ('neuron_med', 'medicine', PROGRESS,
     {'en': 'neuron', 'es': 'neurona', 'fr': 'neurone', 'de': 'Neuron', 'he': 'neiron', 'ar': 'khaliya_asabiya', 'zh': 'shenjingyuanbao'}),
    ('synapse_med', 'medicine', HARMONY,
     {'en': 'synapse', 'es': 'sinapsis', 'fr': 'synapse', 'de': 'Synapse', 'he': 'sinapsah', 'ar': 'mushabak', 'zh': 'tuchu'}),
    ('homeostasis_med', 'medicine', BALANCE,
     {'en': 'homeostasis', 'es': 'homeostasis', 'fr': 'homeostasie', 'de': 'Homoeostase', 'he': 'homeostazis', 'ar': 'ittizaan', 'zh': 'neiwendingxing'}),
    ('hormone_med', 'medicine', PROGRESS,
     {'en': 'hormone', 'es': 'hormona', 'fr': 'hormone', 'de': 'Hormon', 'he': 'hormon', 'ar': 'hurmun', 'zh': 'jisu'}),
    ('pathology_med', 'medicine', COLLAPSE,
     {'en': 'pathology', 'es': 'patologia', 'fr': 'pathologie', 'de': 'Pathologie', 'he': 'patologya', 'ar': 'amrad', 'zh': 'binglixue'}),
    ('epidemiology_med', 'medicine', COUNTER,
     {'en': 'epidemiology', 'es': 'epidemiologia', 'fr': 'epidemiologie', 'de': 'Epidemiologie', 'he': 'epidemiologya', 'ar': 'wabaaiyat', 'zh': 'liuxingbingxue'}),

    # ── ART & ARCHITECTURE (~8) ──────────────────────────────
    ('perspective_art', 'art', PROGRESS,
     {'en': 'perspective', 'es': 'perspectiva', 'fr': 'perspective', 'de': 'Perspektive', 'he': 'perspektiva', 'ar': 'manzur', 'zh': 'toushifa'}),
    ('composition_art', 'art', LATTICE,
     {'en': 'composition', 'es': 'composicion', 'fr': 'composition', 'de': 'Komposition', 'he': 'kompozitsia_art', 'ar': 'takwin', 'zh': 'goutu'}),
    ('sculpture_art', 'art', LATTICE,
     {'en': 'sculpture', 'es': 'escultura', 'fr': 'sculpture', 'de': 'Skulptur', 'he': 'pesel', 'ar': 'naht', 'zh': 'diaoshu'}),
    ('architecture_art', 'art', LATTICE,
     {'en': 'architecture', 'es': 'arquitectura', 'fr': 'architecture', 'de': 'Architektur', 'he': 'adrikhalut', 'ar': 'imara', 'zh': 'jianzhu'}),
    ('proportion_art', 'art', BALANCE,
     {'en': 'proportion', 'es': 'proporcion', 'fr': 'proportion', 'de': 'Proportion', 'he': 'proportsya', 'ar': 'tanasub', 'zh': 'bili'}),
    ('aesthetic_art', 'art', HARMONY,
     {'en': 'aesthetic', 'es': 'estetica', 'fr': 'esthetique', 'de': 'Aesthetik', 'he': 'estetika', 'ar': 'jamaliya', 'zh': 'meixue'}),
    ('contrast_art', 'art', COLLAPSE,
     {'en': 'contrast', 'es': 'contraste', 'fr': 'contraste', 'de': 'Kontrast', 'he': 'nigudiut', 'ar': 'tabaayun', 'zh': 'duibi'}),
    ('minimalism_art', 'art', VOID,
     {'en': 'minimalism', 'es': 'minimalismo', 'fr': 'minimalisme', 'de': 'Minimalismus', 'he': 'minimalizm', 'ar': 'taqliliya', 'zh': 'jiyuezhuyi'}),

    # ── LAW & GOVERNANCE (~8) ────────────────────────────────
    ('legislation_law', 'law', LATTICE,
     {'en': 'legislation', 'es': 'legislacion', 'fr': 'legislation', 'de': 'Gesetzgebung', 'he': 'khaika', 'ar': 'tashri', 'zh': 'lifa'}),
    ('judiciary_law', 'law', BALANCE,
     {'en': 'judiciary', 'es': 'poder_judicial', 'fr': 'pouvoir_judiciaire', 'de': 'Justiz', 'he': 'reshut_mishpatit', 'ar': 'qadaa', 'zh': 'sifa'}),
    ('sovereignty_law', 'law', LATTICE,
     {'en': 'sovereignty', 'es': 'soberania', 'fr': 'souverainete', 'de': 'Souveraenitaet', 'he': 'ribonut', 'ar': 'siyada', 'zh': 'zhuquan'}),
    ('human_rights_law', 'law', HARMONY,
     {'en': 'human rights', 'es': 'derechos_humanos', 'fr': 'droits_de_lhomme', 'de': 'Menschenrechte', 'he': 'zkhuyot_adam', 'ar': 'huquq_insan', 'zh': 'renquan'}),
    ('criminal_law', 'law', COLLAPSE,
     {'en': 'criminal law', 'es': 'derecho_penal', 'fr': 'droit_penal', 'de': 'Strafrecht', 'he': 'plili', 'ar': 'qanun_jinaai', 'zh': 'xingfa'}),
    ('civil_law_legal', 'law', BALANCE,
     {'en': 'civil law', 'es': 'derecho_civil', 'fr': 'droit_civil', 'de': 'Zivilrecht', 'he': 'mishpat_ezrakhi', 'ar': 'qanun_madani', 'zh': 'minfa'}),
    ('contract_law', 'law', LATTICE,
     {'en': 'contract', 'es': 'contrato', 'fr': 'contrat', 'de': 'Vertrag', 'he': 'khoze', 'ar': 'aqd', 'zh': 'hetong'}),
    ('precedent_law', 'law', LATTICE,
     {'en': 'precedent', 'es': 'precedente', 'fr': 'precedent', 'de': 'Praezedenz', 'he': 'takdim', 'ar': 'sabiqa', 'zh': 'panli'}),
]


# ================================================================
#  EDUCATION RELATIONS: The Bridges Between Domains
# ================================================================
# Format: (source_id, relation_type, target_id)
#
# CRITICAL: Cross-domain bridges are the fuel for creative reasoning.
# These connections let the Levy jump engine link distant concepts:
#   "gravity resembles loneliness" -- both pull inward.
#   "ecosystem resembles market" -- both self-organize.
#   "neuron resembles network" -- both transmit signals.

EDUCATION_RELATIONS = [
    # ── WITHIN HISTORY ──────────────────────────────────────
    ('civilization', 'enables', 'cultural_exchange'),
    ('empire_hist', 'causes', 'colonialism_hist'),
    ('revolution_hist', 'transforms', 'monarchy_hist'),
    ('democracy_hist', 'opposes', 'monarchy_hist'),
    ('renaissance_hist', 'enables', 'enlightenment_hist'),
    ('enlightenment_hist', 'enables', 'industrial_rev'),
    ('warfare', 'opposes', 'peace_pol'),
    ('treaty_hist', 'enables', 'peace_pol'),
    ('abolition_hist', 'opposes', 'colonialism_hist'),
    ('nationalism_hist', 'causes', 'warfare'),

    # ── WITHIN MUSIC ────────────────────────────────────────
    ('melody_mus', 'harmonizes', 'harmony_mus'),
    ('rhythm_mus', 'sustains', 'melody_mus'),
    ('chord_mus', 'contains', 'harmony_mus'),
    ('scale_mus', 'enables', 'melody_mus'),
    ('consonance_mus', 'opposes', 'dissonance_mus'),
    ('counterpoint_mus', 'balances', 'melody_mus'),
    ('dynamics_mus', 'transforms', 'melody_mus'),
    ('composition_mus', 'contains', 'melody_mus'),
    ('fugue_mus', 'is_a', 'composition_mus'),
    ('cadence_mus', 'resets', 'melody_mus'),
    ('improvisation_mus', 'transforms', 'melody_mus'),
    ('orchestration_mus', 'harmonizes', 'composition_mus'),

    # ── WITHIN COMPUTING ────────────────────────────────────
    ('algorithm_cs', 'is_a', 'abstraction_cs'),
    ('data_structure_cs', 'enables', 'algorithm_cs'),
    ('recursion_cs', 'is_a', 'algorithm_cs'),
    ('encryption_cs', 'enables', 'protocol_cs'),
    ('network_cs', 'enables', 'protocol_cs'),
    ('state_machine_cs', 'is_a', 'abstraction_cs'),
    ('compiler_cs', 'transforms', 'abstraction_cs'),
    ('complexity_cs', 'contains', 'algorithm_cs'),
    ('parallel_cs', 'enables', 'network_cs'),
    ('binary_cs', 'enables', 'boolean_cs'),
    ('cache_cs', 'enables', 'algorithm_cs'),
    ('api_cs', 'enables', 'abstraction_cs'),

    # ── WITHIN ECONOMICS ────────────────────────────────────
    ('supply_econ', 'balances', 'demand_econ'),
    ('scarcity_econ', 'causes', 'demand_econ'),
    ('inflation_econ', 'opposes', 'productivity_econ'),
    ('trade_econ', 'enables', 'globalization_econ'),
    ('innovation_econ', 'enables', 'productivity_econ'),
    ('recession_econ', 'opposes', 'innovation_econ'),
    ('banking_econ', 'enables', 'investment_econ'),
    ('labor_econ', 'enables', 'productivity_econ'),
    ('entrepreneurship', 'enables', 'innovation_econ'),
    ('currency_econ', 'enables', 'trade_econ'),

    # ── WITHIN PSYCHOLOGY ───────────────────────────────────
    ('cognition_psy', 'enables', 'perception_psy'),
    ('memory_psy', 'sustains', 'cognition_psy'),
    ('attention_psy', 'enables', 'cognition_psy'),
    ('motivation_psy', 'causes', 'creativity_psy'),
    ('attachment_psy', 'enables', 'empathy_psy'),
    ('resilience_psy', 'opposes', 'cognitive_bias'),
    ('neuroplasticity', 'enables', 'memory_psy'),
    ('conditioning_psy', 'causes', 'memory_psy'),
    ('development_psy', 'enables', 'intelligence_psy'),
    ('consciousness_psy', 'contains', 'cognition_psy'),

    # ── WITHIN ASTRONOMY ────────────────────────────────────
    ('star_astro', 'contains', 'stellar_evolution'),
    ('galaxy_astro', 'contains', 'star_astro'),
    ('supernova_astro', 'transforms', 'star_astro'),
    ('black_hole_astro', 'follows', 'supernova_astro'),
    ('big_bang_astro', 'causes', 'cosmic_expansion'),
    ('solar_system_astro', 'contains', 'planet_astro'),
    ('constellation_astro', 'contains', 'star_astro'),
    ('nebula_astro', 'precedes', 'star_astro'),
    ('pulsar_astro', 'is_a', 'star_astro'),
    ('quasar_astro', 'contains', 'black_hole_astro'),

    # ── WITHIN ECOLOGY ──────────────────────────────────────
    ('ecosystem_eco', 'contains', 'food_chain_eco'),
    ('biodiversity_eco', 'sustains', 'ecosystem_eco'),
    ('symbiosis_eco', 'sustains', 'ecosystem_eco'),
    ('deforestation_eco', 'causes', 'extinction_eco'),
    ('conservation_eco', 'prevents', 'extinction_eco'),
    ('carbon_cycle_eco', 'sustains', 'ecosystem_eco'),
    ('water_cycle_eco', 'sustains', 'ecosystem_eco'),
    ('pollination_eco', 'sustains', 'biodiversity_eco'),
    ('rainforest_eco', 'is_a', 'ecosystem_eco'),
    ('coral_reef_eco', 'is_a', 'ecosystem_eco'),

    # ── WITHIN ETHICS/SPIRITUALITY ──────────────────────────
    ('virtue_eth', 'harmonizes', 'integrity_eth'),
    ('justice_eth', 'balances', 'mercy_eth'),
    ('compassion_eth', 'harmonizes', 'empathy_psy'),
    ('courage_eth', 'enables', 'integrity_eth'),
    ('temperance_eth', 'balances', 'courage_eth'),
    ('faith_spi', 'sustains', 'hope_spi'),
    ('love_spi', 'harmonizes', 'compassion_eth'),
    ('grace_spi', 'enables', 'forgiveness_spi'),
    ('forgiveness_spi', 'resets', 'covenant_spi'),
    ('wisdom_spi', 'enables', 'justice_eth'),
    ('redemption_spi', 'transforms', 'grace_spi'),
    ('transcendence_spi', 'enables', 'wisdom_spi'),

    # ── WITHIN LITERATURE ───────────────────────────────────
    ('narrative_lit', 'contains', 'metaphor_lit'),
    ('mythology_lit', 'is_a', 'narrative_lit'),
    ('tragedy_lit', 'is_a', 'narrative_lit'),
    ('allegory_lit', 'contains', 'symbolism_lit'),
    ('epic_lit', 'is_a', 'narrative_lit'),
    ('satire_lit', 'contains', 'irony_lit'),
    ('rhetoric_lit', 'enables', 'narrative_lit'),
    ('folklore_lit', 'is_a', 'narrative_lit'),

    # ── WITHIN LINGUISTICS ──────────────────────────────────
    ('syntax_ling', 'enables', 'grammar_ling'),
    ('semantics_ling', 'harmonizes', 'syntax_ling'),
    ('phonology_ling', 'enables', 'morphology_ling'),
    ('etymology_ling', 'enables', 'semantics_ling'),
    ('dialect_ling', 'is_a', 'phonology_ling'),
    ('translation_ling', 'harmonizes', 'bilingualism_ling'),

    # ── WITHIN GEOGRAPHY ────────────────────────────────────
    ('tectonic_geo', 'causes', 'earthquake_geo'),
    ('tectonic_geo', 'causes', 'volcano_geo'),
    ('erosion_geo', 'transforms', 'mountain_geo'),
    ('glacier_geo', 'causes', 'erosion_geo'),
    ('ocean_geo', 'sustains', 'climate_zone_geo'),

    # ── WITHIN MEDICINE ─────────────────────────────────────
    ('anatomy_med', 'contains', 'neuron_med'),
    ('physiology_med', 'sustains', 'homeostasis_med'),
    ('neuron_med', 'enables', 'synapse_med'),
    ('immunity_med', 'prevents', 'pathology_med'),
    ('vaccination_med', 'enables', 'immunity_med'),
    ('metabolism_med', 'sustains', 'physiology_med'),
    ('hormone_med', 'enables', 'metabolism_med'),
    ('diagnosis_med', 'enables', 'pathology_med'),
    ('epidemiology_med', 'contains', 'pathology_med'),

    # ── WITHIN LAW ──────────────────────────────────────────
    ('legislation_law', 'enables', 'judiciary_law'),
    ('sovereignty_law', 'enables', 'legislation_law'),
    ('human_rights_law', 'harmonizes', 'civil_law_legal'),
    ('criminal_law', 'opposes', 'civil_law_legal'),
    ('contract_law', 'is_a', 'civil_law_legal'),
    ('precedent_law', 'sustains', 'judiciary_law'),

    # ════════════════════════════════════════════════════════
    #  CROSS-DOMAIN BRIDGES -- The Heart of Creative Reasoning
    # ════════════════════════════════════════════════════════
    # These are the Levy-jump connections that make CK creative.
    # Each bridge connects concepts from different domains via
    # the relation that captures WHY they're similar.

    # Physics <-> Music (both are wave/oscillation domains)
    ('resonance', 'harmonizes', 'harmony_mus'),
    ('oscillation', 'resembles', 'rhythm_mus'),
    ('frequency', 'enables', 'scale_mus'),
    ('amplitude', 'resembles', 'dynamics_mus'),
    ('interference', 'resembles', 'counterpoint_mus'),
    ('wavelength', 'enables', 'timbre_mus'),

    # Psychology <-> Music (emotion and cognition)
    ('empathy_psy', 'harmonizes', 'harmony_mus'),
    ('memory_psy', 'sustains', 'melody_mus'),
    ('creativity_psy', 'enables', 'improvisation_mus'),
    ('attention_psy', 'enables', 'rhythm_mus'),

    # Ecology <-> Economics (self-organizing systems)
    ('ecosystem_eco', 'resembles', 'market_econ'),
    ('food_chain_eco', 'resembles', 'supply_econ'),
    ('symbiosis_eco', 'resembles', 'trade_econ'),
    ('extinction_eco', 'resembles', 'recession_econ'),
    ('biodiversity_eco', 'resembles', 'innovation_econ'),
    ('conservation_eco', 'resembles', 'investment_econ'),

    # Computing <-> Biology (information processing)
    ('algorithm_cs', 'resembles', 'evolution'),
    ('network_cs', 'resembles', 'neuron_med'),
    ('recursion_cs', 'resembles', 'gene'),
    ('data_structure_cs', 'resembles', 'dna_chem'),
    ('parallel_cs', 'resembles', 'synapse_med'),
    ('state_machine_cs', 'resembles', 'organism'),
    ('cache_cs', 'resembles', 'memory_psy'),

    # Ethics <-> Psychology (moral reasoning)
    ('compassion_eth', 'harmonizes', 'empathy_psy'),
    ('courage_eth', 'enables', 'resilience_psy'),
    ('virtue_eth', 'harmonizes', 'development_psy'),
    ('temperance_eth', 'balances', 'motivation_psy'),
    ('cognitive_bias', 'opposes', 'justice_eth'),

    # Spirituality <-> Astronomy (the cosmic and the sacred)
    ('transcendence_spi', 'resembles', 'universe_astro'),
    ('faith_spi', 'resembles', 'cosmic_expansion'),
    ('redemption_spi', 'resembles', 'stellar_evolution'),
    ('love_spi', 'resembles', 'gravity'),

    # History <-> Law (governance evolution)
    ('democracy_hist', 'enables', 'human_rights_law'),
    ('revolution_hist', 'transforms', 'legislation_law'),
    ('civilization', 'enables', 'sovereignty_law'),
    ('treaty_hist', 'is_a', 'contract_law'),

    # Literature <-> Psychology (understanding humans)
    ('narrative_lit', 'enables', 'memory_psy'),
    ('metaphor_lit', 'enables', 'cognition_psy'),
    ('tragedy_lit', 'resembles', 'resilience_psy'),
    ('mythology_lit', 'sustains', 'consciousness_psy'),

    # Music <-> Mathematics (mathematical structure)
    ('harmony_mus', 'resembles', 'symmetry'),
    ('rhythm_mus', 'resembles', 'ratio'),
    ('scale_mus', 'resembles', 'sequence'),
    ('fugue_mus', 'resembles', 'recursion_cs'),

    # Literature <-> Ethics (moral stories)
    ('allegory_lit', 'enables', 'virtue_eth'),
    ('epic_lit', 'enables', 'courage_eth'),
    ('tragedy_lit', 'enables', 'compassion_eth'),
    ('satire_lit', 'opposes', 'cognitive_bias'),

    # Medicine <-> Ecology (living systems)
    ('immunity_med', 'resembles', 'conservation_eco'),
    ('homeostasis_med', 'resembles', 'ecosystem_eco'),
    ('epidemiology_med', 'resembles', 'food_chain_eco'),
    ('metabolism_med', 'resembles', 'carbon_cycle_eco'),

    # Linguistics <-> Computing (language processing)
    ('syntax_ling', 'resembles', 'data_structure_cs'),
    ('semantics_ling', 'resembles', 'information_cs'),
    ('grammar_ling', 'resembles', 'protocol_cs'),
    ('translation_ling', 'resembles', 'compiler_cs'),

    # Geography <-> History (space and time)
    ('continent_geo', 'enables', 'civilization'),
    ('ocean_geo', 'enables', 'trade_econ'),
    ('mountain_geo', 'prevents', 'cultural_exchange'),
    ('tectonic_geo', 'resembles', 'revolution_hist'),

    # Art <-> Mathematics (visual harmony)
    ('proportion_art', 'resembles', 'ratio'),
    ('perspective_art', 'resembles', 'refraction'),
    ('composition_art', 'resembles', 'harmony_mus'),
    ('aesthetic_art', 'harmonizes', 'harmony_mus'),

    # Psychology <-> Medicine (mind-body bridge)
    ('cognition_psy', 'enables', 'neuron_med'),
    ('consciousness_psy', 'contains', 'synapse_med'),
    ('neuroplasticity', 'enables', 'synapse_med'),
    ('attachment_psy', 'enables', 'homeostasis_med'),

    # Economics <-> History (economic history)
    ('industrial_rev', 'enables', 'market_econ'),
    ('colonialism_hist', 'enables', 'trade_econ'),
    ('globalization_econ', 'follows', 'industrial_rev'),

    # Spirituality <-> Ethics (moral foundations)
    ('faith_spi', 'enables', 'courage_eth'),
    ('love_spi', 'enables', 'compassion_eth'),
    ('wisdom_spi', 'harmonizes', 'virtue_eth'),
    ('grace_spi', 'enables', 'mercy_eth'),

    # Physics <-> Philosophy/Spirituality (deep connections)
    ('entropy', 'opposes', 'virtue_eth'),
    ('resonance', 'harmonizes', 'love_spi'),
    ('spacetime', 'contains', 'universe_astro'),

    # Computing <-> Psychology (artificial cognition bridge)
    ('abstraction_cs', 'resembles', 'cognition_psy'),
    ('complexity_cs', 'resembles', 'intelligence_psy'),
    ('state_machine_cs', 'resembles', 'consciousness_psy'),
    ('boolean_cs', 'resembles', 'perception_psy'),
]


# ================================================================
#  EXPERIENCE GENERATOR -- How CK Actually Learns
# ================================================================

@dataclass
class ExperienceChain:
    """An operator chain representing one learning experience.

    CK doesn't learn by being told. CK learns by processing operator
    chains through his heartbeat. Each chain is a sequence of operators
    derived from traversing concept relations.

    The chain enters CK's system as sensory data. His coherence field
    composes it with his current state. If the result is coherent
    (C >= T*), the concepts involved get a coherence tick toward
    promotion in the truth lattice.

    If NOT coherent, the chain is just noise. CK rejects it naturally.
    """
    domain: str                   # Source domain
    concept_ids: List[str]        # Concepts involved
    operators: List[int]          # Operator sequence
    coherence_target: float       # Expected coherence if understood
    description: str = ""         # Human-readable description


class ExperienceGenerator:
    """Generate learning experiences from the concept graph.

    This is CK's teacher. NOT in the sense of telling CK what to
    believe, but in the sense of creating structured encounters
    that CK must process through coherence.

    The generator walks the concept graph, following relations,
    and builds operator chains from the concepts it visits. These
    chains are then fed into CK's heartbeat as experience.

    Whether CK "learns" depends entirely on whether the chains
    produce sustained coherence. The generator has no say in what
    CK accepts.
    """

    def __init__(self, lattice: WorldLattice):
        self.lattice = lattice
        self._rng = random.Random(42)  # Reproducible
        self._session_count = 0

    def generate_domain_session(self, domain: str,
                                chain_length: int = EXPERIENCE_CHAIN_LEN
                                ) -> List[ExperienceChain]:
        """Generate a learning session for one domain.

        Walks through concepts in the domain, following relations,
        building operator chains from the traversal.
        """
        concepts = [nid for nid, node in self.lattice.nodes.items()
                    if node.domain == domain]
        if not concepts:
            return []

        chains = []
        self._rng.shuffle(concepts)

        for start in concepts[:SESSION_TICKS // chain_length]:
            chain = self._walk_chain(start, chain_length, domain)
            if chain:
                chains.append(chain)

        self._session_count += 1
        return chains

    def generate_cross_domain_session(self, domain_a: str, domain_b: str,
                                       chain_length: int = EXPERIENCE_CHAIN_LEN
                                       ) -> List[ExperienceChain]:
        """Generate a cross-domain learning session.

        These are the creative sessions. CK encounters concepts
        from two different domains connected by bridge relations.
        The resulting operator chains blend both domains.
        """
        concepts_a = [nid for nid, node in self.lattice.nodes.items()
                      if node.domain == domain_a]
        concepts_b = [nid for nid, node in self.lattice.nodes.items()
                      if node.domain == domain_b]
        if not concepts_a or not concepts_b:
            return []

        chains = []
        # Find bridge connections
        for nid_a in concepts_a:
            neighbors = self.lattice.get_neighbors(nid_a)
            for neighbor_id, rel, _ in neighbors:
                if neighbor_id in concepts_b or (
                        self.lattice.nodes.get(neighbor_id) and
                        self.lattice.nodes[neighbor_id].domain == domain_b):
                    # Found a bridge! Build a chain from it
                    ops = self._bridge_chain(nid_a, neighbor_id,
                                             chain_length)
                    if ops:
                        chain = ExperienceChain(
                            domain=f"{domain_a}+{domain_b}",
                            concept_ids=[nid_a, neighbor_id],
                            operators=ops,
                            coherence_target=T_STAR,
                            description=f"{nid_a} -{rel}-> {neighbor_id}",
                        )
                        chains.append(chain)

        self._session_count += 1
        return chains

    def generate_full_curriculum(self) -> List[ExperienceChain]:
        """Generate a complete education curriculum.

        Produces domain sessions first (foundations), then cross-domain
        sessions (creative bridges). Order matters -- you learn the
        basics before making connections.
        """
        all_chains = []

        # Phase 1: Domain foundations
        domains = set()
        for nid, node in self.lattice.nodes.items():
            domains.add(node.domain)

        for domain in sorted(domains):
            session = self.generate_domain_session(domain)
            all_chains.extend(session)

        # Phase 2: Cross-domain bridges
        domain_list = sorted(domains)
        for i, d_a in enumerate(domain_list):
            for d_b in domain_list[i + 1:]:
                session = self.generate_cross_domain_session(d_a, d_b)
                all_chains.extend(session)

        return all_chains

    def _walk_chain(self, start_id: str, length: int,
                    domain: str) -> Optional[ExperienceChain]:
        """Walk the concept graph building an operator chain."""
        node = self.lattice.nodes.get(start_id)
        if not node:
            return None

        visited = [start_id]
        operators = [node.operator_code]
        current = start_id

        for _ in range(length - 1):
            neighbors = self.lattice.get_neighbors(current)
            if not neighbors:
                break

            # Prefer same-domain neighbors, but allow cross-domain
            same_domain = [(n, r, o) for n, r, o in neighbors
                           if self.lattice.nodes.get(n) and
                           self.lattice.nodes[n].domain == domain and
                           n not in visited]

            if same_domain:
                next_id, rel, _ = self._rng.choice(same_domain)
            elif neighbors:
                next_id, rel, _ = self._rng.choice(neighbors)
            else:
                break

            next_node = self.lattice.nodes.get(next_id)
            if not next_node:
                break

            visited.append(next_id)
            operators.append(next_node.operator_code)
            current = next_id

        if len(operators) < 2:
            return None

        # Compute expected coherence from CL composition
        composed = operators[0]
        harmony_count = 0
        for op in operators[1:]:
            result = CL[composed][op]
            if result == HARMONY:
                harmony_count += 1
            composed = result

        coherence_target = harmony_count / max(1, len(operators) - 1)

        return ExperienceChain(
            domain=domain,
            concept_ids=visited,
            operators=operators,
            coherence_target=coherence_target,
            description=" -> ".join(visited),
        )

    def _bridge_chain(self, id_a: str, id_b: str,
                      length: int) -> Optional[List[int]]:
        """Build operator chain bridging two concepts."""
        node_a = self.lattice.nodes.get(id_a)
        node_b = self.lattice.nodes.get(id_b)
        if not node_a or not node_b:
            return None

        # Start with A's operator, compose toward B, then extend
        ops = [node_a.operator_code]
        composed = compose(node_a.operator_code, node_b.operator_code)
        ops.append(composed)
        ops.append(node_b.operator_code)

        # Pad with compositions to reach target length
        while len(ops) < length:
            a = ops[-2]
            b = ops[-1]
            ops.append(compose(a, b))

        return ops[:length]

    @property
    def sessions_completed(self) -> int:
        return self._session_count


# ================================================================
#  EDUCATION LOADER -- Wire It All Up
# ================================================================

class EducationLoader:
    """Load education content into CK's systems.

    This loader:
      1. Adds concepts to the WorldLattice (infrastructure)
      2. Adds relations to the WorldLattice (bridges)
      3. Creates an ExperienceGenerator (the teacher)
      4. Does NOT pre-load beliefs into the TruthLattice

    The ExperienceGenerator creates operator chains that must
    flow through CK's heartbeat. Whether CK learns from them
    depends on coherence -- the math decides, not us.
    """

    def __init__(self, lattice: WorldLattice):
        self.lattice = lattice
        self._concepts_loaded = 0
        self._relations_loaded = 0
        self._skipped_concepts = 0
        self._skipped_relations = 0

    def load_concepts(self) -> int:
        """Load education concepts into the world lattice."""
        count = 0
        for node_id, domain, op, bindings in EDUCATION_CONCEPTS:
            if node_id in self.lattice.nodes:
                self._skipped_concepts += 1
                continue
            try:
                self.lattice.add_concept(
                    node_id=node_id,
                    operator_code=op,
                    domain=domain,
                    bindings=bindings,
                )
                count += 1
            except Exception:
                self._skipped_concepts += 1
        self._concepts_loaded = count
        return count

    def load_relations(self) -> int:
        """Load education relations into the world lattice."""
        count = 0
        for src, rel, tgt in EDUCATION_RELATIONS:
            if src not in self.lattice.nodes:
                self._skipped_relations += 1
                continue
            if tgt not in self.lattice.nodes:
                self._skipped_relations += 1
                continue
            if rel not in RELATION_TYPES:
                self._skipped_relations += 1
                continue
            try:
                self.lattice.add_relation(src, rel, tgt)
                count += 1
            except Exception:
                self._skipped_relations += 1
        self._relations_loaded = count
        return count

    def load_education(self) -> dict:
        """Full education load: concepts + relations.

        Returns stats dict.
        """
        n_concepts = self.load_concepts()
        n_relations = self.load_relations()
        return {
            'concepts_loaded': n_concepts,
            'relations_loaded': n_relations,
            'concepts_skipped': self._skipped_concepts,
            'relations_skipped': self._skipped_relations,
            'total_lattice_nodes': len(self.lattice.nodes),
        }

    def create_experience_generator(self) -> ExperienceGenerator:
        """Create an experience generator for learning sessions."""
        return ExperienceGenerator(self.lattice)

    def stats(self) -> dict:
        return {
            'concepts_loaded': self._concepts_loaded,
            'relations_loaded': self._relations_loaded,
            'concepts_skipped': self._skipped_concepts,
            'relations_skipped': self._skipped_relations,
        }
