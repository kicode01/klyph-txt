from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field

class TextSpan(BaseModel):
    start: int
    end: int
    original: str
    replacement: str
    category: Literal["correctness", "clarity", "engagement", "delivery", "spelling"]
    rule_id: str
    message: str
    explanation: Optional[str] = None
    confidence: float = 1.0

class GrammarCheckRequest(BaseModel):
    text: str
    language: str = "en-US"

class SentenceGroup(BaseModel):
    id: int
    sentence_start: int
    sentence_end: int
    original_sentence: str
    rewritten_sentence: str
    issues_count: int
    category: str
    diff_html: str
    preview: str
    issue_indices: List[int]

class HabitInstance(BaseModel):
    id: int
    start: int
    end: int
    original: str
    replacement: str
    diff_html: str
    sentence_preview: str

class HabitCluster(BaseModel):
    id: str
    title: str
    category: str
    explanation: str
    count: int
    impact_penalty: int
    batch_fix_available: bool = True
    instances: List[HabitInstance] = Field(default_factory=list)

class GrammarCheckResponse(BaseModel):
    text: str
    corrected_text: str
    total_issues: int
    issues: List[TextSpan]
    readability_score: float
    reading_time_seconds: int
    quality_score: int = 100
    category_counts: Dict[str, int] = Field(default_factory=dict)
    sentence_groups: List[SentenceGroup] = Field(default_factory=list)
    habit_clusters: List[HabitCluster] = Field(default_factory=list)

class HabitBatchFixRequest(BaseModel):
    text: str
    habit_id: str

class HabitBatchFixResponse(BaseModel):
    original_text: str
    corrected_text: str
    habit_id: str
    count_fixed: int

class ParagraphRewrite(BaseModel):
    id: int
    start: int
    end: int
    original: str
    rewritten: str
    diff_html: str
    issues_addressed: int
    improvement_summary: str

class ParagraphImprovementResponse(BaseModel):
    paragraphs: List[ParagraphRewrite]
    total_paragraphs: int

class ParaphraseRequest(BaseModel):
    text: str
    mode: Literal[
        "standard",
        "fluency",
        "formal",
        "academic",
        "simple",
        "creative",
        "shorten",
        "expand",
        "heavyweight"
    ] = "standard"
    synonym_level: int = Field(default=2, ge=1, le=4, description="1=Low, 2=Medium, 3=High, 4=Extreme")
    preserve_words: Optional[List[str]] = Field(default_factory=list)
    voice_mode: Literal["auto", "force_active", "force_passive"] = "auto"
    split_sentences: bool = False
    add_transitions: bool = False

class ParaphraseAlternative(BaseModel):
    text: str
    label: str
    strategy: str
    changes_count: int
    diff_tokens: List[Dict[str, Any]]
    burstiness_score: float
    perplexity_risk: str = "human-natural"

class ParaphraseResponse(BaseModel):
    original_text: str
    paraphrased_text: str
    alternatives: List[ParaphraseAlternative]
    mode_applied: str
    metrics: Dict[str, Any]

class WordSynonymRequest(BaseModel):
    word: str
    context_sentence: Optional[str] = None
    mode: str = "standard"

class WordSynonymResponse(BaseModel):
    word: str
    synonyms: List[str]

class AIDetectionRequest(BaseModel):
    text: str
    boundary: float = 50.0

class AIDetectionResponse(BaseModel):
    human_probability: float
    ai_probability: float
    burstiness_score: float
    perplexity_score: float
    classification: str
    decision_boundary: float
    position_x: float
    risk_level: str
    sentence_lengths: List[int]
    total_sentences: int
    total_words: int
    sentence_breakdown: List[Dict[str, Any]] = Field(default_factory=list)

class CompanionInspectRequest(BaseModel):
    text: str

class TopHabitSummary(BaseModel):
    id: str
    title: str
    category: str
    count: int

class CompanionInspectResponse(BaseModel):
    text: str
    quality_score: int
    total_issues: int
    habit_clusters_count: int
    word_count: int
    reading_time_seconds: int
    ai_probability: float
    human_probability: float
    ai_classification: str
    fixed_preview: str
    diff_html: str
    top_habits: List[TopHabitSummary] = Field(default_factory=list)

class CompanionQuickFixRequest(BaseModel):
    text: str

class CompanionQuickFixResponse(BaseModel):
    original_text: str
    fixed_text: str
    count_fixed: int
    quality_score_after: int

class HeavyweightParaphraseRequest(BaseModel):
    text: str
    target_burstiness: float = 7.0

class HeavyweightSentenceDetail(BaseModel):
    index: int
    original: str
    transformed: str
    strategy: str

class HeavyweightParaphraseResponse(BaseModel):
    original_text: str
    heavyweight_text: str
    paraphrased_text: Optional[str] = None
    alternatives: List[ParaphraseAlternative] = Field(default_factory=list)
    metrics: Dict[str, Any] = Field(default_factory=dict)
    burstiness_before: float
    burstiness_after: float
    sentences_count: int
    syntactic_transforms_count: int
    lexical_transforms_count: int
    factual_invariance_score: float = 100.0
    ai_detection_risk: str = "0.0% (Mathematical AST Invariant)"
    sentence_details: List[HeavyweightSentenceDetail] = Field(default_factory=list)


