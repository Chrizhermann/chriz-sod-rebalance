#!/usr/bin/env python3
"""Public265 dependency/XP integration with real WeiDU and synthetic game data.

The corrective library fixtures are composed, not inherited: their 16 tests do
not run again here. Set WEIDU_EXE to WeiDU 249 for the public TP2 parser.
"""
from __future__ import annotations

import re
import shutil
import unittest

try:
    from tests import test_comp265_installer as corrective
except ImportError:  # unittest discover -s tests
    import test_comp265_installer as corrective


PUBLIC = 'chriz-sod-remix/setup-chriz-sod-remix.tp2'
CHAPTER_XP = '''IF
  GlobalGT("bd_plot","global",400)
  GlobalLT("chapter","global",11)
THEN
  RESPONSE #100
    SetGlobal("bd_npc_camp_chapter","global",5)
    IncrementChapter("chptxt11")
    AddXPObject(Player1,20000)
    AddexperienceParty(103600)
    AddXPObject(Player2,20000)
    AddXPObject(Player3,20000)
    AddXPObject(Player4,20000)
    AddXPObject(Player5,20000)
    AddXPObject(Player6,20000)
END
'''
FOREIGN_XP = '''IF
  Global("FOREIGN_XP","GLOBAL",0)
THEN
  RESPONSE #100
    SetGlobal("FOREIGN_XP","GLOBAL",1)
    AddexperienceParty(777)
END
'''
ORIGINAL_XP = FOREIGN_XP + CHAPTER_XP + corrective.FOREIGN


@unittest.skipUnless(corrective.WEIDU.is_file(), 'real WeiDU unavailable; set WEIDU_EXE')
class FillerPublicInstallerTests(unittest.TestCase):
    def setUp(self):
        self.fixture_game = corrective.Component265InstallerTests(
            'test_full_repair_preserves_raw_items_other_tables_quests_and_ai')
        self.fixture_game.setUp()
        self.addCleanup(self.fixture_game.doCleanups)
        self.game = self.fixture_game.game
        self.override = self.fixture_game.override
        shutil.copytree(corrective.ROOT / 'chriz-sod-remix',
                        self.game / 'chriz-sod-remix', dirs_exist_ok=True)
        for name, definitions in {
            'action': '161 IncrementChapter(S:RESREF*)\n164 AddexperienceParty(I:XP*)\n259 AddXPObject(O:Object*,I:XP*)\n',
            'trigger': '0x4034 GlobalGT(S:Name*,S:Area*,I:Value*)\n0x4035 GlobalLT(S:Name*,S:Area*,I:Value*)\n',
            'object': ''.join(f'{20+n} Player{n}\n' for n in range(2, 7)),
        }.items():
            path = self.override / f'{name}.ids'
            path.write_text(path.read_text() + definitions, encoding='ascii')
        path = self.game / 'fixture/setup-fixture.tp2'
        path.write_text(path.read_text() + 'COMPILE ~fixture/bd4000.baf~\nCOMPILE ~fixture/bd0063.baf~\n')

    def prepare(self, xp=ORIGINAL_XP, prerequisites=(260, 240)):
        (self.game / 'fixture/bd4000.baf').write_text(xp, encoding='ascii')
        # Presence satisfies135's public resource predicate. Force-install265
        # must leave this script untouched despite135's INSTALL_BY_DEFAULT.
        (self.game / 'fixture/bd0063.baf').write_text(corrective.FOREIGN, encoding='ascii')
        self.fixture_game.fixture()
        self.log = next(p for p in self.game.iterdir() if p.name.lower() == 'weidu.log')
        # Synthetic history only; this test never opens a real install log.
        self.log.write_text(self.log.read_text() + ''.join(
            f'~{PUBLIC.upper()}~ #0 #{number} // synthetic prerequisite\n'
            for number in prerequisites), encoding='utf-8')
        self.before = corrective.tree(self.override)
        self.protected = {p:p.read_bytes() for p in (
            self.game/'chitin.key', self.game/'dialog.tlk',
            self.game/'lang/en_us/dialog.tlk')}

    def install(self):
        return self.fixture_game.run_weidu(PUBLIC, '--force-install-list', '265')

    def installed_components(self):
        return [int(m.group(1)) for m in re.finditer(
            r'^~[^~]*SETUP-CHRIZ-SOD-REMIX\.TP2~\s+#\d+\s+#(\d+)',
            self.log.read_text(), re.I | re.M)]

    def assert_preserved(self, changed):
        after = corrective.tree(self.override)
        self.assertEqual(after.keys(), self.before.keys())
        self.assertEqual({name for name in after if after[name] != self.before[name]}, changed)
        for path, data in self.protected.items():
            self.assertEqual(path.read_bytes(), data, str(path))

    def assert_xp_contract(self):
        actual = corrective.compact(self.fixture_game.decompile('bd4000.bcs'))
        self.assertEqual(actual, corrective.compact(ORIGINAL_XP.replace(
            'AddexperienceParty(103600)', 'AddexperienceParty(106800)')))
        for member in range(1, 7):
            self.assertEqual(actual.count(f'ADDXPOBJECT(PLAYER{member},20000)'), 1)
        self.assertEqual(actual.count('ADDEXPERIENCEPARTY(106800)'), 1)
        self.assertNotIn('ADDEXPERIENCEPARTY(3200)', actual)

    def assert_failed_and_rolled_back(self):
        result = self.install()
        self.assertNotEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertIn('NOT INSTALLED DUE TO ERRORS', result.stdout)
        self.assertIn('comp265', result.stdout+result.stderr)
        self.assert_preserved(set())
        self.assertNotIn(265, self.installed_components())
        self.assertNotIn(135, self.installed_components())

    def test_public265_with240_applies_all_repairs_and_future_xp_only(self):
        self.prepare()
        self.fixture_game.assert_success(self.install())
        self.assert_preserved({'BD5000.ARE','BD5110.ARE','BD5000.BCS','BDASHIRU.BCS','BD4000.BCS'})
        self.assertEqual(self.installed_components(), [260,240,265])
        self.assert_xp_contract()
        self.assertEqual(corrective.compact(self.fixture_game.decompile('bdashiru.bcs')),
                         corrective.compact(corrective.CURRENT_ASHIRUK))
        target = corrective.containers((self.override/'bd5000.are').read_bytes())['Dead_fighter']
        self.assertEqual(sum(raw[:8] == b'BDMISC68' for raw in target), 1)

    def test_public265_without240_still_removes_globally_banned_summons(self):
        self.prepare(prerequisites=(260,))
        self.fixture_game.assert_success(self.install())
        self.assert_preserved({'BD5000.ARE','BD5110.ARE','BD5000.BCS','BDASHIRU.BCS','BD4000.BCS'})
        self.assertEqual(self.installed_components(), [260,265])
        self.assert_xp_contract()
        self.assertEqual(corrective.compact(self.fixture_game.decompile('bdashiru.bcs')),
                         corrective.compact(corrective.CURRENT_ASHIRUK))

    def test_missing260_is_skipped_and_never_installs_default135(self):
        self.prepare(prerequisites=(240,))
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertIn('SKIPPING', result.stdout)
        self.assertNotIn('NOT INSTALLED DUE TO ERRORS', result.stdout)
        self.assert_preserved(set())
        self.assertEqual(self.installed_components(), [240])

    def test_unknown_xp_amount_rolls_back_corrective_resources(self):
        self.prepare(ORIGINAL_XP.replace('103600','103601'))
        self.assert_failed_and_rolled_back()

    def test_missing_xp_anchor_rolls_back_corrective_resources(self):
        self.prepare(ORIGINAL_XP.replace('    AddexperienceParty(103600)\n',''))
        self.assert_failed_and_rolled_back()

    def test_missing_xp_resource_is_skipped_before_resource_writes(self):
        self.prepare(); (self.override/'bd4000.bcs').unlink()
        self.before = corrective.tree(self.override)
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertIn('SKIPPING', result.stdout)
        self.assert_preserved(set())
        self.assertNotIn(265, self.installed_components())

    def test_missing_ashiruk_without240_is_skipped_before_resource_writes(self):
        self.prepare(prerequisites=(260,)); (self.override/'bdashiru.bcs').unlink()
        self.before = corrective.tree(self.override)
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertIn('SKIPPING', result.stdout)
        self.assert_preserved(set())
        self.assertEqual(self.installed_components(), [260])

    def test_already_corrected_xp_rejects_an_unrecorded_second_delta(self):
        self.prepare(ORIGINAL_XP.replace('103600','106800'))
        self.assert_failed_and_rolled_back()

    def test_two_original_xp_anchors_are_rejected(self):
        self.prepare(ORIGINAL_XP + CHAPTER_XP)
        self.assert_failed_and_rolled_back()

    def test_original_and_corrected_xp_anchors_together_are_rejected(self):
        self.prepare(ORIGINAL_XP + CHAPTER_XP.replace('103600','106800'))
        self.assert_failed_and_rolled_back()


if __name__ == '__main__':
    unittest.main(verbosity=2)
