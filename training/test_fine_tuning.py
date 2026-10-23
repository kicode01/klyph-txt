from transformers import AutoTokenizer
from datasets import load_dataset
import os

def test_pipeline():
    print("Testing Hugging Face Dataset & Tokenizer loading...")
    data_file = os.path.join(os.path.dirname(__file__), "synthetic_paraphrase_data.jsonl")
    ds = load_dataset("json", data_files=data_file, split="train")
    print(f"Loaded {len(ds)} rows from {data_file}")
    print("Sample row:", ds[0])

    tokenizer = AutoTokenizer.from_pretrained("t5-small")
    sample_inputs = ds[:3]["input_text"]
    tokens = tokenizer(sample_inputs, max_length=64, truncation=True, padding=True)
    print("Tokenized successfully! Input IDs count:", len(tokens["input_ids"]))
    print("Tokenized shape for batch 0:", len(tokens["input_ids"][0]))
    print("Pipeline ready for full GPU/CPU training!")

if __name__ == "__main__":
    test_pipeline()
