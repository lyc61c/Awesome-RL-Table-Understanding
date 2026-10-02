# Awesome RL for Table Understanding

> 用强化学习训练表格理解模型：文本表格与多模态表格，覆盖 TQA、TFV、T2T。

## 🌟 Overview

- [收录标准与任务定义](#scope)
- [文本表格理解](#text-table-understanding)
- [多模态表格理解](#multimodal-table-understanding)
- [任务索引](#task-index)
- [逐篇证据卡](docs/PAPERS.md)
- [排除与边界记录](docs/SCREENING.md)
- [独立核对记录](docs/AUDIT.md)
- [结构化数据](data/papers.json) · [CSV 索引](data/papers.csv) · [图片来源](img/README.md)

<a id="scope"></a>
## 📌 收录标准与任务定义

只收录论文中确实执行了 **RL 策略更新**、并用于表格理解任务的工作。可包含 GRPO、PPO、DQN、DAPO 及其变体，也包含 RL 训练的表格检索调度器或过程验证器；条目会标明训练对象。仅提示、SFT、蒸馏、奖励打分/搜索而无 RL 更新的工作不收录。DPO-only、纯图表 QA、仅 OCR/表格结构识别、仅 Text-to-SQL 且没有表格理解实验的论文不计入主索引。

| 缩写 | 本仓库定义 |
| --- | --- |
| TQA | Table Question Answering，包含短答案、数值推理、自由形式回答、多表与开放域表格问答。 |
| TFV | Table Fact Verification，判断声明是否受表格支持。 |
| T2T | Table-to-Text，不依赖显式问题的表格描述或生成任务。FeTaQA 的自由形式回答仍标 TQA。 |

分类依据是 **模型实际输入**：序列化表格、SQL/DataFrame、表格+文字属于文本表格；直接接收表格图像/截图的 VLM 属于多模态表格。数据集名字含 “MultiModal” 不足以决定分类。任务标签表示论文涉及的任务，可能只作域外评测；**不能据此推断该任务参与 RL 训练**。训练数据列单独区分 SFT 与 RL。

日期原则为首次公开时间，正式会议/期刊列在标题下；无法核实预印本日期时使用正式发布日期并注明。采用较新的可核实版本，同名论文与更名版本分别去重。未核实的代码链接记为“未核实”。这是截至检索日的可核实清单，不声称穷尽所有论文。

<a id="text-table-understanding"></a>
## 🔥 文本表格理解

### [When LLMs Read Tables Carelessly: Measuring and Reducing Data Referencing Errors](https://aclanthology.org/2026.acl-long.762/)

**2026-06-30** · ACL 2026 Main · `TQA / TFV` · [GitHub](https://github.com/ayyyq/table-referencing) · [证据卡](docs/PAPERS.md#dre-critic)

<p align="center"><a href="img/dre-critic.png"><img src="img/dre-critic.png" width="1000" alt="When LLMs Read Tables Carelessly: Measuring and Reducing Data Referencing Errors method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>SFT + RLVR / GRPO</strong><br>训练 Critic-4B 检测推理片段中的单元格误引与遗漏。先蒸馏 Sonnet-3.7 判断做 SFT，再以经核验的 True/False 标签为奖励做 GRPO；推理时用 critic 过滤候选或局部拒绝采样，从而减少错误数据引用。<br>⚑ RL 训练表格引用错误 critic；原图为 critic 提示示意，论文未单列 RL 架构图。</td><td valign="top"><strong>RL：</strong>同一 WTQ 响应片段来源的 5,712 条，GRPO 20 epochs、每题 8 rollouts。另有规则插入四类 DRE 的 synthetic critic 对照。<br><br><strong>SFT：</strong>WTQ 训练集上 Qwen3-8B 生成的响应片段；Sonnet-3.7 标注的 2,000 条正负平衡样本，SFT 2 epochs。</td></tr>
</tbody>
</table>

---

### [What are Key Factors for Updates in RL for LLM Reasoning?](https://arxiv.org/abs/2606.22570)

**2026-06-21** · arXiv · `TQA` · [GitHub](https://github.com/Control-derek/ACPO) · [证据卡](docs/PAPERS.md#acpo)

<p align="center"><a href="img/acpo.png"><img src="img/acpo.png" width="1000" alt="What are Key Factors for Updates in RL for LLM Reasoning? method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>Adaptive Clip Policy Optimization（ACPO）</strong><br>分析 rollout 后更新次数导致的重要性采样与梯度偏移；按行为 token 概率分组，以各组重要性比率的经验方差动态设置裁剪边界。使用 GRPO 类相对优势，分别训练表格 QA、数学与逻辑推理模型。</td><td valign="top"><strong>RL：</strong>表格 QA 实验单独在 HiTab 上训练；其他实验分别使用 ORZ 57K 数学数据与 Countdown。未报告 HiTab 最终训练子集数量。<br><br><strong>SFT：</strong>未新增 SFT；从 Qwen 系列模型进行 RL。</td></tr>
</tbody>
</table>

---

### [RSAT: Structured Attribution Makes Small Language Models Faithful Table Reasoners](https://arxiv.org/abs/2605.00199)

**2026-04-30** · ACL 2026 SURGeLLM Workshop (accepted; arXiv v2) · `TQA / TFV` · [GitHub](https://github.com/JugalGajjar/RSAT) · [证据卡](docs/PAPERS.md#rsat)

<p align="center"><a href="img/rsat.png"><img src="img/rsat.png" width="1000" alt="RSAT: Structured Attribution Makes Small Language Models Faithful Table Reasoners method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>SFT + GRPO</strong><br>先用带单元格坐标引用的 JSON 推理轨迹做 SFT，再用 GRPO 优化答案 F1、引用坐标有效性、DeBERTa NLI 证据蕴含分数和引用简约性，并对无效 JSON 惩罚；使小模型的每步推理可追溯到表格单元格。</td><td valign="top"><strong>RL：</strong>相同三个数据集的 table-question-answer 池；候选训练池 38,647 条，但每个模型实际抽取 500 条进行 GRPO。<br><br><strong>SFT：</strong>WikiTableQuestions、FeTaQA、TabFact；Claude Opus 4.5 生成 1,000 条轨迹，训练 900 条（630/135/135），验证 100 条。</td></tr>
</tbody>
</table>

---

### [Probing How Scalable Table Data Enhances General Long-Context Reasoning](https://arxiv.org/abs/2603.21719)

**2026-03-23** · arXiv · `TQA` · 代码：未核实 · [证据卡](docs/PAPERS.md#tablelong)

<p align="center"><a href="img/tablelong.png"><img src="img/tablelong.png" width="1000" alt="Probing How Scalable Table Data Enhances General Long-Context Reasoning method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>GRPO / RLVR</strong><br>把真实表格组织成可执行 SQL 环境，合成检索、计算与跨表关联问题；用 SQL 执行答案验证奖励，并保留成功率介于 0 与 1 的训练题。以 GRPO 训练长上下文推理模型。<br>⚑ 表格 QA 用于 RL 训练，主要评测通用长上下文迁移；未报告标准 TQA 基准结果。</td><td valign="top"><strong>RL：</strong>TableLong 合成 QA：BIRD、CoSQL、Spider 及文档抽取得到的 10,000+ 表格；每题组合 1–30 张表，构造中英双语、最长约 32K 上下文。未单列最终 QA 对总数。<br><br><strong>SFT：</strong>未新增 SFT；从 Qwen / DeepSeek-R1-Distill 系列模型直接进行 RL。</td></tr>
</tbody>
</table>

---

### [TaREx: Reinforcement Learning for Code-Driven Table Reasoning](https://ojs.aaai.org/index.php/AAAI/article/view/40415)

**2026-03-14** · AAAI 2026 · `TQA / TFV / Data Analysis` · 代码：未核实 · [证据卡](docs/PAPERS.md#tarex)

<p align="center"><a href="img/tarex.png"><img src="img/tarex.png" width="1000" alt="TaREx: Reinforcement Learning for Code-Driven Table Reasoning method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>GRPO + DAPO clip-higher</strong><br>统一用 DataFrame 表示不同结构的表格，让策略在最多五轮交互中生成 Python、读取执行反馈并作答。使用 GRPO 的组内优势和 DAPO 非对称裁剪，以格式与答案奖励训练；过滤超时、无效和停滞轨迹来稳定更新。</td><td valign="top"><strong>RL：</strong>过滤后的 WikiTQ 9,472、MultiHiertt 5,119、FinQA 4,333、TAT-QA 8,085、HiTab 4,888、TabFact 15,087 条（共 46,984）。<br><br><strong>SFT：</strong>无额外 SFT 或蒸馏，直接对 Qwen2.5-7B-Instruct 做 RL。</td></tr>
</tbody>
</table>

---

### [Replacing Multi-Step Assembly of Data Preparation Pipelines with One-Step LLM Pipeline Generation for Table QA](https://arxiv.org/abs/2602.22721)

**2026-02-26** · arXiv · `TQA / TFV` · [GitHub](https://github.com/ZJU-DAILY/Operation-R1) · [证据卡](docs/PAPERS.md#operation-r1)

<p align="center"><a href="img/operation-r1.png"><img src="img/operation-r1.png" width="1000" alt="Replacing Multi-Step Assembly of Data Preparation Pipelines with One-Step LLM Pipeline Generation for Table QA method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>ORPO (Operation-wise Group Relative Policy Optimization)</strong><br>一次生成 select/filter/sort/group/add-column 操作流水线，ORPO 用答案信息保留率、行列压缩和长度奖励训练预处理策略，并按组内奖励质量与方差重采样。推理时合并候选操作树、逐步回滚，交给下游模型作答。</td><td valign="top"><strong>RL：</strong>主实验：WikiTQ 过滤后 5,403 条 cell-focused 样本，按 19:1 划分训练/验证。额外数据源实验：TabFact 5,000 条，LLM 标注终端推理所需单元格并做难度过滤。<br><br><strong>SFT：</strong>未报告额外 SFT；初始化 Qwen3 模型后用 LoRA 做 RL。</td></tr>
</tbody>
</table>

---

### [Enhancing Table Reasoning with Deterministic Table-State Rewards](https://arxiv.org/abs/2601.22530)

**2026-01-30** · arXiv (v2 2026-05-15) · `TQA` · [GitHub](https://github.com/ThomasK1018/RE_Tab) · [证据卡](docs/PAPERS.md#re-tab)

<p align="center"><a href="img/re-tab.png"><img src="img/re-tab.png" width="1000" alt="Enhancing Table Reasoning with Deterministic Table-State Rewards method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>GRPO proof-of-concept (main RE-Tab framework is training-free)</strong><br>将操作后的中间表序列化为 header-is-value 文本，以查询与状态的最长公共子序列除以状态长度构成 TabROUGE 奖励。主框架用它指导推理和轨迹选择；v2 另用该确定性奖励对 Qwen3-8B 进行 GRPO 后训练。<br>⚑ 仅纳入 v2 的 GRPO 实验；主框架为 training-free。</td><td valign="top"><strong>RL：</strong>WikiTQ：200 条；MMQA：92 条；MMTU：92 条。WikiTQ/MMQA 训练 300 steps，MMTU 因 OOM 训练 150 steps（Appendix G.3）。<br><br><strong>SFT：</strong>该 GRPO 实验未报告额外 SFT 阶段。</td></tr>
</tbody>
</table>

---

### [ReasonTabQA: A Comprehensive Benchmark for Table Question Answering from Real World Industrial Scenarios](https://arxiv.org/abs/2601.07280)

**2026-01-12** · arXiv · `TQA` · 代码：未核实 · [证据卡](docs/PAPERS.md#reasontabqa)

<p align="center"><a href="img/reasontabqa.png"><img src="img/reasontabqa.png" width="1000" alt="ReasonTabQA: A Comprehensive Benchmark for Table Question Answering from Real World Industrial Scenarios method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>TabCodeRL / DAPO</strong><br>用双语工业表格的 thinking 或 no-thinking 轨迹做冷启动，再用 DAPO 优化 Python 推理。奖励组合代码提取、执行与答案的分段分数、表路径选择，以及组内代码语义相似度，给复杂多表推理提供更细的反馈。</td><td valign="top"><strong>RL：</strong>ReasonTabQA 训练部分的另一半，使用金标答案计算 TabCodeRL 奖励；原文未提供取整后的各子集准确样本数。<br><br><strong>SFT：</strong>ReasonTabQA：总体 1,932 个标注实例，按 8:2 划分训练/测试；训练部分的一半用于 SFT，按模型选择 thinking 或 no-thinking 轨迹。</td></tr>
</tbody>
</table>

---

### [TableGPT-R1: Advancing Tabular Reasoning Through Reinforcement Learning](https://arxiv.org/abs/2512.20312)

**2025-12-23** · arXiv · `TQA / TFV` · 代码：未核实 · [证据卡](docs/PAPERS.md#tablegpt-r1)

<p align="center"><a href="img/tablegpt-r1.png"><img src="img/tablegpt-r1.png" width="1000" alt="TableGPT-R1: Advancing Tabular Reasoning Through Reinforcement Learning method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>SFT + 三阶段 GRPO++</strong><br>以少量 SFT 热启动，再按通用推理、表格工具交互和困难样本三阶段训练。GRPO++ 使用序列重要性权重、解耦裁剪和熵正则；奖励结合可执行答案规则、注入评价标准的模型评判及中间代码执行反馈。</td><td valign="top"><strong>RL：</strong>公开通用推理数据 + 合成表格代理 QA；通过多模型答案一致性筛选及 pass@k 难度过滤进入后续阶段。原文未完整公开各数据集名称与分项数量。<br><br><strong>SFT：</strong>约占整体训练池 3% 的热启动样本；训练池绝对规模未报告。</td></tr>
</tbody>
</table>

---

### [JT-DA: Enhancing Data Analysis with Tool-Integrated Table Reasoning Large Language Models](https://arxiv.org/abs/2512.06859)

**2025-12-07** · arXiv · `TQA` · [GitHub](https://github.com/JT-LM/JT-DA-8B) · [证据卡](docs/PAPERS.md#jt-da)

<p align="center"><a href="img/jt-da.png"><img src="img/jt-da.png" width="1000" alt="JT-DA: Enhancing Data Analysis with Tool-Integrated Table Reasoning Large Language Models method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>多模式 SFT + GRPO</strong><br>构造文本 CoT、程序 PoT 与交织 ICoT 的表格分析轨迹，经质量评分和任务平衡后做 SFT；再对新的表格任务用无 KL 的 token 级 GRPO，以回答正确性和推理格式奖励提升沙箱工具推理。</td><td valign="top"><strong>RL：</strong>约 3,000 条未用于此前训练阶段的新表格任务 QA；提供部分结构与 CSV 路径，支持沙箱读取大表。<br><br><strong>SFT：</strong>汇集 29 个公开表格数据集（如 AIT-QA、ToTTo、HybridQA、TableBench）及约 300 万张原始表，合成并筛选 34 类任务轨迹；300 万是表格数，并非最终 SFT 样本数。</td></tr>
</tbody>
</table>

---

### [STaR: Towards Effective and Stable Table Reasoning via Slow-Thinking Large Language Models](https://arxiv.org/abs/2511.11233)

**2025-11-14** · The Web Conference 2026 · `TQA / TFV` · [GitHub](https://github.com/ustc-table-mining/STaR) · [证据卡](docs/PAPERS.md#star)

<p align="center"><a href="img/star.png"><img src="img/star.png" width="1000" alt="STaR: Towards Effective and Stable Table Reasoning via Slow-Thinking Large Language Models method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>Difficulty-aware enhanced GRPO (DAPO variant)</strong><br>自验证筛选慢思考轨迹做 SFT，随后用带非对称裁剪的 GRPO 先训练容易样本，再动态筛选困难样本。格式、部分重合与完整答案奖励缓解稀疏反馈；推理时融合 token 置信度和答案一致性选择轨迹。</td><td valign="top"><strong>RL：</strong>相同三个数据集的训练划分，依据 pass@k 分为 easy/hard，并对 hard 子集动态筛选。<br><br><strong>SFT：</strong>WikiTableQuestions、HiTab、FinQA 的训练划分，经自验证的慢思考轨迹。</td></tr>
</tbody>
</table>

---

### [Mixture-of-Minds: Multi-Agent Reinforcement Learning for Table Understanding](https://aclanthology.org/2026.acl-long.112/)

**2025-10-23** · ACL 2026 Main · `TQA / TFV / Data Analysis` · [GitHub](https://github.com/Tonyzhou98/mixture-of-minds) · [证据卡](docs/PAPERS.md#mixture-of-minds)

<p align="center"><a href="img/mixture-of-minds.png"><img src="img/mixture-of-minds.png" width="1000" alt="Mixture-of-Minds: Multi-Agent Reinforcement Learning for Table Understanding method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>Sequential multi-agent GRPO</strong><br>把表格推理拆成规划、代码执行、作答三个代理。MCTS 式分支采样从答对的路径回溯出伪金标计划与代码，再依次用 GRPO 优化三个代理；奖励分别衡量计划相似度、代码执行与操作质量、最终答案正确性。</td><td valign="top"><strong>RL：</strong>TableInstruct：4,897 个去重 QA，经答案一致性与人工核对清洗；MCTS 式 rollout 生成计划、代码、答案训练实例。<br><br><strong>SFT：</strong>本文代理训练流程未单列额外 SFT 阶段；成功 rollout 生成的伪金标用于 GRPO 奖励。</td></tr>
</tbody>
</table>

---

### [Imbalanced Gradients in RL Post-Training of Multi-Task LLMs](https://aclanthology.org/2026.findings-eacl.164/)

**2025-10-22** · Findings of EACL 2026 · `TQA` · 代码：未核实 · [证据卡](docs/PAPERS.md#imbalanced-gradients)

<p align="center"><a href="img/imbalanced-gradients.png"><img src="img/imbalanced-gradients.png" width="1000" alt="Imbalanced Gradients in RL Post-Training of Multi-Task LLMs method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>GRPO / RLVR；任务采样对比</strong><br>研究多任务 RL 中各任务梯度尺度不均衡：在 FinQA、数学、代码与算术混合训练中比较均匀采样和按梯度范数分配的采样，分析采样权重如何影响各任务学习。没有提出新的表格专用 RL 算法。<br>⚑ 通用 RL 训练实证研究，包含 FinQA；图为训练诊断，非 RL 架构图。</td><td valign="top"><strong>RL：</strong>跨域混合：FinQA、R1-Code、Countdown、MATH；另有 DeepScaleR/MATH/Arithmetic 单域分析。原文未统一给出最终训练池数量。<br><br><strong>SFT：</strong>未新增 SFT；从 Qwen2.5 / Llama-3.2 指令模型进行 RL。</td></tr>
</tbody>
</table>

---

### [TaTToo: Tool-Grounded Thinking PRM for Test-Time Scaling in Tabular Reasoning](https://openreview.net/forum?id=zc1ezBrr5m)

**2025-10-07** · ICLR 2026 · `TQA / TFV / Data Analysis` · 代码：未核实 · [证据卡](docs/PAPERS.md#tattoo)

<p align="center"><a href="img/tattoo.png"><img src="img/tattoo.png" width="1000" alt="TaTToo: Tool-Grounded Thinking PRM for Test-Time Scaling in Tabular Reasoning method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>Modified GRPO with dense step-level reward shaping</strong><br>训练可生成验证理由、调用 Python/SQL 与表格检索工具的 PRM。SFT 学会区域前缀与工具验证，再用 GRPO 优化标签匹配、置信度校准及工具证据支持；推理时给回答策略的候选轨迹打分，支持 Best-of-N 和树搜索。<br>⚑ RL 训练的是过程验证器/PRM。</td><td valign="top"><strong>RL：</strong>上述合成的步级验证语料中 10K（Table 8），用于 PRM 的 GRPO；训练对象是验证器。<br><br><strong>SFT：</strong>TableInstruct、HybridQA、ToTTo、WikiTQ 的专家推理轨迹，经 LLM/人工核验和工具调用合成约 60K 步级验证实例；Table 8 的 SFT 阶段使用 50K。</td></tr>
</tbody>
</table>

---

### [Two-Stage Training with Reinforcement Learning for Vietnamese Financial Numerical Reasoning](https://aclanthology.org/2025.vlsp-1.28/)

**2025-10** · VLSP 2025 · `TQA` · 代码：未核实 · [证据卡](docs/PAPERS.md#vietnamese-two-stage)

<p align="center"><a href="img/vietnamese-two-stage.png"><img src="img/vietnamese-two-stage.png" width="1000" alt="Two-Stage Training with Reinforcement Learning for Vietnamese Financial Numerical Reasoning method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>LoRA SFT + GRPO</strong><br>Qwen3 先学习越南语金融程序生成，再以 GRPO 强化：程序执行失败为 −2、执行答案正确为 +1、其他为 0。最终方案保留完整 Markdown 表格及前后文，避免检索裁剪丢失运算依据。</td><td valign="top"><strong>RL：</strong>同一 VLSP train（2,993 条），在 SFT 后进行一轮 GRPO；每提示采样 4 个程序。<br><br><strong>SFT：</strong>VLSP 2025 Vietnamese Financial Numerical Reasoning train：2,993 条，含翻译 FinQA 和越南语财务报告来源。</td></tr>
</tbody>
</table>

---

### [MoFin: A Small Vietnamese Language Model for Financial Reasoning via Reinforcement Learning](https://aclanthology.org/2025.vlsp-1.27/)

**2025-10** · VLSP 2025 · `TQA` · 代码：未核实 · [证据卡](docs/PAPERS.md#mofin)

<p align="center"><a href="img/mofin.png"><img src="img/mofin.png" width="1000" alt="MoFin: A Small Vietnamese Language Model for Financial Reasoning via Reinforcement Learning method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>CoT SFT + GRPO</strong><br>翻译并核验 FinQA 金融表格与推理程序，蒸馏执行正确的 CoT 后做 LoRA SFT；GRPO 结合格式、程序匹配和执行结果奖励，提升越南语金融数值推理。<br>⚑ 图为原文数据构造流程，论文未单独绘制 RL 架构图。</td><td valign="top"><strong>RL：</strong>从上述金融 QA 池按提示长度筛选（第 19 百分位阈值）后做 GRPO；未单列最终 RL 数量。<br><br><strong>SFT：</strong>VLSP 官方 540 条 + 翻译 FinQA 3,247 条，含蒸馏 CoT。§3.3.1 报告总数 3,747，但分项合计 3,787，原文不一致。</td></tr>
</tbody>
</table>

---

### [Enhancing Numerical Reasoning in Vietnamese Financial Question Answering through Program-Centric Policy Optimization](https://aclanthology.org/2025.vlsp-1.26/)

**2025-10** · VLSP 2025 · `TQA` · [GitHub](https://github.com/duccd4/vlsp2025-financial-numerical-reasoning) · [证据卡](docs/PAPERS.md#vietnamese-program-grpo)

<p align="center"><a href="img/vietnamese-program-grpo.png"><img src="img/vietnamese-program-grpo.png" width="1000" alt="Enhancing Numerical Reasoning in Vietnamese Financial Question Answering through Program-Centric Policy Optimization method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>CoNR SFT + PCPO 奖励 / GRPO</strong><br>教师模型生成 Chain-of-Numerical-Reasoning 轨迹供 SFT；GRPO 用程序可执行性、答案匹配和简洁性组成 PCPO 奖励，先通过有效程序门控，再优化数值正确性与输出长度。PCPO 是奖励设计，实际优化算法为 GRPO。</td><td valign="top"><strong>RL：</strong>上述金融问答训练池用于程序中心 GRPO；未单列 RL 筛选后样本数。<br><br><strong>SFT：</strong>VLSP 2025 train（2,993）+ 越南语翻译并程序重增强的 FinQA，论文报告 CoNR SFT 共 14,661 条。</td></tr>
</tbody>
</table>

---

### [TableMind: An Autonomous Programmatic Agent for Tool-Augmented Table Reasoning](https://arxiv.org/abs/2509.06278)

**2025-09-08** · arXiv（v4 原文标注 WSDM 2026） · `TQA / TFV` · [GitHub](https://github.com/ustc-table-mining/TableMind) · [证据卡](docs/PAPERS.md#tablemind)

<p align="center"><a href="img/tablemind.png"><img src="img/tablemind.png" width="1000" alt="TableMind: An Autonomous Programmatic Agent for Tool-Augmented Table Reasoning method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>轨迹 SFT + RAPO</strong><br>代理循环执行规划、Python 工具调用与反思。少量正确轨迹热启动后，RAPO 增强被当前策略低估的高质量轨迹优势；联合格式、答案准确性、工具成功及轮次成本奖励训练自主表格推理。</td><td valign="top"><strong>RL：</strong>按 Table 1：TabFact 3,500 + TabMWP 3,500 + WikiTQ 1,000，共 8,000；正文对来源的描述存在不一致，见证据卡。<br><br><strong>SFT：</strong>200 条经过筛选的合成多轮工具推理轨迹。</td></tr>
</tbody>
</table>

---

### [M3TQA: Massively Multilingual Multitask Table Question Answering](https://aclanthology.org/2026.findings-acl.1134/)

**2025-08-22** · Findings of ACL 2026 · `TQA / TFV` · [GitHub（占位，训练代码未发布）](https://github.com/sdxvv/m3TQA) · [证据卡](docs/PAPERS.md#m3tqa)

<p align="center"><a href="img/m3tqa.png"><img src="img/m3tqa.png" width="1000" alt="M3TQA: Massively Multilingual Multitask Table Question Answering method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>SFT followed by GRPO</strong><br>将中英真实表格经翻译与验证扩展到 97 种语言，合成四类 QA。先用含或不含思考轨迹的指令做 SFT，再从最佳 SFT checkpoint 做 GRPO；奖励按任务使用数值/单元格 Jaccard、事实验证 F1 或开放答案 ROUGE-L。<br>⚑ 图为训练数据构造流程，论文未单列 RL 架构图。</td><td valign="top"><strong>RL：</strong>同一 M3TQA-INSTRUCT，经 SFT 后继续 GRPO；原文未报告另一个独立 RL 语料或准确子集数量。<br><br><strong>SFT：</strong>M3TQA-INSTRUCT：97 种语言的 39,982 条自动生成 QA（ACL 正式版）；分别测试 thinking 与 non-thinking 训练。</td></tr>
</tbody>
</table>

---

### [OpenTable-R1: A Reinforcement Learning Augmented Tool Agent for Open-Domain Table Question Answering](https://arxiv.org/abs/2507.03018)

**2025-07-02** · arXiv · `TQA` · [GitHub](https://github.com/TabibitoQZP/OpenTableR1) · [证据卡](docs/PAPERS.md#opentable-r1)

<p align="center"><a href="img/opentable-r1.png"><img src="img/opentable-r1.png" width="1000" alt="OpenTable-R1: A Reinforcement Learning Augmented Tool Agent for Open-Domain Table Question Answering method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>Cold-start SFT + Async GRPO</strong><br>训练 Qwen3-4B 在多轮对话中调用 BM25+ 表检索和 SQLite SQL 执行工具。先以简单问题的正确轨迹冷启动，再在困难问题上用 Async GRPO 优化策略；LoRA 与 rollout buffer 重叠采样和参数更新以缓解长轨迹带来的等待。</td><td valign="top"><strong>RL：</strong>Open-WikiTable train 的其余 21,860 条困难样本；Async GRPO + LoRA rank 12，1,504 update steps。<br><br><strong>SFT：</strong>Open-WikiTable train 的 31,959 条简单样本；由 Qwen3-32B 生成答案并按答案 EM 筛选；full-parameter SFT 2 epochs。</td></tr>
</tbody>
</table>

---

### [Table-r1: Self-supervised and Reinforcement Learning for Program-based Table Reasoning in Small Language Models](https://arxiv.org/abs/2506.06137)

**2025-06-06** · arXiv · `TQA / TFV` · [GitHub](https://github.com/AriKing11/Table_r1_public) · [证据卡](docs/PAPERS.md#table-r1-program)

<p align="center"><a href="img/table-r1-program.png"><img src="img/table-r1-program.png" width="1000" alt="Table-r1: Self-supervised and Reinforcement Learning for Program-based Table Reasoning in Small Language Models method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>Mix-paradigm GRPO</strong><br>先用自生成的布局变换推断任务学习表格结构，再蒸馏代码推理冷启动。混合范式 GRPO 优先学习可执行 Python，并允许在合适问题上回退为文本推理；格式、编译和答案奖励配合退化短代码惩罚。</td><td valign="top"><strong>RL：</strong>WikiTQ、TabFact、HiTab 的官方训练划分；AIT-QA 按问题随机 8:2 划分后的训练部分。<br><br><strong>SFT：</strong>布局变换合成三元组；WikiTQ、TabFact、HiTab、AIT-QA 训练划分由 DeepSeek-v3 蒸馏，每数据集最多 5,000 条冷启动轨迹。</td></tr>
</tbody>
</table>

---

### [Reasoning-Table: Exploring Reinforcement Learning for Table Reasoning](https://arxiv.org/abs/2506.01710)

**2025-06-02** · arXiv · `TQA / TFV / T2T / Text-to-SQL` · [GitHub](https://github.com/MJinXiang/Reasoning-Table) · [证据卡](docs/PAPERS.md#reasoning-table)

<p align="center"><a href="img/reasoning-table.png"><img src="img/reasoning-table.png" width="1000" alt="Reasoning-Table: Exploring Reinforcement Learning for Table Reasoning method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>GRPO</strong><br>比较 RL-zero 与 Reason-SFT+RL，用最终答案、SQL 执行或文本 BLEU 阈值构造结果奖励，并加入格式奖励。系统研究教师轨迹过滤、训练样本难度、单任务与合并训练；位置证据一致性奖励作为消融实验。</td><td valign="top"><strong>RL：</strong>单数据集 RL：上述 11 个表格语料训练划分，以及 Spider/BIRD；T2T 明确在 ToTTo 上做 RL-zero 与 Reason-SFT+RL。另报告合并 TQA 训练及难度控制；原文未给所有 RL 配置共用的单一样本总数。<br><br><strong>SFT：</strong>WikiTQ、HybridQA、MultiHiertt、OTT-QA、FinQA、FeTaQA、TAT-QA、HiTab、ToTTo、TabFact、FEVEROUS 的教师推理轨迹；Table 8 保留 97,564 条，统一 SFT 为 43,201 条；ToTTo 单任务 Reason-SFT 为 1,896 条。Spider/BIRD 另有 SQL 实验。</td></tr>
</tbody>
</table>

---

### [Table-R1: Inference-Time Scaling for Table Reasoning Tasks](https://aclanthology.org/2025.emnlp-main.1040/)

**2025-05-29** · EMNLP 2025 · `TQA / TFV / T2T` · [GitHub](https://github.com/Table-R1/Table-R1) · [证据卡](docs/PAPERS.md#table-r1-scaling)

<p align="center"><a href="img/table-r1-scaling.png"><img src="img/table-r1-scaling.png" width="1000" alt="Table-R1: Inference-Time Scaling for Table Reasoning Tasks method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>GRPO with DAPO token-level loss and asymmetric clipping; no KL penalty</strong><br>Table-R1-Zero 直接从指令模型做 RL：采用 DAPO 的 token 级损失与非对称裁剪，不加 KL 惩罚。短答案与事实验证用正确性奖励，长答案用 BLEU/ROUGE-L，另加结构化输出奖励；多次采样扩展推理时计算。</td><td valign="top"><strong>RL：</strong>四个训练划分过滤后共 48,563 条：WTQ 13,706；HiTab 6,793；TabFact 20,740；FeTaQA 7,324。<br><br><strong>SFT：</strong>独立 Table-R1-SFT 对照：WTQ、HiTab、TabFact、FeTaQA 经 DeepSeek-R1 生成并验证的 33,601 条长思维链；不是 Table-R1-Zero 的冷启动阶段。</td></tr>
</tbody>
</table>

---

### [Formula-R1: Incentivizing LLM Reasoning over Complex Tables with Numerical Computation via Formula-Driven Reinforcement Learning](https://arxiv.org/abs/2505.23667)

**2025-05-29** · arXiv · `TQA / TFV` · [GitHub](https://github.com/microsoft/Fortune) · [证据卡](docs/PAPERS.md#formula-r1)

<p align="center"><a href="img/formula-r1.png"><img src="img/formula-r1.png" width="1000" alt="Formula-R1: Incentivizing LLM Reasoning over Complex Tables with Numerical Computation via Formula-Driven Reinforcement Learning method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>PPO</strong><br>Formula Tuning 让模型先思考再生成可执行表格公式，借助公式引擎提供可验证奖励：答对 1、可执行但错误 0.2、不可执行 0，另加格式奖励。比较直接 PPO 与蒸馏冷启动；Plus 在推理时融合文本和公式答案投票。</td><td valign="top"><strong>RL：</strong>合并 WikiTQ 13,753、TabFact 10,000（随机下采样）、FinQA 6,251、HiTab 7,399、MultiHiertt 7,795 条训练数据。<br><br><strong>SFT：</strong>五个源训练集上由 GPT-4o 生成思维链/公式，经答案或公式执行正确性拒绝筛选的冷启动数据；SFT+RL 配置使用，RL-zero 不使用。</td></tr>
</tbody>
</table>

---

### [Mixture-of-Retrieval Experts for Reasoning-Guided Multimodal Knowledge Exploitation](https://arxiv.org/abs/2505.22095)

**2025-05-28** · SIGIR 2026 (arXiv v2 2026-04-06) · `TQA / TFV` · [GitHub](https://github.com/OpenBMB/MoRE) · [证据卡](docs/PAPERS.md#more)

<p align="center"><a href="img/more.png"><img src="img/more.png" width="1000" alt="Mixture-of-Retrieval Experts for Reasoning-Guided Multimodal Knowledge Exploitation method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>Step-GRPO</strong><br>通用检索代理 MoRE 在文本、图像、结构化表格专家之间逐步路由。先生成并筛选教师轨迹，再按步骤采样，用查询与教师查询的 BGE-M3 相似度、专家选择正确性、观察/答案质量和格式奖励做 Step-GRPO；明确包含表格 QA 的 RL 训练。<br>⚑ 通用多模态 RAG 代理；表格任务输入为文本。</td><td valign="top"><strong>RL：</strong>Open-WikiTable 500 条（表格 QA）；另含 2WikiMultihopQA 500 条、InfoSeek 1,000 条，总计 2,000 条源问题。步骤级展开后的训练记录数未明确报告。<br><br><strong>SFT：</strong>主方法未报告独立 SFT 热启动；代码直接从 Qwen2.5-VL-Instruct 开始 Step-GRPO。教师轨迹来自相同训练集（Qwen2.5-VL-7B 生成 VQA，R1-Distill-Qwen-32B 生成 Text/Table QA）；SFT 是对照方法。</td></tr>
</tbody>
</table>

---

### [Table-R1: Region-based Reinforcement Learning for Table Understanding](https://arxiv.org/abs/2505.12415)

**2025-05-18** · arXiv · `TQA / TFV / Data Analysis` · [GitHub](https://github.com/wuzhenhe/Table-R1) · [证据卡](docs/PAPERS.md#table-r1-region)

<p align="center"><a href="img/table-r1-region.png"><img src="img/table-r1-region.png" width="1000" alt="Table-R1: Region-based Reinforcement Learning for Table Understanding method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>TARPO (Table-Aware Group Relative Policy Optimization)</strong><br>RE-SFT 先学习在推理步骤中定位最小相关行列区域；再用 TARPO 将行列 IoU 与最终答案正确性组合为奖励，逐步衰减区域奖励，并惩罚区域与答案优势方向不一致的更新。支持直接、文本思维链、符号和程序推理。</td><td valign="top"><strong>RL：</strong>同一 TableInstruct-RE，随机按 9:1 划分 TARPO 训练/验证；不把 TableBench、WikiTQ 或 WikiSQL 测试集列作训练数据。<br><br><strong>SFT：</strong>TableInstruct-RE：在 TableInstruct 的 19,661 条指令上由 DeepSeek-R1 生成最小相关区域并人工核对；RE-SFT 使用全量。</td></tr>
</tbody>
</table>

---

### [Sparks of Tabular Reasoning via Text2SQL Reinforcement Learning](https://aclanthology.org/2025.trl-1.20/)

**2025-04-23** · TRL Workshop 2025 (ACL) · `TQA / TFV / Text-to-SQL` · [GitHub](https://github.com/josefastoisser/sparks_of_tabular_reasoning) · [证据卡](docs/PAPERS.md#sparks-text2sql)

<p align="center"><a href="img/sparks-text2sql.png"><img src="img/sparks-text2sql.png" width="1000" alt="Sparks of Tabular Reasoning via Text2SQL Reinforcement Learning method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>GRPO</strong><br>先用 o3-mini 生成 SQL 与逐步推理，由第二模型检查答案和轨迹，再做 SFT；随后在 BIRD 上做 GRPO，用 SQL 质量、匹配与 LLM 评分奖励。检验仅 SQL 训练是否迁移到 CRT-QA 和表格事实验证。<br>⚑ SQL 训练后明确评测表格 QA 迁移能力。</td><td valign="top"><strong>RL：</strong>BIRD；正式论文 Figure 2、Table 1 和实现说明明确用于 GRPO，但未明确给出 RL 子集的准确条数与划分。<br><br><strong>SFT：</strong>Clinton/Text-to-SQL 集合生成并验证的 3,174 条 SQL/CoT 轨迹（正式版本数字）。</td></tr>
</tbody>
</table>

---

### [DianJin-R1: Evaluating and Enhancing Financial Reasoning in Large Language Models](https://arxiv.org/abs/2504.15716)

**2025-04-22** · arXiv · `TQA` · [GitHub](https://github.com/aliyun/qwen-dianjin) · [证据卡](docs/PAPERS.md#dianjin-r1)

<p align="center"><a href="img/dianjin-r1.png"><img src="img/dianjin-r1.png" width="1000" alt="DianJin-R1: Evaluating and Enhancing Financial Reasoning in Large Language Models method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>SFT + GRPO</strong><br>先以金融 CoT 数据做 SFT，再对困难金融选择题做 GRPO，以答案选项匹配和 think/answer 格式提供奖励；在 FinQA 上检验后训练模型的表格数值推理能力。<br>⚑ 表格 QA 属于 SFT 与评测；实际 RL 训练的是金融选择题，不能把 FinQA 标成 RL 数据。</td><td valign="top"><strong>RL：</strong>CFLUE-MCQ 的 4,096 道困难选择题；当前版本未将 FinQA 用于 RL。<br><br><strong>SFT：</strong>CFLUE-MCQ 26,672、CFLUE-OE 5,045、FinQA 4,851、Chinese Compliance Check 1,800。</td></tr>
</tbody>
</table>

---

### [Fin-R1: A Large Language Model for Financial Reasoning through Reinforcement Learning](https://arxiv.org/abs/2503.16252)

**2025-03-20** · arXiv · `TQA` · [GitHub](https://github.com/SUFE-AIFLM-Lab/Fin-R1) · [证据卡](docs/PAPERS.md#fin-r1)

<p align="center"><a href="img/fin-r1.png"><img src="img/fin-r1.png" width="1000" alt="Fin-R1: A Large Language Model for Financial Reasoning through Reinforcement Learning method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>SFT + GRPO</strong><br>以 DeepSeek-R1 蒸馏的金融推理轨迹做 SFT，再用答案准确性与输出格式奖励进行 GRPO。RL 使用题目和客观答案，不依赖完整教师推理轨迹，并保留部分 SFT 阶段过滤掉的困难题。<br>⚑ 通用金融推理模型；训练池包含表格 QA，也包含非表格金融任务。</td><td valign="top"><strong>RL：</strong>从上述原始来源整理客观题 (question, solution)，包含部分蒸馏未通过筛选的困难样本；未单列 RL 总量及各来源数量。60,091 是 SFT 数据规模。<br><br><strong>SFT：</strong>Fin-R1-Data：60,091 条中英金融推理样本；包含 FinQA 2,948、ConvFinQA 7,629，以及 FinanceQT、Finance500K、FinanceIQ、FinPEE、AntFinance、FinCorpus、TFNS、FinCUGE。</td></tr>
</tbody>
</table>

---

### [Question Answering with Texts and Tables through Deep Reinforcement Learning](https://arxiv.org/abs/2407.04858)

**2024-07-05** · BRACIS 2024 · `TQA` · [GitHub](https://github.com/MMenonJ/DRL_QA_TT) · [证据卡](docs/PAPERS.md#drl-qa-text-tables)

<p align="center"><a href="img/drl-qa-text-tables.png"><img src="img/drl-qa-text-tables.png" width="1000" alt="Question Answering with Texts and Tables through Deep Reinforcement Learning method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>DQN / PPO (module-selection policy)</strong><br>用 DRL 控制器在检索文本、检索表格、调用阅读器作答三种动作间决策，底层检索器和阅读器保持预训练权重。DQN/PPO 根据最终答案 EM/F1 获得延迟奖励，并对每次检索施加小额成本，学习开放域多跳证据获取顺序。<br>⚑ RL 训练模块调度控制器，底层阅读器保持固定。</td><td valign="top"><strong>RL：</strong>OTT-QA train：41,469 个问题；Tri-encoder 方案 1M timesteps，BM25 方案 100K timesteps。<br><br><strong>SFT：</strong>控制器未使用动作序列 SFT；使用已有 BM25/Tri-encoder 检索器、FiE 阅读器和编码器，不重新训练这些底层模型。</td></tr>
</tbody>
</table>

---

<a id="multimodal-table-understanding"></a>
## 🔥 多模态表格理解

### [Think with Structured Grounding: Perceptual Reinforcement Learning for Chart and Visual-Tabular Understanding](https://arxiv.org/abs/2608.22429)

**2026-08-23** · arXiv · `TQA / TFV` · 代码：未核实 · [证据卡](docs/PAPERS.md#twsg)

<p align="center"><a href="img/twsg.png"><img src="img/twsg.png" width="1000" alt="Think with Structured Grounding: Perceptual Reinforcement Learning for Chart and Visual-Tabular Understanding method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>Cold-start SFT + TL-GRPO</strong><br>先蒸馏区域定位、局部观察与交错推理轨迹，再用 TL-GRPO 按 think/observation/answer 标签分别归一化重要性权重；奖励结合答案 ANLS、格式与视觉观察核验，CGS 去除组内优势离群样本。</td><td valign="top"><strong>RL：</strong>64,334 条：原 SFT 数据及 ChartQA、ChartQA-X、Visual-TableQA 训练集，用 SFT checkpoint 四次采样后去除全对样本。<br><br><strong>SFT：</strong>TwSG-12K：12,674 条；Appendix E 将来源写作 TableQA、TableQA-X、Visual-TableQA，含合成多图表/多表格布局。</td></tr>
</tbody>
</table>

---

### [TableMix: Enhancing Multimodal Table Reasoning in MLLMs from a Data-Centric Perspective](https://openaccess.thecvf.com/content/CVPR2026/html/Liu_TableMix_Enhancing_Multimodal_Table_Reasoning_in_MLLMs_from_a_Data-Centric_CVPR_2026_paper.html)

**2026-06** · CVPR 2026 · `TQA / TFV` · 代码：未核实 · [证据卡](docs/PAPERS.md#tablemix)

<p align="center"><a href="img/tablemix.png"><img src="img/tablemix.png" width="1000" alt="TableMix: Enhancing Multimodal Table Reasoning in MLLMs from a Data-Centric Perspective method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>GRPO + Difficulty-Aware Reward Shaping (DRS)</strong><br>按 batch 混合视觉表格推理、纯文本数学与简单表格感知数据，用 GRPO 同时恢复逻辑推理并保持视觉定位；DRS 根据组内成功率和退火长度惩罚，让简单问题的正确回答更简洁。</td><td valign="top"><strong>RL：</strong>表格来源：TabMWP、WTQ、HiTab、TAT-QA、FeTaQA、ToTTo、TabFact、FEVEROUS、HybridQA、FinQA、MultiModalQA、InfoTabs；数学默认 MetaMath；另规则生成单元格定位 QA。混合比例 0.7:0.2:0.1。<br><br><strong>SFT：</strong>主训练流程未报告单独 SFT 阶段；基座为 Qwen2.5-VL-7B。</td></tr>
</tbody>
</table>

---

### [V-tableR1: Process-Supervised Multimodal Table Reasoning with Critic-Guided Policy Optimization](https://arxiv.org/abs/2604.20755)

**2026-04-22** · arXiv · `TQA / TFV` · 代码：未核实 · [证据卡](docs/PAPERS.md#v_tabler1)

<p align="center"><a href="img/v_tabler1.png"><img src="img/v_tabler1.png" width="1000" alt="V-tableR1: Process-Supervised Multimodal Table Reasoning with Critic-Guided Policy Optimization method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>SFT + Process-Guided Direct Alignment Policy Optimization (PGPO)</strong><br>策略 VLM 生成含单元格坐标的视觉 CoT，独立 critic VLM 核验中间步骤；过程分数门控答案和格式奖励，配合解耦 clipping 与长度感知采样，惩罚幻觉和猜中答案的错误推理。</td><td valign="top"><strong>RL：</strong>TabFact 3,648；FinQA 583；HiTab 1,546；TabMWP 3,791；WTQ 5,887，共 15,455 条。<br><br><strong>SFT：</strong>TabFact 5,250；FinQA 2,569；HiTab 3,195；TabMWP 4,412；WTQ 5,738，共 21,164 条视觉 CoT。critic 用真实/核验轨迹与 Qwen3-8B 扰动的负例。</td></tr>
</tbody>
</table>

---

### [Thinking with Tables: Enhancing Multi-Modal Tabular Understanding via Neuro-Symbolic Reasoning](https://arxiv.org/abs/2603.24004)

**2026-03-25** · arXiv · `TQA` · [GitHub](https://github.com/kunyang-YU/Thinking-with-Tables) · [证据卡](docs/PAPERS.md#thinking-with-tables)

<p align="center"><a href="img/thinking-with-tables.png"><img src="img/thinking-with-tables.png" width="1000" alt="Thinking with Tables: Enhancing Multi-Modal Tabular Understanding via Neuro-Symbolic Reasoning method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>TO-SFT + AL-GRPO</strong><br>VLM 读取视觉表头并通过 Python 沙箱操作完整 CSV，以神经符号交互回答问题。TO-SFT 学习工具轨迹；AL-GRPO 根据最终任务结果给奖励，只让成功执行的代码片段参与 RL 损失，减少不可执行动作的干扰。<br>⚑ QA 的视觉输入是表头，完整表格通过 CSV 工具访问；另有多模态表格预测任务。</td><td valign="top"><strong>RL：</strong>上述池选取 0.5K QA + 0.4K 表格预测用于 AL-GRPO；分类/回归是表格预测任务，不标为 TFV。<br><br><strong>SFT：</strong>TO-SFT：1.5K QA（WikiTQ、TabMWP、FinQA、TAT-QA）+ 1.2K 表格预测（Adoption、SkinCA、Pawpularity、Paintings）；由 Qwen3-VL-Plus / Qwen3-Max 合成。</td></tr>
</tbody>
</table>

---

### [Multimodal Table Understanding with Difficulty-aware Reinforcement Learning](https://ojs.aaai.org/index.php/AAAI/article/view/37042)

**2026-03-14** · AAAI 2026 · `TQA / TFV / TR` · 代码：未核实 · [证据卡](docs/PAPERS.md#mm_table_r1)

<p align="center"><a href="img/mm_table_r1.png"><img src="img/mm_table_r1.png" width="1000" alt="Multimodal Table Understanding with Difficulty-aware Reinforcement Learning method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>Two-stage difficulty-aware GRPO</strong><br>MM-Table-R1 先以 GRPO 学习 HTML 表格重建，以单元格内容和 rowspan/colspan 的面积加权正确率奖励感知；再用答案和格式奖励训练推理。课程难度结合合并单元格比例、单元格数与模型失败率。</td><td valign="top"><strong>RL：</strong>TabMWP、WTQ、HiTab、TAT-QA、FeTaQA、TabFact、InfoTabs、ToTTo，统一图像+HTML+QA；FeTaQA 经 DeepSeek-V3 拆分 QA。论文未公布各阶段来源样本数量。<br><br><strong>SFT：</strong>主方法不含独立 SFT；表格重建 Stage 1 也采用 RL。SFT 仅作为消融方案。</td></tr>
</tbody>
</table>

---

### [CoReTab: Improving Multimodal Table Understanding with Code-driven Reasoning](https://aclanthology.org/2026.eacl-long.306/)

**2026-01-27** · EACL 2026 Long · `TQA / TFV / TSU` · 代码：未核实 · [证据卡](docs/PAPERS.md#coretab)

<p align="center"><a href="img/coretab.png"><img src="img/coretab.png" width="1000" alt="CoReTab: Improving Multimodal Table Understanding with Code-driven Reasoning method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>SFT + GRPO with separate LoRA adapters</strong><br>将自然语言推理与可执行 Python 结合，先做表格识别和代码轨迹 SFT，再用答案正确性与格式奖励做 GRPO；三阶段分别更新 LoRA。推理时优先返回代码执行结果。</td><td valign="top"><strong>RL：</strong>CoReTab 语料；原文未单列 RL 子集数量。GRPO 每题采样 4 条，奖励为二元答案正确性＋二元格式。<br><br><strong>SFT：</strong>MMTab-pre 表格识别 150K；CoReTab 115K：WTQ 9.5K、HiTab 7.5K、TabMWP 30K、TAT-QA 6K、TabFact 22K、InfoTabs 15K，加五种结构任务各 5K。轨迹通过代码执行核验。</td></tr>
</tbody>
</table>

---

### [Towards Efficient Multimodal Unified Reasoning Model via Model Merging](https://openaccess.thecvf.com/content/CVPR2026F/html/Yin_Towards_Efficient_Multimodal_Unified_Reasoning_Model_via_Model_Merging_CVPRF_2026_paper.html)

**2025-10-10** · CVPR Findings 2026 · `TQA / TFV` · [GitHub（占位，训练代码未发布）](https://github.com/buptyqx/Tiny-R1V) · [证据卡](docs/PAPERS.md#tiny-r1v)

<p align="center"><a href="img/tiny-r1v.png"><img src="img/tiny-r1v.png" width="1000" alt="Towards Efficient Multimodal Unified Reasoning Model via Model Merging method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>Length-Informed Relative Policy Optimization（LIPO）+ AMM</strong><br>分别以 LIPO 训练数学、结构数据和 OCR 专家，按回答长度调整奖励与相对优势，偏向简洁而正确的推理；再用 AMM 合并专家任务向量。强化学习发生在专家训练阶段，模型合并阶段不做 RL。<br>⚑ 表格 QA/TFV 明确参与 RL 训练；主结果未单列这两个表格任务的测试。</td><td valign="top"><strong>RL：</strong>结构数据专家 15K：TAT-DQA、WTQ、TabFact、PlotQA、TQA、ChartGalaxy；另有数学专家 15K 和 OCR 专家 10K。15K 是混合结构数据量，并非全部为表格 QA。<br><br><strong>SFT：</strong>未新增冷启动 SFT；从 Qwen2.5-VL-3B-Instruct 直接训练三个专家。</td></tr>
</tbody>
</table>

---

### [DeFacto: Counterfactual Thinking with Images for Enforcing Evidence-Grounded and Faithful Reasoning](https://arxiv.org/abs/2509.20912)

**2025-09-25** · arXiv · `TQA` · [GitHub](https://github.com/tinnel123666888/defacto) · [证据卡](docs/PAPERS.md#defacto)

<p align="center"><a href="img/defacto.png"><img src="img/defacto.png" width="1000" alt="DeFacto: Counterfactual Thinking with Images for Enforcing Evidence-Grounded and Faithful Reasoning method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>反事实对齐 + Counterfactual GRPO</strong><br>为图像问题构造原图、关键证据遮挡图和随机非关键遮挡图；GRPO 联合答案、格式与证据框奖励，让关键证据缺失时输出 Unknown，并约束回答依赖真实图像证据。在视觉 WTQ 上评测表格问答迁移。<br>⚑ 通用视觉 RL 方法，表格任务的明确证据是视觉 WTQ 评测；不据此推断 WTQ 参与训练。</td><td valign="top"><strong>RL：</strong>DeFacto-100K（约 10 万图像；VQAv2、ChartQA、DocVQA 等来源），构造正样本/关键遮挡/随机遮挡三类训练输入；未单列 WTQ 训练占比。<br><br><strong>SFT：</strong>Table 4 消融包含原始数据 SFT 和反事实对齐；所列版本未单列 SFT 数据量或阶段配比。</td></tr>
</tbody>
</table>

---

### [Can GRPO Boost Complex Multimodal Table Understanding?](https://aclanthology.org/2025.emnlp-main.637/)

**2025-09-21** · EMNLP 2025 · `TQA / TFV / TR` · 代码：未核实 · [证据卡](docs/PAPERS.md#visual_table_r1)

<p align="center"><a href="img/visual_table_r1.png"><img src="img/visual_table_r1.png" width="1000" alt="Can GRPO Boost Complex Multimodal Table Understanding? method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>SFT warm-up + PA-GRPO + HC-GRPO</strong><br>Table-R1 三阶段训练：SFT 热身提升感知与推理起点，PA-GRPO 用 TEDS 连续奖励优化图像到 HTML/Markdown，HC-GRPO 在给定部分推理提示后补全剩余步骤，以最终答案正确性与格式奖励缓解稀疏反馈。</td><td valign="top"><strong>RL：</strong>相同四个 held-in 来源；PA-GRPO 用图像重建数据 Dp，HC-GRPO 用 hint-completion 推理数据 Dr。<br><br><strong>SFT：</strong>MMTab 中 WTQ、HiTab、TabMWP、TabFact 各抽 8K QA；感知目标为结构化表格，推理目标由 GPT-4o 扩写并拆成 hint-completion。</td></tr>
</tbody>
</table>

---

### [DocR1: Evidence Page-Guided GRPO for Multi-Page Document Understanding](https://ojs.aaai.org/index.php/AAAI/article/view/38097)

**2025-08-10** · AAAI 2026 · `TQA / TFV` · 代码：未核实 · [证据卡](docs/PAPERS.md#docr1)

<p align="center"><a href="img/docr1.png"><img src="img/docr1.png" width="1000" alt="DocR1: Evidence Page-Guided GRPO for Multi-Page Document Understanding method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>Evidence Page-Guided GRPO（EviGRPO）</strong><br>用单页→多页课程训练 Qwen2.5-VL，先定位证据页再回答。GRPO 联合答案 ANLS、证据页 F1 与输出格式奖励，降低多页定位错误；两阶段均为 RL，教师标注过程不等于 SFT。<br>⚑ 多页文档 RL，训练池明确包含视觉表格 QA 和 TabFact 事实验证。</td><td valign="top"><strong>RL：</strong>EviBench 4,800：单页 1,300（13 来源各 100，含 WTQ 与 TabFact）；多页 3,500（DUDE 1,000，MP-DocVQA/TATDoc/SlideVQA/MultiHiertt/ArxivFullQA 各 500）。<br><br><strong>SFT：</strong>未新增 SFT；直接从 Qwen2.5-VL-7B-Instruct 进入两阶段 EviGRPO。</td></tr>
</tbody>
</table>

---

### [MTabVQA: Evaluating Multi-Tabular Reasoning of Language Models in Visual Space](https://aclanthology.org/2025.findings-emnlp.1083/)

**2025-06-13** · Findings of EMNLP 2025 · `TQA` · [GitHub](https://github.com/anshulsc/MTabVQA-EMNLP) · [证据卡](docs/PAPERS.md#mtabvqa)

<p align="center"><a href="img/mtabvqa.png"><img src="img/mtabvqa.png" width="1000" alt="MTabVQA: Evaluating Multi-Tabular Reasoning of Language Models in Visual Space method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>GRPO experimental branch (EasyR1)</strong><br>在多张表格图像之间执行多跳 QA；论文附加 GRPO 实验训练 Qwen2.5-VL-3B，复合奖励包含 EM/F1 答案正确性、think/answer 标签结构和 JSON 有效性，并与独立 SFT 分支比较。<br>⚑ 收录 GRPO 实验分支；主 TableVision 方法为 SFT。</td><td valign="top"><strong>RL：</strong>MTabVQA-Instruct 的 Spider 来源 2,395 QA 子集；Qwen2.5-VL-3B 用 EasyR1 训练 270 steps。<br><br><strong>SFT：</strong>独立 SFT 比较分支：同一 2,395 条 Spider 来源子集；主 TableVision 模型另用完整 MTabVQA-Instruct 进行 SFT。</td></tr>
</tbody>
</table>

---

### [Multimodal Tabular Reasoning with Privileged Structured Information](https://arxiv.org/abs/2506.04088)

**2025-06-04** · NeurIPS 2025 · `TQA / TFV` · 代码：未核实 · [证据卡](docs/PAPERS.md#turbo)

<p align="center"><a href="img/turbo.png"><img src="img/turbo.png" width="1000" alt="Multimodal Tabular Reasoning with Privileged Structured Information method diagram"></a></p>

<table>
<thead>
<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>
</thead>
<tbody>
<tr><td valign="top"><strong>Structure-aware trace SFT + GRPO</strong><br>TURBO 在训练期把 Markdown 表格作为特权信息，让 DeepSeek-R1 生成并筛选结构感知推理轨迹；先蒸馏到图像模型，再以答案正确性和输出格式奖励做 GRPO。推理期仅输入表格图像。</td><td valign="top"><strong>RL：</strong>同一约 9K 数据；各问题采 16 个回答，执行 GRPO。HiTab 因 Markdown 层级格式困难而未用于训练。<br><br><strong>SFT：</strong>TabMWP、WTQ、TAT-QA、TabFact、InfoTabs 各采 2K，10K 经拒绝采样保留约 9K 高质量轨迹。</td></tr>
</tbody>
</table>

---

<a id="task-index"></a>
## 🧭 任务索引

| 任务 | 篇数 | 条目 |
| --- | --- | --- |
| TQA | 42 | [twsg](docs/PAPERS.md#twsg) · [dre-critic](docs/PAPERS.md#dre-critic) · [acpo](docs/PAPERS.md#acpo) · [tablemix](docs/PAPERS.md#tablemix) · [rsat](docs/PAPERS.md#rsat) · [v_tabler1](docs/PAPERS.md#v_tabler1) · [thinking-with-tables](docs/PAPERS.md#thinking-with-tables) · [tablelong](docs/PAPERS.md#tablelong) · [tarex](docs/PAPERS.md#tarex) · [mm_table_r1](docs/PAPERS.md#mm_table_r1) · [operation-r1](docs/PAPERS.md#operation-r1) · [re-tab](docs/PAPERS.md#re-tab) · [coretab](docs/PAPERS.md#coretab) · [reasontabqa](docs/PAPERS.md#reasontabqa) · [tablegpt-r1](docs/PAPERS.md#tablegpt-r1) · [jt-da](docs/PAPERS.md#jt-da) · [star](docs/PAPERS.md#star) · [mixture-of-minds](docs/PAPERS.md#mixture-of-minds) · [imbalanced-gradients](docs/PAPERS.md#imbalanced-gradients) · [tiny-r1v](docs/PAPERS.md#tiny-r1v) · [tattoo](docs/PAPERS.md#tattoo) · [vietnamese-two-stage](docs/PAPERS.md#vietnamese-two-stage) · [mofin](docs/PAPERS.md#mofin) · [vietnamese-program-grpo](docs/PAPERS.md#vietnamese-program-grpo) · [defacto](docs/PAPERS.md#defacto) · [visual_table_r1](docs/PAPERS.md#visual_table_r1) · [tablemind](docs/PAPERS.md#tablemind) · [m3tqa](docs/PAPERS.md#m3tqa) · [docr1](docs/PAPERS.md#docr1) · [opentable-r1](docs/PAPERS.md#opentable-r1) · [mtabvqa](docs/PAPERS.md#mtabvqa) · [table-r1-program](docs/PAPERS.md#table-r1-program) · [turbo](docs/PAPERS.md#turbo) · [reasoning-table](docs/PAPERS.md#reasoning-table) · [table-r1-scaling](docs/PAPERS.md#table-r1-scaling) · [formula-r1](docs/PAPERS.md#formula-r1) · [more](docs/PAPERS.md#more) · [table-r1-region](docs/PAPERS.md#table-r1-region) · [sparks-text2sql](docs/PAPERS.md#sparks-text2sql) · [dianjin-r1](docs/PAPERS.md#dianjin-r1) · [fin-r1](docs/PAPERS.md#fin-r1) · [drl-qa-text-tables](docs/PAPERS.md#drl-qa-text-tables) |
| TFV | 26 | [twsg](docs/PAPERS.md#twsg) · [dre-critic](docs/PAPERS.md#dre-critic) · [tablemix](docs/PAPERS.md#tablemix) · [rsat](docs/PAPERS.md#rsat) · [v_tabler1](docs/PAPERS.md#v_tabler1) · [tarex](docs/PAPERS.md#tarex) · [mm_table_r1](docs/PAPERS.md#mm_table_r1) · [operation-r1](docs/PAPERS.md#operation-r1) · [coretab](docs/PAPERS.md#coretab) · [tablegpt-r1](docs/PAPERS.md#tablegpt-r1) · [star](docs/PAPERS.md#star) · [mixture-of-minds](docs/PAPERS.md#mixture-of-minds) · [tiny-r1v](docs/PAPERS.md#tiny-r1v) · [tattoo](docs/PAPERS.md#tattoo) · [visual_table_r1](docs/PAPERS.md#visual_table_r1) · [tablemind](docs/PAPERS.md#tablemind) · [m3tqa](docs/PAPERS.md#m3tqa) · [docr1](docs/PAPERS.md#docr1) · [table-r1-program](docs/PAPERS.md#table-r1-program) · [turbo](docs/PAPERS.md#turbo) · [reasoning-table](docs/PAPERS.md#reasoning-table) · [table-r1-scaling](docs/PAPERS.md#table-r1-scaling) · [formula-r1](docs/PAPERS.md#formula-r1) · [more](docs/PAPERS.md#more) · [table-r1-region](docs/PAPERS.md#table-r1-region) · [sparks-text2sql](docs/PAPERS.md#sparks-text2sql) |
| T2T | 2 | [reasoning-table](docs/PAPERS.md#reasoning-table) · [table-r1-scaling](docs/PAPERS.md#table-r1-scaling) |

## 🤝 Contributing

欢迎补充有原文证据的新论文，参见 [CONTRIBUTING.md](CONTRIBUTING.md)。更新 `data/papers.json` 后运行 `python scripts/build_readme.py`；提图与维护说明见贡献指南。

## 📄 来源与版权

论文方法图属于原作者/出版方，保留来源与图号；本仓库不对第三方图片重新授权。原文 PDF 仅缓存于忽略目录，不打包分发。使用或转载图片请遵守对应论文许可，见 [RIGHTS.md](RIGHTS.md)。
