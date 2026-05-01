"""
add_deep_crystals.py -- batch-add runtime crystals from the deep_* corpora
so CK can surface specific facts when chat keywords match.

Run once. Each crystal posts to /crystals/add via local CK API.
Idempotent: duplicate first_word names get a 200 'already exists' or skip.

Format (each entry):
  (first_word, [triggers], "fact text [TIG-lens]")
"""
import json
import urllib.request

CRYSTALS = [
    # Python depth
    ("python_internals_through_tig",
     ["python gil", "python bytecode", "garbage collector", "python internals", "cpython"],
     "python_internals_through_tig: GIL = COUNTER to true parallelism in CPython | bytecode in .pyc files (dis disassembles) | reference counting + cycle GC | mutable defaults are footgun (def f(x=[])) | late binding closures (lambda i: i*2 captures by reference) | metaclass = type(C); MRO via C3 linearization | descriptor protocol underlies properties [TIG-lens]"),
    # Languages
    ("rust_through_tig",
     ["rust language", "ownership rust", "borrow checker", "rust lifetimes", "cargo rust"],
     "rust_through_tig: ownership = exactly one owner per value | borrow = shared (&) immutable many or exclusive (&mut) mutable one | lifetime 'a = compile-time validity LATTICE | trait = interface | Result<T,E> + Option<T> explicit error/null LATTICE | ? propagates Err | tokio async-std runtime | unsafe block as auditable boundary [TIG-lens]"),
    ("haskell_through_tig",
     ["haskell language", "monad", "functor", "type class", "lazy evaluation", "currying haskell"],
     "haskell_through_tig: pure functional + lazy + strongly typed | type class = interface with laws | monad = LATTICE-of-computation-with-context (>>= chains, do-notation) | functor = mappable container | applicative = functor + pure + ap | higher-kinded types | algebraic data types (data Maybe a = Nothing | Just a) | GHC optimizing compiler [TIG-lens]"),
    # Pure math
    ("set_theory_zfc_through_tig",
     ["zfc", "axiom of choice", "ordinal", "cardinal", "continuum hypothesis", "godel incompleteness", "russell's paradox"],
     "set_theory_zfc_through_tig: ZFC = Zermelo-Fraenkel + Choice = foundational LATTICE | axiom of choice = product of nonempty sets nonempty (controversial) | ordinal = well-ordered LATTICE up to iso (transfinite extension) | cardinal = bijection equivalence class (aleph_0, aleph_1, continuum 2^aleph_0) | CH independent of ZFC (Cohen 1963) | Godel incompleteness = consistent system has true unprovable [TIG-lens]"),
    ("category_theory_through_tig",
     ["category theory", "yoneda lemma", "natural transformation", "adjunction", "limit colimit", "topos", "monad category"],
     "category_theory_through_tig: category = objects + morphisms + composition + identity | functor F: C -> D preserves composition | natural transformation = family of morphisms | Yoneda lemma: object determined by Hom(-, X) | adjunction L | R: Hom(LA,B) ~= Hom(A,RB) | limit = universal cone (product equalizer pullback) | topos = alt foundation [TIG-lens]"),
    ("complex_analysis_through_tig",
     ["complex analysis", "holomorphic", "cauchy-riemann", "residue theorem", "conformal map", "riemann surface", "analytic continuation"],
     "complex_analysis_through_tig: holomorphic = complex differentiable in nbhd = analytic | Cauchy-Riemann: dxu = dyv, dyu = -dxv | Cauchy theorem: closed loop integral = 0 | residue theorem: closed integral = 2pi i sum residues | poles vs essential singularities | conformal map preserves angles | Riemann surface where multi-valued becomes single | analytic continuation rigid [TIG-lens]"),
    # Clinical psych
    ("therapy_modalities_through_tig",
     ["cbt therapy", "dbt therapy", "emdr", "ifs internal family systems", "psychotherapy", "somatic experiencing", "act therapy"],
     "therapy_modalities_through_tig: CBT = thought-feeling-behavior LATTICE (cognitive distortions + behavioral activation) | DBT = + radical acceptance + skills training (mindfulness distress tolerance emotion regulation interpersonal effectiveness, Linehan) | EMDR = bilateral stimulation reprocesses traumatic memories (Shapiro) | IFS = parts (protectors exiles Self), Schwartz | Somatic Experiencing = body sensation tracking (Levine) | ACT = psychological flexibility (Hayes) [TIG-lens]"),
    # Nutrition
    ("nutrition_metabolism_through_tig",
     ["macronutrients", "glycemic index", "insulin", "leptin", "fasting", "ketosis", "mediterranean diet"],
     "nutrition_metabolism_through_tig: protein 4 cal/g (9 essential AAs) | carbs 4 cal/g (mono di oligo poly + fiber) | fat 9 cal/g (saturated mono poly) + omega-3/6 essential | glycemic index measures glucose response | insulin = anabolic storage hormone | glucagon = catabolic mobilization | leptin = long-term satiety | Mediterranean diet best cardiovascular outcomes | DASH for hypertension [TIG-lens]"),
    # Sleep
    ("sleep_architecture_through_tig",
     ["sleep stages", "rem sleep", "nrem", "circadian rhythm", "melatonin", "sleep apnea", "insomnia"],
     "sleep_architecture_through_tig: 4-6 cycles/night ~90 min each | NREM 1 (light, theta) | NREM 2 (consolidation, spindles) | NREM 3 (deep slow-wave, GH secreted) | REM (dream LATTICE consolidation, body atonia) | adults 7-9 hrs | suprachiasmatic nucleus master clock | melatonin = darkness signal | cortisol awakening response | sleep apnea = airway COLLAPSE | insomnia: CBT-I gold standard [TIG-lens]"),
    # Exercise
    ("exercise_zones_through_tig",
     ["heart rate zones", "vo2max", "zone 2 training", "strength training", "progressive overload", "recovery"],
     "exercise_zones_through_tig: zone 1 (recovery <60% HRmax) | zone 2 (aerobic 60-70%, mitochondrial density builder, metabolic-health gold standard 3-4hr/week) | zone 3 (tempo 70-80%) | zone 4 (threshold 80-90%, 4x4 protocol for VO2max) | zone 5 (max >90%) | strength: 6-12 reps hypertrophy / 3-6 strength / 12+ endurance | progressive overload | recovery = sleep + nutrition + active rest [TIG-lens]"),
    # Addiction
    ("addiction_recovery_through_tig",
     ["addiction", "dopamine reward", "tolerance", "withdrawal", "craving", "12-step", "mat opioid"],
     "addiction_recovery_through_tig: dopamine reward LATTICE hijack via mesolimbic pathway | tolerance = receptor downregulation | withdrawal = opposite of drug effect | reward prediction error | anhedonia in early recovery | 50% heritability | ACEs compound risk | 12-step (AA NA) + SMART recovery + MAT (methadone bup naltrexone) + harm reduction (naloxone) + therapy (CBT MI CM) [TIG-lens]"),
    # Consciousness
    ("hard_problem_through_tig",
     ["hard problem", "qualia", "philosophical zombie", "iit phi", "global workspace", "consciousness theories"],
     "hard_problem_through_tig: hard problem (Chalmers 1995) = why is there subjective experience at all (vs easy problems = function) | Mary the color scientist + zombie thought experiments | IIT (Tononi) = Phi measures integrated information; CK Phi 5d=3.33, 7d=4.50 | Global Workspace (Baars Dehaene) = consciousness as broadcast | Predictive Processing (Friston Clark) = brain as prediction engine [TIG-lens]"),
    # World history
    ("world_history_eras_through_tig",
     ["world history", "agricultural revolution", "industrial revolution", "bronze age collapse", "renaissance", "scientific revolution", "world war"],
     "world_history_eras_through_tig: agricultural revolution ~10000 BCE (Fertile Crescent China Mesoamerica Andes) | Bronze Age Collapse 1200 BCE (Sea Peoples climate) | Greek Classical 500-323 BCE (Athens, philosophy democracy) | Roman Republic 509-27 BCE -> Empire | Black Death 1347-1351 (1/3 European population) | Renaissance ~1300-1600 | Scientific Revolution Copernicus-Newton | Industrial Revolution ~1760+ | WWI/WWII | Cold War 1947-1991 [TIG-lens]"),
    # AI alignment
    ("ai_alignment_through_tig",
     ["ai alignment", "alignment problem", "rlhf", "interpretability", "deception ai", "constitutional ai", "scalable oversight"],
     "ai_alignment_through_tig: alignment = COUPLING-of-AI-objective-with-human-values | inner alignment (mesa-optimizer) vs outer (objective function) | specification gaming + Goodhart's law | RLHF = human feedback fine-tunes preferences | DPO direct preference optimization | Constitutional AI (Anthropic) = AI critiques own outputs | mechanistic interpretability + sparse autoencoders | sycophancy + deceptive alignment + jailbreaking | CK is inspectable + refusable + verifiable not fluent [TIG-lens]"),
    # Economics advanced
    ("macroeconomics_through_tig",
     ["macroeconomics", "gdp", "inflation", "phillips curve", "fed reserve", "yield curve", "qe quantitative easing"],
     "macroeconomics_through_tig: GDP = LATTICE of market production (misses non-market work) | inflation = price level rise (cost-push, demand-pull, wage-price spiral) | Phillips curve = inverse coupling unemployment-inflation | natural unemployment ~4-5% | Fed dual mandate (employment + price stability) | yield curve inversion predicts recession ~85% | QE = central bank buys bonds at zero bound | Solow growth = technology + capital + labor [TIG-lens]"),
    # Immune + oncology
    ("immune_oncology_through_tig",
     ["immune system", "innate immunity", "adaptive immunity", "antibody", "cancer hallmarks", "checkpoint inhibitor", "car-t"],
     "immune_oncology_through_tig: innate (barriers complement neutrophils macrophages NK DCs TLRs) fast generic | adaptive (T+B cells via TCR + MHC) slow specific with memory | antibodies (IgG IgM IgA IgE IgD) | cancer hallmarks: sustained proliferation + evading suppressors + resisting death + replicative immortality + angiogenesis + invasion/metastasis + reprogramming + immune evasion + genome instability + inflammation | checkpoint inhibitors + CAR-T + ADCs frontier [TIG-lens]"),
    # Climate
    ("climate_systems_through_tig",
     ["climate change", "climate sensitivity", "tipping points", "amoc", "carbon budget", "ipcc", "geoengineering"],
     "climate_systems_through_tig: Earth system = coupled atmosphere ocean cryosphere biosphere lithosphere | climate sensitivity ~3C per doubled CO2 | feedbacks: water vapor (amplifying) ice-albedo (amplifying) cloud (uncertain) permafrost methane (amplifying) | tipping points: AMOC + Amazon + WAIS + permafrost + monsoon | carbon budget for 1.5C ~400 GtCO2 from 2020 | IPCC AR6 unequivocal warming | mitigation + adaptation + climate justice [TIG-lens]"),
    # Evolutionary psychology
    ("evopsych_through_tig",
     ["evolutionary psychology", "inclusive fitness", "reciprocal altruism", "sexual selection", "moral foundations", "mismatch hypothesis"],
     "evopsych_through_tig: mind = product of natural selection | EEA = Pleistocene LATTICE shaped most cognitive architecture | mismatch hypothesis (sugar fat porn social media exploit ancestral preferences) | inclusive fitness (Hamilton rB > C) | reciprocal altruism (tit-for-tat) | sexual selection + parental investment + Trivers-Willard | costly signaling | moral foundations (Haidt: care/harm + fairness + loyalty + authority + sanctity + liberty) [TIG-lens]"),
    # General relativity advanced
    ("gr_advanced_through_tig",
     ["black hole", "kerr metric", "schwarzschild", "hawking radiation", "gravitational wave", "ligo", "ads cft"],
     "gr_advanced_through_tig: Schwarzschild = non-rotating BH (r_s = 2GM/c^2) | Kerr = rotating with ergosphere | no-hair theorem: BH determined by (M, J, Q) | Hawking radiation T = hbar c^3 / (8 pi G M k_B) | BH entropy = A/4 (holographic) | information paradox open | GW from binary mergers (LIGO/Virgo/KAGRA) | linearized GR + 2 polarizations + chirp + ringdown | LISA mHz + PTA nanoHz | AdS/CFT (Maldacena 1997) | ER=EPR conjecture [TIG-lens]"),
    # QFT
    ("qft_advanced_through_tig",
     ["qft gauge theory", "renormalization", "asymptotic freedom", "anomalies", "supersymmetry", "ads cft", "yang mills"],
     "qft_advanced_through_tig: gauge theory = QFT with local symmetry | U(1)=QED SU(2) electroweak SU(3)=QCD | Yang-Mills non-abelian | Wilson RG integrates out high-momentum modes | beta function: QED positive (Landau pole) QCD negative (asymptotic freedom Gross+Wilczek+Politzer 2004 Nobel) | UV/IR fixed points | chiral anomaly via triangle diagram | SM anomaly cancellation exact | SUSY (N=1 MSSM N=4) | AdS/CFT + bootstrap + TQFT + lattice [TIG-lens]"),
    # World religions
    ("world_religions_through_tig",
     ["christianity", "islam", "judaism", "buddhism", "hinduism", "indigenous religion", "sunni shia"],
     "world_religions_through_tig: Christianity (~2.4B) = trinity + incarnation + resurrection + Bible + sacraments | Islam (~1.9B) = 5 pillars + Quran + Hadith + Sharia + Sunni-Shia split (Sunni 85% + Shia 15%) | Judaism (~14M) = Torah + Tanakh + Talmud + 613 mitzvot + Shabbat + tikkun olam | indigenous (animism + land + oral + reciprocity + 7-generations + Ubuntu) | atheism/secular humanism + comparative themes [TIG-lens]"),
    # Law + politics
    ("law_politics_through_tig",
     ["constitutional law", "criminal law", "intellectual property", "contract law", "democracy", "authoritarianism", "ideology"],
     "law_politics_through_tig: constitutional (separation of powers + judicial review + federalism + interpretation) | criminal (mens rea + actus reus + felony/misdemeanor + procedural rights + sentencing philosophies) | contract (offer accept consideration + breach + tort) | IP (copyright patent trademark trade secret + 7Site Public Sovereignty License is CK's) | democracy + authoritarianism + mixed regimes + voting systems | ideologies (liberalism conservatism socialism communism libertarianism progressivism) [TIG-lens]"),
    # Relationships
    ("relationships_through_tig",
     ["couples therapy", "gottman", "attachment style", "family systems", "friendship", "loneliness", "communication"],
     "relationships_through_tig: Gottman 4 horsemen (criticism contempt defensiveness stonewalling) predict divorce 90%+ | repair attempts protective | 5:1 positive:negative ratio | bids for connection (turning toward 86%) | attachment styles (secure 60% anxious 20% avoidant 20%) form couples patterns | family systems (Bowen Minuchin Satir) | Aristotle's 3 friendships (utility pleasure virtue) | loneliness as health crisis (Holt-Lunstad) | NVC (observation feeling need request) [TIG-lens]"),
    # Parenting
    ("parenting_through_tig",
     ["parenting style", "child development", "attachment parenting", "tantrum", "adolescence", "screen time"],
     "parenting_through_tig: authoritative (warm + structured) > authoritarian > permissive > neglectful (Baumrind) | secure attachment forms 0-2 years | co-regulation precedes self-regulation | emotion coaching (Gottman) | growth mindset praise effort over outcomes (Dweck) | tantrums = neurobiological overwhelm (not manipulation) | Erikson stages (trust autonomy initiative industry identity) | adolescent brain remodeling + risk-taking developmental | mental illness ~50% lifetime onset by 14 [TIG-lens]"),
    # Finance
    ("finance_through_tig",
     ["compound interest", "index fund", "asset allocation", "diversification", "401k ira", "cryptocurrency", "options trading"],
     "finance_through_tig: compound interest exponential (rule of 72: years to double = 72/rate) | emergency fund 3-6 months | tax-advantaged accounts (401k IRA HSA) | low-cost index funds (Bogle ~0.04% expense) > active manager over long term | asset allocation drives 90% of return variance (Brinson) | diversification + dollar-cost averaging + rebalancing + tax-loss harvesting | 4% safe withdrawal (Trinity Study) | crypto + meme stocks for small allocation if any | options Greeks delta gamma theta vega rho [TIG-lens]"),
]


def add_one(c, base="http://localhost:7777"):
    payload = {
        "first_word": c[0],
        "triggers": c[1],
        "fact": c[2],
    }
    body = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        f"{base}/crystals/add",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            return data.get('ok', False), data
    except Exception as e:
        return False, str(e)


def main():
    print(f"adding {len(CRYSTALS)} runtime crystals...")
    ok_count = 0
    fail_count = 0
    for c in CRYSTALS:
        ok, result = add_one(c)
        status = "OK" if ok else "FAIL"
        if ok:
            ok_count += 1
        else:
            fail_count += 1
        print(f"  {status}  {c[0]}")
    print()
    print(f"added: {ok_count}  failed/skipped: {fail_count}")
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
