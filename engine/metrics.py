import math
import re
from typing import List, Dict, Any
from difflib import SequenceMatcher
from wordfreq import zipf_frequency
from .adversarial_lexicon import (
    TIER_1_DEAD_GIVEAWAYS,
    TIER_2_FORMULAIC_CONNECTORS,
    TIER_3_LATINATE_INFLATION,
    TIER_4_CORPORATE_JARGON,
)

_ALL_AI_LEXICON = (
    set(k.lower() for k in TIER_1_DEAD_GIVEAWAYS)
    | set(k.lower() for k in TIER_2_FORMULAIC_CONNECTORS)
    | set(k.lower() for k in TIER_3_LATINATE_INFLATION)
    | set(k.lower() for k in TIER_4_CORPORATE_JARGON)
)


def calculate_readability(text: str) -> Dict[str, Any]:
    """Calculates Flesch Reading Ease and Flesch-Kincaid Grade Level."""
    words = re.findall(r"\b[A-Za-z0-9'-]+\b", text)
    sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]

    total_words = len(words)
    total_sentences = max(len(sentences), 1)

    if total_words == 0:
        return {
            "flesch_reading_ease": 100.0,
            "grade_level": 0.0,
            "reading_time_seconds": 0,
            "word_count": 0,
            "sentence_count": 0
        }

    def count_syllables(word: str) -> int:
        w = word.lower()
        if len(w) <= 3:
            return 1
        w = re.sub(r"(?:[^laeiouy]|ed|es|e)$", "", w)
        w = re.sub(r"^y", "", w)
        syl = len(re.findall(r"[aeiouy]{1,2}", w))
        return max(syl, 1)

    total_syllables = sum(count_syllables(w) for w in words)

    asl = total_words / total_sentences
    asw = total_syllables / total_words
    fre = 206.835 - (1.015 * asl) - (84.6 * asw)
    fre = max(0.0, min(100.0, round(fre, 1)))

    fkgl = (0.39 * asl) + (11.8 * asw) - 15.59
    fkgl = max(0.0, round(fkgl, 1))

    reading_time = max(1, round((total_words / 200) * 60))

    return {
        "flesch_reading_ease": fre,
        "grade_level": fkgl,
        "reading_time_seconds": reading_time,
        "word_count": total_words,
        "sentence_count": total_sentences
    }


def calculate_burstiness(text: str) -> float:
    """
    Calculates sentence length variance (Burstiness).
    Higher burstiness (>4.0) is a hallmark of natural human writing.
    Low burstiness (<2.0) is characteristic of repetitive synthetic generation.
    """
    sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
    if len(sentences) <= 1:
        return 5.2

    lengths = [len(re.findall(r"\b\w+\b", s)) for s in sentences]
    mean = sum(lengths) / len(lengths)
    variance = sum((l - mean) ** 2 for l in lengths) / len(lengths)
    std_dev = math.sqrt(variance)
    return round(std_dev, 2)


def compute_token_diff(original: str, transformed: str) -> List[Dict[str, Any]]:
    """Computes word-level diff between original and paraphrased text."""
    orig_words = original.split()
    trans_words = transformed.split()

    matcher = SequenceMatcher(None, orig_words, trans_words)
    diff_tokens = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            for w in trans_words[j1:j2]:
                diff_tokens.append({"word": w, "type": "unchanged"})
        elif tag == "replace":
            for w in trans_words[j1:j2]:
                diff_tokens.append({"word": w, "type": "replaced", "orig": " ".join(orig_words[i1:i2])})
        elif tag == "insert":
            for w in trans_words[j1:j2]:
                diff_tokens.append({"word": w, "type": "added"})
        elif tag == "delete":
            pass

    return diff_tokens


def calculate_ai_detection_profile(text: str, boundary: float = 50.0) -> Dict[str, Any]:
    """
    Forensic Multi-Detector Adversarial Simulation Oracle (v5.0).
    Evaluates:
    1. Burstiness (Sentence Length Variance)
    2. Perplexity Proxy (Zipf Frequency Variance + Type-Token Ratio)
    3. Surviving Lexical AI Tells (Tiers 1-4)
    4. Surviving Structural Skeleton Tells (SKILL.md §1 contrasts, §8 dashes, §15 -ing riders, 'By...' templates)
    5. Abstract Nominalization Density (-tion, -ment, -ity, -ness stacks)
    """
    words = re.findall(r"\b[A-Za-z'-]+\b", text)
    sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]

    if not words or not sentences:
        return {
            "human_probability": 95.0,
            "ai_probability": 5.0,
            "burstiness_score": 5.0,
            "perplexity_score": 65.0,
            "classification": "Human-Written",
            "decision_boundary": boundary,
            "position_x": 25.0,
            "risk_level": "Safe",
            "sentence_lengths": [],
            "detectors": {
                "gptzero": 5.0,
                "turnitin": 5.0,
                "winston": 5.0,
                "originality": 5.0,
                "copyleaks": 5.0,
                "zerogpt": 5.0
            },
            "sentence_breakdown": []
        }

    # 1. Burstiness (Sentence Length Variance)
    sentence_lengths = [len(re.findall(r"\b\w+\b", s)) for s in sentences]
    burstiness = calculate_burstiness(text)

    # 2. Perplexity Proxy (Lexical Diversity & Zipf Surprise Index)
    zipf_scores = [zipf_frequency(w.lower(), "en") for w in words]
    zipf_mean = sum(zipf_scores) / len(zipf_scores) if zipf_scores else 4.5
    zipf_variance = sum((z - zipf_mean) ** 2 for z in zipf_scores) / len(zipf_scores) if zipf_scores else 0.5

    unique_words = len(set(w.lower() for w in words))
    ttr = unique_words / len(words)
    perplexity_proxy = round(min(100.0, max(20.0, (zipf_variance * 35.0) + (ttr * 50.0))), 1)

    # 3. Lexical Tell Density (Tiers 1-4)
    ai_word_hits = sum(1 for w in words if w.lower() in _ALL_AI_LEXICON)
    lexical_penalty = min(45.0, (ai_word_hits / max(len(words), 1)) * 350.0)

    # 4. Structural Skeleton Tells (SKILL.md §1, §8, §15)
    structural_hits = 0
    structural_hits += len(re.findall(r"\bit(?:'s| is) not (?:just|only|merely)\b", text, re.I))
    structural_hits += len(re.findall(r",\s+(?:offering|highlighting|underscoring|emphasizing|ensuring|reflecting|fostering|encompassing|showcasing)\b", text, re.I))
    structural_hits += len(re.findall(r"\bby\s+[a-z-]+ing\s+[^,]+,\s+[a-z\s]+?\s+(?:can|will|may)\b", text, re.I))
    structural_hits += len(re.findall(r"\s(?:[—–]|--)\s", text))
    structural_penalty = min(35.0, structural_hits * 12.0)

    # 5. Sentence-by-Sentence Breakdown (GPTZero / Originality.ai Granular Heatmap)
    sentence_breakdown = []
    mean_sent_len = sum(sentence_lengths) / max(len(sentence_lengths), 1)
    for idx, s in enumerate(sentences):
        s_words = re.findall(r"\b\w+\b", s)
        s_len = len(s_words)
        s_reasons = []
        s_risk = 8.0

        # Check lexical tells in sentence
        matched_lex = sorted(list({w.lower() for w in s_words if w.lower() in _ALL_AI_LEXICON}))
        if matched_lex:
            s_risk += min(55.0, len(matched_lex) * 20.0)
            s_reasons.append(f"AI Vocabulary: {', '.join(matched_lex[:4])}")

        # Check structural tells in sentence
        if re.search(r"\bit(?:'s| is) not (?:just|only|merely)\b", s, re.I):
            s_risk += 25.0
            s_reasons.append("Negative contrast ('Not X, but Y')")
        if re.search(r",\s+(?:offering|highlighting|underscoring|emphasizing|ensuring|reflecting|fostering|encompassing|showcasing)\b", s, re.I):
            s_risk += 24.0
            s_reasons.append("Shallow '-ing' participial rider")
        if re.search(r"\bby\s+[a-z-]+ing\s+[^,]+,\s+[a-z\s]+?\s+(?:can|will|may)\b", s, re.I):
            s_risk += 22.0
            s_reasons.append("Formulaic 'By [verb]-ing...' opener")
        if re.search(r"\b(enable|enables|allow|allows|empower|empowers)\s+[a-z\s]+?\s+to\s+[^,]+,\s+[^,]+,\s+and\s+", s, re.I):
            s_risk += 20.0
            s_reasons.append("Symmetric 3-verb AI triad")
        if re.search(r"\s(?:[—–]|--)\s", s):
            s_risk += 18.0
            s_reasons.append("AI em-dash pivot")

        # Check uniform cadence contribution
        if burstiness < 2.5 and abs(s_len - mean_sent_len) <= 2.5 and s_len >= 12:
            s_risk += 18.0
            s_reasons.append(f"Uniform sentence length ({s_len}w vs {round(mean_sent_len, 1)}w avg)")

        s_risk = round(min(98.0, max(5.0, s_risk)), 1)
        s_level = "high" if s_risk >= 60.0 else ("moderate" if s_risk >= 30.0 else "human")
        if not s_reasons:
            s_reasons.append("Natural human cadence & lexical entropy")

        sentence_breakdown.append({
            "index": idx,
            "sentence": s,
            "word_count": s_len,
            "ai_risk": s_risk,
            "level": s_level,
            "reasons": s_reasons
        })

    # 6. Burstiness & Perplexity Penalties
    ai_indicators = lexical_penalty + structural_penalty

    if burstiness < 2.0:
        ai_indicators += 35.0
    elif burstiness < 3.5:
        ai_indicators += 18.0
    else:
        ai_indicators += max(0.0, 10.0 - (burstiness * 1.5))

    if perplexity_proxy < 45.0:
        ai_indicators += 25.0
    elif perplexity_proxy < 60.0:
        ai_indicators += 12.0

    position_x = round(max(5.0, min(98.0, ai_indicators)), 1)

    is_flagged_ai = position_x >= boundary
    human_prob = round(100.0 - position_x, 1)
    ai_prob = position_x

    classification = "AI-Generated" if is_flagged_ai else "Human-Written"
    risk_level = "High Risk" if is_flagged_ai else ("Low / Safe" if human_prob > 75 else "Moderate Risk")

    gptzero_risk = round(min(99.0, max(2.0, (ai_prob * 1.05) if burstiness < 3.0 else (ai_prob * 0.85))), 1)
    turnitin_risk = round(min(99.0, max(2.0, ai_prob * 0.95)), 1)
    originality_risk = round(min(99.0, max(2.0, (ai_prob * 1.15) if (burstiness < 3.5 or structural_hits > 0) else (ai_prob * 0.8))), 1)
    winston_risk = round(min(99.0, max(2.0, ai_prob * 0.9)), 1)
    copyleaks_risk = round(min(99.0, max(2.0, ai_prob * 0.88)), 1)
    zerogpt_risk = round(min(99.0, max(2.0, (ai_prob * 1.1) if perplexity_proxy < 55.0 else (ai_prob * 0.75))), 1)

    return {
        "human_probability": human_prob,
        "ai_probability": ai_prob,
        "burstiness_score": burstiness,
        "perplexity_score": perplexity_proxy,
        "lexical_tells": ai_word_hits,
        "structural_tells": structural_hits,
        "classification": classification,
        "decision_boundary": boundary,
        "position_x": position_x,
        "risk_level": risk_level,
        "sentence_lengths": sentence_lengths,
        "total_sentences": len(sentences),
        "total_words": len(words),
        "sentence_breakdown": sentence_breakdown,
        "detectors": {
            "gptzero": gptzero_risk,
            "turnitin": turnitin_risk,
            "winston": winston_risk,
            "originality": originality_risk,
            "copyleaks": copyleaks_risk,
            "zerogpt": zerogpt_risk
        }
    }
