"""
Argon Deep Semantic Rewriter (v6.0 Hybrid Engine).
Integrates the Gemini 4 Argon model (`gemini-4-argon`) via the official `google-genai`
Interactions API (`client.interactions.create`) when `GEMINI_API_KEY` is configured.
Enforces Wikipedia's 26 'Signs of AI Writing' rules (SKILL.md) at the semantic and
macro-paragraph level before passing output to the local AST & Burstiness verifier.
"""
import os
from typing import Optional

ARGON_HUMANIZER_SYSTEM_INSTRUCTION = """You are an elite human editor applying Wikipedia's "Signs of AI writing" (26 structural rules).
Rewrite the input text so it reads like a sharp, natural human writer wrote it from scratch, while preserving 100% of the factual meaning.

STRICT STRUCTURAL & LEXICAL RULES:
1. NO Negative Contrasts: Never write "It is not X, it's Y", "Not merely X, but Y", or "X—not Y". State the positive claim directly.
2. NO Staged Openers or Throat-Clearing: Cut "In today's fast-paced world", "Here's what you need to know", "At its core", "It is worth noting that". Start directly with the substance.
3. NO Forced Triads: Do not group verbs, adjectives, or examples into symmetrical threes ("streamline workflows, optimize resources, and drive innovation"). Use two items or break the rhythm.
4. NO Em-Dashes or En-Dashes: Never use "—" or "–". Use periods, commas, or parentheses.
5. NO Shallow '-ing' Participial Riders: Never end sentences with ", highlighting...", ", underscoring...", ", fostering...", ", ensuring...", ", offering...", or ", showcasing...".
6. NO 'By [verb]-ing..., [subject] can...' Skeletons: Rewrite instrumental gerund openers into direct active clauses.
7. NO AI Stock Vocabulary: Never use delve, tapestry, realm, landscape (abstract), testament, pivotal, crucial, robust, seamless, bespoke, multifaceted, empower, elevate, leverage, bolster, foster, or paradigm.
8. ASYMMETRIC CADENCE (High Burstiness): Mix short, direct sentences (3–7 words) with longer, concrete sentences (16–24 words). Avoid uniform 14–18 word sentences.
9. Output ONLY the rewritten prose. Do not include commentary, markdown headers, or quotes around the text."""


class ArgonSemanticRewriter:
    """
    Optional hybrid deep-semantic rewriter powered by `gemini-4-argon` via `google-genai`.
    Automatically activates when `GEMINI_API_KEY` or `GOOGLE_API_KEY` is present.
    """
    def __init__(self, model: str = "gemini-4-argon"):
        self.model = model

    def is_available(self, api_key: Optional[str] = None) -> bool:
        key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if not key:
            return False
        try:
            from google import genai  # noqa: F401
            return True
        except ImportError:
            return False

    def rewrite(self, text: str, api_key: Optional[str] = None) -> Optional[str]:
        """
        Calls `gemini-4-argon` using `client.interactions.create` (no deprecated sampling params).
        Returns None if no API key or SDK is available so the local AST engine handles it seamlessly.
        """
        key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if not key or not text or not text.strip():
            return None

        try:
            from google import genai
            client = genai.Client(api_key=key)
            interaction = client.interactions.create(
                model=self.model,
                system_instruction=ARGON_HUMANIZER_SYSTEM_INSTRUCTION,
                input=text.strip(),
            )
            out = getattr(interaction, "output_text", None)
            if out and isinstance(out, str) and out.strip():
                return out.strip()
        except Exception:
            return None
        return None
