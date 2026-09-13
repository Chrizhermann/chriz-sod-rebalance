"""Skie's SCS potion compatibility: real WeiDU, disposable games only.

Compiled script guards and byte-preservation are tested here. Native
TransformItem stack/slot preservation and inventory movement require playtest.
"""
from pathlib import Path
import re
import shutil
import struct
import tempfile
import unittest

from test_comp197_xp import (ROOT, WEIDU, decompile, run_weidu, tree,
                             write_skie_xp_fixture)


def potion(flags=0x68):
    data = bytearray(0x100)
    data[:8] = b'ITM V1  '
    struct.pack_into('<I', data, 0x18, flags)
    struct.pack_into('<H', data, 0x1c, 9)
    # Include embedded zero bytes and mixed-case data on both sides of flags.
    data[0x10:0x14] = b'A\0bC'
    data[0x40:0x44] = b'D\0eF'
    return bytes(data)


@unittest.skipUnless(WEIDU.is_file(), 'real WeiDU unavailable; set WEIDU_EXE')
class SkiePotionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='csr197-potions-')
        self.addCleanup(temporary.cleanup)
        self.game = Path(temporary.name)
        write_skie_xp_fixture(self.game)
        for filename, extra in {
            'action.ids': '356 TransformItem(S:OldItem*,S:NewItem*)\n',
            'trigger.ids': ('0x40D3 InPartyAllowDead(O:Object*)\n'
                            '0x406F Name(S:ScriptName*,O:Object*)\n'
                            '0x4009 HasItem(S:ResRef*,O:Object*)\n'),
        }.items():
            with (self.game / 'override' / filename).open('a') as stream:
                stream.write(extra)
        self.assert_success(run_weidu(self.game, 'fixture/setup-fixture.tp2',
                                      '--force-install-list', '0'))
        for name in ('minhp1.itm', 'dw#haspt.itm'):
            (self.game / 'override' / name).write_bytes(potion(0x28))
        # Keep the random tokens/table intact: conversion runs after the
        # engine resolves them, rather than replacing or duplicating tokens.
        (self.game / 'override/rndtres.2da').write_bytes(
            b'2DA V1.0\n*\n1 2 3\n'
            b'dw#rnd18 dw#ptn45 DW#BLANK *\n'
            b'dw#rnd38 dw#ptn10 dw#ptn10*2 DW#BLANK\n')
        (self.game / 'potions.tp2').write_text('''BACKUP ~potions-backup~
AUTHOR ~test~ BEGIN ~Palace Skie SCS potion cleanup~ DESIGNATED 197
INCLUDE ~chriz-sod-remix/lib/comp197_potions.tpa~
LAF csr197_install_potion_cleanup END
''')

    def pair(self, number):
        (self.game / 'override' / f'dw#ptn{number}.itm').write_bytes(potion())
        (self.game / 'override' / f'potn{number}.itm').write_bytes(potion(0x6c))

    def install(self, tp2='potions.tp2'):
        return run_weidu(self.game, tp2, '--force-install-list', '197')

    def assert_success(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_optional_scs_absent_is_byte_exact_noop(self):
        before = tree(self.game / 'override')
        self.assert_success(self.install())
        self.assertEqual(tree(self.game / 'override'), before)

    def test_single_present_pair_installs_only_its_conversion(self):
        for number in ('10', '45'):
            with self.subTest(number=number):
                self.pair(number)
                self.assert_success(self.install())
                source = decompile(self.game, 'bdskie.bcs').lower()
                self.assertEqual(re.findall(r'transformitem\("([^"]+)","([^"]+)"\)', source),
                                 [(f'dw#ptn{number}', f'potn{number}')])
                self.assert_success(run_weidu(self.game, 'potions.tp2',
                                              '--force-uninstall-list', '197'))
                for name in (f'dw#ptn{number}.itm', f'potn{number}.itm'):
                    (self.game / 'override' / name).unlink()

    def test_only_script_changes_and_uninstall_restores_exact_resources(self):
        self.pair('10')
        self.pair('45')
        before = tree(self.game / 'override')
        original_script = decompile(self.game, 'bdskie.bcs')
        self.assert_success(self.install())
        after = tree(self.game / 'override')
        self.assertEqual(after.keys(), before.keys())
        self.assertEqual({n for n in after if after[n] != before[n]}, {'BDSKIE.BCS'})
        self.assertTrue(decompile(self.game, 'bdskie.bcs').endswith(original_script))
        self.assert_success(run_weidu(self.game, 'potions.tp2',
                                      '--force-uninstall-list', '197'))
        self.assertEqual(tree(self.game / 'override'), before)

    def test_saved_and_fresh_actor_guard_only_converts_recruited_palace_skie(self):
        self.pair('10')
        self.pair('45')
        self.assert_success(self.install())
        source = re.sub(r'//[^\n]*', '', decompile(self.game, 'bdskie.bcs'))
        blocks = re.findall(r'\bIF\s+(.*?)\s+THEN\s+RESPONSE\s+#100\s+(.*?)\s+END',
                            source, flags=re.S | re.I)
        conversions = []
        for conditions, actions in blocks:
            if 'TransformItem' not in actions:
                continue
            # Full guards, not a weak action-only match: imported SKIE and
            # dismissed/unjoined BDSKIE must not receive this cleanup.
            compact_conditions = re.sub(r'\s+', '', conditions).lower()
            match = re.fullmatch(r'name\("bdskie",myself\)inpartyallowdead\(myself\)'
                                 r'hasitem\("(dw#ptn(?:10|45))",myself\)',
                                 compact_conditions)
            self.assertIsNotNone(match, conditions)
            old = match.group(1)
            self.assertEqual(re.sub(r'\s+', '', actions).lower(),
                             f'transformitem("{old}","potn{old[-2:]}")continue()')
            conversions.append(old)
        self.assertCountEqual(conversions, ['dw#ptn10', 'dw#ptn45'])
        # No startup-only/global/local latch, area or XP dependency that
        # would prevent a saved or freshly joined BDSKIE from being repaired.
        self.assertEqual(source.upper().count('SETGLOBAL('), 1)  # foreign block

    def test_second_tail_execution_does_not_duplicate_blocks(self):
        self.pair('10')
        self.pair('45')
        self.assert_success(self.install())
        before = tree(self.game / 'override')
        shutil.copyfile(self.game / 'potions.tp2', self.game / 'second.tp2')
        self.assert_success(self.install('second.tp2'))
        self.assertEqual(tree(self.game / 'override'), before)

    def test_already_droppable_clone_needs_no_conversion(self):
        self.pair('10')
        (self.game / 'override/dw#ptn10.itm').write_bytes(potion(0x6c))
        before = tree(self.game / 'override')
        self.assert_success(self.install())
        self.assertEqual(tree(self.game / 'override'), before)

    def test_changed_bytes_after_embedded_zero_abort_without_resource_changes(self):
        # Prefix/tail, case-only changes, flags and length all matter. This
        # catches accidentally NUL-terminated or case-folded binary compares.
        self.pair('10')
        for offset, value in ((0x12, ord('B')), (0x42, ord('E')), (0x18, 0x7c),
                              (0xff, 1), (0x100, 0)):
            with self.subTest(offset=offset):
                target = bytearray(potion(0x6c))
                if offset == len(target):
                    target.append(value)
                else:
                    target[offset] = value
                (self.game / 'override/potn10.itm').write_bytes(target)
                before = tree(self.game / 'override')
                result = self.install()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('differ beyond the droppable flag', result.stdout + result.stderr)
                self.assertEqual(tree(self.game / 'override'), before)

    def test_second_pair_conflict_rolls_back_first_pair_script_edit(self):
        self.pair('10')
        self.pair('45')
        target = bytearray(potion(0x6c))
        target[0xfe] = 1
        (self.game / 'override/potn45.itm').write_bytes(target)
        before = tree(self.game / 'override')
        self.assertNotEqual(self.install().returncode, 0)
        self.assertEqual(tree(self.game / 'override'), before)

    def test_missing_counterpart_aborts_without_guessing_replacement(self):
        (self.game / 'override/dw#ptn10.itm').write_bytes(potion())
        before = tree(self.game / 'override')
        result = self.install()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('exists without potn10.itm', result.stdout + result.stderr)
        self.assertEqual(tree(self.game / 'override'), before)

    def test_same_non_potion_pair_is_rejected(self):
        self.pair('10')
        for name in ('dw#ptn10.itm', 'potn10.itm'):
            target = bytearray((self.game / 'override' / name).read_bytes())
            struct.pack_into('<H', target, 0x1c, 1)
            (self.game / 'override' / name).write_bytes(target)
        before = tree(self.game / 'override')
        self.assertNotEqual(self.install().returncode, 0)
        self.assertEqual(tree(self.game / 'override'), before)

    def test_coexists_with_xp_ladder_without_changing_xp_or_cre(self):
        self.pair('10')
        self.assert_success(run_weidu(self.game, 'xp.tp2', '--force-install-list', '197'))
        before = tree(self.game / 'override')
        xp_script = decompile(self.game, 'bdskie.bcs')
        self.assert_success(self.install())
        after = tree(self.game / 'override')
        self.assertEqual({n for n in after if after[n] != before[n]}, {'BDSKIE.BCS'})
        self.assertTrue(decompile(self.game, 'bdskie.bcs').endswith(xp_script))

    def test_component_197_calls_cleanup_after_existing_companion_hooks(self):
        source = (ROOT / 'chriz-sod-remix/lib/comp197.tpa').read_text()
        self.assertEqual(source.count('LAF csr197_install_potion_cleanup END'), 1)
        self.assertLess(source.index('LAF csr197_install_dialogue_route END'),
                        source.index('LAF csr197_install_potion_cleanup END'))


if __name__ == '__main__':
    unittest.main()
