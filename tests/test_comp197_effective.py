"""Public #197 regression and late recovery on copied effective resources.

Set CSR_197_FIXTURE to a read-only capture directory containing current-fixture/
(override, lang/en_us/dialog.tlk, WeiDU.log) and before115/override (the original
#115 backup resources). Source resources stay outside Git. Every install runs
in a new disposable game; no source installation is ever a WeiDU target.
The pre-115 overlay is an isolated ordering fixture, not a historical full game.
"""
import os
from pathlib import Path
import re
import struct
import subprocess
import unittest

from test_bdscry_compat import WEIDU
from test_khalid_continuity_installer import (
    EffectiveKhalidGame, baf_blocks, dialog_states)
from test_comp115_comp197_order import SPAWN_LINE
from test_comp115_comp256_order import assert_victory_routes


CAPTURE = Path(os.environ.get("CSR_197_FIXTURE", "__absent_csr197_fixture__"))
TP2 = "chriz-sod-remix/setup-chriz-sod-remix.tp2"


@unittest.skipUnless(WEIDU.is_file() and (CAPTURE / "current-fixture").is_dir(),
                     "effective capture unavailable; set CSR_197_FIXTURE and WEIDU_EXE")
class EffectiveSkieCompatibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = CAPTURE / "current-fixture"
        cls.resources = {p.name.lower(): p.read_bytes()
                         for p in (source / "override").iterdir() if p.is_file()}
        cls.pre115 = {p.name.lower(): p.read_bytes()
                      for p in (CAPTURE / "before115/override").iterdir() if p.is_file()}
        cls.tlk = (source / "lang/en_us/dialog.tlk").read_bytes()
        cls.log = (source / "WeiDU.log").read_bytes()

    def fixture(self, *, pre115=False):
        resources = dict(self.resources)
        if pre115:
            resources.update(self.pre115)
        game = EffectiveKhalidGame(resources, self.tlk, prerequisite=False)
        self.addCleanup(game.cleanup)
        if pre115:
            # Fabricated prerequisite rows only in this isolated ordering case.
            log = "".join(f"~{TP2.upper()}~ #0 #{n} // fixture prerequisite\n"
                          for n in (110, 150, 185, 210)).encode()
        else:
            log = self.log
        (game.root / "WeiDU.log").write_bytes(log)
        return game

    def install(self, game, component):
        result = subprocess.run([
            str(WEIDU), TP2, "--force-install-list", str(component),
            "--language", "0", "--use-lang", "en_us", "--no-exit-pause",
            "--noautoupdate", "--quick-log"], cwd=game.root, capture_output=True,
            text=True, errors="replace", timeout=90)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("SUCCESSFULLY INSTALLED", result.stdout)

    def remove_only_spawns(self, game, count):
        source = game.decompile("bd2000.bcs")["bd2000.bcs"]
        expected, found = SPAWN_LINE.subn("", source)
        self.assertEqual(found, count)
        self.install(game, 197)
        actual = game.decompile("bd2000.bcs")["bd2000.bcs"]
        self.assertEqual(baf_blocks(actual), baf_blocks(expected))
        return actual

    def test_public_197_without_115(self):
        game = self.fixture(pre115=True)
        self.remove_only_spawns(game, 2)

    def test_public_115_followed_by_public_197(self):
        game = self.fixture(pre115=True)
        self.install(game, 115)
        after = self.remove_only_spawns(game, 4)
        victories = [(g, a) for g, a in baf_blocks(after)
                     if 'createcreature("bdbence",[2425.2660],nw)' in a]
        self.assertEqual(len(victories), 4)
        self.assertEqual(sum(g.startswith('!global("csr_kh_fort","global",1)')
                             for g, _ in victories), 2)
        self.assertEqual(sum(g.startswith('global("csr_kh_fort","global",1)')
                             for g, _ in victories), 2)

    def test_public_197_appends_after_all_later_writers(self):
        game = self.fixture()
        before = game.tree()
        old_scripts = game.decompile("bdbence.bcs", "bd7100.bcs")
        old_dialogue = dialog_states(before["bdbence.dlg"])
        original_rows = [line for line in self.log.decode().splitlines()
                         if line.startswith("~")]
        self.assertEqual(len(original_rows), 369)
        self.assertFalse(any(re.match(rf"~{re.escape(TP2)}~ #0 #197\b", row, re.I)
                             for row in original_rows))
        after_script = self.remove_only_spawns(game, 2)
        assert_victory_routes(self, after_script)
        after = game.tree()
        changed = {name for name in before.keys() | after.keys()
                   if before.get(name) != after.get(name)}
        self.assertEqual(changed, {
            "bd0102.bcs", "bdskie.bcs", "bd2000.bcs", "bdbence.bcs", "bd7100.bcs",
            "bd4000.are", "bdskie.dlg", "bdbence.dlg", "bdnederl.dlg", "bddialog.2da"})

        new_scripts = game.decompile("bdbence.bcs", "bd7100.bcs")
        bence = baf_blocks(new_scripts["bdbence.bcs"])
        old_bence = baf_blocks(old_scripts["bdbence.bcs"])
        # The one prepended legacy block is disabled in #256's pending wrap.
        self.assertIn('!global("csr256_stage","bd2000",3)', bence[0][0])
        self.assertIn('setglobal("csr_bence_ot","locals",1)', bence[0][1])
        # Every older block is unchanged except the intended missing-Skie gate.
        expected_bence = [(('false()' + g) if
                           'global("bd_plot","global",310)' in g and
                           'global("bd_skie_plot","global",0)' in g else g, a)
                          for g, a in old_bence]
        self.assertEqual(bence[1:], expected_bence)
        retry = next(g for g, a in bence
                     if 'setglobaltimer("csr256_bence_try","locals",2)' in a)
        for guard in ('combatcounter(0)', 'range(player1,7)',
                      'isvalidforpartydialogue(player1)'):
            self.assertIn(guard, retry)
        # This captured IDS gives opcode 0x4043 both names; WeiDU prints the
        # last alias. Verify the numeric equivalence before comparing text.
        ids = before["trigger.ids"].decode()
        for alias in ("InParty", "IsValidForPartyDialogue"):
            self.assertRegex(ids, rf"(?im)^0x4043\s+{alias}\(")
        expected_travel = old_scripts["bd7100.bcs"].replace(
            '  InMyArea("bdskie")',
            '  !IsValidForPartyDialogue("bdskie")\n  InMyArea("bdskie")')
        self.assertEqual(baf_blocks(new_scripts["bd7100.bcs"]),
                         baf_blocks(expected_travel))

        # #290's ending edits (including state 65) and all other dialogue
        # states must survive semantically; #197 owns only these four states.
        new_dialogue = dialog_states(after["bdbence.dlg"])
        self.assertEqual(len(old_dialogue), len(new_dialogue))
        for index, (old, new) in enumerate(zip(old_dialogue, new_dialogue)):
            if index not in {25, 32, 33, 39}:
                self.assertEqual(old, new, f"BDBENCE state {index}")
        old_action = old_dialogue[32].transitions[0].action
        self.assertEqual(new_dialogue[32].transitions[0].action, old_action.replace(
            'actionoverride("bdskie",escapeareaobject("crusade_camp_exit"))', ''))
        final_rows = [line for line in (game.root / "WeiDU.log").read_text().splitlines()
                      if line.startswith("~")]
        # --quick-log avoids loading the absent 332 other mod sources in this
        # minimal fixture and strips display comments. Installed identities,
        # languages, component numbers and order must remain exactly intact.
        self.assertEqual(final_rows[:-1],
                         [row.split("//", 1)[0].rstrip() for row in original_rows])
        self.assertRegex(final_rows[-1], r"(?i)^~CHRIZ-SOD-REMIX/SETUP-CHRIZ-SOD-REMIX.TP2~ #0 #197$")
        # Existing TLK entries retain text/sound records; only new strings append.
        final_tlk = (game.root / "lang/en_us/dialog.tlk").read_bytes()
        old_count, old_text = struct.unpack_from("<II", self.tlk, 10)
        new_count, new_text = struct.unpack_from("<II", final_tlk, 10)
        self.assertGreater(new_count, old_count)
        self.assertEqual(final_tlk[18:18 + old_count * 26],
                         self.tlk[18:18 + old_count * 26])
        self.assertEqual(final_tlk[new_text:new_text + len(self.tlk) - old_text],
                         self.tlk[old_text:])


if __name__ == "__main__":
    unittest.main()
