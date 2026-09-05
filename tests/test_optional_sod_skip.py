"""Compiled-dialog/XP contracts and a disposable native ground-pile probe.

The state replay is a model over WeiDU-decompiled actions, not a live game test.
The ground-pile probe's native CopyGroundPilesTo behavior requires a coordinated
engine run; these tests deliberately do not claim to simulate that primitive.
"""

import importlib.util
import json
import re
import shutil
import struct
import subprocess
import unittest
import zlib
from pathlib import Path

from test_bdscry_compat import (
    ROOT, WEIDU, SyntheticDialogGame, _dialog_source, _load_verifier,
)


PROTOTYPE = ROOT / "research/prototypes/optional-sod-skip"


def replay(actions, state):
    """Fail on unknown modeled actions; consume the actual compiled action text."""
    for line in actions.splitlines():
        line = line.split("//", 1)[0].strip()
        if not line:
            continue
        match = re.fullmatch(r'SetGlobal\("([^"]+)","GLOBAL",(\d+)\)', line, re.I)
        if match:
            state["globals"][match[1].upper()] = int(match[2])
            continue
        match = re.fullmatch(r'AddXPObject\(Player(\d),(\d+)\)', line, re.I)
        if match:
            state["xp"][int(match[1]) - 1] += int(match[2])
            continue
        raise AssertionError(f"unmodeled action: {line}")


def parse_containers(data):
    offset, = struct.unpack_from("<I", data, 0x70)
    count, = struct.unpack_from("<H", data, 0x74)
    items, = struct.unpack_from("<I", data, 0x78)
    result = {}
    for index in range(count):
        pos = offset + index * 0xC0
        name = data[pos:pos + 32].split(b"\0")[0].decode("ascii")
        first, length = struct.unpack_from("<II", data, pos + 0x40)
        result[name] = {
            "xy": struct.unpack_from("<HH", data, pos + 0x20),
            "type": struct.unpack_from("<H", data, pos + 0x24)[0],
            "items": [
                data[items + n * 20:items + n * 20 + 8].split(b"\0")[0].decode("ascii")
                for n in range(first, first + length)
            ],
        }
    return result


@unittest.skipUnless(WEIDU.is_file(), f"WeiDU unavailable: {WEIDU}")
class OptionalSkipContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.game = SyntheticDialogGame(_dialog_source())
        cls.addClassCleanup(cls.game.cleanup)
        shutil.copytree(PROTOTYPE, cls.game.root / "prototype")
        ids = cls.game.root / "override/action.ids"
        ids.write_text(ids.read_text() + "259 AddXPObject(O:Object*,I:XP*)\n", encoding="ascii")
        (cls.game.root / "override/object.ids").write_text(
            "IDS V1.0\n21 Player1\n22 Player2\n23 Player3\n24 Player4\n25 Player5\n26 Player6\n",
            encoding="ascii",
        )
        setup = cls.game.root / "setup-skip-contract.tp2"
        setup.write_text(
            'BACKUP ~weidu_external/backup/skip-contract~\nAUTHOR ~test~\n'
            'BEGIN ~compile optional skip prototype~\n'
            'LOAD_TRA ~prototype/english.tra~\n'
            'COMPILE ~prototype/csrskip.d~\nCOMPILE ~prototype/csrskxp.baf~\n',
            encoding="ascii",
        )
        result = cls.game._run(setup)
        if "SUCCESSFULLY INSTALLED" not in cls.game.transcript(result):
            raise AssertionError(cls.game.transcript(result))
        cls.verifier = _load_verifier()
        cls.dialog = cls.game.decompile("csrskip")
        cls.states = cls.verifier.dialog_states(cls.dialog)
        out = Path(cls.game.temporary.name) / "xp-decompile"
        out.mkdir()
        resource = cls.game._find_output(cls.game.root / "override", "csrskxp.bcs")
        result = subprocess.run(
            [str(WEIDU), str(resource), "--game", str(cls.game.root), "--no-exit-pause"],
            cwd=out, capture_output=True, text=True, timeout=60,
        )
        if result.returncode:
            raise AssertionError(result.stdout + result.stderr)
        cls.xp_script = cls.game._find_output(out, "csrskxp.baf").read_text()

    def fresh(self):
        return {"globals": {"CSR_SKIP_CHOICE": 0, "CSR_SKIP_ITEMS_READY": 0,
                            "CSR_SKIP_XP": 0}, "xp": [161000, 150000, 120000, 100000, 90000, 80000]}

    def choose(self, index, reply, state):
        transitions = self.verifier.dialog_transitions(self.states[index])
        self.assertEqual(2, len(transitions))
        _, route = transitions[reply]
        action = re.search(r'DO\s+~(.*?)~', route, re.S | re.I)
        if action:
            replay(action[1], state)
        target = re.search(r'GOTO\s+(\d+)', route, re.I)
        return int(target[1]) if target else None

    def tick(self, state):
        blocks = self.verifier.baf_blocks(self.xp_script)
        self.assertEqual(1, len(blocks))
        trigger, action = blocks[0]
        self.assertEqual(1, len(re.findall(r'RESPONSE\s+#100', action)))
        action = re.sub(r'RESPONSE\s+#100\s*', '', action)
        guards = re.findall(r'Global\("([^"]+)","GLOBAL",(\d+)\)', trigger, re.I)
        self.assertEqual(3, len(guards), trigger)
        if all(state["globals"].get(name.upper(), 0) == int(value) for name, value in guards):
            replay(action, state)

    def test_exact_prompt_and_two_independent_confirmation_states(self):
        self.assertEqual({0, 1, 2}, set(self.states))
        self.assertIn("Do you want to skip SoD? You will get 250000 experience on your main character if you skip.", self.dialog)
        self.assertIn("Are you sure you want to skip SoD?", self.dialog)
        self.assertIn("Are you sure you want to play SoD?", self.dialog)
        self.assertRegex(self.dialog, r'(?is)IF\s+~\s*False\(\)\s*~\s+THEN BEGIN 1\b')
        self.assertRegex(self.dialog, r'(?is)IF\s+~\s*False\(\)\s*~\s+THEN BEGIN 2\b')

    def test_both_confirmation_declines_loop_without_side_effects(self):
        for reply, confirmation in ((0, 1), (1, 2)):
            state = self.fresh()
            original = json.dumps(state, sort_keys=True)
            self.assertEqual(confirmation, self.choose(0, reply, state))
            self.assertEqual(0, self.choose(confirmation, 1, state))
            self.assertEqual(original, json.dumps(state, sort_keys=True))

    def test_confirm_play_sod_never_awards_xp_even_after_reload(self):
        state = self.fresh()
        self.choose(2, 0, state)
        self.assertEqual(2, state["globals"]["CSR_SKIP_CHOICE"])
        state["globals"]["CSR_SKIP_ITEMS_READY"] = 1
        state = json.loads(json.dumps(state))
        for _ in range(10):
            self.tick(state)
        self.assertEqual(self.fresh()["xp"], state["xp"])

    def test_skip_awards_only_after_item_preflight_and_only_once(self):
        state = self.fresh()
        self.choose(1, 0, state)
        self.tick(state)
        self.assertEqual(self.fresh()["xp"], state["xp"])
        state["globals"]["CSR_SKIP_ITEMS_READY"] = 1
        for _ in range(3):
            self.tick(state)
            state = json.loads(json.dumps(state))
        self.assertEqual([411000, 150000, 120000, 100000, 90000, 80000], state["xp"])
        self.assertEqual(1, state["globals"]["CSR_SKIP_XP"])

    def test_guard_precedes_the_only_additive_protagonist_award(self):
        self.assertEqual(1, self.xp_script.lower().count("addxpobject("))
        self.assertLess(self.xp_script.index('SetGlobal("CSR_SKIP_XP"'), self.xp_script.index("AddXPObject"))
        self.assertNotRegex(self.xp_script + self.dialog, r'(?i)AddexperienceParty|SetXP|GiveGold|GiveItemCreate')


@unittest.skipUnless(WEIDU.is_file(), f"WeiDU unavailable: {WEIDU}")
class GroundPileProbeTests(unittest.TestCase):
    def test_probe_only_publishes_new_owned_resources(self):
        game = SyntheticDialogGame(_dialog_source())
        self.addCleanup(game.cleanup)
        shutil.copytree(PROTOTYPE / "csr-ground-probe", game.root / "csr-ground-probe")
        area = bytearray(0x11C)
        area[:8] = b"AREAV1.0"
        area[8:16] = b"BD0103\0\0"
        item = bytearray(0x72)
        item[:8] = b"ITM V1  "
        (game.root / "override/bd0103.are").write_bytes(area)
        (game.root / "override/potn08.itm").write_bytes(item)
        before = {p.name.casefold(): p.read_bytes() for p in (game.root / "override").iterdir()}
        missing_gate = game._run(game.root / "csr-ground-probe/setup-csr-ground-probe.tp2")
        self.assertIn("SKIPPING:", game.transcript(missing_gate))
        self.assertEqual(before, {p.name.casefold(): p.read_bytes() for p in (game.root / "override").iterdir()})
        (game.root / "csr_ground_probe_disposable.ok").write_text("synthetic test fixture\n")
        result = game._run(game.root / "csr-ground-probe/setup-csr-ground-probe.tp2")
        self.assertIn("SUCCESSFULLY INSTALLED", game.transcript(result), game.transcript(result))
        after = {p.name.casefold(): p.read_bytes() for p in (game.root / "override").iterdir()}
        for name, data in before.items():
            self.assertEqual(data, after[name], name)
        self.assertEqual({"csrgp001.are", "csrgp002.are", "csrgpa.itm", "csrgpb.itm", "csrgpc.itm", "csrgpd.itm"}, set(after) - set(before))
        source = parse_containers(after["csrgp001.are"])
        target = parse_containers(after["csrgp002.are"])
        self.assertEqual(["csrgpa"], source["CSRSourceA"]["items"])
        self.assertEqual(["csrgpb"], source["CSRSourceB"]["items"])
        self.assertEqual(4, source["CSRSourceA"]["type"])
        self.assertEqual(4, source["CSRSourceB"]["type"])
        self.assertEqual(2, source["CSRSourceControl"]["type"])
        self.assertEqual(["csrgpc"], source["CSRSourceControl"]["items"])
        self.assertEqual([], target["CSRBG1PILE"]["items"])
        self.assertEqual((190, 540), target["CSRBG1PILE"]["xy"])
        self.assertEqual(4, target["CSRBG1PILE"]["type"])
        self.assertEqual([], target["CSRProbeBank"]["items"])
        self.assertEqual(["csrgpd"], target["CSRTargetControl"]["items"])
        for name in ("csrgp001.are", "csrgp002.are"):
            self.assertEqual(0, struct.unpack_from("<H", after[name], 0x58)[0])
            self.assertEqual(0, struct.unpack_from("<H", after[name], 0x5A)[0])
            self.assertEqual(b"\0" * 8, after[name][0x94:0x9C])


class GroundProbeVerifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("ground_probe_verifier", PROTOTYPE / "verify_ground_probe.py")
        cls.verifier = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.verifier)

    @staticmethod
    def area(definitions):
        count = sum(len(items) for _, _, items in definitions)
        item_offset = 0x11C + len(definitions) * 0xC0
        data = bytearray(item_offset + count * 20)
        data[:8] = b"AREAV1.0"
        struct.pack_into("<IHHI", data, 0x70, 0x11C, len(definitions), count, item_offset)
        item_index = 0
        for index, (name, kind, items) in enumerate(definitions):
            pos = 0x11C + index * 0xC0
            data[pos:pos + 32] = name.encode().ljust(32, b"\0")
            struct.pack_into("<HHH", data, pos + 0x20, 190, 540, kind)
            struct.pack_into("<II", data, pos + 0x40, item_index, len(items))
            for item in items:
                start = item_offset + item_index * 20
                data[start:start + 8] = item.encode().ljust(8, b"\0")
                item_index += 1
        return data

    def archive(self, target):
        source = [("CSRSourceA", 4, ["csrgpa"]), ("CSRSourceB", 4, ["csrgpb"]),
                  ("CSRSourceControl", 2, ["csrgpc"])]
        data = bytearray(b"SAV V1.0")
        for name, rows in ((b"CSRGp001.ARE\0", source), (b"csrgp002.are\0", target)):
            area = self.area(rows)
            compressed = zlib.compress(area)
            data += struct.pack("<I", len(name)) + name
            data += struct.pack("<II", len(area), len(compressed)) + compressed
        return data

    def target(self, stage="copy"):
        return [("CSRBG1PILE", 4, ["csrgpa", "csrgpb"] if stage == "copy" else []),
                ("CSRProbeBank", 2, [] if stage == "copy" else ["csrgpa", "csrgpb"]),
                ("CSRTargetControl", 2, ["csrgpd"])]

    def test_accepts_named_copy_and_targeted_bank_with_controls_unchanged(self):
        for stage in ("copy", "bank"):
            result = self.verifier.verify(self.archive(self.target(stage)), stage)
            self.assertTrue(result["passed"], result)

    def test_rejects_copied_items_in_an_unnamed_pile(self):
        rows = self.target()
        rows[0] = ("CSRBG1PILE", 4, [])
        rows.append(("", 4, ["csrgpa", "csrgpb"]))
        self.assertFalse(self.verifier.verify(self.archive(rows), "copy")["passed"])

    def test_rejects_native_source_named_copy_beside_empty_receptacle(self):
        # Native 2.7.3.0 probe result: the copy created a source-named pile,
        # leaving the preplaced destination receptacle empty at the same point.
        rows = self.target()
        rows[0] = ("CSRBG1PILE", 4, [])
        rows.append(("CSRSourceA", 4, ["csrgpa", "csrgpb"]))
        result = self.verifier.verify(self.archive(rows), "copy")
        self.assertFalse(result["passed"])
        self.assertEqual(1, len(result["errors"]))
        self.assertIn("CSRBG1PILE", result["errors"][0])

    def test_rejects_unrelated_chest_item_or_duplicate_ground_item(self):
        for unexpected in ("csrgpc", "csrgpa"):
            rows = self.target()
            rows[0][2].append(unexpected)
            self.assertFalse(self.verifier.verify(self.archive(rows), "copy")["passed"])

    def test_allows_empty_ground_pile_to_disappear_after_bank(self):
        rows = self.target("bank")[1:]
        self.assertTrue(self.verifier.verify(self.archive(rows), "bank")["passed"])

    def test_rejects_truncated_archive(self):
        with self.assertRaises(ValueError):
            self.verifier.verify(self.archive(self.target())[:-3], "copy")

    def test_rejects_duplicate_named_receptacle(self):
        rows = self.target() + [("CSRBG1PILE", 4, [])]
        self.assertFalse(self.verifier.verify(self.archive(rows), "copy")["passed"])


if __name__ == "__main__":
    unittest.main()
