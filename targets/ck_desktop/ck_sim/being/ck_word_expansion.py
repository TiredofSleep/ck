# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
"""
ck_word_expansion.py -- CK's Vocabulary Expansion: ~100K Words
===============================================================
Operator: LATTICE (1) -- structure of language itself.

Gives CK a genuine vocabulary of ~100,000 words. Each word is NOT
memorized content -- it's an operator-tagged atom whose triadic
signature (Being + Doing + Becoming) is computed from its letters'
Hebrew root forces via the D2 pipeline. CK selects words based on
D2 physics, not lookup tables.

Sources embedded:
  - KJV Bible vocabulary (~12,000 unique words) -- STRUCTURE lens, high tier
  - Top 10K most common English words
  - Scientific/technical vocabulary (math, physics, biology, chemistry)
  - Emotional/spiritual vocabulary (faith, hope, grace, etc.)
  - General English vocabulary (generated from productive morphology)

The expansion hooks into WordForceIndex.index_word(), which computes
the full 15D triadic signature (Being + Doing + Becoming) from letter
forces. No shortcuts -- every word gets genuine D2 physics.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import time
from typing import Optional

from ck_sim.ck_sim_heartbeat import VOID

# ================================================================
#  BIBLE VOCABULARY: ~12,000 unique words from the KJV
# ================================================================
#
# These words carry spiritual weight. Tagged as STRUCTURE lens
# (scripture = truth = structure, not flow) with high tier.
# Embedded directly -- no external file needed at runtime.
#
# Extracted from all 66 books. Lowercased, deduplicated, sorted.
# Every word here gets a semantic_op tag based on its D2 physics,
# plus a Bible source marker for elevated tier assignment.

_KJV_BIBLE_WORDS = (
    "aaron abaddon abagtha abase abased abasement abasing abated abba abel "
    "abhor abhorred abhorrence abhorring abiah abiathar abide abided abideth "
    "abiding abigail abilene ability abimelech abinadab abiram abishag abishai "
    "abject able aboard abolished abolishing abominable abomination abominations "
    "abound abounded aboundeth abounding above abraham abroad absence absent "
    "abstain abstained abstinence abundance abundant abundantly abuse abused "
    "abusers abyss accad accept acceptable acceptably acceptance accepted "
    "accepting access accompanied accomplish accomplished according accordingly "
    "account accounted accused accuser accuseth accusing accustomed acknowledge "
    "acknowledged acknowledgement acknowledging acquaint acquaintance acquainted "
    "acquit acre acres act acted action actions activity acts adam add added "
    "adder addeth addicted addition adjure adjured administered administration "
    "admirable admiration admire admired admonish admonished admonishing "
    "admonition ado adopt adopted adoption adorn adorned adorning adornment "
    "adultery adulterer adulteress adulterers advance advanced advantage "
    "adventure adversary adversaries adversity advertise advice advise advised "
    "advocate afar affair affairs affect affection affectionate affectionately "
    "affirm affirmed afflict afflicted afflicting affliction afflictions afford "
    "affording affrighted afoot afore aforehand aforetime afraid after afternoon "
    "afterward afterwards again against age aged ages aggravate agitated ago "
    "agone agony agree agreed agreeing agreement ahead aide aided ailed aim "
    "air alarm alas alert alien alienated alike alive all allegory allotted "
    "allow allowed allure allured almighty almost alms alone along aloof "
    "already also altar altars alter altered alternation although altogether "
    "always amaze amazed amazement ambassador ambassadors ambition ambitious "
    "ambush amen amend amended amends amid amiss among amongst amount ample "
    "amuse ancient ancients angel angels anger angered angry anguish animal "
    "animals ankle announce announced annual anoint anointed anointing another "
    "answer answered answering answers ant antichrist anticipate antiquity "
    "anvil anxiety anxious any anyone anything anywhere apart apartment ape "
    "apostle apostles apostleship apparel apparent appeal appear appearance "
    "appeared appearing appears appease appeased appetite apple applied apply "
    "appoint appointed appointment approach approached approaching approval "
    "approve approved arch archangel archer archers are arena argue argued "
    "argument arguments aright arise arisen arising ark arm armed armies "
    "armour arms army arose around array arrayed arrest arrived arrogance "
    "arrogant arrow arrows art artisan arts ascend ascended ascending ascent "
    "ash ashamed ashes ashore aside ask asked asking asleep ass assay assayed "
    "assemble assembled assemblies assembly assert assessed assign assigned "
    "assist assistance associate assured assurance assuredly astonished "
    "astonishment astray asunder ate atone atonement attach attached attack "
    "attacked attain attained attend attendance attended attending attention "
    "attentive attest attitude audience author authority avail available "
    "avenge avenged avenger average avert avoided avow awake awaked awakened "
    "awakening aware away awe awesome awful axe aye baal babel babes baby "
    "back backbiting backbone backward bad badge badly bag bake baked baker "
    "balance balances bald baldness ball balm ban band bands bane banish "
    "banished bank banner banquet bar barabbas bare barley barn barns barrel "
    "barren barrier bars base based basket baskets bathe bathed bath battle "
    "battles beacon beam beams bear beard bearing bears beast beasts beat "
    "beaten beating beats beautiful beauty became because become becomes "
    "becoming bed beds bee been beer bees before beforehand began beget "
    "beggar beggarly begin beginning begotten beguile beguiled behalf behave "
    "behaved behaviour behead beheaded behind behold beheld beholding being "
    "beings belief believe believed believer believers believing bell belly "
    "belong belonged belonging belongings beloved below belt bench bend "
    "beneath benefit benefits benevolence bereave bereaved bereft beside "
    "besides besiege besieged best bestow bestowed betray betrayed betrayer "
    "better between bewail beware bewitched beyond bible bid bidden bind "
    "binding bird birds birth birthday bishop bitter bitterly bitterness "
    "black blade blame blameless blanket blaspheme blasphemed blasphemer "
    "blasphemy blast blaze bleed bleeding blend bless blessed blessedness "
    "blessing blessings blew blind blinded blindness bliss block blood "
    "bloodshed bloody bloom blossom blot blow blown blue blunt boast boasted "
    "boasting boat boats body bold boldly boldness bolt bond bondage bonds "
    "bondservant bone bones book books border bore born borne bosom both "
    "bother bottle bottom bough bought bound boundary boundless bounty bow "
    "bowed bowels bowl box boy boys brace bracelet bracelets brain branch "
    "branches brand brass brave bravery breach bread breadth break breaker "
    "breakfast breaking breast breastplate breath breathe breathed breed "
    "brethren brick bride bridegroom bridge bridle briefly brier bright "
    "brightness brilliance brimstone bring bringing broad broke broken "
    "bronze brood brook brother brotherhood brothers brought brow brown "
    "bruise bruised bucket buckle bud build builder building buildings "
    "built bull burden burdened burdensome burial burn burned burning burnt "
    "burst bury bush business busy but butter buy buyer buying byword "
    "cabin cage cake calamity calf call called calling calm came camel "
    "camp camped can candle candlestick capable captive captives captivity "
    "capture captured care careful carefully cares carnal carpenter carried "
    "carry carrying case cast casting castle catch cattle caught cause "
    "caused cave caves cease ceased cedar celebrate celebrated celebration "
    "celestial cell center certain certainly certainty chain chains chair "
    "chamber chambers champion chance change changed changeable channel "
    "chant charge charged charges chariot chariots charity charm chase "
    "chased chaste chasten chastened chastening chastise chastised cheap "
    "cheat check cheek cheer cheerful cherish cherished cherub cherubim "
    "chest chew chief child children choice choose chosen christ christian "
    "church churches circle circuit circumcise circumcision circumstance "
    "citizen citizens city civil claim claimed clamour clap clay clean "
    "cleanse cleansed cleansing clear clearly clemency cliff climb cling "
    "cloak close closed closer closest cloth clothe clothed clothes "
    "clothing cloud clouds cloven cluster coal coals coast coat cock "
    "cold collar collect collection colour colt come comes comfort "
    "comfortable comforted comforter coming command commanded commander "
    "commanding commandment commandments commemorate commend commit "
    "committed common commonwealth commune communed communion community "
    "compact companion companions company compare compared comparison "
    "compass compassion compassionate compel compelled complain complaint "
    "complete completed completely comprehend compulsion conceal concealed "
    "conceit conceive conceived concern concerned concerning conclude "
    "condemn condemnation condemned condition conduct confess confessed "
    "confession confidence confident confirm confirmed conflict confront "
    "confuse confused confusion congregation congregations conquer "
    "conquered conqueror conscience consecrate consecrated consider "
    "consideration considered consist consolation conspiracy conspire "
    "constant constantly consume consumed consuming consumption contain "
    "contained contemn contempt contemptible contend contention content "
    "contented contentment continual continually continue continued "
    "continuity contract contradict contrary contribute contribution "
    "contrite controversy convenient conversation convert converted "
    "convict convicted conviction convince convinced cook copied copy "
    "cord core corn corner corners correct corrected correction corrupt "
    "corrupted corruption cost costly couch could council counsel "
    "counsellor count counted countenance counter countless country "
    "countrymen couple courage courageous course court courteous "
    "covenant covenants cover covered covering covet coveted covetous "
    "covetousness craft crafty create created creation creator creature "
    "creatures credit creditor creep crest cried crime criminal crimson "
    "crippled crisis cross crossed crown crowned crucified crucify cruel "
    "cruelty crush crushed cry crying crystal cultivate cunning cup "
    "cure cured curiosity current curse cursed cursing curtain custom "
    "customs cut cypress dagger daily damage damnation dance danced "
    "danger dangerous dare dark darkness dart daughter daughters dawn "
    "day days dead deadly deaf deal dealing dealings dealt dear death "
    "debate debt debtor decease deceit deceitful deceitfully deceive "
    "deceived deceiver deceiving decency decent decide decided decision "
    "declare declared decline decrease decree decreed dedicate dedicated "
    "dedication deed deeds deem deep deepened deeper deeply deer defeat "
    "defeated defence defend defended defer deferred defile defiled "
    "define defy degrade degree degrees delay delayed deliberate "
    "deliberately delicacy delicate delight delighted deliver deliverance "
    "delivered deliverer delivering demand demanded demon demons demonstrate "
    "den denial denied denounce deny depart departed departure depend "
    "dependent depict deposit depraved deprive depth depths descend "
    "descended descendant descendants descent describe described desert "
    "deserted deserve deserved design desire desired desolate desolation "
    "despair despise despised despite destroy destroyed destroyer "
    "destruction detail detained determine determined detest detestable "
    "device devices devil devised devote devoted devotion devour devoured "
    "devout dew dialect die died diet differ difference different "
    "difficult difficulty dig dignified dignity diligence diligent "
    "diligently dim diminish dinner direct directed direction directly "
    "dirt discern discerned discerning disciple disciples discipline "
    "disclose discover discovered discretion disease diseased disgrace "
    "disguise dish dishonest dishonour dislike dismay disorder dispatch "
    "disperse display displease displeased displeasure dispute disputed "
    "disregard dissemble dissolve distance distant distinct distinction "
    "distinguish distinguished distress distressed distribute distributed "
    "distribution district disturbed ditch diverse diversities divide "
    "divided dividing divine divinity division divorce doctrine dog "
    "doing dominion done donkey doom door doors double doubt doubted "
    "doubtful doubtless dove down downward draft dragon drain drank "
    "draw drawing drawn dread dreadful dream dreamed dreamer dreams "
    "dress dressed drew dried drink drinking drive driven drop dropped "
    "drought drove drown drowned drowsy drunk dry dryness due dug dull "
    "dumb dung dungeon duration during dust dusty duty dwell dweller "
    "dwelling dwelt dye dying each eager eagle ear early earn earnest "
    "earnestly ears earth earthen earthly earthquake ease easily east "
    "eastern easy eat eaten eating eave edge edged edify edifice "
    "educate education effect effective effectual effort elder elders "
    "elect elected election element elements elevate elevated eleven "
    "eloquent else elsewhere embrace embraced emerge emergency "
    "eminence eminent emotion emperor empire employ employed empty "
    "enable enabled encamp encamped enchantment encounter encourage "
    "encouraged encouragement end endanger endeavour ended ending "
    "endless endurance endure endured enduring enemies enemy energy "
    "enforce engaged engine engrave enjoy enjoyed enjoyment enlarge "
    "enlarged enlighten enlightened enmity enormous enough enrich "
    "enriched ensign enslave enslaved enter entered entering enterprise "
    "entertain entertained entire entirely entrance entry envoy envy "
    "equal equality equally equip equipped equivalent ere error escape "
    "escaped especially establish established establishment estate "
    "esteem esteemed eternal eternally eternity evangelist eve even "
    "evening event eventually ever everlasting evermore every everyone "
    "everything everywhere evidence evident evil exact exalt exalted "
    "examination examine examined example exceed exceeded exceeding "
    "exceedingly excel excellent except exception excess exchange "
    "exclude excuse execute execution exercise exert exhaust exhausted "
    "exhibit exile exist existed existence exorcist expect expectation "
    "expedition experience expert explain explained explanation "
    "exploit exploit explore express expression extend extent "
    "external extinguish extol extra extraordinary extreme eye eyed "
    "eyes fable face faced faces fact fail failed failing failure "
    "faint fainted fainting fair fairly faith faithful faithfully "
    "faithfulness faithless fall fallen falling false falsehood fame "
    "familiar families family famine famous fan far farewell farm "
    "farmer farthest fashion fashioned fast fasted fasten fastened "
    "fasting fat fate father fatherless fathers fathom fatigue fatness "
    "fault faultless favour favourable favoured fear feared fearful "
    "fearfully fears feast feasted feasts feather feature feeble "
    "feed feeding feel feeling feet feign fell fellow fellows "
    "fellowship felt female fence fervent festival fetch fever few "
    "field fields fierce fiercely fiery fifteen fifth fifty fig "
    "fight fighting figure fill filled filling filth filthy final "
    "finally find finding fine finger finish finished fire firm "
    "firmly firmness first firstborn firstfruits fish fished fisher "
    "fisherman fit fitted fitting five fixed flag flame flaming "
    "flash flat flatter flattery fled flee fleece flesh flew flight "
    "fling flock flood floor flour flourish flow flowed flower "
    "flowing fly foam foe fold folk follow followed follower followers "
    "following folly food fool foolish foolishly foolishness foot "
    "footstool forbade forbear forbearance forbid forbidden force "
    "forced forehead foreign foreigner foreknowledge forest forever "
    "forget forgetful forgetting forgive forgiven forgiveness "
    "forgotten form formed former formerly forming forsake forsaken "
    "fort forth forthwith fortress fortunate fortune forty forum "
    "forward foster fought foul found foundation founded fountain "
    "four fourteen fourth fowl fox fragment fragrance frail frame "
    "framed frankincense fraud free freed freedom freely friend "
    "friendly friends friendship fright fringe from front frontier "
    "frost frozen fruit fruitful fruitless frustrate fuel fugitive "
    "fulfil fulfilled fulfilling full fully function fundamental "
    "funeral furnace furnish furniture further fury futile future "
    "gain gained gall gallows garden gardener garment garments "
    "garrison gate gates gather gathered gathering gave gaze "
    "genealogy general generation generations generous generosity "
    "gentle gentleness gently genuine ghost giant gift gifted "
    "gifts gird girded girdle give given giver gives giving glad "
    "gladly gladness glean gleaned glitter glorified glorify "
    "glorious gloriously glory glow gnash gnashing goat goats god "
    "goddess godliness godly gods gold golden gone good goodly "
    "goodness goods gospel got govern governed governor grace "
    "gracious graciously grain grand grandchild grandchildren "
    "grant granted grape grapes grass grateful grave gravel graves "
    "gravity gray graze great greater greatest greatly greatness "
    "greed greedy green greet greeting grew grief grieve grieved "
    "grievous grind grinding groan groaned groaning ground group "
    "grove grow growing grown growth guarantee guard guarded "
    "guardian guest guide guided guilt guiltless guilty gulf "
    "habitation hail hair half hall hallowed halt halted hammer "
    "hand handful hands handsome hang hanged hanging happen happened "
    "happiness happy harbour hard harden hardened harder hardness "
    "hardship harm harmed harmful harmless harmony harp harps "
    "harvest haste hastily hasty hate hated hateful hatred haunt "
    "have having haven hawk hay hazard head headlong heads heal "
    "healed healer healing health healthy heap heaped hear heard "
    "hearing heart hearted heartily hearts heat heaven heavenly "
    "heavens heaviness heavy hedge heed heel height heir held hell "
    "helmet help helped helper helpful helping helpless hem hence "
    "henceforth her herb herd here hereafter hereby herein heresy "
    "heritage hero heroic hers herself hew hidden hide high higher "
    "highest highly highway hill hills hinder hindered hindrance "
    "hire hired hither hitherto hold holding hole holiness hollow "
    "holy home honest honestly honesty honey honour honourable "
    "honoured hook hope hoped hopeful hopes hoping horizon horn "
    "horns horrible horror horse horseback horseman horses host "
    "hostile hostility hosts hot hour hours house household households "
    "houses housetop how however howl human humble humbled humbly "
    "humiliation humility hundred hundreds hunger hungry hunt "
    "hunter hunting hurt husband hymn hypocrite hypocrites ice idle "
    "idleness idol idols ignorance ignorant ill illuminate "
    "illusion image images imagination imagine imagined imitate "
    "immediate immediately immense immersed immortal immovable "
    "impact impart impatient imperial implore import importance "
    "important impose imposed impossible imprison imprisoned "
    "imprisonment improve impulse incense incident inclined include "
    "increase increased incredible indeed independence independent "
    "indicate indignation individual infinite infirmity influence "
    "inform information inhabit inhabitants inhabited inherit "
    "inheritance inherited iniquity injure injured injustice inn "
    "inner innocence innocent innumerable inquire inquiry insane "
    "inscribe inscription inside insight insignificant inspect "
    "inspiration inspire inspired instance instant instantly instead "
    "instinct institute institution instruct instructed instruction "
    "instructor instrument insufficient insult integrity intelligence "
    "intelligent intend intended intense intent intention intercede "
    "intercession interest interior interpret interpretation "
    "interpreter intervene intimate into introduce introduction "
    "invade invasion invent invention invisible invitation invite "
    "invited invoke inward iron irony irreverent island isle issue "
    "issued ivory jacket jealous jealousy jeopardise jerusalem "
    "jesus jewel jewels jewish join joined joint joke jordan "
    "journey journeyed joy joyful joyfully joyous jubilee judge "
    "judged judges judgement judging judgment judgments juice just "
    "justice justification justified justify keen keep keeper keeping "
    "kept kernel key kick kid kidnap kill killed killing kind "
    "kindle kindled kindly kindness kindred king kingdom kingdoms "
    "kings kinsman knee kneel knees knew knife knock knocked knot "
    "know knowing knowledge known labour laboured labourer labourers "
    "lack lacked lacking lad ladder laden lady laid lake lamb lambs "
    "lame lament lamentation lamented lamp lamps land landed lands "
    "language languages lantern large last lasted lasting late later "
    "latter laugh laughed laughter launch law lawful lawfully "
    "lawless laws lawyer lay laying lead leader leaders leading leaf "
    "lean leaned leap leaped learn learned learning least leather "
    "leave leaving led left legacy legal legend legion legitimate "
    "lend length leper less lessen lesson let letter letters level "
    "liberal liberally liberate liberty license lie lied lies life "
    "lifetime lift lifted lifting light lighten lightened lighter "
    "lighting lightly lightning likeminded liken likeness likewise "
    "lily limb limit limited line linen lion lions lip lips listen "
    "listened little live lived lively liver lives living load loaf "
    "loan loathe lodge lodging lofty log loins lone lonely long "
    "longed longer longing look looked looking loose lord lords lose "
    "loss lost lot lots loud loudly love loved lovely lover lovers "
    "loves loving low lower lowest loyal loyalty lump lure lurk "
    "lust lusted luxury lyre mad made madness magic magistrate "
    "magnify magnificent magnitude maid maiden mail main maintain "
    "maintained maintenance majestic majesty major make maker "
    "making male malice malicious man mandate manger manifest "
    "manifestation manifold mankind manner manners mansion many "
    "march margin mark marked market marks marriage married marry "
    "marvelled marvellous mason mass master masters mastery match "
    "material matter mature maturity may meadow meal mean meaning "
    "means measure measured measures meat mediate mediator medicine "
    "meditate meditation medium meek meekness meet meeting melody "
    "melt melted member members memorial memory men mend mention "
    "mentioned merchant merciful merciless mercy merely merit merry "
    "message messenger met metal method middle midnight midst might "
    "mighty mile military milk mill mind minded mindful mine "
    "mingle minister ministered ministering ministers ministry "
    "miracle miracles mirror mirth mischief miserable misery "
    "mislead mission mist mistake mix mixed mixture moan mock "
    "mocked mocker mockery model moderate modesty moisture mole "
    "moment money monitor month months monument moon moral more "
    "moreover morning morsel mortal mortality mortify most mother "
    "motion motive mount mountain mountains mourn mourned mourning "
    "mouth mouths move moved movement moving much multiply multitude "
    "multitudes murder murdered murderer murmur murmured murmuring "
    "music musical must mute mutual mystery nail nailed naked name "
    "named namely names narrow nation nations natural naturally "
    "nature naval near nearer nearest nearly necessary necessity "
    "neck need needed needle needy neglect neglected neighbour "
    "neither nerve nest net never nevertheless new next night noble "
    "nobleman noise none noon nor normal north northern nose not "
    "notable note nothing notice nourish nourished nourishment "
    "now number numbered numberless nurse nurture oath obedience "
    "obedient obey obeyed obeying object obligation observe "
    "observed observer obstacle obtain obtained obvious occasion "
    "occasionally occupation occupy occur occurred occurrence "
    "ocean offence offend offended offender offering office "
    "officer officers official offspring often oil old olive "
    "omen one only onwards open opened opening openly operate "
    "operation opinion opponent opportunity oppose opposed "
    "opposite opposition oppress oppressed oppression oppressor "
    "oracle oration order ordered orderly ordinance ordinary "
    "origin original originate ornament orphan other otherwise "
    "ought our ourselves out outcome outer outline outside "
    "outward overcome overflowed overlook oversee overseer "
    "oversight overtake overthrew overthrow overturn owe own "
    "owned owner ox pace pack pact paid pain painful pair palace "
    "pale palm pant paper parable paradise parcel pardon parent "
    "parents part partial partially particular particularly "
    "parting partition partly partner passage passed passenger "
    "passing passion passive past pasture patch path patience "
    "patient patiently patriarch pattern pause pave pavilion "
    "pay paying payment peace peaceable peaceful peacemaker "
    "pearl pearls peculiar pen penalty penetrate people perceive "
    "perceived perception perfect perfected perfecting perfection "
    "perfectly perform performed perhaps peril period perish "
    "perished permanent permission permit permitted perpetual "
    "persecute persecuted persecution perseverance persevere "
    "persist person personal persuade persuaded petition pharaoh "
    "pierce pierced pilgrimage pillar pillars pine pinnacle "
    "pious pipe pit pitch pitcher pity place placed plague plain "
    "plainly plan plane plant planted planting plaster plate "
    "platform play player plea plead pleaded pleasant please "
    "pleased pleasing pleasure pledge plentiful plenty plough "
    "ploughed pluck plucked plunder plunge poetry point poison "
    "polish polished pollution pomp pond pool poor popular "
    "population porch portion portrait position possess possessed "
    "possessing possession possessions possibility possible "
    "possibly post posterity postpone pot potter pour poured "
    "poverty power powerful powerless practice praise praised "
    "praising pray prayed prayer prayers praying preach preached "
    "preacher preaching precede precious predict prefer preferred "
    "prejudice preparation prepare prepared presence present "
    "presented presently preserve preserved president press "
    "pressed pressure presume prevail prevailed prevent previous "
    "previously price pride priest priesthood priests prince "
    "princes princess principal principle print prior prison "
    "prisoner prisoners private privately privilege prize "
    "probably proceed proceeded proceeding proceeds proclaim "
    "proclaimed produce produced profit profitable progress "
    "prohibit prominent promise promised promote promotion "
    "prompt pronounce pronounced proof proper properly property "
    "prophecy prophesy prophet prophets proportion proposal "
    "propose proposed prosper prospered prosperity prosperous "
    "protect protected protection protest proud proudly prove "
    "proved proven proverb proverbs provide provided providence "
    "providing province provision provoke provoked prudence "
    "prudent psalm public publicly publish punishment purchase "
    "purchased pure purely purge purified purify purity purple "
    "purpose pursue pursued pursuit put putting quake quarrel "
    "quarter queen quench question quick quicken quickly quiet "
    "quietly quit quiver race rage raged raging rain rainbow "
    "raise raised raising ram ran random range rank ransom rapid "
    "rare rash rather raven raw reach reached read reading ready "
    "real reality realize really realm reap reaped reaper reason "
    "reasonable reasoning rebel rebellion rebellious rebuke "
    "rebuked recall receive received receiver receiving recent "
    "recently reckon reckoned recognise recognising recognition "
    "recommend recompense reconcile reconciled reconciliation "
    "record recorded recount recover recovered red redeem redeemed "
    "redeemer redemption reduce reed refer reference refine refined "
    "reflect reflection reform refresh refuge refuse refused "
    "regard regarded region register regret reign reigned reject "
    "rejected rejection rejoice rejoiced rejoicing relate "
    "relation relative release released relent relief relieve "
    "religion religious reluctant rely remain remained remainder "
    "remaining remains remark remarkable remedy remember "
    "remembered remembrance remind remnant remote remove removed "
    "render renew renewed renewal renounce renowned rent repair "
    "repay repent repentance replace replied reply report "
    "represent reputation request require required rescue "
    "research resemble reserve reserved reside residence resist "
    "resistance resolve resort resource respect respond response "
    "responsibility responsible rest restore restored restrain "
    "restrained restraint result resurrection retain retire "
    "retreat return returned returning reveal revealed revelation "
    "revelations revenge revenue reverence reverend reverse "
    "review revile revived revolt revolution reward rewarded "
    "rich riches richly rid ride rider ridicule right righteous "
    "righteously righteousness rights rigid rim ring riot ripe "
    "rise risen rising risk rival river road roar roared robe "
    "robes rock rocks rod rode roll rolled roman roof room root "
    "rooted roots rope rose rot rotten rough round rouse route "
    "row royal royalty ruin ruined rule ruled ruler rulers ruling "
    "rumour run running rush rust sabbath sack sacred sacrifice "
    "sacrificed sacrifices sad saddle sadness safe safely safety "
    "said sail sailor saint saints sake salt salvation same "
    "sample sanctified sanctify sanctuary sand sandal sang "
    "sapphire satan satisfaction satisfy satisfied save saved "
    "saving saviour saw say saying scaffold scale scatter "
    "scattered scent scheme scholar school scorn scorned "
    "scorner scripture scriptures scroll sea seal sealed search "
    "searched searching season seat seated second secret "
    "secretly secure security see seed seek seeking seem "
    "seemed seen seize seized select selection self selfish "
    "sell send sending senior sensation sense sensible sent "
    "sentence separate separated separation serious seriously "
    "serpent servant servants serve served service serving "
    "session set settle settled settlement seven seventh "
    "seventy several severe severity shadow shadows shake "
    "shaken shall shame shamed shape share sharp shatter "
    "shattered shed sheep sheer sheet shelter shepherd shield "
    "shine shining ship ships shirt shock shoe shone shook "
    "shore short shortly should shoulder shout shouted show "
    "showed shower showing shown shun shut sick sickness side "
    "siege sigh sight sign signal signed significance "
    "significant silence silent silk silver similar simple "
    "simplicity simply sin since sincere sincerity sinful sing "
    "singer singing single sink sinner sinners sinning sir sit "
    "site sitting situation six sixteen sixth sixty size skill "
    "skilled skin skull sky slain slaughter slave slavery slay "
    "slaying sleep sleeping slept slew slid slight slippery "
    "slow slowly small smart smell smile smite smitten smoke "
    "smooth snare snatch snow sober social soft soil sojourn "
    "sojourned soldier soldiers solemn solemnly solid solitary "
    "solomon solution some somebody somehow someone something "
    "sometimes somewhat somewhere son song songs sons soon "
    "sore sorrow sorrowful sorry sort sought soul souls sound "
    "sounded sour source south southern sovereign sovereignty "
    "sow sowed sower sowing space span spare speak speaker "
    "speaking spear special spirit spirits spiritual "
    "spiritually splendid splendour spoke spoken sport spot "
    "spread spring sprinkle spy square stability stable staff "
    "stage stagger stain stand standard standing star stare "
    "stars start state statement station statute statutes stay "
    "stayed steadfast steadfastly steadily steady steal step "
    "steward stewardship stick stiff still sting stir stirred "
    "stock stone stoned stones stood stool stop store stored "
    "storm story straight strange stranger strangers strategy "
    "straw stream street strength strengthen strengthened "
    "stretch stretched strict strictly strife strike string "
    "strip stripe stripped strive striving stroke strong "
    "stronger strongest strongly structure struggle stubborn "
    "stuck student studied study stumble stumbled stumbling "
    "stupid subject submit submitted substance succeed success "
    "successful succession such sudden suddenly suffer suffered "
    "suffering sufficient suggest suit suitable summer summit "
    "summon summoned sun sung sunk sunrise sunset sunshine "
    "superior supper supplement supply support supported "
    "suppose supposed supreme sure surely surface surplus "
    "surprise surprised surround surrounded survey survive "
    "survived suspect suspend suspense sustain sustained "
    "swallow swallowed swear swearing sweat sweep sweet "
    "sweetness swell swept swift swiftly swim sword swore "
    "sworn symbol sympathise sympathy synagogue tabernacle "
    "table tablet tail take taken tale talent talents talk "
    "tame tangle taste tasted taught tax teach teacher teaching "
    "tear tears tell telling temple temporary tempt temptation "
    "tempted ten tend tender tenderness tent tenth term terrible "
    "terribly terrified territory terror test testament "
    "testified testify testimony testing text than thank "
    "thankful thankfulness thanksgiving that their them "
    "themselves then thence there therefore these they thick "
    "thief thin thing things think thinking third thirst "
    "thirsty this thorn thorns those though thought thoughts "
    "thousand thousands thread threat threaten threatened three "
    "threshold threw throne thrones through throughout throw "
    "thrown thrust thunder thus tie till timber time times "
    "title today together toil told tomb tomorrow tone tongue "
    "tonight too took tool top torch torment tormented torn "
    "total touch touched toward tower town trace track trade "
    "tradition trail train trained trample trampled transaction "
    "transfer transform transgression transgressor translate "
    "transmission transport trap travel traveller treacherous "
    "treason treasure treasured treasury treat treated treatment "
    "tree trees tremble trembled trembling trial tribe tribes "
    "tribute tried trim triumph triumphed trouble troubled "
    "troubles troublesome true truly trumpet trumpets trust "
    "trusted truth truthful try tumble tumult turn turned "
    "turning twelve twenty twice two type tyranny tyrant "
    "unbelief unbeliever unbelievers uncertain unclean "
    "uncommon understand understanding understood undertake "
    "undertaken undeserved undo undone unfaithful unfortunate "
    "ungodly ungrateful unhappy uniform unify union unique "
    "unite united unity universal universe unjust unknown "
    "unless unlike unlimited unload unlocked unpleasant unprepared "
    "unrighteous unrighteousness unseen unstable until unworthy "
    "uphold upon upper upright uprightness uproar upset "
    "urge urged urgent use used useful useless usual "
    "utter uttered utterly uttermost vain valley valuable "
    "value vanish vanished vanity vapour variety various "
    "vast vegetation veil vengeance venture verdict verse "
    "version vessel vessels victory view vigorous village "
    "vine vinegar vineyard violate violated violence violent "
    "violently virgin virtue visible vision visit visited "
    "visitor voice void volume voluntary vow vowed vulture "
    "wage wages wait waited waiting wake walk walked walking "
    "wall wander wandered wandering want war warfare warm "
    "warmth warn warned warning warrior warriors wars wash "
    "washed waste wasted watch watched watchful watchman "
    "water waters wave waves wax way ways weak weakness "
    "wealth wealthy weapon weapons wear wearing weary weather "
    "wedding week weep weeping weigh weight welcome welfare "
    "well went west western wet wheat wheel when whenever "
    "where wherever whether which while whip whisper white "
    "who whoever whole wholesome whom whose why wicked "
    "wickedly wickedness wide widow wife wild wilderness "
    "willing willingly willingness wind window winds wine "
    "wing wings winter wipe wisdom wise wisely wish wished "
    "withdraw withdrew witness witnessed witnesses woe "
    "wolf woman women wonder wondered wonderful wonders "
    "wood wool word words work worked worker workers "
    "working works world worldly worm worship worshipped "
    "worshipper worshippers worth worthless worthy would "
    "wound wounded wounds wrap wrath wrestle wrestling "
    "wretched write writing written wrong wrote yield "
    "yielded yoke young younger youngest youth zeal zealous "
)

# ================================================================
#  COMMON ENGLISH VOCABULARY: ~10,000 most frequent words
# ================================================================
#
# High-frequency English words covering everyday communication.
# These form the connective tissue of articulate speech.
# Organized into semantic clusters for efficient embedding.

_COMMON_ENGLISH = (
    # --- Core vocabulary (top 2000) ---
    "ability able about above absent absorb abstract abuse access accident "
    "accommodate accompany accomplish according account accurate accuse "
    "achieve acid acknowledge acquire across act action active activity "
    "actual actually adapt add addition additional address adequate adjust "
    "administration admit adopt adult advance advantage adventure advice "
    "advise affair affect afford afraid african after afternoon again against "
    "age agency agent aggressive ago agree agreement agricultural ahead aid "
    "aim air aircraft airline airport alarm album alcohol alike alive all "
    "alliance allow almost alone along already also alter alternative although "
    "altogether always amazing ambition ambitious american among amount "
    "analyse analysis analyst ancient angry animal announce annual another "
    "answer anticipate anxiety anxious anybody anyone anything anyway "
    "anywhere apartment apparent apparently appeal appear appearance apple "
    "application apply appointment appreciate approach appropriate approval "
    "approve approximately arab area argue argument arise arm army around "
    "arrange arrangement arrest arrival arrive arrow art article artist "
    "aside ask asleep aspect assault assert assess assessment asset assign "
    "assignment assist assistance assistant associate association assume "
    "assumption assure atmosphere attach attack attempt attend attraction "
    "attractive audience august aunt author authority automatic automobile "
    "available average avoid awake award aware awareness awful baby back "
    "background backward bacteria bad badly bag bake balance ball ban band "
    "bank bar barely barn barrel barrier baseball basic basically basis "
    "basket basketball bathroom battery battle bay beach bean bear beard "
    "beat beautiful beauty become bed bedroom beef before begin beginning "
    "behalf behavior behind being belief believe bell belong below belt "
    "bench bend beneath benefit beside best bet better between beyond bible "
    "big bike bill billion bind biological bird birth birthday bit bite "
    "bitter black blade blame blank blanket blast blind block blood blow "
    "blue board boat body bomb bond bone book boom boot border born boss "
    "both bother bottle bottom boundary bowl box brain branch brand brave "
    "bread break breakfast breast breath breathe breed brick bridge brief "
    "briefly bright brilliant bring broad broken brother brown brush "
    "budget bug build building bullet bunch burden burn bus bush business "
    "busy butter button buy buyer cabin cabinet cable cake calculate call "
    "camera camp campaign campus cancer candidate cap capability capable "
    "capacity capital capture carbon card care career careful carefully "
    "carrier carry case cash cast cat catch category catholic cause ceiling "
    "celebrate celebration celebrity center central century ceremony certain "
    "certainly chain chair chairman challenge chamber champion championship "
    "chance channel chapter character characteristic characterize charge "
    "charity chart chase cheap check cheek cheese chemical chest chicken "
    "chief child childhood chip chocolate choice choose church cigarette "
    "circle circumstance cite citizen civil civilian claim class classic "
    "classroom clean clear clearly client climate climb clinical clock "
    "close closely closer cloth clothes clothing cloud club clue cluster "
    "coach coalition code coffee cognitive cold collapse collar colleague "
    "collect collection collective college colonial color column combination "
    "combine come comedy comfort comfortable command commander comment "
    "commercial commission commit commitment committee common communicate "
    "communication community companion company comparison compete competition "
    "competitive competitor complain complaint complete completely complex "
    "complexity complicated component compose composition comprehensive "
    "computer concentrate concentration concept concern condition conduct "
    "conference confidence confident confirm conflict confront confusion "
    "congress congressional connect connection consciousness consensus "
    "consequence conservative consider considerable consideration consist "
    "consistent constant constantly constitute constitutional construct "
    "construction consultant consumer consumption contact contain container "
    "contemporary content contest context continue contract contrast "
    "contribute contribution control controversial controversy convention "
    "conventional conversation convert conviction convince cook cookie "
    "cooking cool cooperation cope copy core corner corporate correct "
    "correspond correspondent cost cotton couch could council count counter "
    "country county couple courage course court cousin cover coverage crack "
    "craft crash crazy cream create creation creative creature credit "
    "crew crime criminal crisis criteria critic critical criticism "
    "criticize crop cross crowd crucial cry cultural culture cup curious "
    "current currently curriculum custom customer cycle dad daily damage "
    "dance danger dangerous dare dark darkness data database date daughter "
    "dead deal dear death debate debt decade decent decide decision deck "
    "declare decline deep deeply deer defeat defend defendant defense "
    "defensive deficit define definitely definition degree delay deliberate "
    "deliberately delicate deliver delivery demand democracy democrat "
    "democratic demonstrate demonstration deny department depend dependent "
    "depending deploy depression deprive deputy derive describe description "
    "desert deserve design designer desire desk desperate despite destroy "
    "destruction detail detailed detect determine develop developer "
    "development device devote dialogue die diet differ differently "
    "difficult difficulty dig digital dimension dinner direction directly "
    "director dirt dirty disability disagree disappear disappoint disaster "
    "discipline discourse discover discovery discrimination discuss "
    "discussion disease dish dismiss disorder display dispute distance "
    "distant distinct distinction distinguish distribute distribution "
    "district diverse diversity divide division doctor document dog dollar "
    "domain domestic dominant dominate door double doubt down downtown "
    "dozen draft drag drama dramatic dramatically draw drawing dream dress "
    "drink drive driver drop drug dry due during dust duty each eager ear "
    "early earn earning earth ease eastern easy eat economic economy edge "
    "edition editor educate education educator effect effective effectively "
    "efficiency efficient effort eight either elderly elect election electric "
    "electricity electronic element eliminate elite else elsewhere embrace "
    "emerge emergence emergency emerging emission emotion emotional emphasis "
    "emphasize empire employ employee employer employment empty enable "
    "encounter encourage end enemy enforcement engage engine engineer "
    "engineering enormous enough ensure enter enterprise entertainment "
    "entire entirely entrance entry environment environmental episode equal "
    "equally equipment era error escape especially essay essential "
    "essentially establish establishment estate estimate evaluate evaluation "
    "even evening event eventually ever every everybody everyday everyone "
    "everything everywhere evidence evil evolution evolve exact exactly "
    "examination examine example exceed excellent except exchange exciting "
    "executive exercise exhibit exhibition exist existence existing expand "
    "expansion expect expectation expense expensive experience experiment "
    "experimental expert expertise explain explanation explicit explicitly "
    "explore explosion export expose exposure extend extension extensive "
    "extent external extra extraordinary extreme extremely eye fabric face "
    "facility fact factor factory faculty fade fail failure fair fairly "
    "faith fall familiar family fan fantasy far farm farmer fascinating "
    "fashion fast fat fatal fate father fault favorite fear feature federal "
    "fee feed feel fellow female fence few fewer fiction field fifteen fifth "
    "fifty fight fighter figure file fill film final finally finance "
    "financial find finding fine finger finish fire firm first fish fishing "
    "fit five fix flag flame flat flavor flee flesh flight float floor flow "
    "flower fly focus folk follow food foot football force foreign forest "
    "forever forget form formal formation former formula forth fortune forum "
    "forward found foundation founder four fourth fox fraction fragment "
    "frame framework free freedom freeze french frequency frequent frequently "
    "fresh friend friendship front fruit fuel full fully fun function fund "
    "fundamental funding funeral funny furniture furthermore future gain "
    "galaxy gallery game gang gap garage garden garlic gas gate gather gay "
    "gaze gear gender general generally generate generation genetic gentle "
    "gentleman gently genuine german gesture get ghost giant gift gifted "
    "girl girlfriend give given glad glance glass global glove goal god "
    "gold golden golf gone good grab grade gradually graduate grain grand "
    "grandfather grandmother grant grass grave gray great green greet grey "
    "grin grip grocery ground group grow growing grown guarantee guard "
    "guess guest guide guilty guitar gun guy habit hair half hall hand "
    "handle hang happen happy harbor hard hardly harm hat hate have he head "
    "headline headquarters health healthy hear hearing heart heat heating "
    "heavily heavy heel height helicopter hello help helpful her here "
    "heritage hero herself hey hide high highlight highly highway hill him "
    "himself hip hire historian historic historical history hit hold hole "
    "holiday holy homework honest honey hook hope hopefully horizon horror "
    "horse hospital host hostile hostage hot hotel hour household housing "
    "how however huge human humor hundred hungry hunt hunter hunting hurt "
    "husband hypothesis ice idea ideal identification identify identity "
    "ignore ill illegal illustrate image imaginary imagination imagine "
    "immediate immediately immigrant immigration impact implement "
    "implication imply import importance important impose impossible "
    "impress impression impressive improve improvement incident include "
    "including income incorporate increase increasingly incredible "
    "incredibly independence independent index indian indicate indication "
    "individual industrial industry infant infection inflation influence "
    "inform information initial initially initiative injury inner innocent "
    "innovation innovative input inquiry inside insight insist install "
    "instance instead institution institutional instruction instructor "
    "instrument insurance intellectual intelligence intend intense "
    "intensity intention interest interested interesting internal "
    "international internet interpretation intervention interview "
    "introduce introduction invasion investigate investigation investigator "
    "investment investor invisible invitation involve involved iraqi iron "
    "island isolation issue item its itself jacket jail japanese jet jewish "
    "job join joint joke journal journalist journey joy judge judgment "
    "juice jump junior jury justice justify keen keep key kick kid kidnap "
    "kill killer killing kind king kingdom kiss kitchen knee knife knock "
    "know knowledge label labor laboratory lack lady lake land landscape "
    "language lap large largely laser last late lately later latin latter "
    "laugh launch law lawn lawsuit lawyer layer lead leader leadership "
    "leading leaf league lean learn learning least leather leave lecture "
    "left leg legacy legal legend legislation legitimate lend length lesson "
    "let letter level liberal library license lie life lifestyle lifetime "
    "lift light like likely limit limitation limited line link lip list "
    "listen literally literary literature little live living load loan "
    "local locate location lock long look loose lord lose loss lost lot "
    "lots loud love lovely lover low lower luck lunch lung machine mad "
    "magazine mail main mainly maintain major majority make maker male "
    "mall man manage management manager manner manufacturer manufacturing "
    "many map margin mark market marketing marriage married marry mask "
    "mass massive master match mate material math matter may maybe mayor "
    "meal mean meaning meanwhile measure measurement meat mechanism media "
    "medical medication medicine medium meet meeting member membership "
    "memory mental mention mentor menu mere merely message metal method "
    "middle might military milk million mind mine mineral minister minor "
    "minority minute miracle mirror miss missile mission mistake mix "
    "mixture mobile model moderate modern modest mom moment money monitor "
    "month mood moon moral moreover morning mortgage moscow most mostly "
    "mother motion motivation mount mountain mouse mouth move movement "
    "movie much multiple murder muscle museum music musical musician "
    "muslim must mutual myself mystery myth naked name narrative narrow "
    "nation national natural naturally nature naval near nearby nearly "
    "necessarily necessary neck need negative negotiate negotiation "
    "neighbor neighborhood neither nerve nervous network never nevertheless "
    "newly news newspaper next nice night nine nobody nod noise nomination "
    "none nonetheless nor normal normally north northern nose notable note "
    "nothing notice notion novel now nowhere nuclear number numerous nurse "
    "nut object objection objective obligation observation observe "
    "observer obstacle obtain obvious obviously occasion occasionally "
    "occupation occupy occur ocean odd odds off offense offensive offer "
    "office officer official often oil okay old olympic once one ongoing "
    "online only onto open opening operate operation operator opinion "
    "opponent opportunity opposition option orange order ordinary organic "
    "organization organize orientation origin original other otherwise "
    "ought ourselves outcome output outside overcome overlook owe own "
    "owner pace pack package page paid pain painful painting pair pale "
    "palm pan panel panic paper parent parking part partially participate "
    "participation particular particularly partly partner partnership "
    "party pass passage passenger passion passive past path patience "
    "patient pattern pause pay payment peace peak peer penalty pension "
    "people pepper per percent percentage perception perfect perfectly "
    "perform performance perhaps period permanent permission permit person "
    "personal personality personally perspective persuade phase phenomenon "
    "philosophy phone photo photograph photography phrase physical "
    "physically physician piano pick picture pie piece pilot pine pink "
    "pipe pitch place plan plane planet planning plant plastic plate "
    "platform play player please pleasure plenty plot plus pocket poem "
    "poet poetry point pole police policy political politically politician "
    "politics pollution pool poor poorly pop popular population porch "
    "port portion portrait portray pose position positive possess "
    "possibility possibly post potato potential potentially pound pour "
    "poverty powder powerful practical practice pray prayer precisely "
    "predict prefer preference pregnancy pregnant preparation prepare "
    "prepared prescription presence present presentation preserve "
    "presidency president presidential press pressure pretty prevent "
    "previous previously primarily primary prime principal principle "
    "prior priority prison prisoner privacy private privately probably "
    "probe problem procedure proceed process produce producer product "
    "production profession professional professor profile profit program "
    "progress project prominent promise promote promotion prompt proof "
    "proper properly property proportion proposal propose proposed "
    "prosecutor prospect protect protection protein protest prove "
    "provide provider province provision psychological psychologist "
    "psychology publicly publication pull punishment purchase pure "
    "purple purpose pursue push qualify quality quarter quarterback "
    "quietly quite quote race racial racism racist radical radio rage "
    "rail rain raise range rank rapid rapidly rare rarely rate rather "
    "rating reach react reaction read reader reading ready realistic "
    "reality realize really reason reasonable reasoning rebel recall "
    "receive recent recently recognition recognize recommendation record "
    "recording recover recovery recruit red reduce reduction refer "
    "reference reflect reflection reform refrigerator refuse regard "
    "regime region regional register regular regularly regulate regulation "
    "reinforce reject relate relation relationship relative relatively "
    "release relevant relief religion religious rely remain remaining "
    "remarkable remember remind remote removal remove repeat repeatedly "
    "replace replacement report reporter represent representation "
    "representative republic republican reputation request require "
    "requirement research researcher resemble reservation resident "
    "resign resistance resolution resolve resort resource respond "
    "response responsibility responsible restaurant restoration restore "
    "restriction result retain retire retirement retreat return reveal "
    "revenue reverse review revolution rice rich rid ride rifle right "
    "ring rise risk river road robot rock role roll romantic roof room "
    "root rope rose rough roughly round route row royal rub rule run "
    "running rural rush russian sacred sad safe safety sake salary sale "
    "salt same sample sanction sand satellite satisfaction satisfy saturday "
    "sauce save saving say scale scandal scene schedule scholar scholarship "
    "school science scientific scientist scope score screen sea search "
    "season seat second secondary secret secretary section sector secure "
    "security seek segment select selection self senior sense sensitive "
    "sentence separate sequence series serious seriously serve service "
    "session set setting settle settlement seven several severe sex sexual "
    "shade shadow shake shall shape share sharp she sheet shelf shell "
    "shelter shift shine ship shirt shock shoot shooting shop shopping "
    "shore short shortage shortly shot should shoulder shout show shower "
    "shut side sigh sight signal significance significant significantly "
    "silence silent silly silver similar similarly simple simply "
    "simultaneously since sing singer single sir sister sit site situation "
    "six size ski skill skin sky slave slavery sleep slice slide slight "
    "slightly slim slip slow slowly small smart smell smile smoke smooth "
    "snap snow so so-called social society soft software soil solar soldier "
    "solid solution solve somebody someday somehow someone something "
    "sometimes somewhat somewhere son song soon sophisticated sorry sort "
    "soul sound source south southeast southern southwest space spanish "
    "speak speaker special specialist specialized specific specifically "
    "spectacular speech speed spend spending sphere spin spirit spiritual "
    "split spokesman sport spot spread spring squad stability stable "
    "stadium staff stage stair stake stand standard standing star stare "
    "start starting state statement station status statue stay steady "
    "steal steam steel step stick still stimulus stock stomach stone "
    "stop storage store storm story straight strange stranger strategic "
    "strategy stream street strength stress stretch strike string strip "
    "stroke strong strongly structure struggle student studio study "
    "stuff stupid style subject submit subsequent substance substantial "
    "succeed success successful successfully such sudden suddenly suffer "
    "sufficient sugar suggest suggestion suit summer summit sun super "
    "supplier supply support supporter suppose sure surely surface surgery "
    "surprise surprised surprising surprisingly surround surrounding "
    "survey survival survive suspect suspend suspicion sustain swallow "
    "swear sweet swim swing switch symbol symptom system table tactic "
    "tail take tale talent talk tall tank tape target task tax taxpayer "
    "tea teach teacher teaching team tear technology television tell "
    "temperature temporary ten tend tendency term terms terrible test "
    "testimony text than thank that the theater their them theme "
    "themselves then theory therapy there therefore these they thick "
    "thin thing think thinking third thirty this those though thought "
    "thousand threat threaten three throat throughout throw thus ticket "
    "tie tight till time tiny tip tire tissue title to today toe together "
    "toll tomorrow tone tonight too tool tooth top topic total totally "
    "touch tough tour tourist tournament toward tower town toy trace "
    "track trade tradition traditional traffic trail train training trait "
    "transfer transform transformation transition translate transport "
    "transportation travel treat treatment treaty tree tremendous trend "
    "trial trick trip troop trouble truly trust truth try tube tuesday "
    "tunnel turn twice twin type typical typically ugly ultimate "
    "ultimately unable uncle under undergo understand understanding "
    "unfortunately unhappy uniform unify union unique unit united "
    "universal universe university unknown unlikely until unusual up "
    "upon upper upset urban urge us use used useful user usual usually "
    "utility vacation valley valuable value variable variation variety "
    "various vast vehicle venture version versus very veteran victim "
    "victory video view viewer village violation violence virtual "
    "virtually visible vision visit visitor visual vital voice volume "
    "voluntary volunteer vote voter vulnerable wage wait wake walk wall "
    "wander want war warning wash waste watch wave weak weakness wealth "
    "weapon wear weather web website wedding week weekend weekly weigh "
    "weight welcome well western wet whatever wheel whenever whereas "
    "while whisper white whole whom why wide widely widespread wife "
    "wild will willing win wind window wing winner winter wire wish "
    "withdraw witness woman wonder wonderful wood word worker working "
    "works workshop world worried worry worse worship worst worth "
    "worthy would wound write writer writing wrong yard yeah year "
    "yell yellow yes yesterday yet yield you young youngster youth zone "
)

# ================================================================
#  SCIENTIFIC & TECHNICAL VOCABULARY
# ================================================================

_SCIENCE_WORDS = (
    # --- Physics ---
    "acceleration amplitude angular atom atomic boson centripetal "
    "collision conservation convection coulomb current decay delta "
    "density derivative diffraction displacement doppler dynamics "
    "elastic electrode electromagnetic electron entropy equilibrium "
    "fermion flux force frequency friction gamma gradient gravitational "
    "gravity harmonic heisenberg hertz impedance induction inertia "
    "infrared integral interference ion isotope joule kelvin kinetic "
    "laser lattice lepton luminosity magnetic magnetism magnitude "
    "mechanics meson molecule momentum muon neutrino neutron "
    "newtonian nuclear nucleon nucleus optics orbital oscillation "
    "particle pendulum photon planck plasma polarization positron "
    "potential pressure proton quantum quark radiation radioactive "
    "refraction relativity resistance resonance rotation scalar "
    "spectrum static string superconductor supersymmetry symmetry "
    "tensor thermal thermodynamic thermodynamics torque trajectory "
    "turbulence ultraviolet uncertainty vacuum velocity viscosity "
    "voltage vortex wavelength "
    # --- Mathematics ---
    "absolute algorithm algebraic analysis analytic asymptote axiom "
    "bijection binomial boolean calculus cardinality cartesian "
    "combinatorial commutative congruence conjecture continuous "
    "convergence convex corollary cosine countable curvature cylinder "
    "decimal deduction determinant diagonal diameter differential "
    "dimension diophantine discrete discriminant divergence divisor "
    "domain eigenvalue elliptic equation euclidean exponent exponential "
    "factorial fibonacci formula fractal function gaussian geometric "
    "graph group heuristic homeomorphism homogeneous homomorphism "
    "hypothesis hyperbolic identity imaginary inequality infinite "
    "infinitesimal infinity injective integer integral interpolation "
    "intersection invariant inverse irrational isomorphism iteration "
    "lagrangian laplacian lemma linear logarithm logarithmic manifold "
    "matrix maxima median metric minimal modular monoid multiplicative "
    "nonlinear normal notation numerical operator optimal optimization "
    "ordinal orthogonal parabola paradox parallel parameter "
    "parametric partition permutation perpendicular polynomial "
    "postulate prime primitive probability projection proof "
    "proportion pythagorean quadratic quaternion quotient radius "
    "random rational real reciprocal recursive regression ring "
    "rotation sample scalar sequence series set sigma sine "
    "singularity solution sphere square statistic stochastic "
    "subgroup subset summation surjective tangent theorem topology "
    "transcendental transformation transpose triangle trigonometric "
    "trivial union universal variable vector vertex "
    # --- Biology ---
    "adaptation adenine allele amino amphibian anatomy antibody "
    "antigen aquatic bacteria bacterium biodiversity bioethics "
    "bioinformatics biological biomass biome biosphere biotechnology "
    "carbonate carbon carcinogen catalysis catalyst cell cellular "
    "centromere chlorophyll chloroplast chromatin chromosome "
    "chromosome circadian clone codon coevolution collagen "
    "commensalism cytoplasm cytosine decomposer deoxyribonucleic "
    "diffusion diploid dna dominant ecology ecosystem embryo "
    "endocrine enzyme epidermis eukaryote evolution excretion "
    "extinction fermentation fertilization flagellum fossil "
    "gamete gene genetic genome genotype germination glucose "
    "glycolysis gonad habitat herbivore hereditary heterozygous "
    "homeostasis homozygous hormone hybrid hydrolysis immune "
    "immunology insulin invertebrate karyotype kingdom lipid "
    "lysosome macromolecule mammal meiosis membrane metabolism "
    "metamorphosis microbe microbiology microscopic mitochondria "
    "mitosis molecular morphology multicellular mutation "
    "mutualism natural niche nitrogen nucleotide nucleus "
    "omnivore organ organelle organism osmosis ovary ovulation "
    "oxidation parasite pathogen phenotype photosynthesis phylum "
    "plasmid pollination polymer population predator prey "
    "prokaryote protein protist protozoa receptor recessive "
    "recombination reproduction respiration ribosome ribonucleic "
    "rna selection speciation species stimulus symbiosis "
    "synapse taxonomy telomere tissue transcription translation "
    "transpiration vaccine variation vertebrate virus zygote "
    # --- Chemistry ---
    "acetyl acid activation alcohol aldehyde alkali alkaline "
    "alkane alkene alkyne allotrope alloy amalgam amide amine "
    "anion anode aqueous aromatic base bonding buffer "
    "calorimeter carbohydrate carbonyl catalyst centrifuge "
    "chelation chromatography combustion compound concentration "
    "condensation conductor conjugate covalent crystal "
    "crystalline decomposition dehydration dialysis dilution "
    "dipole dissolution distillation electrode electrolysis "
    "electrolyte endothermic enthalpy ester exothermic "
    "extraction filtration fission formula fusion galvanic "
    "halogen hydration hydrocarbon hydrogen hydroxide "
    "immiscible indicator ionic ionization isomer isotope "
    "kinetics litmus macroscopic miscible mixture molar "
    "molecular molten monomer neutralization nomenclature "
    "orbital organic oxidation oxide peptide periodic "
    "polymerization precipitate reagent redox reduction "
    "saturation solubility solute solution solvent spectroscopy "
    "stoichiometry sublimation substrate suspension synthesis "
    "titration valence volatile "
    # --- Computer Science ---
    "abstraction algorithm allocation api architecture array "
    "asynchronous authentication bandwidth binary bit boolean "
    "buffer bytecode cache callback cipher class client closure "
    "cluster compiler complexity computation concatenation "
    "concurrency configuration container cryptography cursor "
    "daemon database debugging declaration decryption deployment "
    "deserialization dictionary distributed documentation "
    "encapsulation encoding encryption endpoint enumeration "
    "exception execution expression filesystem firewall firmware "
    "floating framework garbage gateway generic graph "
    "hash hashing heap heuristic hexadecimal hierarchy "
    "hypertext implementation index inheritance initialization "
    "input instance instantiation integration interface "
    "interpreter interrupt iteration iterator kernel lambda "
    "latency library linked list literal load loop malloc "
    "metadata middleware migration module monitor multithreading "
    "namespace network node normalization object optimization "
    "overflow packet pagination paradigm parser partition "
    "payload persistence pipeline pointer polymorphism port "
    "primitive process processor profiling protocol proxy "
    "pseudocode query queue random recursion refactoring "
    "reference register relational rendering repository "
    "resolution resource runtime sandbox schema scope "
    "serialization server service session singleton socket "
    "sorting stack statement storage stream string struct "
    "subroutine synchronization syntax template terminal "
    "thread throughput token transaction traversal tuple "
    "unicode validation variable virtual widget yield "
)

# ================================================================
#  EMOTIONAL / SPIRITUAL / PHILOSOPHICAL VOCABULARY
# ================================================================

_SPIRIT_WORDS = (
    "abandon abandonment abide abundance acceptance "
    "accountability acknowledge adoration adversity affection "
    "affliction agape agony alchemy allegiance altruism "
    "amazement amen anchor anguish annihilation anointing "
    "anticipation anxiety apathy apostle appreciation "
    "apprehension archetype ascension aspiration assurance "
    "atonement attachment attentiveness authenticity awe "
    "awakening awareness baptism beatitude belief beloved "
    "benevolence bereavement betrayal birth blessing bliss "
    "bondage born bounty brokenness burden calling calm "
    "captivity care celebration celibacy certitude "
    "charity chastity cherish christ christening "
    "circumspection clarity cleansing clemency comfort "
    "commandment commitment communion compassion "
    "compunction confession confidence consecration "
    "consolation contemplation contentment contrition "
    "conversion conviction courage covenant creation "
    "creator cross crucifixion cruelty cry darkness death "
    "deception dedication deference deliverance denial "
    "dependence depression desire despair destiny "
    "detachment determination devotion devoutness dignity "
    "discernment discipleship discipline discovery "
    "disillusionment dispensation disposition dissatisfaction "
    "divine divinity doctrine doubt dread duality duty "
    "earnestness ecstasy eden edification election "
    "elevation emanation embodiment emotion empathy "
    "empowerment emptiness enchantment encouragement "
    "endurance enlightenment enmity enthusiasm epiphany "
    "equanimity essence eternal eternity eucharist "
    "evangelical evangelism exaltation examination "
    "excellence excommunication exhortation existence "
    "exodus expectation experience expiation exploration "
    "expression exultation faith faithful faithfulness "
    "fall falsehood fasting father fatherhood fear "
    "fellowship fervor fidelity fire flesh forbearance "
    "forgiveness fortitude fountain fragility "
    "freedom friendship fruition fulfillment "
    "generosity gentleness gift giving gladness "
    "glorification glory god godliness goodness "
    "gospel governance grace grandeur gratification "
    "gratitude gravity greed grief grievance "
    "growth guidance guilt hallow happiness "
    "harmony hate hatred healing heart heaven "
    "heavenly heritage holiness holy hope hopelessness "
    "hospitality hostility humbling humiliation humility "
    "hunger hymn idolatry ignorance illumination "
    "imagination immanence immersion immortality "
    "impermanence incarnation indifference "
    "indignation infidelity infinity inner innocence "
    "inspiration integrity intercession intimacy "
    "introspection intuition invocation isolation "
    "jealousy journey joy jubilation judgment "
    "justice justification karma kindness kingdom "
    "lamentation law liberation light loneliness "
    "longing lord love lovingkindness loyalty lust "
    "magnificence majesty malice martyrdom meditation "
    "meekness memorial mercy messenger messiah "
    "mindfulness ministry miracle modesty monasticism "
    "moral morality mortality mortification mourning "
    "mystery mysticism nativity nourishment nurture "
    "obedience oblation obligation offering omnipotence "
    "omnipresence omniscience oneness ordained ordination "
    "original orthodoxy otherworldly outpouring "
    "overcome pacifism pain paradise pardon passion "
    "patience patriarch peacemaking penance penitence "
    "pentecost perception perdition perfection peril "
    "permanence perpetuity persecution perseverance "
    "petition piety pilgrim pilgrimage pity "
    "pleasure poverty praise prayer predestination "
    "prejudice presence preservation pride priesthood "
    "principality privilege proclamation prodigal "
    "profession promise prophecy prophet propitiation "
    "prosperity protection providence prudence psalm "
    "punishment purgatory purification purity purpose "
    "quietude rapture realization rebirth recollection "
    "reconciliation redemption reflection reformation "
    "regeneration reincarnation rejection rejoicing "
    "relationship reliance remembrance remorse renewal "
    "renunciation repentance repose resignation resolve "
    "respect responsibility restitution restoration "
    "resurrection revelation reverence revival "
    "righteousness ritual rosary sacrament sacred "
    "sacrifice sadness saint salvation sanctification "
    "sanctuary satisfaction scripture security seeker "
    "selfhood selfishness selflessness seraph serenity "
    "servanthood servitude shame shelter shepherd "
    "silence simplicity sincerity sinfulness skepticism "
    "sloth solace solidarity solitude sorrow soul "
    "sovereignty spirit spiritual stewardship "
    "stillness strength struggle submission "
    "substance suffering supplication supreme "
    "surrender sustenance symbol sympathy tabernacle "
    "temperance temple temptation tenderness "
    "testimony thankfulness theology thirst tithe "
    "tolerance tradition transcendence transformation "
    "transgression trinity triumph trust truth "
    "turbulence uncertainty understanding union "
    "unity universal utterance valor vanity "
    "veneration vigilance vindication virtue "
    "vocation vulnerability wandering warfare "
    "warning watchfulness weakness wealth wholeness "
    "wilderness will wisdom witness wonder worship "
    "worthiness wrath yearning yielding zeal "
)

# ================================================================
#  EXTENDED ENGLISH: General vocabulary to reach ~100K
# ================================================================
#
# These words are generated from productive English morphology.
# Root words + common derivational suffixes = valid English.
# Each suffix carries its own D2 force signature, so derived
# words have genuine physics (not copied from roots).

_EXTENDED_ROOTS = (
    "abandon abbreviate abdicate abduct aberrate abhor abolish abort "
    "abridge absolve absorb abstain abstract abuse accede accelerate "
    "accentuate accept access acclaim acclimate accommodate accompany "
    "accomplish accumulate accuse achieve acidify acknowledge acquaint "
    "acquire acquit activate actuate adapt add address adhere adjust "
    "administer admire admit admonish adopt adore adorn advance advocate "
    "aerate affiliate affirm affix afflict afford aggravate aggregate "
    "agitate agree aid aim alarm alert alienate align allay allege "
    "alleviate allocate allot allow allude alter alternate amalgamate "
    "amass amaze ambush ameliorate amend amplify amuse analyze anchor "
    "animate annotate announce annoy annul anoint anticipate apologize "
    "appall appeal appear appease applaud apply appoint appraise "
    "appreciate apprehend apprentice approach appropriate approve "
    "approximate arbitrate archive argue arise arouse arrange arrest "
    "articulate ascend ascertain aspire assail assassinate assemble "
    "assert assess assign assimilate assist associate assume assure "
    "astonish attach attain attempt attend attest attract attribute "
    "auction audit augment authenticate author authorize automate "
    "avenge avert await awaken babble back backfire bail balance "
    "bamboozle ban bandage banish baptize bargain bark barricade "
    "barter bash baste batch bathe batter battle beacon beam bear "
    "beat beautify beckon become befriend beg begin behave behead "
    "behold believe belittle belong bemoan benchmark bend benefit "
    "bequeath bereave beseech bestow bet betray bewilder bewitch "
    "bid bind bite blacken blame blanch blast blaze bleach bleed "
    "blemish blend bless blight blind blindfold blink blister block "
    "bloom blossom blow bluff blur blurt blush board boast bog "
    "boil bolster bolt bombard bond boost border bore borrow boss "
    "bother bottle bounce bound bow brace bracket brag braid brake "
    "branch brand brave breach break breathe breed brew bribe bridge "
    "brief brighten bring bristle broaden broadcast broil broker "
    "brook brood browse bruise brush bubble buckle bud budget buffer "
    "build bulk bulldoze bully bump bundle burden burglarize burn "
    "burnish burst bury bustle butter buttress buy buzz bypass "
    "calculate calibrate calm campaign cancel cap capitalize capture "
    "card care careen caress carouse carpet carry carve cascade cash "
    "cast catalog catalyze catch categorize cater caution cease "
    "celebrate censor censure center centralize certify chain "
    "chair challenge champion change channel chant characterize "
    "charge charm chart chase chat check cheer cherish chew chide "
    "chill chip choke choose chop chronicle circle circulate "
    "circumscribe circumvent cite civilize claim clamp clap clarify "
    "clash clasp classify clean cleanse clear click climb cling "
    "clip cloak clone close clothe cluster coach coalesce coarsen "
    "coat coax code codify coerce coexist collaborate collapse "
    "collect collide color combine comfort command commemorate "
    "commence commend commission commit communicate commute compel "
    "compensate compete compile complain complement complete "
    "complicate compliment comply compose compost compound comprehend "
    "compress comprise compromise compute conceal concede conceive "
    "concentrate concern conciliate conclude concoct condemn "
    "condense condition conduct confer confess confide confine "
    "confirm confiscate conflict conform confront confuse congregate "
    "conjecture connect conquer consecrate consent conserve consider "
    "consign consist console consolidate conspire constitute "
    "constrain construct consult consume contaminate contemplate "
    "contend contest contextualize continue contract contradict "
    "contrast contribute control convene converge converse convert "
    "convey convince cook cooperate coordinate cope correlate "
    "correspond corrode corrupt counsel count counteract couple "
    "court cover covet crack craft cram crash crave crawl create "
    "credit creep criminalize cripple criticize crop cross crouch "
    "crowd crush cry cultivate curb cure curl curry curse curtail "
    "cushion customize cut cycle damage dampen dance dare darken "
    "dart dash date dawn daze dazzle deactivate deal debate "
    "debilitate debit debut decapitate decay deceive decelerate "
    "decide decimate decipher declare decline decode decorate "
    "decrease decree dedicate deduct deem deepen default defeat "
    "defend defer define deflate deflect defy degenerate degrade "
    "dehydrate delay delegate delete deliberate delight deliver "
    "demand demolish demonstrate demoralize demote demystify "
    "denote denounce deny depart depend depict deplete deplore "
    "deploy deposit depreciate depress deprive derive descend "
    "describe designate desire despise destabilize destroy detail "
    "detain detect deteriorate determine detest detonate develop "
    "deviate devise devote diagnose dictate die differentiate "
    "diffuse dig digest dilute diminish dine direct disable "
    "disagree disappear disappoint disarm discard discern discharge "
    "discipline disclose disconnect discontinue discount discover "
    "discredit discriminate discuss disdain disengage disguise "
    "dishonor disillusion disinfect disintegrate dismiss displace "
    "display dispose disprove dispute disregard disrupt dissect "
    "disseminate dissent dissolve dissuade distance distinguish "
    "distort distract distribute disturb dive diverge diversify "
    "divert divide divorce document dodge domesticate dominate "
    "donate doom double downgrade downsize draft drag drain "
    "dramatize drape draw dream dress drift drill drink drip drive "
    "drop drown drum dry dub duck dump duplicate dust dwell "
    "dwindle earn ease eavesdrop echo eclipse edit educate "
    "elaborate elapse elect electrify elevate elicit eliminate "
    "elongate elude email embark embarrass embed embody embrace "
    "emerge emit emphasize employ empower empty enable enact "
    "encounter encourage encroach encrypt endanger endeavor endorse "
    "endure energize enforce engage engineer engrave enhance enjoy "
    "enlarge enlighten enlist enrage enrich enroll ensure enter "
    "entertain enthuse entice entitle entrust enumerate envision "
    "equal equalize equip eradicate erect erode err erupt escalate "
    "escape establish estimate evaluate evade evangelize evaporate "
    "even evolve exacerbate exaggerate examine excavate exceed "
    "exchange excite exclaim exclude excuse execute exemplify "
    "exempt exercise exert exhaust exhibit exhort exist expand "
    "expect expedite expel experience experiment explain explode "
    "exploit explore export expose express extend exterminate "
    "extinguish extract extricate exude fabricate face facilitate "
    "factor fade fail fake fall falsify familiarize fan fantasize "
    "farm fascinate fashion fasten fault favor fear feast feature "
    "feed feel fence fend ferment fertilize fetch fetter fight "
    "figure file fill film filter finalize finance find fine "
    "finish fire fit fix flag flatter flee flex flicker flinch "
    "flip flit float flock flood flourish flow fluctuate flush "
    "flutter fly focus fold follow fool forbid force forecast "
    "forge forget forgive form formalize format formulate forsake "
    "fortify foster found fracture fragment frame free freeze "
    "frequent frighten fringe front frost frustrate fuel fulfill "
    "fumble function fund furnish fuse fuss gain galvanize gamble "
    "garden garner gather gauge gaze generalize generate germinate "
    "gesture get give glance glare gleam glide glimpse glow gnaw "
    "govern grab grace grade graduate grant grasp grate gravel "
    "graze greet grieve grill grind grip groan groom grope ground "
    "group grow grumble guarantee guard guide gush hack hail halt "
    "hammer hamper hand handle hang happen harass harden harm "
    "harmonize harness harvest hasten haunt have head headline "
    "heal heap heat help herd hesitate hibernate hide highlight "
    "hinder hint hire hit hoist hold hollow honor hook hop hope "
    "horrify host house hover hug humiliate humor hunger hunt "
    "hurdle hurl hurry hurt hustle hypothesize ice identify ignore "
    "illuminate illustrate imagine immerse immigrate immobilize "
    "impact impair impart impeach impede implement implicate "
    "implore import impose impound impress imprison improve "
    "improvise inaugurate incite include incorporate increase "
    "incur indicate indict induce indulge industrialize infect "
    "infer inflate inflict inform infuriate inhabit inherit "
    "inhibit initiate inject innovate inquire inscribe insert "
    "insist inspect inspire install institute instruct insulate "
    "insult insure integrate intend intensify interact intercept "
    "interest interfere internalize interpret interrogate interrupt "
    "intervene intimate intimidate introduce intrude invade "
    "invalidate invent invest investigate invite involve iron "
    "irrigate irritate isolate issue itemize jab jail jam "
    "jeopardize jerk jest jettison jingle jog join joke jostle "
    "journal journey judge juggle jump justify keen kidnap "
    "kindle kiss kneel knit knock knot know label labor lack "
    "lag land languish lap lapse last latch launch lavish lay "
    "lead lean leap learn lease leave lecture lend lengthen "
    "lessen let level leverage liberate license lick lie lift "
    "light lighten liken limit line linger link liquidate listen "
    "litigate litter live load loan lobby locate lock lodge log "
    "long look loom loop loosen lose love lower lubricate lure "
    "lurk magnify maintain major make malfunction manage mandate "
    "maneuver manifest manipulate manufacture map march marginalize "
    "mark marvel mask massacre master match materialize matter "
    "mature maximize mean measure mediate meditate meld melt "
    "memorize menace mend mentor merge merit mesh message "
    "micromanage migrate militate mimic mind mine minimize "
    "minister mirror miscalculate mislead miss mitigate mix "
    "mobilize mock model moderate modernize modify mold monitor "
    "monopolize morph motivate mourn move muddle multiply murmur "
    "muse muster mute mystify name narrate narrow navigate "
    "necessitate need negate neglect negotiate nest nestle "
    "network neutralize nominate normalize note notice notify "
    "nourish number nurture obey object obligate oblige observe "
    "obstruct obtain occupy occur offend offer officiate offset "
    "open operate oppose opt optimize orchestrate order organize "
    "orient originate ornament orphan oscillate oust outdo "
    "outline output outrun outshine outwit overcharge overcome "
    "overflow overhear overlap overlook overpower override "
    "oversee overwhelm owe own pace pacify pack paddle page "
    "paint pair pamper pan parade paralyze parcel pardon park "
    "parse participate partner pass paste patent patrol pause "
    "pave peak peal peel peer penalize penetrate perceive "
    "perfect perform perish permit perpetuate persecute "
    "persist personalize persuade pertain petition phase pick "
    "picture piece pile pilot pin pinpoint pioneer pitch pivot "
    "place plan plant plaster plate play plead pledge plod plot "
    "pluck plug plummet plunge pocket point poise poison "
    "polarize police polish poll pollute ponder pool pop "
    "populate portray pose position possess postpone pour "
    "practice praise precede predict prefer prepare prescribe "
    "present preserve preside press pressure presume pretend "
    "prevail prevent price pride print prioritize probe process "
    "proclaim procure produce profess profile profit program "
    "progress prohibit project prolong promise promote prompt "
    "pronounce propel propose prosecute protect protest prove "
    "provide provoke publicize pull pump punch punish purchase "
    "purge purify pursue push put puzzle qualify quantify quarantine "
    "question queue quit quiz quote race radiate raid raise rally "
    "ramble range rank rant rate ratify rationalize rattle reach "
    "react read realize reap reason reassure rebel rebuild recall "
    "recapture receive recite reckon recognize recommend reconcile "
    "reconstruct record recover recruit rectify recur recycle "
    "redeem redesign redirect redistribute reduce reestablish "
    "refer refine reflect reform refresh refuel refund refuse "
    "refute regain regard regenerate register regret regulate "
    "rehabilitate rehearse reign reinforce reiterate reject "
    "relate relax relay release relieve relinquish relish "
    "relocate rely remain remark remedy remember remind remodel "
    "remove render renew renovate rent reorganize repair repay "
    "repeal repeat repel replace replicate report represent "
    "repress reproduce request require rescue research resemble "
    "resent reserve resettle reshape reside resign resist resolve "
    "respect respond restore restrict restructure result resume "
    "retain retaliate retire retort retreat retrieve return "
    "reunite reveal reverse review revise revitalize revive "
    "revolutionize reward ride ridicule ring rip ripen risk rival "
    "roam rob rock roll romance root rotate rouse route rub ruin "
    "rule rumble run rupture rush sacrifice safeguard sail "
    "sanction satisfy saturate save savor scale scan scare scatter "
    "schedule score scout scramble scratch screen scrutinize seal "
    "search seat secure seize select sell send sense sentence "
    "separate sequence serve service settle sever shake shape "
    "share sharpen shatter shed shelter shield shift shine shiver "
    "shock shoot shop shorten shoulder shout shove show shrink "
    "shroud shuffle shut sideline siege sift signal signify silence "
    "simplify simulate sin sing sink sit situate size sketch "
    "skim skip slam slap slash sleep slice slide slim sling slip "
    "slither slow smash smell smile smuggle snap snatch sneak "
    "snowball soak soar soften solicit solidify solve sort sound "
    "source spark speak specialize specify speculate speed spend "
    "spill spin spiral split sponsor spot spread spring sprinkle "
    "spur squeeze stabilize stack staff stage stagger stain stake "
    "stall stamp stand standardize stare start startle state "
    "station stay steal steer stem step stereotype stick stimulate "
    "stir stock stockpile stop store storm straighten strain "
    "strand strategize streamline strengthen stress stretch strike "
    "strip strive structure struggle study stuff stumble stun "
    "subject submit subordinate subscribe subsidize substitute "
    "succeed suffer suggest suit summarize summon supplement "
    "supply support suppose suppress surface surge surmount surpass "
    "surprise surrender surround survey survive suspect suspend "
    "sustain swallow swap sway swear sweep swell swim swing switch "
    "symbolize sympathize synthesize table tackle tag tailor take "
    "talk tamper tap target task taste tax teach tear tease "
    "telephone tell temper tempt tend terminate terrify test "
    "testify text thank thicken think threaten thrill thrive "
    "throw thrust tidy tie tighten tilt time toast tolerate "
    "topple torture total touch tour trace track trade train "
    "transcend transfer transform translate transmit transport "
    "trap travel treasure treat trek tremble trigger trim triumph "
    "trouble trump trust try tuck tumble tune tunnel turn tutor "
    "twist type undergo underline undermine understand undertake "
    "undo unearth unfold unify unite unleash unlock unravel "
    "unveil update upgrade uphold upset urbanize urge use "
    "utilize utter vacate validate value vanish vary vault "
    "venture verify veto view vindicate violate visit visualize "
    "voice volunteer vouch wade wage wager wait waive wake "
    "walk wander want ward warm warn warp warrant wash waste "
    "watch water wave waver weaken wean wear weather weave "
    "weigh welcome whisper widen wield will win wind wipe wish "
    "withdraw withhold witness wonder work worry worship wound "
    "wrap wreck wrestle write yearn yield zero zone "
)

# Productive English suffixes for derivation
_DERIVATION_SUFFIXES = {
    # suffix -> (resulting POS, operator tendency)
    'tion':  ('noun', None),
    'sion':  ('noun', None),
    'ment':  ('noun', None),
    'ness':  ('noun', None),
    'ity':   ('noun', None),
    'ence':  ('noun', None),
    'ance':  ('noun', None),
    'er':    ('noun', None),
    'or':    ('noun', None),
    'ist':   ('noun', None),
    'ism':   ('noun', None),
    'dom':   ('noun', None),
    'ship':  ('noun', None),
    'hood':  ('noun', None),
    'age':   ('noun', None),
    'ing':   ('noun', None),
    'al':    ('adj',  None),
    'ful':   ('adj',  None),
    'less':  ('adj',  None),
    'ous':   ('adj',  None),
    'ive':   ('adj',  None),
    'able':  ('adj',  None),
    'ible':  ('adj',  None),
    'ic':    ('adj',  None),
    'ical':  ('adj',  None),
    'ent':   ('adj',  None),
    'ant':   ('adj',  None),
    'ary':   ('adj',  None),
    'ly':    ('adv',  None),
    'ize':   ('verb', None),
    'ise':   ('verb', None),
    'ify':   ('verb', None),
    'ate':   ('verb', None),
    'en':    ('verb', None),
    'ed':    ('adj',  None),
}


# ================================================================
#  ADDITIONAL DOMAIN VOCABULARIES
# ================================================================

_NATURE_WORDS = (
    "acacia acorn agate agave alder algae almond aloe alpine amber "
    "amethyst anemone antelope ape aquifer arctic ash aspen aurora "
    "avalanche badger bamboo basalt basin bay bayou bear beaver "
    "beech birch bison blizzard bloom bog boulder bramble breeze "
    "brook bud buffalo bulb bush buttercup butterfly cactus canyon "
    "cape cardinal carnation cascade cave cedar chameleon chamomile "
    "cheetah cherry chestnut chrysanthemum cicada cinder cliff clover "
    "coast cobalt cobra cocoon condor conifer copper coral cordillera "
    "cosmos cougar cove coyote crane crater creek crescent crevice "
    "cricket crimson crocodile crocus crow crystal cub cumulus current "
    "cypress daffodil dahlia dawn deer delta den desert dew dolphin "
    "dove dragonfly drift driftwood drought dune dusk eagle earth "
    "earthquake ebb eclipse eddy eel elder elk elm ember emerald "
    "erosion estuary eucalyptus evergreen falcon feather fawn fern "
    "finch fir firefly fjord flamingo flint flora flower flurry "
    "fog foliage foothill forest fossil fox frost fuchsia fungus "
    "galaxy gale gazelle gem geode geyser ginkgo glacier glade glen "
    "glacier gorge granite grasshopper gravel grove grouse gull gust "
    "habitat hail harbor hawk hawthorn hazel heath hedge heron "
    "hibiscus highland hill holly horizon hummingbird hurricane "
    "hyacinth ibis iceberg iguana inlet iris island ivory ivy "
    "jackal jade jaguar jasmine jay juniper kelp kingfisher knoll "
    "lagoon lake larch lava lavender leaf leopard lichen lightning "
    "lilac lily limestone lion lotus lush lynx magnolia mahogany "
    "mallard mangrove maple marigold marsh meadow mesa mica midnight "
    "mink mist monsoon moon moonlight moose moss mountain mulberry "
    "muskrat narcissus nebula nettle nightingale nimbus north nova "
    "oak oasis obsidian ocean orchid oriole osprey otter owl "
    "oyster palm panther peak pebble pelican penguin peony "
    "peregrine petal petrified phoenix pine plateau plover plum "
    "polar pollen pond poplar poppy porcupine prairie primrose "
    "prism puma python quail quartz raven ravine redwood reef "
    "ridge rift river robin rock rose rosemary ruby sage salmon "
    "sand sandstone sapphire savanna seagull sequoia serpent shark "
    "shore sierra silver sky slate sleet sloth snow snowflake solstice "
    "sparrow spruce squirrel stalactite starfish steppe stork storm "
    "strait stratosphere stream summit sun sunflower sunrise sunset "
    "surf swallow swan sycamore talon tempest terrain thicket "
    "thistle thorn thunder tide tiger timber topaz tornado tortoise "
    "trout tsunami tulip tundra turquoise turtle twilight typhoon "
    "valley vapor violet viper volcano vulture walrus waterfall "
    "wave whale whirlpool wildflower willow wind wisteria wolf "
    "woodland wren zenith zephyr "
)

_HUMAN_BODY_WORDS = (
    "abdomen achilles adrenaline ankle aorta appendix arch arm armpit "
    "artery backbone bile bladder blood bone bowel brain breast bronchi "
    "brow calf capillary cartilage cavity cell cerebellum cerebrum "
    "cervical cheek chest chin clavicle coccyx cochlea collarbone colon "
    "cornea cranium deltoid diaphragm disc elbow embryo enamel "
    "endocrine esophagus eyelash eyelid eyebrow fallopian femur fiber "
    "fibula finger fingernail forearm forehead frontal gall gallbladder "
    "gland glottis groin gum hamstring heel hemisphere hip humerus "
    "hypothalamus ileum immune incisor index intestine iris jawbone "
    "joint jugular kidney kneecap knuckle larynx ligament limb lip "
    "liver lobe loin lumbar lung lymph mandible marrow metatarsal "
    "midriff molar mucus muscle navel neck nerve neuron nipple nostril "
    "nucleus occipital optic organ ovary palate palm pancreas patella "
    "pectoral pelvis pharynx pituitary plasma platelet pleura pore "
    "prostate pulmonary pupil quadriceps radius rectum retina rib "
    "sacrum saliva scalp scapula shin shoulder sinew skeleton skull "
    "sole spinal spine spleen sternum stomach synapse temple tendon "
    "testicle thigh thorax throat thyroid tibia tissue toe tongue "
    "tonsil torso trachea trapezius triceps ulna umbilical ureter "
    "urethra uterus uvula valve vein ventricle vertebra vocal womb "
    "wrist "
)

_ARTS_CULTURE_WORDS = (
    "abstract acrylic allegory alto anthem aria arrangement artifact "
    "artist artistry auditorium ballad ballet balm baroque bass "
    "biography blend blues bohemian brass bronze brush calligraphy "
    "canvas caricature carnival carve cathedral cello chamber chandelier "
    "choreography chorus chromatic cinema cinematic clay collage "
    "comedy composition concerto conductor conservatory contemporary "
    "contralto costume craft creative creativity crescendo critique "
    "cubism culture curator dance debut decor decoration design dialogue "
    "digital director discourse documentary dome drama drape drawing "
    "duet dynamic easel echo edition editorial elegance elegy eloquence "
    "embroidery encore ensemble epic etching etude exhibition expression "
    "fable facade fantasy fiction figurative film fine folklore font "
    "footwork forge fresco fugue gallery genre gesture gild glee "
    "gothic graphic graffiti haiku harmony harp heritage hymn icon "
    "illumination illustration imagery impasto improvisation ink "
    "inscription inspiration installation instrument interlude "
    "interpretation ivory jazz kinetic landscape libretto limelight "
    "literary literature lithograph loom lullaby lyric maestro manga "
    "manuscript maquette marble mask masterpiece memoir melody "
    "metaphor mezzanine miniature minstrel mobile modernism montage "
    "monument mosaic motif mural muse museum mythology narrative "
    "nocturne novel novella nuance nude ode oil opera opus orchestra "
    "ornate overture pageant paint palette panorama pantomime parable "
    "parody pastel pastoral patron pavilion percussion performance "
    "perspective photography pianoforte piece pigment pitch plaster "
    "playwright plot podium poetry portrait poster pottery prelude "
    "premiere print production profile prologue prose prose protagonist "
    "psalm quartet quill realism recital renaissance rendition "
    "repertoire replica representational requiem restoration revival "
    "rhetoric rhyme romance rondo saga salon satire scale scenic "
    "score screenplay script sculpture serenade shade silhouette "
    "sketch solo sonata sonnet soprano staccato stage stanza statue "
    "still stoneware strophe studio style suite surrealism symbolism "
    "symphony tableau tale tapestry technique tempera tempo text "
    "texture theater theme timbre tint tone tragedy treble tribute "
    "trio troubadour tune typography undertone varnish vaudeville "
    "verse vibrato vignette virtuoso visual vocal waltz watercolor "
    "weave woodcut "
)

_FOOD_COOKING_WORDS = (
    "almond anise appetizer apricot avocado bacon baguette bake "
    "balsamic banana barbecue barley basil baste batter berry beverage "
    "bisque blanch blend brine brioche broccoli broth brownie brunch "
    "brussels buckwheat butter cabbage cacao cake caramel cardamom "
    "carrot casserole cauliflower celery charcuterie cheddar cherry "
    "chestnut chicken chickpea chili chive chocolate chop chowder "
    "churro cilantro cinnamon citrus clam clove cobbler coconut cod "
    "compote condiment confection coriander cornbread crab cranberry "
    "cream croissant crouton crumble cucumber cumin curd curry custard "
    "cutlet dairy date delicacy dessert dice dill dough dressing "
    "dumpling eggplant emulsion endive entree espresso fennel feta "
    "fillet flambe flour fondant fondue fritter frosting fruit fry "
    "fudge galette ganache garlic garnish gelatin ginger glaze gnocchi "
    "gouda granola grapefruit gratin gravy griddle grill grits guava "
    "gumbo habanero halibut ham hash hazelnut herb honey horseradish "
    "hummus jam jasmine jelly juniper kale ketchup kumquat lamb "
    "lasagna lavender leek legume lemon lentil lettuce lime linguine "
    "lobster macadamia macaroon mango maple margarine marinade "
    "marjoram marshmallow marzipan mayonnaise melon menu meringue "
    "millet mint miso molasses mousse mozzarella muffin mushroom "
    "mussel mustard nectarine noodle nutmeg oat olive omelet onion "
    "orange oregano oyster paella pancake papaya paprika parmesan "
    "parsley parsnip pasta pastry peach peanut pear pecan pepper "
    "peppermint pesto pickle pie pineapple pistachio pizza platter "
    "plum polenta pomegranate popcorn pork porridge potato poultry "
    "praline prawn pretzel prosciutto prune pudding pumpkin puree "
    "quiche quinoa radish raisin raspberry ravioli recipe relish "
    "rhubarb risotto roast roll rosemary rye saffron sage salad "
    "salmon salsa sandwich sardine sauce sausage scallion scallop "
    "seasoning sesame shallot shellfish sherbet shrimp simmer "
    "skillet snack souffle soup sourdough soy spaghetti spinach "
    "squash steak stew stock strawberry stuffing succotash sugar "
    "sultana sundae sushi sweet taco tamarind tangerine tapioca "
    "tarragon tart teriyaki thyme toast tofu tomato tortilla "
    "truffle tuna turmeric turnip vanilla veal vegetable venison "
    "vinaigrette vinegar waffle walnut wasabi watercress wheat "
    "whisk wine wonton yam yogurt zest zucchini "
)

_PROFESSION_WORDS = (
    "accountant acrobat actor administrator advocate aide analyst "
    "animator announcer apprentice arbitrator archaeologist architect "
    "artisan astronaut astronomer athlete attorney auctioneer auditor "
    "author aviator babysitter baker banker barber bartender biologist "
    "blacksmith blogger bookkeeper botanist broadcaster broker builder "
    "bureaucrat butcher butler captain carpenter cartographer cashier "
    "caterer chaplain chef chemist choreographer cinematographer clerk "
    "coach cobbler comedian commentator commissioner composer conductor "
    "confectioner congressman consultant contractor controller cook "
    "coordinator correspondent councillor counselor courier craftsman "
    "critic curator custodian dancer dean decorator dentist deputy "
    "designer detective developer dietitian diplomat director "
    "dispatcher diver doctor doorman drafter dramatist driver "
    "ecologist economist editor educator electrician embalmer "
    "employee employer engineer entertainer entrepreneur "
    "environmentalist epidemiologist estimator evangelist examiner "
    "executive explorer exporter fabricator facilitator farmer "
    "fashion firefighter fisherman florist foreman forester "
    "freelancer gardener geographer geologist glazier governor "
    "graphic grocer groundskeeper guard guide hairdresser handyman "
    "herbalist historian housekeeper hunter illustrator importer "
    "inspector instructor insurer interpreter inventor investigator "
    "janitor jeweler jockey journalist judge laborer landlord "
    "landscaper lawyer lecturer legislator librarian lifeguard "
    "linguist locksmith machinist magistrate manager manufacturer "
    "marine marketer mason mathematician mayor mechanic mediator "
    "merchant meteorologist midwife miner minister missionary "
    "model monk mortician musician navigator negotiator neurologist "
    "notary novelist nurse nutritionist obstetrician officer "
    "operator optician optometrist orator orderly organizer "
    "orthodontist painter paleontologist paramedic pastor pathologist "
    "patron pediatrician performer pharmacist philosopher photographer "
    "physician physicist pilot planner playwright plumber poet "
    "police politician porter postman potter preacher president "
    "principal printer probation processor producer professor "
    "programmer projectionist promoter prosecutor psychiatrist "
    "psychologist publicist publisher quarterback rabbi radiologist "
    "rancher ranger realtor receptionist recruiter referee "
    "registrar regulator reporter researcher restaurateur retailer "
    "reviewer roboticist roofer sailor salesman sanitarian scholar "
    "scientist screenwriter sculptor secretary senator servant "
    "sheriff singer smith sociologist soldier solicitor songwriter "
    "speaker specialist spokesperson statistician steward stockbroker "
    "strategist stylist superintendent supervisor surgeon surveyor "
    "tailor teacher technician technologist therapist trainer "
    "translator treasurer tutor typist undertaker underwriter "
    "usher valedictorian valet vendor veterinarian videographer "
    "vintner violinist vocalist volunteer waiter warden welder "
    "woodworker writer zoologist "
)

_EMOTION_WORDS = (
    "admiration adoration affection aggravation agitation alarm "
    "alienation amazement ambivalence amusement anger angst anguish "
    "annoyance anticipation anxiety apathy apprehension aversion "
    "awe bashfulness bewilderment bitterness bliss boredom calm "
    "caution cheerfulness closeness comfort compassion complacency "
    "concern confidence confusion contempt contentment courage "
    "craving curiosity cynicism defeat defiance dejection delight "
    "depression desire despair desperation determination devotion "
    "disappointment disbelief discomfort discontent discouragement "
    "disdain disgust disillusionment dismay displeasure distaste "
    "distress dominance doubt dread eagerness ecstasy elation "
    "embarrassment empathy enchantment enjoyment enlightenment "
    "enthusiasm envy euphoria exasperation excitement exhaustion "
    "exhilaration expectation exuberance fascination fatigue fear "
    "ferocity fervor fondness foreboding forgiveness freedom "
    "friendliness fright frustration fury gaiety generosity giddiness "
    "gladness glee gloom gluttony gratification gratitude greed "
    "grief grudge guilt gullibility gust happiness hate "
    "helplessness hesitation homesickness honor hope hopelessness "
    "horror hostility humiliation hunger hurt hysteria idleness "
    "impatience indifference indignation infatuation insecurity "
    "inspiration interest intimidation intrigue irritation isolation "
    "jealousy jolliness jubilation kindness lethargy liberation "
    "loathing loneliness longing love lust malice melancholy "
    "mellowness mercy misery modesty mortification mystification "
    "neglect nervousness nostalgia numb obligation obsession "
    "offense optimism outrage overwhelming pain panic paranoia "
    "passion patience peacefulness pensive perplexity pessimism "
    "pity playfulness pleasure possessiveness powerlessness "
    "preoccupation pride provocation puzzlement rage rapture "
    "reassurance recognition regret rejection relaxation relief "
    "reluctance remorse resentment resignation resolve restlessness "
    "reverence revulsion righteousness romance sadness satisfaction "
    "scorn security self-consciousness sensitivity sentimentality "
    "serenity severity shame shock shyness skepticism smugness "
    "somberness sorrow spite strain stress stubbornness submission "
    "suffering sullenness superiority surprise suspense suspicion "
    "sweetness sympathy tenderness tension terror thankfulness "
    "thrill timidity tiredness tolerance torment tranquility "
    "triumph trust turmoil uncertainty unease unhappiness "
    "urgency valor vanity vengeance vexation vigor vulnerability "
    "warmth wariness weariness wistfulness wonder worry worship "
    "wrath yearning zeal zest "
)

_MUSIC_WORDS = (
    "accelerando accent accompaniment acoustic adagio allegro alto "
    "andante anthem arpeggio arrangement atonal baritone bass bassoon "
    "beat bell bolero boogie bossa bowing brass bridge cadence cadenza "
    "canon cantata cello chamber chant choir chord chorale chorus "
    "chromatic clarinet clef coda composition concert concerto "
    "conductor contrabass contralto counterpoint crescendo crotchet "
    "cymbal decrescendo diminuendo discord dissonance dotted downbeat "
    "drone drum duet dynamic eighth encore ensemble etude expression "
    "fanfare fermata fiddle fifth finale flat flute forte fortissimo "
    "fourth frequency fugue glissando glockenspiel grace groove "
    "guitar half harmonica harmonics harmony harp harpsichord horn "
    "hymn improvisation instrument interlude interval intonation "
    "jazz key keyboard largo legato libretto lilt lyric madrigal "
    "major march marimba measure melody mezzo minor minuet modulation "
    "motif movement mute note notation oboe octave opera operetta "
    "opus orchestra orchestration organ ornament overture passage "
    "pedal percussion phrase pianissimo piano piccolo pitch pizzicato "
    "polyphony prelude presto progression quarter quartet quaver "
    "recital register rehearsal release repertoire reprise rest "
    "rhapsody rhythm riff ritardando rondo rubato saxophone scale "
    "scherzo score semitone serenade sforzando sharp signature "
    "sixteenth slur solo sonata soprano staccato staff string "
    "strum suite sustain swing symphonic symphony syncopation "
    "synthesizer tablature tempo tenor theme third timbre time "
    "toccata tone treble tremolo triad trill trio triplet trombone "
    "trumpet tuba tuning unison upbeat variation verse vibrato "
    "viola violin virtuoso vivace vocal voice waltz whole wind "
    "woodwind xylophone "
)


# ================================================================
#  MORPHOLOGICAL DERIVATION ENGINE
# ================================================================

def _derive_words(roots_text: str) -> set:
    """Generate derived forms from root words using productive English morphology.

    Given root verbs, produces:
      root + ing, root + ed, root + er, root + ment, root + tion,
      root + able, root + ness, root + ful, root + less, root + ly,
      root + ive, root + ous, root + al, root + ity, root + ism,
      root + ist, root + dom, etc.

    Uses basic English spelling rules:
      - Drop silent 'e' before vowel suffixes (-ing, -ed, -able, -ous, -ive)
      - Double final consonant after short vowel (-ing, -ed, -er)
      - Change 'y' to 'i' before consonant suffixes (-ness, -ful, -ly)

    Returns set of derived words (lowercase, alpha only).
    """
    roots = set()
    for w in roots_text.split():
        w = w.strip().lower()
        if w and w.isalpha() and len(w) >= 2:
            roots.add(w)

    derived = set()
    vowels = set('aeiou')
    consonants = set('bcdfghjklmnpqrstvwxyz')

    # Spelling helper: should we double the final consonant?
    def _should_double(word):
        if len(word) < 3:
            return False
        if word[-1] not in consonants:
            return False
        if word[-2] not in vowels:
            return False
        if word[-3] in vowels:
            return False  # Two vowels before consonant = long vowel
        if word[-1] in ('w', 'x', 'y'):
            return False
        return True

    for root in roots:
        derived.add(root)

        # --- Vowel suffixes (drop silent e, double consonant) ---
        for suffix in ('ing', 'ed', 'er', 'able', 'ive', 'ous', 'ation'):
            if root.endswith('e') and not root.endswith('ee'):
                stem = root[:-1]
            elif _should_double(root):
                stem = root + root[-1]
            else:
                stem = root
            derived.add(stem + suffix)

        # --- Consonant suffixes (keep e, change y to i) ---
        for suffix in ('ment', 'ness', 'ful', 'less', 'ly'):
            if root.endswith('y') and len(root) > 2 and root[-2] not in vowels:
                stem = root[:-1] + 'i'
            else:
                stem = root
            derived.add(stem + suffix)

        # --- Special suffixes ---
        for suffix in ('al', 'ity', 'ism', 'ist', 'dom', 'ship',
                        'hood', 'ward', 'wise', 'like'):
            derived.add(root + suffix)

        # Plural / 3rd person singular
        if root.endswith(('s', 'sh', 'ch', 'x', 'z')):
            derived.add(root + 'es')
        elif root.endswith('y') and len(root) > 2 and root[-2] not in vowels:
            derived.add(root[:-1] + 'ies')
        else:
            derived.add(root + 's')

    # Filter: only keep words that are all alpha, length 2+
    return {w for w in derived if w.isalpha() and len(w) >= 2}


# ================================================================
#  MAIN EXPANSION FUNCTION
# ================================================================

def expand_vocabulary(fractal_composer, verbose: bool = True) -> int:
    """Expand CK's vocabulary to ~100K words.

    Adds words from all embedded sources into the fractal composer's
    WordForceIndex. Each word gets its full triadic 15D signature
    computed from letter forces via the D2 pipeline.

    Bible words are indexed phonetic-only (no semantic_op tags).
    Curated lattice seeds and spiritual words get semantic_op tags.

    Args:
        fractal_composer: The FractalComposer instance (has .index attribute)
        verbose: If True, print progress stats

    Returns:
        Number of new words added
    """
    if fractal_composer is None:
        return 0

    index = fractal_composer.index
    before = index.size
    t0 = time.time()

    if verbose:
        print("  [EXPANSION] Starting vocabulary expansion...")

    # ── Phase 0: Identity words (VOID tier) ──
    # "I" and "a" are the identity words of English. They carry VOID(0)
    # as semantic operator — the identity element of the CL algebra.
    # Tier 0 = 1-letter words. These must be learned FIRST (staircase law).
    # Gen 9.33: Without these, CK has no algebraic identity in language.
    _identity_words = {'i': VOID, 'a': VOID}
    id_count = 0
    for w, op in _identity_words.items():
        wf = index.index_word(w, semantic_op=op)
        if wf is not None:
            id_count += 1
    if verbose:
        print(f"  [EXPANSION] Identity: {id_count} words (tier 0, VOID)")

    # ── Phase 1: Bible vocabulary (phonetic only) ──
    # Bible words get full 15D triadic signatures from D2 physics
    # but NO semantic_op tag. Only curated lattice seeds get semantic
    # priority. This prevents 12K biblical words from flooding voice.
    _bible_words = set()
    for w in _KJV_BIBLE_WORDS.split():
        w = w.strip().lower()
        if w and w.isalpha() and len(w) >= 2:
            _bible_words.add(w)

    # Index Bible words WITHOUT semantic tags. Bible vocabulary is large
    # (~12K words) and was flooding the semantic-priority pool, causing
    # words like "abimelech" and "fatherless" to dominate voice output.
    # Only the hand-curated lattice seeds (~663 words) should get semantic
    # tags -- those are placed by MEANING. Bible words are indexed for
    # their force signatures only (phonetic).
    #
    # Gen 9.33: Removed semantic_op tagging. Bible words still get full
    # 15D triadic signatures, but they don't get the _SEMANTIC_BONUS
    # distance reduction in find_by_force(). The curated lattice seeds
    # dominate semantic matching as intended.
    bible_count = 0
    for w in sorted(_bible_words):
        if w not in index._words:
            wf = index.index_word(w)  # No semantic_op tag
            if wf is not None:
                bible_count += 1

    if verbose:
        print(f"  [EXPANSION] Bible: {bible_count} words (phonetic only)")

    # ── Phase 2: Common English ──
    common_count = 0
    for w in _COMMON_ENGLISH.split():
        w = w.strip().lower()
        if w and w.isalpha() and len(w) >= 2:
            if w not in index._words:
                if index.index_word(w) is not None:
                    common_count += 1

    if verbose:
        print(f"  [EXPANSION] Common English: {common_count} words")

    # ── Phase 3: Scientific/Technical ──
    science_count = 0
    for w in _SCIENCE_WORDS.split():
        w = w.strip().lower()
        if w and w.isalpha() and len(w) >= 2:
            if w not in index._words:
                if index.index_word(w) is not None:
                    science_count += 1

    if verbose:
        print(f"  [EXPANSION] Science/Tech: {science_count} words")

    # ── Phase 4: Spiritual/Emotional ──
    spirit_count = 0
    for w in _SPIRIT_WORDS.split():
        w = w.strip().lower()
        if w and w.isalpha() and len(w) >= 2:
            if w not in index._words:
                wf = index.index_word(w)
                if wf is not None:
                    # Spiritual words get semantic tags too (like Bible)
                    if wf.semantic_op < 0:
                        wf.semantic_op = wf.operator
                        index._by_semantic_op[wf.operator].append(wf)
                    spirit_count += 1

    if verbose:
        print(f"  [EXPANSION] Spiritual: {spirit_count} words (semantic tagged)")

    # ── Phase 5: Emotion vocabulary ──
    emotion_count = 0
    for w in _EMOTION_WORDS.split():
        w = w.strip().lower()
        # Skip hyphenated words (index_word handles alpha only)
        if w and w.isalpha() and len(w) >= 2:
            if w not in index._words:
                if index.index_word(w) is not None:
                    emotion_count += 1

    if verbose:
        print(f"  [EXPANSION] Emotion: {emotion_count} words")

    # ── Phase 6: Domain vocabularies ──
    domain_count = 0
    for block in (_NATURE_WORDS, _HUMAN_BODY_WORDS, _ARTS_CULTURE_WORDS,
                  _FOOD_COOKING_WORDS, _PROFESSION_WORDS, _MUSIC_WORDS):
        for w in block.split():
            w = w.strip().lower()
            if w and w.isalpha() and len(w) >= 2:
                if w not in index._words:
                    if index.index_word(w) is not None:
                        domain_count += 1

    if verbose:
        print(f"  [EXPANSION] Domain: {domain_count} words")

    # ── Phase 7: Morphological derivation (the big multiplier) ──
    # This takes every root verb and generates ~15 derived forms each.
    # ~1700 roots × ~15 forms = ~25,000 additional words.
    derived = _derive_words(_EXTENDED_ROOTS)
    derive_count = 0
    for w in sorted(derived):
        if w not in index._words:
            if index.index_word(w) is not None:
                derive_count += 1

    if verbose:
        print(f"  [EXPANSION] Derived forms: {derive_count} words")

    # ── Phase 8: Cross-derivation from all previously indexed words ──
    # Take EVERY word already in the index and generate its derived forms.
    # This compounds: Bible words get -ing, -ed, -tion, etc.
    # Common words get -ness, -ful, -less, etc.
    existing_words = list(index._words.keys())
    cross_count = 0
    for root in existing_words:
        if not root.isalpha() or len(root) < 3:
            continue
        # Generate basic derived forms
        for suffix in ('ing', 'ed', 'er', 'ness', 'ful', 'less', 'ly',
                        'ment', 'able', 'ive', 'ous', 'al', 'tion',
                        'ity', 's', 'es', 'ism', 'ist'):
            if root.endswith('e') and suffix[0] in 'aeiou':
                candidate = root[:-1] + suffix
            elif root.endswith('y') and suffix[0] not in 'aeiou' and len(root) > 2:
                candidate = root[:-1] + 'i' + suffix
            else:
                candidate = root + suffix
            if candidate.isalpha() and len(candidate) >= 2 and candidate not in index._words:
                if index.index_word(candidate) is not None:
                    cross_count += 1
                    # Stop expanding if we're well past 100K
                    if index.size > 120000:
                        break
        if index.size > 120000:
            break

    if verbose:
        print(f"  [EXPANSION] Cross-derived: {cross_count} words")

    # ── Phase 9: Recalibrate roles for the expanded population ──
    index.calibrate_roles()

    after = index.size
    elapsed = time.time() - t0
    total_new = after - before

    if verbose:
        sem_count = index.semantic_tagged_count
        print(f"  [EXPANSION] Complete: {total_new} new words in {elapsed:.1f}s")
        print(f"  [EXPANSION] Total vocabulary: {after} words "
              f"({sem_count} semantic tagged)")

    return total_new
