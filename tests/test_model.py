import os
import warnings
import pandas as pd
import torch

# Make matplotlib optional (important for CI)
try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from transformers.trainer_callback import TrainerCallback
from peft import LoraConfig, get_peft_model, TaskType

# Environment settings for predictable CPU behavior
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "0"
os.environ["CUDA_VISIBLE_DEVICES"] = ""
warnings.filterwarnings("ignore")

# ---------------------------------------------------------
# EXPORTED CONSTANT FOR TESTS
# ---------------------------------------------------------
MODEL = "Qwen/Qwen2-0.5B-Instruct"


# ---------------------------------------------------------
# TRAINING LOGIC ONLY RUNS WHEN EXECUTING THIS FILE DIRECTLY
# ---------------------------------------------------------
def main():

    print("📦 Loading tokenizer…")
    tokenizer = AutoTokenizer.from_pretrained(MODEL, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token

    print("📄 Loading dataset…")
    ds = load_dataset("csv", data_files={"train": "data/finrebut400.csv"})["train"]

    def fmt(x):
        return {"text": f"Rationale: {x['text']}\nCounter: {x['rebuttal']}"}

    ds = ds.map(fmt, remove_columns=ds.column_names)

    def tokenize(batch):
        out = tokenizer(batch["text"], truncation=True, max_length=128, padding="max_length")
        out["labels"] = out["input_ids"].copy()
        return out

    print("🔧 Tokenizing…")
    ds = ds.map(tokenize, batched=True)
    ds.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])

    print("🧠 Loading base model…")
    base = AutoModelForCausalLM.from_pretrained(MODEL, torch_dtype=torch.float32)

    print("✨ Applying LoRA…")
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=8,
        lora_alpha=16,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05,
    )
    model = get_peft_model(base, lora_config)

    class LossCollector(TrainerCallback):
        def __init__(self):
            self.loss = []

        def on_log(self, args, state, control, logs=None, **kwargs):
            if logs and "loss" in logs:
                self.loss.append(logs["loss"])

    loss_cb = LossCollector()

    args = TrainingArguments(
        output_dir="ckpt",
        per_device_train_batch_size=1,
        gradient_accumulation_steps=16,
        num_train_epochs=1,
        learning_rate=3e-4,
        logging_steps=10,
        save_steps=0,
        report_to="none",
        fp16=False,
        dataloader_pin_memory=False,
    )

    print("🚀 Starting training…")
    trainer = Trainer(model=model, args=args, train_dataset=ds, callbacks=[loss_cb])
    trainer.train()

    print("💾 Saving final checkpoint…")
    trainer.save_model("ckpt/final")

    # ---------------------------------------------------------
    # OPTIONAL PLOTTING
    # ---------------------------------------------------------
    if plt is not None:
        print("📊 Plotting loss curve…")
        plt.plot(loss_cb.loss)
        plt.title("MiniCrit-0.5B LoRA Loss (CPU)")
        plt.xlabel("Log step")
        plt.ylabel("Loss")
        plt.savefig("assets/loss.png", dpi=150)
        print("✅ Done – plot saved to assets/loss.png")
    else:
        print("⚠️ matplotlib not installed — skipping plot.")

    print(f"🎉 Training complete — final loss: {loss_cb.loss[-1]:.3f}")


# ---------------------------------------------------------
# MAIN ENTRYPOINT
# ---------------------------------------------------------
if __name__ == "__main__":
    main()
