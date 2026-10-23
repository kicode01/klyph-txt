from engine.grammar_checker import GrammarChecker
from engine.paraphraser import Paraphraser
from engine.schemas import GrammarCheckRequest, ParaphraseRequest

def main():
    print("=== Testing Grammar Checker ===")
    checker = GrammarChecker()
    text = "She do not knows how to writes clean codes. In order to make a decision, we conducted an investigation into the matter."
    res = checker.check(text)
    print(f"Original: {text}")
    print(f"Corrected: {res.corrected_text}")
    print(f"Total issues: {res.total_issues}")
    for issue in res.issues:
        print(f"  [{issue.category.upper()}] ({issue.start}-{issue.end}) '{issue.original}' -> '{issue.replacement}' : {issue.message}")

    print("\n=== Testing Paraphraser ===")
    paraphraser = Paraphraser(grammar_checker=checker)
    
    modes = ["standard", "formal", "simple", "shorten"]
    for m in modes:
        p_res = paraphraser.paraphrase(ParaphraseRequest(text=res.corrected_text, mode=m, synonym_level=2))
        print(f"\n--- Mode: {m.upper()} ---")
        print(f"Paraphrased: {p_res.paraphrased_text}")
        print(f"Alternatives count: {len(p_res.alternatives)}")
        for idx, alt in enumerate(p_res.alternatives):
            print(f"  Alt {idx+1} (Changes: {alt.changes_count}): {alt.text}")

    print("\nAll tests completed successfully!")

if __name__ == "__main__":
    main()
