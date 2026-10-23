import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from engine.schemas import (
    GrammarCheckRequest,
    GrammarCheckResponse,
    ParaphraseRequest,
    ParaphraseResponse,
    WordSynonymRequest,
    WordSynonymResponse,
    AIDetectionRequest,
    AIDetectionResponse,
    ParagraphImprovementResponse,
    HabitBatchFixRequest,
    HabitBatchFixResponse,
    CompanionInspectRequest,
    CompanionInspectResponse,
    CompanionQuickFixRequest,
    CompanionQuickFixResponse,
    TopHabitSummary,
    HeavyweightParaphraseRequest,
    HeavyweightParaphraseResponse
)
from engine.grammar_checker import GrammarChecker
from engine.paraphraser import Paraphraser
from engine.heavyweight_engine import HeavyweightEngine
from engine.metrics import calculate_ai_detection_profile, calculate_readability
from engine.humanizer import HumanizerEngine

app = FastAPI(
    title="klyph-txt Engine",
    description="Deterministic, non-generative symbolic & statistical NLP writing assistant with Humanizer v6.0.",
    version="6.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engines
grammar_checker = GrammarChecker()
paraphraser = Paraphraser(grammar_checker=grammar_checker)
heavyweight_engine = HeavyweightEngine(grammar_checker=grammar_checker)
humanizer = HumanizerEngine()

@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "engine": "Symbolic & Statistical NLP + Humanizer v2.2",
        "generative_ai": False,
        "datasets": [
            "Humanizer 28 AI Pattern Detectors & 560+ Tier Vocabulary",
            "PPDB Phrasal 2.0 (Multi-word Paraphrases)",
            "Coxhead Academic Word List (AWL)",
            "Princeton WordNet 3.1 Synsets & Hyponyms",
            "Google & Reddit Zipf Human Frequency Distributions",
            "English Idiom & Authentic Collocation Repository",
            "Pleonasm & Tautology Reduction Catalog",
            "Vivid Action Verbs & Copula Eliminator",
            "Epistemic Hedging & Academic Calibration Markers",
            "Multi-Word Synthetic Cliché Eliminator",
            "Plain English Simplification Corpus",
            "Discourse Transitions Catalog",
            "LanguageTool 50,000+ Rule Grammar Database"
        ]
    }

@app.post("/api/check", response_model=GrammarCheckResponse)
def check_grammar(req: GrammarCheckRequest):
    try:
        return grammar_checker.check(req.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/paraphrase", response_model=ParaphraseResponse)
def paraphrase_text(req: ParaphraseRequest):
    try:
        return paraphraser.paraphrase(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/heavyweight/paraphrase", response_model=HeavyweightParaphraseResponse)
def heavyweight_paraphrase_endpoint(req: HeavyweightParaphraseRequest):
    try:
        return heavyweight_engine.transform_document(req.text, target_burstiness=req.target_burstiness)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/synonyms-for-word", response_model=WordSynonymResponse)
def get_synonyms_for_word(req: WordSynonymRequest):
    try:
        syns = paraphraser.get_word_synonyms(req.word, mode=req.mode)
        return WordSynonymResponse(word=req.word, synonyms=syns)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/detect-ai", response_model=AIDetectionResponse)
def detect_ai(req: AIDetectionRequest):
    try:
        return calculate_ai_detection_profile(req.text, boundary=req.boundary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/humanize")
def humanize_text_endpoint(req: dict):
    try:
        text = req.get("text", "")
        order_diversity = float(req.get("order_diversity", 0.6))
        lex_diversity = float(req.get("lex_diversity", 0.6))
        api_key = req.get("api_key") or os.environ.get("GEMINI_API_KEY")
        scan_res = humanizer.scan(text)
        beam_res = humanizer.humanize_beam(
            text,
            order_diversity=order_diversity,
            lex_diversity=lex_diversity,
            api_key=api_key
        )
        humanized_text = beam_res["best_text"]
        profile_before = calculate_ai_detection_profile(text)
        profile_after = beam_res.get("best_profile") or calculate_ai_detection_profile(humanized_text)
        return {
            "original_text": text,
            "humanized_text": humanized_text,
            "engine_mode": beam_res.get("engine_mode", "local_adversarial_beam_v6"),
            "candidates": beam_res.get("candidates", []),
            "scan": scan_res,
            "profile_before": profile_before,
            "profile_after": profile_after
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/improve-paragraphs", response_model=ParagraphImprovementResponse)
def improve_paragraphs_endpoint(req: dict):
    try:
        text = req.get("text", "")
        return grammar_checker.improve_paragraphs(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/apply-habit-fix", response_model=HabitBatchFixResponse)
def apply_habit_fix_endpoint(req: HabitBatchFixRequest):
    try:
        new_text, count = grammar_checker.apply_habit_fix(req.text, req.habit_id)
        return HabitBatchFixResponse(
            original_text=req.text,
            corrected_text=new_text,
            habit_id=req.habit_id,
            count_fixed=count
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/companion/inspect", response_model=CompanionInspectResponse)
def companion_inspect_endpoint(req: CompanionInspectRequest):
    try:
        text = req.text or ""
        if not text.strip():
            return CompanionInspectResponse(
                text=text,
                quality_score=100,
                total_issues=0,
                habit_clusters_count=0,
                word_count=0,
                reading_time_seconds=0,
                ai_probability=0.0,
                human_probability=100.0,
                ai_classification="Human-Authentic",
                fixed_preview="",
                diff_html="",
                top_habits=[]
            )
        
        # 1. Grammar & Habit inspection
        check_res = grammar_checker.check(text)
        
        # 2. Readability & metrics
        read_metrics = calculate_readability(text)
        
        # 3. AI detection metrics
        ai_res = calculate_ai_detection_profile(text)
        
        # 4. Quick fix & diff
        fixed_text, count_fixed = grammar_checker.quick_fix_all(text)
        diff_html = grammar_checker._build_paragraph_diff_html(text, fixed_text) if count_fixed > 0 else ""
        
        # 5. Top habits
        top_habits = [
            TopHabitSummary(
                id=h.id,
                title=h.title,
                category=h.category,
                count=h.count
            )
            for h in check_res.habit_clusters[:3]
        ]
        
        return CompanionInspectResponse(
            text=text,
            quality_score=check_res.quality_score,
            total_issues=check_res.total_issues,
            habit_clusters_count=len(check_res.habit_clusters),
            word_count=read_metrics.get("word_count", 0),
            reading_time_seconds=read_metrics.get("reading_time_seconds", 0),
            ai_probability=ai_res.get("ai_probability", 0.0),
            human_probability=ai_res.get("human_probability", 100.0),
            ai_classification=ai_res.get("classification", "Human-Written"),
            fixed_preview=fixed_text,
            diff_html=diff_html,
            top_habits=top_habits
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/companion/quick-fix", response_model=CompanionQuickFixResponse)
def companion_quick_fix_endpoint(req: CompanionQuickFixRequest):
    try:
        text = req.text or ""
        fixed_text, count = grammar_checker.quick_fix_all(text)
        after_check = grammar_checker.check(fixed_text)
        return CompanionQuickFixResponse(
            original_text=text,
            fixed_text=fixed_text,
            count_fixed=count,
            quality_score_after=after_check.quality_score
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static web UI
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)

@app.get("/hud")
def serve_hud():
    hud_path = os.path.join(static_dir, "hud.html")
    if os.path.exists(hud_path):
        return FileResponse(hud_path)
    return FileResponse(os.path.join(static_dir, "index.html"))

app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

@app.on_event("shutdown")
def shutdown_event():
    grammar_checker.close()
