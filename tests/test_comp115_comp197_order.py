"""Focused #115/#197/#256 bridge-script compatibility with real WeiDU.

All resources are synthetic and installs run in disposable games. The #115
shape is the independent model shared with its #256 ordering regression;
#197's production patch function and #256's production world patch are real.
These checks establish installer/script preservation, not in-game acceptance.
"""
from pathlib import Path
import re
import shutil
import tempfile
import unittest

import test_comp256_world as world_fixture
import test_comp115_comp256_order as continuity_fixture
import test_comp256_aftermath as aftermath_fixture


SPAWN = '    CreateCreature("bdskie",[2485.2655],NW)'
NATIVE = world_fixture.SCRIPT.replace(
    '    CreateCreature("bdbence",[2425.2660],NW)',
    '    CreateCreature("bdbence",[2425.2660],NW)\n' + SPAWN)
SPAWN_LINE = re.compile(
    r'(?mi)^[ \t]*CreateCreature\("bdskie",\[2485\.2655\],NW\)'
    r'[ \t]*(?://[^\n]*)?\n')
FOREIGN = '''IF
  Global("csr_kh_fort","GLOBAL",1)
  Global("FOREIGN_MOD","GLOBAL",0)
THEN
  RESPONSE #100
    SetGlobal("FOREIGN_MOD","GLOBAL",9)
    Continue()
END
'''


@unittest.skipUnless(world_fixture.WEIDU.is_file(),
                     "real WeiDU unavailable; set WEIDU_EXE")
class SkieBridgeCompatibilityTests(unittest.TestCase):
    def setUp(self):
        self.harness = world_fixture.BridgeWorldTests()
        self.harness.setUp()
        self.addCleanup(self.harness.doCleanups)
        library = "chriz-sod-remix/lib/comp197_bridge.tpa"
        shutil.copy2(world_fixture.ROOT / library, self.harness.game / library)
        (self.harness.game / "skie.tp2").write_text('''BACKUP ~skie-backup~
AUTHOR ~test~
BEGIN ~production197 bridge spawn patch~ DESIGNATED 197
INCLUDE ~chriz-sod-remix/lib/comp197_bridge.tpa~
COPY_EXISTING ~bd2000.bcs~ ~override~
  DECOMPILE_AND_PATCH BEGIN
    LPF csr197_bridge_spawns END
  END
BUT_ONLY
''', encoding="ascii")

    def install_skie(self):
        return self.harness.weidu("skie.tp2", "--force-install-list", "197")

    def world(self):
        result = self.harness.install()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def remove_only_spawns(self, expected_count):
        before_text = self.harness.decompile()
        before_files = world_fixture.tree(self.harness.override)
        expected_text, count = SPAWN_LINE.subn("", before_text)
        self.assertEqual(count, expected_count)
        result = self.install_skie()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("SUCCESSFULLY INSTALLED", result.stdout)
        after_text = self.harness.decompile()
        # Compare the complete compiler-normalized script, including every
        # route guard and action outside the exact Skie spawn lines.
        self.assertEqual(world_fixture.compact(after_text),
                         world_fixture.compact(expected_text))
        after_files = world_fixture.tree(self.harness.override)
        self.assertEqual({name for name in before_files.keys() | after_files.keys()
                          if before_files.get(name) != after_files.get(name)},
                         {"BD2000.BCS"})
        self.assertNotIn('CREATECREATURE("BDSKIE"',
                         world_fixture.compact(after_text))
        return before_files, after_text

    def reject(self, source):
        self.harness.fixture(source)
        before = world_fixture.tree(self.harness.override)
        result = self.install_skie()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("chriz-sod-remix #197", result.stdout + result.stderr)
        self.assertEqual(world_fixture.tree(self.harness.override), before)

    def test_native_two_spawns_without_115_preserves_every_other_action(self):
        self.harness.fixture(NATIVE + FOREIGN)
        before, after = self.remove_only_spawns(2)
        self.assertEqual(world_fixture.compact(after).count(
            'ACTIONOVERRIDE("KHALID",SAVELOCATION('), 2)
        self.assertTrue(world_fixture.compact(after).endswith(
            world_fixture.compact(FOREIGN)))
        result = self.harness.weidu("skie.tp2", "--force-uninstall-list", "197")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(world_fixture.tree(self.harness.override), before)

    def test_115_four_spawns_preserves_both_native_victory_pairs(self):
        self.harness.fixture(continuity_fixture.continuity_script(NATIVE) + FOREIGN)
        _, after = self.remove_only_spawns(4)
        # The two ordinary branches retain their retreat actions, while the
        # carried routes and unrelated branch preserve their separate guards.
        text = world_fixture.compact(after)
        self.assertEqual(text.count('!GLOBAL("CSR_KH_FORT","GLOBAL",1)'), 2)
        self.assertEqual(text.count('ACTIONOVERRIDE("KHALID",SAVELOCATION('), 2)
        self.assertTrue(text.endswith(world_fixture.compact(FOREIGN)))

    def test_115_forks_preserve_foreign_conditions_and_actions_inside_victories(self):
        def extend_victory(match):
            block = match.group(0)
            if SPAWN not in block:
                return block
            return block.replace("THEN\n", '  Global("FOREIGN_GATE","GLOBAL",1)\nTHEN\n', 1).replace(
                SPAWN + "\n", SPAWN + '\n    SetGlobal("FOREIGN_VICTORY","GLOBAL",7)\n', 1)

        source = continuity_fixture.BLOCK.sub(extend_victory, NATIVE)
        self.harness.fixture(continuity_fixture.continuity_script(source))
        _, after = self.remove_only_spawns(4)
        text = world_fixture.compact(after)
        self.assertEqual(text.count('GLOBAL("FOREIGN_GATE","GLOBAL",1)'), 4)
        self.assertEqual(text.count('SETGLOBAL("FOREIGN_VICTORY","GLOBAL",7)'), 4)

    def test_197_then_256_without_115_preserves_consolidated_victory(self):
        self.harness.fixture(NATIVE + FOREIGN)
        self.remove_only_spawns(2)
        self.world()
        text = world_fixture.compact(self.harness.decompile())
        self.assertNotIn('CREATECREATURE("BDSKIE"', text)
        self.assertEqual(text.count('CREATECREATUREOBJECT("BDBENCE",PLAYER1,6,0,0)'), 1)
        self.assertEqual(text.count('ACTIONOVERRIDE("KHALID",SAVELOCATION('), 1)
        self.assertTrue(text.endswith(world_fixture.compact(FOREIGN)))

    def test_115_then_197_then_256_preserves_both_consolidated_routes(self):
        self.harness.fixture(continuity_fixture.continuity_script(NATIVE) + FOREIGN)
        self.remove_only_spawns(4)
        self.world()
        after = self.harness.decompile()
        continuity_fixture.assert_victory_routes(self, after)
        self.assertNotIn('CREATECREATURE("BDSKIE"', world_fixture.compact(after))
        self.assertTrue(world_fixture.compact(after).endswith(
            world_fixture.compact(FOREIGN)))

    def test_256_then_197_without_115_preserves_consolidated_victory(self):
        self.harness.fixture(NATIVE + FOREIGN)
        self.world()
        _, after = self.remove_only_spawns(1)
        text = world_fixture.compact(after)
        self.assertEqual(text.count('CREATECREATUREOBJECT("BDBENCE",PLAYER1,6,0,0)'), 1)
        self.assertIn('GLOBAL("CSR256_STAGE","BD2000",2)', text)
        self.assertIn('COMBATCOUNTER(0)', text)

    def test_115_then_256_then_197_preserves_both_recovery_routes(self):
        self.harness.fixture(continuity_fixture.continuity_script(NATIVE) + FOREIGN)
        self.world()
        _, after = self.remove_only_spawns(2)
        continuity_fixture.assert_victory_routes(self, after)

    def test_four_unforked_spawns_are_rejected(self):
        self.reject(NATIVE + "\n" + NATIVE)

    def test_three_spawn_partial_fork_is_rejected(self):
        first = next(m.group(0) for m in continuity_fixture.BLOCK.finditer(NATIVE)
                     if continuity_fixture.RETREAT in m.group(0))
        self.reject(NATIVE.replace(first, continuity_fixture.continuity_script(first), 1))

    def test_missing_carried_route_is_rejected(self):
        source = continuity_fixture.continuity_script(NATIVE)
        carried = next(m.group(0) for m in continuity_fixture.BLOCK.finditer(source)
                       if SPAWN in m.group(0)
                       and 'Global("csr_kh_fort"' in m.group(0)
                       and '!Global("csr_kh_fort"' not in m.group(0))
        self.reject(source.replace(carried, "", 1))

    def test_two_positive_guards_instead_of_complementary_routes_are_rejected(self):
        self.reject(continuity_fixture.continuity_script(NATIVE).replace(
            '!Global("csr_kh_fort","GLOBAL",1)',
            'Global("csr_kh_fort","GLOBAL",1)', 1))

    def test_fork_payload_disagreement_is_rejected(self):
        self.reject(continuity_fixture.continuity_script(NATIVE).replace(
            'AddJournalEntry(123,QUEST)', 'AddJournalEntry(124,QUEST)', 1))

    def test_extra_spawn_outside_known_victories_is_rejected(self):
        self.reject(continuity_fixture.continuity_script(NATIVE) +
                    FOREIGN.replace('    Continue()', SPAWN))

    def test_two_spawns_in_one_native_victory_are_rejected(self):
        source = NATIVE.replace(SPAWN + "\n", "", 1)
        self.reject(source.replace(SPAWN, SPAWN + "\n" + SPAWN, 1))

    def test_unknown_native_victory_guard_is_rejected(self):
        self.reject(NATIVE.replace('Dead("bdcrubbm")',
                                   'Dead("foreign")', 1))

    def test_consolidated_pair_payload_disagreement_is_rejected(self):
        self.harness.fixture(continuity_fixture.continuity_script(NATIVE))
        self.world()
        source = self.harness.decompile().replace('AddJournalEntry(123,QUEST)',
                                                'AddJournalEntry(124,QUEST)', 1)
        # Compile a mutation directly, avoiding a reinstall of the fixture
        # component and WeiDU's unrelated dependent-component reinstall path.
        (self.harness.game / "mutated.baf").write_text(source, encoding="ascii")
        (self.harness.game / "mutate.tp2").write_text('''BACKUP ~mutate-backup~
AUTHOR ~test~
BEGIN ~mutated script fixture~
COMPILE ~mutated.baf~
COPY_EXISTING ~mutated.bcs~ ~override/bd2000.bcs~
''', encoding="ascii")
        result = self.harness.weidu("mutate.tp2", "--force-install-list", "0")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        before = world_fixture.tree(self.harness.override)
        result = self.install_skie()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("chriz-sod-remix #197", result.stdout + result.stderr)
        self.assertEqual(world_fixture.tree(self.harness.override), before)

    def test_bence_starter_preserves_256_priority_in_both_install_orders(self):
        for world_first in (False, True):
            with self.subTest(world_first=world_first), tempfile.TemporaryDirectory(
                    prefix="csr197-bence-order-") as temporary:
                game = Path(temporary)
                aftermath_fixture.write_aftermath_fixture(game)
                action_ids = game / "override/action.ids"
                action_ids.write_text(action_ids.read_text() + '''50 MoveViewObject(O:Target*,I:ScrollSpeed*Scroll)
63 Wait(I:Time*)
86 SetInterrupt(I:State*BOOLEAN)
198 StartDialogNoSet(O:Object*)
229 FaceObject(O:Object*)
''', encoding="ascii")
                (game / "override/scroll.ids").write_text(
                    "IDS V1.0\n0 INSTANT\n", encoding="ascii")
                baf = game / "chriz-sod-remix/baf"
                baf.mkdir()
                shutil.copy2(world_fixture.ROOT / "chriz-sod-remix/baf/csr197bnc.baf", baf)
                (game / "skie-bence.tp2").write_text('''BACKUP ~skie-bence-backup~
AUTHOR ~test~
BEGIN ~production197 Bence starter~ DESIGNATED 197
EXTEND_TOP ~bdbence.bcs~ ~chriz-sod-remix/baf/csr197bnc.baf~
''', encoding="ascii")
                packages = [("aftermath.tp2", "256"), ("skie-bence.tp2", "197")]
                if not world_first:
                    packages.reverse()
                for package, component in [("fixture/setup-fixture.tp2", "0"), *packages]:
                    result = aftermath_fixture.run_weidu(
                        game, package, "--force-install-list", component)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                script = aftermath_fixture.decompile(game, "BDBENCE.BCS")
                model = aftermath_fixture.AftermathDecisions(script)
                model.actors["PLAYER1"].position = aftermath_fixture.at(6)
                # This fixture has one PC; resolve the legacy [PC] selector
                # to that actor for the bounded compiled-condition check.
                model.actors["[PC]"] = model.actors["PLAYER1"]

                def first_actions():
                    return next(actions for guards, actions in model.blocks
                                if model.conditions(guards))

                self.assertIn("CSR256_BENCE_TRY", "\n".join(first_actions()))
                model.combat_counter = 1
                self.assertEqual(["NoAction()"], [a.strip() for a in first_actions()])
                model.variables[("BD2000", "CSR256_STAGE")] = 0
                self.assertIn("CSR_BENCE_OT", "\n".join(first_actions()).upper())


if __name__ == "__main__":
    unittest.main()
