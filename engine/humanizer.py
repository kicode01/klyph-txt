"""
Unified Deep Adversarial Neurosymbolic Humanizer Engine (v5.0 - Structural & Context-Aware Edition).
Implements all 26 structural editing rules from Wikipedia's 'Signs of AI Writing' (SKILL.md)
combined with DIPPER syntactic AST reordering and CoPA collocation de-inflation.
"""
import re
import spacy
from typing import List, Dict, Any, Optional
from .adversarial_lexicon import (
    TIER_1_DEAD_GIVEAWAYS,
    TIER_2_FORMULAIC_CONNECTORS,
    TIER_3_LATINATE_INFLATION,
    TIER_4_CORPORATE_JARGON,
    TIER_5_CHATBOT_PHRASES,
    TIER_6_SIGNIFICANCE_INFLATION,
    TIER_7_METAPHORS,
)
from .syntactic_mutator import SyntacticMutator
from .metrics import calculate_ai_detection_profile, calculate_burstiness
from .argon_rewriter import ArgonSemanticRewriter


class HumanizerEngine:
    def __init__(self, nlp: Optional[spacy.language.Language] = None):
        self.nlp = nlp if nlp is not None else spacy.load("en_core_web_sm")
        self.mutator = SyntacticMutator(self.nlp)
        self.argon = ArgonSemanticRewriter(model="gemini-4-argon")

        # Build unified lookup dictionaries
        self.tier1_set = set(k.lower() for k in TIER_1_DEAD_GIVEAWAYS)
        self.tier2_set = set(k.lower() for k in TIER_2_FORMULAIC_CONNECTORS)
        self.tier3_set = set(k.lower() for k in TIER_3_LATINATE_INFLATION)
        self.tier4_set = set(k.lower() for k in TIER_4_CORPORATE_JARGON)

        # Unified Anglo-Saxon replacement dictionary
        self.anglo_saxon_map: Dict[str, str] = {}
        self.anglo_saxon_map.update(TIER_1_DEAD_GIVEAWAYS)
        self.anglo_saxon_map.update(TIER_2_FORMULAIC_CONNECTORS)
        self.anglo_saxon_map.update(TIER_3_LATINATE_INFLATION)
        self.anglo_saxon_map.update(TIER_4_CORPORATE_JARGON)

        # Structural pattern scanners (SKILL.md §1, §8, §15)
        self.structural_scanners = [
            (
                re.compile(r"\bit(?:'s| is) not (?:just|only|merely) (?:about )?[^,]+,\s*(?:but|rather|it's|it is)\s+[^.!?]+", re.I),
                "Stage-setting 'Not X, but Y' contrast (§1)"
            ),
            (
                re.compile(r",\s+(?:offering|highlighting|underscoring|emphasizing|ensuring|reflecting|symbolizing|fostering|encompassing|showcasing)\s+[^.!?]+", re.I),
                "Shallow trailing '-ing' participial rider (§15)"
            ),
            (
                re.compile(r"\bby\s+[a-z-]+ing\s+[^,]+,\s+[a-z\s]+?\s+(?:can|will|may)\s+", re.I),
                "Formulaic 'By [verb]-ing..., [subject] can...' template"
            ),
            (
                re.compile(r"\s(?:[—–]|--)\s"),
                "Overused dash connector (§8)"
            ),
        ]

    def scan(self, text: str) -> Dict[str, Any]:
        """
        Comprehensive Multi-Tier & Structural AI Scan across all 7 Lexical Tiers + Structural Patterns.
        """
        if not text or not text.strip():
            return {
                "ai_score": 0.0,
                "tier1_count": 0,
                "tier2_count": 0,
                "tier3_count": 0,
                "tier4_count": 0,
                "phrases_count": 0,
                "structural_count": 0,
                "total_detections": 0,
                "findings": [],
                "clean_text": text
            }

        findings = []
        words = re.findall(r"\b[A-Za-z'-]+\b", text)
        total_words = max(len(words), 1)

        # 1. Scan Structural Tells (SKILL.md §1, §8, §15)
        for pattern, desc in self.structural_scanners:
            for match in pattern.finditer(text):
                findings.append({
                    "start": match.start(),
                    "end": match.end(),
                    "match": match.group(0).strip(),
                    "replacement": "Direct clause rewrite",
                    "tier": "Structural Tell (Syntax)",
                    "category": "AI Sentence Skeleton",
                    "description": desc
                })

        # 2. Scan Phrasal Collocations (Tiers 5, 6, 7)
        for pattern, replacement, desc in TIER_5_CHATBOT_PHRASES:
            for match in pattern.finditer(text):
                findings.append({
                    "start": match.start(),
                    "end": match.end(),
                    "match": match.group(0),
                    "replacement": replacement,
                    "tier": "Tier 5 (Chatbot / Opener Artifact)",
                    "category": "Discourse Tell",
                    "description": desc
                })

        for pattern, replacement, desc in TIER_6_SIGNIFICANCE_INFLATION:
            for match in pattern.finditer(text):
                findings.append({
                    "start": match.start(),
                    "end": match.end(),
                    "match": match.group(0),
                    "replacement": replacement,
                    "tier": "Tier 6 (Significance Inflation)",
                    "category": "Formulaic Collocation",
                    "description": desc
                })

        for pattern, replacement, desc in TIER_7_METAPHORS:
            for match in pattern.finditer(text):
                findings.append({
                    "start": match.start(),
                    "end": match.end(),
                    "match": match.group(0),
                    "replacement": replacement,
                    "tier": "Tier 7 (Cliché Metaphor)",
                    "category": "AI Hallmarked Metaphor",
                    "description": desc
                })

        # 3. Scan Vocabulary Tiers (Tiers 1, 2, 3, 4)
        for match in re.finditer(r"\b[A-Za-z'-]+\b", text):
            w_lower = match.group(0).lower()
            if w_lower in self.tier1_set:
                rep = self.anglo_saxon_map.get(w_lower, "simpler word")
                findings.append({
                    "start": match.start(),
                    "end": match.end(),
                    "match": match.group(0),
                    "replacement": rep,
                    "tier": "Tier 1 (Dead Giveaway)",
                    "category": "High-Frequency AI Tell",
                    "description": f"AI hallmark '{match.group(0)}'. Humans prefer '{rep}'."
                })
            elif w_lower in self.tier2_set:
                rep = self.anglo_saxon_map.get(w_lower, "")
                findings.append({
                    "start": match.start(),
                    "end": match.end(),
                    "match": match.group(0),
                    "replacement": rep,
                    "tier": "Tier 2 (Formulaic Connector)",
                    "category": "Overused Transition",
                    "description": f"Formulaic transition: '{match.group(0)}'."
                })
            elif w_lower in self.tier3_set:
                rep = self.anglo_saxon_map.get(w_lower, "simpler root")
                findings.append({
                    "start": match.start(),
                    "end": match.end(),
                    "match": match.group(0),
                    "replacement": rep,
                    "tier": "Tier 3 (Latinate Inflation)",
                    "category": "Abstract Nominalization",
                    "description": f"Pretentious Latinate: '{match.group(0)}'. Use direct '{rep}'."
                })
            elif w_lower in self.tier4_set:
                rep = self.anglo_saxon_map.get(w_lower, "plain term")
                findings.append({
                    "start": match.start(),
                    "end": match.end(),
                    "match": match.group(0),
                    "replacement": rep,
                    "tier": "Tier 4 (Corporate Buzzword)",
                    "category": "Corporate Inflation",
                    "description": f"Corporate buzzword: '{match.group(0)}'."
                })

        tier1_count = sum(1 for f in findings if "Tier 1" in f["tier"])
        tier2_count = sum(1 for f in findings if "Tier 2" in f["tier"])
        tier3_count = sum(1 for f in findings if "Tier 3" in f["tier"])
        tier4_count = sum(1 for f in findings if "Tier 4" in f["tier"])
        phrases_count = sum(1 for f in findings if any(t in f["tier"] for t in ["Tier 5", "Tier 6", "Tier 7"]))
        structural_count = sum(1 for f in findings if "Structural" in f["tier"])

        score = min(
            100.0,
            round(
                (
                    (tier1_count * 15.0)
                    + (tier2_count * 5.0)
                    + (tier3_count * 8.0)
                    + (tier4_count * 6.0)
                    + (phrases_count * 12.0)
                    + (structural_count * 14.0)
                )
                / (total_words / 50.0),
                1
            )
        )

        return {
            "ai_score": score,
            "total_words": total_words,
            "tier1_count": tier1_count,
            "tier2_count": tier2_count,
            "tier3_count": tier3_count,
            "tier4_count": tier4_count,
            "phrases_count": phrases_count,
            "structural_count": structural_count,
            "total_detections": len(findings),
            "findings": findings
        }

    def _apply_phrasal_collocations(self, text: str) -> str:
        """Applies context-aware phrase and collocation replacements (Tiers 5, 6, 7)."""
        res = text
        for pat, rep, _ in TIER_5_CHATBOT_PHRASES:
            res = pat.sub(rep, res)
        for pat, rep, _ in TIER_6_SIGNIFICANCE_INFLATION:
            res = pat.sub(rep, res)
        for pat, rep, _ in TIER_7_METAPHORS:
            res = pat.sub(rep, res)
        res = re.sub(r"\s*(?:ultimately|in conclusion|all in all|in summary|to sum up),\s*", " ", res, flags=re.I)
        return res.strip()

    def _clean_wikipedia_tells(self, text: str) -> str:
        """
        Eradicates Wikipedia's 'Signs of AI writing' (SKILL.md §1 Not X but Y, §6 Triads, §8 Dashes).
        """
        res = text

        # 1. SKILL.md §1: 'Not X, but Y' -> State the positive point directly or use 'Beyond X, the goal is Y'
        def not_x_repl(m):
            x = m.group(1).strip()
            y = m.group(2).strip()
            return f"Beyond {x}, the focus is {y}"

        res = re.sub(
            r"\bit(?:'s| is) not (?:just|only|merely) about ([^,]+),\s*(?:but rather|but|rather)\s+([^.!?]+)",
            not_x_repl,
            res,
            flags=re.I
        )
        res = re.sub(
            r"\bit(?:'s| is) not (?:just|only|merely)\s+([^,]+),\s*(?:but rather|but|rather)\s+([^.!?]+)",
            lambda m: m.group(2).strip()[0].upper() + m.group(2).strip()[1:],
            res,
            flags=re.I
        )

        # 2. SKILL.md §8: Strip em-dashes and en-dashes
        res = self.mutator.strip_em_dashes(res)

        # 3. SKILL.md §6: Action Triads & Modal Coordinates
        res = self.mutator.split_action_triads(res)
        res = self.mutator.split_modal_coordinates(res)

        # 4. Forced Noun Triads ('A, B, and C' -> 'A and C')
        res = re.sub(
            r"\b(\w+ing|\w+tion|\w+ity|\w+ness),\s+(\w+ing|\w+tion|\w+ity|\w+ness),\s+and\s+(\w+ing|\w+tion|\w+ity|\w+ness)\b",
            r"\1 and \3",
            res,
            flags=re.I
        )

        return res

    def _apply_anglo_saxon_shift(self, text: str, intensity: float = 1.0) -> str:
        """Applies context-safe Anglo-Saxon Kernel Shift across Tiers 1-4."""
        res = text
        # Sort longest keys first so multi-word entries match before substrings
        for latinate in sorted(self.anglo_saxon_map.keys(), key=len, reverse=True):
            anglo = self.anglo_saxon_map[latinate]
            pattern = re.compile(rf"\b{re.escape(latinate)}\b", re.IGNORECASE)
            def repl(m, target=anglo):
                orig = m.group(0)
                if orig[0].isupper() and len(target) > 1:
                    return target[0].upper() + target[1:]
                return target
            res = pattern.sub(repl, res)
        return res

    def _apply_ast_order_diversity(
        self,
        text: str,
        order_diversity: float = 0.6,
        variant: int = 0
    ) -> str:
        """
        DIPPER Order Diversity & Structural Deconstruction (Multi-Variant Beam Generator):
        - Variant 0: Balanced AST deconstruction (Eliminate -ing riders, rewrite 'By...' openers, coordinate split, prep front)
        - Variant 1: High-Burstiness Clause Inversion (Subordinate clause inversion on all eligible sentences + coordinate split)
        - Variant 2: Active Voice & Topological Fronting (Passive-to-active voice conversion + prepositional fronting)
        """
        doc = self.nlp(text)
        raw_sents = [s.text.strip() for s in doc.sents if s.text.strip()]
        processed_sents = []

        for i, s in enumerate(raw_sents):
            # 1. Eliminate trailing '-ing' riders (SKILL.md §15)
            s = self.mutator.eliminate_ing_riders(s)

            # 2. Rewrite 'By [verb]-ing..., [subject] can...' templates
            s = self.mutator.rewrite_by_gerund_opener(s)

            # Variant-specific syntactic transformations
            if variant == 1:
                # High-Burstiness: split relative '... decisions that reach ...' or '... tools lets ...'
                s = re.sub(
                    r"\b(decisions|solutions|systems|strategies)\s+that\s+([a-z]+\s+[^.!?]+)([.!?]?)$",
                    lambda m: f"{m.group(1)}. They {m.group(2)}{m.group(3) or '.'}",
                    s,
                    flags=re.I
                )
            elif variant == 2:
                # Direct & Concise: strip transitional throat-clearing adverbs & convert passive voice
                s = re.sub(r"^(?:Also|Besides|Still|In fact),\s+", "", s, flags=re.I)
                if s:
                    s = s[0].upper() + s[1:]
                act = self.mutator.convert_passive_to_active(s)
                if act:
                    s = act

            # 3. Coordinate clause splitting
            if order_diversity >= 0.35:
                split_parts = self.mutator.split_coordinate_clauses(s)
                if len(split_parts) > 1:
                    processed_sents.extend(split_parts)
                    continue

            # 4. Subordinate clause inversion
            if order_diversity >= 0.45:
                inv = self.mutator.invert_subordinate_clause(s)
                if inv and (variant == 1 or i % 2 == 1):
                    processed_sents.append(inv)
                    continue

            # 5. Prepositional front inversion (only on Variant 0 and Variant 2)
            if order_diversity >= 0.3 and variant in (0, 2):
                prep_inv = self.mutator.invert_prepositional_front(s)
                if prep_inv:
                    processed_sents.append(prep_inv)
                    continue

            processed_sents.append(s)

        return " ".join(processed_sents)

    def _optimize_rhythm_and_burstiness(self, text: str) -> str:
        """
        Ensures asymmetric sentence lengths without injecting repetitive starter words.
        """
        doc = self.nlp(text)
        sents = [s.text.strip() for s in doc.sents if s.text.strip()]
        if len(sents) < 2:
            return text

        burst = calculate_burstiness(" ".join(sents))
        if burst < 4.0:
            new_sents = []
            modified = False
            for s in sents:
                if len(s.split()) >= 16 and not modified:
                    split_parts = self.mutator.split_coordinate_clauses(s)
                    if len(split_parts) > 1:
                        new_sents.extend(split_parts)
                        modified = True
                        continue
                new_sents.append(s)
            sents = new_sents

        res = " ".join(sents)
        res = re.sub(r"\s{2,}", " ", res)
        res = re.sub(r"\s+([.,!?;:])", r"\1", res)
        return res.strip()

    def _finalize_sentences(self, candidate: str) -> str:
        doc = self.nlp(candidate)
        capitalized = []
        for s in doc.sents:
            st = s.text.strip()
            if st:
                st = st[0].upper() + st[1:] if len(st) > 1 else st.upper()
                capitalized.append(st)

        out = " ".join(capitalized).strip()
        out = re.sub(r"\s{2,}", " ", out)
        out = re.sub(r"\s+([.,!?;:])", r"\1", out)
        return out

    def _generate_candidate_variant(
        self,
        text: str,
        order_diversity: float = 0.6,
        lex_diversity: float = 0.6,
        use_contractions: bool = True,
        variant: int = 0
    ) -> str:
        t1 = self._apply_phrasal_collocations(text)
        t2 = self._apply_anglo_saxon_shift(t1, intensity=lex_diversity)
        t3 = self._clean_wikipedia_tells(t2)
        if use_contractions:
            t3 = self.mutator.inject_contractions(t3)
        t4 = self._apply_ast_order_diversity(t3, order_diversity=order_diversity, variant=variant)
        t5 = self._clean_wikipedia_tells(t4)
        t6 = self._optimize_rhythm_and_burstiness(t5)
        return self._finalize_sentences(t6)

    def humanize_beam(
        self,
        text: str,
        order_diversity: float = 0.6,
        lex_diversity: float = 0.6,
        use_contractions: bool = True,
        api_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Closed-Loop Adversarial Beam Search (v6.0 Argon Neurosymbolic Edition):
        Generates multiple structural & syntactic candidates (plus optional Hybrid Gemini 4 Argon
        deep semantic rewrite when GEMINI_API_KEY is available), scores every candidate against
        the multi-signal AI detector, and selects the lowest-risk, highest-burstiness tree.
        """
        if not text or not text.strip():
            return {
                "best_text": text,
                "engine_mode": "local_ast_beam",
                "candidates": []
            }

        beam_specs = [
            ("AST Structural & Collocation De-Inflation", order_diversity, lex_diversity, True, 0),
            ("High-Burstiness Clause Transposition", max(0.85, order_diversity), max(0.85, lex_diversity), True, 1),
            ("Active Voice & Topological Fronting", 0.95, 1.0, False, 2),
        ]

        candidates = []
        seen_texts = set()

        # Optional Candidate 0: Hybrid Gemini 4 Argon Deep Semantic Rewrite + Local AST Verifier
        engine_mode = "local_adversarial_beam_v6"
        if self.argon.is_available(api_key=api_key):
            argon_raw = self.argon.rewrite(text, api_key=api_key)
            if argon_raw:
                argon_verified = self._generate_candidate_variant(
                    argon_raw, order_diversity=0.6, lex_diversity=0.8, use_contractions=use_contractions, variant=0
                )
                prof = calculate_ai_detection_profile(argon_verified)
                fitness = (
                    (100.0 - prof["ai_probability"])
                    + min(18.0, prof["burstiness_score"] * 2.5)
                    - (prof.get("lexical_tells", 0) * 15.0)
                    - (prof.get("structural_tells", 0) * 20.0)
                    + 5.0  # Semantic coherence bonus for verified Argon rewrite
                )
                candidates.append({
                    "label": "Gemini 4 Argon Deep Semantic + AST Verifier",
                    "strategy": "argon_hybrid_verified",
                    "text": argon_verified,
                    "ai_probability": prof["ai_probability"],
                    "human_probability": prof["human_probability"],
                    "burstiness_score": prof["burstiness_score"],
                    "fitness": round(fitness, 2),
                    "profile": prof
                })
                seen_texts.add(argon_verified)
                engine_mode = "hybrid_gemini_4_argon_v6"

        # Local Neurosymbolic Beam Search Candidates
        for label, o_div, l_div, contract, var_idx in beam_specs:
            cand_text = self._generate_candidate_variant(
                text,
                order_diversity=o_div,
                lex_diversity=l_div,
                use_contractions=contract if use_contractions else False,
                variant=var_idx
            )
            if cand_text in seen_texts and len(candidates) > 0:
                continue
            seen_texts.add(cand_text)
            prof = calculate_ai_detection_profile(cand_text)
            fitness = (
                (100.0 - prof["ai_probability"])
                + min(18.0, prof["burstiness_score"] * 2.5)
                - (prof.get("lexical_tells", 0) * 15.0)
                - (prof.get("structural_tells", 0) * 20.0)
            )
            candidates.append({
                "label": label,
                "strategy": f"ast_beam_v{var_idx}",
                "text": cand_text,
                "ai_probability": prof["ai_probability"],
                "human_probability": prof["human_probability"],
                "burstiness_score": prof["burstiness_score"],
                "fitness": round(fitness, 2),
                "profile": prof
            })

        # Rank candidates by highest adversarial fitness (lowest AI risk + highest burstiness)
        candidates.sort(key=lambda c: c["fitness"], reverse=True)
        best = candidates[0] if candidates else {
            "text": text,
            "profile": calculate_ai_detection_profile(text)
        }

        return {
            "best_text": best["text"],
            "best_profile": best["profile"],
            "engine_mode": engine_mode,
            "candidates": candidates
        }

    def humanize(
        self,
        text: str,
        order_diversity: float = 0.6,
        lex_diversity: float = 0.6,
        use_contractions: bool = True,
        adversarial_passes: int = 3,
        api_key: Optional[str] = None
    ) -> str:
        """
        Master Structural & Lexical De-AI Pipeline (v6.0 Closed-Loop Beam Search).
        """
        if not text or not text.strip():
            return text
        beam_result = self.humanize_beam(
            text,
            order_diversity=order_diversity,
            lex_diversity=lex_diversity,
            use_contractions=use_contractions,
            api_key=api_key
        )
        return beam_result["best_text"]
