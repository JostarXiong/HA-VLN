#!/usr/bin/env bash
# Add CMA dependencies to the public Habitat 0.1.7 runtime container.
set -euo pipefail
repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
python -c 'import sys, torch; assert sys.version_info[:2] == (3, 8); assert torch.__version__ == "2.0.1+cu118"'
core_before=$(python -c 'import habitat; assert habitat.__version__ == "0.1.7"; print(habitat.__file__)')
python -m pip install --no-cache-dir -r "$repo_root/requirements-py38.txt" \
  --extra-index-url https://download.pytorch.org/whl/cu118
# Restore only habitat_baselines; keep the image's patched Habitat core.
python - <<'PY'
import hashlib
from pathlib import Path, PurePosixPath
import shutil
import site
import tarfile
import urllib.request

revision = 'd6ed1c0a0e786f16f261de2beafe347f4186d0d8'
expected = 'eb9a121a15ed58f788154f4e0ff8db80535b8a07bb057a0927d4ea600db2bf1b'
root = Path('/tmp/havln-cma-baselines')
root.mkdir(exist_ok=True)
archive = root / 'habitat-lab.tar.gz'
if not archive.exists():
    partial = archive.with_suffix('.partial')
    url = 'https://codeload.github.com/facebookresearch/habitat-lab/tar.gz/' + revision
    with urllib.request.urlopen(url, timeout=120) as source, partial.open('wb') as target:
        shutil.copyfileobj(source, target)
    partial.replace(archive)
assert hashlib.sha256(archive.read_bytes()).hexdigest() == expected, 'Habitat-Lab checksum mismatch'
with tarfile.open(archive) as source:
    for member in source.getmembers():
        parts = PurePosixPath(member.name).parts[1:]
        if not parts or parts[0] != 'habitat_baselines':
            continue
        if '..' in parts or not (member.isfile() or member.isdir()):
            raise ValueError('Unsafe Habitat-Baselines archive member')
        target = root.joinpath(*parts)
        if member.isdir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            with source.extractfile(member) as src, target.open('wb') as dst:
                shutil.copyfileobj(src, dst)
Path(site.getsitepackages()[0], 'havln_cma_baselines.pth').write_text(str(root) + '\n')
PY
core_after=$(python -c 'import habitat; print(habitat.__file__)')
[[ "$core_before" == "$core_after" ]] || { echo 'Habitat core changed unexpectedly.' >&2; exit 1; }
python -m pip check
python -c 'import habitat_baselines; print("CMA dependencies ready; Habitat core preserved.")'
