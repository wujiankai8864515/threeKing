#!/usr/bin/env python3
"""Verify all indexed content and restore original paths into a NEW directory."""
from pathlib import Path
import argparse, hashlib, json, shutil
p=argparse.ArgumentParser(); p.add_argument('--verify-only',action='store_true'); p.add_argument('--output',type=Path); a=p.parse_args()
snapshot=Path(__file__).resolve().parents[1]
entries=json.loads((snapshot/'asset-index.json').read_text())['entries']
for e in entries:
    src=snapshot/e['stored_path']
    if not src.resolve().is_relative_to(snapshot): raise SystemExit('Unsafe source path')
    if hashlib.sha256(src.read_bytes()).hexdigest()!=e['sha256']: raise SystemExit('Checksum mismatch: '+str(src))
print('Verified',len(entries),'indexed files')
if a.verify_only: raise SystemExit(0)
if a.output is None: p.error('--output is required unless --verify-only')
if a.output.exists(): raise SystemExit('Output must not exist; old versions will not be overwritten')
a.output.mkdir(parents=True)
for e in entries:
    target=a.output/e['original_path']
    if not target.resolve().is_relative_to(a.output.resolve()): raise SystemExit('Unsafe original path')
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(snapshot/e['stored_path'],target)
print('Restored to',a.output)
