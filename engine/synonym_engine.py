import spacy
from typing import List, Optional, Set, Tuple
from nltk.corpus import wordnet as wn
import lemminflect
from wordfreq import zipf_frequency

class SynonymEngine:
    def __init__(self, nlp: Optional[spacy.language.Language] = None):
        self.nlp = nlp if nlp is not None else spacy.load("en_core_web_sm")
        
        # High-frequency formal word mappings (Curated natural pairs)
        self.formal_enhancements = {
            "big": "substantial",
            "small": "modest",
            "good": "favorable",
            "bad": "detrimental",
            "show": "demonstrate",
            "help": "facilitate",
            "look at": "examine",
            "use": "utilize",
            "get": "obtain",
            "buy": "purchase",
            "tell": "inform",
            "ask": "inquire",
            "check": "verify",
            "start": "commence",
            "end": "conclude",
            "need": "require",
            "give": "provide",
            "make": "produce",
            "hard": "challenging",
            "easy": "straightforward",
            "change": "modify",
            "fix": "rectify",
            "stop": "cease",
            "try": "attempt",
            "job": "profession",
            "smart": "astute",
            "danger": "hazard",
            "kids": "children",
            "boss": "supervisor",
            "know": "understand",
            "clean": "elegant",
            "find": "discover",
            "fast": "rapid",
            "slow": "gradual",
            "clear": "explicit",
            "wrong": "erroneous",
            "old": "antecedent",
            "new": "contemporary",
            "investigate": "examine",
            "think": "hypothesize",
            "see": "observe"
        }
        
        # Simple word mappings
        self.simple_enhancements = {v: k for k, v in self.formal_enhancements.items()}
        self.simple_enhancements.update({
            "utilize": "use",
            "facilitate": "help",
            "commence": "start",
            "conclude": "end",
            "demonstrate": "show",
            "purchase": "buy",
            "inquire": "ask",
            "rectify": "fix",
            "attempt": "try",
            "substantial": "large",
            "detrimental": "harmful",
            "straightforward": "simple",
            "understand": "know",
            "procure": "buy",
            "elucidate": "explain",
            "erroneous": "wrong"
        })

    def _get_wordnet_pos(self, spacy_tag: str):
        """Maps Penn Treebank POS tag to WordNet POS."""
        if spacy_tag.startswith("NN"):
            return wn.NOUN
        elif spacy_tag.startswith("VB"):
            return wn.VERB
        elif spacy_tag.startswith("JJ"):
            return wn.ADJ
        elif spacy_tag.startswith("RB"):
            return wn.ADV
        return None

    def get_synonyms(self, word: str, tag: str, mode: str = "standard", max_candidates: int = 8) -> List[str]:
        """
        Retrieves context-appropriate synonyms using multi-tier WordNet relations
        (direct synsets, hypernyms, hyponyms) filtered by human Zipf frequency.
        """
        wn_pos = self._get_wordnet_pos(tag)
        lower_w = word.lower()
        candidates: Set[str] = set()

        # Check curated lookup dictionaries first for strong mode alignment
        if mode in ["formal", "academic"] and lower_w in self.formal_enhancements:
            candidates.add(self.formal_enhancements[lower_w])
        elif mode in ["simple", "fluency", "shorten"] and lower_w in self.simple_enhancements:
            candidates.add(self.simple_enhancements[lower_w])

        # Multi-tier WordNet discovery
        if wn_pos:
            synsets = wn.synsets(lower_w, pos=wn_pos)
            
            # Tier 1: Direct synset lemmas
            for s in synsets[:6]:
                for lemma in s.lemmas():
                    cand = lemma.name().lower().replace("_", " ")
                    if cand != lower_w:
                        candidates.add(cand)

                # Tier 2: Related hypernyms (broader terms)
                for h in s.hypernyms()[:2]:
                    for lemma in h.lemmas():
                        cand = lemma.name().lower().replace("_", " ")
                        if cand != lower_w:
                            candidates.add(cand)

                # Tier 3: Hyponyms (more specific terms)
                for h in s.hyponyms()[:3]:
                    for lemma in h.lemmas():
                        cand = lemma.name().lower().replace("_", " ")
                        if cand != lower_w:
                            candidates.add(cand)

                # Tier 4: Similar to (for adjectives)
                if wn_pos == wn.ADJ:
                    for sim in s.similar_tos():
                        for lemma in sim.lemmas():
                            cand = lemma.name().lower().replace("_", " ")
                            if cand != lower_w:
                                candidates.add(cand)

        # Inflect candidates to match the exact grammatical form of the original word
        inflected_candidates: List[Tuple[str, float]] = []
        for cand in candidates:
            # If candidate is a single word, inflect it
            if " " not in cand and (tag.startswith("VB") or tag.startswith("NN")):
                forms = lemminflect.getInflection(cand, tag=tag)
                inflected_form = forms[0] if forms else cand
            else:
                inflected_form = cand
                
            freq = zipf_frequency(inflected_form.lower(), "en")
            # Filter out extreme non-words (Zipf < 2.2)
            if freq >= 2.2:
                inflected_candidates.append((inflected_form, freq))

        # Sort candidates according to the mode
        if mode in ["formal", "academic"]:
            # Prefer longer, higher register words
            inflected_candidates.sort(key=lambda x: (len(x[0]), x[1]), reverse=True)
        elif mode in ["simple", "shorten"]:
            # Prefer shorter, high frequency everyday words
            inflected_candidates.sort(key=lambda x: (x[1], -len(x[0])), reverse=True)
        elif mode == "creative":
            # Prefer expressive, varied words
            inflected_candidates.sort(key=lambda x: (-abs(len(x[0]) - 8), x[1]))
        else:
            # Standard / Fluency: highest human frequency
            inflected_candidates.sort(key=lambda x: x[1], reverse=True)

        final_list = []
        for cand, _ in inflected_candidates:
            if word[0].isupper() and len(cand) > 1:
                cand = cand[0].upper() + cand[1:]
            if cand not in final_list:
                final_list.append(cand)

        return final_list[:max_candidates]

    def get_ranked_synonyms_for_word(self, word: str, mode: str = "standard", count: int = 8) -> List[str]:
        """Provides on-demand synonyms when user clicks on a single word in the UI."""
        clean = word.strip()
        doc = self.nlp(clean)
        tag = doc[0].tag_ if len(doc) > 0 else "NN"
        return self.get_synonyms(clean, tag, mode=mode, max_candidates=count)

    def substitute_sentence(
        self,
        sentence: str,
        mode: str = "standard",
        synonym_level: int = 2,
        preserve_words: Optional[List[str]] = None,
        candidate_index: int = 0
    ) -> str:
        """Substitutes eligible content words based on density level and candidate variation."""
        doc = self.nlp(sentence.strip())
        preserve_set = set(w.lower() for w in (preserve_words or []))
        
        eligible_tokens = []
        for token in doc:
            if (
                token.pos_ in ["NOUN", "VERB", "ADJ", "ADV"]
                and not token.is_stop
                and token.tag_ not in ["NNP", "NNPS"]
                and token.lemma_ not in ["be", "have", "do"]
                and token.text.lower() not in preserve_set
                and len(token.text) > 2
            ):
                eligible_tokens.append(token)

        if not eligible_tokens:
            return sentence

        # Stride based on synonym_level (1=Low, 2=Med, 3=High, 4=Extreme)
        if synonym_level == 1:
            stride = 4
        elif synonym_level == 2:
            stride = 2
        elif synonym_level == 3:
            stride = 1
        else:
            stride = 1

        replacements = {}
        for i, token in enumerate(eligible_tokens):
            if i % stride == 0:
                syns = self.get_synonyms(token.text, token.tag_, mode=mode)
                # Filter to single-word synonyms for seamless sentence inline replacement
                single_syns = [s for s in syns if " " not in s]
                if single_syns:
                    pick_idx = candidate_index % len(single_syns)
                    replacements[token.i] = single_syns[pick_idx]

        reconstructed = ""
        for i, token in enumerate(doc):
            word = replacements.get(token.i, token.text)
            if token.is_punct or (token.dep_ == "poss" and token.text == "'s"):
                reconstructed += word
            else:
                reconstructed += (" " if reconstructed and not reconstructed.endswith((" ", "(", "[")) else "") + word

        return reconstructed
