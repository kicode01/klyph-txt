# klyph-txt (v6.0) — Autonomous Neurosymbolic Writing & Adversarial Humanizer

**`klyph-txt`** is a neurosymbolic NLP writing, paraphrasing, grammar, and anti-AI detection suite uniting deterministic AST dependency transformations, Wikipedia's 26 structural de-AI rules (`SKILL.md`), a Closed-Loop Adversarial Beam Search, and an optional Hybrid `gemini-4-argon` deep semantic rewriter.

---

## 4 Core Modules

### 1. Editorial Chisel (Grammar & Clarity Engine)
- **50,000+ Deterministic Rules:** Powered by LanguageTool and SymSpell.
- **Categorized Spans:** Correctness, Clarity, Engagement, and Delivery with one-click or batch macro-habit fixes.
- **Readability & Flow Telemetry:** Flesch Reading Ease, word count, and reading time.

### 2. Syntactic Morph (Multi-Mode AST Paraphraser)
- **9 Distinct Modes:** Standard, Fluency, Formal, Academic, Simple, Creative, Shorten, Expand, and **Heavyweight AST**.
- **Syntactic Restructuring:** Active $\leftrightarrow$ Passive voice conversion, Chomsky clause transposition, and pleonasm reduction.
- **Click-to-Replace Synonyms:** Click any word in the output to view ranked contextual synonyms from WordNet 3.1 and Zipf frequency distributions.

### 3. Spectral Radar (Granular AI Detector & Decision Boundary Simulator)
- **Interactive Distribution Bell Curve:** Plots overlapping Human $P(H|x)$ vs. Synthetic $P(AI|x)$ distributions on HTML5 Canvas.
- **Sentence-by-Sentence AI Risk Heatmap:** Scores every individual sentence (`HIGH`, `MODERATE`, `HUMAN`) and lists exact lexical and structural triggers (`Not X, but Y`, shallow `-ing` participial riders, `By [verb]-ing...` templates, 3-verb triads, em-dashes, and uniform cadence).
- **One-Click Auto-Humanize:** Neutralize flagged sentences directly from the Radar view.

### 4. Adversarial Humanizer (v6.0 Closed-Loop Beam Search)
- **7-Tier Context-Safe Lexicon (`engine/adversarial_lexicon.py`):** Purges dead-giveaway AI vocabulary, corporate jargon, copula avoidance (`serves as a testament to` $\to$ `shows`), and chatbot throat-clearing without creating unnatural "Frankenstein collocations."
- **Structural AST Deconstructor (`engine/syntactic_mutator.py`):** Eliminates shallow trailing `-ing` riders, rewrites `By [verb]-ing..., [subject] can...` openers, strips em-dashes/en-dashes, and breaks symmetrical 3-verb triads using finite verb inflection.
- **Closed-Loop Adversarial Beam Search (`engine/humanizer.py`):** Generates multiple structural candidates, scores each against `calculate_ai_detection_profile`, and selects the lowest-risk, highest-burstiness ($\sigma$) tree.
- **Optional Hybrid `gemini-4-argon` Mode (`engine/argon_rewriter.py`):** Automatically activates when `GEMINI_API_KEY` is set, pairing deep semantic rewriting with deterministic local AST verification.

---

## Quick Start

### 1. Install Dependencies
```powershell
python -m venv .venv
.\.venv\Scripts\pip.exe install -r requirements.txt
.\.venv\Scripts\python.exe -m spacy download en_core_web_sm
```

### 2. Launch `klyph-txt`
```powershell
.\.venv\Scripts\python.exe run.py
```
Then open `http://127.0.0.1:8000` in your browser.
