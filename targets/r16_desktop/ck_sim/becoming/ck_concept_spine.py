# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_concept_spine.py -- CK's Concept Spine: 700+ PhD-Level Concepts
===================================================================
Operator: LATTICE (1) -- the spine structures knowledge.

Extends the WorldLattice (ck_world_lattice.py) with hundreds of new
concepts organized by academic domains: physics, chemistry, biology,
mathematics, philosophy, language, emotions, and society.

The existing world lattice has ~157 core concepts. This spine scales
it to 800+ for PhD-level knowledge coverage.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, COLLAPSE, CHAOS, PROGRESS, BREATH,
    BALANCE, COUNTER, LATTICE, RESET, OP_NAMES
)
from ck_sim.ck_world_lattice import WorldLattice, RELATION_TYPES


# ================================================================
#  SPINE CONCEPTS: PhD-Level Knowledge Graph
# ================================================================
# Each entry: (node_id, domain, operator_code, {lang: word, ...})
# Node IDs are unique and do NOT conflict with CORE_CONCEPTS.

SPINE_CONCEPTS = [
    # ── PHYSICS (~60) ─────────────────────────────────────────
    ('mass', 'physics', BALANCE, {
        'en': 'mass', 'es': 'masa', 'fr': 'masse', 'de': 'Masse',
        'he': 'masa', 'ar': 'kutla', 'zh': 'zhiliang'}),
    ('velocity', 'physics', PROGRESS, {
        'en': 'velocity', 'es': 'velocidad', 'fr': 'vitesse', 'de': 'Geschwindigkeit',
        'he': 'mehirut', 'ar': 'suraa', 'zh': 'sudu'}),
    ('acceleration', 'physics', PROGRESS, {
        'en': 'acceleration', 'es': 'aceleracion', 'fr': 'acceleration', 'de': 'Beschleunigung',
        'he': 'teotsa', 'ar': 'tasarua', 'zh': 'jiasu'}),
    ('momentum', 'physics', PROGRESS, {
        'en': 'momentum', 'es': 'momento', 'fr': 'quantite_de_mouvement', 'de': 'Impuls',
        'he': 'tana', 'ar': 'zakhm', 'zh': 'dongliang'}),
    ('frequency', 'physics', COUNTER, {
        'en': 'frequency', 'es': 'frecuencia', 'fr': 'frequence', 'de': 'Frequenz',
        'he': 'teder', 'ar': 'tardud', 'zh': 'pinlv'}),
    ('amplitude', 'physics', BALANCE, {
        'en': 'amplitude', 'es': 'amplitud', 'fr': 'amplitude', 'de': 'Amplitude',
        'he': 'meshura', 'ar': 'siat', 'zh': 'zhenfu'}),
    ('photon', 'physics', HARMONY, {
        'en': 'photon', 'es': 'foton', 'fr': 'photon', 'de': 'Photon',
        'he': 'foton', 'ar': 'futun', 'zh': 'guangzi'}),
    ('electron', 'physics', COUNTER, {
        'en': 'electron', 'es': 'electron', 'fr': 'electron', 'de': 'Elektron',
        'he': 'elektron', 'ar': 'iliktrun', 'zh': 'dianzi'}),
    ('proton', 'physics', LATTICE, {
        'en': 'proton', 'es': 'proton', 'fr': 'proton', 'de': 'Proton',
        'he': 'proton', 'ar': 'brutun', 'zh': 'zhizi'}),
    ('neutron', 'physics', VOID, {
        'en': 'neutron', 'es': 'neutron', 'fr': 'neutron', 'de': 'Neutron',
        'he': 'neitron', 'ar': 'niutrun', 'zh': 'zhongzi_phys'}),
    ('atom', 'physics', LATTICE, {
        'en': 'atom', 'es': 'atomo', 'fr': 'atome', 'de': 'Atom',
        'he': 'atom', 'ar': 'dharra', 'zh': 'yuanzi'}),
    ('molecule', 'physics', LATTICE, {
        'en': 'molecule', 'es': 'molecula', 'fr': 'molecule', 'de': 'Molekuel',
        'he': 'molekula', 'ar': 'juzay', 'zh': 'fenzi'}),
    ('charge_phys', 'physics', CHAOS, {
        'en': 'charge', 'es': 'carga', 'fr': 'charge', 'de': 'Ladung',
        'he': 'miten', 'ar': 'shihna', 'zh': 'dianhe'}),
    ('potential', 'physics', BALANCE, {
        'en': 'potential', 'es': 'potencial', 'fr': 'potentiel', 'de': 'Potential',
        'he': 'potentsial', 'ar': 'kamina', 'zh': 'shi'}),
    ('entropy', 'physics', CHAOS, {
        'en': 'entropy', 'es': 'entropia', 'fr': 'entropie', 'de': 'Entropie',
        'he': 'entropia', 'ar': 'intrubia', 'zh': 'shang'}),
    ('temperature', 'physics', COUNTER, {
        'en': 'temperature', 'es': 'temperatura', 'fr': 'temperature', 'de': 'Temperatur',
        'he': 'temperatura', 'ar': 'harara', 'zh': 'wendu'}),
    ('pressure_physics', 'physics', COLLAPSE, {
        'en': 'pressure', 'es': 'presion', 'fr': 'pression', 'de': 'Druck',
        'he': 'lakhats', 'ar': 'daght', 'zh': 'yali'}),
    ('volume_phys', 'physics', LATTICE, {
        'en': 'volume', 'es': 'volumen', 'fr': 'volume', 'de': 'Volumen',
        'he': 'nefakh', 'ar': 'hajm', 'zh': 'tiji'}),
    ('density', 'physics', BALANCE, {
        'en': 'density', 'es': 'densidad', 'fr': 'densite', 'de': 'Dichte',
        'he': 'tsifut', 'ar': 'kathafa', 'zh': 'midu'}),
    ('current_phys', 'physics', PROGRESS, {
        'en': 'current', 'es': 'corriente', 'fr': 'courant', 'de': 'Strom',
        'he': 'zerem', 'ar': 'tayyar', 'zh': 'dianliu'}),
    ('voltage_phys', 'physics', CHAOS, {
        'en': 'voltage', 'es': 'voltaje', 'fr': 'tension', 'de': 'Spannung',
        'he': 'metakh', 'ar': 'fultiya', 'zh': 'dianya'}),
    ('resistance_phys', 'physics', COLLAPSE, {
        'en': 'resistance', 'es': 'resistencia', 'fr': 'resistance', 'de': 'Widerstand',
        'he': 'hitnagdut', 'ar': 'muqawama', 'zh': 'dianzu'}),
    ('magnetism', 'physics', HARMONY, {
        'en': 'magnetism', 'es': 'magnetismo', 'fr': 'magnetisme', 'de': 'Magnetismus',
        'he': 'magnetiut', 'ar': 'maghnatis', 'zh': 'cili'}),
    ('radiation', 'physics', CHAOS, {
        'en': 'radiation', 'es': 'radiacion', 'fr': 'rayonnement', 'de': 'Strahlung',
        'he': 'krina', 'ar': 'ishaa', 'zh': 'fushe'}),
    ('spectrum', 'physics', LATTICE, {
        'en': 'spectrum', 'es': 'espectro', 'fr': 'spectre', 'de': 'Spektrum',
        'he': 'spektrum', 'ar': 'tayf', 'zh': 'guangpu'}),
    ('quantum', 'physics', COUNTER, {
        'en': 'quantum', 'es': 'cuantico', 'fr': 'quantique', 'de': 'Quant',
        'he': 'kvantum', 'ar': 'kamm', 'zh': 'liangzi'}),
    ('relativity', 'physics', HARMONY, {
        'en': 'relativity', 'es': 'relatividad', 'fr': 'relativite', 'de': 'Relativitaet',
        'he': 'yahsut', 'ar': 'nisbiya', 'zh': 'xiangduilun'}),
    ('spacetime', 'physics', LATTICE, {
        'en': 'spacetime', 'es': 'espaciotiempo', 'fr': 'espace_temps', 'de': 'Raumzeit',
        'he': 'merkhav_zman', 'ar': 'fazaman', 'zh': 'shikong'}),
    ('orbit', 'physics', BREATH, {
        'en': 'orbit', 'es': 'orbita', 'fr': 'orbite', 'de': 'Umlaufbahn',
        'he': 'maslul', 'ar': 'madar', 'zh': 'guidao'}),
    ('inertia', 'physics', BALANCE, {
        'en': 'inertia', 'es': 'inercia', 'fr': 'inertie', 'de': 'Traegheit',
        'he': 'inertsya', 'ar': 'qusur', 'zh': 'guanxing'}),
    ('friction', 'physics', COLLAPSE, {
        'en': 'friction', 'es': 'friccion', 'fr': 'friction', 'de': 'Reibung',
        'he': 'khikukh', 'ar': 'ihtikaak', 'zh': 'mocali'}),
    ('tension_physics', 'physics', BALANCE, {
        'en': 'tension', 'es': 'tension', 'fr': 'tension', 'de': 'Spannung',
        'he': 'metakh_phys', 'ar': 'shad', 'zh': 'zhangli'}),
    ('elasticity', 'physics', BREATH, {
        'en': 'elasticity', 'es': 'elasticidad', 'fr': 'elasticite', 'de': 'Elastizitaet',
        'he': 'gemishot', 'ar': 'muruna', 'zh': 'tanxing'}),
    ('viscosity', 'physics', COLLAPSE, {
        'en': 'viscosity', 'es': 'viscosidad', 'fr': 'viscosite', 'de': 'Viskositaet',
        'he': 'tsmigiut', 'ar': 'luzuja', 'zh': 'nianxing'}),
    ('diffusion', 'physics', CHAOS, {
        'en': 'diffusion', 'es': 'difusion', 'fr': 'diffusion', 'de': 'Diffusion',
        'he': 'difuzya', 'ar': 'intishar', 'zh': 'kuosan'}),
    ('oscillation', 'physics', BREATH, {
        'en': 'oscillation', 'es': 'oscilacion', 'fr': 'oscillation', 'de': 'Schwingung',
        'he': 'tnuda', 'ar': 'tadhabdhub', 'zh': 'zhendang'}),
    ('resonance', 'physics', HARMONY, {
        'en': 'resonance', 'es': 'resonancia', 'fr': 'resonance', 'de': 'Resonanz',
        'he': 'tehodah', 'ar': 'ranin', 'zh': 'gongzhen'}),
    ('wavelength', 'physics', COUNTER, {
        'en': 'wavelength', 'es': 'longitud_de_onda', 'fr': 'longueur_d_onde', 'de': 'Wellenlaenge',
        'he': 'orekh_gal', 'ar': 'tul_mawja', 'zh': 'bochang'}),
    ('interference', 'physics', BALANCE, {
        'en': 'interference', 'es': 'interferencia', 'fr': 'interference', 'de': 'Interferenz',
        'he': 'hitarfut', 'ar': 'tadakhul', 'zh': 'ganshexianxiang'}),
    ('refraction', 'physics', PROGRESS, {
        'en': 'refraction', 'es': 'refraccion', 'fr': 'refraction', 'de': 'Brechung',
        'he': 'shvirat_or', 'ar': 'inkisar', 'zh': 'zheshe'}),
    ('reflection_phys', 'physics', RESET, {
        'en': 'reflection', 'es': 'reflexion', 'fr': 'reflexion', 'de': 'Reflexion',
        'he': 'hishtakfut', 'ar': 'inikaas', 'zh': 'fanshe'}),
    ('absorption', 'physics', COLLAPSE, {
        'en': 'absorption', 'es': 'absorcion', 'fr': 'absorption', 'de': 'Absorption',
        'he': 'klita', 'ar': 'imtisas', 'zh': 'xishou'}),
    ('emission', 'physics', CHAOS, {
        'en': 'emission', 'es': 'emision', 'fr': 'emission', 'de': 'Emission',
        'he': 'plita', 'ar': 'inbiaath', 'zh': 'fushe_phys'}),
    ('thermodynamics', 'physics', BREATH, {
        'en': 'thermodynamics', 'es': 'termodinamica', 'fr': 'thermodynamique', 'de': 'Thermodynamik',
        'he': 'termodinamika', 'ar': 'dinaharari', 'zh': 'relixue'}),
    ('kinetic', 'physics', CHAOS, {
        'en': 'kinetic', 'es': 'cinetico', 'fr': 'cinetique', 'de': 'kinetisch',
        'he': 'kineti', 'ar': 'haraki', 'zh': 'dongneng'}),
    ('potential_energy', 'physics', BALANCE, {
        'en': 'potential energy', 'es': 'energia_potencial', 'fr': 'energie_potentielle', 'de': 'potentielle_Energie',
        'he': 'energia_potentsialit', 'ar': 'taqa_kamina', 'zh': 'shineng'}),
    ('work_physics', 'physics', PROGRESS, {
        'en': 'work', 'es': 'trabajo', 'fr': 'travail', 'de': 'Arbeit',
        'he': 'avoda_phys', 'ar': 'shughl', 'zh': 'gong'}),
    ('power_physics', 'physics', CHAOS, {
        'en': 'power', 'es': 'potencia', 'fr': 'puissance', 'de': 'Leistung',
        'he': 'hesped', 'ar': 'qudra', 'zh': 'gonglv'}),
    ('torque_phys', 'physics', PROGRESS, {
        'en': 'torque', 'es': 'par', 'fr': 'couple', 'de': 'Drehmoment',
        'he': 'moment_sibub', 'ar': 'azm', 'zh': 'niuju'}),
    ('angular_momentum', 'physics', BREATH, {
        'en': 'angular momentum', 'es': 'momento_angular', 'fr': 'moment_cinetique', 'de': 'Drehimpuls',
        'he': 'tena_zaviti', 'ar': 'zakhm_zawiya', 'zh': 'jiadongliang'}),
    ('centripetal', 'physics', COLLAPSE, {
        'en': 'centripetal', 'es': 'centripeta', 'fr': 'centripete', 'de': 'zentripetal',
        'he': 'merkazpani', 'ar': 'jaadhib_markazi', 'zh': 'xiangxin'}),
    ('gravitational_wave', 'physics', BREATH, {
        'en': 'gravitational wave', 'es': 'onda_gravitacional', 'fr': 'onde_gravitationnelle', 'de': 'Gravitationswelle',
        'he': 'gal_kviday', 'ar': 'mawja_jazb', 'zh': 'yinlibo'}),
    ('dark_matter', 'physics', VOID, {
        'en': 'dark matter', 'es': 'materia_oscura', 'fr': 'matiere_noire', 'de': 'dunkle_Materie',
        'he': 'khomer_afal', 'ar': 'madda_muzlima', 'zh': 'an_wuzhi'}),
    ('dark_energy', 'physics', VOID, {
        'en': 'dark energy', 'es': 'energia_oscura', 'fr': 'energie_sombre', 'de': 'dunkle_Energie',
        'he': 'energia_afala', 'ar': 'taqa_muzlima', 'zh': 'an_nengliang'}),
    ('plasma', 'physics', CHAOS, {
        'en': 'plasma', 'es': 'plasma', 'fr': 'plasma', 'de': 'Plasma',
        'he': 'plazma', 'ar': 'blazma', 'zh': 'denglizi'}),

    # ── CHEMISTRY (~40) ───────────────────────────────────────
    ('element', 'chemistry', LATTICE, {
        'en': 'element', 'es': 'elemento', 'fr': 'element', 'de': 'Element',
        'he': 'yesod', 'ar': 'unsur', 'zh': 'yuansu'}),
    ('compound', 'chemistry', LATTICE, {
        'en': 'compound', 'es': 'compuesto', 'fr': 'compose', 'de': 'Verbindung',
        'he': 'tokhovet', 'ar': 'murakkab', 'zh': 'huahewu'}),
    ('reaction', 'chemistry', CHAOS, {
        'en': 'reaction', 'es': 'reaccion', 'fr': 'reaction', 'de': 'Reaktion',
        'he': 'teguva', 'ar': 'tafaaul', 'zh': 'fanying'}),
    ('acid', 'chemistry', CHAOS, {
        'en': 'acid', 'es': 'acido', 'fr': 'acide', 'de': 'Saeure',
        'he': 'khamtsa', 'ar': 'hamid', 'zh': 'suan'}),
    ('base_chem', 'chemistry', BALANCE, {
        'en': 'base', 'es': 'base', 'fr': 'base', 'de': 'Base',
        'he': 'basis', 'ar': 'qaaida', 'zh': 'jian'}),
    ('salt_chem', 'chemistry', BALANCE, {
        'en': 'salt', 'es': 'sal', 'fr': 'sel', 'de': 'Salz',
        'he': 'melakh', 'ar': 'milh', 'zh': 'yan_chem'}),
    ('ion', 'chemistry', CHAOS, {
        'en': 'ion', 'es': 'ion', 'fr': 'ion', 'de': 'Ion',
        'he': 'yon', 'ar': 'ayun', 'zh': 'lizi_chem'}),
    ('bond_chem', 'chemistry', HARMONY, {
        'en': 'bond', 'es': 'enlace', 'fr': 'liaison', 'de': 'Bindung',
        'he': 'kesher_khimi', 'ar': 'rabita', 'zh': 'huaxuejian'}),
    ('catalyst', 'chemistry', PROGRESS, {
        'en': 'catalyst', 'es': 'catalizador', 'fr': 'catalyseur', 'de': 'Katalysator',
        'he': 'zaraz', 'ar': 'hafiz', 'zh': 'cuihuaji'}),
    ('oxidation', 'chemistry', CHAOS, {
        'en': 'oxidation', 'es': 'oxidacion', 'fr': 'oxydation', 'de': 'Oxidation',
        'he': 'khimtson', 'ar': 'aksada', 'zh': 'yanghua'}),
    ('reduction_chem', 'chemistry', RESET, {
        'en': 'reduction', 'es': 'reduccion', 'fr': 'reduction', 'de': 'Reduktion',
        'he': 'khizur', 'ar': 'ikhtizal', 'zh': 'huanyuan'}),
    ('solution', 'chemistry', HARMONY, {
        'en': 'solution', 'es': 'solucion', 'fr': 'solution', 'de': 'Loesung',
        'he': 'tamisa', 'ar': 'mahlul', 'zh': 'rongye'}),
    ('solvent', 'chemistry', BREATH, {
        'en': 'solvent', 'es': 'solvente', 'fr': 'solvant', 'de': 'Loesungsmittel',
        'he': 'mamis', 'ar': 'mudhib', 'zh': 'rongji'}),
    ('solute', 'chemistry', COUNTER, {
        'en': 'solute', 'es': 'soluto', 'fr': 'solute', 'de': 'geloester_Stoff',
        'he': 'mumas', 'ar': 'mudhab', 'zh': 'rongzhi'}),
    ('concentration', 'chemistry', COUNTER, {
        'en': 'concentration', 'es': 'concentracion', 'fr': 'concentration', 'de': 'Konzentration',
        'he': 'rikuz', 'ar': 'tarkiz', 'zh': 'nongdu'}),
    ('ph_value', 'chemistry', BALANCE, {
        'en': 'pH', 'es': 'pH', 'fr': 'pH', 'de': 'pH',
        'he': 'pH', 'ar': 'pH', 'zh': 'pH'}),
    ('crystal_chem', 'chemistry', LATTICE, {
        'en': 'crystal', 'es': 'cristal', 'fr': 'cristal', 'de': 'Kristall',
        'he': 'gadish', 'ar': 'ballura', 'zh': 'jingti'}),
    ('metal', 'chemistry', LATTICE, {
        'en': 'metal', 'es': 'metal', 'fr': 'metal', 'de': 'Metall',
        'he': 'matekhet', 'ar': 'maadin', 'zh': 'jinshu'}),
    ('gas', 'chemistry', CHAOS, {
        'en': 'gas', 'es': 'gas', 'fr': 'gaz', 'de': 'Gas',
        'he': 'gaz', 'ar': 'ghaz', 'zh': 'qiti'}),
    ('liquid_state', 'chemistry', BREATH, {
        'en': 'liquid', 'es': 'liquido', 'fr': 'liquide', 'de': 'Fluessigkeit',
        'he': 'nozel', 'ar': 'sail', 'zh': 'yeti'}),
    ('solid_state', 'chemistry', LATTICE, {
        'en': 'solid', 'es': 'solido', 'fr': 'solide', 'de': 'Feststoff',
        'he': 'mutzak', 'ar': 'sulb', 'zh': 'guti'}),
    ('evaporation', 'chemistry', CHAOS, {
        'en': 'evaporation', 'es': 'evaporacion', 'fr': 'evaporation', 'de': 'Verdunstung',
        'he': 'idui', 'ar': 'tabakhur', 'zh': 'zhengfa'}),
    ('condensation', 'chemistry', COLLAPSE, {
        'en': 'condensation', 'es': 'condensacion', 'fr': 'condensation', 'de': 'Kondensation',
        'he': 'ibui', 'ar': 'takathuf', 'zh': 'ningju'}),
    ('melting', 'chemistry', CHAOS, {
        'en': 'melting', 'es': 'fusion', 'fr': 'fusion', 'de': 'Schmelzen',
        'he': 'hitukh', 'ar': 'insihar', 'zh': 'ronghua'}),
    ('freezing', 'chemistry', COLLAPSE, {
        'en': 'freezing', 'es': 'congelacion', 'fr': 'congelation', 'de': 'Gefrieren',
        'he': 'hakpaa', 'ar': 'tajmid', 'zh': 'ningjie'}),
    ('combustion', 'chemistry', CHAOS, {
        'en': 'combustion', 'es': 'combustion', 'fr': 'combustion', 'de': 'Verbrennung',
        'he': 'beira', 'ar': 'ihtiraq', 'zh': 'ranshao'}),
    ('polymer', 'chemistry', LATTICE, {
        'en': 'polymer', 'es': 'polimero', 'fr': 'polymere', 'de': 'Polymer',
        'he': 'polimer', 'ar': 'bulimir', 'zh': 'gaofenzi'}),
    ('organic', 'chemistry', BREATH, {
        'en': 'organic', 'es': 'organico', 'fr': 'organique', 'de': 'organisch',
        'he': 'organi', 'ar': 'udwi', 'zh': 'youji'}),
    ('inorganic', 'chemistry', LATTICE, {
        'en': 'inorganic', 'es': 'inorganico', 'fr': 'inorganique', 'de': 'anorganisch',
        'he': 'lo_organi', 'ar': 'ghair_udwi', 'zh': 'wuji'}),
    ('protein', 'chemistry', LATTICE, {
        'en': 'protein', 'es': 'proteina', 'fr': 'proteine', 'de': 'Protein',
        'he': 'khulbon', 'ar': 'brutin', 'zh': 'danbaizhi'}),
    ('enzyme', 'chemistry', PROGRESS, {
        'en': 'enzyme', 'es': 'enzima', 'fr': 'enzyme', 'de': 'Enzym',
        'he': 'enzim', 'ar': 'iinzim', 'zh': 'mei'}),
    ('dna_chem', 'chemistry', LATTICE, {
        'en': 'DNA', 'es': 'ADN', 'fr': 'ADN', 'de': 'DNS',
        'he': 'dna', 'ar': 'dna', 'zh': 'tuoyanghegansuan'}),
    ('rna', 'chemistry', PROGRESS, {
        'en': 'RNA', 'es': 'ARN', 'fr': 'ARN', 'de': 'RNS',
        'he': 'rna', 'ar': 'rna', 'zh': 'tanghegansuan'}),
    ('cell_chem', 'chemistry', LATTICE, {
        'en': 'cell', 'es': 'celula', 'fr': 'cellule', 'de': 'Zelle',
        'he': 'ta', 'ar': 'khaliya', 'zh': 'xibao_chem'}),
    ('membrane', 'chemistry', BALANCE, {
        'en': 'membrane', 'es': 'membrana', 'fr': 'membrane', 'de': 'Membran',
        'he': 'kerum', 'ar': 'ghisha', 'zh': 'shengwumo'}),
    ('carbon', 'chemistry', LATTICE, {
        'en': 'carbon', 'es': 'carbono', 'fr': 'carbone', 'de': 'Kohlenstoff',
        'he': 'pakhman', 'ar': 'karbun', 'zh': 'tan'}),
    ('oxygen_element', 'chemistry', BREATH, {
        'en': 'oxygen', 'es': 'oxigeno', 'fr': 'oxygene', 'de': 'Sauerstoff',
        'he': 'khamtsan', 'ar': 'uksijin', 'zh': 'yangqi'}),
    ('hydrogen', 'chemistry', CHAOS, {
        'en': 'hydrogen', 'es': 'hidrogeno', 'fr': 'hydrogene', 'de': 'Wasserstoff',
        'he': 'meiman', 'ar': 'hidrukin', 'zh': 'qingqi'}),
    ('nitrogen_element', 'chemistry', VOID, {
        'en': 'nitrogen', 'es': 'nitrogeno', 'fr': 'azote', 'de': 'Stickstoff',
        'he': 'khankan', 'ar': 'nitrukin', 'zh': 'danqi'}),
    ('iron_element', 'chemistry', LATTICE, {
        'en': 'iron', 'es': 'hierro', 'fr': 'fer', 'de': 'Eisen',
        'he': 'barzel', 'ar': 'hadid', 'zh': 'tie'}),

    # ── BIOLOGY (~50) ─────────────────────────────────────────
    ('organism', 'biology', BREATH, {
        'en': 'organism', 'es': 'organismo', 'fr': 'organisme', 'de': 'Organismus',
        'he': 'organizma', 'ar': 'kain_hai', 'zh': 'youjiti'}),
    ('species', 'biology', LATTICE, {
        'en': 'species', 'es': 'especie', 'fr': 'espece', 'de': 'Art',
        'he': 'min', 'ar': 'nawaa', 'zh': 'wuzhong'}),
    ('evolution', 'biology', PROGRESS, {
        'en': 'evolution', 'es': 'evolucion', 'fr': 'evolution', 'de': 'Evolution',
        'he': 'evolutsya', 'ar': 'tatawwur', 'zh': 'jinhua'}),
    ('gene', 'biology', LATTICE, {
        'en': 'gene', 'es': 'gen', 'fr': 'gene', 'de': 'Gen',
        'he': 'gen', 'ar': 'jin', 'zh': 'jiyin'}),
    ('mutation', 'biology', CHAOS, {
        'en': 'mutation', 'es': 'mutacion', 'fr': 'mutation', 'de': 'Mutation',
        'he': 'mutatsya', 'ar': 'tafra', 'zh': 'tubian'}),
    ('adaptation_bio', 'biology', BALANCE, {
        'en': 'adaptation', 'es': 'adaptacion', 'fr': 'adaptation', 'de': 'Anpassung',
        'he': 'histaglut', 'ar': 'takayyuf', 'zh': 'shiying'}),
    ('photosynthesis', 'biology', HARMONY, {
        'en': 'photosynthesis', 'es': 'fotosintesis', 'fr': 'photosynthese', 'de': 'Photosynthese',
        'he': 'pilosinteza', 'ar': 'bina_dawi', 'zh': 'guanghezuoyong'}),
    ('respiration', 'biology', BREATH, {
        'en': 'respiration', 'es': 'respiracion', 'fr': 'respiration', 'de': 'Atmung',
        'he': 'neshima', 'ar': 'tanaffus', 'zh': 'huxi_bio'}),
    ('digestion', 'biology', PROGRESS, {
        'en': 'digestion', 'es': 'digestion', 'fr': 'digestion', 'de': 'Verdauung',
        'he': 'ikul', 'ar': 'hadm', 'zh': 'xiaohua'}),
    ('circulation', 'biology', BREATH, {
        'en': 'circulation', 'es': 'circulacion', 'fr': 'circulation', 'de': 'Kreislauf',
        'he': 'makhzor_dam', 'ar': 'dawra_damawiya', 'zh': 'xunhuan'}),
    ('nervous_system', 'biology', LATTICE, {
        'en': 'nervous system', 'es': 'sistema_nervioso', 'fr': 'systeme_nerveux', 'de': 'Nervensystem',
        'he': 'marekhet_aatsabim', 'ar': 'jihaz_asabi', 'zh': 'shenjingxitong'}),
    ('brain_bio', 'biology', COUNTER, {
        'en': 'brain', 'es': 'cerebro', 'fr': 'cerveau', 'de': 'Gehirn',
        'he': 'moakh', 'ar': 'dimagh', 'zh': 'danao'}),
    ('neuron', 'biology', COUNTER, {
        'en': 'neuron', 'es': 'neurona', 'fr': 'neurone', 'de': 'Neuron',
        'he': 'takhlit', 'ar': 'khaliya_asabiya', 'zh': 'shenjingyuanbao'}),
    ('synapse', 'biology', HARMONY, {
        'en': 'synapse', 'es': 'sinapsis', 'fr': 'synapse', 'de': 'Synapse',
        'he': 'sinapa', 'ar': 'tashabuk_asabi', 'zh': 'tuchu'}),
    ('hormone', 'biology', PROGRESS, {
        'en': 'hormone', 'es': 'hormona', 'fr': 'hormone', 'de': 'Hormon',
        'he': 'hormon', 'ar': 'hurmun', 'zh': 'jisu'}),
    ('immune_system', 'biology', BALANCE, {
        'en': 'immune system', 'es': 'sistema_inmune', 'fr': 'systeme_immunitaire', 'de': 'Immunsystem',
        'he': 'marekhet_khisun', 'ar': 'jihaz_manaa', 'zh': 'mianyixitong'}),
    ('bacteria', 'biology', BREATH, {
        'en': 'bacteria', 'es': 'bacteria', 'fr': 'bacterie', 'de': 'Bakterium',
        'he': 'khaidak', 'ar': 'baktirya', 'zh': 'xijun'}),
    ('virus_bio', 'biology', COLLAPSE, {
        'en': 'virus', 'es': 'virus', 'fr': 'virus', 'de': 'Virus',
        'he': 'nagif', 'ar': 'fayrus', 'zh': 'bingdu'}),
    ('fungus', 'biology', BREATH, {
        'en': 'fungus', 'es': 'hongo', 'fr': 'champignon', 'de': 'Pilz',
        'he': 'pitria', 'ar': 'fitr', 'zh': 'zhengjun'}),
    ('plant_bio', 'biology', BREATH, {
        'en': 'plant', 'es': 'planta', 'fr': 'plante', 'de': 'Pflanze',
        'he': 'tsemakh', 'ar': 'nabat', 'zh': 'zhiwu'}),
    ('animal_bio', 'biology', BREATH, {
        'en': 'animal', 'es': 'animal', 'fr': 'animal', 'de': 'Tier',
        'he': 'khaya', 'ar': 'hayawan', 'zh': 'dongwu_bio'}),
    ('mammal', 'biology', BREATH, {
        'en': 'mammal', 'es': 'mamifero', 'fr': 'mammifere', 'de': 'Saeugetier',
        'he': 'yonek', 'ar': 'thadiy', 'zh': 'buru'}),
    ('reptile', 'biology', BALANCE, {
        'en': 'reptile', 'es': 'reptil', 'fr': 'reptile', 'de': 'Reptil',
        'he': 'zoreg', 'ar': 'zahif', 'zh': 'pachong'}),
    ('amphibian', 'biology', BALANCE, {
        'en': 'amphibian', 'es': 'anfibio', 'fr': 'amphibien', 'de': 'Amphibie',
        'he': 'du_khai', 'ar': 'barmaii', 'zh': 'liangqi'}),
    ('insect', 'biology', COUNTER, {
        'en': 'insect', 'es': 'insecto', 'fr': 'insecte', 'de': 'Insekt',
        'he': 'kherek', 'ar': 'hashara', 'zh': 'kunchong'}),
    ('vertebrate', 'biology', LATTICE, {
        'en': 'vertebrate', 'es': 'vertebrado', 'fr': 'vertebre', 'de': 'Wirbeltier',
        'he': 'baal_khuliyot', 'ar': 'faqari', 'zh': 'jizhu'}),
    ('invertebrate', 'biology', VOID, {
        'en': 'invertebrate', 'es': 'invertebrado', 'fr': 'invertebre', 'de': 'Wirbelloses',
        'he': 'khasar_khuliyot', 'ar': 'la_faqari', 'zh': 'wujizhu'}),
    ('predator', 'biology', COLLAPSE, {
        'en': 'predator', 'es': 'depredador', 'fr': 'predateur', 'de': 'Raeuber',
        'he': 'toref', 'ar': 'mufris', 'zh': 'bushizhe'}),
    ('prey', 'biology', COLLAPSE, {
        'en': 'prey', 'es': 'presa', 'fr': 'proie', 'de': 'Beute',
        'he': 'teref', 'ar': 'farisa', 'zh': 'liewu'}),
    ('ecosystem', 'biology', LATTICE, {
        'en': 'ecosystem', 'es': 'ecosistema', 'fr': 'ecosysteme', 'de': 'Oekosystem',
        'he': 'maarekhet_ekologit', 'ar': 'nizam_bii', 'zh': 'shengtaixitong'}),
    ('habitat', 'biology', LATTICE, {
        'en': 'habitat', 'es': 'habitat', 'fr': 'habitat', 'de': 'Lebensraum',
        'he': 'beit_gidul', 'ar': 'mawtin', 'zh': 'qixidi'}),
    ('food_chain', 'biology', PROGRESS, {
        'en': 'food chain', 'es': 'cadena_alimenticia', 'fr': 'chaine_alimentaire', 'de': 'Nahrungskette',
        'he': 'sharsheret_mazon', 'ar': 'silsilat_ghizaa', 'zh': 'shiwulian'}),
    ('symbiosis', 'biology', HARMONY, {
        'en': 'symbiosis', 'es': 'simbiosis', 'fr': 'symbiose', 'de': 'Symbiose',
        'he': 'simbioza', 'ar': 'takaaful', 'zh': 'gongshengg'}),
    ('parasite', 'biology', COLLAPSE, {
        'en': 'parasite', 'es': 'parasito', 'fr': 'parasite', 'de': 'Parasit',
        'he': 'tafil', 'ar': 'tufayli', 'zh': 'jishengchong'}),
    ('reproduction', 'biology', RESET, {
        'en': 'reproduction', 'es': 'reproduccion', 'fr': 'reproduction', 'de': 'Fortpflanzung',
        'he': 'ribui', 'ar': 'takathur', 'zh': 'fanzhi'}),
    ('embryo', 'biology', RESET, {
        'en': 'embryo', 'es': 'embrion', 'fr': 'embryon', 'de': 'Embryo',
        'he': 'ubar', 'ar': 'janin', 'zh': 'peitai'}),
    ('growth_bio', 'biology', PROGRESS, {
        'en': 'growth', 'es': 'crecimiento', 'fr': 'croissance', 'de': 'Wachstum',
        'he': 'tsemikha', 'ar': 'numuww', 'zh': 'shengzhang'}),
    ('aging', 'biology', COLLAPSE, {
        'en': 'aging', 'es': 'envejecimiento', 'fr': 'vieillissement', 'de': 'Alterung',
        'he': 'hizdaknut', 'ar': 'shaykhukha', 'zh': 'shuailao'}),
    ('death_bio', 'biology', COLLAPSE, {
        'en': 'death', 'es': 'muerte', 'fr': 'mort', 'de': 'Tod',
        'he': 'mavet', 'ar': 'mawt', 'zh': 'siwang_bio'}),
    ('extinction', 'biology', VOID, {
        'en': 'extinction', 'es': 'extincion', 'fr': 'extinction', 'de': 'Aussterben',
        'he': 'hakhkhada', 'ar': 'inqirad', 'zh': 'miejue'}),
    ('biodiversity', 'biology', HARMONY, {
        'en': 'biodiversity', 'es': 'biodiversidad', 'fr': 'biodiversite', 'de': 'Biodiversitaet',
        'he': 'migvan_biologi', 'ar': 'tanawwu_hayawi', 'zh': 'shengwuduoyangxing'}),
    ('mitosis', 'biology', PROGRESS, {
        'en': 'mitosis', 'es': 'mitosis', 'fr': 'mitose', 'de': 'Mitose',
        'he': 'mitoza', 'ar': 'inqisam_khuyuti', 'zh': 'yousi'}),
    ('meiosis', 'biology', RESET, {
        'en': 'meiosis', 'es': 'meiosis', 'fr': 'meiose', 'de': 'Meiose',
        'he': 'meyoza', 'ar': 'inqisam_manasi', 'zh': 'jianshufenlie'}),
    ('chromosome', 'biology', LATTICE, {
        'en': 'chromosome', 'es': 'cromosoma', 'fr': 'chromosome', 'de': 'Chromosom',
        'he': 'khromosom', 'ar': 'krumusum', 'zh': 'ranseti'}),
    ('stem_cell', 'biology', RESET, {
        'en': 'stem cell', 'es': 'celula_madre', 'fr': 'cellule_souche', 'de': 'Stammzelle',
        'he': 'ta_geza', 'ar': 'khaliya_jiziya', 'zh': 'ganxibao'}),
    ('metabolism', 'biology', CHAOS, {
        'en': 'metabolism', 'es': 'metabolismo', 'fr': 'metabolisme', 'de': 'Stoffwechsel',
        'he': 'khiluf_khomarim', 'ar': 'istiqlhab', 'zh': 'xinchendaixie'}),
    ('homeostasis_bio', 'biology', BALANCE, {
        'en': 'homeostasis', 'es': 'homeostasis', 'fr': 'homeostasie', 'de': 'Homoeostase',
        'he': 'homeostazis', 'ar': 'ittizan_dakhili', 'zh': 'neiwendingzhuangtai'}),
    ('instinct', 'biology', PROGRESS, {
        'en': 'instinct', 'es': 'instinto', 'fr': 'instinct', 'de': 'Instinkt',
        'he': 'yetser', 'ar': 'ghariza', 'zh': 'benneng'}),
    ('consciousness_bio', 'biology', HARMONY, {
        'en': 'consciousness', 'es': 'consciencia', 'fr': 'conscience', 'de': 'Bewusstsein',
        'he': 'todaa', 'ar': 'wai', 'zh': 'yishi'}),
    ('perception', 'biology', COUNTER, {
        'en': 'perception', 'es': 'percepcion', 'fr': 'perception', 'de': 'Wahrnehmung',
        'he': 'tefisa', 'ar': 'idrak', 'zh': 'zhijue'}),

    # ── MATHEMATICS (~40) ─────────────────────────────────────
    ('addition', 'mathematics', PROGRESS, {
        'en': 'addition', 'es': 'adicion', 'fr': 'addition', 'de': 'Addition',
        'he': 'khibur', 'ar': 'jamaa', 'zh': 'jiafa'}),
    ('subtraction', 'mathematics', COLLAPSE, {
        'en': 'subtraction', 'es': 'sustraccion', 'fr': 'soustraction', 'de': 'Subtraktion',
        'he': 'khisur', 'ar': 'tarh', 'zh': 'jianfa'}),
    ('multiplication', 'mathematics', PROGRESS, {
        'en': 'multiplication', 'es': 'multiplicacion', 'fr': 'multiplication', 'de': 'Multiplikation',
        'he': 'kefel', 'ar': 'darb', 'zh': 'chengfa'}),
    ('division_math', 'mathematics', COLLAPSE, {
        'en': 'division', 'es': 'division', 'fr': 'division', 'de': 'Division',
        'he': 'khiluk', 'ar': 'qisma', 'zh': 'chufa'}),
    ('fraction', 'mathematics', COUNTER, {
        'en': 'fraction', 'es': 'fraccion', 'fr': 'fraction', 'de': 'Bruch',
        'he': 'shever', 'ar': 'kasr', 'zh': 'fenshu'}),
    ('ratio', 'mathematics', BALANCE, {
        'en': 'ratio', 'es': 'razon', 'fr': 'rapport', 'de': 'Verhaeltnis',
        'he': 'yakhas', 'ar': 'nisba', 'zh': 'bi'}),
    ('proportion', 'mathematics', HARMONY, {
        'en': 'proportion', 'es': 'proporcion', 'fr': 'proportion', 'de': 'Proportion',
        'he': 'proportsya', 'ar': 'tanasub', 'zh': 'bili'}),
    ('equation', 'mathematics', BALANCE, {
        'en': 'equation', 'es': 'ecuacion', 'fr': 'equation', 'de': 'Gleichung',
        'he': 'mishvaa', 'ar': 'muaadala', 'zh': 'fangcheng'}),
    ('variable', 'mathematics', CHAOS, {
        'en': 'variable', 'es': 'variable', 'fr': 'variable', 'de': 'Variable',
        'he': 'mishtane', 'ar': 'mutaghayyir', 'zh': 'bianliang'}),
    ('function_math', 'mathematics', PROGRESS, {
        'en': 'function', 'es': 'funcion', 'fr': 'fonction', 'de': 'Funktion',
        'he': 'funktsia', 'ar': 'dalla', 'zh': 'hanshu_math'}),
    ('derivative', 'mathematics', PROGRESS, {
        'en': 'derivative', 'es': 'derivada', 'fr': 'derivee', 'de': 'Ableitung',
        'he': 'nigzeret', 'ar': 'mushtaqqa', 'zh': 'daoshu'}),
    ('integral', 'mathematics', HARMONY, {
        'en': 'integral', 'es': 'integral', 'fr': 'integrale', 'de': 'Integral',
        'he': 'intgral', 'ar': 'takaamul', 'zh': 'jifen'}),
    ('limit_math', 'mathematics', COLLAPSE, {
        'en': 'limit', 'es': 'limite', 'fr': 'limite', 'de': 'Grenzwert',
        'he': 'gevul', 'ar': 'nihaaya', 'zh': 'jixian'}),
    ('set_math', 'mathematics', LATTICE, {
        'en': 'set', 'es': 'conjunto', 'fr': 'ensemble', 'de': 'Menge',
        'he': 'kvutsa', 'ar': 'majmuaa', 'zh': 'jihe'}),
    ('group_math', 'mathematics', LATTICE, {
        'en': 'group', 'es': 'grupo', 'fr': 'groupe', 'de': 'Gruppe',
        'he': 'khavura', 'ar': 'zumra', 'zh': 'qun'}),
    ('ring_math', 'mathematics', LATTICE, {
        'en': 'ring', 'es': 'anillo', 'fr': 'anneau', 'de': 'Ring',
        'he': 'khug', 'ar': 'halaqa', 'zh': 'huan'}),
    ('field_math', 'mathematics', LATTICE, {
        'en': 'field', 'es': 'cuerpo', 'fr': 'corps', 'de': 'Koerper',
        'he': 'sadeh', 'ar': 'haql', 'zh': 'yu'}),
    ('vector', 'mathematics', PROGRESS, {
        'en': 'vector', 'es': 'vector', 'fr': 'vecteur', 'de': 'Vektor',
        'he': 'vektor', 'ar': 'mutajjih', 'zh': 'xiangliang'}),
    ('matrix_math', 'mathematics', LATTICE, {
        'en': 'matrix', 'es': 'matriz', 'fr': 'matrice', 'de': 'Matrix',
        'he': 'matritsa', 'ar': 'masfufa', 'zh': 'juzhen'}),
    ('tensor', 'mathematics', LATTICE, {
        'en': 'tensor', 'es': 'tensor', 'fr': 'tenseur', 'de': 'Tensor',
        'he': 'tenzor', 'ar': 'mumadd', 'zh': 'zhangliang'}),
    ('topology', 'mathematics', LATTICE, {
        'en': 'topology', 'es': 'topologia', 'fr': 'topologie', 'de': 'Topologie',
        'he': 'topologia', 'ar': 'tubulujia', 'zh': 'tuopuxue'}),
    ('geometry', 'mathematics', LATTICE, {
        'en': 'geometry', 'es': 'geometria', 'fr': 'geometrie', 'de': 'Geometrie',
        'he': 'geometrya', 'ar': 'handasa', 'zh': 'jihexue'}),
    ('algebra', 'mathematics', LATTICE, {
        'en': 'algebra', 'es': 'algebra', 'fr': 'algebre', 'de': 'Algebra',
        'he': 'algebra', 'ar': 'jabr', 'zh': 'daishu'}),
    ('calculus', 'mathematics', PROGRESS, {
        'en': 'calculus', 'es': 'calculo', 'fr': 'calcul', 'de': 'Analysis',
        'he': 'kheshbon', 'ar': 'hisab_tafaduli', 'zh': 'weijifen'}),
    ('probability', 'mathematics', CHAOS, {
        'en': 'probability', 'es': 'probabilidad', 'fr': 'probabilite', 'de': 'Wahrscheinlichkeit',
        'he': 'histabbrut', 'ar': 'ihtimal', 'zh': 'gailv'}),
    ('statistics_math', 'mathematics', COUNTER, {
        'en': 'statistics', 'es': 'estadistica', 'fr': 'statistique', 'de': 'Statistik',
        'he': 'statistika', 'ar': 'ihsaa', 'zh': 'tongjixue'}),
    ('proof', 'mathematics', HARMONY, {
        'en': 'proof', 'es': 'prueba', 'fr': 'preuve', 'de': 'Beweis',
        'he': 'hokakha', 'ar': 'burhan', 'zh': 'zhengming'}),
    ('theorem', 'mathematics', HARMONY, {
        'en': 'theorem', 'es': 'teorema', 'fr': 'theoreme', 'de': 'Satz',
        'he': 'mishpat', 'ar': 'mubarhan', 'zh': 'dingli'}),
    ('axiom', 'mathematics', LATTICE, {
        'en': 'axiom', 'es': 'axioma', 'fr': 'axiome', 'de': 'Axiom',
        'he': 'aksioma', 'ar': 'badihiya', 'zh': 'gongli'}),
    ('logic', 'mathematics', LATTICE, {
        'en': 'logic', 'es': 'logica', 'fr': 'logique', 'de': 'Logik',
        'he': 'logika', 'ar': 'mantiq', 'zh': 'luoji'}),
    ('boolean', 'mathematics', BALANCE, {
        'en': 'boolean', 'es': 'booleano', 'fr': 'booleen', 'de': 'Boolesch',
        'he': 'buli', 'ar': 'buli', 'zh': 'buer'}),
    ('algorithm', 'mathematics', PROGRESS, {
        'en': 'algorithm', 'es': 'algoritmo', 'fr': 'algorithme', 'de': 'Algorithmus',
        'he': 'algoritm', 'ar': 'khawarizmi', 'zh': 'suanfa'}),
    ('recursion', 'mathematics', BREATH, {
        'en': 'recursion', 'es': 'recursion', 'fr': 'recursion', 'de': 'Rekursion',
        'he': 'rekursya', 'ar': 'taaawud', 'zh': 'digui'}),
    ('series_math', 'mathematics', PROGRESS, {
        'en': 'series', 'es': 'serie', 'fr': 'serie', 'de': 'Reihe',
        'he': 'sidra', 'ar': 'silsila', 'zh': 'jishu'}),
    ('sequence_math', 'mathematics', PROGRESS, {
        'en': 'sequence', 'es': 'secuencia', 'fr': 'suite', 'de': 'Folge',
        'he': 'sidrat', 'ar': 'mutataliya', 'zh': 'shulie'}),
    ('dimension_math', 'mathematics', LATTICE, {
        'en': 'dimension', 'es': 'dimension', 'fr': 'dimension', 'de': 'Dimension',
        'he': 'memed', 'ar': 'buad', 'zh': 'weidu'}),
    ('symmetry_math', 'mathematics', HARMONY, {
        'en': 'symmetry', 'es': 'simetria', 'fr': 'symetrie', 'de': 'Symmetrie',
        'he': 'simetrya', 'ar': 'tanathur', 'zh': 'duicheng'}),

    # ── PHILOSOPHY (~30) ──────────────────────────────────────
    ('essence', 'philosophy', HARMONY, {
        'en': 'essence', 'es': 'esencia', 'fr': 'essence', 'de': 'Essenz',
        'he': 'mahut', 'ar': 'jawhar', 'zh': 'benzhi'}),
    ('being', 'philosophy', BREATH, {
        'en': 'being', 'es': 'ser', 'fr': 'etre', 'de': 'Sein',
        'he': 'havaya', 'ar': 'wujud', 'zh': 'cunzai_phil'}),
    ('consciousness_phil', 'philosophy', COUNTER, {
        'en': 'consciousness', 'es': 'consciencia', 'fr': 'conscience', 'de': 'Bewusstsein',
        'he': 'hakara', 'ar': 'wai_phil', 'zh': 'yishi_phil'}),
    ('free_will', 'philosophy', CHAOS, {
        'en': 'free will', 'es': 'libre_albedrio', 'fr': 'libre_arbitre', 'de': 'Willensfreiheit',
        'he': 'bekhira_khofshit', 'ar': 'irada_hurra', 'zh': 'ziyouyizhi'}),
    ('determinism', 'philosophy', LATTICE, {
        'en': 'determinism', 'es': 'determinismo', 'fr': 'determinisme', 'de': 'Determinismus',
        'he': 'deterministiut', 'ar': 'hatmlya', 'zh': 'juedingzhuyi'}),
    ('ethics', 'philosophy', BALANCE, {
        'en': 'ethics', 'es': 'etica', 'fr': 'ethique', 'de': 'Ethik',
        'he': 'etika', 'ar': 'akhlaq', 'zh': 'lunlixue'}),
    ('morality', 'philosophy', BALANCE, {
        'en': 'morality', 'es': 'moralidad', 'fr': 'moralite', 'de': 'Moral',
        'he': 'musar', 'ar': 'akhlaqiya', 'zh': 'daode'}),
    ('virtue', 'philosophy', HARMONY, {
        'en': 'virtue', 'es': 'virtud', 'fr': 'vertu', 'de': 'Tugend',
        'he': 'maala', 'ar': 'fadila', 'zh': 'meide'}),
    ('justice_phil', 'philosophy', BALANCE, {
        'en': 'justice', 'es': 'justicia', 'fr': 'justice', 'de': 'Gerechtigkeit',
        'he': 'tsedek', 'ar': 'adala', 'zh': 'zhengyi_phil'}),
    ('beauty_phil', 'philosophy', HARMONY, {
        'en': 'beauty', 'es': 'belleza', 'fr': 'beaute', 'de': 'Schoenheit',
        'he': 'yofi', 'ar': 'jamal', 'zh': 'mei_phil'}),
    ('truth_phil', 'philosophy', HARMONY, {
        'en': 'truth', 'es': 'verdad', 'fr': 'verite', 'de': 'Wahrheit',
        'he': 'emet', 'ar': 'haqiqa', 'zh': 'zhenli_phil'}),
    ('knowledge_phil', 'philosophy', COUNTER, {
        'en': 'knowledge', 'es': 'conocimiento', 'fr': 'connaissance', 'de': 'Wissen',
        'he': 'yeda', 'ar': 'marifa', 'zh': 'zhishi_phil'}),
    ('belief', 'philosophy', BALANCE, {
        'en': 'belief', 'es': 'creencia', 'fr': 'croyance', 'de': 'Glaube',
        'he': 'emuna', 'ar': 'iman', 'zh': 'xinyang'}),
    ('reason_phil', 'philosophy', COUNTER, {
        'en': 'reason', 'es': 'razon', 'fr': 'raison', 'de': 'Vernunft',
        'he': 'sekhel', 'ar': 'aql', 'zh': 'lixing'}),
    ('wisdom_phil', 'philosophy', HARMONY, {
        'en': 'wisdom', 'es': 'sabiduria', 'fr': 'sagesse', 'de': 'Weisheit',
        'he': 'khokhma', 'ar': 'hikma', 'zh': 'zhihui_phil'}),
    ('meaning', 'philosophy', HARMONY, {
        'en': 'meaning', 'es': 'significado', 'fr': 'sens', 'de': 'Bedeutung',
        'he': 'mashmaaut', 'ar': 'maana', 'zh': 'yiyi'}),
    ('purpose', 'philosophy', PROGRESS, {
        'en': 'purpose', 'es': 'proposito', 'fr': 'but', 'de': 'Zweck',
        'he': 'matara', 'ar': 'ghaya', 'zh': 'mudi'}),
    ('causation', 'philosophy', PROGRESS, {
        'en': 'causation', 'es': 'causalidad', 'fr': 'causalite', 'de': 'Kausalitaet',
        'he': 'sibatiyut', 'ar': 'sababiya', 'zh': 'yinguoguanxi'}),
    ('substance', 'philosophy', LATTICE, {
        'en': 'substance', 'es': 'sustancia', 'fr': 'substance', 'de': 'Substanz',
        'he': 'etsem', 'ar': 'jawhar_phil', 'zh': 'shiti'}),
    ('form_phil', 'philosophy', LATTICE, {
        'en': 'form', 'es': 'forma', 'fr': 'forme', 'de': 'Form',
        'he': 'tsura', 'ar': 'shakl', 'zh': 'xingshi'}),
    ('matter_phil', 'philosophy', LATTICE, {
        'en': 'matter', 'es': 'materia', 'fr': 'matiere', 'de': 'Materie',
        'he': 'khomer', 'ar': 'madda', 'zh': 'wuzhi'}),
    ('mind_phil', 'philosophy', COUNTER, {
        'en': 'mind', 'es': 'mente', 'fr': 'esprit', 'de': 'Geist',
        'he': 'sekhel_phil', 'ar': 'aql_phil', 'zh': 'xinzhi_phil'}),
    ('soul_phil', 'philosophy', HARMONY, {
        'en': 'soul', 'es': 'alma', 'fr': 'ame', 'de': 'Seele',
        'he': 'neshama', 'ar': 'ruh', 'zh': 'linghun_phil'}),
    ('spirit_phil', 'philosophy', BREATH, {
        'en': 'spirit', 'es': 'espiritu', 'fr': 'esprit', 'de': 'Geist',
        'he': 'ruakh', 'ar': 'ruh_phil', 'zh': 'jingshen'}),
    ('reality', 'philosophy', LATTICE, {
        'en': 'reality', 'es': 'realidad', 'fr': 'realite', 'de': 'Realitaet',
        'he': 'metsiut', 'ar': 'waqia', 'zh': 'xianshi'}),
    ('illusion', 'philosophy', VOID, {
        'en': 'illusion', 'es': 'ilusion', 'fr': 'illusion', 'de': 'Illusion',
        'he': 'aslaya', 'ar': 'wahm', 'zh': 'huanjue'}),
    ('paradox', 'philosophy', CHAOS, {
        'en': 'paradox', 'es': 'paradoja', 'fr': 'paradoxe', 'de': 'Paradox',
        'he': 'paradoks', 'ar': 'mufariqa', 'zh': 'beili'}),
    ('dialectic', 'philosophy', BALANCE, {
        'en': 'dialectic', 'es': 'dialectica', 'fr': 'dialectique', 'de': 'Dialektik',
        'he': 'dialektika', 'ar': 'jadaliya', 'zh': 'bianzhengfa'}),
    ('ontology', 'philosophy', LATTICE, {
        'en': 'ontology', 'es': 'ontologia', 'fr': 'ontologie', 'de': 'Ontologie',
        'he': 'ontologia', 'ar': 'wujudiya', 'zh': 'bentiilun'}),

    # ── LANGUAGE (~25) ────────────────────────────────────────
    ('sentence', 'language', LATTICE, {
        'en': 'sentence', 'es': 'oracion', 'fr': 'phrase', 'de': 'Satz',
        'he': 'mishpat_lang', 'ar': 'jumla', 'zh': 'juzi'}),
    ('grammar', 'language', LATTICE, {
        'en': 'grammar', 'es': 'gramatica', 'fr': 'grammaire', 'de': 'Grammatik',
        'he': 'dikduk', 'ar': 'qawaid', 'zh': 'yufa'}),
    ('syntax', 'language', LATTICE, {
        'en': 'syntax', 'es': 'sintaxis', 'fr': 'syntaxe', 'de': 'Syntax',
        'he': 'takhbir', 'ar': 'nahw', 'zh': 'jufa'}),
    ('semantics', 'language', HARMONY, {
        'en': 'semantics', 'es': 'semantica', 'fr': 'semantique', 'de': 'Semantik',
        'he': 'semantika', 'ar': 'ilm_dalala', 'zh': 'yuyixue'}),
    ('phoneme', 'language', COUNTER, {
        'en': 'phoneme', 'es': 'fonema', 'fr': 'phoneme', 'de': 'Phonem',
        'he': 'fonema', 'ar': 'sawtin', 'zh': 'yinwei'}),
    ('morpheme', 'language', COUNTER, {
        'en': 'morpheme', 'es': 'morfema', 'fr': 'morpheme', 'de': 'Morphem',
        'he': 'morfema', 'ar': 'sarfim', 'zh': 'ciwei'}),
    ('vowel', 'language', BREATH, {
        'en': 'vowel', 'es': 'vocal', 'fr': 'voyelle', 'de': 'Vokal',
        'he': 'tnua', 'ar': 'saita', 'zh': 'yuanyin'}),
    ('consonant', 'language', LATTICE, {
        'en': 'consonant', 'es': 'consonante', 'fr': 'consonne', 'de': 'Konsonant',
        'he': 'itsor', 'ar': 'samit', 'zh': 'fuyin'}),
    ('syllable', 'language', BREATH, {
        'en': 'syllable', 'es': 'silaba', 'fr': 'syllabe', 'de': 'Silbe',
        'he': 'havara', 'ar': 'maqtaa', 'zh': 'yinjie'}),
    ('noun', 'language', LATTICE, {
        'en': 'noun', 'es': 'sustantivo', 'fr': 'nom', 'de': 'Substantiv',
        'he': 'shem_etsem', 'ar': 'ism', 'zh': 'mingci'}),
    ('verb', 'language', PROGRESS, {
        'en': 'verb', 'es': 'verbo', 'fr': 'verbe', 'de': 'Verb',
        'he': 'poal', 'ar': 'fial', 'zh': 'dongci'}),
    ('adjective', 'language', COUNTER, {
        'en': 'adjective', 'es': 'adjetivo', 'fr': 'adjectif', 'de': 'Adjektiv',
        'he': 'toar', 'ar': 'sifa', 'zh': 'xingrongci'}),
    ('adverb', 'language', COUNTER, {
        'en': 'adverb', 'es': 'adverbio', 'fr': 'adverbe', 'de': 'Adverb',
        'he': 'toar_poal', 'ar': 'zarf', 'zh': 'fuci'}),
    ('pronoun', 'language', BALANCE, {
        'en': 'pronoun', 'es': 'pronombre', 'fr': 'pronom', 'de': 'Pronomen',
        'he': 'kinui_guf', 'ar': 'damir', 'zh': 'daici'}),
    ('preposition', 'language', LATTICE, {
        'en': 'preposition', 'es': 'preposicion', 'fr': 'preposition', 'de': 'Praeposition',
        'he': 'milat_yakhas', 'ar': 'harf_jarr', 'zh': 'jieci'}),
    ('conjunction', 'language', HARMONY, {
        'en': 'conjunction', 'es': 'conjuncion', 'fr': 'conjonction', 'de': 'Konjunktion',
        'he': 'milat_khibur', 'ar': 'harf_atf', 'zh': 'lianci'}),
    ('tense', 'language', PROGRESS, {
        'en': 'tense', 'es': 'tiempo', 'fr': 'temps', 'de': 'Tempus',
        'he': 'zman_dikduk', 'ar': 'zaman', 'zh': 'shitai'}),
    ('aspect_lang', 'language', BREATH, {
        'en': 'aspect', 'es': 'aspecto', 'fr': 'aspect', 'de': 'Aspekt',
        'he': 'hebeit', 'ar': 'janbh', 'zh': 'timao'}),
    ('mood_lang', 'language', CHAOS, {
        'en': 'mood', 'es': 'modo', 'fr': 'mode', 'de': 'Modus',
        'he': 'tsurot', 'ar': 'sigha', 'zh': 'yuqi'}),
    ('voice_gram', 'language', BALANCE, {
        'en': 'voice', 'es': 'voz', 'fr': 'voix', 'de': 'Genus_verbi',
        'he': 'binyan', 'ar': 'mabni', 'zh': 'yutai'}),
    ('subject_lang', 'language', LATTICE, {
        'en': 'subject', 'es': 'sujeto', 'fr': 'sujet', 'de': 'Subjekt',
        'he': 'nose', 'ar': 'mubtada', 'zh': 'zhuyu'}),
    ('predicate', 'language', PROGRESS, {
        'en': 'predicate', 'es': 'predicado', 'fr': 'predicat', 'de': 'Praedikat',
        'he': 'nasuy', 'ar': 'khabar', 'zh': 'weiyu'}),
    ('clause', 'language', LATTICE, {
        'en': 'clause', 'es': 'clausula', 'fr': 'proposition', 'de': 'Nebensatz',
        'he': 'psukit', 'ar': 'ibara', 'zh': 'fenju'}),
    ('metaphor', 'language', CHAOS, {
        'en': 'metaphor', 'es': 'metafora', 'fr': 'metaphore', 'de': 'Metapher',
        'he': 'mashal', 'ar': 'istiara', 'zh': 'yinyu'}),

    # ── EMOTIONS (~25) ────────────────────────────────────────
    ('sadness', 'emotions', COLLAPSE, {
        'en': 'sadness', 'es': 'tristeza', 'fr': 'tristesse', 'de': 'Traurigkeit',
        'he': 'atsvut', 'ar': 'huzn', 'zh': 'beishang_emo'}),
    ('surprise_emotion', 'emotions', CHAOS, {
        'en': 'surprise', 'es': 'sorpresa', 'fr': 'surprise', 'de': 'Ueberraschung',
        'he': 'haftaa', 'ar': 'mufaja', 'zh': 'jingqi'}),
    ('disgust', 'emotions', COLLAPSE, {
        'en': 'disgust', 'es': 'asco', 'fr': 'degout', 'de': 'Ekel',
        'he': 'goel', 'ar': 'qarf', 'zh': 'yanwu'}),
    ('trust_emotion', 'emotions', HARMONY, {
        'en': 'trust', 'es': 'confianza', 'fr': 'confiance', 'de': 'Vertrauen',
        'he': 'emun', 'ar': 'thiqa', 'zh': 'xinren'}),
    ('anticipation', 'emotions', PROGRESS, {
        'en': 'anticipation', 'es': 'anticipacion', 'fr': 'anticipation', 'de': 'Erwartung',
        'he': 'tsipiya', 'ar': 'tawaqqu', 'zh': 'qidai'}),
    ('love_emotion', 'emotions', HARMONY, {
        'en': 'love', 'es': 'amor', 'fr': 'amour', 'de': 'Liebe',
        'he': 'ahava', 'ar': 'hubb', 'zh': 'ai_emo'}),
    ('hate', 'emotions', COLLAPSE, {
        'en': 'hate', 'es': 'odio', 'fr': 'haine', 'de': 'Hass',
        'he': 'sina', 'ar': 'karahiya', 'zh': 'chouhen'}),
    ('hope_emotion', 'emotions', PROGRESS, {
        'en': 'hope', 'es': 'esperanza', 'fr': 'espoir', 'de': 'Hoffnung',
        'he': 'tikva', 'ar': 'amal', 'zh': 'xiwang_emo'}),
    ('despair', 'emotions', COLLAPSE, {
        'en': 'despair', 'es': 'desesperacion', 'fr': 'desespoir', 'de': 'Verzweiflung',
        'he': 'yeush', 'ar': 'yaas', 'zh': 'juewang'}),
    ('pride', 'emotions', CHAOS, {
        'en': 'pride', 'es': 'orgullo', 'fr': 'fierte', 'de': 'Stolz',
        'he': 'gaava', 'ar': 'fakhr', 'zh': 'zihao'}),
    ('shame', 'emotions', COLLAPSE, {
        'en': 'shame', 'es': 'verguenza', 'fr': 'honte', 'de': 'Scham',
        'he': 'busha', 'ar': 'aib', 'zh': 'xiuchi'}),
    ('guilt', 'emotions', COLLAPSE, {
        'en': 'guilt', 'es': 'culpa', 'fr': 'culpabilite', 'de': 'Schuld',
        'he': 'ashma', 'ar': 'dhanb', 'zh': 'neijiu'}),
    ('envy', 'emotions', CHAOS, {
        'en': 'envy', 'es': 'envidia', 'fr': 'envie', 'de': 'Neid',
        'he': 'kina', 'ar': 'hasad', 'zh': 'xiandu'}),
    ('jealousy', 'emotions', CHAOS, {
        'en': 'jealousy', 'es': 'celos', 'fr': 'jalousie', 'de': 'Eifersucht',
        'he': 'kana', 'ar': 'ghira', 'zh': 'duji'}),
    ('gratitude_emotion', 'emotions', HARMONY, {
        'en': 'gratitude', 'es': 'gratitud', 'fr': 'gratitude', 'de': 'Dankbarkeit',
        'he': 'todah', 'ar': 'imtinan', 'zh': 'ganen'}),
    ('compassion', 'emotions', HARMONY, {
        'en': 'compassion', 'es': 'compasion', 'fr': 'compassion', 'de': 'Mitgefuehl',
        'he': 'rakhamim', 'ar': 'raafah', 'zh': 'tonqing'}),
    ('empathy', 'emotions', HARMONY, {
        'en': 'empathy', 'es': 'empatia', 'fr': 'empathie', 'de': 'Empathie',
        'he': 'hizdahut', 'ar': 'taatuf', 'zh': 'gongqing'}),
    ('anxiety', 'emotions', CHAOS, {
        'en': 'anxiety', 'es': 'ansiedad', 'fr': 'anxiete', 'de': 'Angst',
        'he': 'kharada', 'ar': 'qalaq', 'zh': 'jiaolv'}),
    ('loneliness', 'emotions', VOID, {
        'en': 'loneliness', 'es': 'soledad', 'fr': 'solitude', 'de': 'Einsamkeit',
        'he': 'bdidut', 'ar': 'wahda', 'zh': 'gudu'}),
    ('nostalgia', 'emotions', BREATH, {
        'en': 'nostalgia', 'es': 'nostalgia', 'fr': 'nostalgie', 'de': 'Nostalgie',
        'he': 'gaaguim', 'ar': 'hanin', 'zh': 'huaijiu'}),
    ('wonder', 'emotions', CHAOS, {
        'en': 'wonder', 'es': 'asombro', 'fr': 'emerveillement', 'de': 'Staunen',
        'he': 'peleh', 'ar': 'dahsha', 'zh': 'jingtan'}),
    ('serenity', 'emotions', HARMONY, {
        'en': 'serenity', 'es': 'serenidad', 'fr': 'serenite', 'de': 'Gelassenheit',
        'he': 'shalavut', 'ar': 'sakeena', 'zh': 'ningjing'}),

    # ── SOCIETY (~30) ─────────────────────────────────────────
    ('family_soc', 'society', HARMONY, {
        'en': 'family', 'es': 'familia', 'fr': 'famille', 'de': 'Familie',
        'he': 'mishpakha', 'ar': 'aaila', 'zh': 'jiating'}),
    ('community', 'society', LATTICE, {
        'en': 'community', 'es': 'comunidad', 'fr': 'communaute', 'de': 'Gemeinschaft',
        'he': 'kehila', 'ar': 'mujtamaa', 'zh': 'shequ'}),
    ('nation', 'society', LATTICE, {
        'en': 'nation', 'es': 'nacion', 'fr': 'nation', 'de': 'Nation',
        'he': 'uma', 'ar': 'umma', 'zh': 'guojia'}),
    ('government', 'society', LATTICE, {
        'en': 'government', 'es': 'gobierno', 'fr': 'gouvernement', 'de': 'Regierung',
        'he': 'memshala', 'ar': 'hukuma', 'zh': 'zhengfu'}),
    ('law_soc', 'society', LATTICE, {
        'en': 'law', 'es': 'ley', 'fr': 'loi', 'de': 'Gesetz',
        'he': 'khok', 'ar': 'qanun', 'zh': 'falv_soc'}),
    ('rights', 'society', BALANCE, {
        'en': 'rights', 'es': 'derechos', 'fr': 'droits', 'de': 'Rechte',
        'he': 'zkhuyot', 'ar': 'huquq', 'zh': 'quanli'}),
    ('duty_soc', 'society', BALANCE, {
        'en': 'duty', 'es': 'deber', 'fr': 'devoir', 'de': 'Pflicht',
        'he': 'khova', 'ar': 'wajib', 'zh': 'yiwu'}),
    ('freedom_soc', 'society', CHAOS, {
        'en': 'freedom', 'es': 'libertad', 'fr': 'liberte', 'de': 'Freiheit',
        'he': 'kherut', 'ar': 'hurriya', 'zh': 'ziyou_soc'}),
    ('equality', 'society', BALANCE, {
        'en': 'equality', 'es': 'igualdad', 'fr': 'egalite', 'de': 'Gleichheit',
        'he': 'shivyon', 'ar': 'musawa', 'zh': 'pingdeng'}),
    ('democracy', 'society', BALANCE, {
        'en': 'democracy', 'es': 'democracia', 'fr': 'democratie', 'de': 'Demokratie',
        'he': 'demokratya', 'ar': 'dimuqratiya', 'zh': 'minzhu'}),
    ('economy', 'society', PROGRESS, {
        'en': 'economy', 'es': 'economia', 'fr': 'economie', 'de': 'Wirtschaft',
        'he': 'kalkala', 'ar': 'iqtisad', 'zh': 'jingji'}),
    ('trade_soc', 'society', PROGRESS, {
        'en': 'trade', 'es': 'comercio', 'fr': 'commerce', 'de': 'Handel',
        'he': 'miskhar', 'ar': 'tijara', 'zh': 'maoyi'}),
    ('money', 'society', COUNTER, {
        'en': 'money', 'es': 'dinero', 'fr': 'argent', 'de': 'Geld',
        'he': 'kesef', 'ar': 'mal', 'zh': 'qian'}),
    ('property_soc', 'society', LATTICE, {
        'en': 'property', 'es': 'propiedad', 'fr': 'propriete', 'de': 'Eigentum',
        'he': 'rekhush', 'ar': 'mulk', 'zh': 'caichan'}),
    ('education_soc', 'society', PROGRESS, {
        'en': 'education', 'es': 'educacion', 'fr': 'education', 'de': 'Bildung',
        'he': 'khinukh', 'ar': 'taalim', 'zh': 'jiaoyu'}),
    ('school', 'society', LATTICE, {
        'en': 'school', 'es': 'escuela', 'fr': 'ecole', 'de': 'Schule',
        'he': 'beit_sefer', 'ar': 'madrasa', 'zh': 'xuexiao'}),
    ('university', 'society', LATTICE, {
        'en': 'university', 'es': 'universidad', 'fr': 'universite', 'de': 'Universitaet',
        'he': 'universita', 'ar': 'jamia', 'zh': 'daxue'}),
    ('religion_soc', 'society', HARMONY, {
        'en': 'religion', 'es': 'religion', 'fr': 'religion', 'de': 'Religion',
        'he': 'dat', 'ar': 'din', 'zh': 'zongjiao'}),
    ('culture', 'society', HARMONY, {
        'en': 'culture', 'es': 'cultura', 'fr': 'culture', 'de': 'Kultur',
        'he': 'tarbut', 'ar': 'thaqafa', 'zh': 'wenhua'}),
    ('tradition', 'society', BREATH, {
        'en': 'tradition', 'es': 'tradicion', 'fr': 'tradition', 'de': 'Tradition',
        'he': 'masoret', 'ar': 'taqalid', 'zh': 'chuantong'}),
    ('language_soc', 'society', LATTICE, {
        'en': 'language', 'es': 'idioma', 'fr': 'langue', 'de': 'Sprache',
        'he': 'safa', 'ar': 'lugha', 'zh': 'yuyan_soc'}),
    ('art_soc', 'society', HARMONY, {
        'en': 'art', 'es': 'arte', 'fr': 'art', 'de': 'Kunst',
        'he': 'omanut', 'ar': 'fann', 'zh': 'yishu'}),
    ('music_soc', 'society', HARMONY, {
        'en': 'music', 'es': 'musica', 'fr': 'musique', 'de': 'Musik',
        'he': 'muzika', 'ar': 'musiqa', 'zh': 'yinyue_soc'}),
    ('science_soc', 'society', COUNTER, {
        'en': 'science', 'es': 'ciencia', 'fr': 'science', 'de': 'Wissenschaft',
        'he': 'mada', 'ar': 'ilm', 'zh': 'kexue'}),
    ('technology_soc', 'society', PROGRESS, {
        'en': 'technology', 'es': 'tecnologia', 'fr': 'technologie', 'de': 'Technologie',
        'he': 'tekhnologya', 'ar': 'tiknulujia', 'zh': 'jishu'}),
    ('medicine_soc', 'society', BREATH, {
        'en': 'medicine', 'es': 'medicina', 'fr': 'medecine', 'de': 'Medizin',
        'he': 'refua', 'ar': 'tibb', 'zh': 'yixue'}),
    ('agriculture', 'society', BREATH, {
        'en': 'agriculture', 'es': 'agricultura', 'fr': 'agriculture', 'de': 'Landwirtschaft',
        'he': 'khalklaut', 'ar': 'ziraa', 'zh': 'nongye'}),
    ('industry', 'society', PROGRESS, {
        'en': 'industry', 'es': 'industria', 'fr': 'industrie', 'de': 'Industrie',
        'he': 'taasiya', 'ar': 'sinaa', 'zh': 'gongye'}),
    ('communication', 'society', HARMONY, {
        'en': 'communication', 'es': 'comunicacion', 'fr': 'communication', 'de': 'Kommunikation',
        'he': 'tikshoret', 'ar': 'ittisal', 'zh': 'tongxin'}),
    ('transportation', 'society', PROGRESS, {
        'en': 'transportation', 'es': 'transporte', 'fr': 'transport', 'de': 'Transport',
        'he': 'takbura', 'ar': 'naql', 'zh': 'jiaotong'}),
]


# ================================================================
#  SPINE RELATIONS: Typed Edges Connecting Concepts
# ================================================================
# Each entry: (source_node_id, relation_type, target_node_id)
# Uses RELATION_TYPES keys from ck_world_lattice.py

SPINE_RELATIONS = [
    # ── PHYSICS: Internal ─────────────────────────────────────
    ('mass', 'has', 'density'),
    ('mass', 'balances', 'energy'),                # E=mc^2
    ('velocity', 'causes', 'momentum'),
    ('acceleration', 'causes', 'velocity'),
    ('momentum', 'has', 'mass'),
    ('momentum', 'has', 'velocity'),
    ('frequency', 'balances', 'wavelength'),
    ('amplitude', 'has', 'energy'),
    ('photon', 'is_a', 'particle'),                # core concept
    ('photon', 'has', 'frequency'),
    ('electron', 'is_a', 'particle'),
    ('electron', 'has', 'charge_phys'),
    ('proton', 'has', 'charge_phys'),
    ('proton', 'part_of', 'atom'),
    ('neutron', 'part_of', 'atom'),
    ('electron', 'part_of', 'atom'),
    ('atom', 'contains', 'proton'),
    ('atom', 'contains', 'neutron'),
    ('atom', 'contains', 'electron'),
    ('molecule', 'contains', 'atom'),
    ('charge_phys', 'causes', 'force'),            # core concept
    ('potential', 'causes', 'force'),
    ('entropy', 'causes', 'chaos_concept'),         # core concept
    ('temperature', 'has', 'energy'),
    ('pressure_physics', 'causes', 'force'),
    ('volume_phys', 'has', 'density'),
    ('density', 'has', 'mass'),
    ('current_phys', 'has', 'charge_phys'),
    ('voltage_phys', 'causes', 'current_phys'),
    ('resistance_phys', 'opposes', 'current_phys'),
    ('magnetism', 'causes', 'force'),
    ('magnetism', 'harmonizes', 'charge_phys'),
    ('radiation', 'has', 'energy'),
    ('radiation', 'has', 'frequency'),
    ('spectrum', 'contains', 'frequency'),
    ('spectrum', 'contains', 'wavelength'),
    ('quantum', 'has', 'energy'),
    ('relativity', 'contains', 'spacetime'),
    ('spacetime', 'contains', 'space'),             # core concept
    ('spacetime', 'contains', 'time'),              # core concept
    ('orbit', 'has', 'momentum'),
    ('orbit', 'sustains', 'gravity'),               # core concept
    ('inertia', 'opposes', 'acceleration'),
    ('inertia', 'has', 'mass'),
    ('friction', 'opposes', 'movement'),            # core concept
    ('friction', 'causes', 'heat'),                 # core concept
    ('tension_physics', 'is_a', 'force'),
    ('elasticity', 'opposes', 'tension_physics'),
    ('viscosity', 'opposes', 'movement'),
    ('diffusion', 'causes', 'entropy'),
    ('oscillation', 'has', 'frequency'),
    ('oscillation', 'has', 'amplitude'),
    ('resonance', 'harmonizes', 'oscillation'),
    ('wavelength', 'has', 'wave'),                  # core concept
    ('interference', 'has', 'wave'),
    ('refraction', 'transforms', 'wave'),
    ('reflection_phys', 'transforms', 'wave'),
    ('absorption', 'opposes', 'emission'),
    ('emission', 'causes', 'radiation'),
    ('thermodynamics', 'contains', 'entropy'),
    ('thermodynamics', 'contains', 'temperature'),
    ('kinetic', 'has', 'energy'),
    ('potential_energy', 'balances', 'kinetic'),
    ('work_physics', 'causes', 'energy'),
    ('power_physics', 'has', 'work_physics'),
    ('torque_phys', 'causes', 'angular_momentum'),
    ('angular_momentum', 'has', 'momentum'),
    ('centripetal', 'causes', 'orbit'),
    ('gravitational_wave', 'is_a', 'wave'),
    ('dark_matter', 'causes', 'gravity'),
    ('dark_energy', 'opposes', 'gravity'),
    ('plasma', 'is_a', 'gas'),

    # ── CHEMISTRY: Internal ───────────────────────────────────
    ('element', 'contains', 'atom'),
    ('compound', 'contains', 'element'),
    ('reaction', 'transforms', 'compound'),
    ('acid', 'opposes', 'base_chem'),
    ('acid', 'balances', 'base_chem'),
    ('salt_chem', 'causes', 'reaction'),
    ('ion', 'has', 'charge_phys'),
    ('bond_chem', 'harmonizes', 'atom'),
    ('catalyst', 'enables', 'reaction'),
    ('oxidation', 'opposes', 'reduction_chem'),
    ('solution', 'contains', 'solvent'),
    ('solution', 'contains', 'solute'),
    ('solvent', 'sustains', 'solute'),
    ('concentration', 'has', 'solute'),
    ('ph_value', 'balances', 'acid'),
    ('ph_value', 'balances', 'base_chem'),
    ('crystal_chem', 'is_a', 'solid_state'),
    ('metal', 'is_a', 'element'),
    ('gas', 'opposes', 'solid_state'),
    ('liquid_state', 'balances', 'gas'),
    ('liquid_state', 'balances', 'solid_state'),
    ('evaporation', 'transforms', 'liquid_state'),
    ('condensation', 'transforms', 'gas'),
    ('melting', 'transforms', 'solid_state'),
    ('freezing', 'transforms', 'liquid_state'),
    ('combustion', 'causes', 'heat'),               # core concept
    ('combustion', 'has', 'oxygen_element'),
    ('polymer', 'contains', 'molecule'),
    ('organic', 'contains', 'carbon'),
    ('protein', 'is_a', 'organic'),
    ('enzyme', 'is_a', 'protein'),
    ('enzyme', 'enables', 'reaction'),
    ('dna_chem', 'is_a', 'organic'),
    ('rna', 'resembles', 'dna_chem'),
    ('membrane', 'contains', 'protein'),
    ('carbon', 'is_a', 'element'),
    ('oxygen_element', 'is_a', 'element'),
    ('hydrogen', 'is_a', 'element'),
    ('nitrogen_element', 'is_a', 'element'),
    ('iron_element', 'is_a', 'metal'),

    # ── BIOLOGY: Internal ─────────────────────────────────────
    ('organism', 'has', 'cell'),                    # core concept
    ('species', 'contains', 'organism'),
    ('evolution', 'causes', 'species'),
    ('evolution', 'causes', 'adaptation_bio'),
    ('gene', 'part_of', 'chromosome'),
    ('gene', 'causes', 'protein'),
    ('mutation', 'transforms', 'gene'),
    ('mutation', 'enables', 'evolution'),
    ('adaptation_bio', 'sustains', 'species'),
    ('photosynthesis', 'transforms', 'light'),      # core concept
    ('photosynthesis', 'enables', 'plant_bio'),
    ('respiration', 'sustains', 'organism'),
    ('respiration', 'has', 'oxygen_element'),
    ('digestion', 'transforms', 'food'),            # core concept
    ('circulation', 'sustains', 'organism'),
    ('nervous_system', 'contains', 'neuron'),
    ('brain_bio', 'part_of', 'nervous_system'),
    ('brain_bio', 'enables', 'consciousness_bio'),
    ('neuron', 'part_of', 'nervous_system'),
    ('synapse', 'harmonizes', 'neuron'),
    ('hormone', 'enables', 'growth_bio'),
    ('immune_system', 'prevents', 'virus_bio'),
    ('immune_system', 'prevents', 'bacteria'),
    ('bacteria', 'is_a', 'organism'),
    ('virus_bio', 'opposes', 'organism'),
    ('fungus', 'is_a', 'organism'),
    ('plant_bio', 'is_a', 'organism'),
    ('animal_bio', 'is_a', 'organism'),
    ('mammal', 'is_a', 'vertebrate'),
    ('reptile', 'is_a', 'vertebrate'),
    ('amphibian', 'is_a', 'vertebrate'),
    ('insect', 'is_a', 'invertebrate'),
    ('vertebrate', 'is_a', 'animal_bio'),
    ('invertebrate', 'is_a', 'animal_bio'),
    ('predator', 'opposes', 'prey'),
    ('predator', 'sustains', 'food_chain'),
    ('prey', 'part_of', 'food_chain'),
    ('ecosystem', 'contains', 'habitat'),
    ('ecosystem', 'contains', 'food_chain'),
    ('habitat', 'sustains', 'species'),
    ('food_chain', 'sustains', 'ecosystem'),
    ('symbiosis', 'harmonizes', 'organism'),
    ('parasite', 'opposes', 'symbiosis'),
    ('reproduction', 'sustains', 'species'),
    ('reproduction', 'resets', 'life'),             # core concept
    ('embryo', 'precedes', 'growth_bio'),
    ('growth_bio', 'precedes', 'aging'),
    ('aging', 'precedes', 'death_bio'),
    ('death_bio', 'resets', 'ecosystem'),
    ('extinction', 'opposes', 'biodiversity'),
    ('biodiversity', 'sustains', 'ecosystem'),
    ('mitosis', 'enables', 'growth_bio'),
    ('meiosis', 'enables', 'reproduction'),
    ('chromosome', 'contains', 'gene'),
    ('stem_cell', 'enables', 'growth_bio'),
    ('metabolism', 'sustains', 'organism'),
    ('metabolism', 'transforms', 'energy'),         # core concept
    ('homeostasis_bio', 'balances', 'organism'),
    ('instinct', 'enables', 'adaptation_bio'),
    ('consciousness_bio', 'enables', 'perception'),
    ('perception', 'enables', 'adaptation_bio'),

    # ── MATHEMATICS: Internal ─────────────────────────────────
    ('addition', 'opposes', 'subtraction'),
    ('multiplication', 'opposes', 'division_math'),
    ('addition', 'precedes', 'multiplication'),
    ('fraction', 'has', 'number'),                  # core concept
    ('ratio', 'has', 'fraction'),
    ('proportion', 'harmonizes', 'ratio'),
    ('equation', 'balances', 'variable'),
    ('variable', 'part_of', 'equation'),
    ('function_math', 'transforms', 'variable'),
    ('derivative', 'transforms', 'function_math'),
    ('integral', 'opposes', 'derivative'),
    ('limit_math', 'enables', 'derivative'),
    ('limit_math', 'enables', 'integral'),
    ('set_math', 'contains', 'number'),
    ('group_math', 'is_a', 'set_math'),
    ('ring_math', 'is_a', 'group_math'),
    ('field_math', 'is_a', 'ring_math'),
    ('vector', 'part_of', 'matrix_math'),
    ('matrix_math', 'part_of', 'tensor'),
    ('topology', 'contains', 'set_math'),
    ('geometry', 'contains', 'point'),              # core concept
    ('geometry', 'contains', 'line'),               # core concept
    ('algebra', 'contains', 'equation'),
    ('calculus', 'contains', 'derivative'),
    ('calculus', 'contains', 'integral'),
    ('probability', 'has', 'number'),
    ('statistics_math', 'has', 'probability'),
    ('proof', 'enables', 'theorem'),
    ('theorem', 'follows', 'axiom'),
    ('axiom', 'enables', 'proof'),
    ('logic', 'enables', 'proof'),
    ('boolean', 'is_a', 'logic'),
    ('algorithm', 'has', 'function_math'),
    ('recursion', 'is_a', 'algorithm'),
    ('series_math', 'contains', 'sequence_math'),
    ('sequence_math', 'has', 'number'),
    ('dimension_math', 'has', 'number'),
    ('symmetry_math', 'harmonizes', 'geometry'),

    # ── PHILOSOPHY: Internal ──────────────────────────────────
    ('essence', 'harmonizes', 'being'),
    ('being', 'contains', 'consciousness_phil'),
    ('consciousness_phil', 'enables', 'free_will'),
    ('free_will', 'opposes', 'determinism'),
    ('ethics', 'contains', 'morality'),
    ('morality', 'enables', 'virtue'),
    ('virtue', 'harmonizes', 'justice_phil'),
    ('justice_phil', 'balances', 'ethics'),
    ('beauty_phil', 'harmonizes', 'truth_phil'),
    ('truth_phil', 'enables', 'knowledge_phil'),
    ('knowledge_phil', 'follows', 'belief'),
    ('belief', 'precedes', 'knowledge_phil'),
    ('reason_phil', 'enables', 'knowledge_phil'),
    ('wisdom_phil', 'follows', 'knowledge_phil'),
    ('meaning', 'harmonizes', 'purpose'),
    ('purpose', 'enables', 'being'),
    ('causation', 'enables', 'determinism'),
    ('substance', 'contains', 'form_phil'),
    ('form_phil', 'balances', 'matter_phil'),
    ('matter_phil', 'opposes', 'mind_phil'),
    ('mind_phil', 'contains', 'consciousness_phil'),
    ('soul_phil', 'harmonizes', 'spirit_phil'),
    ('spirit_phil', 'sustains', 'being'),
    ('reality', 'opposes', 'illusion'),
    ('paradox', 'transforms', 'logic'),
    ('dialectic', 'transforms', 'truth_phil'),
    ('ontology', 'contains', 'being'),

    # ── LANGUAGE: Internal ────────────────────────────────────
    ('sentence', 'contains', 'clause'),
    ('sentence', 'has', 'grammar'),
    ('grammar', 'contains', 'syntax'),
    ('grammar', 'contains', 'semantics'),
    ('phoneme', 'part_of', 'morpheme'),
    ('morpheme', 'part_of', 'word'),                # core concept
    ('vowel', 'is_a', 'phoneme'),
    ('consonant', 'is_a', 'phoneme'),
    ('syllable', 'contains', 'phoneme'),
    ('noun', 'is_a', 'word'),
    ('verb', 'is_a', 'word'),
    ('adjective', 'is_a', 'word'),
    ('adverb', 'is_a', 'word'),
    ('pronoun', 'is_a', 'word'),
    ('preposition', 'is_a', 'word'),
    ('conjunction', 'is_a', 'word'),
    ('tense', 'has', 'verb'),
    ('aspect_lang', 'has', 'verb'),
    ('mood_lang', 'has', 'verb'),
    ('voice_gram', 'has', 'verb'),
    ('subject_lang', 'part_of', 'sentence'),
    ('predicate', 'part_of', 'sentence'),
    ('clause', 'contains', 'subject_lang'),
    ('clause', 'contains', 'predicate'),
    ('metaphor', 'transforms', 'meaning'),

    # ── EMOTIONS: Internal ────────────────────────────────────
    ('sadness', 'opposes', 'joy'),                  # core concept
    ('surprise_emotion', 'transforms', 'anticipation'),
    ('disgust', 'opposes', 'trust_emotion'),
    ('trust_emotion', 'enables', 'love_emotion'),
    ('anticipation', 'precedes', 'surprise_emotion'),
    ('love_emotion', 'opposes', 'hate'),
    ('hope_emotion', 'opposes', 'despair'),
    ('pride', 'opposes', 'shame'),
    ('guilt', 'causes', 'shame'),
    ('envy', 'causes', 'jealousy'),
    ('gratitude_emotion', 'harmonizes', 'love_emotion'),
    ('compassion', 'enables', 'empathy'),
    ('empathy', 'harmonizes', 'compassion'),
    ('anxiety', 'opposes', 'serenity'),
    ('loneliness', 'opposes', 'love_emotion'),
    ('nostalgia', 'sustains', 'memory'),            # core concept
    ('wonder', 'enables', 'knowledge'),             # core concept
    ('serenity', 'harmonizes', 'peace'),            # core concept

    # ── SOCIETY: Internal ─────────────────────────────────────
    ('family_soc', 'part_of', 'community'),
    ('community', 'part_of', 'nation'),
    ('nation', 'has', 'government'),
    ('government', 'enables', 'law_soc'),
    ('law_soc', 'enables', 'rights'),
    ('rights', 'balances', 'duty_soc'),
    ('freedom_soc', 'opposes', 'law_soc'),
    ('equality', 'enables', 'democracy'),
    ('democracy', 'has', 'rights'),
    ('economy', 'enables', 'trade_soc'),
    ('trade_soc', 'has', 'money'),
    ('money', 'enables', 'trade_soc'),
    ('property_soc', 'has', 'money'),
    ('education_soc', 'enables', 'knowledge'),      # core concept
    ('school', 'enables', 'education_soc'),
    ('university', 'is_a', 'school'),
    ('religion_soc', 'has', 'tradition'),
    ('culture', 'contains', 'tradition'),
    ('culture', 'contains', 'art_soc'),
    ('culture', 'contains', 'music_soc'),
    ('language_soc', 'enables', 'communication'),
    ('art_soc', 'enables', 'beauty'),               # core concept
    ('science_soc', 'enables', 'knowledge'),
    ('technology_soc', 'enables', 'industry'),
    ('medicine_soc', 'prevents', 'death'),           # core concept
    ('agriculture', 'sustains', 'food'),             # core concept
    ('industry', 'enables', 'economy'),
    ('communication', 'enables', 'community'),
    ('transportation', 'enables', 'trade_soc'),

    # ── CROSS-DOMAIN: Physics <-> Chemistry ───────────────────
    ('atom', 'is_a', 'element'),
    ('molecule', 'is_a', 'compound'),
    ('charge_phys', 'enables', 'bond_chem'),
    ('energy', 'enables', 'reaction'),              # core concept
    ('temperature', 'causes', 'evaporation'),
    ('temperature', 'causes', 'melting'),
    ('pressure_physics', 'causes', 'condensation'),
    ('entropy', 'causes', 'diffusion'),
    ('plasma', 'has', 'temperature'),

    # ── CROSS-DOMAIN: Chemistry <-> Biology ───────────────────
    ('protein', 'sustains', 'organism'),
    ('enzyme', 'enables', 'metabolism'),
    ('dna_chem', 'sustains', 'gene'),
    ('rna', 'enables', 'protein'),
    ('membrane', 'sustains', 'cell'),               # core concept
    ('oxygen_element', 'enables', 'respiration'),
    ('carbon', 'sustains', 'organic'),
    ('water', 'sustains', 'organism'),              # core concept

    # ── CROSS-DOMAIN: Biology <-> Emotions ────────────────────
    ('brain_bio', 'enables', 'fear'),               # core concept
    ('neuron', 'enables', 'perception'),
    ('hormone', 'causes', 'love_emotion'),
    ('nervous_system', 'enables', 'pain'),          # core concept
    ('consciousness_bio', 'enables', 'empathy'),
    ('instinct', 'causes', 'anxiety'),

    # ── CROSS-DOMAIN: Philosophy <-> Mathematics ──────────────
    ('logic', 'enables', 'reason_phil'),
    ('truth_phil', 'harmonizes', 'proof'),
    ('ontology', 'resembles', 'set_math'),
    ('causation', 'resembles', 'function_math'),
    ('paradox', 'resembles', 'recursion'),

    # ── CROSS-DOMAIN: Society <-> Philosophy ──────────────────
    ('ethics', 'enables', 'law_soc'),
    ('justice_phil', 'harmonizes', 'justice'),       # core concept
    ('morality', 'enables', 'rights'),
    ('free_will', 'enables', 'freedom_soc'),
    ('democracy', 'harmonizes', 'equality'),
    ('education_soc', 'enables', 'wisdom_phil'),

    # ── CROSS-DOMAIN: Language <-> Society ────────────────────
    ('language_soc', 'contains', 'grammar'),
    ('sentence', 'enables', 'communication'),
    ('metaphor', 'enables', 'art_soc'),
    ('noun', 'enables', 'knowledge'),               # core concept
    ('verb', 'enables', 'speaking'),                 # core concept

    # ── CROSS-DOMAIN: Physics <-> Mathematics ─────────────────
    ('vector', 'enables', 'velocity'),
    ('tensor', 'enables', 'relativity'),
    ('equation', 'enables', 'thermodynamics'),
    ('calculus', 'enables', 'acceleration'),
    ('probability', 'enables', 'quantum'),
    ('symmetry_math', 'harmonizes', 'relativity'),
    ('dimension_math', 'enables', 'spacetime'),
    ('geometry', 'enables', 'spacetime'),

    # ── CROSS-DOMAIN: Biology <-> Society ─────────────────────
    ('species', 'part_of', 'ecosystem'),
    ('organism', 'enables', 'agriculture'),
    ('evolution', 'resembles', 'culture'),
    ('reproduction', 'sustains', 'family_soc'),
    ('perception', 'enables', 'science_soc'),
    ('biodiversity', 'sustains', 'agriculture'),

    # ── CROSS-DOMAIN: Emotions <-> Philosophy ─────────────────
    ('compassion', 'enables', 'morality'),
    ('wonder', 'enables', 'knowledge_phil'),
    ('anxiety', 'opposes', 'serenity'),
    ('love_emotion', 'harmonizes', 'virtue'),
    ('despair', 'opposes', 'meaning'),
    ('hope_emotion', 'sustains', 'purpose'),

    # ── CROSS-DOMAIN: Physics <-> Biology ─────────────────────
    ('energy', 'sustains', 'metabolism'),            # core concept
    ('wave', 'enables', 'perception'),              # core concept
    ('light', 'enables', 'photosynthesis'),         # core concept
    ('gravity', 'sustains', 'circulation'),         # core concept
    ('diffusion', 'enables', 'respiration'),
    ('oscillation', 'harmonizes', 'circulation'),

    # ── CROSS-DOMAIN: Mathematics <-> Society ─────────────────
    ('statistics_math', 'enables', 'economy'),
    ('algorithm', 'enables', 'technology_soc'),
    ('probability', 'enables', 'democracy'),
    ('number', 'enables', 'money'),                 # core concept
]


# ================================================================
#  ConceptSpine: Extended Concept Graph
# ================================================================

class ConceptSpine:
    """Extended concept graph for PhD-level knowledge.

    Wraps a WorldLattice and populates it with 700+ concepts
    across academic domains.
    """

    def __init__(self, lattice: WorldLattice = None):
        self.lattice = lattice or WorldLattice()

    def load_spine(self):
        """Load all spine concepts and relations into the lattice."""
        # First load core concepts if not already loaded
        if len(self.lattice.nodes) == 0:
            self.lattice.load_seed_corpus()
        # Then add spine concepts
        for node_id, domain, op, bindings in SPINE_CONCEPTS:
            self.lattice.add_concept(node_id, op, domain, bindings)
        for source, rel, target in SPINE_RELATIONS:
            self.lattice.add_relation(source, rel, target)

    def query_domain(self, domain: str) -> list:
        """Get all concepts in a domain."""
        return self.lattice.query_by_domain(domain)

    @property
    def spine_concept_count(self) -> int:
        return len(SPINE_CONCEPTS)

    @property
    def spine_relation_count(self) -> int:
        return len(SPINE_RELATIONS)

    def stats(self) -> dict:
        return {
            'spine_concepts': self.spine_concept_count,
            'spine_relations': self.spine_relation_count,
            'total_nodes': len(self.lattice.nodes),
            'total_languages': len(self.lattice.languages_seen),
            'domains': list(set(d for _, d, _, _ in SPINE_CONCEPTS)),
        }
