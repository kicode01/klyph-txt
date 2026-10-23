import re
import html
from typing import List, Dict, Any, Tuple, Optional
import language_tool_python
from .schemas import (
    TextSpan,
    GrammarCheckResponse,
    SentenceGroup,
    ParagraphRewrite,
    ParagraphImprovementResponse,
    HabitInstance,
    HabitCluster
)
from .metrics import calculate_readability

class GrammarChecker:
    def __init__(self, language: str = "en-US"):
        self.language = language
        # Initialize LanguageTool server instance locally
        self._tool = language_tool_python.LanguageTool(language)
        
        # Category mapping to Grammarly UX archetypes
        self.category_map = {
            "TYPOS": "correctness",
            "CASING": "correctness",
            "GRAMMAR": "correctness",
            "PUNCTUATION": "correctness",
            "CONFUSED_WORDS": "correctness",
            "REDUNDANCY": "clarity",
            "PLAIN_ENGLISH": "clarity",
            "STYLE": "clarity",
            "COLLOCATIONS": "engagement",
            "VOCABULARY": "engagement",
            "SEMANTICS": "engagement",
            "REGISTER": "delivery",
            "GENDER_NEUTRALITY": "delivery"
        }

    def check(self, text: str) -> GrammarCheckResponse:
        """Runs the deterministic rule engine over text and returns categorized annotations,
        writing quality score, category counts, and sentence-level groups matching Grammarly UX."""
        if not text or not text.strip():
            return GrammarCheckResponse(
                text=text,
                corrected_text=text,
                total_issues=0,
                issues=[],
                readability_score=100.0,
                reading_time_seconds=0,
                quality_score=100,
                category_counts={"all": 0, "correctness": 0, "clarity": 0, "engagement": 0, "delivery": 0},
                sentence_groups=[]
            )

        matches = self._tool.check(text)
        corrected = language_tool_python.utils.correct(text, matches)
        
        issues: List[TextSpan] = []
        for m in matches:
            category_key = str(m.category).upper() if hasattr(m, 'category') else "GRAMMAR"
            category = self.category_map.get(category_key, "correctness")
            
            # Determine replacement
            replacement = m.replacements[0] if m.replacements else ""
            original_slice = text[m.offset : m.offset + m.error_length]
            
            issues.append(TextSpan(
                start=m.offset,
                end=m.offset + m.error_length,
                original=original_slice,
                replacement=replacement,
                category=category,
                rule_id=m.rule_id,
                message=m.message,
                explanation=getattr(m, 'rule_issue_type', None),
                confidence=1.0
            ))

        # Additional Conciseness & Redundancy checks via Pleonasm Corpus
        from .dataset_manager import DatasetManager
        if not hasattr(self, 'dataset_mgr'):
            self.dataset_mgr = DatasetManager()

        for pattern, rep in self.dataset_mgr.pleonasm_patterns:
            for match in pattern.finditer(text):
                start, end = match.start(), match.end()
                overlap = any(iss.start <= start < iss.end or iss.start < end <= iss.end for iss in issues)
                if not overlap:
                    orig_str = match.group(0)
                    target_rep = rep if orig_str[0].islower() else (rep[0].upper() + rep[1:] if len(rep) > 1 else rep)
                    issues.append(TextSpan(
                        start=start,
                        end=end,
                        original=orig_str,
                        replacement=target_rep,
                        category="clarity",
                        rule_id="PLEONASM_REDUNDANCY",
                        message=f"Redundancy: '{orig_str}' is redundant. Consider simplifying to '{target_rep}'.",
                        explanation="Pleonasm & Conciseness",
                        confidence=1.0
                    ))

        # Additional Verbal Fluff and Nominalization checks via ConcisenessEngine
        from .conciseness import ConcisenessEngine
        if not hasattr(self, 'conciseness_engine'):
            self.conciseness_engine = ConcisenessEngine()

        for pattern, rep in self.conciseness_engine.fluff_map:
            for match in pattern.finditer(text):
                start, end = match.start(), match.end()
                overlap = any(iss.start <= start < iss.end or iss.start < end <= iss.end for iss in issues)
                if not overlap:
                    orig_str = match.group(0)
                    target_rep = rep if orig_str[0].islower() else (rep[0].upper() + rep[1:] if len(rep) > 1 else rep)
                    is_nominalization = any(w in orig_str.lower() for w in [
                        "decision", "investigation", "consideration", "explanation", "conclusion"
                    ])
                    rule_id = "NOMINALIZATION_VERB" if is_nominalization else "PLEONASM_REDUNDANCY"
                    issues.append(TextSpan(
                        start=start,
                        end=end,
                        original=orig_str,
                        replacement=target_rep,
                        category="clarity",
                        rule_id=rule_id,
                        message=f"Conciseness: '{orig_str}' can be tightened to active '{target_rep}'.",
                        explanation="Active Verb vs. Verbal Fluff",
                        confidence=1.0
                    ))

        # Academic Demonstrative Precision (e.g. "The study" -> "This study")
        for match in re.finditer(r"\b(The\s+study|The\s+paper|The\s+research|The\s+project|The\s+report)\b", text):
            start, end = match.start(), match.end()
            orig = match.group(0)
            rep = "This " + orig.split()[1]
            overlap = any(iss.start <= start < iss.end or iss.start < end <= iss.end for iss in issues)
            if not overlap:
                issues.append(TextSpan(
                    start=start,
                    end=end,
                    original=orig,
                    replacement=rep,
                    category="clarity",
                    rule_id="DEMONSTRATIVE_SPECIFICITY",
                    message=f"Consider using '{rep}' for clearer referential focus.",
                    explanation="Demonstrative Precision",
                    confidence=1.0
                ))

        # Nominalization to Active Gerund / Verb ("the development and analysis of" -> "developing and analyzing")
        nom_rules = [
            (re.compile(r"\bthe\s+development\s+and\s+analysis\s+of\b", re.I), "developing and analyzing"),
            (re.compile(r"\bthe\s+development\s+of\b", re.I), "developing"),
            (re.compile(r"\banalysis\s+of\b", re.I), "analyzing"),
            (re.compile(r"\bthe\s+analysis\s+of\b", re.I), "analyzing"),
            (re.compile(r"\bthe\s+implementation\s+of\b", re.I), "implementing"),
            (re.compile(r"\bthe\s+creation\s+of\b", re.I), "creating"),
            (re.compile(r"\bthe\s+examination\s+of\b", re.I), "examining"),
            (re.compile(r"\bthe\s+evaluation\s+of\b", re.I), "evaluating"),
            (re.compile(r"\bthe\s+investigation\s+of\b", re.I), "investigating"),
            (re.compile(r"\bthe\s+establishment\s+of\b", re.I), "establishing"),
            (re.compile(r"\bthe\s+measurement\s+of\b", re.I), "measuring"),
        ]
        for pat, rep in nom_rules:
            for match in pat.finditer(text):
                start, end = match.start(), match.end()
                orig = match.group(0)
                overlap = any(iss.start <= start < iss.end or iss.start < end <= iss.end for iss in issues)
                if not overlap:
                    issues.append(TextSpan(
                        start=start,
                        end=end,
                        original=orig,
                        replacement=rep,
                        category="clarity",
                        rule_id="NOMINALIZATION_VERB",
                        message=f"Transform nominalization '{orig}' into active '{rep}' for directness.",
                        explanation="Active Verb vs. Nominalization",
                        confidence=1.0
                    ))

        # Coordinate Adjectives Comma Rule (e.g. "IoT-based occupancy-driven" -> "IoT-based, occupancy-driven")
        for match in re.finditer(r"\b([A-Za-z0-9]+-based)\s+([a-z]+-driven)\b", text):
            start, end = match.start(), match.end()
            part1, part2 = match.group(1), match.group(2)
            orig = match.group(0)
            rep = f"{part1}, {part2}"
            overlap = any(iss.start <= start < iss.end or iss.start < end <= iss.end for iss in issues)
            if not overlap:
                issues.append(TextSpan(
                    start=start,
                    end=end,
                    original=orig,
                    replacement=rep,
                    category="correctness",
                    rule_id="COORDINATE_ADJECTIVES_COMMA",
                    message="Add a comma between coordinate adjectives modifying the noun.",
                    explanation="Punctuation Mechanics",
                    confidence=1.0
                ))

        # Sort issues chronologically by character start offset
        issues.sort(key=lambda x: x.start)

        # Calculate category counts
        cat_counts = {
            "all": len(issues),
            "correctness": sum(1 for i in issues if i.category in ["correctness", "spelling"]),
            "clarity": sum(1 for i in issues if i.category == "clarity"),
            "engagement": sum(1 for i in issues if i.category == "engagement"),
            "delivery": sum(1 for i in issues if i.category == "delivery")
        }

        readability = calculate_readability(text)
        word_count = len(text.split())
        
        # Calculate writing quality score (0 - 100)
        penalty = (len(issues) * 11.0) / max(1.0, word_count / 30.0)
        quality_score = max(40, min(100, int(100.0 - penalty + (readability["flesch_reading_ease"] - 60) * 0.08)))
        if not text.strip():
            quality_score = 100

        # Build sentence groups with full diff html for Grammarly-style sentence rewrite cards
        sentence_groups = self._build_sentence_groups(text, issues)

        # Cluster root-cause habits for high-leverage macro fixes (Phase 3)
        habit_clusters = self._cluster_habits(text, issues)

        return GrammarCheckResponse(
            text=text,
            corrected_text=corrected,
            total_issues=len(issues),
            issues=issues,
            readability_score=readability["flesch_reading_ease"],
            reading_time_seconds=readability["reading_time_seconds"],
            quality_score=quality_score,
            category_counts=cat_counts,
            sentence_groups=sentence_groups,
            habit_clusters=habit_clusters
        )

    def _build_sentence_groups(self, text: str, issues: List[TextSpan]) -> List[SentenceGroup]:
        """Segments text into sentences and aggregates all issues per sentence into an
        interactive 'Improve your text' card with rich inline diff tokens."""
        spans = []
        # Match sentences ending with punctuation (. ! ?) or paragraph boundaries
        for m in re.finditer(r'([A-Z0-9][^.!?\n]*[.!?]+(?:\s+|$)|[^\n]+(?:\n+|$))', text):
            start, end = m.start(), m.end()
            s = text[start:end]
            if s.strip():
                spans.append((start, end, s))

        groups: List[SentenceGroup] = []
        for idx, (s_start, s_end, s_raw) in enumerate(spans):
            # Find issues belonging to this sentence
            s_issues_indices = [
                i for i, iss in enumerate(issues)
                if s_start <= iss.start < s_end
            ]
            if not s_issues_indices:
                continue

            s_issues = [issues[i] for i in s_issues_indices]

            # Generate rewritten sentence
            s_text = text[s_start:s_end]
            # Replace backwards from end to maintain character offsets
            rewritten_s = s_text
            for iss in sorted(s_issues, key=lambda x: x.start, reverse=True):
                rel_start = iss.start - s_start
                rel_end = iss.end - s_start
                if 0 <= rel_start <= len(rewritten_s) and 0 <= rel_end <= len(rewritten_s):
                    rep = iss.replacement or ""
                    rewritten_s = rewritten_s[:rel_start] + rep + rewritten_s[rel_end:]

            # Generate rich inline diff HTML for the card
            diff_parts = []
            last_idx = 0
            for iss in sorted(s_issues, key=lambda x: x.start):
                rel_start = iss.start - s_start
                rel_end = iss.end - s_start
                if rel_start > last_idx and rel_start <= len(s_text):
                    diff_parts.append(html.escape(s_text[last_idx:rel_start]))

                # Deleted token(s)
                if iss.original:
                    diff_parts.append(f'<span class="diff-del">{html.escape(iss.original)}</span>')

                # Inserted token(s)
                if iss.replacement and iss.replacement != iss.original:
                    if iss.replacement in [',', ';', ':', '-', '—']:
                        diff_parts.append(f'<span class="diff-ins-box">{html.escape(iss.replacement)}</span>')
                    else:
                        diff_parts.append(f'<span class="diff-ins">{html.escape(iss.replacement)}</span>')
                last_idx = rel_end

            if last_idx < len(s_text):
                diff_parts.append(html.escape(s_text[last_idx:]))

            diff_html = "".join(diff_parts).strip()
            
            # Snippet preview for collapsed cards
            clean_s = s_text.strip()
            preview = clean_s[:44] + ("..." if len(clean_s) > 44 else "")

            primary_category = s_issues[0].category if s_issues else "clarity"

            groups.append(SentenceGroup(
                id=idx,
                sentence_start=s_start,
                sentence_end=s_end,
                original_sentence=s_text,
                rewritten_sentence=rewritten_s,
                issues_count=len(s_issues),
                category=primary_category,
                diff_html=diff_html,
                preview=preview,
                issue_indices=s_issues_indices
            ))

        return groups

    def improve_paragraphs(self, text: str) -> ParagraphImprovementResponse:
        """Analyzes text at the macro paragraph level, consolidating sentence-level and flow fixes
        into full paragraph rewrites with before/after visual diffs."""
        if not text or not text.strip():
            return ParagraphImprovementResponse(paragraphs=[], total_paragraphs=0)

        raw_paras = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
        if not raw_paras and text.strip():
            raw_paras = [text.strip()]

        paragraphs_data: List[ParagraphRewrite] = []
        for i, p_text in enumerate(raw_paras):
            p_start = text.find(p_text)
            p_end = p_start + len(p_text) if p_start != -1 else len(p_text)

            # Run check over this paragraph
            sub_res = self.check(p_text)
            
            # Apply all actionable replacements
            rewritten = p_text
            for iss in sorted(sub_res.issues, key=lambda x: x.start, reverse=True):
                if iss.replacement and iss.replacement != iss.original:
                    rewritten = rewritten[:iss.start] + iss.replacement + rewritten[iss.end:]

            if rewritten == p_text and not sub_res.issues:
                continue

            # Simple word-level diff HTML for paragraph
            diff_html = self._build_paragraph_diff_html(p_text, rewritten)

            summary = f"{len(sub_res.issues)} precision enhancements applied to optimize flow and conciseness."

            paragraphs_data.append(ParagraphRewrite(
                id=i,
                start=max(0, p_start),
                end=p_end,
                original=p_text,
                rewritten=rewritten,
                diff_html=diff_html,
                issues_addressed=len(sub_res.issues),
                improvement_summary=summary
            ))

        return ParagraphImprovementResponse(
            paragraphs=paragraphs_data,
            total_paragraphs=len(paragraphs_data)
        )

    def _build_paragraph_diff_html(self, original: str, rewritten: str) -> str:
        """Constructs a clean word-level diff between original and rewritten paragraphs."""
        import difflib
        s1 = original.split()
        s2 = rewritten.split()
        matcher = difflib.SequenceMatcher(None, s1, s2)
        out = []
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                out.append(html.escape(" ".join(s1[i1:i2])))
            elif tag == 'delete':
                out.append(f'<span class="diff-del">{html.escape(" ".join(s1[i1:i2]))}</span>')
            elif tag == 'insert':
                out.append(f'<span class="diff-ins">{html.escape(" ".join(s2[j1:j2]))}</span>')
            elif tag == 'replace':
                out.append(f'<span class="diff-del">{html.escape(" ".join(s1[i1:i2]))}</span> <span class="diff-ins">{html.escape(" ".join(s2[j1:j2]))}</span>')
        return " ".join(out)

    def _cluster_habits(self, text: str, issues: List[TextSpan]) -> List[HabitCluster]:
        """Clusters individual issues into high-leverage stylistic and grammatical habits,
        providing educational context and single-click macro batch replacements."""
        clusters_map: Dict[str, Dict[str, Any]] = {
            "smothered_verbs": {
                "title": "Smothered Verbs (Nominalizations)",
                "category": "Clarity",
                "explanation": "Abstract nouns formed from verbs (nominalizations like 'decision' or 'investigation') cause verb drag. Converting them to direct active verbs creates immediate momentum.",
                "penalty_weight": 4,
                "matcher": lambda iss: (
                    iss.rule_id == "NOMINALIZATION_VERB" or
                    any(kw in iss.original.lower() for kw in [
                        "decision", "investigation", "consideration", "explanation", "conclusion",
                        "development", "analysis", "implementation", "creation", "examination",
                        "evaluation", "establishment", "measurement"
                    ])
                )
            },
            "pleonasms": {
                "title": "Pleonastic Padding & Wordiness",
                "category": "Clarity",
                "explanation": "Circumlocutions and redundant phrases inflate sentence length without conveying extra meaning. Pruning them sharpens reading speed.",
                "penalty_weight": 3,
                "matcher": lambda iss: (
                    iss.rule_id == "PLEONASM_REDUNDANCY" or
                    any(kw in iss.original.lower() for kw in [
                        "in order to", "due to the fact that", "at the present time", "at this point in time",
                        "in the event that", "for the purpose of", "with reference to", "with regard to",
                        "a large number of", "a majority of", "a small number of", "has the capacity to",
                        "has a tendency to", "in spite of the fact that", "in close proximity to",
                        "until such time as", "prior to", "subsequent to", "in a timely manner",
                        "advance planning", "end result", "close proximity", "future plans", "past history"
                    ])
                )
            },
            "demonstrative_precision": {
                "title": "Vague Referents & Context Anchoring",
                "category": "Clarity",
                "explanation": "Generic definite articles ('The study') create referential ambiguity in academic discourse. Anchoring them with precise demonstratives ('This study') clarifies scope.",
                "penalty_weight": 2,
                "matcher": lambda iss: (
                    iss.rule_id == "DEMONSTRATIVE_SPECIFICITY" or
                    (iss.original.lower().startswith("the ") and iss.replacement.lower().startswith("this "))
                )
            },
            "agreement_mechanics": {
                "title": "Subject-Verb & Inflection Discord",
                "category": "Correctness",
                "explanation": "Disagreements in grammatical person, number, or tense between subjects and predicates weaken structural authority. Aligning inflections restores clarity.",
                "penalty_weight": 5,
                "matcher": lambda iss: (
                    iss.category in ["correctness", "spelling"] and
                    any(k in iss.rule_id.upper() for k in [
                        "AGREEMENT", "PERS", "SINGULAR", "PLURAL", "VERB", "SHE_DO", "DO_NOT", "HAVE_HAS"
                    ])
                )
            },
            "punctuation_mechanics": {
                "title": "Clausal Boundaries & Comma Mechanics",
                "category": "Correctness",
                "explanation": "Missing or misplaced delimiters around coordinate modifiers or dependent clauses hinder pacing. Calibrated punctuation guides natural reading cadence.",
                "penalty_weight": 2,
                "matcher": lambda iss: (
                    iss.category in ["correctness"] and
                    (iss.rule_id == "COORDINATE_ADJECTIVES_COMMA" or any(k in iss.rule_id.upper() for k in ["COMMA", "PUNCTUATION"]))
                )
            },
            "epistemic_hedging": {
                "title": "Throat-Clearing & Non-Committal Hedging",
                "category": "Delivery",
                "explanation": "Meta-commentary prefixes delay the core claim. Removing throat-clearing clauses delivers the message with crisp confidence.",
                "penalty_weight": 3,
                "matcher": lambda iss: (
                    any(kw in iss.original.lower() for kw in [
                        "it is important to", "it could be argued", "it is worth noting",
                        "it should be noted", "needless to say", "it goes without saying", "it is interesting to note"
                    ])
                )
            }
        }

        # Sentence lookup helper for previews
        def get_sentence_preview(start: int, end: int, orig: str, rep: str) -> str:
            left = max(0, text.rfind('.', 0, start) + 1)
            right = text.find('.', end)
            if right == -1:
                right = len(text)
            else:
                right = min(len(text), right + 1)
            
            s_ctx = text[left:right].strip()
            diff_str = f'<span class="diff-del">{html.escape(orig)}</span> <span class="diff-ins">{html.escape(rep)}</span>'
            clean_orig = html.escape(orig)
            escaped_ctx = html.escape(s_ctx)
            if clean_orig in escaped_ctx:
                return escaped_ctx.replace(clean_orig, diff_str, 1)
            return diff_str

        # Assign issues to habit clusters
        clustered_instances: Dict[str, List[HabitInstance]] = {k: [] for k in clusters_map}

        for idx, iss in enumerate(issues):
            if not iss.replacement or iss.replacement == iss.original:
                continue
            for h_id, h_cfg in clusters_map.items():
                if h_cfg["matcher"](iss):
                    preview_html = get_sentence_preview(iss.start, iss.end, iss.original, iss.replacement)
                    clustered_instances[h_id].append(HabitInstance(
                        id=idx,
                        start=iss.start,
                        end=iss.end,
                        original=iss.original,
                        replacement=iss.replacement,
                        diff_html=f'<span class="diff-del">{html.escape(iss.original)}</span> <span class="diff-ins">{html.escape(iss.replacement)}</span>',
                        sentence_preview=preview_html
                    ))
                    break

        result_clusters: List[HabitCluster] = []
        for h_id, instances in clustered_instances.items():
            if not instances:
                continue
            h_cfg = clusters_map[h_id]
            penalty = len(instances) * h_cfg["penalty_weight"]
            result_clusters.append(HabitCluster(
                id=h_id,
                title=h_cfg["title"],
                category=h_cfg["category"],
                explanation=h_cfg["explanation"],
                count=len(instances),
                impact_penalty=penalty,
                batch_fix_available=True,
                instances=instances
            ))

        # Sort clusters by impact penalty descending
        result_clusters.sort(key=lambda c: c.impact_penalty, reverse=True)
        return result_clusters

    def apply_habit_fix(self, text: str, habit_id: str) -> Tuple[str, int]:
        """Applies all replacements for a designated habit in a single reverse-offset pass."""
        check_res = self.check(text)
        target_cluster = next((c for c in check_res.habit_clusters if c.id == habit_id), None)
        if not target_cluster or not target_cluster.instances:
            return text, 0

        # Sort instances reverse by start offset to prevent position displacement
        sorted_instances = sorted(target_cluster.instances, key=lambda x: x.start, reverse=True)
        new_text = text
        count = 0
        for inst in sorted_instances:
            if 0 <= inst.start <= len(new_text) and 0 <= inst.end <= len(new_text):
                new_text = new_text[:inst.start] + inst.replacement + new_text[inst.end:]
                count += 1

        return new_text, count

    def quick_fix_all(self, text: str) -> Tuple[str, int]:
        """Applies all actionable grammar, conciseness, and style replacements in a single reverse-offset pass."""
        if not text or not text.strip():
            return text, 0
        
        check_res = self.check(text)
        actionable_issues = [
            iss for iss in check_res.issues
            if iss.replacement and iss.replacement != iss.original
        ]
        
        if not actionable_issues:
            return text, 0
            
        # Reverse sort by start to avoid offset displacement
        sorted_issues = sorted(actionable_issues, key=lambda x: x.start, reverse=True)
        new_text = text
        count = 0
        for iss in sorted_issues:
            if 0 <= iss.start <= len(new_text) and 0 <= iss.end <= len(new_text):
                new_text = new_text[:iss.start] + iss.replacement + new_text[iss.end:]
                count += 1
                
        return new_text, count

    def close(self):
        if hasattr(self, '_tool') and self._tool:
            self._tool.close()
