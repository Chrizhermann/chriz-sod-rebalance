"""Khalid continuity and bridge-world install ordering, with real WeiDU.

Synthetic cases run without game resources. The optional effective-resource
cases read CSR_DEV_GAME and install only into disposable fixture copies. These
are installer/script checks, not native encounter acceptance.
"""
from pathlib import Path
import re
import subprocess
import unittest

import test_comp256_world as world_fixture
from test_comp256_world import SCRIPT, BODY, WEIDU, tree, compact
from test_khalid_continuity_installer import (
    DEV_GAME, RESOURCE_NAMES, EffectiveKhalidGame, biff_only_ids, baf_blocks)


RETREAT = "".join(line + "\n" for line in BODY.splitlines()
                  if 'ActionOverride("khalid"' in line)
BLOCK = re.compile(r"(?ms)^IF\n.*?^END\n")


def continuity_script(source=SCRIPT):
    """Independent model of #115's exact carried/noncarried native fork."""
    def fork(match):
        original = match.group(0)
        if RETREAT not in original:
            return original
        carried = original.replace(RETREAT, "").replace(
            "IF\n", 'IF\n  Global("csr_kh_fort","GLOBAL",1)\n', 1)
        ordinary = original.replace(
            "IF\n", 'IF\n  !Global("csr_kh_fort","GLOBAL",1)\n', 1)
        return carried + "\n" + ordinary
    return BLOCK.sub(fork, source)


def assert_victory_routes(case, source):
    routes = [(guard, actions) for guard, actions in baf_blocks(source)
              if 'createcreatureobject("bdbence",player1,6,0,0)' in actions]
    case.assertEqual(len(routes), 2)
    carried = next((g, a) for g, a in routes if
                   g.startswith('global("csr_kh_fort","global",1)'))
    ordinary = next((g, a) for g, a in routes if
                    g.startswith('!global("csr_kh_fort","global",1)'))
    case.assertEqual(carried[0], ordinary[0][1:])
    for guard, actions in routes:
        for condition in ('global("csr256_stage","bd2000",2)',
                          'globallt("bd_plot","global",293)',
                          'combatcounter(0)', 'inmyarea(player1)', 'hpgt(player1,0)'):
            case.assertIn(condition, guard)
        for dv in ('FM', 'CM', 'G1', 'G2', 'E1', 'E2', 'F1', 'F2'):
            for condition in (f'dead("csr256{dv}")', f'!exists("csr256{dv}")',
                              f'statecheck("csr256{dv}",state_stone_death)'):
                case.assertIn(condition.lower(), guard)
        for action in ('setglobal("csr256_stage","bd2000",3)',
                       'setglobal("bd_plot","global",293)',
                       'setglobal("bd_cant_rest","myarea",0)',
                       'setglobaltimer("bd_npc_banter","global",five_rounds)'):
            case.assertIn(action, actions)
        case.assertEqual(actions.count('addjournalentry('), 1)
    retreat = compact(RETREAT).lower()
    case.assertNotIn('actionoverride("khalid"', carried[1])
    case.assertIn(retreat, ordinary[1])
    case.assertEqual(carried[1], ordinary[1].replace(retreat, ""))
    return routes


@unittest.skipUnless(WEIDU.is_file(), "real WeiDU unavailable; set WEIDU_EXE")
class SyntheticBridgeOrderTests(unittest.TestCase):
    def setUp(self):
        self.harness = world_fixture.BridgeWorldTests()
        self.harness.setUp()
        self.addCleanup(self.harness.doCleanups)

    def install(self, script):
        self.harness.fixture(script)
        before = tree(self.harness.override)
        result = self.harness.install()
        return before, result

    def reject(self, script):
        before, result = self.install(script)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("chriz-sod-remix #256", result.stdout + result.stderr)
        self.assertEqual(tree(self.harness.override), before)
        backup = self.harness.game / "world-backup/256"
        self.assertFalse(backup.exists() and any(
            p.suffix.lower() in {".bcs", ".are"} for p in backup.iterdir()))

    def test_115_first_retains_both_victory_routes_and_unrelated_branches(self):
        foreign = '''IF
  Global("csr_kh_fort","GLOBAL",1)
  Global("FOREIGN_MOD","GLOBAL",0)
THEN
  RESPONSE #100
    SetGlobal("FOREIGN_MOD","GLOBAL",9)
    Continue()
END
'''
        before, result = self.install(continuity_script() + foreign)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        output = self.harness.decompile()
        assert_victory_routes(self, output)
        self.assertTrue(compact(output).endswith(compact(foreign)))
        self.assertEqual(compact(output).count('SETGLOBAL("CSR256_REQUEST","BD2000",1)'), 2)
        result = self.harness.weidu("world.tp2", "--force-uninstall-list", "256")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(tree(self.harness.override), before)

    def test_native_skie_is_preserved_in_both_continuity_routes(self):
        source = SCRIPT.replace('    CreateCreature("bdbence",[2425.2660],NW)',
            '    CreateCreature("bdbence",[2425.2660],NW)\n'
            '    CreateCreature("bdskie",[2485.2655],NW)')
        _, result = self.install(continuity_script(source))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        routes = assert_victory_routes(self, self.harness.decompile())
        for _, actions in routes:
            self.assertEqual(actions.count('createcreature("bdskie",[2485.2655],nw)'), 1)

    def test_missing_carried_branch_is_rejected_before_writes(self):
        source = continuity_script()
        carried = next(m.group(0) for m in BLOCK.finditer(source)
                       if 'Global("csr_kh_fort"' in m.group(0)
                       and '!Global("csr_kh_fort"' not in m.group(0))
        self.reject(source.replace(carried, "", 1))

    def test_only_one_native_victory_forked_is_rejected(self):
        first = next(m.group(0) for m in BLOCK.finditer(SCRIPT) if RETREAT in m.group(0))
        self.reject(SCRIPT.replace(first, continuity_script(first), 1))

    def test_carried_and_ordinary_payload_disagreement_is_rejected(self):
        self.reject(continuity_script().replace('AddJournalEntry(123,QUEST)',
                                               'AddJournalEntry(124,QUEST)', 1))

    def test_unknown_added_action_even_in_both_copies_is_rejected(self):
        self.reject(continuity_script(SCRIPT.replace('    AddJournalEntry(123,QUEST)',
            '    NoAction()\n    AddJournalEntry(123,QUEST)')))

    def test_duplicate_carried_branch_is_rejected(self):
        source = continuity_script()
        carried = next(m.group(0) for m in BLOCK.finditer(source)
                       if 'Global("csr_kh_fort"' in m.group(0)
                       and '!Global("csr_kh_fort"' not in m.group(0))
        self.reject(source + carried)


@unittest.skipUnless(WEIDU.is_file(), "real WeiDU unavailable; set WEIDU_EXE")
@unittest.skipUnless((DEV_GAME / "override").is_dir(),
                     "effective pre-115 fixture unavailable; set CSR_DEV_GAME")
class EffectiveBridgeOrderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = {p.name.casefold(): p for p in (DEV_GAME / "override").iterdir() if p.is_file()}
        missing = RESOURCE_NAMES - source.keys()
        if missing:
            raise AssertionError(f"effective fixture lacks {sorted(missing)}")
        cls.resources = {name: path.read_bytes() for name, path in source.items()
                         if name in RESOURCE_NAMES or
                         (path.suffix.casefold() == ".ids" and name != "add_spell.ids")}
        cls.resources.update(biff_only_ids(DEV_GAME, set(source)))
        cls.tlk = (DEV_GAME / "lang/en_us/dialog.tlk").read_bytes()

    def fixture(self):
        game = EffectiveKhalidGame(self.resources, self.tlk)
        self.addCleanup(game.cleanup)
        (game.root / "world.tp2").write_text('''BACKUP ~world-backup~
AUTHOR ~test~
BEGIN ~production256 world seams~ DESIGNATED 256
OUTER_SET csr256_warning = 123
INCLUDE ~chriz-sod-remix/lib/comp256_world.tpa~
LAF csr256_world_preflight END
LAF csr256_world_install END
''', encoding="ascii")
        return game

    def world(self, game):
        result = subprocess.run([str(WEIDU), "world.tp2", "--force-install-list", "256",
            "--language", "0", "--use-lang", "en_us", "--no-exit-pause", "--noautoupdate"],
            cwd=game.root, capture_output=True, text=True, errors="replace", timeout=90)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("SUCCESSFULLY INSTALLED", result.stdout)

    def run_order(self, *, world_first):
        game = self.fixture()
        if world_first:
            self.world(game)
        result, transcript = game.install()
        self.assertEqual(result.returncode, 0, transcript)
        self.assertIn("SUCCESSFULLY INSTALLED", transcript)
        before_world = game.tree()
        if not world_first:
            self.world(game)
            after_world = game.tree()
            self.assertEqual({name for name in before_world.keys() | after_world.keys()
                              if before_world.get(name) != after_world.get(name)},
                             {"bd2000.bcs", "bd2000.are"})
        source = game.decompile("bd2000.bcs")["bd2000.bcs"]
        assert_victory_routes(self, source)
        # The independently installed #115 route/history and spokesman changes
        # must survive regardless of which component sees the native finale.
        for token in ('csr_kh_fort', 'csr_kh_carry', 'csr_jh_carry', 'bdbfort'):
            self.assertIn(token, source.lower())
        for protected, original in game.protected_before.items():
            self.assertEqual((game.root / protected).read_bytes(), original)

    def test_public_115_then_production_256_world(self):
        self.run_order(world_first=False)

    def test_production_256_world_then_public_115(self):
        self.run_order(world_first=True)


if __name__ == "__main__":
    unittest.main()
