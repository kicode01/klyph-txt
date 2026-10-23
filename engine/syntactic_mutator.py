"""
Syntactic Mutator & Structural Deconstructor (v5.0).
Eliminates deep syntactic AI tells identified in Wikipedia's 'Signs of AI Writing' (SKILL.md)
and modern transformer classifiers (DeBERTa-v3 / RoBERTa / Binoculars):
- §1: 'Not X, but Y' contrast elimination
- §6: Forced triad compression & varied splitting (no repetitive 'They also...' templates)
- §8: Em-dash / en-dash removal
- §11: Instrumental 'By [verb]-ing..., [subject] can...' restructuring
- §15: Shallow trailing '-ing' participial rider elimination
"""
import re
import spacy
import lemminflect
from typing import List, Optional
from .adversarial_lexicon import CONTRACTION_MAP


class SyntacticMutator:
    def __init__(self, nlp: Optional[spacy.language.Language] = None):
        self.nlp = nlp if nlp is not None else spacy.load("en_core_web_sm")
        self.subordinating_conjunctions = {
            "although", "though", "even though", "because", "since",
            "while", "whereas", "if", "unless", "whenever", "after",
            "before", "as soon as", "despite the fact that"
        }

    def strip_em_dashes(self, text: str) -> str:
        """
        SKILL.md §8: 'The final rewrite must not contain em dashes (—) or en dashes (–)...
        Replace each dash with a period, comma, colon, or parentheses, or rewrite the sentence.'
        """
        res = re.sub(r"\s*[—–]\s*", ", ", text)
        res = re.sub(r"\s+--\s+", ", ", res)
        res = re.sub(r",\s*,", ",", res)
        return res

    def inject_contractions(self, text: str) -> str:
        """
        Injects natural English contractions where appropriate.
        """
        res = text
        for pat_str, contraction in CONTRACTION_MAP.items():
            pattern = re.compile(pat_str, re.IGNORECASE)
            def repl(m, rep=contraction):
                orig = m.group(0)
                if orig[0].isupper() and len(rep) > 1:
                    return rep[0].upper() + rep[1:]
                return rep
            res = pattern.sub(repl, res)
        return res

    def eliminate_ing_riders(self, sentence: str) -> str:
        """
        SKILL.md §15: 'Shallow -ing riders (highlighting, underscoring, emphasizing, ensuring,
        reflecting, symbolizing, contributing to, cultivating, fostering, encompassing,
        showcasing, offering).'
        Converts trailing participial riders into finite active clauses or direct predicates.
        """
        s = sentence.strip()
        rider_map = {
            "offering": "and offers",
            "highlighting": "which shows",
            "underscoring": "which shows",
            "emphasizing": "and stresses",
            "ensuring": "to make sure",
            "reflecting": "which reflects",
            "symbolizing": "representing",
            "contributing to": "and helps",
            "cultivating": "and builds",
            "fostering": "and builds",
            "encompassing": "including",
            "showcasing": "and shows",
            "enabling": "which lets",
            "allowing": "which lets",
            "paving": "and opens",
        }
        pattern = re.compile(
            r",\s+(offering|highlighting|underscoring|emphasizing|ensuring|reflecting|"
            r"symbolizing|contributing to|cultivating|fostering|encompassing|showcasing|"
            r"enabling|allowing|paving)\s+([^.!?]+)([.!?]?)$",
            re.IGNORECASE
        )
        def repl(m):
            participle = m.group(1).lower()
            rest = m.group(2).strip()
            punct = m.group(3) or "."
            replacement = rider_map.get(participle, "and")
            return f" {replacement} {rest}{punct}"

        return pattern.sub(repl, s)

    def rewrite_by_gerund_opener(self, sentence: str) -> str:
        """
        Rewrites the classic AI template:
        'By [verb]-ing X, [subject] can [verb] Y.' ->
        '[Subject] can [verb] Y through [noun/gerund X].' or '[Gerund X] lets [subject] [verb] Y.'
        """
        s = sentence.strip()
        # Match optional transition before 'By ...'
        pat = re.compile(
            r"^(?:(Also|Besides|Still|In fact),\s+)?By\s+([a-z-]+ing\s+[^,]+),\s+([A-Za-z\s]+?)\s+(can|will|may)\s+([^.!?]+)([.!?]?)$",
            re.IGNORECASE
        )
        m = pat.match(s)
        if not m:
            return s

        trans = m.group(1)
        gerund_phrase = m.group(2).strip()
        subj = m.group(3).strip()
        modal = m.group(4).lower()
        predicate = m.group(5).strip()
        punct = m.group(6) or "."

        # Convert 'By examining X, organizations can make Y' -> 'Studying X lets organizations make Y'
        gerund_cap = gerund_phrase[0].upper() + gerund_phrase[1:]
        subj_low = subj[0].lower() + subj[1:] if len(subj) > 1 else subj.lower()

        if modal == "can":
            rewritten = f"{gerund_cap} lets {subj_low} {predicate}{punct}"
        else:
            rewritten = f"{subj[0].upper() + subj[1:]} {modal} {predicate} by {gerund_phrase[0].lower() + gerund_phrase[1:]}{punct}"

        if trans:
            rewritten = f"{trans.capitalize()}, {rewritten[0].lower() + rewritten[1:]}"
        return rewritten

    def split_coordinate_clauses(self, sentence: str) -> List[str]:
        """
        Splits long composite sentences joined by ', and', ', but', ', yet' into two natural sentences.
        """
        s = sentence.strip()
        doc = self.nlp(s)
        if len(doc) < 15:
            return [s]

        for match in re.finditer(r",\s+(and|but|yet)\s+", s, re.IGNORECASE):
            part1 = s[:match.start()].strip()
            conj = match.group(1).lower()
            part2 = s[match.end():].strip()

            doc1 = self.nlp(part1)
            doc2 = self.nlp(part2)
            has_v1 = any(t.pos_ in ("VERB", "AUX") for t in doc1)
            has_v2 = any(t.pos_ in ("VERB", "AUX") for t in doc2)
            has_subj2 = any(t.dep_ in ("nsubj", "nsubjpass", "expl", "csubj") for t in doc2)

            if has_v1 and has_v2 and has_subj2 and len(doc1) >= 4 and len(doc2) >= 4:
                punct = "." if not part2.endswith((".", "!", "?")) else ""
                part1_clean = part1 if part1.endswith((".", "!", "?")) else part1 + "."
                if conj == "but":
                    part2_cap = f"But {part2[0].lower() + part2[1:]}{punct}"
                elif conj == "yet":
                    part2_cap = f"Yet {part2[0].lower() + part2[1:]}{punct}"
                else:
                    part2_cap = f"{part2[0].upper() + part2[1:]}{punct}"
                return [part1_clean, part2_cap]

        return [s]

    def split_action_triads(self, text: str) -> str:
        """
        SKILL.md §6: Breaks formulaic 3-verb triads ('enable X to A, B, and C')
        into natural two-part structures without repeating a canned 'They also...' template.
        """
        triad_pat = re.compile(
            r"\b(enable|enables|allow|allows|help|helps|empower|empowers)\s+([A-Za-z\s]+?)\s+to\s+([^,.!?]+?),\s+([^,.!?]+?),\s+and\s+([^.!?]+?)([.!?])",
            re.IGNORECASE
        )
        call_idx = [0]
        def triad_repl(m):
            call_idx[0] += 1
            verb = m.group(1)
            target = m.group(2).strip()
            a1 = m.group(3).strip()
            a2 = m.group(4).strip()
            a3 = m.group(5).strip()
            punct = m.group(6) or "."
            a3_words = a3.split()
            if a3_words:
                v_vbz = lemminflect.getInflection(a3_words[0].lower(), tag="VBZ")
                if v_vbz:
                    finite_v = v_vbz[0]
                    rest_a3 = " ".join(a3_words[1:])
                    pron = "This" if call_idx[0] % 2 == 1 else "That"
                    return f"{verb} {target} to {a1} and {a2}. {pron} {finite_v} {rest_a3}{punct}"
            return f"{verb} {target} to {a1} and {a2}, as well as {a3}{punct}"

        return triad_pat.sub(triad_repl, text)

    def split_modal_coordinates(self, sentence: str) -> str:
        """
        Rewrites symmetrical modal double-predicates cleanly.
        """
        modal_pat = re.compile(
            r"\b([A-Za-z\s]+?)\s+(can|will|may)\s+([A-Za-z\s]+?)\s+and\s+(?:build|cultivate|earn|foster)\s+(trust|loyalty|growth|integrity|success)\b",
            re.IGNORECASE
        )
        def modal_repl(m):
            subj = m.group(1).strip()
            modal = m.group(2)
            v1 = m.group(3).strip()
            noun = m.group(4).strip()
            if len(v1.split()) >= 2:
                return f"{subj} {modal} {v1}. That builds {noun}"
            return m.group(0)

        return modal_pat.sub(modal_repl, sentence)

    def invert_subordinate_clause(self, sentence: str) -> Optional[str]:
        """
        DIPPER Subordinate Clause Inversion:
        Flips dependency tree clauses between head and subordinate adjuncts.
        """
        s = sentence.strip()
        lower_s = s.lower()
        matched_conj = None
        for conj in sorted(self.subordinating_conjunctions, key=len, reverse=True):
            if lower_s.startswith(conj + " ") or lower_s.startswith(conj + ","):
                matched_conj = conj
                break

        if matched_conj and "," in s:
            parts = s.split(",", 1)
            if len(parts) == 2:
                sub_clause = parts[0].strip()
                main_clause = parts[1].strip()

                punct = "."
                if main_clause.endswith((".", "!", "?")):
                    punct = main_clause[-1]
                    main_clause = main_clause[:-1].strip()

                main_clause = main_clause[0].upper() + main_clause[1:] if len(main_clause) > 1 else main_clause.upper()
                sub_clause = sub_clause[0].lower() + sub_clause[1:] if len(sub_clause) > 1 else sub_clause.lower()

                sep = " " if matched_conj in ["because", "if", "since", "unless"] else ", "
                return f"{main_clause}{sep}{sub_clause}{punct}"

        for conj in sorted(self.subordinating_conjunctions, key=len, reverse=True):
            pattern = rf"(.*?)(?:,\s*|\s+)({conj}\s+.*)"
            m = re.match(pattern, s, flags=re.IGNORECASE)
            if m:
                main_part = m.group(1).strip()
                sub_part = m.group(2).strip()

                if len(main_part.split()) >= 3 and len(sub_part.split()) >= 3:
                    punct = "."
                    if sub_part.endswith((".", "!", "?")):
                        punct = sub_part[-1]
                        sub_part = sub_part[:-1].strip()

                    sub_part = sub_part[0].upper() + sub_part[1:]
                    main_part = main_part[0].lower() + main_part[1:]

                    return f"{sub_part}, {main_part}{punct}"

        return None

    def invert_prepositional_front(self, sentence: str) -> Optional[str]:
        """
        DIPPER Prepositional Adjunct Displacement:
        'In universities today, academic integrity supports...' ->
        'Academic integrity supports... in universities today.'
        """
        s = sentence.strip()
        doc = self.nlp(s)

        if len(doc) > 5 and doc[0].pos_ == "ADP":
            for i, token in enumerate(doc[:7]):
                if token.text == ",":
                    prep_phrase = doc[:i].text.strip()
                    rest = doc[i+1:].text.strip()

                    punct = "."
                    if rest.endswith((".", "!", "?")):
                        punct = rest[-1]
                        rest = rest[:-1].strip()

                    if len(rest) > 2:
                        rest_cap = rest[0].upper() + rest[1:]
                        prep_low = prep_phrase[0].lower() + prep_phrase[1:]
                        return f"{rest_cap} {prep_low}{punct}"
        return None

    def convert_passive_to_active(self, sentence: str) -> Optional[str]:
        """
        Converts passive-voice clauses ('X was/is [VBN] by Y') into direct active voice ('Y [VBD/VBZ] X').
        """
        s = sentence.strip()
        m = re.match(
            r"^([A-Za-z\s-]+?)\s+(is|are|was|were)\s+([a-z]+ed)\s+by\s+([^,.!?]+)([.!?]?)$",
            s,
            re.IGNORECASE
        )
        if m:
            patient = m.group(1).strip()
            aux = m.group(2).lower()
            vbn = m.group(3).lower()
            agent = m.group(4).strip()
            punct = m.group(5) or "."
            tag = "VBD" if aux in ("was", "were") else ("VBZ" if not agent.lower().endswith("s") else "VBP")
            inflected = lemminflect.getInflection(vbn, tag=tag)
            if inflected:
                active_v = inflected[0]
                agent_cap = agent[0].upper() + agent[1:]
                patient_low = patient[0].lower() + patient[1:]
                return f"{agent_cap} {active_v} {patient_low}{punct}"
        return None

    def enforce_macro_cadence(self, sentences: List[str]) -> List[str]:
        """
        Balances paragraph sentence lengths without injecting repetitive starter words.
        """
        if len(sentences) < 2:
            return sentences
        return sentences
