import re
from typing import Dict, Tuple, List

class ConcisenessEngine:
    def __init__(self):
        # High-impact fluff and nominalization patterns
        self.fluff_map: List[Tuple[re.Pattern, str]] = [
            (re.compile(r"\bdue to the fact that\b", re.IGNORECASE), "because"),
            (re.compile(r"\bin order to\b", re.IGNORECASE), "to"),
            (re.compile(r"\bat the present time\b", re.IGNORECASE), "currently"),
            (re.compile(r"\bat this point in time\b", re.IGNORECASE), "now"),
            (re.compile(r"\bin the event that\b", re.IGNORECASE), "if"),
            (re.compile(r"\bfor the purpose of\b", re.IGNORECASE), "to"),
            (re.compile(r"\bwith reference to\b", re.IGNORECASE), "regarding"),
            (re.compile(r"\bwith regard to\b", re.IGNORECASE), "about"),
            (re.compile(r"\ba large number of\b", re.IGNORECASE), "many"),
            (re.compile(r"\ba majority of\b", re.IGNORECASE), "most"),
            (re.compile(r"\ba small number of\b", re.IGNORECASE), "few"),
            (re.compile(r"\bis able to\b", re.IGNORECASE), "can"),
            (re.compile(r"\bare able to\b", re.IGNORECASE), "can"),
            (re.compile(r"\bhas the capacity to\b", re.IGNORECASE), "can"),
            (re.compile(r"\bmake a decision\b", re.IGNORECASE), "decide"),
            (re.compile(r"\bmakes a decision\b", re.IGNORECASE), "decides"),
            (re.compile(r"\bmade a decision\b", re.IGNORECASE), "decided"),
            (re.compile(r"\bconduct an investigation into\b", re.IGNORECASE), "investigate"),
            (re.compile(r"\bconducted an investigation into\b", re.IGNORECASE), "investigated"),
            (re.compile(r"\btake into consideration\b", re.IGNORECASE), "consider"),
            (re.compile(r"\btook into consideration\b", re.IGNORECASE), "considered"),
            (re.compile(r"\bgive an explanation of\b", re.IGNORECASE), "explain"),
            (re.compile(r"\bgave an explanation of\b", re.IGNORECASE), "explained"),
            (re.compile(r"\bcome to the conclusion that\b", re.IGNORECASE), "conclude that"),
            (re.compile(r"\bcame to the conclusion that\b", re.IGNORECASE), "concluded that"),
            (re.compile(r"\bhas a tendency to\b", re.IGNORECASE), "tends to"),
            (re.compile(r"\bin spite of the fact that\b", re.IGNORECASE), "although"),
            (re.compile(r"\bin close proximity to\b", re.IGNORECASE), "near"),
            (re.compile(r"\bprior to\b", re.IGNORECASE), "before"),
            (re.compile(r"\bsubsequent to\b", re.IGNORECASE), "after"),
            (re.compile(r"\buntil such time as\b", re.IGNORECASE), "until"),
            (re.compile(r"\bplay a key role in\b", re.IGNORECASE), "drive"),
            (re.compile(r"\bin a timely manner\b", re.IGNORECASE), "promptly"),
        ]

    def simplify(self, text: str) -> str:
        """Substitutes verbose and redundant phrases with clean, direct wording."""
        res = text
        for pattern, replacement in self.fluff_map:
            # Preserve capitalization of first letter if match is capitalized
            def match_replacer(match):
                orig = match.group(0)
                if orig[0].isupper():
                    return replacement[0].upper() + replacement[1:]
                return replacement

            res = pattern.sub(match_replacer, res)
        return res
