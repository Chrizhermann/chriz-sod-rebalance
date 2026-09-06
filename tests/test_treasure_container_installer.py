"""Component 900 through public WeiDU, using only disposable synthetic areas."""

import re
import struct
import subprocess
import unittest

from test_bdscry_compat import WEIDU
from test_optional_sod_skip_installer import SkipGame


def item(name, *, expiration=0, charges=(0, 0, 0), flags=1):
    return struct.pack("<8s4HI", name.encode("ascii"), expiration, *charges, flags)


PAYLOAD = [item(name, charges=(charges, 0, 0)) for name, charges in (
    ("BDDAGG03", 0), ("BDSHLD02", 0), ("BDBOOT04", 0), ("WAND04", 5),
    ("RING09", 0), ("SODTRE08", 0), ("SODTRE08", 0), ("SODTRE09", 0),
)]


def area(contents, *, target="Container009", containers=None, unused_items=0):
    """Nonzero target run, opaque metadata/trailer, and optional unused records."""
    if containers is None:
        containers = [("ControlBefore", [item("SW1H02")]),
                      (target, contents), ("ControlAfter", [item("STAF01")])]
    header = 0x11C
    item_offset = header + len(containers) * 0xC0
    data = bytearray(item_offset)
    data[:8] = b"AREAV1.0"
    struct.pack_into("<IH", data, 0x70, header, len(containers))
    rows = []
    for index, (name, items) in enumerate(containers):
        base = header + index * 0xC0
        data[base:base + 0xC0] = bytes([index + 1]) * 0xC0
        struct.pack_into("<32sHHH", data, base, name.encode("ascii"), 509, 3220, 2)
        struct.pack_into("<II", data, base + 0x40, len(rows), len(items))
        rows.extend(items)
    rows.extend([item("UNUSED")] * unused_items)
    struct.pack_into("<HI", data, 0x76, len(rows), item_offset if rows else 0)
    data.extend(b"".join(rows))
    data.extend(b"Opaque unrelated area section\x00\xff" * 3)
    return bytes(data)


def container_records(data, index):
    container_offset = struct.unpack_from("<I", data, 0x70)[0]
    item_offset = struct.unpack_from("<I", data, 0x78)[0]
    first, count = struct.unpack_from("<II", data, container_offset + index * 0xC0 + 0x40)
    return [data[item_offset + i * 20:item_offset + (i + 1) * 20]
            for i in range(first, first + count)]


class TreasureGame(SkipGame):
    def __init__(self, data, *, prerequisite=True, **kwargs):
        super().__init__(**kwargs)
        (self.root / "override/bd1000.are").write_bytes(data)
        log = self._find_output(self.root, "weidu.log")
        if prerequisite:
            # Synthetic fixture history only, never a real install's log.
            log.write_text(log.read_text() +
                           "~CHRIZ-SOD-REMIX/SETUP-CHRIZ-SOD-REMIX.TP2~ #0 #210 // fixture\n")
        self.before = self.tree()

    def install(self, *components):
        result = subprocess.run([
            str(WEIDU), "chriz-sod-remix/setup-chriz-sod-remix.tp2",
            "--force-install-list", *(str(n) for n in components or (900,)),
            "--language", "0", "--use-lang", "en_us", "--no-exit-pause",
            "--noautoupdate", "--quick-log",
        ], cwd=self.root, capture_output=True, text=True, timeout=60)
        return result, self.transcript(result)

    def installed_components(self):
        log = self._find_output(self.root, "weidu.log").read_text()
        return [int(n) for n in re.findall(
            r"^~CHRIZ-SOD-REMIX/SETUP-CHRIZ-SOD-REMIX.TP2~ #0 #(\d+)",
            log, re.MULTILINE | re.IGNORECASE)]


@unittest.skipUnless(WEIDU.is_file(), f"WeiDU unavailable: {WEIDU}")
class TreasureContainerInstallerTests(unittest.TestCase):
    def game(self, data, **kwargs):
        game = TreasureGame(data, **kwargs)
        self.addCleanup(game.cleanup)
        return game

    def assert_preserved(self, before, after, target_index=1):
        offset, count = struct.unpack_from("<IH", before, 0x70)
        target_base = offset + target_index * 0xC0
        original_items = container_records(before, target_index)
        self.assertEqual(original_items + PAYLOAD, container_records(after, target_index))
        for index in range(count):
            if index != target_index:
                self.assertEqual(container_records(before, index), container_records(after, index))
        expected_prefix = bytearray(before)
        for pos, width in ((0x76, 2), (0x78, 4), (target_base + 0x40, 8)):
            expected_prefix[pos:pos + width] = after[pos:pos + width]
        self.assertEqual(bytes(expected_prefix), after[:len(before)])
        old_count = struct.unpack_from("<H", before, 0x76)[0]
        new_count, new_offset = struct.unpack_from("<HI", after, 0x76)
        self.assertEqual(old_count + len(original_items) + len(PAYLOAD), new_count)
        self.assertEqual(len(before), new_offset)
        self.assertEqual(len(before) + new_count * 20, len(after))
        old_offset = struct.unpack_from("<I", before, 0x78)[0]
        self.assertEqual(before[old_offset:old_offset + old_count * 20],
                         after[new_offset:new_offset + old_count * 20])

    def test_empty_changed_and_same_resref_chests_preserve_every_original_record(self):
        variants = {
            "empty": [],
            "vanilla": [item("SW1H01")],
            "nondefault_metadata": [item("SW1H01", expiration=123,
                                         charges=(7, 8, 9), flags=0x82)],
            # Exact reported shape: count 3, first SW1H01; other resrefs synthetic.
            "reported_three_item_shape": [item("SW1H01"), item("STAF01"), item("POTN01")],
            "randomiser_shaped": [item("DW#FAKE", expiration=42, charges=(2, 3, 4), flags=6)],
            "existing_reward_resrefs": [item("WAND04", charges=(2, 1, 9), flags=0),
                                        item("SODTRE08"), item("SODTRE08")],
        }
        for name, contents in variants.items():
            with self.subTest(name=name):
                before = area(contents)
                game = self.game(before)
                result, text = game.install()
                self.assertEqual(0, result.returncode, text)
                self.assert_preserved(before, game.tree()["bd1000.are"])
                self.assertEqual([900], game.installed_components()[-1:])
                changed = {n for n, value in game.tree().items() if value != game.before.get(n)}
                self.assertEqual({"bd1000.are"}, changed)
                self.assertEqual(game.tlk_before, (game.root / "lang/en_us/dialog.tlk").read_bytes())

    def test_zero_length_item_table_is_valid(self):
        before = area([], containers=[("Container009", [])])
        game = self.game(before)
        result, text = game.install()
        self.assertEqual(0, result.returncode, text)
        self.assert_preserved(before, game.tree()["bd1000.are"], target_index=0)

    def test_largest_representable_relocated_item_count(self):
        before = area([item("SW1H01")], unused_items=65523)
        game = self.game(before)
        result, text = game.install()
        self.assertEqual(0, result.returncode, text)
        after = game.tree()["bd1000.are"]
        self.assert_preserved(before, after)
        self.assertEqual(65535, struct.unpack_from("<H", after, 0x76)[0])

    def test_case_and_space_normalized_target(self):
        before = area([item("SW1H01")], target="cOnTaInEr 009")
        game = self.game(before)
        result, text = game.install()
        self.assertEqual(0, result.returncode, text)
        self.assert_preserved(before, game.tree()["bd1000.are"])

    def test_900_then_910_public_invocation_keeps_exact_suffix(self):
        before = area([item("SW1H01"), item("STAF01"), item("POTN01")])
        game = self.game(before)
        result, text = game.install(900, 910)
        self.assertEqual(0, result.returncode, text)
        self.assertEqual([900, 910], game.installed_components()[-2:])
        self.assert_preserved(before, game.tree()["bd1000.are"])
        changed = {n for n, value in game.tree().items() if value != game.before.get(n)}
        self.assertEqual({"bd1000.are", "csrskask.cre", "csrskask.bcs", "csrskip.dlg",
                          "bd0103.bcs", "bd6100.bcs", "baldur.bcs"}, changed)

    def test_treasure_remove_marker_does_not_touch_the_area(self):
        game = self.game(area([item("SW1H01"), item("STAF01")]))
        result, text = game.install(901)
        self.assertEqual(0, result.returncode, text)
        self.assertEqual(game.before, game.tree())
        self.assertEqual([901], game.installed_components()[-1:])
        self.assertNotIn(900, game.installed_components())

    def test_210_prerequisite_remains_required(self):
        game = self.game(area([]), prerequisite=False)
        _, text = game.install()
        self.assertIn("SKIPPING:", text)
        self.assertIn("install component 210", text)
        self.assertNotIn(900, game.installed_components())
        self.assertEqual(game.before, game.tree())

    def test_missing_bd1000_resource_remains_a_skip(self):
        game = self.game(area([]))
        (game.root / "override/bd1000.are").unlink()
        before = game.tree()
        _, text = game.install()
        self.assertIn("SKIPPING:", text)
        self.assertNotIn(900, game.installed_components())
        self.assertEqual(before, game.tree())

    def test_non_eet_fixture_does_not_require_eet_or_910(self):
        before = area([item("STAF01"), item("POTN01")])
        game = self.game(before, eet=False)
        result, text = game.install()
        self.assertEqual(0, result.returncode, text)
        self.assert_preserved(before, game.tree()["bd1000.are"])

    def test_invalid_structures_fail_without_writing_area_or_tlk(self):
        good = area([item("SW1H01")])
        base = 0x11C + 0xC0
        variants = {"short_header": good[:0x100],
                    "wrong_signature": b"AREAV9.9" + good[8:],
                    "missing_target": area([], target="Elsewhere"),
                    "duplicate_target": area([], containers=[("Container009", []),
                                                               ("Container009", [])]),
                    "aliased_duplicate": area([], containers=[("Container009", []),
                                                                ("CONTAINER 009", [])]),
                    "item_count_overflow": area([item("SW1H01")], unused_items=65532)}
        for name, pos, value in (
            ("container_table_past_eof", 0x70, len(good)),
            ("container_table_in_header", 0x70, 0x20),
            ("container_table_high_bit", 0x70, 0xFFFFFFF0),
            ("item_table_past_eof", 0x78, len(good)),
            ("item_table_in_header", 0x78, 0x20),
            ("item_table_high_bit", 0x78, 0xFFFFFFF0),
            ("item_table_overlaps_containers", 0x78, 0x11C),
            ("target_first_out_of_bounds", base + 0x40, 4),
            ("target_count_out_of_bounds", base + 0x44, 4),
            ("target_count_high_bit", base + 0x44, 0xFFFFFFFF),
            ("other_container_run_out_of_bounds", 0x11C + 0x44, 4),
        ):
            bad = bytearray(good)
            struct.pack_into("<I", bad, pos, value)
            variants[name] = bytes(bad)
        for name, data in variants.items():
            with self.subTest(name=name):
                game = self.game(data)
                result, text = game.install()
                self.assertNotEqual(0, result.returncode, text)
                self.assertIn("comp900:", text)
                self.assertIn("NOT INSTALLED DUE TO ERRORS", text)
                self.assertNotIn(900, game.installed_components())
                self.assertEqual(game.before, game.tree())
                self.assertEqual(game.tlk_before, (game.root / "lang/en_us/dialog.tlk").read_bytes())


if __name__ == "__main__":
    unittest.main()
