"""
Fine-tuning pipeline for training a custom Seq2Seq Paraphrasing & GEC model
using Hugging Face Transformers and PyTorch.
"""
import os
import argparse
from typing import Dict, Any
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
    DataCollatorForSeq2Seq
)
from datasets import load_dataset, Dataset

def prepare_dataset(dataset_name: str = "paws", split: str = "train", max_samples: int = 1000):
    """Loads and formats benchmark paraphrase or grammar correction datasets."""
    print(f"Loading dataset: {dataset_name} ({split})...")
    
    if dataset_name == "paws":
        # PAWS: Paraphrase Adversaries from Word Scrambling
        raw_ds = load_dataset("google-research-datasets/paws", "labeled_final", split=split)
        # Filter for true paraphrases (label == 1)
        filtered = raw_ds.filter(lambda x: x["label"] == 1)
        if max_samples:
            filtered = filtered.select(range(min(len(filtered), max_samples)))
            
        def format_paws(example):
            return {
                "input_text": f"paraphrase: {example['sentence1']}",
                "target_text": example["sentence2"]
            }
        return filtered.map(format_paws)

    elif dataset_name == "synthetic":
        # Load local AI-generated synthetic training data
        synthetic_path = os.path.join(os.path.dirname(__file__), "synthetic_paraphrase_data.jsonl")
        if os.path.exists(synthetic_path):
            return load_dataset("json", data_files=synthetic_path, split="train")
        else:
            raise FileNotFoundError(f"Synthetic dataset not found at {synthetic_path}")
            
    else:
        raise ValueError(f"Unsupported dataset: {dataset_name}")

def train(
    model_name: str = "t5-small",
    dataset_name: str = "paws",
    output_dir: str = "./models/custom_paraphraser",
    epochs: int = 3,
    batch_size: int = 8,
    max_samples: int = 500
):
    print("=" * 60)
    print(f" Starting Fine-Tuning Pipeline: {model_name}")
    print(f" Dataset: {dataset_name} | Epochs: {epochs} | Batch Size: {batch_size}")
    print("=" * 60)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    # 1. Load Tokenizer & Model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    model.to(device)

    # 2. Load & Preprocess Dataset
    train_dataset = prepare_dataset(dataset_name, split="train", max_samples=max_samples)

    def preprocess_function(examples):
        inputs = examples["input_text"]
        targets = examples["target_text"]
        model_inputs = tokenizer(inputs, max_length=128, truncation=True, padding="max_length")
        labels = tokenizer(text_target=targets, max_length=128, truncation=True, padding="max_length")
        
        # Replace padding token id's with -100 so loss ignores them
        labels["input_ids"] = [
            [(l if l != tokenizer.pad_token_id else -100) for l in label]
            for label in labels["input_ids"]
        ]
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    tokenized_dataset = train_dataset.map(preprocess_function, batched=True)

    # 3. Training Arguments
    training_args = Seq2SeqTrainingArguments(
        output_dir=output_dir,
        per_device_train_batch_size=batch_size,
        num_train_epochs=epochs,
        learning_rate=5e-5,
        weight_decay=0.01,
        save_strategy="epoch",
        logging_steps=10,
        push_to_hub=False,
        fp16=(device == "cuda"),
        use_cpu=(device == "cpu")
    )

    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

    # 4. Trainer Initialization
    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
        data_collator=data_collator,
        processing_class=tokenizer
    )

    # 5. Execute Training
    print("\nExecuting model training...")
    trainer.train()

    # 6. Save Artifacts
    print(f"\nSaving fine-tuned model checkpoint to: {output_dir}")
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print("Training successfully finished!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train custom paraphrase model")
    parser.add_argument("--model", type=str, default="t5-small")
    parser.add_argument("--dataset", type=str, default="paws")
    parser.add_argument("--epochs", type=int, default=1)
    parser.add_argument("--samples", type=int, default=100)
    parser.add_argument("--output", type=str, default="./models/custom_paraphraser")
    args = parser.parse_args()

    train(
        model_name=args.model,
        dataset_name=args.dataset,
        output_dir=args.output,
        epochs=args.epochs,
        max_samples=args.samples
    )
