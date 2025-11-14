# MiniCrit-1.5B — Model Card  
**Adversarial Financial Critic for Autonomous LLM Trading Systems**

---

## 🧠 Model Overview

**MiniCrit-1.5B** is a LoRA-extended adversarial critic model designed to detect flawed reasoning, weak logic, hallucinations, and low-quality rationales in financial LLM systems. It is used as a validation layer inside multi-LLM autonomous trading engines.

---

## 📘 Intended Use

MiniCrit is designed for:

- Evaluating financial trade rationales  
- Detecting hallucinations and weak logical structure  
- Generating adversarial rebuttals  
- Supporting reinforcement-style iterative refinement  
- Serving as a critic/risk gate in automated trading workflows  

---

## 🚫 Out-of-Scope

MiniCrit is **not** intended for:

- Standalone financial investment decisions  
- Predictive modeling of price movement  
- Legal/compliance/financial advice  
- High-stakes real-time trading without human oversight  

---

## 📊 Training Data

The **FinRebut-600** dataset contains:

- 600 realistic trading rationales  
- 600 adversarial rebuttals  
- 3–7 sentence structure  
- Balanced logical flaw types:
  - overconfidence  
  - missing data  
  - flawed inference  
  - misaligned reasoning  
  - hallucinated evidence  

Future versions: **FinRebut-2000**.

---

## 🧪 Evaluation

Forward test on paper-trading engine:

- Baseline Sharpe: **+0.2**  
- MiniCrit-validated Sharpe: **+0.8**  
- 18% → 6% hallucination reduction  
- Stronger error-catching on high-volatility regimes  

---

## 📉 Limitations

- Small dataset (600 examples)  
- Critic only — no predictive capability  
- LoRA-based model inherits base model biases  
- Does not detect regulatory violations  
- May be too strict on ambiguous rationales  

---

## 🔐 Ethical Considerations

- Model must *not* be used for financial advice  
- Requires human supervision in any environment with risk  
- Dataset includes synthetic and anonymized examples  

---
Ousley, W. A. (2025). MiniCrit-1.5B and FinRebut-600 Dataset (v1.2.0). Zenodo.
https://doi.org/10.5281/zenodo.17594497
## 📄 Citation

