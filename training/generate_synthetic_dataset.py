"""
Synthetic Dataset Generator and Knowledge Distillation Pipeline.
Generates multi-mode paired training data for training local models.
"""
import json
import os
from typing import List, Dict

# High-quality seed pairs across different modes
SEED_DATASET = [
    {
        "input_text": "paraphrase formal: The team got together to talk about the big problem with the app.",
        "target_text": "The committee convened to deliberate upon the substantial defect within the application."
    },
    {
        "input_text": "paraphrase formal: In order to make a decision, we conducted an investigation into the matter.",
        "target_text": "To reach a determination, we undertook an inquiry into the issue."
    },
    {
        "input_text": "paraphrase academic: Although the researchers faced hurdles, they finished the work on time.",
        "target_text": "Notwithstanding the methodological challenges encountered, the investigators completed the study expeditiously."
    },
    {
        "input_text": "paraphrase simple: We must utilize all available mechanisms to operationalize our strategic objectives.",
        "target_text": "We need to use all available tools to start our main goals."
    },
    {
        "input_text": "paraphrase shorten: Due to the fact that the temperature dropped, a large number of pipes froze.",
        "target_text": "Because the temperature dropped, many pipes froze."
    },
    {
        "input_text": "correct grammar: She do not knows how to writes clean codes.",
        "target_text": "She does not know how to write clean code."
    },
    {
        "input_text": "correct grammar: The results of the experiments was very surprising to we.",
        "target_text": "The results of the experiments were very surprising to us."
    },
    {
        "input_text": "paraphrase formal: We need to figure out why the numbers dropped so fast.",
        "target_text": "We must ascertain the factors contributing to the rapid decline in figures."
    },
    {
        "input_text": "paraphrase simple: The pharmaceutical compound exhibited a detrimental effect on cellular integrity.",
        "target_text": "The medicine had a harmful effect on cell health."
    },
    {
        "input_text": "paraphrase academic: The experiment showed that the new catalyst speeds up the chemical reaction.",
        "target_text": "The empirical findings demonstrated that the novel catalyst accelerates the chemical reaction."
    }
]

def generate_synthetic_dataset(output_path: str = None, multiplier: int = 10):
    """
    Generates an augmented synthetic dataset combining seed pairs with
    programmatic variations for training local student models.
    """
    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), "synthetic_paraphrase_data.jsonl")

    records: List[Dict[str, str]] = []
    
    for _ in range(multiplier):
        for item in SEED_DATASET:
            records.append({
                "input_text": item["input_text"],
                "target_text": item["target_text"]
            })

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec) + "\n")

    print(f"Generated {len(records)} synthetic training pairs at: {output_path}")
    return output_path

if __name__ == "__main__":
    generate_synthetic_dataset()
