#!/usr/bin/env python3
"""Component 285 installer checks; every write is inside a disposable fake game.

The effective-resource checks are opt-in: set CSR285_SOURCE_GAME to a BG2EE/EET
game directory. Resources are read directly from override/KEY/BIFF and copied to
TemporaryDirectory; WeiDU is never run against that source game. Proprietary
resource bytes are neither stored in this repository nor needed by default tests.
These are installer/resource checks, not live encounter acceptance.
"""
from __future__ import annotations

import os
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
from test_comp291_installer import WEIDU, compact, tree, write_fake_game

SOURCE_GAME = os.environ.get("CSR285_SOURCE_GAME")
PUBLIC = "chriz-sod-remix/setup-chriz-sod-remix.tp2"
TYPES = {"itm": 1005, "spl": 1006, "bcs": 1007, "ids": 1008,
         "cre": 1009, "are": 1010, "dlg": 1011, "2da": 1012,
         "vvc": 1019, "eff": 1016}


def word(data: bytes, offset: int) -> int:
    return struct.unpack_from("<H", data, offset)[0]


def dword(data: bytes, offset: int) -> int:
    return struct.unpack_from("<I", data, offset)[0]


def resref(data: bytes, offset: int) -> str:
    return data[offset:offset + 8].split(b"\0", 1)[0].decode("ascii").upper()


def script_blocks(source: str) -> list[str]:
    return re.findall(r"(?ms)^IF\n.*?^END\s*", source.replace("\r\n", "\n"))


def effects(data: bytes, kind: str):
    """Read indexed effect records; do not assume their physical order."""
    if kind in {"itm", "spl"}:
        base = dword(data, 0x6A)
        indices = set(range(word(data, 0x6E), word(data, 0x6E) + word(data, 0x70)))
        stride = 0x38 if kind == "itm" else 0x28
        for ability in range(word(data, 0x68)):
            header = dword(data, 0x64) + ability * stride
            start = word(data, header + 0x20)
            indices.update(range(start, start + word(data, header + 0x1E)))
        return [data[base + i * 0x30:base + (i + 1) * 0x30] for i in sorted(indices)]
    if kind == "cre":
        base, count = dword(data, 0x2C4), dword(data, 0x2C8)
        if data[0x33] == 0:
            return [data[base + i * 0x30:base + (i + 1) * 0x30] for i in range(count)]
        result = []
        for i in range(count):
            source = data[base + i * 0x108:base + (i + 1) * 0x108]
            # Normalize the fields tested here to compact V1 positions. CRE V2
            # effect records include the eight-byte EFF header reservation.
            effect = bytearray(0x30)
            struct.pack_into("<HBBII", effect, 0, dword(source, 8), dword(source, 12),
                             dword(source, 16), dword(source, 20), dword(source, 24))
            effect[12] = dword(source, 28) & 0xFF
            struct.pack_into("<I", effect, 14, dword(source, 32))
            effect[20:28] = source[40:48]
            result.append(bytes(effect))
        return result
    raise ValueError(kind)


class EffectiveResources:
    """Read loose resources and uncompressed BIFF resources without game writes."""

    def __init__(self, game: Path):
        self.game = game
        self.loose = {p.name.upper(): p for p in (game / "override").iterdir()}
        key = (game / "chitin.key").read_bytes()
        if key[:8] != b"KEY V1  ":
            raise ValueError("unsupported source KEY format")
        self.biffs = []
        for i in range(dword(key, 8)):
            entry = dword(key, 0x10) + 12 * i
            offset, length = dword(key, entry + 4), word(key, entry + 8)
            name = key[offset:offset + length].rstrip(b"\0").decode("ascii").replace("\\", "/")
            self.biffs.append(game / name)
        self.index = {}
        for i in range(dword(key, 12)):
            entry = dword(key, 0x14) + 14 * i
            self.index[(resref(key, entry), word(key, entry + 8))] = dword(key, entry + 10)

    def read(self, name: str) -> bytes:
        if name.upper() in self.loose:
            return self.loose[name.upper()].read_bytes()
        suffix = Path(name).suffix[1:].lower()
        locator = self.index[(Path(name).stem.upper(), TYPES[suffix])]
        with self.biffs[locator >> 20].open("rb") as stream:
            header = stream.read(0x14)
            if header[:8] != b"BIFFV1  ":
                raise ValueError("source uses compressed BIFF; extract the required resources to a separate source fixture first")
            ordinal = locator & 0xFFFFF
            stream.seek(dword(header, 0x10) + ordinal * 16)
            entry = stream.read(16)
            stream.seek(dword(entry, 4))
            result = stream.read(dword(entry, 8))
            if len(result) != dword(entry, 8):
                raise ValueError(f"truncated BIFF resource {name}")
            return result

    def copy(self, name: str, target: Path) -> None:
        (target / name.lower()).write_bytes(self.read(name))

    def copy_ids(self, target: Path) -> None:
        names = {f"{ref}.IDS" for ref, kind in self.index if kind == TYPES["ids"]}
        names.update(name for name in self.loose if name.endswith(".IDS"))
        # WeiDU discards its generated ADD_SPELL scratch map at startup. It is
        # not an engine IDS dependency and must not be seeded as a game asset.
        names.discard("ADD_SPELL.IDS")
        for name in names:
            self.copy(name, target)

    def copy_symbol(self, symbol: str, target: Path) -> str:
        ids = self.read("spell.ids").decode("ascii", errors="replace")
        match = re.search(rf"^\s*(0x[\da-fA-F]+|\d+)\s+{re.escape(symbol)}\s*$", ids, re.M)
        if not match:
            raise KeyError(f"spell symbol unavailable: {symbol}")
        value = int(match[1], 16 if match[1].lower().startswith("0x") else 10)
        kind, number = divmod(value, 1000)
        name = f"{ {1: 'sppr', 2: 'spwi', 3: 'spin'}[kind]}{number:03}.spl"
        self.copy(name, target)
        return name


class InstallerFixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="csr285-installer-")
        self.addCleanup(self.temp.cleanup)
        self.game = Path(self.temp.name)
        write_fake_game(self.game)
        self.override = self.game / "override"
        shutil.copytree(ROOT / "chriz-sod-remix", self.game / "chriz-sod-remix")

    def run_weidu(self, *args):
        return subprocess.run([str(WEIDU), *args, "--game", str(self.game),
                               "--language", "0", "--use-lang", "en_US", "--no-exit-pause"],
                              cwd=self.game, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=60)

    def install(self):
        return self.run_weidu(PUBLIC, "--force-install-list", "285")

    def assert_success(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("SUCCESSFULLY INSTALLED", result.stdout)

    def protected(self):
        return {name: (self.game / name).read_bytes() for name in (
            "chitin.key", "data/csr291.bif", "dialog.tlk", "lang/en_us/dialog.tlk")}

    def decompile(self, name):
        destination = self.game / "decompiled"
        destination.mkdir(exist_ok=True)
        result = self.run_weidu(str(self.override / name.lower()), "--out", str(destination),
                                "--log", str(destination / "audit.log"))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        matches = [p for p in destination.iterdir() if p.name.upper() == Path(name).stem.upper() + ".BAF"]
        self.assertEqual(len(matches), 1)
        return matches[0].read_text(encoding="utf-8", errors="replace")


@unittest.skipUnless(WEIDU.is_file(), "real WeiDU unavailable; set WEIDU_EXE")
class Component285MissingResourceTests(InstallerFixture):
    def test_absent_finale_cannot_publish_any_resource(self):
        before, protected = tree(self.override), self.protected()
        result = self.install()
        self.assertNotIn("SUCCESSFULLY INSTALLED", result.stdout)
        self.assertRegex(result.stdout, "SKIPPING|NOT INSTALLED DUE TO ERRORS")
        self.assertEqual(tree(self.override), before)
        self.assertEqual(self.protected(), protected)


@unittest.skipUnless(WEIDU.is_file() and SOURCE_GAME,
                     "opt-in effective fixtures: set CSR285_SOURCE_GAME and optionally WEIDU_EXE")
class Component285EffectiveTests(InstallerFixture):
    INPUTS = (
        "BDBELHIF.CRE", "BDBELHIF.BCS", "BDBELHIA.ITM", "BDBELHI1.ITM", "BDBELHI2.ITM",
        "BD4700.BCS", "BD4700.ARE", "BD4600.ARE", "BDELEV01.BCS", "BDCUT56.BCS", "DDOORH.VVC",
        "BDABIGRE.CRE", "BDABIRED.CRE", "BDERINYE.CRE", "BDBONEFI.CRE",
        "BDHEPHER.BCS", "BDFINHEP.CRE", "BDFINHEP.SPL", "BDCLMA01.BCS",
    )
    SPELLS = (
        "WIZARD_STONE_SKIN", "WIZARD_MIRROR_IMAGE", "CLERIC_ARMOR_OF_FAITH",
        "WIZARD_MINOR_GLOBE_OF_INVULNERABILITY", "CLERIC_FREE_ACTION",
        "WIZARD_MAGIC_MISSILE", "WIZARD_MELF_ACID_ARROW", "WIZARD_FLAME_ARROW",
        "WIZARD_BREACH", "WIZARD_GLITTERDUST", "WIZARD_SECRET_WORD",
        "WIZARD_GREATER_MALISON", "CLERIC_CURE_SERIOUS_WOUNDS", "CLERIC_COMMAND",
    )
    CHANGED = {"BDBELHIF.CRE", "BDBELHIF.BCS", "BD4700.BCS", "BD4600.ARE",
               "BDELEV01.BCS", "BDHEPHER.BCS"}
    CREATED = ({f"CSR285D{i}.{suffix}" for i in range(1, 5) for suffix in ("CRE", "BCS")}
               | {f"CSR285H{i}.SPL" for i in range(2, 6)}
               | {"CSR285AR.ITM", "CSR285W1.ITM", "CSR285W2.ITM",
                  "CSR285HP.CRE", "CSR285HI.CRE", "CSR285HF.SPL", "CSR285HX.SPL",
                  "CSR285HB.BCS", "CSR285HN.BCS", "CSR285HC.BCS"})

    @classmethod
    def setUpClass(cls):
        cls.source = EffectiveResources(Path(SOURCE_GAME))

    def setUp(self):
        super().setUp()
        self.source.copy_ids(self.override)
        for name in self.INPUTS:
            self.source.copy(name, self.override)
        # Script references in existing creature slots are inputs, not guesses
        # at SCS's install-specific generated resource names.
        for name in ("BDABIGRE.CRE", "BDABIRED.CRE", "BDERINYE.CRE", "BDBONEFI.CRE", "SHUPOL01.CRE"):
            try:
                creature = self.source.read(name)
            except KeyError:
                if name == "SHUPOL01.CRE":
                    continue
                raise
            self.source.copy(name, self.override)
            for offset in (0x248, 0x250, 0x258, 0x260, 0x268):
                script = resref(creature, offset)
                if script and script != "NONE":
                    self.source.copy(script + ".BCS", self.override)
        self.spells = {symbol: self.source.copy_symbol(symbol, self.override) for symbol in self.SPELLS}

    def resource(self, name):
        return (self.override / name.lower()).read_bytes()

    def script(self, name):
        return compact(self.decompile(name))

    def assert_failure_rollback(self, before, protected, result):
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("NOT INSTALLED DUE TO ERRORS", result.stdout)
        self.assertIn("#285", result.stdout + result.stderr)
        self.assertEqual(tree(self.override), before)
        self.assertEqual(self.protected(), protected)

    def test_public_installer_preserves_foreign_resources_and_encounter_contract(self):
        before = tree(self.override)
        originals = {name: self.resource(name) for name in self.INPUTS}
        original_boss_ai = self.decompile("BDBELHIF.BCS")
        original_heph_ai = self.script("BDHEPHER.BCS")
        protected = self.protected()
        self.assert_success(self.install())
        after = tree(self.override)
        self.assertEqual(after.keys() - before.keys(), self.CREATED)
        self.assertEqual({name for name in before if after[name] != before[name]}, self.CHANGED)
        # The portal map label legitimately appends a TLK string.
        for name in ("chitin.key", "data/csr291.bif"):
            self.assertEqual((self.game / name).read_bytes(), protected[name])
        self.assertEqual((self.game / "lang/en_us/dialog.tlk").read_bytes()[18:44],
                         protected["lang/en_us/dialog.tlk"][18:44])

        boss = self.resource("BDBELHIF.CRE")
        self.assertEqual(word(boss, 0x24), word(originals["BDBELHIF.CRE"], 0x24))
        self.assertEqual(word(boss, 0x26), word(originals["BDBELHIF.CRE"], 0x26))
        self.assertEqual(boss[0x5D], 60)
        self.assertEqual(boss[0x60:0x64], originals["BDBELHIF.CRE"][0x60:0x64])
        self.assertEqual(boss[0x53], originals["BDBELHIF.CRE"][0x53], "base APR must not increase")
        movement = [fx for fx in effects(boss, "cre") if word(fx, 0) == 176]
        self.assertEqual([(dword(fx, 4), dword(fx, 8), fx[12]) for fx in movement], [(125, 2, 9)])
        for name in ("CSR285AR.ITM", "CSR285W1.ITM", "CSR285W2.ITM"):
            fx = effects(self.resource(name), "itm")
            self.assertFalse(any(word(f, 0) == 166 for f in fx), name)
            gates = [f for f in fx if word(f, 0) == 120 and dword(f, 8) == 0]
            self.assertTrue(all(dword(f, 4) == 0 for f in gates), name)
        self.assertTrue(any(word(f, 0) == 120 for f in effects(self.resource("CSR285AR.ITM"), "itm")))
        self.assertTrue(any(word(f, 0) == 120 for f in effects(self.resource("CSR285W2.ITM"), "itm")))
        for tier, bonus in ((2, 50), (3, 100), (4, 125), (5, 150)):
            hp = [f for f in effects(self.resource(f"CSR285H{tier}.SPL"), "spl") if word(f, 0) == 18]
            self.assertEqual([(dword(f, 4), dword(f, 8), f[12]) for f in hp], [(bonus, 0, 1)])

        ai = self.script("BDBELHIF.BCS")
        for block in script_blocks(original_boss_ai):
            if not any(flag in block.upper() for flag in ("BD_DISPEL", "BD_GATE", "BD_IINV")):
                self.assertIn(compact(block), ai, "unrelated native/third-party boss behavior changed")
        self.assertNotIn("FORCESPELL([PC],WIZARD_TRUE_DISPEL_MAGIC)", ai)
        self.assertEqual(ai.count('GLOBAL("CSR285_INIT","LOCALS",0)'), 5)
        self.assertEqual(ai.count('SETGLOBAL("CSR285_INIT","LOCALS",1)'), 5)
        self.assertIn('SETGLOBALTIMER("CSR285_BREACH","LOCALS",THREE_ROUNDS)', ai)
        self.assertIn('SETGLOBALTIMER("CSR285_BREACH","LOCALS",FOUR_ROUNDS)', ai)
        focus = "ATTACKONEROUND(LASTSEENBY(MYSELF))"
        self.assertEqual(ai.count(focus) - compact(original_boss_ai).count(focus), 6)
        self.assertIn('GLOBALLT("CSR285_ADDS","BD4700",4)', ai)
        self.assertIn('SETGLOBALTIMER("CSR285_GATE","LOCALS",FOUR_ROUNDS)', ai)
        for i in range(1, 5):
            death = self.script(f"CSR285D{i}.BCS")
            self.assertIn('GLOBAL("CSR285_COUNTED_DEAD","LOCALS",0)', death)
            self.assertIn('SETGLOBAL("CSR285_COUNTED_DEAD","LOCALS",1)', death)
            self.assertIn('INCREMENTGLOBAL("CSR285_ADDS","BD4700",-1)', death)
        arena_source = self.decompile("BD4700.BCS")
        arena = compact(arena_source)
        for old in ("BDDCOR01", "BDHAMATU"):
            self.assertNotIn(f'CREATECREATUREEFFECT("{old}"', arena)
        self.assertEqual(arena.count('INCREMENTGLOBAL("CSR285_ADDS","BD4700",1)'), 10)
        # Count opening creatures at each difficulty, allowing the native
        # plot/area guards to stand. This catches an accidentally retained
        # six-devil Insane branch despite a correct-looking cap elsewhere.
        tiers = {"EASIEST": 1, "EASY": 2, "NORMAL": 3, "HARD": 4, "HARDEST": 5}
        opening = {}
        for difficulty in range(1, 6):
            count = 0
            for block in script_blocks(arena_source):
                if not re.search(r'CreateCreatureEffect\("CSR285D[1-4]"', block, re.I):
                    continue
                tests = re.findall(r"(!?)Difficulty(GT|LT)?\((\w+)\)", block, re.I)
                allowed = True
                for negated, operator, tier in tests:
                    value = tiers[tier.upper()]
                    passed = difficulty > value if operator.upper() == "GT" else difficulty < value if operator.upper() == "LT" else difficulty == value
                    allowed &= not passed if negated else passed
                if allowed:
                    count += len(re.findall(r'CreateCreatureEffect\("CSR285D[1-4]"', block, re.I))
            opening[difficulty] = count
        self.assertEqual(opening, {1: 0, 2: 0, 3: 2, 4: 4, 5: 4})

        portal = self.script("BDELEV01.BCS")
        self.assertIn('GLOBAL("BD_HELLEVATOR","GLOBAL",0)', portal)
        self.assertEqual(portal.count('SETGLOBAL("BD_PLOT","GLOBAL",560)'), 1)
        self.assertEqual(portal.count('STARTCUTSCENEEX("BDCUT56",FALSE)'), 1)
        self.assertNotIn('STARTCUTSCENEEX("BDCUT55",FALSE)', portal)
        self.assertEqual(self.resource("BDCUT56.BCS"), originals["BDCUT56.BCS"])
        self.assertIn('GLOBALLT("BD_PLOT","GLOBAL",560)', arena)

        moderate = self.resource("CSR285HP.CRE")
        insane = self.resource("CSR285HI.CRE")
        native = originals["BDFINHEP.CRE"]
        for creature in (moderate, insane):
            self.assertEqual(creature[0x273], 14, "cleric/mage class")
            self.assertEqual(creature[0x234:0x237], bytes((14, 14, 0)))
            self.assertEqual(creature[0x28:0x2C], native[0x28:0x2C], "devil animation")
            self.assertEqual(creature[0x24:0x28], native[0x24:0x28], "no second boss HP boost")
            self.assertEqual(resref(creature, 0x268), "CSR285HC")
            self.assertGreater(dword(creature, 0x2B4), 0, "real finite memorized spells")
            total = 0
            for index in range(dword(creature, 0x2AC)):
                info = dword(creature, 0x2A8) + index * 16
                count = dword(creature, info + 12)
                self.assertEqual(word(creature, info + 2), count, "base spell capacity matches finite book")
                self.assertEqual(word(creature, info + 4), count, "total spell capacity matches finite book")
                total += count
            self.assertEqual(total, dword(creature, 0x2B4))
        self.assertLess(dword(moderate, 0x2B4), dword(insane, 0x2B4))
        for name, target in (("CSR285HF.SPL", "CSR285HP"), ("CSR285HX.SPL", "CSR285HI")):
            forms = [f for f in effects(self.resource(name), "spl") if word(f, 0) == 151]
            self.assertEqual([resref(f, 20) for f in forms], [target])
        heph = self.script("BDHEPHER.BCS")
        self.assertIn(original_heph_ai, heph, "human and other encounter behavior remains intact")
        self.assertIn('DIFFICULTY(HARDEST)', heph)
        self.assertIn('!DIFFICULTY(HARDEST)', heph)
        self.assertIn('FORCESPELLRES("CSR285HF",MYSELF)', heph)
        self.assertIn('FORCESPELLRES("CSR285HX",MYSELF)', heph)
        combat = self.script("CSR285HC.BCS")
        for forbidden in ("FORCESPELL", "SPELLNODEC", "REST(", "APPLYSPELL", "CREATECREATURE"):
            self.assertNotIn(forbidden, combat)
        self.assertIn("HAVESPELL(", combat)

    def test_ambiguous_portal_activation_rejects_and_restores_everything(self):
        # Duplicate the actual compiled blocks. This is an unsupported source
        # collision, not a text-only test of the installer's matching expression.
        script = self.resource("BDELEV01.BCS")
        framing = script.replace(b"\r\n", b"\n")
        self.assertTrue(framing.startswith(b"SC\n") and framing.endswith(b"SC\n"))
        (self.override / "bdelev01.bcs").write_bytes(framing[:-3] + framing[3:])
        before, protected = tree(self.override), self.protected()
        self.assert_failure_rollback(before, protected, self.install())

    def test_truncated_transform_rejects_without_partial_boss_or_portal_changes(self):
        (self.override / "bdfinhep.spl").write_bytes(b"SPL V1  ")
        before, protected = tree(self.override), self.protected()
        self.assert_failure_rollback(before, protected, self.install())

    def test_native_caster_fallback_still_installs_the_full_encounter(self):
        (self.override / "shupol01.cre").unlink(missing_ok=True)
        self.test_public_installer_preserves_foreign_resources_and_encounter_contract()

    def test_second_tail_attempt_cannot_stack_movement_or_hp_setup(self):
        self.assert_success(self.install())
        before, protected = tree(self.override), self.protected()
        (self.game / "second-tail.tp2").write_text('''BACKUP ~second-tail-backup~
AUTHOR ~fixture~
LANGUAGE ~English~ ~english~ ~chriz-sod-remix/languages/english/setup.tra~
BEGIN ~separate tail application~ DESIGNATED 285
INCLUDE ~chriz-sod-remix/lib/comp285.tpa~
''', encoding="ascii")
        result = self.run_weidu("second-tail.tp2", "--force-install-list", "285")
        self.assert_failure_rollback(before, protected, result)


if __name__ == "__main__":
    unittest.main()
