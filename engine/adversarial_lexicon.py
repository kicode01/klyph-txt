"""
Adversarial Lexicon & Structural Tell Repository (v5.0 - Deep Structural & Context-Aware Edition).
Aligned with Wikipedia's 'Signs of AI Writing' (26 structural patterns) and empirical
detector forensics (GPTZero, Originality.ai, Turnitin, Winston AI, Copyleaks, ZeroGPT).
"""
from typing import Dict, List, Tuple
import re

# ═══════════════════════════════════════════════════════════════════════════════════
# TIER 1: DEAD GIVEAWAYS (Context-Safe Replacements — Zero Frankenstein Collocations)
# ═══════════════════════════════════════════════════════════════════════════════════
TIER_1_DEAD_GIVEAWAYS: Dict[str, str] = {
    # Core AI Hallmark Verbs
    "delve": "dig", "delving": "digging", "delved": "dug", "delves": "digs",
    "embark": "begin", "embarking": "beginning", "embarked": "began", "embarks": "begins",
    "foster": "build", "fostering": "building", "fostered": "built", "fosters": "builds",
    "showcase": "show", "showcasing": "showing", "showcased": "showed", "showcases": "shows",
    "underscore": "show", "underscoring": "showing", "underscored": "showed", "underscores": "shows",
    "leverage": "use", "leveraging": "using", "leveraged": "used", "leverages": "uses",
    "garner": "earn", "garnering": "earning", "garnered": "earned", "garners": "earns",
    "unpack": "examine", "unpacking": "examining", "unpacked": "examined", "unpacks": "examines",
    "unravel": "untangle", "unraveling": "untangling", "unraveled": "untangled", "unravels": "untangles",
    "reimagine": "rethink", "reimagining": "rethinking", "reimagined": "rethought", "reimagines": "rethinks",
    "spearhead": "lead", "spearheading": "leading", "spearheaded": "led", "spearheads": "leads",
    "bolster": "strengthen", "bolstering": "strengthening", "bolstered": "strengthened", "bolsters": "strengthens",
    "catalyze": "spark", "catalyzing": "sparking", "catalyzed": "sparked", "catalyzes": "sparks",
    "navigate": "handle", "navigating": "handling", "navigated": "handled", "navigates": "handles",
    "illuminate": "clarify", "illuminating": "clarifying", "illuminated": "clarified", "illuminates": "clarifies",
    "elucidate": "explain", "elucidating": "explaining", "elucidated": "explained", "elucidates": "explains",
    "streamline": "simplify", "streamlining": "simplifying", "streamlined": "simplified", "streamlines": "simplifies",
    "alleviate": "ease", "alleviates": "eases", "alleviated": "eased", "alleviating": "easing",
    "elevate": "raise", "elevating": "raising", "elevated": "raised", "elevates": "raises",
    "empower": "allow", "empowering": "allowing", "empowered": "allowed", "empowers": "allows",
    "cultivate": "build", "cultivating": "building", "cultivated": "built", "cultivates": "builds",
    "revolutionize": "reshape", "revolutionizing": "reshaping", "revolutionized": "reshaped", "revolutionizes": "reshapes",

    # Core AI Hallmark Nouns
    "tapestry": "mix", "tapestries": "mixes",
    "realm": "field", "realms": "fields",
    "landscape": "field", "landscapes": "fields",
    "testament": "proof", "testaments": "proofs",
    "intricacy": "detail", "intricacies": "details",
    "complexity": "problem", "complexities": "problems",
    "interplay": "interaction", "interplays": "interactions",
    "synergy": "teamwork", "synergies": "results",
    "paradigm": "model", "paradigms": "models",
    "cornerstone": "foundation", "cornerstones": "foundations",
    "cadence": "pace", "cadences": "paces",
    "learnings": "lessons",
    "takeaway": "point", "takeaways": "points",
    "touchpoint": "contact", "touchpoints": "contacts",

    # Core AI Hallmark Adjectives
    "vibrant": "lively",
    "crucial": "important",
    "pivotal": "key",
    "intricate": "detailed",
    "meticulous": "careful",
    "meticulously": "carefully",
    "bustling": "busy",
    "nestled": "set",
    "robust": "reliable",
    "seamless": "smooth",
    "seamlessly": "smoothly",
    "groundbreaking": "new",
    "renowned": "well-known",
    "enduring": "lasting",
    "daunting": "hard",
    "ever-evolving": "changing",
    "ever-changing": "shifting",
    "game-changing": "major",
    "holistic": "full",
    "holistically": "fully",
    "actionable": "practical",
    "impactful": "effective",
    "poised": "ready",
    "multifaceted": "complex",
    "transformative": "major",
    "invaluable": "useful",
    "cutting-edge": "modern",
    "state-of-the-art": "modern",
    "comprehensive": "full",
}

# ═══════════════════════════════════════════════════════════════════════════════════
# TIER 2: FORMULAIC TRANSITIONS & CONNECTORS
# ═══════════════════════════════════════════════════════════════════════════════════
TIER_2_FORMULAIC_CONNECTORS: Dict[str, str] = {
    "furthermore": "also",
    "moreover": "besides",
    "notably": "in particular",
    "consequently": "so",
    "subsequently": "later",
    "accordingly": "so",
    "nonetheless": "still",
    "henceforth": "from now on",
    "indeed": "in fact",
    "specifically": "for example",
    "essentially": "basically",
    "ultimately": "in the end",
    "arguably": "often",
    "fundamentally": "at root",
    "inherently": "by nature",
    "profoundly": "deeply",
    "additionally": "also",
    "undoubtedly": "clearly",
}

# ═══════════════════════════════════════════════════════════════════════════════════
# TIER 3: PSEUDO-ACADEMIC LATINATE INFLATION
# ═══════════════════════════════════════════════════════════════════════════════════
TIER_3_LATINATE_INFLATION: Dict[str, str] = {
    "ameliorate": "improve", "ameliorates": "improves", "ameliorated": "improved", "ameliorating": "improving",
    "disseminate": "share", "disseminates": "shares", "disseminated": "shared", "disseminating": "sharing",
    "juxtapose": "compare", "juxtaposes": "compares", "juxtaposed": "compared", "juxtaposing": "comparing",
    "juxtaposition": "contrast", "juxtapositions": "contrasts",
    "ubiquitous": "common", "ubiquity": "spread",
    "plethora": "many",
    "salient": "main",
    "concomitant": "related",
    "epitome": "example",
    "quintessential": "classic",
    "efficacious": "effective", "efficacy": "effectiveness",
    "dichotomy": "split", "dichotomies": "splits",
    "manifestation": "sign", "manifestations": "signs",
    "reverberate": "echo", "reverberates": "echoes", "reverberated": "echoed", "reverberating": "echoing",
    "propensity": "tendency", "propensities": "tendencies",
    "inextricably": "closely",
    "veritable": "real",
    "stratification": "layering",
    "heterogeneous": "mixed",
    "homogeneous": "uniform",
    "coalesce": "join", "coalesces": "joins", "coalesced": "joined", "coalescing": "joining",
    "germane": "relevant",
    "nascent": "early",
    "surpass": "beat", "surpasses": "beats", "surpassed": "beat", "surpassing": "beating",
    "accentuate": "stress", "accentuates": "stresses", "accentuated": "stressed", "accentuating": "stressing",
    "delineate": "outline", "delineates": "outlines", "delineated": "outlined", "delineating": "outlining",
    "promulgate": "publish", "promulgates": "publishes", "promulgated": "published", "promulgating": "publishing",
    "recapitulate": "sum up", "recapitulates": "sums up", "recapitulated": "summed up", "recapitulating": "summing up",
    "substantiate": "prove", "substantiates": "proves", "substantiated": "proved", "substantiating": "proving",
    "explicate": "explain", "explicates": "explains", "explicated": "explained", "explicating": "explaining",
    "obviate": "remove", "obviates": "removes", "obviated": "removed", "obviating": "removing",
    "cogent": "clear",
    "disparate": "different",
    "pervasive": "widespread",
    "superfluous": "extra",
    "utilize": "use", "utilizes": "uses", "utilized": "used", "utilizing": "using", "utilization": "use",
    "facilitate": "help", "facilitates": "helps", "facilitated": "helped", "facilitating": "helping",
    "demonstrate": "show", "demonstrates": "shows", "demonstrated": "showed", "demonstrating": "showing",
    "ascertain": "find out", "ascertains": "finds out", "ascertained": "found out", "ascertaining": "finding out",
    "commence": "start", "commences": "starts", "commenced": "started", "commencing": "starting",
    "endeavor": "effort", "endeavors": "efforts", "endeavored": "tried", "endeavoring": "trying",
    "methodology": "method", "methodologies": "methods",
    "unprecedented": "rare",
    "substantial": "large", "substantially": "largely",
    "implement": "put in place", "implementing": "putting in place", "implemented": "put in place", "implementation": "rollout",
}

# ═══════════════════════════════════════════════════════════════════════════════════
# TIER 4: CORPORATE & SILICON VALLEY JARGON
# ═══════════════════════════════════════════════════════════════════════════════════
TIER_4_CORPORATE_JARGON: Dict[str, str] = {
    "ideate": "brainstorm", "ideating": "brainstorming", "ideated": "brainstormed", "ideation": "planning",
    "operationalize": "run", "operationalizing": "running", "operationalized": "ran",
    "deliverable": "result", "deliverables": "results",
    "bandwidth": "time",
    "table stakes": "basics",
    "core competency": "strength", "core competencies": "strengths",
    "value proposition": "benefit", "value propositions": "benefits",
    "stakeholder": "team", "stakeholders": "teams",
    "buy-in": "support",
    "pivot": "shift", "pivoting": "shifting", "pivoted": "shifted", "pivots": "shifts",
    "hyper-growth": "fast growth",
    "frictionless": "easy",
    "best-of-breed": "top",
    "mission-critical": "critical",
    "bespoke": "custom",
    "next-gen": "new",
    "disruptive": "new", "disruption": "change", "disrupt": "change",
    "north star": "goal",
    "low-hanging fruit": "easy wins",
    "move the needle": "make a difference",
    "circle back": "follow up",
    "touch base": "talk",
}

# ═══════════════════════════════════════════════════════════════════════════════════
# TIER 5: SYCOPHANTIC CHATBOT OPENERS, CLOSERS & STAGED RUN-UPS (SKILL.md §2, §4, §22)
# ═══════════════════════════════════════════════════════════════════════════════════
TIER_5_CHATBOT_PHRASES: List[Tuple[re.Pattern, str, str]] = [
    # Staged openers and throat-clearing
    (re.compile(r"\bin today'?s\s+(?:[\w-]+\s+){0,4}(?:world|age|era|landscape|environment|society|market)[,\s]*", re.IGNORECASE), "", "Strip generic AI opener"),
    (re.compile(r"\bin the\s+(?:modern|contemporary|digital)\s+(?:world|age|era|landscape|environment)[,\s]*", re.IGNORECASE), "", "Strip modern era cliché"),
    (re.compile(r"\b(?:it is|it's) (?:worth|important to|essential to|crucial to) not(?:e|ing) that\s*", re.IGNORECASE), "", "Strip throat-clearing filler"),
    (re.compile(r"\bit (?:should|must) be noted that\s*", re.IGNORECASE), "", "Strip passive filler"),
    (re.compile(r"\bwhen it comes to\s+", re.IGNORECASE), "for ", "Tighten conversational filler"),
    (re.compile(r"\bin order to\b", re.IGNORECASE), "to", "Streamline infinitive verb"),
    (re.compile(r"\bat its core[,\s]*", re.IGNORECASE), "", "Remove aphorism staging (§3)"),
    (re.compile(r"\bthe real question is\s+", re.IGNORECASE), "the question is ", "Remove depth staging (§3)"),
    (re.compile(r"\bwhat really matters is\s+", re.IGNORECASE), "", "Remove depth staging (§3)"),
    (re.compile(r"\bwithout further ado[,\s]*", re.IGNORECASE), "", "Remove stage-setting filler (§4)"),
    (re.compile(r"\bhere'?s what you need to know[.!?,]*\s*", re.IGNORECASE), "", "Remove staged run-up (§4)"),
    (re.compile(r"\blet'?s (?:dive in|break this down|be honest|face it)[.!?,]*\s*", re.IGNORECASE), "", "Remove staged run-up (§4)"),
    (re.compile(r"\blet'?s explore\s+", re.IGNORECASE), "consider ", "Replace conversational prompt (§4)"),
    (re.compile(r"\bas an ai (?:language model|assistant)[,\s]*", re.IGNORECASE), "", "Remove AI persona artifact (§22)"),
    (re.compile(r"\bi hope this (?:helps|information is useful)!?[,\s]*", re.IGNORECASE), "", "Remove chatbot artifact (§22)"),
    (re.compile(r"\bgreat question!?[,\s]*", re.IGNORECASE), "", "Remove sycophantic chatbot filler (§22)"),
    (re.compile(r"\byou'?re absolutely right!?[,\s]*", re.IGNORECASE), "", "Remove chatbot agreement loop (§22)"),
    (re.compile(r"\bthe future looks bright[^.!?]*[.!?]*\s*", re.IGNORECASE), "", "Remove stock send-off (§13)"),
    (re.compile(r"\bexciting times lie ahead[^.!?]*[.!?]*\s*", re.IGNORECASE), "", "Remove stock send-off (§13)"),
    (re.compile(r"\bonly time will tell[^.!?]*[.!?]*\s*", re.IGNORECASE), "", "Remove stock send-off (§13)"),
    (re.compile(r"\b(?:ultimately|in conclusion|all in all|in summary|to sum up),\s*embracing these [^,]+ will [^.!?]+[.!?]?\s*", re.IGNORECASE), "", "Cut empty horizon send-off (§13)"),
]

# ═══════════════════════════════════════════════════════════════════════════════════
# TIER 6: COPULA AVOIDANCE & SIGNIFICANCE INFLATION (SKILL.md §13, §16, §18)
# ═══════════════════════════════════════════════════════════════════════════════════
TIER_6_SIGNIFICANCE_INFLATION: List[Tuple[re.Pattern, str, str]] = [
    # High-frequency AI multi-word collocations (Context-Aware)
    (re.compile(r"\bplays? a (?:crucial|pivotal|vital|key|fundamental) role in fostering\b", re.IGNORECASE), "supports", "Replace inflated role cliché (§13)"),
    (re.compile(r"\bplays? a (?:crucial|pivotal|vital|key|fundamental) role in shaping\b", re.IGNORECASE), "shapes", "Replace inflated role cliché (§13)"),
    (re.compile(r"\bplays? a (?:crucial|pivotal|vital|key|fundamental) role in driving\b", re.IGNORECASE), "drives", "Replace inflated role cliché (§13)"),
    (re.compile(r"\bplays? a (?:crucial|pivotal|vital|key|fundamental) role in ensuring\b", re.IGNORECASE), "ensures", "Replace inflated role cliché (§13)"),
    (re.compile(r"\bplays? a (?:crucial|pivotal|vital|key|fundamental) role in\b", re.IGNORECASE), "shapes", "Replace inflated role cliché (§13)"),

    # Serves as a testament to...
    (re.compile(r"\b(?:serves|stands) as a testament to the (?:enduring|lasting) value of\b", re.IGNORECASE), "shows the value of", "Deflate significance (§13)"),
    (re.compile(r"\b(?:serves|stands) as a testament to\b", re.IGNORECASE), "shows", "Replace pretentious copula avoidance (§18)"),
    (re.compile(r"\bis a testament to\b", re.IGNORECASE), "shows", "Replace pretentious copula avoidance (§18)"),
    (re.compile(r"\bbears testament to\b", re.IGNORECASE), "shows", "Replace pretentious copula avoidance (§18)"),

    # Corporate/Academic Noun Cluster De-Inflation
    (re.compile(r"\bin the realm of contemporary higher education\b", re.IGNORECASE), "in universities today", "De-inflate academic setting"),
    (re.compile(r"\bin contemporary higher education\b", re.IGNORECASE), "in universities", "De-inflate academic setting"),
    (re.compile(r"\bauthentic learning environments\b", re.IGNORECASE), "honest classrooms", "Replace abstract noun stack"),
    (re.compile(r"\ba rapidly evolving (?:landscape|space|field) shaped by\b", re.IGNORECASE), "rapid changes from", "De-inflate evolving landscape (§13)"),
    (re.compile(r"\ba rapidly evolving (?:landscape|space|field)\b", re.IGNORECASE), "fast changes", "De-inflate evolving landscape (§13)"),
    (re.compile(r"\bis essential to drive operational excellence\b", re.IGNORECASE), "keeps operations running well", "De-corporatize predicate"),
    (re.compile(r"\bdrive operational excellence\b", re.IGNORECASE), "run operations well", "De-corporatize predicate"),
    (re.compile(r"\bas we (?:embark|start|begin) on this (?:transformative|deep|major) journey,\s*", re.IGNORECASE), "", "Strip theatrical journey opener (§13)"),
    (re.compile(r"\bwill (?:empower|help|let) (?:stakeholders|partners|teams) to thrive in an (?:ever-changing|shifting) market\b", re.IGNORECASE), "helps teams compete as the market shifts", "De-corporatize horizon closer"),
    (re.compile(r"\b(?:empower|help) (?:stakeholders|partners|teams) to thrive\b", re.IGNORECASE), "help teams succeed", "Simplify corporate cliché"),
    (re.compile(r"\bfor forward-thinking brands\b", re.IGNORECASE), "for brands", "Remove sales adjective (§16)"),
    (re.compile(r"\b(?:this|that) (?:paradigm|model) shift (?:allows|enables|lets)\b", re.IGNORECASE), "this shift allows", "Remove paradigm cliché"),
    (re.compile(r"\bresonate (?:profoundly|deeply) with their target audience\b", re.IGNORECASE), "reach their customers", "Replace marketing cliché (§16)"),
    (re.compile(r"\bpave the way for sustainable growth\b", re.IGNORECASE), "support steady growth", "Deflate horizon promise (§13)"),

    # Prepositional & Determiner Inflation
    (re.compile(r"\bin the realm of\s+", re.IGNORECASE), "in ", "Simplify prepositional inflation"),
    (re.compile(r"\bacross the realm of\s+", re.IGNORECASE), "across ", "Simplify prepositional inflation"),
    (re.compile(r"\ba myriad of\b", re.IGNORECASE), "many", "Replace myriad"),
    (re.compile(r"\ba wide array of\b", re.IGNORECASE), "many", "Simplify noun phrase"),
    (re.compile(r"\ba wide variety of\b", re.IGNORECASE), "many", "Simplify noun phrase"),
    (re.compile(r"\ba broad spectrum of\b", re.IGNORECASE), "many", "Simplify noun phrase"),
    (re.compile(r"\ba multifaceted approach\b", re.IGNORECASE), "several steps", "De-corporatize approach"),
    (re.compile(r"\bmarking a pivotal moment in\b", re.IGNORECASE), "changing", "Replace significance inflation (§13)"),
    (re.compile(r"\bpivotal moment\b", re.IGNORECASE), "turning point", "Replace clichéd idiom"),
    (re.compile(r"\bwatershed moment\b", re.IGNORECASE), "turning point", "Replace cliché"),
    (re.compile(r"\bheralds a new era of\b", re.IGNORECASE), "starts", "Deflate significance (§13)"),
    (re.compile(r"\bsets the stage for\b", re.IGNORECASE), "prepares for", "Simplify theatrical idiom (§13)"),

    # Delving & Deep Diving
    (re.compile(r"\bdelv(?:e|es) into\b", re.IGNORECASE), "examine", "Purge AI hallmark 'delve' (§12)"),
    (re.compile(r"\bdelving into\b", re.IGNORECASE), "studying", "Purge AI hallmark 'delving' (§12)"),
    (re.compile(r"\bdelved into\b", re.IGNORECASE), "examined", "Purge AI hallmark 'delved' (§12)"),
    (re.compile(r"\btake a deep dive into\b", re.IGNORECASE), "study", "Replace corporate buzzword (§12)"),
    (re.compile(r"\bharness(?:ing)? the power of\b", re.IGNORECASE), "use", "Replace hyperbolic phrasing"),
    (re.compile(r"\bembark(?:ed|ing)? on a (?:transformative )?journey\b", re.IGNORECASE), "start", "Replace theatrical cliché"),
    (re.compile(r"\bis poised to revolutionize\b", re.IGNORECASE), "is changing", "Deflate sales prediction (§16)"),
    (re.compile(r"\bpoised to\b", re.IGNORECASE), "ready to", "Replace overused participle"),

    # Direct Copula Avoidance (SKILL.md §18)
    (re.compile(r"\bserves as an?\b", re.IGNORECASE), "is a", "Restore natural copula (§18)"),
    (re.compile(r"\bboasts an?\b", re.IGNORECASE), "has a", "Restore natural copula (§18)"),
    (re.compile(r"\bfeatures an?\b", re.IGNORECASE), "has a", "Restore natural copula (§18)"),
    (re.compile(r"\bstands as an?\b", re.IGNORECASE), "is a", "Restore natural copula (§18)"),
    (re.compile(r"\bfunctions as an?\b", re.IGNORECASE), "is a", "Restore natural copula (§18)"),
    (re.compile(r"\bpaints a vivid picture of\b", re.IGNORECASE), "shows", "De-theatricalize prose"),
]

# ═══════════════════════════════════════════════════════════════════════════════════
# TIER 7: CLICHÉ METAPHORS & TAPESTRY HALLMARKS
# ═══════════════════════════════════════════════════════════════════════════════════
TIER_7_METAPHORS: List[Tuple[re.Pattern, str, str]] = [
    (re.compile(r"\ba rich tapestry of\b", re.IGNORECASE), "a mix of", "Replace cliché tapestry"),
    (re.compile(r"\ba vibrant tapestry of\b", re.IGNORECASE), "a mix of", "Replace cliché tapestry"),
    (re.compile(r"\bthe intricate tapestry of\b", re.IGNORECASE), "the mix of", "Replace cliché tapestry"),
    (re.compile(r"\ba beacon of hope\b", re.IGNORECASE), "a guide", "Replace poetic cliché"),
    (re.compile(r"\ba symphony of\b", re.IGNORECASE), "a combination of", "Replace musical metaphor"),
    (re.compile(r"\ba kaleidoscope of\b", re.IGNORECASE), "a shifting mix of", "Replace optical metaphor"),
    (re.compile(r"\ba double-edged sword\b", re.IGNORECASE), "a tradeoff", "Replace tired idiom"),
    (re.compile(r"\ba melting pot of\b", re.IGNORECASE), "a mix of", "Replace sociological cliché"),
    (re.compile(r"\ba treasure trove of\b", re.IGNORECASE), "a collection of", "Replace commercial cliché"),
    (re.compile(r"\ba breath of fresh air\b", re.IGNORECASE), "a welcome change", "Replace conversational cliché"),
    (re.compile(r"\ban intricate dance of\b", re.IGNORECASE), "a balance between", "Replace theatrical cliché"),
    (re.compile(r"\buncharted territory\b", re.IGNORECASE), "new ground", "Replace geographical cliché"),
]

# ═══════════════════════════════════════════════════════════════════════════════════
# CONTRACTION INJECTION MAP (Natural Human Entropy Differentiator)
# ═══════════════════════════════════════════════════════════════════════════════════
CONTRACTION_MAP: Dict[str, str] = {
    r"\bdo not\b": "don't",
    r"\bdoes not\b": "doesn't",
    r"\bdid not\b": "didn't",
    r"\bcannot\b": "can't",
    r"\bcan not\b": "can't",
    r"\bcould not\b": "couldn't",
    r"\bwould not\b": "wouldn't",
    r"\bshould not\b": "shouldn't",
    r"\bwill not\b": "won't",
    r"\bhave not\b": "haven't",
    r"\bhas not\b": "hasn't",
    r"\bhad not\b": "hadn't",
    r"\bis not\b": "isn't",
    r"\bare not\b": "aren't",
    r"\bwas not\b": "wasn't",
    r"\bwere not\b": "weren't",
    r"\bit is\b": "it's",
    r"\bthere is\b": "there's",
    r"\bthat is\b": "that's",
    r"\bwhat is\b": "what's",
}
