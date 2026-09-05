"""WeiDU integration tests for the current native BDSCRY picker patch.

The fixtures are source-only synthetic dialogs.  A locally supplied WeiDU 249
compiles them in a temporary fake game, then exercises the production helper.
No game-owned dialog binary is stored in this repository.
"""

from __future__ import annotations

import importlib.util
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WEIDU = Path(
    os.environ.get("WEIDU_EXE")
    or shutil.which("weidu")
    or r"C:\src\private\chriz-bg-rebalance\weidu.exe"
)
HELPER = ROOT / "chriz-sod-remix/lib/bdscry_compat.tpa"
SETUP = ROOT / "chriz-sod-remix/setup-chriz-sod-remix.tp2"
HOOD_SOURCE = ROOT / "chriz-sod-remix/dlg/csrhood.d"
OMEN_SOURCE = ROOT / "chriz-sod-remix/lib/comp225.tpa"
COMP220_LISTS = ROOT / "chriz-sod-remix/lib/comp220_lists.tpa"
VERIFIER_SOURCE = ROOT / "research/scripts/verify_scrying_pool.py"

ONE_EMPTY_STRING_TLK = (
    struct.pack("<8sHII", b"TLK V1  ", 0, 1, 0x2C)
    + struct.pack("<H8siiII", 0, b"\0" * 8, 0, 0, 0, 0)
)

ROUTES = {
    "bd_sddd12_imoen": (1, "bdscry01"),
    "bd_sddd12_caelar": (2, "bdscry03"),
    "bd_sddd12_hood": (3, "bdscry05"),
}


def _load_verifier():
    spec = importlib.util.spec_from_file_location("verify_scrying_pool", VERIFIER_SOURCE)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load {VERIFIER_SOURCE}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _write_key_and_bif(game_root: Path) -> None:
    """Write a minimal BG2EE-shaped KEY/BIFF with one marker resource."""
    payload = b"synthetic BG2EE marker"
    bif_relative = Path("data/bdsctest.bif")
    bif_path = game_root / bif_relative
    bif_path.parent.mkdir(parents=True)
    table_offset = 0x14
    payload_offset = table_offset + 0x10
    bif_path.write_bytes(
        struct.pack("<4s4sIII", b"BIFF", b"V1  ", 1, 0, table_offset)
        + struct.pack("<IIIHH", 0, payload_offset, len(payload), 1010, 0)
        + payload
    )

    encoded_name = (str(bif_relative).replace("/", "\\") + "\0").encode("ascii")
    bif_table_offset = 0x18
    resource_table_offset = bif_table_offset + 0x0C
    names_offset = resource_table_offset + 0x0E
    (game_root / "chitin.key").write_bytes(
        struct.pack(
            "<4s4sIIII",
            b"KEY ",
            b"V1  ",
            1,
            1,
            bif_table_offset,
            resource_table_offset,
        )
        + struct.pack(
            "<IIHH", bif_path.stat().st_size, names_offset, len(encoded_name), 0
        )
        + struct.pack("<8sHI", b"OH6000\0\0", 1010, 0)
        + encoded_name
    )


def _choice(flag: str, destination: int) -> str:
    return (
        f'  IF ~Global("{flag}","LOCALS",0)~ '
        f"THEN REPLY #0 GOTO {destination}\n"
    )


def _destination(label: int, flag: str, script: str) -> str:
    return f'''IF ~~ THEN BEGIN {label}
  SAY #0
  IF ~~ THEN DO ~SetGlobal("{flag}","LOCALS",1)
StartCutSceneMode()
StartCutSceneEx("{script}",FALSE)~ EXIT
END

'''


def _dialog_source(
    *,
    extra_hood_choice: bool = False,
    omit_hood_choice: bool = False,
) -> str:
    lines = ["BEGIN ~BDSCRY~\n\n", "IF ~~ THEN BEGIN 0\n", "  SAY #0\n"]
    for flag, (destination, _) in ROUTES.items():
        if flag == "bd_sddd12_hood" and omit_hood_choice:
            continue
        lines.append(_choice(flag, destination))
    if extra_hood_choice:
        lines.append(_choice("bd_sddd12_hood", 3))
    lines.extend(("  IF ~~ THEN REPLY #0 EXIT\n", "END\n\n"))
    for flag, (destination, script) in ROUTES.items():
        lines.append(_destination(destination, flag, script))

    return "".join(lines)


def _bdimoen_source() -> str:
    """Build the inspected state-67 three-reply shape with stable numeric indices."""
    lines = ["BEGIN ~BDIMOEN~\n\n"]
    for state in range(67):
        lines.append(
            f"IF ~~ THEN BEGIN {state}\n"
            "  SAY #0\n"
            "  IF ~~ THEN EXIT\n"
            "END\n\n"
        )
    lines.append(
        'IF ~Global("BD_MDD007","BD0103",1)~ THEN BEGIN 67\n'
        "  SAY #0\n"
        '  IF ~~ THEN REPLY #0 DO ~SetGlobal("BD_MDD007","BD0103",2)~ GOTO 74\n'
        '  IF ~~ THEN REPLY #0 DO ~SetGlobal("BD_MDD007","BD0103",2)~ GOTO 68\n'
        '  IF ~~ THEN REPLY #0 DO ~SetGlobal("BD_MDD007","BD0103",2)~ GOTO 76\n'
        "END\n\n"
    )
    for state in range(68, 77):
        lines.append(
            f"IF ~~ THEN BEGIN {state}\n"
            "  SAY #0\n"
            "  IF ~~ THEN EXIT\n"
            "END\n\n"
        )
    return "".join(lines)


class SyntheticDialogGame:
    def __init__(self, source: str):
        self.temporary = tempfile.TemporaryDirectory(prefix="csr-bdscry-compat-")
        self.root = Path(self.temporary.name) / "game"
        self.root.mkdir()
        (self.root / "override").mkdir()
        (self.root / "override/trigger.ids").write_text(
            "IDS V1.0\n"
            "0x400F Global(S:Name*,S:Area*,I:Value*)\n"
            "0x4023 True()\n"
            "0x4030 False()\n",
            encoding="ascii",
            newline="\n",
        )
        (self.root / "override/action.ids").write_text(
            "IDS V1.0\n"
            "30 SetGlobal(S:Name*,S:Area*,I:Value*)\n"
            "120 StartCutSceneEx(S:CutScene*,I:evaluateConditions*BOOLEAN)\n"
            "121 StartCutSceneMode()\n",
            encoding="ascii",
            newline="\n",
        )
        (self.root / "override/boolean.ids").write_text(
            "IDS V1.0\n0 FALSE\n1 TRUE\n",
            encoding="ascii",
            newline="\n",
        )
        _write_key_and_bif(self.root)
        self.tlks = (
            self.root / "dialog.tlk",
            # WeiDU 249 detects EE layouts through this lowercase path on Linux.
            self.root / "lang/en_us/dialog.tlk",
        )
        for tlk in self.tlks:
            tlk.parent.mkdir(parents=True, exist_ok=True)
            tlk.write_bytes(ONE_EMPTY_STRING_TLK)

        fixture = self.root / "fixture"
        fixture.mkdir()
        (fixture / "bdscry.d").write_text(source, encoding="ascii", newline="\n")
        (fixture / "bdimoen.d").write_text(
            _bdimoen_source(), encoding="ascii", newline="\n"
        )
        bootstrap = self.root / "setup-bdscry-bootstrap.tp2"
        bootstrap.write_text(
            "BACKUP ~weidu_external/backup/bdscry-bootstrap~\n"
            "AUTHOR ~test~\n"
            "BEGIN ~compile synthetic BDSCRY~\n"
            "COMPILE ~fixture/bdscry.d~\n"
            "COMPILE ~fixture/bdimoen.d~\n",
            encoding="ascii",
            newline="\n",
        )
        result = self._run(bootstrap)
        if "SUCCESSFULLY INSTALLED" not in self.transcript(result):
            self.cleanup()
            raise AssertionError(self.transcript(result))
        self.pre_patch_tlks = tuple(tlk.read_bytes() for tlk in self.tlks)

        shutil.copytree(ROOT / "chriz-sod-remix", self.root / "chriz-sod-remix")

    def cleanup(self) -> None:
        self.temporary.cleanup()

    def _run(self, setup: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                str(WEIDU),
                str(setup),
                "--game",
                str(self.root),
                "--force-install-list",
                "0",
                "--language",
                "0",
                "--use-lang",
                "en_us",
                "--no-exit-pause",
                "--quick-log",
            ],
            cwd=self.root,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )

    @staticmethod
    def transcript(result: subprocess.CompletedProcess[str]) -> str:
        return f"{result.stdout}\n{result.stderr}".strip()

    def install_patch(self, *flags: str) -> subprocess.CompletedProcess[str]:
        calls = "\n".join(
            "LAF csr_disable_bdscry_picker_route STR_VAR "
            f"csr_scry_flag = ~{flag}~ csr_scry_component = ~test~ END"
            for flag in flags
        )
        setup = self.root / "setup-bdscry-patch.tp2"
        setup.write_text(
            "BACKUP ~weidu_external/backup/bdscry-patch~\n"
            "AUTHOR ~test~\n"
            "ALWAYS\n"
            "  INCLUDE ~chriz-sod-remix/lib/bdscry_compat.tpa~\n"
            "END\n"
            "BEGIN ~patch synthetic BDSCRY~\n"
            f"{calls}\n",
            encoding="ascii",
            newline="\n",
        )
        return self._run(setup)

    def install_component_120_dialog_patch(self) -> subprocess.CompletedProcess[str]:
        setup = self.root / "setup-component-120-dialog.tp2"
        setup.write_text(
            "BACKUP ~weidu_external/backup/component-120-dialog~\n"
            "AUTHOR ~test~\n"
            "ALWAYS\n"
            "  INCLUDE ~chriz-sod-remix/lib/bdscry_compat.tpa~\n"
            "END\n"
            "BEGIN ~install component 120 dialog patch~\n"
            "LAF csr_disable_bdscry_picker_route STR_VAR "
            "csr_scry_flag = ~bd_sddd12_hood~ csr_scry_component = ~120~ END\n"
            "COMPILE ~chriz-sod-remix/dlg/csrhood.d~\n",
            encoding="ascii",
            newline="\n",
        )
        return self._run(setup)

    def tlks_unchanged(self) -> bool:
        return tuple(tlk.read_bytes() for tlk in self.tlks) == self.pre_patch_tlks

    @staticmethod
    def _find_output(directory: Path, filename: str) -> Path:
        matches = [
            path for path in directory.iterdir()
            if path.name.casefold() == filename.casefold() and path.is_file()
        ]
        if len(matches) != 1:
            raise AssertionError(f"expected exactly one {filename} in {directory}: {matches}")
        return matches[0]

    def dialog_path(self, resource: str = "BDSCRY") -> Path:
        return self._find_output(self.root / "override", f"{resource}.dlg")

    def decompile(self, resource: str = "BDSCRY") -> str:
        output = Path(self.temporary.name) / "decompiled"
        output.mkdir(exist_ok=True)
        result = subprocess.run(
            [
                str(WEIDU),
                str(self.dialog_path(resource)),
                "--game",
                str(self.root),
                "--out",
                str(output),
                "--no-exit-pause",
            ],
            cwd=output,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        if result.returncode:
            raise AssertionError(self.transcript(result))
        return self._find_output(output, f"{resource}.d").read_text(encoding="utf-8")


@unittest.skipUnless(WEIDU.is_file(), f"WeiDU 249 fixture input not found: {WEIDU}")
class BdscryNativeLayoutTests(unittest.TestCase):
    def _game(self, source: str) -> SyntheticDialogGame:
        game = SyntheticDialogGame(source)
        self.addCleanup(game.cleanup)
        return game

    def assert_false_gated(self, dialog: str, flag: str, count: int) -> None:
        matches = re.findall(
            rf'False\s*\(\s*\)\s+Global\s*\(\s*"{re.escape(flag)}"\s*,'
            r'\s*"LOCALS"\s*,\s*0\s*\)',
            dialog,
            re.IGNORECASE,
        )
        self.assertEqual(len(matches), count, dialog)

    def test_no_aura_four_state_picker_supports_component_120_then_225(self) -> None:
        game = self._game(_dialog_source())
        result = game.install_patch(*ROUTES)
        transcript = game.transcript(result)
        self.assertIn("SUCCESSFULLY INSTALLED", transcript, transcript)
        dialog = game.decompile()
        for flag in ROUTES:
            self.assert_false_gated(dialog, flag, 1)
        self.assertNotRegex(dialog, r"THEN BEGIN 4\b")
        self.assertTrue(game.tlks_unchanged(), "semantic gating must stay TLK-neutral")

    def test_component_120_gates_the_inspected_bdimoen_reply(self) -> None:
        game = self._game(_dialog_source())
        result = game.install_component_120_dialog_patch()
        transcript = game.transcript(result)
        self.assertIn("SUCCESSFULLY INSTALLED", transcript, transcript)

        verifier = _load_verifier()
        states = verifier.dialog_states(game.decompile("BDIMOEN"))
        transitions = verifier.dialog_transitions(states[67])
        self.assertEqual(3, len(transitions), states[67])
        hood_routes = [
            (trigger, route)
            for trigger, route in transitions
            if re.search(r"\bGOTO\s+68\b", route, re.IGNORECASE)
        ]
        self.assertEqual(1, len(hood_routes), states[67])
        trigger, route = hood_routes[0]
        self.assertRegex(trigger, r"(?i)\bFalse\s*\(\s*\)")
        self.assertRegex(
            route,
            r'(?i)SetGlobal\s*\(\s*"BD_MDD007"\s*,\s*"BD0103"\s*,\s*2\s*\)',
        )
        self.assert_false_gated(game.decompile(), "bd_sddd12_hood", 1)
        self.assertTrue(game.tlks_unchanged(), "dialog gating must stay TLK-neutral")

    def test_no_aura_picker_rejects_a_duplicate_hood_route(self) -> None:
        game = self._game(
            _dialog_source(
                extra_hood_choice=True,
            )
        )
        original = game.dialog_path().read_bytes()
        result = game.install_patch("bd_sddd12_hood")
        transcript = game.transcript(result)
        self.assertNotIn("SUCCESSFULLY INSTALLED", transcript, transcript)
        self.assertIn("does not match the current no-Aura four-state picker", transcript)
        self.assertEqual(game.dialog_path().read_bytes(), original)

    def test_no_aura_picker_rejects_a_missing_hood_route(self) -> None:
        game = self._game(
            _dialog_source(
                omit_hood_choice=True,
            )
        )
        original = game.dialog_path().read_bytes()
        result = game.install_patch("bd_sddd12_hood")
        transcript = game.transcript(result)
        self.assertNotIn("SUCCESSFULLY INSTALLED", transcript, transcript)
        self.assertIn("does not match the current no-Aura four-state picker", transcript)
        self.assertEqual(game.dialog_path().read_bytes(), original)

    def test_components_use_the_semantic_helper_not_numeric_bdscry_edits(self) -> None:
        self.assertTrue(HELPER.is_file(), "production native-layout helper is missing")
        setup = SETUP.read_text(encoding="utf-8")
        hood = HOOD_SOURCE.read_text(encoding="utf-8")
        omen = OMEN_SOURCE.read_text(encoding="utf-8")
        self.assertIn("csr_scry_flag = ~bd_sddd12_hood~", setup)
        self.assertIn("csr_scry_flag = ~bd_sddd12_imoen~", omen)
        self.assertIn("csr_scry_flag = ~bd_sddd12_caelar~", omen)
        self.assertNotRegex(setup + hood + omen, r"ADD_TRANS_TRIGGER\s+BDSCRY\s+\d+")

    def test_component_225_preserves_the_component_220_item_contract(self) -> None:
        setup = SETUP.read_text(encoding="utf-8")
        omen = OMEN_SOURCE.read_text(encoding="utf-8")
        cut_lists = COMP220_LISTS.read_text(encoding="utf-8")

        self.assertRegex(
            setup,
            r"(?s)BEGIN\s+@225\s+DESIGNATED\s+225.*?"
            r"REQUIRE_COMPONENT\s+~[^~]+~\s+~120~.*?"
            r"REQUIRE_COMPONENT\s+~[^~]+~\s+~220~.*?"
            r"INCLUDE\s+~chriz-sod-remix/lib/comp225\.tpa~",
        )
        self.assertIn(
            "$csr_cut_bd1200(~BDWIGHDD@2474@1951~)",
            cut_lists,
        )
        self.assertIn("csr225_schedule != 0", omen)
        self.assertIn("WRITE_ASCIIE csr225_essence_dst ~BDMISC59~ #8", omen)
        self.assertIn("WRITE_LONG  (csr225_target + 0x44) 2", omen)


class ScryingPoolVerifierLayoutTests(unittest.TestCase):
    def test_verifier_accepts_no_aura_four_state_layout(self) -> None:
        verifier = _load_verifier()
        self.assertEqual(
            verifier.scry_picker_states({0: "", 1: "", 2: "", 3: ""}),
            (0,),
        )

    def test_verifier_rejects_a_changed_five_state_layout(self) -> None:
        verifier = _load_verifier()
        with self.assertRaises(verifier.VerificationError):
            verifier.scry_picker_states({index: "" for index in range(5)})


if __name__ == "__main__":
    unittest.main()
