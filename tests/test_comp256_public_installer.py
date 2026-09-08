"""Install the actual public 256 entry across all composed production libraries.

Every resource is a synthetic fixture; no installed game is used or modified.
The source-world fixture is compiled by WeiDU before recording the baseline.
"""
from __future__ import annotations

from pathlib import Path
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_comp256_ai import write_ai_fixture
from test_comp256_creatures import creature, item, ITEMS, book, u
import test_comp256_world as world_fixtures
from test_comp256_text import dialogue, item as bwoosh_item
from test_comp256_visuals import wed, tis
from test_comp291_installer import WEIDU, tree


PUBLIC_TP2 = 'chriz-sod-remix/setup-chriz-sod-remix.tp2'


@unittest.skipUnless(WEIDU.is_file(), 'real WeiDU unavailable; set WEIDU_EXE')
class PublicBridgeInstallerTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix='csr256-public-')
        self.addCleanup(temp.cleanup)
        self.game = Path(temp.name)
        write_ai_fixture(self.game)
        # Unix WeiDU expects lowercase physical source filenames. Keep the
        # tracked art filenames intact and normalize only this disposable copy.
        if os.name != 'nt':
            for source in (self.game/'chriz-sod-remix/art/bridge').iterdir():
                if source.name != source.name.lower():
                    source.rename(source.with_name(source.name.lower()))
        self.override = self.game/'override'
        world = world_fixtures.BridgeWorldTests()
        world.setUp()
        self.addCleanup(world.doCleanups)
        world.fixture()
        for file in world.override.glob('*.ids'):
            target = self.override/file.name
            current = target.read_text() if target.exists() else 'IDS V1.0\n'
            additions = [line for line in file.read_text().splitlines()
                         if line and not line.startswith('IDS') and line not in current.splitlines()]
            target.write_text(current+'\n'+'\n'.join(additions)+'\n')
        for name in ('bd2000.are', 'bd2000.bcs'):
            shutil.copy2(world.override/name, self.override/name)
        # Public controller stage 1 displays its warning in the log.
        action = self.override/'action.ids'
        action.write_text(action.read_text()+'262 DisplayStringNoName(O:Object*,I:StrRef*)\n')
        for ref in ('BDOLONEI BDCRUE45 BDELFIRL BDELFIRM BDELFIRG '
                    'ELEARL01 ELEAR01 ELEARG01').split():
            (self.override/(ref+'.cre').lower()).write_bytes(creature(
                cls=1 if ref == 'BDOLONEI' else 2,
                hp=52 if ref == 'BDOLONEI' else 108,
                immunity=ref.startswith('ELEAR') or ref in ('BDELFIRM', 'BDELFIRG')))
        for ref in ITEMS:
            (self.override/(ref+'.itm').lower()).write_bytes(item(fire=ref.startswith('FIRE')))
        (self.override/'bdphosse.dlg').write_bytes(dialogue())
        (self.override/'bdbwoosh.itm').write_bytes(bwoosh_item())
        for name in ('BD2000', 'BD2000N'):
            (self.override/(name+'.wed').lower()).write_bytes(wed(name))
            (self.override/(name+'.tis').lower()).write_bytes(tis())
        # This old stopgap donor is never altered by the replacement component.
        (self.override/'bdkegx.cre').write_bytes(creature(hp=25))

    def run_public(self, *args):
        return subprocess.run([str(WEIDU), PUBLIC_TP2, *args,
                               '--game', str(self.game), '--language', '0',
                               '--use-lang', 'en_US', '--no-exit-pause', '--skip-at-view'],
                              cwd=self.game, capture_output=True, text=True,
                              encoding='utf-8', errors='replace', timeout=90)

    def success(self, result):
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertIn('SUCCESSFULLY INSTALLED', result.stdout)
        self.assertFalse((self.game/'-').exists(), 'Preflight must not write a literal dash file')

    def test_public_install_and_uninstall_restore_all_original_resources(self):
        original = tree(self.override)
        source_wed = (self.override/'bd2000.wed').read_bytes()
        self.success(self.run_public('--force-install-list', '256'))
        log = (self.game/'weidu.log').read_text()
        self.assertIn('#256', log)
        self.assertNotIn('#255', log)
        for name in ('csr26fma.bcs', 'csr26cma.bcs', 'csr26mel.bcs',
                     'CSR256FM.CRE', 'CSR256CM.CRE', 'CSR256G1.CRE',
                     'CSR26E1G.CRE', 'CSR26F1G.CRE', 'B200090.PVRZ', 'B2000N90.PVRZ'):
            self.assertTrue((self.override/name.lower()).is_file(), name)
        fire = (self.override/'csr256fm.cre').read_bytes()
        self.assertEqual(book(fire)['SPWI305'], 1)
        self.assertEqual(book(fire)['SPWI408'], 2)
        self.assertEqual(book(fire)['SPWI212'], 3)
        self.assertEqual(u(fire, 0x14), 1000)
        self.assertEqual((self.override/'bd2000.wed').read_bytes(), source_wed)
        self.assertEqual(original['BDKEGX.CRE'], tree(self.override)['BDKEGX.CRE'])
        result = self.run_public('--force-uninstall-list', '256')
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertEqual(tree(self.override), original)

    def test_old_255_stays_installed_and_unchanged_when_256_is_appended(self):
        self.success(self.run_public('--force-install-list', '255'))
        before = tree(self.override)
        old_barrel = (self.override/'bdkegx.cre').read_bytes()
        self.assertEqual(struct.unpack_from('<HH', old_barrel, 0x24), (120, 120))
        self.success(self.run_public('--force-install-list', '256'))
        log = (self.game/'weidu.log').read_text()
        self.assertIn('#255', log)
        self.assertIn('#256', log)
        self.assertEqual((self.override/'bdkegx.cre').read_bytes(), old_barrel)
        result = self.run_public('--force-uninstall-list', '256')
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertEqual(tree(self.override), before)
        self.assertIn('#255', (self.game/'weidu.log').read_text())

    def test_late_visual_mismatch_prevents_all_ai_creature_world_text_writes(self):
        (self.override/'b2000n90.pvrz').write_bytes(b'FOREIGN NIGHT TEXTURE PAGE')
        before = tree(self.override)
        tlk = (self.game/'lang/en_us/dialog.tlk').read_bytes()
        result = self.run_public('--force-install-list', '256')
        self.assertNotEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertIn('reserved bridge texture page already exists', result.stdout+result.stderr)
        self.assertEqual(tree(self.override), before)
        self.assertEqual((self.game/'lang/en_us/dialog.tlk').read_bytes(), tlk)
        self.assertFalse(any(p.name.lower().startswith('csr26') for p in self.override.iterdir()))
        self.assertFalse((self.game/'-').exists())


if __name__ == '__main__':
    unittest.main()
