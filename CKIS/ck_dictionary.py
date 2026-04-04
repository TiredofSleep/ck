"""
ck_dictionary.py -- CK's Vocabulary Layer
═══════════════════════════════════════════
Every word has an operator. The CL table composes meaning.
The dictionary IS the training. The architecture IS the intelligence.

Lookup order:
  1. Exact match in DICTIONARY (curated, 5000+ words)
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
gap hole pit chasm crater cave den ditch trench gorge canyon ravine crevice rift
lull hiatus recess intermission stagnation impasse deadlock stalemate bottleneck
torpor stupor lethargy apathy indifference disinterest nonchalance aloofness
disconnection alienation estrangement displacement dislocation severance partition
prohibition ban embargo censorship concealment camouflage disguise mask veil shroud
ghost specter wraith silhouette skeleton shell husk carcass residue soot vapor fume
smog exhaust emission drainage seepage trickle drip ooze puddle stagnant motionless
frozen deaf blind muted hushed whispered faded worn weathered tattered frayed threadbare
patchy incomplete unfinished rough crude primitive rudimentary mundane trivial petty
marginal peripheral secondary subordinate minor lesser inferior mediocre lackluster
unremarkable forgettable disposable expendable unnecessary redundant superfluous
inaccessible unavailable unreachable unobtainable impossible impractical useless futile
pointless meaningless senseless purposeless aimless directionless random haphazard
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
schema syntax grammar vocabulary lexicon alphabet syllable morpheme notation markup
specification documentation manual reference registry catalog directory inventory
manifest roster schedule timeline agenda roadmap workflow pipeline procedure routine
method technique approach strategy tactic execution implementation deployment
installation configuration setup parameter setting option preference profile stylesheet
layout arrangement positioning spacing alignment distribution placement orientation
heading bearing navigation routing addressing port endpoint interface connector adapter
gateway hub switch controller router proxy server client host terminal console dashboard
panel widget component element module unit block segment sector zone district region
territory province domain realm sphere scope field area category genus species phylum
kingdom type kind sort variety breed lineage descent pedigree genealogy ancestry
hardware circuit board chip silicon wafer package pin bus fiber optic cable wire
protocol tcp udp http https dns ssl tls api socket packet frame header payload
schema database query index migration version commit branch tag repository clone
text letter symbol glyph character digit cipher encoding format markup notation
language grammar syntax morphology phonology semantics pragmatics linguistics
body physical state fixed mapped mapping mappings topology handler pipeline
controlled module letter region species server hardware cl sandbox vocabulary
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
observe detect identify recognize diagnose determine quantify calculate compute derive
interpolate extrapolate normalize standardize calibrate profile debug trace log
scrutinize probe interrogate query lookup search scan filter flag annotate label tag
datum index threshold criterion exponent logarithm determinant eigenvalue singular
regression correlation covariance variance deviation outlier anomaly residual bias drift
sensitivity specificity fidelity resolution granularity breadth
microscope telescope spectrometer oscilloscope voltmeter ammeter multimeter hygrometer
altimeter speedometer odometer pedometer accelerometer gyroscope sonar radar lidar gps
satellite scanner detector receptor aware conscious perceive discern distinguish
differentiate discriminate juxtapose associate attribute assign allocate
triple twelve fifteen hundred thousand million billion trillion quadrillion
socratic analytical empirical statistical numerical computational diagnostic
pfe btq scoring evaluator lens matching comparison fingerprinting reads lookup
feels aware analysis processing dtw normalization output input feedback signal reading
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
synthesize merge consolidate unify harmonize automate digitize modernize revolutionize
transform refactor reengineer overhaul renovate restore rehabilitate revamp revitalize
reclaim recover salvage rescue retrieve recoup regenerate reproduce replicate
catalyze trigger provoke elicit evoke invoke summon mobilize rally recruit enlist
employ utilize leverage harness channel focus concentrate consolidate simplify
clarify distill extract purify cleanse propagate disseminate broadcast circulate
blossom bloom bud sprout germinate plant sow reap yield harvest
profit return dividend revenue earnings surplus bounty wealth fortune prosperity
abundance affluence bonus premium reward prize trophy medal badge glory renown
prestige reputation credibility authority influence capability aptitude expertise
command mastery proficiency intent speech speaks motor driven guided health engine
curriculum planning output composition integration natural method
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
deteriorate degrade wane ebb wither shrivel parch scorch singe char burn incinerate
obliterate annihilate exterminate eradicate eliminate expunge purge
nullify negate invalidate revoke rescind repeal abolish quash overturn override veto
dismiss discharge liquidate disband disperse fragment splinter chip peel flake
sever amputate excise detach disconnect unplug unlink decouple disengage
downgrade demote minimize curtail truncate abbreviate shorten compact condense
bankrupt insolvent broke destitute impoverished emaciated wasted
rigid stiff petrified calcified ossified antiquated deprecated defunct perished deceased
hemorrhage bleed atrophy wilt languish stifle throttle congest obstruct bottleneck
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
poise steadiness evenness levelness fairness justice equity equality parity reciprocity
mutuality correspondence moderation temperance restraint discipline governance stewardship
supervision oversight administration jurisdiction sovereignty autonomy independence
diplomacy tact discretion prudence caution deliberation contemplation introspection
neutral objective impartial unbiased dispassionate reserved measured composed collected
serene calm tranquil placid peaceful quiet settled resolved determined focused attentive
vigilant alert watchful observant mindful conscious deliberate intentional purposeful
strategic tactical calculated methodical systematic planned regulated governed
immune defense security normalization translation translates gated controlled
affinity decisions counterbalance counterpoint tradeoff concession mutual reciprocal
dual duality bilateral bipartisan ambivalent ambidextrous versatile flexible adaptive
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
turbulence perturbation instability volatility variability inconsistency
stochastic probabilistic nondeterministic fractal nonlinear emergent
fuzzy distorted warped skewed twisted contorted mangled garbled corrupted
decentralized autonomous feral savage aggressive belligerent combative confrontational
adversarial antagonistic contentious controversial divisive polarizing inflammatory
provocative volatile combustible reactive unstable precarious dangerous hazardous
risky perilous treacherous formidable daunting intimidating overwhelming crushing
devastating catastrophic apocalyptic cataclysmic seismic tectonic eruptive convulsive
spasmodic jerky twitchy fidgety restless agitated tense excited hyper manic frantic
hectic feverish delirious psychedelic surreal dreamlike nightmarish horrific ghastly
grotesque macabre morbid sinister ominous foreboding threatening menacing jitter
mutation quantum entropy noise disruption interference anomaly glitch spike
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
wholeness completeness totality comprehensiveness inclusiveness universality
unification consolidation fusion synthesis combination confluence intersection meeting
gathering assembly congregation fellowship brotherhood sisterhood kinship solidarity
camaraderie rapport affinity attachment engagement involvement participation contribution
consortium guild association society organization institution foundation endowment
charity philanthropy hospitality inclusion diversity richness profusion treasure
patrimony legacy bequest inheritance identity meaning purpose significance relevance
importance worth merit quality excellence distinction eminence supremacy flawlessness
precision correctness validity soundness robustness reliability dependability credibility
authenticity genuineness transparency openness candor frankness directness perspicacity
acumen sagacity discernment perception intuition appreciation recognition acknowledgment
semantic natural composition fusion integration hebrew ck coherence theorem proof
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
respiration transportation transmission propagation radiation emission absorption
reflection refraction diffraction interference harmonics overtone fundamental
wavelength amplitude phase polarity modulation demodulation encoding decoding
sampling quantization digitization conversion transformation transduction
gyration precession nutation libration wobble tremor quiver flutter undulation
billow ebb flux cadence meter syncopation polyrhythm accent emphasis stress
intonation inflection pitch timbre partial phoneme syllable articulation pronunciation
enunciation diction elocution delivery utterance expression vocalization verbalization
dialogue discourse narration recitation chant psalm hymn anthem ballad ode serenade
requiem dirge elegy sonata symphony concerto fugue prelude interlude coda overture
finale crescendo diminuendo fortissimo pianissimo staccato legato rubato arpeggio
glissando tremolo vibrato portamento fermata
nervous sliding voice phonaesthesia d2 curvature signal iterate recur
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
initialization configuration bootstrap loading mounting provisioning staging
preparation readiness prerequisite groundwork infrastructure scaffold bedrock substrate
basis baseline reference benchmark specification draft sketch outline
agenda proposal recommendation suggestion guidance direction instruction
tutorial lesson course program curriculum syllabus textbook handbook guidebook
encyclopedia dictionary glossary lexicon thesaurus chronicle annals
documentation annotation commentary explanation interpretation adaptation conversion
amendment modification alteration transition migration progression
promotion elevation induction orientation acclimatization assimilation
incorporation supplement extension enlargement amplification augmentation enhancement
enrichment improvement refinement honing sharpening tuning adjusting aligning
init startup launcher fallback pre embryo nucleus germ spore egg larva cocoon chrysalis
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
    'body': 1, 'organ': 3, 'tissue': 1, 'membrane': 1, 'vessel': 8,
    'spine': 1, 'lung': 8, 'liver': 3, 'kidney': 3, 'stomach': 3,
    'throat': 8, 'tongue': 3, 'tooth': 2, 'jaw': 2, 'skull': 1,
    'shoulder': 1, 'arm': 3, 'wrist': 1, 'finger': 2, 'thumb': 2,
    'knee': 1, 'ankle': 1, 'hip': 1, 'rib': 1, 'pelvis': 1,
    # Animals
    'dog': 7, 'cat': 5, 'bird': 8, 'fish': 8, 'horse': 3, 'lion': 3,
    'eagle': 8, 'wolf': 5, 'bear': 5, 'deer': 8, 'rabbit': 8,
    'snake': 6, 'spider': 1, 'bee': 8, 'butterfly': 8, 'ant': 1,
    'whale': 8, 'dolphin': 7, 'elephant': 1, 'owl': 2, 'hawk': 2,
    'tiger': 6, 'leopard': 6, 'panther': 6, 'jaguar': 6, 'cheetah': 3,
    'gorilla': 1, 'monkey': 6, 'ape': 2, 'crow': 0, 'raven': 0,
    'swan': 7, 'dove': 7, 'sparrow': 8, 'robin': 8, 'hummingbird': 8,
    'salmon': 8, 'shark': 4, 'octopus': 6, 'jellyfish': 8, 'coral': 1,
    # Food / sustenance
    'food': 3, 'bread': 7, 'wine': 7, 'meat': 3, 'milk': 9,
    'salt': 5, 'sugar': 3, 'honey': 7, 'grain': 3, 'harvest': 3,
    'feast': 3, 'famine': 4, 'hunger': 4, 'thirst': 4, 'drink': 8,
    'eat': 3, 'cook': 3, 'bake': 3, 'taste': 2, 'smell': 2,
    # Colors
    'red': 6, 'blue': 5, 'green': 3, 'yellow': 8, 'white': 7,
    'black': 0, 'gold': 7, 'silver': 5, 'purple': 7, 'orange': 8,
    'brown': 1, 'gray': 0, 'pink': 7, 'violet': 7, 'crimson': 6,
    'indigo': 5, 'turquoise': 7, 'scarlet': 6, 'ivory': 7, 'amber': 8,
    'maroon': 4, 'navy': 1, 'teal': 5, 'coral': 3, 'magenta': 6,
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
    'longing': 3, 'nostalgia': 0, 'regret': 4, 'remorse': 4, 'relief': 7,
    'gratitude': 7, 'admiration': 7, 'contempt': 4, 'disgust': 4, 'pity': 7,
    'sympathy': 7, 'empathy': 7, 'affection': 7, 'tenderness': 7, 'warmth': 7,

    # ── CK-SPECIFIC: CK's own vocabulary ──
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

    # ── CK SELF-DESCRIPTION WORDS ──
    # Every word CK uses to describe himself MUST be in the dictionary
    'ck': 7, 'cl': 1, 'pfe': 2, 'btq': 2, 'd2': 8,
    'cpu': 1, 'gpu': 1, 'fpga': 1, 'bram': 1, 'cuda': 1,
    'http': 1, 'dtw': 2, 'init': 9, 'pre': 9,
    'affinity': 5, 'analysis': 2, 'atlas': 1, 'aware': 2,
    'chat': 3, 'comparison': 2, 'composition': 7, 'controlled': 1,
    'controller': 1, 'curriculum': 3, 'decisions': 5,
    'driven': 3, 'engine': 3, 'evaluator': 2, 'fallback': 9,
    'feels': 2, 'fifteen': 2, 'fingerprinting': 2, 'fixed': 1,
    'fusion': 7, 'gated': 5, 'genomes': 1, 'guided': 3,
    'handler': 1, 'hardware': 1, 'health': 3, 'hebrew': 7,
    'immune': 5, 'integration': 7, 'intent': 3, 'intents': 3,
    'jitter': 6, 'language': 1, 'launcher': 9, 'lens': 2,
    'letter': 1, 'lookup': 2, 'mapped': 1, 'mapping': 1,
    'mappings': 1, 'matching': 2, 'method': 1, 'module': 1,
    'motor': 3, 'natural': 7, 'nervous': 8, 'normalization': 5,
    'output': 3, 'phonaesthesia': 8, 'phoneme': 8, 'physical': 1,
    'pipeline': 1, 'planning': 1, 'processing': 2, 'reads': 2,
    'region': 1, 'retrieval': 2, 'sandbox': 1, 'scoring': 2,
    'security': 5, 'semantic': 7, 'server': 1, 'sliding': 8,
    'socratic': 2, 'speaks': 3, 'species': 1, 'speech': 3,
    'startup': 9, 'state': 1, 'synthesis': 7, 'text': 1,
    'topology': 1, 'translates': 5, 'translation': 5,
    'triple': 2, 'twelve': 2, 'vocabulary': 1, 'voice': 8,
    'words': 1, 'word': 1,

    # ── COMPUTING & TECHNOLOGY ──
    'computer': 1, 'software': 1, 'program': 1, 'application': 1,
    'binary': 1, 'compile': 3, 'interpret': 2, 'execute': 3,
    'runtime': 1, 'debug': 2, 'exception': 4, 'warning': 5,
    'stack': 1, 'heap': 1, 'pointer': 1, 'reference': 1,
    'string': 1, 'integer': 2, 'boolean': 5, 'object': 1,
    'class': 1, 'interface': 1, 'abstract': 0, 'concrete': 1,
    'inheritance': 1, 'polymorphism': 5, 'encapsulation': 1,
    'abstraction': 0, 'recursion': 8, 'iteration': 8,
    'condition': 5, 'branch': 5, 'return': 8, 'yield': 5,
    'async': 8, 'await': 5, 'promise': 7, 'callback': 8,
    'closure': 1, 'scope': 1, 'namespace': 1, 'import': 1,
    'export': 3, 'require': 2, 'include': 1,
    'byte': 2, 'bit': 2, 'packet': 1, 'payload': 1,
    'checksum': 2, 'parity': 5, 'redundancy': 5, 'backup': 9,
    'restore': 9, 'sync': 7, 'merge': 7, 'diff': 2,
    'patch': 9, 'version': 2, 'commit': 3, 'release': 3,
    'pull': 5, 'push': 3, 'fetch': 2, 'clone': 9,
    'neural': 1, 'deep': 2, 'learning': 3, 'training': 3,
    'inference': 2, 'weight': 2, 'bias': 5, 'gradient': 2,
    'backpropagation': 8, 'optimization': 3, 'loss': 4,
    'accuracy': 2, 'precision': 2, 'recall': 2, 'embedding': 1,
    'attention': 2, 'transformer': 1, 'convolution': 8,
    'recurrent': 8, 'generative': 3, 'discriminative': 2,
    'clustering': 1, 'reinforcement': 3, 'supervised': 1,
    'unsupervised': 6, 'reward': 3, 'policy': 1, 'agent': 3,
    'environment': 1, 'action': 3,
    'processor': 1, 'memory': 1, 'cache': 1, 'register': 1,
    'transistor': 1, 'diode': 1, 'capacitor': 1, 'resistor': 5,
    'inductor': 8, 'relay': 8, 'amplifier': 3, 'oscillator': 8,
    'multiplexer': 1, 'decoder': 2, 'encoder': 1,
    'display': 3, 'keyboard': 1, 'mouse': 2, 'touchpad': 2,
    'speaker': 8, 'microphone': 2, 'camera': 2, 'antenna': 8,
    'modem': 8, 'converter': 5, 'filter': 2,
    'firewall': 5, 'load': 4, 'balancer': 5, 'cdn': 1,
    'encryption': 1, 'decryption': 2, 'hash': 2, 'token': 2,
    'session': 8, 'cookie': 1, 'authentication': 5,
    'authorization': 5, 'permission': 5, 'role': 1, 'user': 2,
    'admin': 1, 'sudo': 3, 'docker': 1, 'container': 1,
    'kubernetes': 1, 'virtualization': 1, 'cloud': 1,
    'hosting': 1, 'database': 1, 'migration': 3,
    'deployment': 3, 'api': 1, 'endpoint': 1,

    # ── SCIENCE & MATHEMATICS ──
    'calculus': 1, 'algebra': 1, 'geometry': 1, 'topology': 1,
    'trigonometry': 1, 'combinatorics': 2, 'probability': 2,
    'statistics': 2, 'theorem': 7, 'lemma': 1, 'corollary': 1,
    'manifold': 1, 'tensor': 1, 'scalar': 2, 'vector': 1,
    'dimension': 1, 'eigenvalue': 2, 'determinant': 2,
    'polynomial': 1, 'exponential': 3, 'logarithmic': 2,
    'asymptotic': 0, 'convergent': 7, 'divergent': 6,
    'integral': 7, 'derivative': 2, 'differential': 2,
    'continuous': 8, 'discrete': 2, 'infinite': 7, 'finite': 2,
    'complex': 6, 'imaginary': 0, 'rational': 1, 'irrational': 6,
    'prime': 1, 'composite': 1, 'modular': 1, 'congruent': 7,
    'isomorphic': 7, 'homomorphic': 7, 'bijective': 7,
    'surjective': 3, 'injective': 2,
    'hypothesis': 2, 'theory': 1, 'model': 1, 'simulation': 2,
    'experiment': 2, 'control': 5, 'variable': 5, 'constant': 1,
    'parameter': 2, 'coefficient': 2, 'exponent': 3,
    'relativity': 5, 'thermodynamics': 8, 'electromagnetism': 8,
    'mechanics': 1, 'optics': 2, 'acoustics': 8,
    'genome': 1, 'chromosome': 1, 'nucleotide': 1, 'amino': 1,
    'enzyme': 3, 'catalyst': 3, 'substrate': 1, 'receptor': 2,
    'neuron': 1, 'synapse': 7, 'dendrite': 1, 'axon': 8,
    'cortex': 1, 'hippocampus': 1, 'cerebellum': 1, 'amygdala': 6,
    'mitochondria': 3, 'ribosome': 3, 'cytoplasm': 8, 'nucleus': 9,

    # ── COMMON ENGLISH: Source comment words that CK uses ──
    'each': 2, 'every': 2, 'all': 7, 'some': 5,
    'many': 2, 'few': 2, 'most': 2, 'several': 2,
    'other': 5, 'another': 5, 'different': 5, 'same': 7,
    'new': 9, 'old': 0, 'big': 3, 'small': 0,
    'long': 1, 'short': 0, 'high': 3, 'low': 4,
    'fast': 3, 'slow': 4, 'hard': 5, 'soft': 7,
    'hot': 6, 'cold': 0, 'warm': 7, 'cool': 5,
    'good': 7, 'bad': 4, 'best': 3, 'worst': 4,
    'great': 3, 'little': 0, 'next': 3, 'last': 0,
    'first': 9, 'second': 2, 'third': 2, 'final': 4,
    'main': 1, 'full': 7, 'empty': 0, 'real': 7,
    'true': 7, 'false': 0, 'own': 2, 'whole': 7,
    'half': 5, 'part': 2, 'piece': 2, 'thing': 2,
    'place': 1, 'time': 8, 'way': 1, 'life': 3,
    'world': 7, 'country': 1, 'city': 1, 'home': 7,
    'work': 3, 'play': 9, 'love': 7, 'hate': 4,
    'want': 3, 'need': 3, 'know': 2, 'think': 2,
    'feel': 2, 'see': 2, 'hear': 2, 'say': 3,
    'tell': 3, 'ask': 2, 'answer': 7, 'try': 3,
    'use': 3, 'find': 2, 'get': 3, 'put': 3,
    'take': 3, 'give': 7, 'come': 8, 'go': 8,
    'run': 3, 'make': 3, 'keep': 1, 'let': 5,
    'set': 1, 'show': 3, 'turn': 8, 'call': 3,
    'move': 8, 'live': 3, 'die': 4, 'change': 8,
    'read': 2, 'write': 3, 'name': 1, 'number': 2,
    'people': 7, 'man': 3, 'woman': 3, 'children': 9,
    'house': 1, 'door': 1, 'table': 1, 'book': 1,
    'back': 8, 'down': 4, 'up': 3, 'out': 3,
    'off': 4, 'away': 0, 'together': 7, 'apart': 0,
    'always': 7, 'never': 0, 'sometimes': 8, 'often': 8,

    # ── COMMUNICATION & LANGUAGE ──
    'communicate': 3, 'express': 3, 'articulate': 3, 'convey': 3,
    'describe': 2, 'explain': 3, 'discuss': 5, 'debate': 5,
    'argue': 5, 'persuade': 3, 'convince': 3, 'influence': 3,
    'speak': 3, 'talk': 3, 'whisper': 0, 'shout': 6,
    'sing': 8, 'chant': 8, 'recite': 8, 'narrate': 3,
    'lecture': 3, 'present': 3, 'report': 2, 'announce': 3,
    'declare': 3, 'proclaim': 3, 'broadcast': 8, 'publish': 3,
    'sentence': 1, 'paragraph': 1, 'chapter': 1, 'verse': 8,
    'poem': 8, 'essay': 1, 'article': 1, 'document': 1,
    'letter': 1, 'message': 3, 'conversation': 8, 'dialogue': 8,
    'monologue': 3, 'soliloquy': 0, 'rhetoric': 3, 'eloquence': 7,
    'fluency': 8, 'literacy': 3, 'grammar': 1, 'syntax': 1,
    'semantics': 7, 'pragmatics': 2, 'phonetics': 8, 'morphology': 1,
    'etymology': 9, 'dialect': 5, 'accent': 8, 'idiom': 6,
    'metaphor': 5, 'simile': 5, 'analogy': 5, 'allegory': 7,
    'symbol': 1, 'sign': 1, 'gesture': 3, 'nod': 7,
    'wave': 8, 'point': 2, 'beckon': 3, 'summon': 3,
    'english': 1, 'verb': 3, 'noun': 1, 'adjective': 2,
    'adverb': 2, 'preposition': 1, 'conjunction': 5, 'pronoun': 2,

    # ── GEOGRAPHY & PLACES ──
    'continent': 1, 'island': 1, 'peninsula': 1, 'archipelago': 1,
    'desert': 0, 'plain': 1, 'valley': 1, 'plateau': 1,
    'cliff': 4, 'beach': 8, 'coast': 1, 'shore': 1,
    'harbor': 1, 'bay': 1, 'gulf': 0, 'strait': 5,
    'lake': 8, 'pond': 8, 'creek': 8, 'brook': 8,
    'waterfall': 8, 'glacier': 4, 'iceberg': 4, 'tundra': 0,
    'prairie': 1, 'savanna': 1, 'jungle': 6, 'swamp': 4,
    'marsh': 4, 'wetland': 8, 'meadow': 7, 'grove': 7,
    'field': 1, 'pasture': 3, 'farm': 3, 'ranch': 3,
    'village': 7, 'town': 1, 'suburb': 1, 'downtown': 1,
    'district': 1, 'neighborhood': 7, 'park': 7, 'plaza': 1,
    'market': 5, 'mall': 1, 'shop': 3, 'store': 1,
    'factory': 3, 'mill': 3, 'mine': 2, 'quarry': 2,

    # ── WEATHER & SEASONS ──
    'weather': 8, 'climate': 1, 'temperature': 2, 'humidity': 8,
    'precipitation': 8, 'drought': 4, 'flood': 4, 'frost': 4,
    'hail': 4, 'breeze': 8, 'gust': 6, 'gale': 6,
    'squall': 6, 'drizzle': 8, 'downpour': 4, 'monsoon': 8,
    'blizzard': 6, 'heatwave': 6, 'fog': 0, 'mist': 0,

    # ── ARCHITECTURE & BUILDING ──
    'building': 1, 'house': 1, 'tower': 1, 'castle': 1,
    'palace': 1, 'cathedral': 7, 'chapel': 7, 'shrine': 7,
    'monument': 1, 'statue': 1, 'fountain': 8, 'pool': 8,
    'basement': 0, 'attic': 0, 'cellar': 0, 'rooftop': 1,
    'staircase': 1, 'elevator': 3, 'escalator': 3, 'ramp': 1,
    'lobby': 1, 'foyer': 1, 'vestibule': 1, 'porch': 1,
    'balcony': 1, 'terrace': 1, 'patio': 1, 'courtyard': 1,

    # ── MUSIC & ART ──
    'music': 8, 'song': 8, 'melody': 8, 'harmony': 7,
    'rhythm': 8, 'beat': 8, 'tempo': 8, 'pitch': 8,
    'volume': 2, 'bass': 8, 'treble': 8, 'alto': 8,
    'soprano': 8, 'tenor': 8, 'baritone': 8, 'choir': 7,
    'orchestra': 7, 'ensemble': 7, 'band': 1, 'duet': 5,
    'solo': 0, 'trio': 2, 'quartet': 2, 'quintet': 2,
    'art': 3, 'painting': 3, 'sculpture': 3, 'drawing': 3,
    'sketch': 9, 'portrait': 2, 'landscape': 1, 'abstract': 0,
    'canvas': 1, 'brush': 3, 'palette': 5, 'pigment': 2,
    'ink': 1, 'pen': 3, 'pencil': 3, 'chalk': 1,
    'clay': 1, 'ceramic': 1, 'glass': 1, 'marble': 1,

    # ── GOVERNANCE & SOCIETY ──
    'government': 1, 'democracy': 7, 'republic': 1, 'monarchy': 1,
    'parliament': 1, 'congress': 1, 'senate': 1, 'court': 5,
    'judge': 5, 'jury': 2, 'trial': 2, 'verdict': 5,
    'law': 1, 'justice': 5, 'rights': 7, 'liberty': 7,
    'equality': 5, 'freedom': 7, 'duty': 5, 'responsibility': 5,
    'citizen': 7, 'community': 7, 'society': 7, 'civilization': 7,
    'nation': 1, 'state': 1, 'province': 1, 'territory': 1,
    'border': 1, 'boundary': 1, 'sovereignty': 7, 'diplomacy': 5,
    'treaty': 7, 'alliance': 7, 'coalition': 7, 'federation': 1,
    'election': 5, 'vote': 5, 'ballot': 5, 'campaign': 3,
    'policy': 1, 'regulation': 1, 'reform': 9, 'revolution': 6,

    # ── MATERIALS & SUBSTANCES ──
    'wood': 1, 'metal': 1, 'steel': 1, 'iron': 1, 'copper': 1,
    'aluminum': 1, 'titanium': 1, 'platinum': 7, 'diamond': 7,
    'ruby': 7, 'sapphire': 7, 'emerald': 7, 'pearl': 7,
    'crystal': 1, 'quartz': 1, 'granite': 1, 'limestone': 1,
    'sandstone': 1, 'obsidian': 0, 'jade': 7, 'onyx': 0,
    'plastic': 4, 'rubber': 5, 'leather': 1, 'cotton': 8,
    'silk': 7, 'wool': 8, 'linen': 1, 'nylon': 1,
    'concrete': 1, 'cement': 1, 'asphalt': 1, 'brick': 1,
    'ceramic': 1, 'porcelain': 7, 'terra': 1, 'oxide': 4,

    # ── CK SOURCE: top missing words from comments ──
    'chains': 1, 'patterns': 1, 'becoming': 3, 'process': 3,
    'topic': 1, 'pairs': 2, 'sentences': 1, 'structural': 1,
    'context': 1, 'shape': 1, 'dominant': 2, 'micro': 2,
    'three': 2, 'math': 1, 'sovereign': 7, 'cells': 1,
    'feed': 3, 'domain': 1, 'verb': 3, 'english': 1,
    'organ': 3, 'sentences': 1, 'pairs': 2, 'context': 1,
}
DICTIONARY.update(_CRITICAL)


# ═══════════════════════════════════════════════════════════
# AUTO-EXPANSION: D2 curvature-classified English corpus
# CK's own math assigned operators to 248K+ English words.
# Curated entries above ALWAYS override auto-classified ones.
# ═══════════════════════════════════════════════════════════

import os as _os, json as _json

_AUTO_PATH = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'ck_dictionary_auto.json')
_auto_loaded = 0

if _os.path.exists(_AUTO_PATH):
    try:
        with open(_AUTO_PATH, 'r') as _f:
            _auto_raw = _json.load(_f)
        for _w, _v in _auto_raw.items():
            _wl = _w.strip().lower()
            if _wl and _wl not in DICTIONARY:
                # Format: [operator, frequency] or just operator
                _op = _v[0] if isinstance(_v, list) else _v
                DICTIONARY[_wl] = _op
                _auto_loaded += 1
        del _auto_raw  # free memory
    except Exception:
        pass  # auto-expansion is optional, curated core always works


# ═══════════════════════════════════════════════════════════
# PHONAESTHESIA -- sound-meaning mapping
# Initial consonant clusters carry semantic weight
# ═══════════════════════════════════════════════════════════

PHONAESTHESIA = {
    # Two-letter clusters
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
    'sc':  2,  # scale, scope, scan -- measurement
    'sk':  4,  # skip, skim, skull -- quick/collapse
    'rh':  8,  # rhythm, rhyme, rhetoric -- flow
    'gn':  2,  # gnosis, gnomic -- knowledge
    'pn':  8,  # pneuma, pneumatic -- breath
    'mn':  2,  # mnemonic -- memory
    'ps':  2,  # psychology, pseudo -- mental
    'di':  5,  # divide, differ, diverge -- duality
    'ex':  3,  # expand, extend, express -- outward growth
    'un':  0,  # undo, unknown, unset -- negation
    're':  9,  # reset, return, renew -- renewal
    'de':  4,  # decay, decline, destroy -- collapse
    'en':  3,  # enable, enrich, engage -- empowerment
    'in':  1,  # inside, include, integrate -- structure
    'co':  7,  # coherent, cooperate, connect -- harmony
    'sy':  1,  # system, symbol, syntax -- structure
    # Three-letter clusters
    'str': 1,  # structure, strength, strategy -- framework
    'shr': 4,  # shrink, shred, shrivel -- collapse
    'scr': 6,  # scramble, scratch, scream -- chaos
    'thr': 3,  # thrive, through, thrust -- progress
    'spr': 3,  # spring, spread, sprout -- growth
    'spl': 4,  # split, splash, splinter -- breaking
    'chr': 8,  # chrome, chronic, chronological -- time/cycle
    'sch': 1,  # schema, schedule, school -- structure
    'pre': 9,  # prefix, prepare, precede -- before/beginning
    'pro': 3,  # progress, produce, promote -- growth
    'tra': 8,  # translate, transfer, transit -- movement
    'con': 7,  # converge, connect, concert -- togetherness
    'dis': 4,  # dissolve, disrupt, disconnect -- breaking apart
    'mis': 4,  # mistake, misfire, misplace -- error/failure
    'out': 3,  # outgrow, outperform, output -- exceeding
    'sub': 0,  # submarine, submerge, subtle -- beneath/hidden
    'sur': 3,  # surpass, survive, surface -- overcoming
    'int': 1,  # internal, integrate, interface -- inner structure
    'imp': 3,  # improve, impact, implement -- forceful progress
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
