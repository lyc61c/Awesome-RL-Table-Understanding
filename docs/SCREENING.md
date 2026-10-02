# 检索与筛选记录

检索日：2026-10-02（Asia/Shanghai）。主时间窗口：2023-10-02 至 2026-10-02。日期按首次公开时间或可核实的正式发布日期记录；较新的正式版本优先用于方法与数据核对。

## 检索范围

围绕文本表格、视觉表格、多表问答、事实验证、表格到文本分别检索，再从已确认论文的 Related Work 和 References 反查。搜索引擎仅用于发现；算法、数据和方法图的依据来自 arXiv 全文、ACL Anthology、OpenReview、AAAI/CVPR/PMLR 正式论文及作者仓库。

代表性检索词包括：

- `table understanding reinforcement learning 2024 2025 2026`
- `table reasoning GRPO PPO DAPO RLVR`
- `table question answering reinforcement learning`
- `multimodal table understanding reinforcement learning`
- `visual table reasoning perceptual reinforcement learning`
- `table fact verification reinforcement learning`
- `table-to-text reinforcement learning 2025 2026`
- 对 Table-R1、Reasoning-Table、TaREx、Fortune/Formula-R1、TURBO、CoReTab、TaTToo 等标题和别名逐一核对。

这不是按数据库完整导出完成的系统综述，不能保证没有遗漏。检索未核实到的空档不代表该年份没有相关工作。

## 代表性排除项

| 论文 | 原文依据 / 排除理由 |
| --- | --- |
| [Chain-of-Table: Evolving Tables in the Reasoning Chain for Table Understanding](https://arxiv.org/abs/2401.04398) | 通过 in-context prompting 迭代生成操作与更新表格，没有本文新增的 RL 策略训练。 |
| [H-STAR: LLM-driven Hybrid SQL-Text Adaptive Reasoning on Tables](https://arxiv.org/abs/2407.05952) | 混合 SQL/文本推理的提示与工具框架，未以 RL 更新策略。 |
| [Utilizing Training Data to Improve LLM Reasoning for Tabular Understanding](https://arxiv.org/abs/2508.18676) | 从错误中提取可检索的提示条件；学习的是提示经验，未做策略梯度 RL 后训练。 |
| [From Cells to Sentences: An End-to-End Framework for Table Understanding](https://proceedings.mlr.press/v300/vijaykeerthy26a.html) | 全文 Training Objective 为生成、去噪、对齐等损失的联合优化；未核实到实际 RL 更新，RL 只在参考文献出现。 |
| [TableDART: Dynamic Adaptive Multi-Modal Routing for Table Understanding](https://arxiv.org/abs/2509.14671) | §3 的门控网络按专家经验准确率构造监督分布并用 KL 训练；出现 policy/router 术语不等于 RL。 |
| [TABQAWORLD: Optimizing Multimodal Reasoning for Multi-Turn Table Question Answering](https://arxiv.org/abs/2604.03393) | 摘要明确为 training-free 框架，没有本文 RL 训练。 |
| [TRivia: Self-supervised Fine-tuning of Vision-Language Models for Table Recognition](https://arxiv.org/abs/2512.01248) | 有 GRPO，但目标与实验是表格识别/结构识别；没有本仓库核心 TQA、TFV、T2T 任务。 |
| [An Automatic Prompt Generation System for Tabular Data Tasks](https://arxiv.org/abs/2405.05618) | 有 RL 列选择器，但任务为数据填补、错误检测和实体匹配，不在核心任务范围。 |
| [A Table-to-Text Framework with Heterogeneous Multidominance Attention and Self-Evaluated Multi-Pass Deliberation](https://aclanthology.org/2023.findings-emnlp.44/) | §3 的优化是 MLE 与对比排序损失；RL 在相关工作被讨论，本文不采用。 |
| [Enabling controllable table-to-text generation via prompting large language models with guided planning](https://doi.org/10.1016/j.knosys.2024.112571) | Poised 使用 BART 前缀调优规划和 LLM 提示生成；搜索页面中有关 RL 的文字来自推荐的其他文章，不能据此纳入。 |

## 有条件纳入的边界

以下条目仍有实际 RL 训练，但不能和普通表格回答模型混为一谈：

- **TaTToo**：RL 训练的是工具增强的过程验证器/PRM，用于表格推理轨迹评估与搜索。
- **When LLMs Read Tables Carelessly / Critic-4B**：GRPO 训练表格引用错误检测 critic，推理时过滤回答片段；不更新答案生成模型。原文 Fig.6 是 critic 提示示意，未给出单独 RL 架构图。
- **Question Answering with Texts and Tables through Deep Reinforcement Learning**：DQN/PPO 训练模块调度控制器，底层检索器与阅读器固定。
- **RE-Tab**：主方法 training-free；只因最新版本 §4.3 / Appendix G.3 明确执行 GRPO proof-of-concept 才收录。图展示确定性状态奖励机制，不是单独的 GRPO 流程图。
- **MTabVQA**：主要 TableVision 方法为 SFT；收录的是 Appendix G 的 Qwen2.5-VL-3B GRPO 实验分支。方法图为基准构造流程，论文没有单列 RL 架构图。
- **Sparks of Tabular Reasoning via Text2SQL Reinforcement Learning**：SQL 执行 RL 后明确检验 TQA 迁移能力；单纯 SQL 生成论文不自动纳入。
- **Mixture-of-Retrieval Experts / R1-Router**：通用跨知识库检索代理，因包含明确的表格 QA RL 训练与实验而纳入。

## 任务与数据标注原则

FeTaQA、M3TQA 的 open-ended QA 不因答案是长文本就被改标为 T2T。ToTTo 只有在用于表格文本生成时才支持 T2T 标签；用于 HTML/结构重建时记作感知或重建训练。Reasoning-Table 的 T2T 单数据集实验使用相应奖励，按该明确任务证据记录。

某篇同时评测 TQA 和 TFV 不意味着两个任务都参与了 RL 训练。SFT 合成数据、RL 训练来源、测试/域外基准分别列在证据卡中。图号与页码固定到条目所列 PDF，并保留 SHA256。
