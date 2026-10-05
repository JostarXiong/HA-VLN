"""Regression checks for the Docker CMA onboarding path."""
import ast
import hashlib
import importlib.util
from pathlib import Path
import tempfile
from types import SimpleNamespace, ModuleType
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('download_hf', ROOT / 'scripts/download_hf.py')
download = importlib.util.module_from_spec(spec)
spec.loader.exec_module(download)


class DownloadTests(unittest.TestCase):
    def test_resume_keeps_partial_and_checks_hash(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / 'checkpoint.pth'
            partial = target.with_name(target.name + '.partial')
            partial.write_bytes(b'prefix')
            data = b'prefix-rest'
            def curl(args, check):
                self.assertEqual(args[args.index('--continue-at') + 1], '-')
                self.assertEqual(partial.read_bytes(), b'prefix')
                partial.write_bytes(data)
            with patch.object(download.subprocess, 'run', side_effect=curl):
                download.fetch('https://example.invalid/checkpoint', target, hashlib.sha256(data).hexdigest())
            self.assertEqual(target.read_bytes(), data)
            self.assertFalse(partial.exists())

    def test_existing_haps_directory_is_completed_and_repeat_is_stable(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'downloads').mkdir()
            archive = root / 'downloads/haps.zip'
            first = root / 'HAPS2_0/activity:walking/0.glb'
            first.parent.mkdir(parents=True)
            first.write_bytes(b'first')
            stamp = first.stat().st_mtime_ns
            with zipfile.ZipFile(archive, 'w') as z:
                z.writestr('human_motion_glbs_v3/activity:walking/0.glb', b'first')
                z.writestr('human_motion_glbs_v3/activity:walking/1.glb', b'second')
            for _ in range(2):
                download.unpack_haps(archive, root, 'example')
            self.assertEqual(first.stat().st_mtime_ns, stamp)
            self.assertEqual(first.with_name('1.glb').read_bytes(), b'second')
            self.assertTrue((root / 'downloads/haps-extracted.json').is_file())

    def test_archive_traversal_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            archive = Path(temp) / 'unsafe.zip'
            with zipfile.ZipFile(archive, 'w') as z:
                z.writestr('../escape.glb', b'x')
            with zipfile.ZipFile(archive) as z, self.assertRaises(ValueError):
                list(download.safe_members(z))

    def test_corrupt_existing_file_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / 'checkpoint.pth'
            target.write_bytes(b'wrong')
            with self.assertRaises(ValueError):
                download.fetch('https://example.invalid', target, hashlib.sha256(b'right').hexdigest())
            self.assertEqual(target.read_bytes(), b'wrong')

    def test_all_downloads_include_both_input_formats_and_annotations(self):
        fetched = []
        with tempfile.TemporaryDirectory() as temp:
            with patch.object(download, 'fetch', side_effect=lambda url, target, sha: fetched.append(str(target))), patch.object(download, 'unpack_haps'):
                download.main(['--destination', temp, '--target', 'all'])
        self.assertEqual(len(fetched), 9)
        for split in ('val_seen', 'val_unseen'):
            self.assertTrue(any(p.endswith(split + '.json.gz') for p in fetched))
            self.assertTrue(any(p.endswith(split + '_bertidx.json.gz') for p in fetched))
            self.assertTrue(any(p.endswith('collision_num_' + split + '.json') for p in fetched))
        self.assertTrue(any(p.endswith('human_motion.json') for p in fetched))


class DetectorTests(unittest.TestCase):
    def trainer(self, enabled):
        source = ROOT / 'agent/VLN-CE/vlnce_baselines/common/base_il_trainer.py'
        tree = ast.parse(source.read_text())
        cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'BaseVLNCETrainer')
        cls.body = [next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == '__init__')]
        module = ast.Module(body=[cls], type_ignores=[])
        config = SimpleNamespace(TORCH_GPU_ID=0, TASK_CONFIG=SimpleNamespace(SIMULATOR=SimpleNamespace(HUMAN_COUNTING=enabled)))
        class Base:
            def __init__(self, config):
                self.config = config
        ns = {'BaseILTrainer': Base, 'torch': SimpleNamespace(cuda=SimpleNamespace(is_available=lambda: False), device=lambda name: name)}
        exec(compile(module, str(source), 'exec'), ns)
        return ns['BaseVLNCETrainer'](config)

    def test_disabled_counting_does_not_import_detector(self):
        import builtins
        original = builtins.__import__
        def guarded(name, *args, **kwargs):
            if name.startswith(('groundingdino', 'HASimulator.detector')):
                raise AssertionError('Optional detector imported during navigation')
            return original(name, *args, **kwargs)
        with patch('builtins.__import__', side_effect=guarded):
            self.assertIsNone(self.trainer(False).detector)

    def test_enabled_counting_still_constructs_detector(self):
        fake = ModuleType('HASimulator.detector')
        class Detector:
            def to(self, device):
                self.device = device
                return self
        fake.Detector = Detector
        with patch.dict('sys.modules', {'HASimulator.detector': fake}):
            self.assertEqual(self.trainer(True).detector.device, 'cpu')


if __name__ == '__main__':
    unittest.main()
