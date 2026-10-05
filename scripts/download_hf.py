"""Pinned, resumable public-resource downloader; standard library plus curl."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import zipfile
import zlib

MANIFEST = json.loads(Path(__file__).with_name('hf_resources.json').read_text())


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def fetch(url, target, sha256):
    target = Path(target)
    if any(parent.is_symlink() for parent in target.parents):
        raise ValueError('Refusing symlink download directories: ' + str(target))
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.is_symlink():
        raise ValueError('Refusing a symlink download target: ' + str(target))
    if target.exists():
        if digest(target) != sha256:
            raise ValueError('Existing file has the wrong SHA-256; move it aside: ' + str(target))
        print('Verified existing: ' + str(target), flush=True)
        return
    partial = target.with_name(target.name + '.partial')
    if partial.is_symlink():
        raise ValueError('Refusing a symlink partial file')
    if not partial.exists() or digest(partial) != sha256:
        subprocess.run(['curl', '--fail', '--location', '--continue-at', '-',
                        '--retry', '5', '--retry-delay', '2', '--output', str(partial), url], check=True)
    if digest(partial) != sha256:
        raise ValueError('Download checksum mismatch; move this partial file aside and retry: ' + str(partial))
    os.replace(partial, target)


def safe_members(archive):
    names = set()
    for member in archive.infolist():
        path = PurePosixPath(member.filename)
        if (not path.parts or path.is_absolute() or '..' in path.parts or
                '\\' in member.filename or
                (len(path.parts[0]) >= 2 and path.parts[0][1] == ':') or
                member.filename in names or stat.S_ISLNK(member.external_attr >> 16)):
            raise ValueError('Unsafe or duplicate archive member: ' + member.filename)
        names.add(member.filename)
        yield member


def unpack_haps(archive_path, root, expected):
    output = root / 'HAPS2_0'
    if output.is_symlink():
        raise ValueError('Refusing a symlink HAPS extraction directory')
    marker = root / 'downloads/haps-extracted.json'
    with zipfile.ZipFile(archive_path) as archive:
        members = list(safe_members(archive))
        files = []
        for member in members:
            if member.is_dir():
                continue
            parts = list(PurePosixPath(member.filename).parts)
            if parts[0] in ('human_motion_glbs_v3', 'HAPS2_0'):
                parts.pop(0)
            if parts:
                files.append((member, output.joinpath(*parts)))
        normalized = [str(p) for _, p in files]
        if len(normalized) != len(set(normalized)):
            raise ValueError('Duplicate normalized HAPS archive path')
        for member, destination in files:
            destination.parent.mkdir(parents=True, exist_ok=True)
            if destination.is_symlink() or any(p.is_symlink() for p in destination.parents if p != root.parent):
                raise ValueError('Refusing symlink extraction path: ' + str(destination))
            if destination.exists():
                crc = 0
                with destination.open('rb') as handle:
                    for block in iter(lambda: handle.read(1024 * 1024), b''):
                        crc = zlib.crc32(block, crc)
                if destination.stat().st_size != member.file_size or crc != member.CRC:
                    raise ValueError('Existing HAPS file differs; move it aside: ' + str(destination))
                continue
            partial = destination.with_name(destination.name + '.extract-partial')
            if partial.is_symlink():
                raise ValueError('Refusing a symlink extraction partial')
            with archive.open(member) as source, partial.open('wb') as target:
                shutil.copyfileobj(source, target)
            os.replace(partial, destination)
        marker.write_text(json.dumps({'sha256': expected, 'files': len(files)}) + '\n')
        print('HAPS 2.0 extraction verified: ' + str(len(files)) + ' files.', flush=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path, required=True)
    parser.add_argument('--target', choices=['core', 'cma', 'all'], default='core')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args(argv)
    root = args.destination.resolve()
    files = [f for f in MANIFEST['files'] if args.target in (f['target'], 'all')]
    for item in files:
        print(item['path'] + ' -> ' + str(root / item.get('destination', item['path'])), flush=True)
    print('Matterport3D is obtained separately under its license.', flush=True)
    if args.dry_run:
        return
    for item in files:
        target = root / item.get('destination', item['path'])
        sha = item['sha256']
        base = ('https://huggingface.co/datasets/fly1113/HA-VLN/resolve/' + MANIFEST['hf_revision']
                if item['source'] == 'hf' else
                'https://raw.githubusercontent.com/UWMILab/HA-VLN/' + MANIFEST['github_revision'] + '/Data')
        fetch(base + '/' + item['path'], target, sha)
        if item['path'] == 'HAPS2_0/HAPS2_0.zip':
            unpack_haps(target, root, sha)


if __name__ == '__main__':
    main()
