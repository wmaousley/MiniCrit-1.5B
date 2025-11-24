# MiniCrit-1.5B — Model Card

## 🔍 Model Overview
MiniCrit-1.5B is an adversarial financial critic designed to evaluate and rebut LLM-generated trading rationales. This model functions as an adversarial “validator layer” inside multi-LLM autonomous trading systems.

---

## 🧠 Intended Use

### ✔ Supported Use Cases
- Evaluating trading rationales  
- Detecting weak reasoning  
- Generating adversarial rebuttals  
- Risk-aware validation inside automated trading engines  
- Filtering hallucination-prone decisions  

### ❌ Out of Scope
- Direct financial advice  
- Acting as a trading agent  
- High-frequency execution  

---

## 📦 Model Details
- **Architecture:** LLaMA-based critic (1.5B parameters)  
- **Training:** ATAC-LoRA pipeline (nightly retraining supported)  
- **Checkpoint:** `minicrit_lora_0.5b.pt`  
- **Dataset:** Training data: 12,132 institutional trading rationale-critique pairs
Published: https://huggingface.co/datasets/wmaousley/minicrit-training-12k
License: CC-BY-4.0
- **Author:** William Alexander Ousley  
- **License:** MIT  
- **DOI:** https://doi.org/10.5281/zenodo.17594497  

---

## 🧪 Training Procedure
MiniCrit uses adversarial LoRA refinement:

1. Seed model → generate trading rationale evaluations  
2. Weak / flawed reasoning flagged  
3. Rebuttals generated using adversarial prompt template  
4. Samples stored in FinRebut dataset  
5. Nightly ATAC-LoRA update applied  

---

## 📈 Evaluation

### Forward Test (1 week)
- **Sharpe:** +0.8  
- **Baseline:** +0.2  
- **Reduction in invalid rationales:** ~48%  

---

## 🛡️ Safety
MiniCrit is not designed for:
- Executing trades  
- Financial advice  
- Price prediction  
- High-risk leverage decisioning  

It evaluates reasoning quality only.

---

## 📝 Citation
Please cite:

Ousley, W. A. (2025). *MiniCrit-1.5B and FinRebut-600 Dataset.* Zenodo.  
DOI: https://doi.org/10.5281/zenodo.17594497  
