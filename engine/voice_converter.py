import spacy
from typing import Optional, Tuple
import lemminflect

class VoiceConverter:
    def __init__(self, nlp: Optional[spacy.language.Language] = None):
        self.nlp = nlp if nlp is not None else spacy.load("en_core_web_sm")

    def _get_subtree_text(self, token) -> str:
        """Extracts the entire subtree of a token as clean text."""
        tokens = sorted([t for t in token.subtree], key=lambda t: t.i)
        return " ".join([t.text for t in tokens])

    def _is_plural(self, token) -> bool:
        """Determines if a noun token is plural."""
        return token.tag_ in ["NNS", "NNPS"]

    def active_to_passive(self, sentence: str) -> Optional[str]:
        """Converts an active voice sentence to passive voice using dependency trees."""
        doc = self.nlp(sentence.strip())
        
        # Locate the root verb
        root_verb = None
        for token in doc:
            if token.pos_ == "VERB" and (token.dep_ == "ROOT" or token.dep_ in ["conj", "advcl"]):
                root_verb = token
                break
                
        if not root_verb:
            return None

        # Locate subject (nsubj) and direct object (dobj)
        subj = None
        dobj = None
        aux_tokens = []
        prep_phrases = []
        adv_phrases = []

        for child in root_verb.children:
            if child.dep_ == "nsubj":
                subj = child
            elif child.dep_ == "dobj":
                dobj = child
            elif child.dep_ in ["aux", "auxpass"]:
                aux_tokens.append(child)
            elif child.dep_ == "advmod":
                adv_phrases.append(self._get_subtree_text(child))
            elif child.dep_ == "prep" and child.text.lower() != "by":
                prep_phrases.append(self._get_subtree_text(child))

        if not subj or not dobj:
            return None

        # Build passive parts
        dobj_text = self._get_subtree_text(dobj)
        subj_text = self._get_subtree_text(subj)
        
        # Capitalize new subject properly
        new_subject = dobj_text[0].upper() + dobj_text[1:] if len(dobj_text) > 1 else dobj_text.upper()
        agent_phrase = f"by {subj_text[0].lower() + subj_text[1:]}"

        # Determine "to be" auxiliary form based on root verb tag and new subject plurality
        is_plural = self._is_plural(dobj)
        verb_tag = root_verb.tag_
        
        vbn_forms = lemminflect.getInflection(root_verb.lemma_, tag="VBN")
        past_participle = vbn_forms[0] if vbn_forms else root_verb.lemma_ + "ed"

        be_form = ""
        if verb_tag in ["VBD"]:  # Simple past
            be_form = "were" if is_plural else "was"
        elif verb_tag in ["VBZ", "VBP", "VB"]:  # Simple present
            be_form = "are" if is_plural else "is"
        elif verb_tag == "VBG":  # Continuous
            be_form = "being"
        else:
            be_form = "were" if is_plural else "was"

        # Check existing auxiliaries (e.g. will, can, has, have)
        if aux_tokens:
            aux_str = " ".join([t.text for t in aux_tokens])
            if any(t.lemma_ in ["will", "can", "could", "should", "would", "may", "must"] for t in aux_tokens):
                passive_verb = f"{aux_str} be {past_participle}"
            elif any(t.lemma_ in ["have", "has", "had"] for t in aux_tokens):
                passive_verb = f"{aux_str} been {past_participle}"
            else:
                passive_verb = f"{aux_str} {be_form} {past_participle}"
        else:
            passive_verb = f"{be_form} {past_participle}"

        # Insert adverbs if any
        if adv_phrases:
            adv_str = " ".join(adv_phrases)
            passive_verb = f"{be_form} {adv_str} {past_participle}"

        prep_str = (" " + " ".join(prep_phrases)) if prep_phrases else ""
        
        punctuation = doc[-1].text if doc[-1].is_punct else "."
        result = f"{new_subject} {passive_verb}{prep_str} {agent_phrase}{punctuation}"
        return result

    def passive_to_active(self, sentence: str) -> Optional[str]:
        """Converts a passive voice sentence to active voice."""
        doc = self.nlp(sentence.strip())
        
        root_verb = None
        for token in doc:
            if token.pos_ == "VERB" and (token.dep_ == "ROOT" or token.dep_ in ["conj", "advcl"]):
                root_verb = token
                break

        if not root_verb:
            return None

        nsubjpass = None
        auxpass = None
        agent_obj = None

        for child in root_verb.children:
            if child.dep_ == "nsubjpass":
                nsubjpass = child
            elif child.dep_ == "auxpass":
                auxpass = child
            elif child.dep_ == "agent" or (child.dep_ == "prep" and child.text.lower() == "by"):
                for p in child.children:
                    if p.dep_ == "pobj":
                        agent_obj = p
                        break

        if not nsubjpass or not agent_obj:
            return None

        # Build active sentence
        agent_text = self._get_subtree_text(agent_obj)
        orig_subj_text = self._get_subtree_text(nsubjpass)
        
        new_subject = agent_text[0].upper() + agent_text[1:] if len(agent_text) > 1 else agent_text.upper()
        new_object = orig_subj_text[0].lower() + orig_subj_text[1:]
        
        # Conjugate verb for active voice
        # If auxpass was "was" or "were", active verb is VBD (past)
        if auxpass and auxpass.text.lower() in ["was", "were"]:
            vbd_forms = lemminflect.getInflection(root_verb.lemma_, tag="VBD")
            active_verb = vbd_forms[0] if vbd_forms else root_verb.lemma_ + "ed"
        else:
            is_plural = self._is_plural(agent_obj)
            tag = "VBP" if is_plural else "VBZ"
            v_forms = lemminflect.getInflection(root_verb.lemma_, tag=tag)
            active_verb = v_forms[0] if v_forms else root_verb.lemma_

        punctuation = doc[-1].text if doc[-1].is_punct else "."
        return f"{new_subject} {active_verb} {new_object}{punctuation}"
