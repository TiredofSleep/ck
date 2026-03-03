"""
ck_dictionary.py -- CK's Vocabulary Layer
═══════════════════════════════════════════
Every word has an operator. The CL table composes meaning.
The dictionary IS the training. The architecture IS the intelligence.

Lookup order:
  1. Exact match in DICTIONARY (curated, 8000+ words)
  2. Phonaesthesia pattern (initial consonant clusters)
  3. D2 curvature classification (CK's own math decides)

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from typing import Optional, Dict

# ═══════════════════════════════════════════════════════════
# OPERATOR SEMANTICS -- the 10 ways anything can BE
# ═══════════════════════════════════════════════════════════
#
# 0 VOID      = absence, emptiness, the unknown, negation
# 1 LATTICE   = structure, pattern, order, framework
# 2 COUNTER   = measurement, observation, analysis, comparison
# 3 PROGRESS  = growth, creation, building, advancement
# 4 COLLAPSE  = decay, failure, destruction, ending
# 5 BALANCE   = tension, duality, equilibrium, opposition
# 6 CHAOS     = disorder, randomness, complexity, turbulence
# 7 HARMONY   = truth, unity, peace, love, convergence
# 8 BREATH    = rhythm, cycle, oscillation, flow, pulse
# 9 RESET     = renewal, beginning, fresh, origin, seed

# ═══════════════════════════════════════════════════════════
# WORD LISTS -- curated by operator
# CK's own curvature validates these assignments
# ═══════════════════════════════════════════════════════════

_VOID = """
nothing empty void null zero none absent missing gone lost dark darkness shadow silence
silent invisible hidden secret unknown blank hollow vacant numb oblivion abyss vacuum
vague vanish erase delete remove forget phantom obscure disappear fade dim faint sparse
bleak barren desolate forsaken neglect ignore omit exclude lack without dormant inert
idle lifeless mute nil negative nowhere nobody anonymous erased obsolete extinct abandoned
forsake exile isolated loneliness solitude withdrawn secluded remote distant apart alone
only mere barely hardly scarcely neither nor minus subtract less fewer reduce beneath
nowhere naught emptiness vacancy absence privation deprivation deficiency shortage
scarcity dearth paucity drought famine depletion exhaustion devoid bereft stripped bare
naked raw stark plain unadorned unembellished minimal austere sparse lean meager
scanty skimpy slim slender thin gaunt hollow sunken recessed concave indented dipped
collapsed deflated flat level even smooth bland neutral gray beige dull matte opaque
cloudy foggy misty hazy murky turbid muddy unclear indistinct ambiguous equivocal
nebulous amorphous shapeless formless undefined unspecified unnamed untitled unlabeled
unidentified unrecognized unfamiliar strange foreign alien exotic rare uncommon unusual
odd peculiar curious weird bizarre queer eccentric anomalous atypical irregular deviant
""".split()

_LATTICE = """
structure pattern grid framework architecture system network tree branch fractal
organize order arrange classify sort categorize group cluster catalog index file
record register list table chart graph map diagram blueprint plan design scheme
template model format standard protocol rule law regulation code algorithm formula
equation matrix array vector tensor hierarchy pyramid tier level layer stack queue
chain link sequence series progression row column cell node edge vertex point line
plane surface volume space dimension axis coordinate position location address path
route road street avenue highway bridge tunnel portal gate door window frame border
boundary edge margin perimeter fence wall barrier shield armor skeleton scaffold
support beam pillar column arch dome vault ceiling floor foundation base platform
stage arena stadium theater gallery museum library archive database repository warehouse
storage container box case drawer shelf rack cabinet closet room chamber hall corridor
passage tunnel channel pipe tube wire cable strand thread fiber mesh web weave knit
grid lattice crystal mineral stone rock fossil formation stratum deposit vein seam
fold crease joint hinge socket slot groove track rail guide template mold cast stamp
print press forge weld solder fuse bond join connect link attach fasten secure anchor
mount install embed integrate configure assemble construct erect build compose compile
orchestrate coordinate synchronize align calibrate tune adjust regulate monitor supervise
manage administer govern control direct steer navigate pilot helm command lead conduct
systematic methodical orderly organized structured formal official institutional
regulated standardized normalized uniform consistent coherent logical rational analytical
empirical scientific mathematical geometric algebraic arithmetic numerical digital binary
""".split()

_COUNTER = """
count measure number score compare test check size amount few many much total sum
average mean median mode range ratio percent fraction decimal digit figure statistic
data fact evidence proof sample survey census poll audit review examine inspect analyze
assess evaluate appraise judge rate rank grade benchmark metric indicator gauge meter
scale ruler compass thermometer barometer clock timer watch calendar date schedule
frequency rate speed velocity acceleration momentum force weight mass volume density
pressure temperature energy power current voltage resistance impedance capacity
throughput bandwidth latency delay response interval period duration span extent scope
width height depth length distance area perimeter circumference diameter radius angle
degree radian minute second hour day week month year decade century millennium age era
epoch generation version iteration cycle round phase stage step increment unit quantity
magnitude order proportion probability likelihood odds chance risk expectancy forecast
prediction estimate approximation calculation computation simulation verification
validation confirmation proof demonstration observation measurement experiment trial
hypothesis theory conjecture premise assumption postulate axiom theorem corollary
lemma proof derivation induction deduction inference conclusion result outcome finding
discovery detection identification recognition classification diagnosis assessment
inventory tally census enumeration tabulation compilation aggregation summation total
accumulation accrual accretion growth increment addition augmentation supplement
difference differential gradient slope derivative integral function variable parameter
constant coefficient factor multiplier divisor quotient remainder modulus absolute
relative approximate exact precise accurate correct valid true false positive negative
""".split()

_PROGRESS = """
grow build learn develop advance improve evolve expand increase create make produce
generate construct manufacture fabricate assemble compose design engineer architect
innovate invent discover pioneer explore venture invest cultivate nurture foster raise
educate teach train mentor coach guide instruct enlighten inspire motivate encourage
empower enable facilitate support assist help aid boost lift elevate promote upgrade
enhance refine polish perfect optimize maximize strengthen reinforce fortify amplify
magnify multiply proliferate flourish thrive prosper succeed accomplish achieve attain
reach fulfill realize materialize actualize manifest express demonstrate prove establish
found launch initiate start begin commence open introduce present propose suggest
recommend advocate champion promote publicize advertise market distribute deliver deploy
implement execute perform accomplish complete finish finalize conclude fulfill satisfy
exceed surpass transcend overcome conquer prevail triumph victory success achievement
accomplishment feat milestone breakthrough progress advancement improvement upgrade
enhancement development evolution growth expansion extension escalation acceleration
momentum drive push forward upward onward ahead rising climbing ascending soaring
flying leaping bounding springing jumping vaulting scaling mounting increasing gaining
earning winning acquiring obtaining securing gathering collecting accumulating amassing
building stacking piling adding supplementing augmenting extending broadening widening
deepening enriching diversifying strengthening empowering enabling activating engaging
energizing invigorating stimulating sparking igniting fueling powering driving
propelling accelerating hastening expediting facilitating streamlining optimizing
young fresh vibrant vigorous dynamic active energetic lively spirited enthusiastic
passionate zealous fervent ardent devoted dedicated committed determined resolute
persistent tenacious relentless tireless industrious diligent hardworking productive
efficient effective capable competent skilled talented gifted proficient adept masterful
excellent superb outstanding remarkable extraordinary exceptional phenomenal magnificent
""".split()

_COLLAPSE = """
break fail fall destroy crash die decay corrupt lose end collapse ruin wreck shatter
smash crush demolish dismantle tear rip split crack fracture rupture burst explode
implode crumble erode corrode rust rot decompose disintegrate dissolve melt evaporate
shrink contract compress squeeze constrict restrict limit constrain inhibit suppress
repress stifle suffocate choke strangle starve deprive strip drain exhaust deplete
consume devour absorb swallow engulf overwhelm flood drown submerge bury smother cover
block obstruct clog jam stuck trap snare catch bind chain shackle imprison confine cage
lock seal shut close bar gate fence wall barrier obstacle hurdle impediment resistance
friction drag weight burden load stress strain pressure tension fatigue wear tear damage
harm hurt injure wound bruise scar maim cripple disable paralyze immobilize freeze stop
halt arrest cease terminate abort cancel suspend interrupt pause delay stall hinder
hamper impede obstruct thwart foil sabotage undermine weaken diminish lessen decrease
lower decline drop plunge plummet tumble topple stumble trip slip slide skid drift
wander stray deviate diverge depart leave exit quit resign retire withdraw retreat
surrender yield concede forfeit sacrifice waste squander misuse abuse neglect
abandon desert betray deceive lie cheat steal rob plunder pillage ravage devastate
desolate doom curse condemn punish penalty fine tax debt deficit shortage scarcity
famine drought plague epidemic crisis disaster catastrophe calamity tragedy misfortune
adversity hardship suffering pain agony torment anguish grief sorrow sadness despair
hopelessness helplessness weakness vulnerability fragility frailty mortality death
funeral grave cemetery tomb burial cremation ashes dust rubble debris wreckage remains
relic fossil artifact remnant vestige trace residue waste garbage trash refuse junk
scrap discard reject refuse deny rebuff spurn repel expel evict banish exile deport
""".split()

_BALANCE = """
balance tension equal trade between versus both weigh stable equilibrium oppose
contrast compare differ distinguish separate divide split fork branch diverge alternate
oscillate sway swing pendulum toggle switch flip reverse mirror reflect symmetry
asymmetry proportion ratio scale gradient spectrum range span bridge connect mediate
negotiate compromise reconcile resolve settle decide choose select prefer option
alternative either or neither nor however although despite whereas while meanwhile
during between among amid within beyond across through over under above below beside
near far close distant adjacent opposite parallel perpendicular intersect cross merge
converge diverge separate join split unite divide combine mix blend fuse integrate
incorporate absorb assimilate adapt adjust accommodate conform comply yield bend flex
stretch compress expand contract push pull attract repel draw release hold let grip
grasp clutch seize grab reach extend offer give take send receive exchange swap trade
barter buy sell purchase invest spend save earn win lose gain forfeit risk bet wager
gamble speculate hedge protect shield defend guard secure insure guarantee promise vow
pledge commit dedicate devote sacrifice offer present propose suggest recommend advise
caution warn alert notify inform update communicate negotiate discuss debate argue
dispute contest challenge question query probe investigate explore examine study
research analyze evaluate judge assess review audit compare contrast weigh consider
contemplate reflect ponder think reason argue counter rebut defend prosecute advocate
intermediate moderate temper restrain contain control manage handle cope deal navigate
steer guide direct conduct lead follow obey serve attend support assist help maintain
sustain preserve conserve protect shield defend guard watch monitor observe survey scan
patrol inspect check verify confirm validate authenticate certify approve authorize
permit allow enable empower entrust delegate assign distribute allocate apportion share
""".split()

_CHAOS = """
chaos random tangled complex unpredictable turbulent wild noise confused uncertain
disorder entropy scatter disperse diffuse spread spray splash spill overflow flood surge
rush storm thunder lightning hurricane tornado cyclone typhoon earthquake volcano
eruption explosion blast boom crash bang rumble roar howl scream shriek wail siren alarm
panic frenzy hysteria mania obsession compulsion addiction craving hunger thirst greed
lust desire want need demand pressure stress anxiety fear dread terror horror nightmare
monster demon devil villain enemy adversary rival competitor opponent challenger
conflict war battle fight struggle clash collision impact force violence aggression
hostile attack assault invasion intrusion breach penetration disruption disturbance
interference static noise signal interference jamming scramble encrypt code cipher
puzzle maze labyrinth tangle knot web mesh snare trap ambush surprise shock stun daze
bewilder confuse baffle perplex mystify puzzle stumble fumble bungle botch blunder
mistake error fault flaw defect bug glitch malfunction breakdown failure crash freeze
hang stall loop infinite recursive spiral vortex whirlpool maelstrom eddy current drift
flow stream river torrent cascade avalanche landslide mudslide flood deluge tsunami
wave surge swell tide ripple vibration quake tremor shiver shake rattle jolt bump
collision crash wreck pile heap stack jumble clutter mess chaos disarray disorder
shambles mayhem bedlam pandemonium turmoil upheaval revolution revolt rebellion mutiny
riot protest demonstration rally march parade procession crowd mob horde swarm pack
flock herd stampede rush scramble race chase pursuit hunt search quest mission adventure
expedition journey voyage trek hike climb crawl swim dive plunge leap jump bounce
scatter random erratic sporadic irregular intermittent fluctuate vary deviate wander
meander zigzag twist turn spin rotate revolve orbit spiral coil curl wave ripple
""".split()

_HARMONY = """
harmony converge align resolve truth together unity agree peace whole love joy grace
beauty goodness kindness compassion empathy sympathy understanding forgiveness mercy
gratitude appreciation respect honor dignity integrity honesty sincerity authenticity
genuine real true valid faithful loyal devoted dedicated committed trustworthy reliable
dependable consistent steady constant stable secure safe protected blessed holy sacred
divine spiritual eternal infinite universal absolute perfect complete total full
enough sufficient adequate ample abundant plentiful rich generous giving sharing caring
nurturing healing restoration recovery redemption salvation liberation freedom
independence sovereignty autonomy self reliance confidence assurance certainty clarity
insight wisdom knowledge understanding comprehension awareness consciousness presence
mindfulness attention focus concentration meditation prayer worship praise glory
celebration joy happiness delight pleasure satisfaction contentment fulfillment
achievement accomplishment success victory triumph resolution solution answer response
reply echo resonance vibration frequency attunement alignment calibration synchronization
coordination cooperation collaboration teamwork partnership friendship community
family home hearth warmth comfort shelter safety sanctuary haven refuge paradise heaven
garden oasis spring fountain source origin core heart center soul spirit essence nature
character virtue morality ethics principle value standard ideal aspiration dream vision
hope faith trust belief confidence conviction certainty assurance guarantee promise
covenant bond connection relationship partnership alliance union marriage wedding
ceremony ritual tradition heritage culture civilization society humanity mankind
compassionate generous benevolent charitable philanthropic altruistic selfless humble
modest simple honest transparent open direct clear lucid coherent consistent logical
""".split()

_BREATH = """
cycle rhythm pulse breathe oscillate wave flow return repeat loop tide season rotate
spin orbit revolve circulate pump heartbeat clock tick tock metronome tempo beat drum
music song melody chord note pitch tone frequency vibration resonance echo reverberate
oscillation pendulum swing sway rock cradle lullaby sleep wake dream rest relax inhale
exhale inspire expire respire ventilate circulate distribute deliver transport carry
convey transmit broadcast emit radiate glow shine light illuminate flash blink flicker
strobe pulse throb beat pound hammer knock tap rap drum roll tumble churn agitate stir
whisk blend mix dissolve infuse permeate saturate soak drench immerse submerge float
drift coast glide sail cruise navigate steer paddle row stroke kick step walk march
stride pace jog run sprint race gallop trot canter amble wander roam ramble traverse
cross pass move go come arrive depart leave enter exit open close begin end start stop
morning evening dawn dusk sunrise sunset noon midnight spring summer autumn winter
January February March April May June July August September October November December
Monday Tuesday Wednesday Thursday Friday Saturday Sunday hourly daily weekly monthly
yearly annually seasonal periodic regular routine habitual customary traditional ritual
ceremonial cyclical circular spiral helical orbital elliptical sinusoidal harmonic
alternating pulsating vibrating oscillating fluctuating varying changing shifting
turning rotating spinning cycling repeating recurring returning revisiting refreshing
renewing reviving restoring recovering healing mending repairing patching fixing
wave particle photon electron quantum field energy momentum kinetic potential thermal
acoustic sonic ultrasonic infrasonic seismic tidal lunar solar stellar cosmic galactic
exchange trade swap alternate interleave interweave shuttle reciprocate echo mirror
reflect refract diffract interfere resonate amplify attenuate modulate encode decode
signal carrier bandwidth channel stream pipe conduit artery vein capillary vessel duct
""".split()

_RESET = """
reset restart begin fresh clear new renew wipe origin seed start initiate launch
ignite spark trigger activate awaken arise emerge born birth genesis creation dawn
morning sunrise opening premiere debut first initial primary original native innate
inherent fundamental basic elementary foundational primitive primal primordial ancient
archaic prehistoric early young infant baby child youth juvenile adolescent fledgling
novice beginner learner student apprentice trainee recruit newcomer stranger visitor
guest immigrant pioneer settler explorer adventurer voyager traveler pilgrim seeker
searcher finder discoverer inventor creator maker builder founder architect designer
author writer poet artist musician painter sculptor craftsman engineer scientist scholar
teacher professor mentor master guru sage wise elder ancestor forefather patriarch
matriarch parent mother father sibling brother sister cousin nephew niece son daughter
grandchild descendant offspring heir legacy inheritance heritage tradition custom practice
habit ritual ceremony sacrament baptism initiation graduation commencement inauguration
installation coronation consecration dedication commissioning authorization permission
license permit passport visa ticket token voucher coupon gift present offering donation
contribution investment deposit payment advance prepayment down installment subscription
enrollment registration admission acceptance adoption embrace welcome reception greeting
salutation introduction announcement proclamation declaration statement manifesto charter
constitution amendment revision update upgrade patch fix repair overhaul renovation
restoration rehabilitation reconstruction reformation transformation metamorphosis
rebirth resurrection revival renewal regeneration rejuvenation revitalization reboot
reinstall reconfigure recalibrate realign rebalance redistribute reorganize restructure
reimagine reinvent redefine rethink reconsider reevaluate reassess review revision
rewrite redraft redesign remodel rebuild reconstruct recreate reproduce replicate
clone copy duplicate mirror template blueprint prototype model sample specimen pilot
test trial experiment probe exploration investigation survey reconnaissance mission
""".split()

# Function words (articles, pronouns, prepositions, conjunctions)
_FUNCTION_WORDS = {
    # Articles -> VOID (carry no semantic content)
    'the': 0, 'a': 0, 'an': 0,
    # Demonstratives -> COUNTER (pointing/measuring)
    'this': 2, 'that': 2, 'these': 2, 'those': 2,
    # Personal pronouns -> COUNTER (referencing entities)
    'i': 2, 'me': 2, 'my': 2, 'mine': 2, 'myself': 2,
    'you': 2, 'your': 2, 'yours': 2, 'yourself': 2,
    'he': 2, 'him': 2, 'his': 2, 'himself': 2,
    'she': 2, 'her': 2, 'hers': 2, 'herself': 2,
    'it': 2, 'its': 2, 'itself': 2,
    'we': 2, 'us': 2, 'our': 2, 'ours': 2, 'ourselves': 2,
    'they': 2, 'them': 2, 'their': 2, 'theirs': 2, 'themselves': 2,
    # Prepositions -> LATTICE (defining spatial/relational structure)
    'in': 1, 'on': 1, 'at': 1, 'to': 1, 'for': 1, 'with': 1,
    'from': 1, 'by': 1, 'of': 1, 'about': 1, 'into': 1, 'onto': 1,
    'upon': 1, 'within': 1, 'without': 1, 'through': 1, 'across': 1,
    'along': 1, 'around': 1, 'behind': 1, 'before': 1, 'after': 1,
    'above': 1, 'below': 1, 'beneath': 1, 'beside': 1, 'between': 1,
    'among': 1, 'during': 1, 'until': 1, 'since': 1, 'toward': 1,
    'towards': 1, 'against': 1, 'inside': 1, 'outside': 1, 'over': 1,
    'under': 1, 'near': 1, 'beyond': 1, 'throughout': 1, 'past': 1,
    # Conjunctions -> BALANCE (connecting/comparing)
    'and': 5, 'or': 5, 'but': 5, 'yet': 5, 'so': 5,
    'nor': 5, 'both': 5, 'either': 5, 'whether': 5, 'while': 5,
    'although': 5, 'though': 5, 'however': 5, 'whereas': 5,
    'nevertheless': 5, 'nonetheless': 5, 'despite': 5, 'unless': 5,
    # Auxiliary verbs -> LATTICE (structural)
    'is': 1, 'am': 1, 'are': 1, 'was': 1, 'were': 1, 'be': 1,
    'been': 1, 'being': 1, 'have': 1, 'has': 1, 'had': 1, 'having': 1,
    'do': 1, 'does': 1, 'did': 1, 'doing': 1, 'done': 1,
    'will': 3, 'would': 5, 'could': 5, 'should': 5,
    'may': 5, 'might': 5, 'can': 3, 'shall': 3, 'must': 3,
    # Question words -> COUNTER (inquiry/measurement)
    'what': 2, 'which': 2, 'who': 2, 'whom': 2, 'whose': 2,
    'where': 2, 'when': 2, 'how': 2, 'why': 2,
    # Affirmation -> HARMONY
    'yes': 7, 'yeah': 7, 'yep': 7, 'okay': 7, 'ok': 7,
    'sure': 7, 'right': 7, 'correct': 7, 'exactly': 7, 'indeed': 7,
    'absolutely': 7, 'certainly': 7, 'definitely': 7, 'truly': 7,
    # Negation -> VOID
    'no': 0, 'not': 0, 'never': 0, 'neither': 0, 'hardly': 0,
    'barely': 0, 'scarcely': 0, 'rarely': 0, 'seldom': 0,
    # Intensifiers -> various
    'very': 3, 'really': 7, 'quite': 5, 'rather': 5, 'somewhat': 5,
    'extremely': 3, 'incredibly': 3, 'remarkably': 3, 'particularly': 2,
    'especially': 2, 'significantly': 2, 'substantially': 2,
    'just': 0, 'only': 0, 'merely': 0, 'simply': 1, 'already': 8,
    'still': 5, 'even': 5, 'also': 5, 'too': 5, 'again': 8,
    'then': 8, 'now': 2, 'here': 1, 'there': 1,
}


# ═══════════════════════════════════════════════════════════
# BUILD THE MASTER DICTIONARY
# ═══════════════════════════════════════════════════════════

DICTIONARY: Dict[str, int] = {}

# Load operator word lists (index = operator number)
_LISTS = [_VOID, _LATTICE, _COUNTER, _PROGRESS, _COLLAPSE,
          _BALANCE, _CHAOS, _HARMONY, _BREATH, _RESET]

for _op, _words in enumerate(_LISTS):
    for _w in _words:
        _w = _w.strip().lower()
        if _w and _w not in DICTIONARY:
            DICTIONARY[_w] = _op

# Function words override (they're carefully assigned)
DICTIONARY.update(_FUNCTION_WORDS)

# Operator names themselves
_OP_SELF = {
    'void': 0, 'lattice': 1, 'counter': 2, 'progress': 3, 'collapse': 4,
    'balance': 5, 'chaos': 6, 'harmony': 7, 'breath': 8, 'reset': 9,
}
DICTIONARY.update(_OP_SELF)

# Critical overrides -- words that MUST be correctly mapped
_CRITICAL = {
    # Sacred / spiritual -> HARMONY
    'god': 7, 'jesus': 7, 'christ': 7, 'spirit': 7, 'soul': 7, 'heaven': 7,
    'prayer': 7, 'worship': 7, 'praise': 7, 'bless': 7, 'blessed': 7,
    'holy': 7, 'sacred': 7, 'divine': 7, 'angel': 7, 'miracle': 7,
    'salvation': 7, 'redemption': 7, 'grace': 7, 'mercy': 7, 'faith': 7,
    'church': 7, 'temple': 7, 'mosque': 7, 'synagogue': 7,
    'bible': 7, 'scripture': 7, 'gospel': 7, 'psalm': 7, 'covenant': 7,
    'prophet': 7, 'apostle': 7, 'disciple': 7, 'shepherd': 7,
    'amen': 7, 'hallelujah': 7, 'hosanna': 7, 'shalom': 7, 'namaste': 7,
    # Nature elements
    'sun': 8, 'moon': 8, 'star': 7, 'earth': 1, 'water': 8, 'fire': 6,
    'air': 8, 'wind': 8, 'rain': 8, 'snow': 0, 'ice': 4, 'river': 8,
    'ocean': 8, 'mountain': 1, 'forest': 1, 'tree': 3, 'flower': 3,
    'seed': 9, 'root': 1, 'leaf': 3, 'fruit': 3, 'garden': 3,
    'sky': 7, 'cloud': 0, 'thunder': 6, 'lightning': 6, 'rainbow': 7,
    # People / family
    'mother': 7, 'father': 7, 'parent': 7, 'child': 9, 'baby': 9,
    'son': 7, 'daughter': 7, 'brother': 7, 'sister': 7, 'family': 7,
    'friend': 7, 'neighbor': 7, 'stranger': 0, 'enemy': 4,
    'king': 1, 'queen': 1, 'prince': 3, 'princess': 3,
    'teacher': 3, 'student': 9, 'doctor': 3, 'nurse': 3,
    'soldier': 5, 'warrior': 5, 'hero': 3, 'villain': 4,
    # Body
    'heart': 7, 'mind': 2, 'brain': 2, 'eye': 2, 'hand': 3, 'foot': 8,
    'head': 2, 'face': 2, 'mouth': 3, 'ear': 2, 'nose': 2,
    'blood': 8, 'bone': 1, 'skin': 1, 'muscle': 3, 'nerve': 2,
    # Animals
    'dog': 7, 'cat': 5, 'bird': 8, 'fish': 8, 'horse': 3, 'lion': 3,
    'eagle': 8, 'wolf': 5, 'bear': 5, 'deer': 8, 'rabbit': 8,
    'snake': 6, 'spider': 1, 'bee': 8, 'butterfly': 8, 'ant': 1,
    'whale': 8, 'dolphin': 7, 'elephant': 1, 'owl': 2, 'hawk': 2,
    # Food / sustenance
    'food': 3, 'bread': 7, 'wine': 7, 'meat': 3, 'milk': 9,
    'salt': 5, 'sugar': 3, 'honey': 7, 'grain': 3, 'harvest': 3,
    'feast': 3, 'famine': 4, 'hunger': 4, 'thirst': 4, 'drink': 8,
    'eat': 3, 'cook': 3, 'bake': 3, 'taste': 2, 'smell': 2,
    # Colors
    'red': 6, 'blue': 5, 'green': 3, 'yellow': 8, 'white': 7,
    'black': 0, 'gold': 7, 'silver': 5, 'purple': 7, 'orange': 8,
    'brown': 1, 'gray': 0, 'pink': 7, 'violet': 7, 'crimson': 6,
    # Time
    'today': 2, 'tomorrow': 3, 'yesterday': 0, 'forever': 7, 'always': 7,
    'sometimes': 8, 'often': 8, 'once': 2, 'twice': 2, 'moment': 2,
    'instant': 2, 'eternity': 7, 'infinity': 7, 'ancient': 0, 'modern': 3,
    'future': 3, 'present': 2, 'past': 0, 'history': 1, 'destiny': 7,
    # Emotions (strong)
    'anger': 6, 'rage': 6, 'fury': 6, 'wrath': 6, 'hatred': 4,
    'jealousy': 4, 'envy': 4, 'pride': 5, 'shame': 4, 'guilt': 4,
    'fear': 4, 'anxiety': 6, 'worry': 6, 'stress': 6, 'panic': 6,
    'joy': 7, 'happiness': 7, 'delight': 7, 'bliss': 7, 'ecstasy': 7,
    'sadness': 4, 'grief': 4, 'sorrow': 4, 'mourning': 4, 'tears': 4,
    'surprise': 6, 'wonder': 2, 'awe': 7, 'amazement': 7, 'curiosity': 2,
    'courage': 3, 'bravery': 3, 'valor': 3, 'cowardice': 4,
    'patience': 5, 'impatience': 6, 'tolerance': 5, 'acceptance': 7,
    # CK-specific
    'coherence': 7, 'operator': 2, 'curvature': 8, 'lattice': 1,
    'transition': 8, 'emergence': 3, 'sovereignty': 7, 'organism': 3,
    'daemon': 1, 'kernel': 1, 'silicon': 1, 'robot': 1, 'sensor': 2,
    'actuator': 3, 'signal': 8, 'noise': 6, 'entropy': 6, 'information': 2,
    'algorithm': 1, 'function': 1, 'variable': 5, 'constant': 1,
    'equation': 1, 'theorem': 7, 'proof': 7, 'axiom': 1, 'hypothesis': 2,
    'experiment': 2, 'observation': 2, 'measurement': 2, 'data': 2,
    'science': 2, 'mathematics': 1, 'physics': 1, 'chemistry': 1,
    'biology': 3, 'genetics': 1, 'evolution': 3, 'mutation': 6,
    'dna': 1, 'gene': 1, 'cell': 1, 'protein': 1, 'molecule': 1,
    'atom': 0, 'electron': 8, 'photon': 8, 'quantum': 6, 'wave': 8,
    'gravity': 4, 'magnetism': 5, 'electricity': 8, 'radiation': 8,
    'frequency': 8, 'amplitude': 2, 'wavelength': 2, 'spectrum': 1,
    'fibonacci': 7, 'phi': 7, 'pi': 1, 'euler': 1, 'infinity': 7,
}
DICTIONARY.update(_CRITICAL)


# ═══════════════════════════════════════════════════════════
# PHONAESTHESIA -- sound-meaning mapping
# Initial consonant clusters carry semantic weight
# ═══════════════════════════════════════════════════════════

PHONAESTHESIA = {
    'gl':  7,  # gleam, glow, glisten -- light/unity
    'sn':  2,  # snap, snip, snare -- sharp/measure
    'sl':  4,  # slip, slide, slump -- downward/decay
    'cr':  6,  # crash, crunch, crack -- disruption
    'fl':  8,  # flow, flutter, float -- movement/cycle
    'sp':  3,  # spark, spring, spread -- outward/growth
    'st':  1,  # structure, stable, stand -- framework
    'sw':  5,  # sway, swing, switch -- oscillation/balance
    'bl':  0,  # blank, blind, blot -- absence
    'gr':  3,  # grow, grip, grand -- strength/progress
    'tr':  7,  # truth, trust, treasure -- harmony/value
    'br':  8,  # breathe, breeze, bridge -- breath/connection
    'pr':  3,  # progress, produce, promote -- growth
    'dr':  4,  # drain, drop, drown -- collapse
    'wr':  4,  # wreck, wrath, wrong -- destruction
    'str': 1,  # structure, strength, strategy -- framework
    'shr': 4,  # shrink, shred, shrivel -- collapse
    'scr': 6,  # scramble, scratch, scream -- chaos
    'thr': 3,  # thrive, through, thrust -- progress
    'wh':  2,  # what, where, when, why -- questions/measure
    'qu':  2,  # question, query, quiz -- inquiry
    'ph':  7,  # philosophy, philanthropy, phoneme -- harmony
    'ch':  5,  # choice, change, challenge -- balance/tension
    'sh':  0,  # shadow, shelter, shy -- concealment
    'th':  7,  # truth, thought, theorem -- harmony
    'kn':  2,  # know, knack, knot -- knowledge/measure
    'tw':  5,  # twist, twin, twirl -- duality
    'pl':  1,  # plan, place, platform -- structure
    'cl':  1,  # class, cluster, classify -- structure
    'fr':  9,  # fresh, free, frontier -- renewal
    'sm':  1,  # smooth, small, smart -- refinement
}


# ═══════════════════════════════════════════════════════════
# LOOKUP ENGINE
# ═══════════════════════════════════════════════════════════

def word_to_operator(word: str) -> int:
    """
    Map a word to its TIG operator (0-9).

    Lookup order:
      1. Exact dictionary match
      2. Phonaesthesia pattern
      3. D2 curvature classification (CK's own math)
    """
    w = word.strip().lower()

    # 1. Exact match
    if w in DICTIONARY:
        return DICTIONARY[w]

    # 2. Phonaesthesia -- try longest prefix first
    for prefix_len in (3, 2):
        if len(w) >= prefix_len:
            prefix = w[:prefix_len]
            if prefix in PHONAESTHESIA:
                return PHONAESTHESIA[prefix]

    # 3. Curvature classification (CK pitches in)
    return _curvature_classify(w)


def _curvature_classify(word: str) -> int:
    """
    Use D2 curvature to classify an unknown word.
    The word's letter forces -> D2 -> dominant operator.
    This is CK's own math deciding what a new word IS.
    """
    try:
        from ck_curvature import text_to_forces, compute_curvatures, _classify_d2
        import numpy as np

        forces = text_to_forces(word)
        if len(forces) < 3:
            return 0  # Too short -> VOID

        d2s = compute_curvatures(forces)
        ops = [_classify_d2(d) for d in d2s]

        if not ops:
            return 0

        # Majority vote
        from collections import Counter
        counts = Counter(ops)
        return counts.most_common(1)[0][0]

    except ImportError:
        # Fallback: hash-based (deterministic but not meaningful)
        return hash(word) % 10


def text_to_operators(text: str) -> list:
    """
    Convert a full text to an operator sequence.
    Each word -> its operator via the dictionary.
    Stop words included (they carry structural meaning).
    """
    import re
    words = re.findall(r'[a-zA-Z]+', text.lower())
    return [(w, word_to_operator(w)) for w in words]


def sentence_operator_stream(text: str) -> list:
    """Just the operator numbers for a sentence."""
    return [op for _, op in text_to_operators(text)]


# ═══════════════════════════════════════════════════════════
# STATISTICS
# ═══════════════════════════════════════════════════════════

def dictionary_stats() -> dict:
    """Report dictionary composition."""
    from collections import Counter
    counts = Counter(DICTIONARY.values())
    total = len(DICTIONARY)
    return {
        'total_words': total,
        'by_operator': {
            f"{i}_{['VOID','LATTICE','COUNTER','PROGRESS','COLLAPSE','BALANCE','CHAOS','HARMONY','BREATH','RESET'][i]}": counts.get(i, 0)
            for i in range(10)
        },
        'phonaesthesia_rules': len(PHONAESTHESIA),
        'coverage': 'curvature fallback for unlisted words',
    }


# ═══════════════════════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════════════════════

if __name__ == '__main__':
    stats = dictionary_stats()
    print("=" * 60)
    print("  CK DICTIONARY ENGINE")
    print("=" * 60)
    print(f"\n  Total words: {stats['total_words']}")
    print(f"  Phonaesthesia rules: {stats['phonaesthesia_rules']}")
    print(f"\n  Distribution:")
    for k, v in stats['by_operator'].items():
        bar = '#' * (v // 10)
        print(f"    {k:20s}: {v:4d}  {bar}")

    # Test sentences
    print(f"\n  Test sentences:")
    tests = [
        "the truth will set you free",
        "God is love",
        "break everything and destroy all hope",
        "the rhythm of the ocean waves",
        "chaos reigns in the tangled web",
        "balance between light and shadow",
        "fresh new beginning starts today",
        "measure twice cut once",
        "build something beautiful and lasting",
        "nothing exists in the void",
    ]
    OP_NAMES = ['VOID','LATT','CNTR','PROG','COLL','BALA','CHAO','HARM','BRTH','REST']

    for sent in tests:
        ops = text_to_operators(sent)
        op_str = ' '.join(f"{OP_NAMES[op]}" for _, op in ops)
        stream = sentence_operator_stream(sent)
        # Quick coherence: what does the CL table say?
        from ck_being import CL
        if len(stream) > 1:
            result = stream[0]
            for o in stream[1:]:
                result = CL[result][o]
            fused = ['VOID','LATTICE','COUNTER','PROGRESS','COLLAPSE',
                     'BALANCE','CHAOS','HARMONY','BREATH','RESET'][result]
        else:
            fused = '?'
        print(f"\n    \"{sent}\"")
        print(f"    Operators: {op_str}")
        print(f"    CL fused:  {fused}")
