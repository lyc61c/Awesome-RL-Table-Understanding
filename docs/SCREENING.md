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

## 第二轮补漏（2026-10-02）

在原 27 篇基础上再查相关论文引用、金融数值推理赛道和通用 RL 的表格实验，补充 15 篇：文本 11 篇、多模态 4 篇。当前共 42 篇（文本 30 / 多模态 12）。各篇实际更新策略、SFT/RL 来源与原文图均已逐项核对；新增内容保持现有 README 版式。

新增检索方向包括 `FinQA GRPO reinforcement learning`、`HiTab policy optimization`、`TabFact multimodal GRPO`、`Vietnamese financial numerical reasoning GRPO`、`table agent reinforcement fine tuning`、`table data long context RLVR`。同时反查 [2026 年表格 QA 综述](https://aclanthology.org/2026.acl-long.557/) 的文献；综述引用仅作线索，纳入依据仍是论文自身的方法和实验。

| 类别 | 本轮新增 |
| --- | --- |
| 文本：表格代理 / 长上下文 | [TableGPT-R1](PAPERS.md#tablegpt-r1)、[TableMind](PAPERS.md#tablemind)、[JT-DA](PAPERS.md#jt-da)、[TableLong](PAPERS.md#tablelong) |
| 文本：金融表格与越南语数值推理 | [Fin-R1](PAPERS.md#fin-r1)、[DianJin-R1](PAPERS.md#dianjin-r1)、[MoFin](PAPERS.md#mofin)、[Program-Centric Policy Optimization](PAPERS.md#vietnamese-program-grpo)、[Two-Stage Training](PAPERS.md#vietnamese-two-stage) |
| 文本：通用 RL 的明确表格训练 | [ACPO](PAPERS.md#acpo)、[Imbalanced Gradients](PAPERS.md#imbalanced-gradients) |
| 多模态 | [Thinking with Tables](PAPERS.md#thinking-with-tables)、[DocR1](PAPERS.md#docr1)、[Tiny-R1V](PAPERS.md#tiny-r1v)、[DeFacto](PAPERS.md#defacto) |

边界说明：DianJin-R1 的 RL 来源是金融选择题，FinQA 仅用于 SFT 和评测；DeFacto 的视觉 WTQ 属于明确评测，未报告 WTQ 专属训练量。TableLong 用合成表格 QA 训练而主要评测长上下文迁移。Tiny-R1V 明确以 WTQ/TabFact 等训练结构数据专家，但主结果未单列这两项留出测试。上述限定已显示在 README 和证据卡。

新增的图均来自所列版本原文。MoFin 使用原文数据构造图；Thinking with Tables 使用工具交互图；Imbalanced Gradients 无独立架构图，明确使用原文 RL 训练诊断图。没有将这些图称为专门的 RL 框图。

### 补查排除与去重

| 论文 | 判断与原文依据 |
| --- | --- |
| [TableMind++](https://arxiv.org/abs/2603.07528) | 延续 TableMind 的 SFT/RAPO 框架，新增重点为推理时记忆修剪、动作精炼及轨迹聚合；作为同一方法家族的扩展在 TableMind 证据卡关联，不重复计数。 |
| [GRIT: Teaching MLLMs to Think with Images](https://arxiv.org/abs/2505.15879) | 原文训练和主评测没有明确表格 QA/TFV/T2T 任务。其他论文把 GRIT 用作 WTQ 基线不能当成 GRIT 自身的表格实验。 |
| [Stronger-MAS](https://arxiv.org/abs/2510.11062) | 原文主要实验为游戏、规划、数学与代码；综述引用并不证明有本仓库核心表格任务实验。 |
| [DiSCo](https://arxiv.org/abs/2602.03491) | 本文的训练为监督学习，GRPO 出现在对照方法；不能把基线的训练算法当作本文方法。 |
| [CSPO: Alleviating Reward Ambiguity for Structured Table-to-LaTeX Generation](https://arxiv.org/abs/2604.10918) | 实际有 RL，但任务为表格识别/LaTeX 结构生成，没有语义 TQA、TFV、T2T 实验。 |
| [APOLLO: An Optimized Training Approach for Long-form Numerical Reasoning](https://arxiv.org/abs/2212.07249) | 有相关 RL 工作，但首次公开于 2022-12，早于窗口；不能因正式发表于 2024 年而改用较晚日期纳入。 |

### 待核实线索

| 论文 | 当前状态 |
| --- | --- |
| [SWING: Weakly Supervised Table Question Answering with Self-training via Reinforcement Learning](https://doi.org/10.1109/BigComp64353.2025.00058) | BigComp 2025；题名与发表信息已核实，尚未获得可公开读取的全文，无法逐项确认 RL 目标、实际训练数据与原图。暂不加入主索引和篇数；[作者所在机构出版记录](https://scholar.pusan.ac.kr/publications/?scholar_id=128190)。 |

本轮仍未核实到应新增的独立 T2T 工作。长答案 QA、程序生成、HTML/LaTeX 重建均没有被改标成 T2T。
