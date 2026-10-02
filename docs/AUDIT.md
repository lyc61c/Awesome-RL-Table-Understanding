# 独立核对记录

核对日期：2026-10-02。本次核对针对汇总到 `data/papers.json` 的 27 个主条目，以及 `docs/SCREENING.md`。这是一轮独立抽查与完整性检查，不等同于对所有实验的复现。

## 数据与任务边界

- **Reasoning-Table** 的 ToTTo 单数据集实验确实进行了 GRPO：§3.4 明确采用 BLEU 阈值奖励，Table 2 同时报出 RL-zero 与 Reason-SFT+RL。统一 SFT 中 ToTTo/FEVEROUS 为 0，并不否定其单数据集实验。位置奖励默认权重为 0，不能把消融改写成全部主实验的机制。
- **Table-R1: Inference-Time Scaling** 的 T2T 标签来自 ToTTo/QTSumm/RotoWire 域外生成评测；RL 来源仍为 WTQ/HiTab/TabFact/FeTaQA。独立 SFT 对照不是 RL-zero 的热启动。
- **MoRE** 的 GRPO 训练明确包含 Open-WikiTable 500 条。TabFact 只属于域外测试。作者代码中 VQA 输入真正的图片像素，但表格任务输入是文本问题与结构化表格检索结果，因此按表格任务归入文本类别。R1-Router 与最新 MoRE 是同一篇文章的版本与别名。
- **RE-Tab** 的主推理框架为 training-free；收录依据是 v2 §4.3 / Appendix G.3 的实际 GRPO proof-of-concept，而不是单凭 reward 一词。TabFact 只出现在主框架评测，不属于该 GRPO 训练来源。
- **RSAT** 的训练池规模和实际 GRPO 使用量不同：38,647 条候选训练数据中，每模型实际抽取 500 条。FeTaQA 为自由形式 QA，不能据答案长度改为 T2T。
- **OpenTable-R1** 使用 Open-WikiTable，而非 WikiTableQuestions 或 OTT-QA。源训练集按容易 31,959 / 困难 21,860 分别用于 SFT 与 Async GRPO；论文没有完整披露奖励权重，不补写公式。
- **V-tableR1** 的 PGPO 虽名字含 Direct Alignment，但正文有明确 GRPO/DAPO 裁剪目标，是 RL，并非仅 DPO。InfoTabs/TAT-QA 训练列为空，只能标测试。
- **MM-Table-R1** 两阶段均为 GRPO，不能把表格重建阶段改为 SFT；ToTTo 在该论文中用于重建，不能因此加 T2T 标签。
- **MTabVQA** 收录的是附加 GRPO 实验分支；TableVision 主模型为 SFT。其 Fig.2 是数据构造方法图，不能标成独立 RL 架构图。
- **CoReTab** 正式 EACL 2026 版本存在第三阶段 GRPO；因此应纳入，不能仅因主要贡献是数据构造而排除。RL 子集数量未单列，不能自行把 115K 写成实际 RL 样本数。
- **Critic-4B / When LLMs Read Tables Carelessly** 与 TaTToo 是不同论文。训练数据来自 WTQ 响应片段，SFT 2,000 / GRPO 5,712；训练后的 critic 在 WTQ、TableBench、FinQA 上验证，SciTab/ToTTo 仅在前面的通用模型错误分析中出现。RL 更新 critic，不更新答案生成模型。论文只提供 critic 提示图，未给出专门 RL 架构图。

## 排除项核对

`SCREENING.md` 的代表性排除理由与原文一致。重点检查了容易被关键词误收的条目：

- [TableDART](https://arxiv.org/html/2509.14671v1)：§3.3 Eq.3–5 用专家经验准确率构造监督分布，以 KL 与成本目标训练门控；policy/router 不等于 RL。
- [SG-HMA](https://aclanthology.org/2023.findings-emnlp.44/)：优化为 MLE 与对比排序损失，RL 是相关工作。
- [Poised](https://doi.org/10.1016/j.knosys.2024.112571)：BART 前缀规划与 LLM 提示；搜索摘要的 RL 文字来自页面推荐文章，不能当作本文机制。
- [Automatic Prompt Generation](https://arxiv.org/abs/2405.05618)：确有 RL 列选择器，但下游是填补、错误检测、实体匹配，超出核心 TQA/TFV/T2T。

## 完整性检查与本轮补漏

27 个主条目没有重复 slug；已登记的图片路径均存在，图页码未超出对应 PDF 页数，已提供 SHA256 的 PDF 均匹配。原图的 crop 坐标用于可追溯重提取，不代表作者发布了独立图片许可。

本轮通过 `TabFact PPO`、`ToTTo GRPO` 与 TFV/T2T 组合检索发现并补录了 [When LLMs Read Tables Carelessly](https://aclanthology.org/2026.acl-long.762/)。当前未发现需要删除的主条目；各边界条目的限定说明应在 README 或论文证据卡中保留。
