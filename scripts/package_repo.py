"""Package distributable repository files without PDFs or research caches."""
from pathlib import Path
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NAME = 'Awesome-RL-Table-Understanding'


def package():
    files = [ROOT / name for name in
             ['README.md', 'CONTRIBUTING.md', 'RIGHTS.md', '.gitignore', 'requirements.txt',
              'data/papers.json', 'data/papers.csv']]
    for folder in ['docs', 'img', 'scripts']:
        files.extend(p for p in (ROOT / folder).rglob('*')
                     if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc')
    output = ROOT / 'output' / f'{NAME}.zip'
    output.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for file in sorted(files):
            archive.write(file, f'{NAME}/{file.relative_to(ROOT).as_posix()}')
    manifest = json.loads((ROOT / 'data/papers.json').read_text(encoding='utf-8'))
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None, 'Archive integrity check failed'
        names = archive.namelist()
        assert not any('/tmp/' in name or '/.git/' in name or name.endswith('.pdf')
                       or '/data/research_' in name for name in names)
        for paper in manifest['papers']:
            assert f"{NAME}/{paper['figure_path']}" in names
        packed = json.loads(archive.read(f'{NAME}/data/papers.json'))
        assert packed == manifest
    print(f'Created {output}: {len(files)} files, {len(manifest["papers"])} papers, '
          f'{output.stat().st_size / 1024 / 1024:.2f} MiB; archive verified.')


if __name__ == '__main__':
    package()
