"""Build the GitHub paper index and evidence cards from data/papers.json."""
from pathlib import Path
import csv
import html
import json
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]

def cell(value):
    return html.escape(str(value)).replace('|', '&#124;').replace('\n', '<br>')

def note_text(value):
    return '; '.join(value) if isinstance(value, list) else str(value or '未报告')

def build():
    manifest = json.loads((ROOT / 'data/papers.json').read_text(encoding='utf-8'))
    papers = manifest['papers']
    papers = sorted(papers, key=lambda e: (e['date'], e['title']), reverse=True)
    counts = Counter(e['modality'] for e in papers)
    tasks = Counter(t for e in papers for t in e['tasks'])
    lines = [
        '# Awesome RL for Table Understanding', '',
        '> 用强化学习训练表格理解模型：文本表格与多模态表格，覆盖 TQA、TFV、T2T。', '',
        '## 🌟 Overview', '',
        '- [收录标准与任务定义](#scope)',
        '- [文本表格理解](#text-table-understanding)',
        '- [多模态表格理解](#multimodal-table-understanding)',
        '- [任务索引](#task-index)',
        '- [逐篇证据卡](docs/PAPERS.md)',
        '- [排除与边界记录](docs/SCREENING.md)',
        '- [独立核对记录](docs/AUDIT.md)',
        '- [结构化数据](data/papers.json) · [CSV 索引](data/papers.csv) · [图片来源](img/README.md)', '',
        '<a id="scope"></a>',
        '## 📌 收录标准与任务定义', '',
        '只收录论文中确实执行了 **RL 策略更新**、并用于表格理解任务的工作。可包含 GRPO、PPO、DQN、DAPO 及其变体，也包含 RL 训练的表格检索调度器或过程验证器；条目会标明训练对象。仅提示、SFT、蒸馏、奖励打分/搜索而无 RL 更新的工作不收录。DPO-only、纯图表 QA、仅 OCR/表格结构识别、仅 Text-to-SQL 且没有表格理解实验的论文不计入主索引。', '',
        '| 缩写 | 本仓库定义 |',
        '| --- | --- |',
        '| TQA | Table Question Answering，包含短答案、数值推理、自由形式回答、多表与开放域表格问答。 |',
        '| TFV | Table Fact Verification，判断声明是否受表格支持。 |',
        '| T2T | Table-to-Text，不依赖显式问题的表格描述或生成任务。FeTaQA 的自由形式回答仍标 TQA。 |', '',
        '分类依据是 **模型实际输入**：序列化表格、SQL/DataFrame、表格+文字属于文本表格；直接接收表格图像/截图的 VLM 属于多模态表格。数据集名字含 “MultiModal” 不足以决定分类。任务标签表示论文涉及的任务，可能只作域外评测；**不能据此推断该任务参与 RL 训练**。训练数据列单独区分 SFT 与 RL。', '',
        '日期原则为首次公开时间，正式会议/期刊列在标题下；无法核实预印本日期时使用正式发布日期并注明。采用较新的可核实版本，同名论文与更名版本分别去重。未核实的代码链接记为“未核实”。这是截至检索日的可核实清单，不声称穷尽所有论文。', ''
    ]
    for modality, anchor, heading in [('text','text-table-understanding','文本表格理解'), ('multimodal','multimodal-table-understanding','多模态表格理解')]:
        group = [e for e in papers if e['modality'] == modality]
        lines += [f'<a id="{anchor}"></a>', f'## 🔥 {heading}', '']
        for e in group:
            slug = e['slug']
            fig = e.get('figure_path', f'img/{slug}.png')
            code_label = 'GitHub（占位，训练代码未发布）' if e.get('code_status') == 'author repository placeholder' else 'GitHub'
            code = f'[{code_label}]({e["code_url"]})' if e.get('code_url') else '代码：未核实'
            lines += [f'### [{cell(e["title"])}]({e["paper_url"]})', '',
                      f'**{e["date"]}** · {cell(e["venue"])} · `{" / ".join(e["tasks"])}` · {code} · [证据卡](docs/PAPERS.md#{slug})', '',
                      f'<p align="center"><a href="{fig}"><img src="{fig}" width="1000" alt="{cell(e["title"])} method diagram"></a></p>', '',
                      '<table>', '<thead>',
                      '<tr><th width="50%" align="left">方法描述</th><th width="50%" align="left">训练数据集</th></tr>',
                      '</thead>', '<tbody>']
            method = f"<strong>{cell(e['algorithm'])}</strong><br>{cell(e['method_zh'])}"
            if e.get('scope_note'):
                method += f"<br>⚑ {cell(e['scope_note'])}"
            data = f"<strong>RL：</strong>{cell(note_text(e['rl_data']))}<br><br><strong>SFT：</strong>{cell(note_text(e['sft_data']))}"
            lines += [f'<tr><td valign="top">{method}</td><td valign="top">{data}</td></tr>',
                      '</tbody>', '</table>', '', '---', '']
    lines += ['<a id="task-index"></a>', '## 🧭 任务索引', '', '| 任务 | 篇数 | 条目 |', '| --- | --- | --- |']
    for task in ['TQA', 'TFV', 'T2T']:
        group = [e for e in papers if task in e['tasks']]
        links = ' · '.join(f"[{e['slug']}](docs/PAPERS.md#{e['slug']})" for e in group)
        lines.append(f'| {task} | {len(group)} | {links or "本次未核实符合标准的工作"} |')
    lines += ['',
              '## 🤝 Contributing', '', '欢迎补充有原文证据的新论文，参见 [CONTRIBUTING.md](CONTRIBUTING.md)。更新 `data/papers.json` 后运行 `python scripts/build_readme.py`；提图与维护说明见贡献指南。', '',
              '## 📄 来源与版权', '', '论文方法图属于原作者/出版方，保留来源与图号；本仓库不对第三方图片重新授权。原文 PDF 仅缓存于忽略目录，不打包分发。使用或转载图片请遵守对应论文许可，见 [RIGHTS.md](RIGHTS.md)。', '']
    (ROOT / 'README.md').write_text('\n'.join(lines), encoding='utf-8')
    cards = ['# 逐篇证据卡', '', f"核对日期：{manifest['as_of']}。图页码为所列 PDF 的一基页序号，不一定等于出版物印刷页码。", '', 'SFT 和 RL 数据表示本文新增训练阶段；不列基座模型预训练数据。任务标签可能包含仅评测任务。', '']
    attribution = ['# 方法图来源', '', '所有图片均由公开论文 PDF 渲染裁切，未用 AI 重绘。坐标单位为 PDF points，原点在页面左上角。版权归原作者/出版方。', '', '| 文件 | 论文及原图 | PDF 页 | 裁切区域 | PDF SHA256 |', '| --- | --- | --- | --- | --- |']
    for e in papers:
        slug = e['slug']
        fig = e.get('figure_path', f'img/{slug}.png')
        cards += [f'<a id="{slug}"></a>', f"## {e['title']}", '',
                  f"**首次公开：** {e['date']} · **发表/版本：** {e['venue']} · **类别：** {e['modality']} · **任务：** {' / '.join(e['tasks'])}", '',
                  f"[论文]({e['paper_url']}) · [核对 PDF]({e['pdf_url']})" + (f" · [代码]({e['code_url']})" if e.get('code_url') else ' · 代码链接：未核实'), '']
        if e.get('aliases'):
            cards += ['**旧标题/别名：** ' + '; '.join(e['aliases']), '']
        if e.get('date_basis'):
            cards += ['**日期说明：** ' + e['date_basis'], '']
        if e.get('pdf_version'):
            cards += ['**核对版本：** ' + e['pdf_version'], '']
        if e.get('code_status') == 'author repository placeholder':
            cards += ['**代码状态：** 作者 GitHub 仓库目前为占位，训练代码未发布。', '']
        cards += [f"**RL 方法：** {e['algorithm']}", '', e['method_zh'], '',
                  '| 阶段 | 数据与用途 |', '| --- | --- |',
                  f"| SFT / 冷启动 | {cell(note_text(e['sft_data']))} |", f"| RL 训练 | {cell(note_text(e['rl_data']))} |", f"| 评测 | {cell(note_text(e['eval_data']))} |", '',
                  f"![{e['title']} method diagram](../{fig})", '', f"*原文 Fig. {e['figure_number']}，PDF 第 {e['figure_page']} 页。{e['figure_caption']}*", '', '**原文证据：**', '']
        for ev in e['evidence']:
            cards.append(f"- [{ev['location']}]({ev['url']})：{ev['note']}")
        if e.get('caveats'):
            cards += ['', '**阅读备注：**', ''] + ['- ' + c for c in e['caveats']]
        cards.append('')
        attribution.append(f"| [{slug}.png]({Path(fig).name}) | [{cell(e['title'])}, Fig. {e['figure_number']}]({e['pdf_url']}) | {e['figure_page']} | {cell(e.get('figure_crop', '见元数据'))} | `{e['pdf_sha256']}` |")
    (ROOT / 'docs').mkdir(exist_ok=True)
    (ROOT / 'docs/PAPERS.md').write_text('\n'.join(cards), encoding='utf-8')
    (ROOT / 'img/README.md').write_text('\n'.join(attribution) + '\n', encoding='utf-8')
    fields = ['slug','date','title','venue','modality','tasks','algorithm','sft_data','rl_data','eval_data','paper_url','pdf_url','code_url','figure_path','figure_number','figure_page']
    with (ROOT / 'data/papers.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        for e in papers:
            writer.writerow({k: note_text(e.get(k, '')) for k in fields})
    print(json.dumps({'papers':len(papers),'modality_counts':counts,'task_counts':tasks}, ensure_ascii=False))

if __name__ == '__main__':
    build()
