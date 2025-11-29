import os
import warnings
import pandas as pd
import torch

# Make matplotlib optional (prevents CI import failure)
try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from transformers.trainer_callback import TrainerCallback
from peft import LoraConfig, get_peft_model, TaskType

os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "0"
os.environ["CUDA_VISIBLE_DEVICES"] = ""
warnings.filterwarnings("ignore")

# ---------------------------------------------------------
# ONLY THIS RUNS ON IMPORT (Safe for CI)
# ---------------------------------------------------------
MODEL = "Qwen/Qwen2-0.5B-Instruct"


# ---------------------------------------------------------
# TRAINING CODE — Runs ONLY if executed directly
# ---------------------------------------------------------
def main():

    tokenizer = AutoTokenizer.from_pretrained(MODEL, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token

    ds = load_dataset("csv", data_files={"train": "data/finrebut400.csv"})["train"]

    def fmt(x):
        return {"text": f"Rationale: {x['text']}\nCounter: {x['rebuttal']}"}

    ds = ds.map(fmt, remove_columns=ds.column_names)

    def tokenize(batch):
        out = tokenizer(batch["text"], truncation=True, max_length=128, padding="max_length")
        out["labels"] = out["input_ids"].copy()
        return out

    ds = ds.map(tokenize, batched=True)
    ds.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])

    base = AutoModelForCausalLM.from_pretrained(MODEL, torch_dtype=torch.float32)

    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=8,
        lora_alpha=16,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05
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

    trainer = Trainer(model=model, args=args, train_dataset=ds, callbacks=[loss_cb])
    trainer.train()
    trainer.save_model("ckpt/final")

    if plt is not None:
        plt.plot(loss_cb.loss)
        plt.title("MiniCrit-0.5B LoRA loss (CPU)")
        plt.xlabel("Log step")
        plt.ylabel("Loss")
        plt.savefig("assets/loss.png", dpi=150)
        print(f"Done — final loss {loss_cb.loss[-1]:.3f} — plot saved assets/loss.png")
    else:
        print(f"Done — final loss {loss_cb.loss[-1]:.3f} — no matplotlib")


# ENTRYPOINT
if __name__ == "__main__":
    main()
