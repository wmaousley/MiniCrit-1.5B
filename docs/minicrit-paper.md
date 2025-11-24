# MiniCrit-1.5B: An Adversarial Financial Critique Model for Trading Rationale Evaluation
**William Ousley**  
**Antagon Labs — AI/ML Systems for Trading and Safety**  
**founders@antagon.ai**

---

## Abstract
Large language models (LLMs) increasingly support the decision-making pipelines of quantitative trading systems. However, most conventional LLMs are optimized to be compliant rather than adversarial, often failing to identify weak reasoning, missing assumptions, or hallucinated conclusions inside trading rationales. This gap exposes algorithmic trading agents to silent failure modes where flawed reasoning passes through unchallenged.

We introduce **MiniCrit-1.5B**, a compact adversarial financial-critic language model designed to detect reasoning errors, flawed logic chains, unsupported claims, and hallucinations within financial explanations. MiniCrit-1.5B is trained on two curated datasets of trading rationales and adversarial critiques: **MiniCrit-Training-12k** and **FinRebut-600**, enabling the system to evaluate reasoning quality across equities, macro topics, news-driven catalysts, and algorithmic decision pipelines.

Our results show that MiniCrit-1.5B achieves strong performance on financial reasoning critique tasks, obtaining **0.82 Weak Reasoning F1** and **0.76 Hallucination Detection F1**, outperforming comparably sized open-source baselines. We release the model, datasets, evaluation suite, and training code to support research on LLM safety in trading environments.

---

# 1. Introduction

## 1.1 Motivation
Financial decision systems increasingly integrate LLMs to:
- Summarize market conditions  
- Explain algorithmic trading actions  
- Justify buy/sell decisions  
- Interpret news catalysts  
- Evaluate risks and scenario probabilities  

While LLMs provide interpretability and natural-language interfaces, they also introduce new risks:
- **Weak reasoning** that appears coherent but is logically incorrect  
- **Hallucinated data points or fake statistics**  
- **Overconfidence in low-certainty predictions**  
- **Cherry-picked rationales that mislead human oversight**  

These behaviors are catastrophic in trading systems, where a single flawed rationale may produce millions in downstream losses.

MiniCrit aims to **attack** a rationale and reveal its failure points, similar to a human red-team financial analyst.

## 1.2 Contributions
This paper provides four key contributions:

1. **MiniCrit-1.5B**, a lightweight adversarial critic model optimized for financial reasoning evaluation.  
2. **MiniCrit-Training-12k**, the largest open dataset of adversarial critiques on trading rationales.  
3. **FinRebut-600**, a high-quality evaluation set with structured error annotations.  
4. **A reproducible benchmark suite** for reasoning-error detection in financial contexts.

The full pipeline is open-source and suitable for risk-aware trading agents, interpretability research, and LLM safety work.

---

# 2. Background and Related Work

## 2.1 LLM reasoning issues in finance
Unlike deterministic algorithms, LLMs:
- Produce variable explanations  
- Often generate plausible but incorrect arguments  
- Struggle with multi-step financial logic  
- Show overconfidence in uncertain market outcomes  

Existing reinforcement learning systems rarely incorporate **reasoning validation modules**.

## 2.2 Critique models
Recent work explores “critic models” for:
- Chain-of-Thought review  
- Hallucination detection  
- Self-consistency evaluation  

However:
- Few focus on **financial domains**  
- No open-source adversarial critic models exist for trading rationales  
- Datasets are scarce  

MiniCrit fills this gap.

---

# 3. MiniCrit Model Architecture

## 3.1 Base Model
MiniCrit-1.5B builds on:
- A compact decoder-only transformer  
- ~1.5B parameters  
- Rotary embeddings  
- BFloat16 training  
- Optimized for critique style and adversarial reasoning  

## 3.2 Adversarial instruction tuning
The model is trained to:
- Decompose arguments  
- Identify unsupported claims  
- Challenge assumptions  
- Detect hallucinations  
- Point out missing context  
- Attack flawed logical chains  

## 3.3 Critique reasoning format
The model outputs:
- **Error Classifications**  
- **Evidence Quotes**  
- **Logical Fallacy Detection**  
- **Alternative Interpretations**  
- **Confidence Estimates**  

---

# 4. Datasets

## 4.1 MiniCrit-Training-12k
12,000 samples including:
- Alpaca-style trading rationales  
- LLM-generated explanations  
- Human-written rationales  
- Adversarial critiques  
- Multi-turn correction cycles  

Annotations include:
- Logical errors  
- Data hallucinations  
- Narrative inconsistencies  
- Market knowledge gaps  

## 4.2 FinRebut-600
600 curated high-quality samples:
- More rigorous error labels  
- Reasoning fallacies (e.g., post-hoc, anchoring, sunk cost)  
- Financial domain checks  
- Missing data detection  

FinRebut-600 serves as the primary test set.

---

# 5. Training Setup

## 5.1 Hardware
Training utilized:
- A100 GPUs (Lambda Labs)  
- Gradient accumulation for large sequence lengths  
- FlashAttention for efficient long-context critique tasks  

## 5.2 Optimization
- AdamW optimizer  
- Cosine learning rate schedule  
- KL penalty for stability  
- Adversarial sampling of flawed rationales  

## 5.3 Evaluation
We evaluate on:
- Reasoning error detection  
- Hallucination detection  
- Critique completeness  
- Few-shot correction quality  
- Scalability vs. larger models (7B–70B)  

---

# 6. Results

## 6.1 Quantitative Metrics

| Metric | MiniCrit-1.5B | Baseline 7B Models |
|--------|----------------|---------------------|
| Weak Reasoning F1 | **0.82** | 0.55–0.67 |
| Hallucination Detection F1 | **0.76** | 0.48–0.61 |
| Critique Precision | **0.79** | 0.52 |
| Critique Recall | **0.85** | 0.67 |

MiniCrit substantially outperforms larger models due to targeted adversarial training.

## 6.2 Qualitative Observations
MiniCrit:
- Provides deeper, more hostile critiques  
- Detects hidden assumptions missed by standard models  
- Offers realistic counterarguments  
- Is less likely to “agree” with flawed reasoning  
- Identifies ambiguous market logic and missing conditions  

---

# 7. Use Cases

## 7.1 Trading agent supervision
MiniCrit acts as a “reasoning firewall” before a trade is executed.

## 7.2 Risk management systems
Detecting:
- Overconfident statements  
- Unsupported predictions  
- Market hallucinations  

## 7.3 Dataset auditing
MiniCrit helps identify contaminated, low-quality rationales.

## 7.4 LLM safety & governance
Models producing financial advice can be evaluated for:
- Safety violations  
- Misleading claims  
- Unsupported reasoning  

---

# 8. MiniCrit Model Card

## 8.1 Intended Use
- Critiquing trading rationales  
- Evaluating LLM reasoning safety  
- Supporting autonomous trading oversight  

## 8.2 Limitations
- Not a predictive model  
- Not a financial advisor  
- Should not be the sole risk control mechanism  
- Sensitive to poorly structured inputs  

## 8.3 Ethical considerations
Financial reasoning errors may cause real-world harm. MiniCrit aims to reduce, not eliminate, systemic trading risks.

---

# 9. Societal Impact Statement
LLMs in financial domains influence markets, retail behaviors, and automated trading frameworks. MiniCrit contributes to safer AI systems by:
- Identifying hallucinations  
- Enforcing reasoning standards  
- Improving interpretability  

However, adversarial critics may themselves produce false negatives or false positives. Human oversight is required.

---

# 10. Future Work
- Scaling to 7B and 13B critic variants  
- Multi-agent critique systems  
- Integration with real-time market feeds  
- Reinforcement learning from critique signals  
- Finance-specific chain-of-thought validation  

---

# 11. Conclusion
MiniCrit-1.5B introduces a powerful adversarial critic for financial reasoning. By attacking flawed trading rationales, MiniCrit helps build safer, more robust AI trading systems. We release the full model, datasets, training code, and benchmarks to support ongoing research in financial LLM safety.

---

# References
1. Raffel et al. “Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer.”  
2. OpenAI. “GPT-4 System Card.”  
3. Google DeepMind. “Socratic Models for Reasoning.”  
4. Anthropic. “Constitutional AI.”  
5. Lo, A. “Adaptive Markets.”  
6. Ousley, W. “FinRebut-600 Dataset.” (Zenodo, forthcoming)  
7. Ousley, W. “MiniCrit-Training-12k Dataset.” (Zenodo, forthcoming)
