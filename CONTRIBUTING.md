# 贡献与更新

新增论文需同时满足时间窗口、表格理解任务、实际 RL 策略更新三项标准。证据需来自作者论文、正式出版页面或作者代码库。

1. 在 `data/papers.json` 的 `papers` 中新增条目。填写完整标题、首次公开日期、版本/会议、论文/代码链接、输入模态、任务、算法、方法概述、SFT 数据、RL 数据、评测数据与原文证据位置。
2. 固定 PDF 版本。运行 `python scripts/extract_figures.py data/papers.json --download --slug <slug>` 将 PDF 下载到忽略目录。
3. 渲染并查看包含方法图的原页；确认图号、页码后，以 PDF points 坐标裁切：`python scripts/extract_figures.py data/papers.json --slug <slug> --page <page> --crop <x0> <y0> <x1> <y1> --output img/<slug>.png`。
4. 检查图片完整、清晰且无正文混入。记录 `figure_number`、`figure_page`、`figure_crop`、`figure_path` 和源文件 `pdf_sha256`；若图只描述数据构造或主方法而非 RL 阶段，明确注明。
5. 运行 `python scripts/build_readme.py` 重建 README、证据卡、CSV 和图来源表，再运行 `python scripts/validate_repo.py` 检查本地引用和元数据。
6. 运行 `python scripts/package_repo.py` 生成可上传的 ZIP；发布包包含索引、证据卡、原图与维护脚本，排除原文 PDF 和研究缓存。

避免把只在评测中出现的数据集写进 RL 训练列；不要把 FeTaQA 自动标为 T2T，也不要把 ToTTo 表格重建自动标为 T2T。同名 Table-R1 依论文 ID 区分，更名论文只保留一个条目并记录别名。

`scope_note` 用于区分 RL 训练验证器、模块调度、主方法之外的 GRPO 实验等边界。没有核实的代码用 `null`，原文未给出的细节用“未报告”，不要猜测样本数或奖励权重。
