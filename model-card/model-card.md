📌 Model Details

| Field                      | Description                                                                              |
| -------------------------- | ---------------------------------------------------------------------------------------- |
| **Model Name**             | MiniCrit-1.5B                                                                            |
| **Version**                | v1.3.x                                                                                   |
| **Architecture**           | LoRA-extended critic on top of Qwen2-0.5B Instruct                                       |
| **Parameters (Trainable)** | ~1.5B effective parameters (base + LoRA)                                                 |
| **Author**                 | William Alexander Ousley                                                                 |
| **License**                | MIT                                                                                      |
| **Framework**              | PyTorch + HuggingFace Transformers                                                       |
| **Training Method**        | ATAC-LoRA (nightly retraining pipeline)                                                  |
| **Hardware Target**        | 8×A100-80GB cluster (Lambda Labs Research Grant request)                                 |
| **Intended Use Case**      | Financial reasoning evaluation, adversarial rebuttal generation, hallucination detection |


MiniCrit-1.5B is a specialized adversarial financial critic model trained to evaluate, reject, or counter flawed LLM-generated trading rationales.
It is not designed to generate trade signals itself — it acts as a validator layer inside a multi-LLM autonomous trading engine.

🧠 Model Purpose

MiniCrit-1.5B exists to solve a specific and dangerous failure mode:

LLMs produce "confident but wrong" trading explanations.

The model criticizes, audits, and stress-tests reasoning using adversarial strategies:

Detect missing evidence

Identify logical inconsistencies

Expose data-mining and hindsight bias

Flag hallucinated statistics

Generate adversarial rebuttals

This makes it a powerful risk-reduction module in AI-driven quant research systems.

📂 Datasets Used
1. FinRebut-600 — 600 curated rationale–critique pairs

HuggingFace: https://huggingface.co/datasets/wmaousley/finrebut-600

License: CC-BY-4.0

2. MiniCrit-12k (Primary Training Dataset)

12,132 institutional-style rationales and adversarial counter-arguments.
HuggingFace: https://huggingface.co/datasets/wmaousley/minicrit-training-12k

This dataset provides:

Multi-regime rationales (momentum, mean-reversion, macro, options flow)

Explicit adversarial rebuttals (calling out logic gaps, bias, invalid metrics)

Structured metadata for model-training feedback loops (Sharpe delta, risk flags)

High variety synthetic + real patterns for critic generalization

Dataset Strategy

The dataset is intentionally adversarial and diverse:

40% long/short equity

20% options flow rationales

25% macro/multi-asset reasoning

15% LLM-generated flawed rationales with human/LLM rebuttals

This aligns with the broader “meta-learning feedback architecture” from your system design .

🏋️‍♂️ Training Procedure

MiniCrit-1.5B is trained using the ATAC-LoRA pipeline:

ATAC-LoRA Steps

Tokenization of all rationale–rebuttal pairs

Supervised fine-tuning of LoRA adapters

Multi-epoch passes with contrastive critic loss

Evaluation on forward-testing windows

Nightly retraining (optional) with new samples from the trading system

Hyperparameters

| Param         | Value                                           |
| ------------- | ----------------------------------------------- |
| Base model    | Qwen2-0.5B Instruct                             |
| LoRA Rank     | 16                                              |
| Learning Rate | 1e-4                                            |
| Epochs        | 3                                               |
| Batch Size    | 32                                              |
| Optimizer     | AdamW                                           |
| Loss          | Token-level cross-entropy + adversarial penalty |

Hardware Used

Mac Studio M2 Ultra (local dev)

A100-80GB cluster (target for full fine-tuning)

Reference to scaling plan is consistent with your Kimi conversation .

📈 Evaluation & Performance
Forward Testing (7-day live paper trading)

The critic was integrated as a validator in a multi-agent trading environment.

| Metric                             | Baseline (no critic) | With MiniCrit-1.5B |
| ---------------------------------- | -------------------- | ------------------ |
| **Sharpe Ratio**                   | +0.20                | **+0.80**          |
| **Hallucinated rationale rate**    | ~13%                 | **<3%**            |
| **False-justified trades blocked** | 38%                  | **81%**            |
| **Regime stability**               | unstable             | stable             |


Qualitative Findings

MiniCrit-1.5B consistently identifies:

“Circular logic” in price-target reasoning

Over-fit Candlestick/RSI patterns

Macro-narratives unsupported by data

Fake metrics (hallucinated IV, gamma exposure)

Incorrect interpretations of CPI, FOMC minutes, or treasury moves

💡 Intended Use Cases
✔ Recommended

LLM validation inside autonomous trading systems

Dataset labeling for finance critic benchmarks

As an adversarial rater in RLHF pipelines

Filtering flawed rationales before execution

As a research tool for financial safety testing

❌ Not Recommended

Generating trade signals

Acting as a standalone trading algorithm

Replacing human compliance oversight

Operating without risk controls

⚠️ Model Limitations
1. Domain Fragility

MiniCrit-1.5B is highly domain-tuned — outside of financial reasoning, performance may degrade.

2. Non-deterministic Behavior

As with all LLMs, small prompt variations may produce different critiques.

3. Limited Macro Understanding

While it can detect flawed macro arguments, it does not truly understand global macroeconomics.

4. Does Not Guarantee Profitability

The critic reduces hallucination risk but does not create alpha by itself.

🔒 Security, Bias & Ethical Considerations

Model is NOT permitted to output trade instructions

Critiques are adversarial but not malicious

Biases may exist depending on training distribution

Does not circumvent compliance frameworks

Should only be used with human supervision

📜 Citation

Ousley, W. A. (2025). MiniCrit-1.5B: Adversarial Financial Critic Model and 
FinRebut-600 / MiniCrit-12k Datasets (v1.3.x). Zenodo. 
https://doi.org/10.5281/zenodo.17594497

BibTeX:

@dataset{ousley2025minicrit,
  author    = {William A. Ousley},
  title     = {MiniCrit-1.5B: Adversarial Financial Critic Model and Training Datasets},
  year      = {2025},
  version   = {1.3.x},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.17594497},
  url       = {https://doi.org/10.5281/zenodo.17594497}
}

👤 Author & Contact

William Alexander Ousley
AI/ML Researcher — Autonomous Trading Systems
ORCID: https://orcid.org/0009-0009-2503-2010
