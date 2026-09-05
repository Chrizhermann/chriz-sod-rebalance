#!/usr/bin/env python3
"""Exercise production component 291 with real WeiDU in synthetic game fixtures.

No real game/save is written. Set WEIDU_EXE to a WeiDU binary, or use the local
dev-install executable. A tiny KEY/BIF/TLK and audited IDS signatures are generated
inside TemporaryDirectory; source dialogs/scripts are compiled by WeiDU itself.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
MOD = ROOT / "chriz-sod-remix"
DEFAULT_WEIDU = Path("C:/Games/Baldur's Gate II Enhanced Edition modded - dev eet install/weidu.exe")
WEIDU = Path(os.environ.get("WEIDU_EXE", shutil.which("weidu") or DEFAULT_WEIDU))

OLD_ENDPOINT = '''SetGlobal("CSR_ENDING_USED","GLOBAL",1)
EraseJournalEntry(266908)
StartCutSceneMode()
FadeToColor([1.0],0)
CreateCreatureObject("CSRETBGT",Player1,0,0,0)'''
NEW_ENDPOINT = OLD_ENDPOINT.replace(
    'CreateCreatureObject(', 'EndCutSceneMode()\nSetCutSceneLite(TRUE)\nCreateCreatureObject(')
OLD_GUARD = '''IF
  OR(2)
    !AreaCheck("BD4300")
    !Exists("K#ImportContainer")
THEN
  RESPONSE #100
    DisplayStringNoName(Player1,123)
    FadeFromColor([1.0],0)
    EndCutSceneMode()
    SetGlobal("CSR_ENDING_FAILED","GLOBAL",1)
    DestroySelf()
END
'''
NEW_GUARD = OLD_GUARD.replace('    EndCutSceneMode()', '    SetCutSceneLite(FALSE)\n    EndCutSceneMode()')
FOREIGN_TAIL = '''
IF
  Global("FOREIGN_BEFORE","GLOBAL",0)
THEN
  RESPONSE #100
    SetGlobal("FOREIGN_BEFORE","GLOBAL",1)
    Continue()
END

IF
  True()
THEN
  RESPONSE #100
    SetGlobal("FOREIGN_AFTER","GLOBAL",9)
    DestroySelf()
END
'''
ACTION_IDS = '''IDS V1.0
30 SetGlobal(S:Name*,S:Area*,I:Value*)
36 Continue()
111 DestroySelf()
121 StartCutSceneMode()
122 EndCutSceneMode()
202 FadeToColor(P:Point*,I:Blue*)
203 FadeFromColor(P:Point*,I:Blue*)
227 CreateCreatureObject(S:ResRef*,O:Object*,I:Usage1*,I:Usage2*,I:Usage3*)
262 DisplayStringNoName(O:Object*,I:StrRef*)
263 EraseJournalEntry(I:STRREF*)
338 SetCutSceneLite(I:BOOL*BOOLEAN)
'''
TRIGGER_IDS = '''IDS V1.0
0x400D Exists(O:Object*)
0x400F Global(S:Name*,S:Area*,I:Value*)
0x4023 True()
0x407E AreaCheck(S:ResRef*)
0x4089 OR(I:OrCount*)
'''


def compact(value: str) -> str:
    return re.sub(r"\s+", "", re.sub(r"//[^\n]*", "", value)).upper()


def tree(directory: Path) -> dict[str, str]:
    return {str(path.relative_to(directory)).upper(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in directory.rglob("*") if path.is_file()}


def write_fake_game(directory: Path) -> None:
    """One BIFF resource identifies BG2EE; every tested resource is in override."""
    # Unix WeiDU normalizes paths to lowercase. Use that physical layout for
    # the BIFF, IDS, sources, and override resources on every platform.
    (directory / "data").mkdir()
    payload = b"synthetic BG2EE marker"
    bif = (struct.pack("<4s4sIII", b"BIFF", b"V1  ", 1, 0, 0x14)
           + struct.pack("<IIIHH", 0, 0x24, len(payload), 1010, 0) + payload)
    (directory / "data/csr291.bif").write_bytes(bif)
    name = b"data\\csr291.bif\0"
    key = (struct.pack("<4s4sIIII", b"KEY ", b"V1  ", 1, 1, 0x18, 0x24)
           + struct.pack("<IIHH", len(bif), 0x32, len(name), 1)
           + struct.pack("<8sHI", b"OH6000\0\0", 1010, 0) + name)
    (directory / "chitin.key").write_bytes(key)
    tlk = struct.pack("<8sHII", b"TLK V1  ", 0, 1, 0x2C) + struct.pack("<H8siiII", 0, b"\0" * 8, 0, 0, 0, 0)
    (directory / "lang/en_us").mkdir(parents=True)
    (directory / "dialog.tlk").write_bytes(tlk)
    (directory / "lang/en_us/dialog.tlk").write_bytes(tlk)
    override = directory / "override"
    override.mkdir()
    ids = {"ACTION": ACTION_IDS, "TRIGGER": TRIGGER_IDS,
           "OBJECT": "IDS V1.0\n1 Myself\n21 Player1\n", "BOOLEAN": "IDS V1.0\n0 FALSE\n1 TRUE\n"}
    for name in ("EA", "GENERAL", "RACE", "CLASS", "SPECIFIC", "GENDER", "ALIGN"):
        ids[name] = "IDS V1.0\n0 ANYONE\n"
    for name, value in ids.items():
        (override / f"{name.lower()}.ids").write_text(value, encoding="ascii")


@unittest.skipUnless(WEIDU.is_file(), "real WeiDU unavailable; set WEIDU_EXE")
class Component291InstallerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="csr291-installer-")
        self.addCleanup(self.temp.cleanup)
        self.game = Path(self.temp.name)
        write_fake_game(self.game)
        shutil.copytree(MOD, self.game / "chriz-sod-remix")
        (self.game / "fixture").mkdir()
        (self.game / "fixture/setup-fixture.tp2").write_text('''BACKUP ~fixture/backup~
AUTHOR ~fixture~
BEGIN ~compile synthetic ending fixture~ DESIGNATED 0
COMPILE ~fixture/bddazzo.d~
COMPILE ~fixture/csretbgt.baf~
''', encoding="ascii")
        (self.game / "repair.tp2").write_text('''BACKUP ~repair-backup~
AUTHOR ~fixture~
BEGIN ~production component 291 harness~ DESIGNATED 291
INCLUDE ~chriz-sod-remix/lib/comp291.tpa~
''', encoding="ascii")
        for name in ("K#TELBGT.BCS", "K#TELBGT.CRE", "AR0602.BCS", "BD6100.ARE", "BD6100.BCS", "CSRETBGT.CRE"):
            (self.game / "override" / name.lower()).write_bytes(f"immutable sentinel for {name}".encode("ascii"))

    def run_weidu(self, *arguments: str) -> subprocess.CompletedProcess:
        return subprocess.run([str(WEIDU), *arguments, "--game", str(self.game),
                               "--language", "0", "--use-lang", "en_US", "--no-exit-pause"],
                              cwd=self.game, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=45)

    def fixture(self, endpoint: str = OLD_ENDPOINT, guard: str = OLD_GUARD,
                other_endpoint: str | None = None, extra_transition: bool = False) -> None:
        states = ['BEGIN ~BDDAZZO~']
        for index in range(4):
            action = endpoint if index == 2 else (other_endpoint or endpoint)
            transition = f'IF ~~ THEN DO ~{action}~ EXIT' if index >= 2 else 'IF ~~ THEN EXIT'
            if index == 2 and extra_transition:
                transition += '\nIF ~~ THEN EXIT'
            states.append(f'IF ~True()~ THEN BEGIN {index}\nSAY #0\n{transition}\nEND')
        (self.game / "fixture/bddazzo.d").write_text("\n\n".join(states), encoding="ascii")
        (self.game / "fixture/csretbgt.baf").write_text(guard + FOREIGN_TAIL, encoding="ascii")
        result = self.run_weidu("fixture/setup-fixture.tp2", "--force-install-list", "0")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("SUCCESSFULLY INSTALLED", result.stdout)

    def baseline(self) -> dict[str, object]:
        return {"override": tree(self.game / "override"),
                "protected": {str(path.relative_to(self.game)): path.read_bytes() for path in (
                    self.game / "chitin.key", self.game / "data/csr291.bif", self.game / "dialog.tlk",
                    self.game / "lang/en_us/dialog.tlk")}}

    def repair(self) -> subprocess.CompletedProcess:
        return self.run_weidu("repair.tp2", "--force-install-list", "291")

    def decompile(self, name: str) -> str:
        destination = self.game / "decompiled"
        destination.mkdir(exist_ok=True)
        result = self.run_weidu(str(self.game / "override" / name.lower()), "--out", str(destination),
                                "--log", str(destination / "audit.log"))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        extension = ".d" if name.upper().endswith(".DLG") else ".baf"
        matches = [path for path in destination.iterdir() if path.name.upper() == (Path(name).stem + extension).upper()]
        self.assertEqual(len(matches), 1)
        return matches[0].read_text(encoding="utf-8", errors="replace")

    def assert_protected(self, before: dict, allowed: set[str]) -> None:
        after = tree(self.game / "override")
        self.assertEqual(after.keys(), before["override"].keys())
        for name, digest in before["override"].items():
            if name not in allowed:
                self.assertEqual(after[name], digest, f"unexpected game resource write: {name}")
        for name, value in before["protected"].items():
            self.assertEqual((self.game / name).read_bytes(), value, name)

    def assert_failure_before_writes(self, before: dict, result: subprocess.CompletedProcess) -> None:
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("NOT INSTALLED DUE TO ERRORS", result.stdout)
        self.assertIn("#291", result.stdout + result.stderr)
        self.assert_protected(before, set())
        backups = self.game / "repair-backup/291"
        if backups.exists():
            self.assertFalse(any(path.suffix.upper() in (".DLG", ".BCS", ".CRE", ".ARE") for path in backups.rglob("*")),
                             "resource backup exists: mutation began before the failing preflight")

    def assert_repaired(self) -> None:
        dazzo = compact(self.decompile("BDDAZZO.DLG"))
        carrier = compact(self.decompile("CSRETBGT.BCS"))
        self.assertEqual(dazzo.count(compact(NEW_ENDPOINT)), 2)
        self.assertEqual(carrier, compact(NEW_GUARD + FOREIGN_TAIL))

    def test_legacy_both_routes_and_guard_repaired_without_foreign_resource_changes(self):
        self.fixture()
        before = self.baseline()
        result = self.repair()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("SUCCESSFULLY INSTALLED", result.stdout)
        self.assert_protected(before, {"BDDAZZO.DLG", "CSRETBGT.BCS"})
        self.assert_repaired()

    def test_already_current_is_byte_exact_noop(self):
        self.fixture(NEW_ENDPOINT, NEW_GUARD)
        before = self.baseline()
        result = self.repair()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assert_protected(before, set())
        self.assert_repaired()

    def test_current_guard_and_legacy_dialogue_only_rewrites_dialogue(self):
        self.fixture(OLD_ENDPOINT, NEW_GUARD)
        before = self.baseline()
        result = self.repair()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assert_protected(before, {"BDDAZZO.DLG"})
        self.assert_repaired()

    def test_current_dialogue_and_legacy_guard_only_rewrites_guard(self):
        self.fixture(NEW_ENDPOINT, OLD_GUARD)
        before = self.baseline()
        result = self.repair()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assert_protected(before, {"CSRETBGT.BCS"})
        self.assert_repaired()

    def test_mixed_dazzo_states_fail_before_any_write(self):
        self.fixture(OLD_ENDPOINT, OLD_GUARD, other_endpoint=NEW_ENDPOINT)
        before = self.baseline()
        self.assert_failure_before_writes(before, self.repair())

    def test_malformed_dazzo_action_fails_before_guard_write(self):
        self.fixture(OLD_ENDPOINT.replace('EraseJournalEntry(266908)', 'EraseJournalEntry(266909)'))
        before = self.baseline()
        self.assert_failure_before_writes(before, self.repair())

    def test_extra_dazzo_transition_fails_before_any_write(self):
        self.fixture(extra_transition=True)
        before = self.baseline()
        self.assert_failure_before_writes(before, self.repair())

    def test_malformed_guard_fails_before_dazzo_write(self):
        self.fixture(guard=OLD_GUARD.replace('DestroySelf()', 'Continue()\n    DestroySelf()'))
        before = self.baseline()
        self.assert_failure_before_writes(before, self.repair())

    def test_guard_with_weakened_trigger_fails_before_any_write(self):
        self.fixture(guard=OLD_GUARD.replace('!AreaCheck("BD4300")', 'AreaCheck("BD4300")'))
        before = self.baseline()
        self.assert_failure_before_writes(before, self.repair())

    def test_exact_guard_after_foreign_block_is_not_accepted_as_first_guard(self):
        self.fixture(guard=FOREIGN_TAIL + OLD_GUARD)
        before = self.baseline()
        result = self.repair()
        self.assert_failure_before_writes(before, result)
        self.assertIn("first", (result.stdout + result.stderr).lower())

    def test_missing_eet_anchor_fails_before_any_write(self):
        self.fixture()
        (self.game / "override/k#telbgt.cre").unlink()
        before = self.baseline()
        self.assert_failure_before_writes(before, self.repair())


if __name__ == "__main__":
    unittest.main()
