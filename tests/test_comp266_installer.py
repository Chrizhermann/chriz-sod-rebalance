#!/usr/bin/env python3
"""Real WeiDU tests for the append-only Shadow Aspect Mislead cap.

All writes and installs use disposable synthetic games. The native opening and
adjacent AI excerpts below were transcribed from the effective Combined-stack
BDASHIRU decompile on 2026-09-13; they are not a claim of native playtesting.
"""
from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "research/scripts"))
from test_comp291_installer import WEIDU, tree, write_fake_game


NATIVE_MISLEAD = '''IF
  !StateCheck(Myself,STATE_INVISIBLE)
  Difficulty(HARDEST)
  !GlobalTimerNotExpired("bd_invis","locals")
THEN
  RESPONSE #100
    SetGlobalTimer("bd_invis","locals",TWO_ROUNDS)
    CreateVisualEffectObject("shair",Myself)
    ApplySpell(Myself,WIZARD_MISLEAD)
END
'''

CAPPED_MISLEAD = '''IF
  !StateCheck(Myself,STATE_INVISIBLE)
  Difficulty(HARDEST)
  !GlobalTimerNotExpired("bd_invis","locals")
  Global("CSR266_MISLEAD","LOCALS",0)
THEN
  RESPONSE #100
    SetGlobal("CSR266_MISLEAD","LOCALS",1)
    SetGlobalTimer("bd_invis","locals",TWO_ROUNDS)
    CreateVisualEffectObject("shair",Myself)
    ApplySpell(Myself,WIZARD_MISLEAD)
END
'''

# Exact compiled native block extracted offline from BDASHIRU.BCS, whose complete
# source SHA256 was 462ca1008a0fca1176bd26ce01ca2558fdc1d7908c7502d7dcc0444a3edaae6c.
# Only SC framing is added. This independent binary fixture also verifies the
# target's real trigger/action IDs instead of relying only on fixture compilation.
NATIVE_MISLEAD_BCS = b'''SC
CR
CO
TR
16439 16 1 0 0 "" "" OB
0 0 0 0 0 0 0 1 0 0 0 0 ""OB
TR
TR
16592 5 0 0 0 "" "" OB
0 0 0 0 0 0 0 0 0 0 0 0 ""OB
TR
TR
16449 0 1 0 0 "bd_invis" "locals" OB
0 0 0 0 0 0 0 0 0 0 0 0 ""OB
TR
CO
RS
RE
100AC
115OB
0 0 0 0 0 0 0 0 0 0 0 0 ""OB
OB
0 0 0 0 0 0 0 0 0 0 0 0 ""OB
OB
0 0 0 0 0 0 0 0 0 0 0 0 ""OB
12 0 0 0 0"localsbd_invis" "" AC
AC
273OB
0 0 0 0 0 0 0 0 0 0 0 0 ""OB
OB
0 0 0 0 0 0 0 1 0 0 0 0 ""OB
OB
0 0 0 0 0 0 0 0 0 0 0 0 ""OB
0 0 0 0 0"shair" "" AC
AC
160OB
0 0 0 0 0 0 0 0 0 0 0 0 ""OB
OB
0 0 0 0 0 0 0 1 0 0 0 0 ""OB
OB
0 0 0 0 0 0 0 0 0 0 0 0 ""OB
2607 0 0 0 0"" "" AC
RE
RS
CR
SC
'''

# Actual effective neighbouring blocks: the cap must not suppress or rewrite
# the later invisibility fallback, normal Shadow summons, or offensive timer.
NATIVE_BEFORE = '''IF
  Die()
THEN
  RESPONSE #100
    CreateVisualEffectObject("shsmkjet",Myself)
    DestroySelf()
END
'''
NATIVE_AFTER = '''IF
  !StateCheck(Myself,STATE_INVISIBLE)
  DifficultyGT(EASY)
  !GlobalTimerNotExpired("bd_invis","locals")
THEN
  RESPONSE #100
    SetGlobalTimer("bd_invis","locals",THREE_ROUNDS)
    CreateVisualEffectObject("shair",Myself)
    ApplySpell(Myself,WIZARD_IMPROVED_INVISIBILITY)
END

IF
  !StateCheck(Myself,STATE_INVISIBLE)
  !DifficultyGT(EASY)
  !GlobalTimerNotExpired("bd_invis","locals")
THEN
  RESPONSE #100
    SetGlobalTimer("bd_invis","locals",THREE_ROUNDS)
    CreateVisualEffectObject("shair",Myself)
    ApplySpell(Myself,WIZARD_INVISIBILITY)
END

IF
  !StateCheck(Myself,STATE_INVISIBLE)
  Difficulty(HARD)
  !GlobalTimerNotExpired("bd_summons","locals")
  See(NearestEnemyOf(Myself))
THEN
  RESPONSE #100
    SetGlobalTimer("bd_summons","locals",TEN_ROUNDS)
    ApplySpell(Myself,WIZARD_SHADOW_DOOR)
    ApplySpell(Myself,WIZARD_DARKNESS_15_FOOT)
    CreateCreatureObject("bdshad04",Myself,1,0,0)
    CreateCreatureObject("bdshad04",Myself,1,0,0)
    Continue()
END

IF
  !StateCheck(Myself,STATE_INVISIBLE)
  Difficulty(HARDEST)
  !GlobalTimerNotExpired("bd_summons","locals")
  See(NearestEnemyOf(Myself))
THEN
  RESPONSE #100
    SetGlobalTimer("bd_summons","locals",TEN_ROUNDS)
    ApplySpell(Myself,WIZARD_SHADOW_DOOR)
    ApplySpell(Myself,WIZARD_DARKNESS_15_FOOT)
    CreateCreatureObject("bdshad04",Myself,1,0,0)
    CreateCreatureObject("bdshad04",Myself,1,0,0)
    Continue()
END

IF
  !GlobalTimerNotExpired("bd_cast","locals")
  DifficultyGT(EASY)
  !GlobalTimerNotExpired("WIZARD_DARKNESS_15_FOOT","locals")
  See(LastSeenBy)
  !Range(LastSeenBy,0)
  !StateCheck(LastSeenBy,STATE_REALLY_DEAD)
  !StateCheck(LastSeenBy,STATE_DEBUFF)
THEN
  RESPONSE #100
    SetGlobalTimer("WIZARD_DARKNESS_15_FOOT","locals",FIVE_ROUNDS)
    SetGlobalTimer("bd_cast","locals",ONE_ROUND)
    SpellNoDec(LastSeenBy,WIZARD_DARKNESS_15_FOOT)
  RESPONSE #50
    Continue()
END
'''
FOREIGN = '''IF
  Global("FOREIGN_BEHAVIOUR","LOCALS",0)
THEN
  RESPONSE #37
    SetGlobal("FOREIGN_BEHAVIOUR","LOCALS",9)
    Continue()
END
'''


@unittest.skipUnless(WEIDU.is_file(), "real WeiDU unavailable; set WEIDU_EXE")
class Component266InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="csr266-installer-")
        self.addCleanup(self.temp.cleanup)
        self.game = Path(self.temp.name)
        write_fake_game(self.game)
        self.override = self.game / "override"
        additions = {
            "action": '''115 SetGlobalTimer(S:Name*,S:Area*,I:Time*GTIMES)
160 ApplySpell(O:Target*,I:Spell*SPELL)
191 SpellNoDec(O:Target*,I:Spell*SPELL)
273 CreateVisualEffectObject(S:ResRef*,O:Target*)
''',
            "trigger": '''0x0025 Die()
0x4018 Range(O:Object*,I:Range*)
0x401C See(O:Object*)
0x4037 StateCheck(O:Object*,I:State*STATE)
0x4041 GlobalTimerNotExpired(S:Name*,S:Area*)
0x40D0 Difficulty(I:Amount*DIFFLEV)
0x40D1 DifficultyGT(I:Amount*DIFFLEV)
''',
            "object": "12 NearestEnemyOf\n18 LastSeenBy\n",
            "state": "16 STATE_INVISIBLE\n4032 STATE_REALLY_DEAD\n-2146095059 STATE_DEBUFF\n",
            "difflev": "2 EASY\n4 HARD\n5 HARDEST\n",
            "gtimes": "6 ONE_ROUND\n12 TWO_ROUNDS\n18 THREE_ROUNDS\n30 FIVE_ROUNDS\n60 TEN_ROUNDS\n",
            "spell": '''2206 WIZARD_INVISIBILITY
2228 WIZARD_DARKNESS_15_FOOT
2405 WIZARD_IMPROVED_INVISIBILITY
2505 WIZARD_SHADOW_DOOR
2607 WIZARD_MISLEAD
''',
        }
        for name, definitions in additions.items():
            path = self.override / f"{name}.ids"
            previous = path.read_text(encoding="ascii") if path.exists() else "IDS V1.0\n"
            path.write_text(previous + definitions, encoding="ascii")
        library = self.game / "chriz-sod-remix/lib"
        library.mkdir(parents=True)
        shutil.copy2(ROOT / "chriz-sod-remix/lib/comp266.tpa", library / "comp266.tpa")
        (self.game / "fixture").mkdir()
        (self.game / "fixture/setup-fixture.tp2").write_text('''BACKUP ~fixture/backup~
AUTHOR ~fixture~
BEGIN ~compile source fixture~ DESIGNATED 0
COMPILE ~fixture/bdashiru.baf~
COMPILE ~fixture/expected.baf~
''', encoding="ascii")
        for name in ("bdashiru.cre", "bd7230.are", "spwi607.spl", "bdshad04.cre", "bdshsoul.cre"):
            (self.override / name).write_bytes(b"UNCHANGED THIRD-PARTY RESOURCE\x00\xff" + name.encode())

    def run_weidu(self, *args):
        return subprocess.run([str(WEIDU), *args, "--game", str(self.game),
                               "--language", "0", "--use-lang", "en_US", "--no-exit-pause"],
                              cwd=self.game, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=45)

    def assert_success(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("SUCCESSFULLY INSTALLED", result.stdout)

    def fixture(self, target=NATIVE_MISLEAD, *, after=NATIVE_AFTER, target_only=False):
        prefix = "" if target_only else FOREIGN + NATIVE_BEFORE
        suffix = "" if target_only else after + FOREIGN
        (self.game / "fixture/bdashiru.baf").write_text(prefix + target + suffix, encoding="ascii")
        # Compile the desired complete script independently of the production regex.
        (self.game / "fixture/expected.baf").write_text(prefix + CAPPED_MISLEAD + suffix, encoding="ascii")
        self.assert_success(self.run_weidu("fixture/setup-fixture.tp2", "--force-install-list", "0"))

    def repair(self, name="repair"):
        (self.game / f"{name}.tp2").write_text(f'''BACKUP ~{name}-backup~
AUTHOR ~fixture~
BEGIN ~production component266 harness~ DESIGNATED 266
INCLUDE ~chriz-sod-remix/lib/comp266.tpa~
''', encoding="ascii")
        return self.run_weidu(f"{name}.tp2", "--force-install-list", "266")

    def protected(self):
        return {name: (self.game / name).read_bytes() for name in (
            "chitin.key", "data/csr291.bif", "dialog.tlk", "lang/en_us/dialog.tlk")}

    def assert_rejected(self, target, *, after=NATIVE_AFTER):
        self.fixture(target, after=after)
        before = tree(self.override)
        protected = self.protected()
        result = self.repair()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("expected one original or one complete capped Insane Mislead block", result.stdout + result.stderr)
        self.assertEqual(tree(self.override), before)
        self.assertEqual(self.protected(), protected)
        backups = self.game / "repair-backup/266"
        self.assertFalse(backups.exists() and any(p.suffix.lower() == ".bcs" for p in backups.iterdir()))

    def test_actual_source_shape_changes_only_one_block_and_uninstall_restores(self):
        self.fixture()
        before = tree(self.override)
        original = (self.override / "bdashiru.bcs").read_bytes()
        protected = self.protected()
        self.assert_success(self.repair())
        self.assertEqual((self.override / "bdashiru.bcs").read_bytes(),
                         (self.override / "expected.bcs").read_bytes())
        after = tree(self.override)
        self.assertEqual({name for name in before.keys() | after.keys() if before.get(name) != after.get(name)},
                         {"BDASHIRU.BCS"})
        self.assertEqual(self.protected(), protected)
        # The compiled prefix/suffix are retained byte-for-byte, not merely similar text.
        changed = (self.override / "bdashiru.bcs").read_bytes()
        old_blocks = original.split(b"CR\n")
        new_blocks = changed.split(b"CR\n")
        self.assertEqual(len(old_blocks), len(new_blocks))
        self.assertEqual(sum(a != b for a, b in zip(old_blocks, new_blocks)), 1)
        result = self.run_weidu("repair.tp2", "--force-uninstall-list", "266")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(tree(self.override), before)
        self.assertEqual(self.protected(), protected)

    def test_already_capped_script_is_byte_exact_noop(self):
        self.fixture(CAPPED_MISLEAD)
        before = tree(self.override)
        self.assert_success(self.repair())
        self.assertEqual(tree(self.override), before)

    def test_public_component_selects_the_cap_and_uninstalls_exactly(self):
        self.fixture()
        shutil.copytree(ROOT / "chriz-sod-remix", self.game / "chriz-sod-remix",
                        dirs_exist_ok=True)
        before = tree(self.override)
        public = "chriz-sod-remix/setup-chriz-sod-remix.tp2"
        self.assert_success(self.run_weidu(public, "--force-install-list", "266"))
        self.assertEqual((self.override / "bdashiru.bcs").read_bytes(),
                         (self.override / "expected.bcs").read_bytes())
        result = self.run_weidu(public, "--force-uninstall-list", "266")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(tree(self.override), before)

    def test_captured_native_binary_matches_source_and_accepts_cap(self):
        self.fixture(target_only=True)
        self.assertEqual((self.override / "bdashiru.bcs").read_bytes(), NATIVE_MISLEAD_BCS)
        (self.override / "bdashiru.bcs").write_bytes(NATIVE_MISLEAD_BCS)
        self.assert_success(self.repair())
        self.assertEqual((self.override / "bdashiru.bcs").read_bytes(),
                         (self.override / "expected.bcs").read_bytes())

    def test_second_tail_application_is_byte_exact_noop(self):
        self.fixture()
        self.assert_success(self.repair())
        before = tree(self.override)
        self.assert_success(self.repair("second-tail"))
        self.assertEqual(tree(self.override), before)

    def test_partial_guard_without_consumption_is_rejected(self):
        self.assert_rejected(CAPPED_MISLEAD.replace('    SetGlobal("CSR266_MISLEAD","LOCALS",1)\n', ""))

    def test_partial_consumption_without_guard_is_rejected(self):
        self.assert_rejected(CAPPED_MISLEAD.replace('  Global("CSR266_MISLEAD","LOCALS",0)\n', ""))

    def test_wrong_consumed_flag_value_is_rejected(self):
        self.assert_rejected(CAPPED_MISLEAD.replace('"LOCALS",1)', '"LOCALS",0)'))

    def test_duplicate_and_mixed_blocks_are_rejected(self):
        for target in (NATIVE_MISLEAD * 2, CAPPED_MISLEAD * 2, NATIVE_MISLEAD + CAPPED_MISLEAD):
            with self.subTest(target=target):
                self.assert_rejected(target)

    def test_changed_timer_or_extra_native_action_is_rejected(self):
        for target in (NATIVE_MISLEAD.replace("TWO_ROUNDS", "THREE_ROUNDS"),
                       NATIVE_MISLEAD.replace("    ApplySpell", "    Continue()\n    ApplySpell")):
            with self.subTest(target=target):
                self.assert_rejected(target)

    def test_missing_target_and_empty_compiled_script_are_rejected(self):
        self.assert_rejected("")
        (self.override / "bdashiru.bcs").write_bytes(b"SC\nSC\n")
        before = tree(self.override)
        result = self.repair("empty-script")
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("expected one original or one complete capped", result.stdout + result.stderr)
        self.assertEqual(tree(self.override), before)

    def test_foreign_owned_flag_reference_is_rejected(self):
        foreign = FOREIGN.replace("FOREIGN_BEHAVIOUR", "CSR266_MISLEAD")
        self.assert_rejected(NATIVE_MISLEAD, after=NATIVE_AFTER + foreign)

    def test_missing_resource_fails_without_writes(self):
        before = tree(self.override)
        result = self.repair()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("BDASHIRU.BCS is missing", result.stdout + result.stderr)
        self.assertEqual(tree(self.override), before)


if __name__ == "__main__":
    unittest.main()
