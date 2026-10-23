import spacy
from typing import Optional, List
import re

class ClauseReorderer:
    """
    Syntactic AST Dependency Transformer implementing DIPPER Order Diversity principles.
    Permutes syntactic parse trees to decouple machine expression patterns from semantic content.
    """
    def __init__(self, nlp: Optional[spacy.language.Language] = None):
        self.nlp = nlp if nlp is not None else spacy.load("en_core_web_sm")
        self.subordinating_conjunctions = {
            "although", "though", "even though", "because", "since",
            "while", "whereas", "if", "unless", "whenever", "after",
            "before", "as soon as", "despite the fact that"
        }

    def split_coordinate_clauses(self, sentence: str) -> List[str]:
        """
        Splits long composite sentences connected by coordinating conjunctions (', and', ', but', ', yet').
        Spikes human burstiness (σ >= 6.8) and introduces natural sentence-initial conjunctions
        without inserting artificial filler.
        """
        s = sentence.strip()
        doc = self.nlp(s)
        if len(doc) < 14:
            return [s]

        # Find ", and ", ", but ", ", yet " connecting two independent clauses
        for match in re.finditer(r",\s+(and|but|yet)\s+", s, re.IGNORECASE):
            part1 = s[:match.start()].strip()
            conj = match.group(1).capitalize()
            part2 = s[match.end():].strip()

            doc1 = self.nlp(part1)
            doc2 = self.nlp(part2)
            has_v1 = any(t.pos_ in ("VERB", "AUX") for t in doc1)
            has_v2 = any(t.pos_ in ("VERB", "AUX") for t in doc2)

            if has_v1 and has_v2 and len(doc1) >= 4 and len(doc2) >= 4:
                punct = "." if not part2.endswith((".", "!", "?")) else ""
                part1_clean = part1 if part1.endswith((".", "!", "?")) else part1 + "."
                return [part1_clean, f"{conj} {part2}{punct}"]

        return [s]

    def invert_subordinate_clause(self, sentence: str) -> Optional[str]:
        """
        Inverts sentences with subordinate clauses.
        Pattern 1: [Subordinate Clause], [Main Clause]. -> [Main Clause] [Subordinate Clause].
        Pattern 2: [Main Clause], [Subordinate Clause]. -> [Subordinate Clause], [Main Clause].
        """
        s = sentence.strip()
        lower_s = s.lower()
        matched_conj = None
        for conj in sorted(self.subordinating_conjunctions, key=len, reverse=True):
            if lower_s.startswith(conj + " ") or lower_s.startswith(conj + ","):
                matched_conj = conj
                break

        # Pattern 1: Starting with subordinating clause
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

        # Pattern 2: Main clause first, subordinate clause second
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
        Shifts fronted prepositional phrases:
        "In recent years, the company developed tools." -> "The company developed tools in recent years."
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
