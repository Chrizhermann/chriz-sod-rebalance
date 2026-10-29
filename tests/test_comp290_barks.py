#!/usr/bin/env python3
"""Run component 290's BD4300 victory-bark check with real WeiDU in synthetic games.

290 sets every victory-bark timer in BD4300 to 2 seconds. Mods add barks of
their own in the vanilla shape (Aura, Sirene), so the check binds the shape of
each block that writes bd_mdd1341a_ot_timer instead of counting blocks. These
fixtures compile independently written scripts, run the same library calls as
290.3 (check only) and 290.4 (check and normalize), and compare the result with
a separately compiled expected script. No game installation is written.
"""

from __future__ import annotations

from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "research/scripts"))
from test_comp291_installer import WEIDU, tree, write_fake_game
from test_gtimes_compat import VANILLA_GTIMES, weidu_append

LIBRARY = ROOT / "chriz-sod-remix/lib/comp290_barks.tpa"
COMP290 = ROOT / "chriz-sod-remix/lib/comp290.tpa"
TP2 = ROOT / "chriz-sod-remix/setup-chriz-sod-remix.tp2"
TIMER = '"bd_mdd1341a_ot_timer","bd4300"'


def block(triggers: list[str], actions: list[str], responses: int = 1) -> str:
    response = "".join(f"    {line}\n" for line in actions)
    body = "".join(f"  RESPONSE #{100 // responses}\n{response}" for _ in range(responses))
    return "IF\n" + "".join(f"  {line}\n" for line in triggers) + "THEN\n" + body + "END\n"


def bark(flag: str, presence: list[str], npc: str, time: str, strref: int,
         extra: list[str] | None = None) -> str:
    """A victory bark in the shape of BD4300's own, plus optional own actions."""
    return block(
        ['Global("bd_plot","global",586)',
         f'!GlobalTimerNotExpired({TIMER})',
         f'Global("bd_ot2_{flag}","bd4300",0)', *presence],
        [f'SetGlobalTimer({TIMER},{time})',
         f'SetGlobal("bd_ot2_{flag}","bd4300",1)',
         f'DisplayStringHead("{npc}",{strref})', *(extra or [])])


def party(npc: str) -> list[str]:
    return [f'IsValidForPartyDialogue("{npc}")']


# The 17 barks of BD4300 after the Avernus victory: flag suffix, presence, speaker
# and timer as the game writes them (numbers and GTIMES names).
VANILLA_BARKS = [
    ("Corwin", party("CORWIN"), "CORWIN", "2"),
    ("Voghil", party("VOGHILN"), "VOGHILN", "3"),
    ("Viconi", party("VICONIA"), "VICONIA", "4"),
    ("Rasaad", party("RASAAD"), "RASAAD", "4"),
    ("Edwin", party("EDWIN"), "EDWIN", "ONE_MINUTE"),
    ("Minsc", party("MINSC"), "MINSC", "2"),
    ("Dynahe", party("DYNAHEIR"), "DYNAHEIR", "3"),
    ("Dorn", party("DORN"), "DORN", "7"),
    ("Neera", party("NEERA"), "NEERA", "2"),
    ("Safana", party("SAFANA"), "SAFANA", "ONE_ROUND"),
    ("Glint", party("GLINT"), "GLINT", "ONE_ROUND"),
    ("Baelot", party("BAELOTH"), "BAELOTH", "ONE_MINUTE"),
    ("MKhiin", party("MKHIIN"), "MKHIIN", "3"),
    ("Jaheir", party("JAHEIRA"), "JAHEIRA", "ONE_MINUTE"),
    ("Khalid", party("KHALID"), "KHALID", "4"),
    ("darnas", ['InMyArea("bddarnas")', '!Dead("bddarnas")'], "bddarnas", "7"),
    ("aun", ['InMyArea("bdaun")'], "bdaun", "7"),
]


def vanilla_barks() -> list[str]:
    return [bark(flag, presence, npc, time, 10 + index)
            for index, (flag, presence, npc, time) in enumerate(VANILLA_BARKS)]


CONVERGENCE = block(['Global("bd_plot","global",586)', f'GlobalTimerExpired({TIMER})'],
                    ['SetGlobal("bd_plot","global",587)'])
AURA = bark("C0Aura", party("C0Aura"), "C0Aura", "3", 40)
# Sirene BG1 adds a mid-fight remark on another variable and its victory bark
# (InParty compiles to the trigger that decompiles as IsValidForPartyDialogue).
SIRENE = [
    block(['Global("bd_mdd1290d_ot","bd4300",1)',
           'Global("bd_mdd1290d_ot_C0Sirene","bd4300",0)', 'InParty("C0Sirene")'],
          ['DisplayStringHead("C0Sirene",41)', 'SetGlobal("bd_mdd1290d_ot","bd4300",2)',
           'SetGlobal("bd_mdd1290d_ot_C0Sirene","bd4300",1)']),
    bark("C0Sirene", ['InParty("C0Sirene")'], "C0Sirene", "4", 42),
]
FOREIGN = [block([f'Global("FOREIGN_{name}","GLOBAL",0)'],
                 [f'SetGlobal("FOREIGN_{name}","GLOBAL",1)', 'Continue()'])
           for name in ("BEFORE", "MIDDLE", "AFTER")]


def script(barks: list[str], *, top: list[str] | None = None,
           bottom: list[str] | None = None) -> list[str]:
    """BD4300 in game order: mod blocks on top, vanilla barks, convergence, appends."""
    middle = barks[:len(barks) // 2] + [FOREIGN[1]] + barks[len(barks) // 2:]
    return [*(top or []), FOREIGN[0], *middle, CONVERGENCE, *(bottom or []), FOREIGN[2]]


def normalized(text: str) -> str:
    return re.sub(r'(SetGlobalTimer\("bd_mdd1341a_ot_timer","bd4300",)[^)]*\)', r"\g<1>2)",
                  text, flags=re.I)


@unittest.skipUnless(WEIDU.is_file(), "real WeiDU unavailable; set WEIDU_EXE")
class Component290VictoryBarkTests(unittest.TestCase):
    def setUp(self) -> None:
        self.make_game()

    def make_game(self, gtimes: str = VANILLA_GTIMES) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="csr290-barks-")
        self.addCleanup(self.temp.cleanup)
        self.game = Path(self.temp.name)
        write_fake_game(self.game)
        self.override = self.game / "override"
        extra_ids = {
            "action": "109 IncrementGlobal(S:Name*,S:Area*,I:Value*)\n"
                      "115 SetGlobalTimer(S:Name*,S:Area*,I:Time*GTimes)\n"
                      "268 RealSetGlobalTimer(S:Name*,S:Area*,I:Time*GTimes)\n"
                      "269 DisplayStringHead(O:Object*,I:StrRef*)\n",
            # EET's TRIGGER.IDS gives InParty and IsValidForPartyDialogue one id.
            "trigger": "0x4040 GlobalTimerExpired(S:Name*,S:Area*)\n"
                       "0x4041 GlobalTimerNotExpired(S:Name*,S:Area*)\n"
                       "0x4043 InParty(O:Object*)\n"
                       "0x4043 IsValidForPartyDialogue(O:Object*)\n"
                       "0x4051 Dead(S:Name*)\n"
                       "0x40CB InMyArea(O:Object*)\n",
        }
        for name, definitions in extra_ids.items():
            path = self.override / f"{name}.ids"
            path.write_text(path.read_text(encoding="ascii") + definitions, encoding="ascii")
        (self.override / "gtimes.ids").write_bytes(gtimes.encode("ascii"))
        # Real TLK text includes punctuation that resembles code.
        text = b"Fixture text: (magic) [sound] <CHARNAME>, 100%!"
        count = 64
        records = b"".join(struct.pack("<H8siiII", 1, b"\0" * 8, 0, 0, index * len(text),
                                       len(text)) for index in range(count))
        tlk = struct.pack("<8sHII", b"TLK V1  ", 0, count, 18 + count * 26) + records + text * count
        for path in (self.game / "dialog.tlk", self.game / "lang/en_us/dialog.tlk"):
            path.write_bytes(tlk)
        (self.game / "chriz-sod-remix/lib").mkdir(parents=True)
        shutil.copy2(LIBRARY, self.game / "chriz-sod-remix/lib/comp290_barks.tpa")
        (self.game / "fixture").mkdir()
        (self.game / "fixture/setup-fixture.tp2").write_text('''BACKUP ~fixture/backup~
AUTHOR ~fixture~
BEGIN ~compile synthetic BD4300~ DESIGNATED 0
COMPILE ~fixture/bd4300.baf~
COMPILE ~fixture/expected.baf~
''', encoding="ascii")
        # The same calls as 290.3 (read-only preflight) and 290.4 (normalization).
        (self.game / "patch.tp2").write_text('''BACKUP ~patch-backup~
AUTHOR ~fixture~
BEGIN ~component 290 victory barks~ DESIGNATED 290
INCLUDE ~chriz-sod-remix/lib/comp290_barks.tpa~
COPY_EXISTING - ~BD4300.BCS~ ~override~
  DECOMPILE_AND_PATCH BEGIN
    LAUNCH_PATCH_FUNCTION csr290_victory_barks
      INT_VAR csr290_normalize = 0
      RET csr290_bark_count
    END
  END
PRINT ~preflight barks: %csr290_bark_count%~
COPY_EXISTING ~BD4300.BCS~ ~override~
  DECOMPILE_AND_PATCH BEGIN
    LAUNCH_PATCH_FUNCTION csr290_victory_barks
      INT_VAR csr290_normalize = 1
      RET csr290_bark_count
    END
  END
BUT_ONLY
PRINT ~normalized barks: %csr290_bark_count%~
''', encoding="ascii")

    def run_weidu(self, *arguments: str) -> subprocess.CompletedProcess:
        return subprocess.run([str(WEIDU), *arguments, "--game", str(self.game),
                               "--language", "0", "--use-lang", "en_US", "--no-exit-pause"],
                              cwd=self.game, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=60)

    def fixture(self, blocks: list[str], expected: list[str] | None = None) -> None:
        original = "\n".join(blocks)
        target = normalized(original) if expected is None else "\n".join(expected)
        (self.game / "fixture/bd4300.baf").write_text(original, encoding="ascii")
        (self.game / "fixture/expected.baf").write_text(target, encoding="ascii")
        result = self.run_weidu("fixture/setup-fixture.tp2", "--force-install-list", "0")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("SUCCESSFULLY INSTALLED", result.stdout)

    def snapshot(self) -> dict:
        return {"override": tree(self.override), "immutable": {
            name: (self.game / name).read_bytes() for name in
            ("chitin.key", "data/csr291.bif", "dialog.tlk", "lang/en_us/dialog.tlk")}}

    def assert_preserved(self, before: dict, changed: bool) -> None:
        after = tree(self.override)
        self.assertEqual(after.keys(), before["override"].keys())
        for name, digest in before["override"].items():
            if changed and name == "BD4300.BCS":
                continue
            self.assertEqual(after[name], digest, name)
        for name, data in before["immutable"].items():
            self.assertEqual((self.game / name).read_bytes(), data, name)

    def install(self, name: str = "patch.tp2") -> subprocess.CompletedProcess:
        return self.run_weidu(name, "--force-install-list", "290")

    def assert_normalized(self, barks: int, *, changed: bool = True) -> None:
        before = self.snapshot()
        result = self.install()
        output = result.stdout + result.stderr
        self.assertEqual(result.returncode, 0, output)
        self.assertIn("SUCCESSFULLY INSTALLED", result.stdout)
        self.assertIn(f"preflight barks: {barks}", output)
        self.assertIn(f"normalized barks: {barks}", output)
        self.assert_preserved(before, changed)
        # Every bark timer is 2 and every other byte of every block, foreign and
        # mod-added ones included, is what the separately compiled script has.
        self.assertEqual((self.override / "bd4300.bcs").read_bytes(),
                         (self.override / "expected.bcs").read_bytes())

    def assert_rejected(self, *messages: str) -> None:
        before = self.snapshot()
        result = self.install()
        output = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0, output)
        self.assertIn("NOT INSTALLED DUE TO ERRORS", result.stdout)
        self.assertIn("chriz-sod-remix #290 [BD4300 victory barks]", output)
        for message in messages:
            self.assertIn(message, output)
        self.assertNotIn("preflight barks:", output)
        self.assert_preserved(before, False)
        backups = self.game / "patch-backup/290"
        self.assertFalse(backups.exists() and any(path.suffix.upper() == ".BCS"
                                                  for path in backups.rglob("*")),
                         "the preflight failure must precede any resource backup")

    # --- installs ---------------------------------------------------------

    def test_vanilla_seventeen_barks_are_normalized_byte_exact(self):
        self.fixture(script(vanilla_barks()))
        self.assert_normalized(17)

    def test_aura_bark_is_an_ordinary_bark(self):
        self.fixture(script(vanilla_barks(), bottom=[AURA]))
        self.assert_normalized(18)

    def test_sirene_bark_keeps_her_own_blocks_and_actions(self):
        # Her bark gets two more actions of its own; only the timer may change.
        own = SIRENE[1].replace('    DisplayStringHead("C0Sirene",42)\n',
                                '    DisplayStringHead("C0Sirene",42)\n'
                                '    SetGlobal("C0SireneVictory","GLOBAL",1)\n    Continue()\n')
        self.fixture(script(vanilla_barks(), top=[SIRENE[0], own]))
        self.assert_normalized(18)

    def test_aura_and_sirene_together(self):
        self.fixture(script(vanilla_barks(), top=SIRENE, bottom=[AURA]))
        self.assert_normalized(19)

    def test_one_vanilla_bark_removed_still_installs(self):
        barks = vanilla_barks()
        del barks[4]
        self.fixture(script(barks, top=SIRENE))
        self.assert_normalized(17)

    def test_a_single_bark_is_enough(self):
        self.fixture(script(vanilla_barks()[:1]))
        self.assert_normalized(1)

    def test_names_and_scopes_match_regardless_of_case(self):
        upper = bark("C0LOUD", party("C0LOUD"), "C0LOUD", "5", 43).replace(
            '"bd_plot","global"', '"BD_PLOT","GLOBAL"').replace(
            "bd_mdd1341a_ot_timer", "BD_MDD1341A_OT_TIMER").replace(
            '"bd4300"', '"BD4300"').replace("bd_ot2_C0LOUD", "BD_OT2_c0loud")
        self.fixture(script(vanilla_barks(), bottom=[upper]))
        self.assert_normalized(18)

    def test_presence_in_an_or_group_is_allowed(self):
        either = bark("C0Pair", ["OR(2)", '  IsValidForPartyDialogue("C0One")',
                                 '  IsValidForPartyDialogue("C0Two")'], "C0One", "3", 44)
        self.fixture(script(vanilla_barks(), bottom=[either]))
        self.assert_normalized(18)

    def test_timer_readers_elsewhere_are_left_alone(self):
        reader = block(['Global("bd_plot","global",587)', f'GlobalTimerExpired({TIMER})',
                        'Global("FOREIGN_READER","GLOBAL",0)'],
                       ['SetGlobal("FOREIGN_READER","GLOBAL",1)'])
        self.fixture(script(vanilla_barks(), bottom=[reader]))
        self.assert_normalized(17)

    def test_already_normalized_script_is_kept_byte_exact(self):
        self.fixture([normalized(text) for text in script(vanilla_barks(), top=SIRENE)])
        self.assert_normalized(18)

    def test_timer_names_from_other_gtimes_files(self):
        # A mod may name 5 seconds differently or give a timer a dotted name,
        # which WeiDU prints in five quotes; the timer value is replaced whole.
        variants = {
            "another mod's name for 5 seconds": weidu_append(VANILLA_GTIMES, "5 MOD_ONE_MINUTE"),
            "dotted name for 7 seconds": weidu_append(VANILLA_GTIMES, "7 SEVEN.SECONDS"),
        }
        for label, gtimes in variants.items():
            with self.subTest(gtimes=label):
                self.make_game(gtimes)
                self.fixture(script(vanilla_barks(), top=SIRENE))
                self.assert_normalized(18)

    # --- refusals, all before anything is written ------------------------

    def test_stray_setter_outside_a_bark_is_rejected(self):
        stray = block(['Global("FOREIGN_STRAY","GLOBAL",0)'],
                      [f'SetGlobalTimer({TIMER},60)', 'SetGlobal("FOREIGN_STRAY","GLOBAL",1)'])
        self.fixture(script(vanilla_barks(), bottom=[stray]))
        self.assert_rejected('(first trigger Global("FOREIGN_STRAY","GLOBAL",0))',
                             'without a Global("bd_plot","global",586) trigger')

    def test_bark_with_two_setters_is_rejected(self):
        double = SIRENE[1].replace(f'    SetGlobalTimer({TIMER},4)\n',
                                   f'    SetGlobalTimer({TIMER},4)\n'
                                   f'    SetGlobalTimer({TIMER},30)\n')
        self.fixture(script(vanilla_barks(), top=[SIRENE[0], double]))
        self.assert_rejected("block 2 (bd_ot2_C0Sirene) has 2 bd_mdd1341a_ot_timer setters")

    def test_script_without_any_bark_is_rejected(self):
        self.fixture(script([]))
        self.assert_rejected("no victory bark sets bd_mdd1341a_ot_timer")

    def test_other_timer_writer_is_rejected(self):
        real = SIRENE[1].replace("SetGlobalTimer(", "RealSetGlobalTimer(")
        self.fixture(script(vanilla_barks(), top=[SIRENE[0], real]))
        self.assert_rejected("block 2 (bd_ot2_C0Sirene) names bd_mdd1341a_ot_timer in 1 action(s), "
                             "0 of them SetGlobalTimer")

    def test_timer_written_with_setglobal_is_rejected(self):
        extra = block(['Global("bd_plot","global",586)', 'Global("FOREIGN_RESET","GLOBAL",0)'],
                      [f'SetGlobal({TIMER},0)', 'SetGlobal("FOREIGN_RESET","GLOBAL",1)'])
        self.fixture(script(vanilla_barks(), bottom=[extra]))
        self.assert_rejected("names bd_mdd1341a_ot_timer in 1 action(s), 0 of them SetGlobalTimer")

    def test_gating_trigger_inside_an_or_group_is_rejected(self):
        loose = block(['OR(2)', '  Global("bd_plot","global",586)', '  True()',
                       f'!GlobalTimerNotExpired({TIMER})', 'Global("bd_ot2_C0Loose","bd4300",0)'],
                      [f'SetGlobalTimer({TIMER},3)', 'SetGlobal("bd_ot2_C0Loose","bd4300",1)'])
        self.fixture(script(vanilla_barks(), bottom=[loose]))
        self.assert_rejected("(bd_ot2_C0Loose) sets bd_mdd1341a_ot_timer without a "
                             'Global("bd_plot","global",586) trigger outside OR groups')

    def test_bark_without_the_timer_wait_is_rejected(self):
        eager = SIRENE[1].replace(f'  !GlobalTimerNotExpired({TIMER})\n', "")
        self.fixture(script(vanilla_barks(), top=[eager]))
        self.assert_rejected("(bd_ot2_C0Sirene) sets bd_mdd1341a_ot_timer without a "
                             f'!GlobalTimerNotExpired({TIMER}) trigger')

    def test_bark_that_never_sets_its_flag_is_rejected(self):
        endless = SIRENE[1].replace('    SetGlobal("bd_ot2_C0Sirene","bd4300",1)\n', "")
        self.fixture(script(vanilla_barks(), top=[endless]))
        self.assert_rejected("never sets bd_ot2_C0Sirene to 1")

    def test_bark_that_sets_another_flag_is_rejected(self):
        crossed = SIRENE[1].replace('SetGlobal("bd_ot2_C0Sirene"', 'SetGlobal("bd_ot2_C0Other"')
        self.fixture(script(vanilla_barks(), top=[crossed]))
        self.assert_rejected("never sets bd_ot2_C0Sirene to 1")

    def test_bark_with_two_flags_is_rejected(self):
        two = SIRENE[1].replace('  Global("bd_ot2_C0Sirene","bd4300",0)\n',
                                '  Global("bd_ot2_C0Sirene","bd4300",0)\n'
                                '  Global("bd_ot2_C0Twin","bd4300",0)\n')
        self.fixture(script(vanilla_barks(), top=[two]))
        self.assert_rejected('with 2 one-shot Global("bd_ot2_<name>","bd4300",0) triggers')

    def test_bark_with_a_setter_in_each_of_two_responses_is_rejected(self):
        split = block(['Global("bd_plot","global",586)', f'!GlobalTimerNotExpired({TIMER})',
                       'Global("bd_ot2_C0Split","bd4300",0)'],
                      [f'SetGlobalTimer({TIMER},3)', 'SetGlobal("bd_ot2_C0Split","bd4300",1)'],
                      responses=2)
        self.fixture(script(vanilla_barks(), bottom=[split]))
        self.assert_rejected("(bd_ot2_C0Split) has 2 bd_mdd1341a_ot_timer setters")

    def test_bark_with_one_setter_in_two_responses_is_rejected(self):
        split = block(['Global("bd_plot","global",586)', f'!GlobalTimerNotExpired({TIMER})',
                       'Global("bd_ot2_C0Split","bd4300",0)'],
                      ['SetGlobal("bd_ot2_C0Split","bd4300",1)'], responses=2)
        split = split.replace('  RESPONSE #50\n    SetGlobal',
                              f'  RESPONSE #50\n    SetGlobalTimer({TIMER},3)\n    SetGlobal', 1)
        self.fixture(script(vanilla_barks(), bottom=[split]))
        self.assert_rejected("(bd_ot2_C0Split) sets bd_mdd1341a_ot_timer in a block with 2 responses")


class Component290WiringTests(unittest.TestCase):
    """290.3 and 290.4 call the library; no fixed bark count remains."""

    def test_preflight_and_mutation_both_use_the_bark_check(self):
        source = COMP290.read_text(encoding="utf-8")
        calls = re.findall(r"LAUNCH_PATCH_FUNCTION csr290_victory_barks\s+INT_VAR "
                           r"csr290_normalize = ([01])", source)
        self.assertEqual(calls, ["0", "1"])
        preflight = source.index("290.3")
        mutation = source.index("290.4")
        first, second = (match.start() for match in re.finditer(
            r"LAUNCH_PATCH_FUNCTION csr290_victory_barks", source))
        self.assertTrue(preflight < first < mutation < second)
        self.assertRegex(source[source.rfind("COPY_EXISTING", 0, first):first],
                         r"COPY_EXISTING - ~BD4300\.BCS~")
        self.assertRegex(source[source.rfind("COPY_EXISTING", 0, second):second],
                         r"COPY_EXISTING ~BD4300\.BCS~")
        self.assertNotIn("C0Aura", source)
        self.assertNotRegex(source, r"\b1[78]\s*\+|=\s*1[78]\b")

    def test_tp2_loads_the_library_before_component_290(self):
        lines = [line.strip() for line in TP2.read_text(encoding="utf-8").splitlines()]
        library = lines.index("INCLUDE ~chriz-sod-remix/lib/comp290_barks.tpa~")
        self.assertEqual(lines[library + 1], "INCLUDE ~chriz-sod-remix/lib/comp290.tpa~")
        begin = max(index for index, line in enumerate(lines[:library])
                    if line.startswith("BEGIN "))
        self.assertIn("DESIGNATED 290 ", lines[begin])


if __name__ == "__main__":
    unittest.main()
