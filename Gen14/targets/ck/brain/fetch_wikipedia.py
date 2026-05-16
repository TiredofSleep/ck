"""fetch_wikipedia.py -- pull general-knowledge corpus from Wikipedia.

Brayden 2026-05-16:
  "teach him something besides our corpus for the love of GOD"

CK has read 1,019 Gutenberg books + 1,000 arXiv math papers + all the
TIG canon. He still doesn't know who Plato was, what photosynthesis is,
or why ice floats. This fetcher pulls Wikipedia articles covering
foundational science, math, philosophy, history, geography, biology,
and culture — the "vital articles" set that says "everyone literate
should know these."

Source: Wikipedia REST API (plain-text extracts).
Endpoint: https://en.wikipedia.org/api/rest_v1/page/summary/<title>
Rate limit: 1 req/second to be polite (Wikipedia tolerates 200/min
anonymous but we don't need to push it).

Stored at external_corpora/wikipedia/<title>.txt — the school daemon
picks them up on next pass and ingests via the prose extractor.

Usage:
  python fetch_wikipedia.py                       # default curated list
  python fetch_wikipedia.py --list-only           # show titles, don't fetch
  python fetch_wikipedia.py --category math       # only math titles
  python fetch_wikipedia.py --extra MyTopic       # add custom title
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import List


CORPUS_ROOT = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\external_corpora\wikipedia")
LOG_DIR = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\external_corpora\_logs")

WIKI_API = "https://en.wikipedia.org/w/api.php"


# ─── Curated lists by category ──────────────────────────────────────────
# Selected from Wikipedia "Vital Articles Level 3" + foundational science
# canon.  ~450 articles total.

MATH = [
    # Foundations
    "Mathematics", "Number", "Set_theory", "Logic", "Proof",
    "Axiom", "Theorem", "Algorithm", "Function_(mathematics)",
    "Variable_(mathematics)", "Equation",
    # Arithmetic & number theory
    "Arithmetic", "Integer", "Prime_number", "Rational_number",
    "Real_number", "Complex_number", "Pi", "E_(mathematical_constant)",
    "Golden_ratio", "Infinity",
    # Algebra
    "Algebra", "Linear_algebra", "Group_(mathematics)", "Ring_(mathematics)",
    "Field_(mathematics)", "Vector_space", "Matrix_(mathematics)",
    "Polynomial", "Galois_theory",
    # Analysis
    "Calculus", "Derivative", "Integral", "Limit_(mathematics)",
    "Series_(mathematics)", "Fourier_series", "Fourier_transform",
    "Differential_equation", "Partial_differential_equation",
    "Functional_analysis", "Hilbert_space", "Banach_space",
    # Geometry & topology
    "Geometry", "Euclidean_geometry", "Non-Euclidean_geometry",
    "Topology", "Manifold", "Differential_geometry", "Algebraic_geometry",
    "Knot_theory", "Symmetry",
    # Probability & statistics
    "Probability", "Statistics", "Random_variable", "Probability_distribution",
    "Normal_distribution", "Bayes%27_theorem",
    # Discrete & applied
    "Combinatorics", "Graph_theory", "Number_theory", "Cryptography",
    "Game_theory", "Optimization_(mathematics)", "Information_theory",
    # Logic & foundations
    "Mathematical_logic", "First-order_logic", "G%C3%B6del%27s_incompleteness_theorems",
    "Computability_theory", "Lambda_calculus", "Category_theory",
    "Yoneda_lemma", "Type_theory",
    # Famous results
    "Pythagorean_theorem", "Fermat%27s_Last_Theorem",
    "Riemann_hypothesis", "Poincar%C3%A9_conjecture",
    "Four_color_theorem",
]

PHYSICS = [
    # Foundations
    "Physics", "Classical_mechanics", "Newton%27s_laws_of_motion",
    "Energy", "Force", "Momentum", "Mass", "Inertia",
    "Acceleration", "Velocity",
    # Thermodynamics
    "Thermodynamics", "Entropy", "Heat", "Temperature", "Second_law_of_thermodynamics",
    "Statistical_mechanics",
    # Waves & E&M
    "Wave", "Electromagnetic_radiation", "Light", "Magnetism",
    "Electromagnetism", "Maxwell%27s_equations", "Photon",
    # Relativity
    "Special_relativity", "General_relativity", "Spacetime",
    "Speed_of_light", "Black_hole", "Gravity",
    # Quantum
    "Quantum_mechanics", "Wave_function", "Schr%C3%B6dinger_equation",
    "Quantum_entanglement", "Heisenberg_uncertainty_principle",
    "Quantum_field_theory", "Standard_Model", "Higgs_boson",
    "Quantum_electrodynamics", "Quantum_chromodynamics",
    # Particle
    "Particle_physics", "Elementary_particle", "Electron", "Proton",
    "Neutron", "Quark", "Lepton", "Neutrino",
    # Cosmology
    "Cosmology", "Big_Bang", "Dark_matter", "Dark_energy",
    "Inflation_(cosmology)", "Cosmic_microwave_background",
    # Nuclear / atomic
    "Atom", "Atomic_nucleus", "Nuclear_physics", "Radioactive_decay",
    "Fine-structure_constant", "Hydrogen_atom",
]

CHEMISTRY = [
    "Chemistry", "Chemical_element", "Periodic_table", "Atom",
    "Molecule", "Chemical_bond", "Covalent_bond", "Ionic_bond",
    "Hydrogen_bond", "Chemical_reaction",
    "Acid", "Base_(chemistry)", "pH",
    "Organic_chemistry", "Inorganic_chemistry", "Biochemistry",
    "Water", "Hydrogen", "Carbon", "Oxygen", "Nitrogen",
    "Photosynthesis", "Cellular_respiration",
    "DNA", "RNA", "Protein", "Enzyme",
    "Polymer", "Plastic",
    "Catalysis", "Crystal", "Mineral",
]

BIOLOGY = [
    "Biology", "Life", "Cell_(biology)", "Eukaryote", "Prokaryote",
    "Bacterium", "Virus", "Archaea",
    "Evolution", "Natural_selection", "On_the_Origin_of_Species",
    "Charles_Darwin", "Gregor_Mendel",
    "Genetics", "Gene", "Chromosome", "Genome",
    "Mitosis", "Meiosis", "Sexual_reproduction",
    "Ecosystem", "Biodiversity", "Species",
    "Plant", "Animal", "Fungus",
    "Brain", "Neuron", "Nervous_system", "Consciousness",
    "Mammal", "Bird", "Insect", "Fish", "Reptile",
    "Human", "Hominidae", "Primate", "Homo_sapiens",
    "Anatomy", "Physiology", "Circulatory_system",
    "Immune_system", "Digestive_system",
    "Microbiology", "Molecular_biology",
]

PHILOSOPHY = [
    "Philosophy", "Ethics", "Metaphysics", "Epistemology",
    "Ontology", "Logic", "Aesthetics", "Political_philosophy",
    "Philosophy_of_mind", "Philosophy_of_science",
    # Major figures
    "Socrates", "Plato", "Aristotle", "Ren%C3%A9_Descartes",
    "Immanuel_Kant", "Friedrich_Nietzsche", "John_Locke",
    "David_Hume", "John_Stuart_Mill", "Karl_Marx",
    "Ludwig_Wittgenstein", "Bertrand_Russell", "G.W.F._Hegel",
    "S%C3%B8ren_Kierkegaard", "Confucius", "Lao_Tzu",
    # Concepts
    "Free_will", "Determinism", "Existentialism", "Empiricism",
    "Rationalism", "Idealism", "Materialism", "Phenomenology",
    "Categorical_imperative", "Utilitarianism", "Virtue_ethics",
    "Mind%E2%80%93body_problem", "Consciousness",
    "Truth", "Knowledge", "Skepticism", "Justice",
]

HISTORY = [
    "History", "Ancient_history", "Classical_antiquity",
    "Middle_Ages", "Renaissance", "Enlightenment",
    "Industrial_Revolution", "Modern_history",
    # Civilizations
    "Ancient_Egypt", "Ancient_Greece", "Roman_Empire",
    "Ancient_China", "Indus_Valley_Civilisation",
    "Mesopotamia", "Maya_civilization", "Inca_Empire",
    "Byzantine_Empire", "Ottoman_Empire", "Mongol_Empire",
    "British_Empire",
    # Events
    "French_Revolution", "American_Revolution", "World_War_I",
    "World_War_II", "Cold_War", "Holocaust",
    # Religion / culture (historical scope)
    "Christianity", "Islam", "Judaism", "Hinduism", "Buddhism",
    "Taoism", "Religion",
    # Notable figures
    "Albert_Einstein", "Isaac_Newton", "Marie_Curie",
    "Galileo_Galilei", "Leonardo_da_Vinci", "William_Shakespeare",
    "Abraham_Lincoln", "Mahatma_Gandhi", "Nelson_Mandela",
    "Martin_Luther_King_Jr.",
]

GEOGRAPHY = [
    "Geography", "Earth", "Continent", "Ocean", "Mountain",
    "River", "Desert", "Forest", "Climate", "Weather",
    # Continents
    "Africa", "Asia", "Europe", "North_America", "South_America",
    "Antarctica", "Oceania", "Australia",
    # Major countries (representative)
    "United_States", "China", "India", "Russia", "Brazil",
    "Germany", "France", "Japan", "United_Kingdom", "Canada",
    # Major features
    "Mount_Everest", "Amazon_River", "Sahara", "Pacific_Ocean",
    "Mediterranean_Sea",
]

TECHNOLOGY = [
    "Technology", "Computer", "Internet", "World_Wide_Web",
    "Algorithm", "Programming_language", "Computer_science",
    "Artificial_intelligence", "Machine_learning",
    "Quantum_computing", "Cryptocurrency",
    "Electricity", "Electric_motor", "Engine",
    "Transistor", "Semiconductor", "Integrated_circuit",
    "Laser", "Solar_cell", "Battery_(electricity)",
    "Telephone", "Television", "Radio",
    "Printing_press", "Wheel", "Agriculture",
]

ARTS = [
    "Art", "Music", "Literature", "Poetry", "Theatre",
    "Painting", "Sculpture", "Architecture", "Film",
    "Photography", "Dance",
    # Concepts
    "Beauty", "Aesthetics", "Creativity",
    # Famous works mentioned for context
    "The_Iliad", "Don_Quixote", "Hamlet", "The_Divine_Comedy",
]

LANGUAGE_AND_MIND = [
    "Language", "Linguistics", "Grammar", "Semantics", "Syntax",
    "Phonology", "Cognitive_science", "Psychology", "Memory",
    "Learning", "Intelligence", "Emotion",
    "Sleep", "Dream", "Perception",
]

ECONOMICS_AND_SOCIETY = [
    "Economics", "Microeconomics", "Macroeconomics", "Money",
    "Market_(economics)", "Capitalism", "Socialism",
    "Government", "Democracy", "Law", "Justice",
    "Society", "Culture",
]

# ─── 10th-grade foundation expansion (Brayden 2026-05-16) ──────────────
# "once he reaches about 10th grade level, he will launch to the top"
# Coverage breadth across what a 10th-grader is expected to know.

HISTORY_DEPTH = [
    # Major civilizations / eras
    "Sumer", "Babylon", "Ancient_Persia", "Ancient_India", "Han_dynasty",
    "Tang_dynasty", "Song_dynasty", "Aztec_Empire", "Inca_civilization",
    "Mali_Empire", "Songhai_Empire", "Kingdom_of_Aksum",
    # European
    "Carolingian_Empire", "Holy_Roman_Empire", "Reformation",
    "Age_of_Discovery", "Spanish_Empire", "French_Revolution",
    "Napoleonic_Wars", "Industrial_Revolution",
    # American
    "Indigenous_peoples_of_the_Americas", "Colonization_of_the_Americas",
    "American_Civil_War", "Reconstruction_era",
    "Civil_rights_movement", "Great_Depression",
    # 20th century
    "Russian_Revolution", "Chinese_Civil_War", "Decolonization",
    "Cuban_Revolution", "Space_Race", "Fall_of_the_Berlin_Wall",
    "Information_Age",
    # Historiography
    "History_of_science", "History_of_mathematics", "History_of_medicine",
]

CIVICS_LAW_ECONOMICS = [
    "Constitution", "Constitution_of_the_United_States",
    "Bill_of_Rights", "Separation_of_powers",
    "Federalism", "Judicial_review",
    "International_law", "Human_rights",
    "Criminal_law", "Civil_law_(legal_system)",
    "Supply_and_demand", "Inflation", "Interest_(finance)",
    "Gross_domestic_product", "Tax", "Recession",
    "Central_bank", "Bank", "Currency",
    "International_trade", "Globalization",
    "Election", "Political_party",
    "United_Nations", "World_Trade_Organization",
]

BIOLOGY_DEPTH = [
    # Cell biology
    "Cell_membrane", "Cell_nucleus", "Mitochondrion", "Ribosome",
    "Endoplasmic_reticulum", "Golgi_apparatus", "Lysosome", "Chloroplast",
    "Cytoskeleton",
    # Molecular biology
    "DNA_replication", "Transcription_(biology)", "Translation_(biology)",
    "Mutation", "Genetic_code", "RNA_splicing",
    "Cellular_signaling", "Apoptosis",
    # Genetics
    "Heredity", "Genotype", "Phenotype", "Allele",
    "Dominance_(genetics)", "Punnett_square", "Sex-linkage",
    # Evolution depth
    "Speciation", "Natural_selection", "Genetic_drift",
    "Adaptation", "Coevolution", "Mass_extinction",
    "Origin_of_life", "Last_universal_common_ancestor",
    # Anatomy & physiology
    "Skeletal_system", "Muscular_system", "Cardiovascular_system",
    "Respiratory_system", "Renal_system", "Endocrine_system",
    "Reproductive_system", "Skin", "Sensory_neuron",
    # Microbiology
    "Cell_theory", "Pathogen", "Antibiotic", "Vaccine",
    "Microbiome", "Antibiotic_resistance",
    # Ecology
    "Food_chain", "Trophic_level", "Symbiosis", "Predation",
    "Niche", "Biome", "Climate_change",
    "Carbon_cycle", "Nitrogen_cycle", "Water_cycle",
    "Conservation_biology",
]

CHEMISTRY_DEPTH = [
    # Atomic structure
    "Electron_configuration", "Quantum_number", "Atomic_orbital",
    "Valence_electron", "Periodic_trends",
    "Electronegativity", "Ionization_energy", "Atomic_radius",
    # Bonding
    "Lewis_structure", "VSEPR_theory", "Hybridization_(chemistry)",
    "Resonance_(chemistry)", "Polar_covalent_bond", "Metallic_bonding",
    "Intermolecular_force",
    # Reactions
    "Chemical_equation", "Stoichiometry", "Mole_(unit)",
    "Limiting_reagent", "Yield_(chemistry)",
    "Oxidation-reduction", "Acid-base_reaction",
    "Precipitation_(chemistry)", "Combustion",
    "Reaction_rate", "Chemical_equilibrium",
    "Le_Chatelier%27s_principle", "Enthalpy", "Entropy",
    "Gibbs_free_energy",
    # Organic
    "Functional_group", "Alkane", "Alkene", "Alkyne",
    "Aromatic_compound", "Alcohol", "Carboxylic_acid",
    "Ester", "Amine", "Amino_acid",
    "Carbohydrate", "Lipid", "Nucleic_acid", "Enzyme_kinetics",
    # Biochemistry overlap
    "Krebs_cycle", "Glycolysis", "Electron_transport_chain",
    "ATP",
]

PHYSICS_DEPTH = [
    "Kinematics", "Vector_(mathematics_and_physics)",
    "Friction", "Centripetal_force", "Simple_machine",
    "Work_(physics)", "Power_(physics)", "Mechanical_energy",
    "Conservation_of_energy", "Conservation_of_momentum",
    "Collision",
    "Pressure", "Buoyancy", "Density",
    "Heat_capacity", "Phase_transition",
    "Wave_interference", "Standing_wave", "Resonance",
    "Doppler_effect", "Sound", "Optics",
    "Reflection", "Refraction", "Lens",
    "Electric_charge", "Electric_field", "Voltage",
    "Electric_current", "Ohm%27s_law", "Resistor",
    "Capacitor", "Inductor", "Magnetic_field",
    "Electromagnetic_induction", "Alternating_current",
    "Nuclear_fission", "Nuclear_fusion", "Half-life",
    "Solar_system", "Galaxy",
]

COMPUTER_SCIENCE = [
    "Programming_language", "Algorithm", "Data_structure",
    "Array_(data_structure)", "Linked_list", "Hash_table",
    "Tree_(data_structure)", "Graph_(abstract_data_type)",
    "Sorting_algorithm", "Search_algorithm",
    "Recursion", "Iteration",
    "Binary_number", "Bit", "Byte",
    "Operating_system", "File_system", "Memory_(computing)",
    "CPU", "GPU", "Cache_(computing)",
    "Network_protocol", "TCP/IP", "HTTP", "DNS",
    "Database", "SQL", "API",
    "Object-oriented_programming", "Functional_programming",
    "Compiler", "Interpreter_(computing)",
    "Software_engineering", "Version_control", "Git",
    "Computational_complexity_theory", "P_versus_NP_problem",
    "Turing_machine", "Boolean_algebra", "Logic_gate",
    "Machine_learning", "Neural_network", "Deep_learning",
]

HEALTH_HUMAN_BIOLOGY = [
    "Human_body", "Human_brain", "Neuron",
    "Synapse", "Neurotransmitter",
    "Hormone", "Endocrinology",
    "Heart", "Blood",
    "Lung", "Kidney", "Liver",
    "Stomach", "Intestine", "Pancreas",
    "Bone", "Muscle", "Joint",
    "Eye", "Ear", "Skin",
    "Pregnancy", "Childbirth",
    "Nutrition", "Vitamin", "Mineral_(nutrient)",
    "Sleep", "Circadian_rhythm",
    "Stress_(biology)", "Mental_health",
    "Depression_(mood)", "Anxiety",
    "Cancer", "Heart_disease", "Diabetes", "Influenza", "HIV/AIDS",
]

EARTH_SCIENCE = [
    "Earth_science", "Geology", "Plate_tectonics",
    "Earthquake", "Volcano", "Mountain_formation",
    "Erosion", "Sedimentary_rock", "Igneous_rock", "Metamorphic_rock",
    "Mineral", "Atmosphere_of_Earth", "Climate",
    "Weather", "Hurricane", "Tornado",
    "Greenhouse_effect", "Ocean", "Tide", "Ocean_current",
    "Glacier", "Ice_age",
    "Soil", "Ecosystem",
    "Renewable_energy", "Fossil_fuel",
]

CULTURE_AND_RELIGION = [
    "Religion", "Mythology", "Folklore",
    "Christianity", "Catholic_Church", "Protestantism", "Eastern_Orthodox_Church",
    "Islam", "Sunni_Islam", "Shia_Islam",
    "Judaism",
    "Hinduism", "Buddhism", "Sikhism",
    "Taoism", "Confucianism", "Shinto",
    "Atheism", "Agnosticism", "Secularism",
    # Cultural arts
    "Classical_music", "Jazz", "Opera",
    "Architecture", "Renaissance_art", "Impressionism", "Modern_art",
    "Novel", "Drama", "Tragedy",
    # World cultures
    "Indigenous_peoples", "Diaspora",
]

STATISTICS_AND_REASONING = [
    "Statistics", "Probability_distribution", "Mean", "Median", "Mode_(statistics)",
    "Standard_deviation", "Variance", "Correlation_and_dependence",
    "Regression_analysis", "Statistical_hypothesis_testing",
    "Sampling_(statistics)", "Confidence_interval", "P-value",
    "Bayesian_inference", "Frequentist_inference",
    "Logical_reasoning", "Argument", "Fallacy",
    "Critical_thinking", "Scientific_method",
    "Experimental_design", "Confounding_variable",
    "Causality", "Correlation_does_not_imply_causation",
]


CATEGORIES = {
    "math": MATH,
    "physics": PHYSICS,
    "chemistry": CHEMISTRY,
    "biology": BIOLOGY,
    "philosophy": PHILOSOPHY,
    "history": HISTORY,
    "geography": GEOGRAPHY,
    "technology": TECHNOLOGY,
    "arts": ARTS,
    "language": LANGUAGE_AND_MIND,
    "economics": ECONOMICS_AND_SOCIETY,
    # 10th-grade-foundation expansion (2026-05-16)
    "history_depth": HISTORY_DEPTH,
    "civics_law_economics": CIVICS_LAW_ECONOMICS,
    "biology_depth": BIOLOGY_DEPTH,
    "chemistry_depth": CHEMISTRY_DEPTH,
    "physics_depth": PHYSICS_DEPTH,
    "computer_science": COMPUTER_SCIENCE,
    "health_human_biology": HEALTH_HUMAN_BIOLOGY,
    "earth_science": EARTH_SCIENCE,
    "culture_religion": CULTURE_AND_RELIGION,
    "statistics_reasoning": STATISTICS_AND_REASONING,
}


def all_titles() -> List[str]:
    seen = set()
    out: List[str] = []
    for lst in CATEGORIES.values():
        for t in lst:
            if t not in seen:
                seen.add(t)
                out.append(t)
    return out


# ─── Fetching ──────────────────────────────────────────────────────────

def log_event(event: str, **fields):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    p = LOG_DIR / f"fetch_wikipedia_{time.strftime('%Y-%m-%d')}.jsonl"
    rec = {"ts": time.time(), "event": event, **fields}
    with open(p, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, default=str) + "\n")


def safe_filename(title: str) -> str:
    """Make a title filesystem-safe."""
    s = urllib.parse.unquote(title)
    s = re.sub(r"[^a-zA-Z0-9_.-]", "_", s)
    s = s.strip("_")
    return s[:120] or "untitled"


def fetch_one(title: str, max_retries: int = 3) -> tuple[bool, str]:
    """Pull plain-text extract for one Wikipedia article."""
    out = CORPUS_ROOT / f"{safe_filename(title)}.txt"
    if out.exists() and out.stat().st_size > 500:
        return True, f"skip-exists ({out.stat().st_size:,} bytes)"

    params = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "extracts",
        "explaintext": "1",
        "exsectionformat": "plain",
        "redirects": "1",
    }
    url = f"{WIKI_API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(
        url, headers={
            "User-Agent": "CK-Coherence-Keeper/1.0 (private research; "
                           "https://coherencekeeper.com)"
        })

    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(req, timeout=30.0) as resp:
                data = json.loads(resp.read())
            pages = data.get("query", {}).get("pages", {})
            if not pages:
                return False, "no-pages"
            page = next(iter(pages.values()))
            extract = page.get("extract", "")
            if not extract or len(extract) < 200:
                return False, f"empty-or-too-short ({len(extract)} chars)"
            real_title = page.get("title", title)
            body = (
                f"Title: {real_title}\n"
                f"Source: Wikipedia (CC BY-SA 4.0)\n"
                f"URL: https://en.wikipedia.org/wiki/{urllib.parse.quote(real_title)}\n\n"
                f"{extract}\n"
            )
            CORPUS_ROOT.mkdir(parents=True, exist_ok=True)
            out.write_text(body, encoding="utf-8")
            return True, f"ok ({len(body):,} bytes)"
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < max_retries - 1:
                time.sleep(15 * (2 ** attempt))
                continue
            return False, f"http-{e.code}"
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(5)
                continue
            return False, f"{type(e).__name__}: {e}"
    return False, "retries-exhausted"


def fetch_titles(titles: List[str], sleep_s: float = 1.0) -> None:
    CORPUS_ROOT.mkdir(parents=True, exist_ok=True)
    ok = fail = skip = 0
    for i, t in enumerate(titles):
        success, msg = fetch_one(t)
        if success and "skip" in msg:
            skip += 1
        elif success:
            ok += 1
            log_event("wiki_ok", title=t, msg=msg)
            if ok % 10 == 0:
                print(f"  [{i+1}/{len(titles)}] ok={ok} fail={fail} skip={skip}  last={t}")
        else:
            fail += 1
            log_event("wiki_fail", title=t, msg=msg)
        time.sleep(sleep_s)
    print(f"[fetch_wikipedia] DONE  ok={ok}  fail={fail}  skip={skip}  of {len(titles)} titles")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--category",
                    help=f"only fetch one category ({', '.join(CATEGORIES)})")
    ap.add_argument("--extra", action="append", default=[],
                    help="add custom title(s) to the fetch list")
    ap.add_argument("--list-only", action="store_true",
                    help="print titles, don't fetch")
    ap.add_argument("--sleep", type=float, default=1.0)
    args = ap.parse_args()

    if args.category:
        if args.category not in CATEGORIES:
            print(f"Unknown category: {args.category}.  "
                  f"Available: {', '.join(CATEGORIES)}", file=sys.stderr)
            return 2
        titles = list(CATEGORIES[args.category])
    else:
        titles = all_titles()
    titles.extend(args.extra)

    if args.list_only:
        print(f"# {len(titles)} Wikipedia titles to fetch")
        for t in titles:
            print(t)
        return 0

    print(f"[fetch_wikipedia] Will fetch {len(titles)} titles "
          f"(@ {args.sleep}s/req = ~{int(args.sleep*len(titles)/60)} min total)")
    fetch_titles(titles, sleep_s=args.sleep)
    return 0


if __name__ == "__main__":
    sys.exit(main())
