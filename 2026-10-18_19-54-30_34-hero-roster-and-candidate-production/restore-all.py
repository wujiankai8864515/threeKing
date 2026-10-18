from pathlib import Path
import argparse, hashlib, json, shutil, tempfile

def digest(path):
    with path.open('rb') as source:
        return hashlib.file_digest(source, 'sha256').hexdigest()

def contained(root, relative):
    path = root / relative
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError('Unsafe path: ' + str(relative))
    return path

parser = argparse.ArgumentParser(description='Verify or restore resolved project assets without modifying historical snapshots.')
parser.add_argument('--output', type=Path)
parser.add_argument('--copy-check', action='store_true', help='Sequential temporary copy and SHA256 check, without duplicating the tree.')
args = parser.parse_args()
repo = Path(__file__).resolve().parents[1]
latest = json.loads((repo / 'LATEST.json').read_text())
items = {}
for delta in [latest['snapshot']] + latest.get('asset_deltas', []):
    for entry in json.loads((repo / delta / 'asset-index.json').read_text())['entries']:
        entry = dict(entry)
        entry.setdefault('repository_path', delta + '/' + entry.get('stored_path', ''))
        items[entry['original_path']] = entry
if args.output and args.output.exists():
    raise SystemExit('Output must not exist')
if args.output:
    args.output.mkdir(parents=True)
with tempfile.TemporaryDirectory(prefix='threeKing-copy-check-') as temporary:
    test = Path(temporary) / 'one-file'
    for name, entry in items.items():
        source = contained(repo, entry['repository_path'])
        if digest(source) != entry['sha256']:
            raise RuntimeError('Archive SHA256 mismatch: ' + name)
        if args.copy_check:
            shutil.copy2(source, test)
            if digest(test) != entry['sha256']:
                raise RuntimeError('Copy SHA256 mismatch: ' + name)
            test.unlink()
        if args.output:
            target = contained(args.output, name)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            if digest(target) != entry['sha256']:
                raise RuntimeError('Restored SHA256 mismatch: ' + name)
print(json.dumps({'resolved_paths_verified': len(items), 'sequential_copy_checked': args.copy_check, 'restored_to': str(args.output) if args.output else None}))
