"""Download source PDFs and render explicit figure crops. No generated diagrams."""
from pathlib import Path
import argparse
import concurrent.futures
import hashlib
import json
import urllib.request

import fitz

ROOT = Path(__file__).resolve().parents[1]

def download(entry):
    path = ROOT / entry.get('pdf_file', f"tmp/pdfs/{entry['slug']}.pdf")
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        req = urllib.request.Request(entry['pdf_url'], headers={'User-Agent': 'Mozilla/5.0 (academic literature curation)'})
        with urllib.request.urlopen(req, timeout=90) as response:
            content = response.read()
        if not content.startswith(b'%PDF'):
            raise ValueError(f"Not a PDF: {entry['slug']}")
        path.write_bytes(content)
    expected = entry.get('pdf_sha256')
    if expected and hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        raise ValueError(f"PDF version/hash differs from manifest: {entry['slug']}")
    with fitz.open(path) as doc:
        text = '\n'.join(f'\n=== PAGE {i+1} ===\n' + p.get_text() for i, p in enumerate(doc))
        path.with_suffix('.txt').write_text(text, encoding='utf-8')
        return {'slug': entry['slug'], 'pages': len(doc), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}

def render(entry, page, crop=None, output=None):
    path = ROOT / entry.get('pdf_file', f"tmp/pdfs/{entry['slug']}.pdf")
    with fitz.open(path) as doc:
        p = doc[page - 1]
        clip = fitz.Rect(crop) if crop else p.rect
        out = ROOT / (output or f"tmp/pdfs/{entry['slug']}-page-{page}.png")
        out.parent.mkdir(parents=True, exist_ok=True)
        p.get_pixmap(matrix=fitz.Matrix(2, 2), clip=clip, alpha=False).save(out)
        print(json.dumps({'slug': entry['slug'], 'page': page, 'crop': list(clip), 'output': str(out)}, ensure_ascii=False))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('manifest')
    parser.add_argument('--download', action='store_true')
    parser.add_argument('--slug')
    parser.add_argument('--page', type=int)
    parser.add_argument('--crop', type=float, nargs=4)
    parser.add_argument('--output')
    args = parser.parse_args()
    entries = json.loads((ROOT / args.manifest).read_text(encoding='utf-8-sig'))
    if isinstance(entries, dict):
        entries = entries['papers']
    if args.slug:
        entries = [e for e in entries if e['slug'] == args.slug]
    if args.download:
        failed = False
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            futures = {pool.submit(download, e): e['slug'] for e in entries}
            for future in concurrent.futures.as_completed(futures):
                try:
                    print(json.dumps(future.result(), ensure_ascii=False))
                except Exception as exc:
                    failed = True
                    print(json.dumps({'slug': futures[future], 'error': str(exc)}, ensure_ascii=False))
        if failed:
            raise SystemExit(1)
    if args.page:
        for entry in entries:
            render(entry, args.page, args.crop, args.output)

if __name__ == '__main__':
    main()
