import os
import json
import re
from typing import Dict, List, Tuple, Optional

class DatasetManager:
    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        self.data_dir = data_dir
        
        # Load 10 Core Linguistic Datasets
        self.ppdb_entries = self._load_json("ppdb_phrasal.json").get("phrasal_paraphrases", [])
        self.academic_words = self._load_json("academic_word_list.json").get("academic_substitutions", {})
        self.simplifications = self._load_json("simplification_corpus.json").get("simplifications", {})
        self.transitions = self._load_json("transitions_catalog.json")
        contractions_data = self._load_json("contractions.json")
        self.contractions_expand = contractions_data.get("expand", {})
        self.contractions_contract = contractions_data.get("contract", {})
        
        # Newly Added Linguistic Corpora
        self.pleonasms = self._load_json("pleonasms.json").get("pleonasms", {})
        self.collocations = self._load_json("collocations.json").get("academic_collocations", {})
        self.vivid_verbs = self._load_json("vivid_verbs.json").get("vivid_verbs", {})
        self.hedging_markers = self._load_json("hedging_markers.json").get("hedging_substitutions", {})
        self.ai_cliches = self._load_json("ai_cliches.json").get("multi_word_cliches", {})

        # Precompile PPDB regex patterns
        self.ppdb_patterns: List[Tuple[re.Pattern, Dict[str, str]]] = []
        for item in self.ppdb_entries:
            src = item["source"]
            pattern = re.compile(rf"\b{re.escape(src)}\b", re.IGNORECASE)
            self.ppdb_patterns.append((pattern, item))

        # Precompile Pleonasm patterns
        self.pleonasm_patterns: List[Tuple[re.Pattern, str]] = [
            (re.compile(rf"\b{re.escape(k)}\b", re.IGNORECASE), v)
            for k, v in self.pleonasms.items()
        ]

        # Precompile Collocation patterns
        self.collocation_patterns: List[Tuple[re.Pattern, str]] = [
            (re.compile(rf"\b{re.escape(k)}\b", re.IGNORECASE), v)
            for k, v in self.collocations.items()
        ]

        # Precompile Vivid Verb patterns
        self.vivid_verb_patterns: List[Tuple[re.Pattern, str]] = [
            (re.compile(rf"\b{re.escape(k)}\b", re.IGNORECASE), v)
            for k, v in self.vivid_verbs.items()
        ]

        # Precompile Hedging patterns
        self.hedging_patterns: List[Tuple[re.Pattern, str]] = [
            (re.compile(rf"\b{re.escape(k)}\b", re.IGNORECASE), v)
            for k, v in self.hedging_markers.items()
        ]

        # Precompile AI Cliché patterns
        self.ai_cliche_patterns: List[Tuple[re.Pattern, str]] = [
            (re.compile(rf"\b{re.escape(k)}\b", re.IGNORECASE), v)
            for k, v in self.ai_cliches.items()
        ]

    def _load_json(self, filename: str) -> dict:
        filepath = os.path.join(self.data_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def apply_phrasal_transforms(self, text: str, mode: str = "standard") -> str:
        """Transforms multi-word idioms and phrases using PPDB database mappings."""
        res = text
        for pattern, mapping in self.ppdb_patterns:
            target = mapping.get(mode) or mapping.get("standard") or mapping.get("formal")
            if not target:
                continue

            def replacer(match, rep=target):
                orig = match.group(0)
                if orig[0].isupper() and len(rep) > 1:
                    return rep[0].upper() + rep[1:]
                return rep

            res = pattern.sub(replacer, res)
        return res

    def apply_academic_elevation(self, text: str) -> str:
        """Elevates vocabulary using Coxhead's Academic Word List."""
        words = text.split()
        out = []
        for w in words:
            clean = re.sub(r"[^\w-]", "", w).lower()
            if clean in self.academic_words:
                rep = self.academic_words[clean]
                if w[0].isupper() and len(rep) > 1:
                    rep = rep[0].upper() + rep[1:]
                p_before = re.match(r"^[^\w]*", w).group(0)
                p_after = re.search(r"[^\w]*$", w).group(0)
                out.append(f"{p_before}{rep}{p_after}")
            else:
                out.append(w)
        return " ".join(out)

    def apply_simplifications(self, text: str) -> str:
        """Converts corporate jargon and complex terms to Plain English."""
        words = text.split()
        out = []
        for w in words:
            clean = re.sub(r"[^\w-]", "", w).lower()
            if clean in self.simplifications:
                rep = self.simplifications[clean]
                if w[0].isupper() and len(rep) > 1:
                    rep = rep[0].upper() + rep[1:]
                p_before = re.match(r"^[^\w]*", w).group(0)
                p_after = re.search(r"[^\w]*$", w).group(0)
                out.append(f"{p_before}{rep}{p_after}")
            else:
                out.append(w)
        return " ".join(out)

    def apply_pleonasm_reduction(self, text: str) -> str:
        """Removes tautologies, redundancies, and pleonasms (e.g. 'future plans' -> 'plans')."""
        res = text
        for pattern, rep in self.pleonasm_patterns:
            def replacer(match, target=rep):
                orig = match.group(0)
                if orig[0].isupper() and len(target) > 1:
                    return target[0].upper() + target[1:]
                return target
            res = pattern.sub(replacer, res)
        return res

    def apply_collocations(self, text: str) -> str:
        """Corrects unnatural verb-noun or adjective-noun pairings using authentic human collocations."""
        res = text
        for pattern, rep in self.collocation_patterns:
            def replacer(match, target=rep):
                orig = match.group(0)
                if orig[0].isupper() and len(target) > 1:
                    return target[0].upper() + target[1:]
                return target
            res = pattern.sub(replacer, res)
        return res

    def apply_vivid_verbs(self, text: str) -> str:
        """Replaces weak copular combinations and phrasal verbs with vivid verbs."""
        res = text
        for pattern, rep in self.vivid_verb_patterns:
            def replacer(match, target=rep):
                orig = match.group(0)
                if orig[0].isupper() and len(target) > 1:
                    return target[0].upper() + target[1:]
                return target
            res = pattern.sub(replacer, res)
        return res

    def apply_hedging(self, text: str) -> str:
        """Substitutes overconfident claims with scholarly epistemic modal qualifiers."""
        res = text
        for pattern, rep in self.hedging_patterns:
            def replacer(match, target=rep):
                orig = match.group(0)
                if orig[0].isupper() and len(target) > 1:
                    return target[0].upper() + target[1:]
                return target
            res = pattern.sub(replacer, res)
        return res

    def apply_ai_cliche_removal(self, text: str) -> str:
        """Replaces multi-word synthetic boilerplates with clean, authentic human phrasing."""
        res = text
        for pattern, rep in self.ai_cliche_patterns:
            def replacer(match, target=rep):
                orig = match.group(0)
                if orig[0].isupper() and len(target) > 1:
                    return target[0].upper() + target[1:]
                return target
            res = pattern.sub(replacer, res)
        return res

    def adjust_contractions(self, text: str, expand: bool = True) -> str:
        """Expands contractions for Formal/Academic mode, or contracts them for Casual/Simple."""
        mapping = self.contractions_expand if expand else self.contractions_contract
        res = text
        for k, v in mapping.items():
            pattern = re.compile(rf"\b{re.escape(k)}\b", re.IGNORECASE)
            def replacer(match, target=v):
                orig = match.group(0)
                if orig[0].isupper() and len(target) > 1:
                    return target[0].upper() + target[1:]
                return target
            res = pattern.sub(replacer, res)
        return res

    def get_transition(self, category: str = "consequence", index: int = 0) -> str:
        """Retrieves a discourse transition marker."""
        options = self.transitions.get(category, [])
        if not options:
            return ""
        return options[index % len(options)]
