"""Check a curated release for broken local assets and incomplete evidence."""
from pathlib import Path
from urllib.parse import unquote
import datetime
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]

def validate():
    data = json.loads((ROOT / 'data/papers.json').read_text(encoding='utf-8'))
    errors = []
    slugs = set()
    titles = set()
    required = ['slug','title','date','venue','paper_url','pdf_url','modality','tasks','algorithm','method_zh','sft_data','rl_data','eval_data','figure_number','figure_page','figure_crop','figure_path','pdf_sha256','evidence']
    start = datetime.date.fromisoformat(data['start_date'])
    end = datetime.date.fromisoformat(data['as_of'])
    for e in data['papers']:
        label = e.get('slug', '<missing slug>')
        for key in required:
            if not e.get(key):
                errors.append(f'{label}: missing {key}')
        if label in slugs or e.get('title') in titles:
            errors.append(f'{label}: duplicate paper')
        slugs.add(label)
        titles.add(e.get('title'))
        date = e.get('date', '')
        try:
            dt = datetime.date.fromisoformat(date + '-01' if len(date) == 7 else date)
            if not start <= dt <= end:
                errors.append(f'{label}: date outside scope')
        except ValueError:
            errors.append(f'{label}: invalid date {date}')
        if e.get('modality') not in ['text','multimodal']:
            errors.append(f'{label}: invalid modality')
        if not any(t in ['TQA','TFV','T2T'] for t in e.get('tasks', [])):
            errors.append(f'{label}: no core table-understanding task')
        for key in ['paper_url','pdf_url']:
            if not e.get(key, '').startswith('https://'):
                errors.append(f'{label}: invalid {key}')
        asset = ROOT / e.get('figure_path', 'missing')
        if not asset.is_file() or asset.stat().st_size < 2000:
            errors.append(f'{label}: missing/empty original figure')
        digest = e.get('pdf_sha256', '')
        if not re.fullmatch('[0-9a-f]{64}', digest):
            errors.append(f'{label}: invalid PDF digest')
        pdf = ROOT / e.get('pdf_file', f'tmp/pdfs/{label}.pdf')
        if pdf.is_file() and hashlib.sha256(pdf.read_bytes()).hexdigest() != digest:
            errors.append(f'{label}: PDF source changed since extraction')
        for ev in e.get('evidence', []):
            if not all(ev.get(k) for k in ['url','location','note']):
                errors.append(f'{label}: incomplete evidence location')
    for path in [ROOT / 'README.md', *sorted((ROOT / 'docs').glob('*.md')), ROOT / 'img/README.md', ROOT / 'CONTRIBUTING.md']:
        source = path.read_text(encoding='utf-8')
        refs = re.findall(r'\]\(([^)]+)\)', source) + re.findall(r'(?:src|href)="([^"]+)"', source)
        for ref in refs:
            if ref.startswith(('https://','http://','#','mailto:')):
                continue
            target, _, fragment = ref.partition('#')
            dest = (path.parent / unquote(target)).resolve()
            if not dest.exists():
                errors.append(f'{path.relative_to(ROOT)}: broken local link {ref}')
            elif fragment and dest.suffix == '.md':
                if f'id="{fragment}"' not in dest.read_text(encoding='utf-8'):
                    errors.append(f'{path.relative_to(ROOT)}: missing anchor {ref}')
        if re.search(r'turn\d+(?:search|view|academia)\d+|cite', source):
            errors.append(f'{path.relative_to(ROOT)}: internal browser citation token')
    if errors:
        print('\n'.join(errors))
        raise SystemExit(1)
    print(f"PASS: {len(slugs)} unique papers, original figures, source hashes, required training/evidence fields and local links.")

if __name__ == '__main__':
    validate()
