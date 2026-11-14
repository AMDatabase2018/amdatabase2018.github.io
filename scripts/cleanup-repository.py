"""Remove only reviewed upload leftovers; stop if any file has changed."""
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'scripts/cleanup-manifest.json').read_text())
    targets = []
    for name, expected in manifest.items():
        path = ROOT / name
        if Path(name).name != name or path.is_symlink():
            raise SystemExit('Refusing unexpected cleanup path: ' + name)
        if not path.exists():
            continue
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise SystemExit('File changed since review; no files deleted: ' + name)
        targets.append(path)
    for path in targets:
        print(('Deleting: ' if args.apply else 'Would delete: ') + path.name)
        if args.apply:
            path.unlink()
    print(f'{len(targets)} reviewed files; ' + ('cleanup complete.' if args.apply else 'dry run only.'))

if __name__ == '__main__':
    main()
