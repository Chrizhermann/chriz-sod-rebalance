"""Focused parser and evidence-failure tests; synthetic resources only."""

from copy import deepcopy
import struct
import unittest
import zlib

from ending_save_evidence import (
    AREAS, compare, multiset, parse_are, parse_cre, parse_gam, parse_sto, read_sav,
)


def pack(data, offset, value, kind="I"):
    struct.pack_into("<" + kind, data, offset, value)


def item_image(resref="CSRMARK", charges=(4, 3, 2)):
    data = bytearray(20)
    data[:len(resref)] = resref.encode("ascii")
    for offset, charge in zip((10, 12, 14), charges):
        pack(data, offset, charge, "H")
    pack(data, 16, 1)
    return data


def cre_image():
    data = bytearray(0x2D4 + 80 + 20)
    data[:8] = b"CRE V1.0"
    pack(data, 0x2B8, 0x2D4)
    pack(data, 0x2BC, 0x2D4 + 80)
    pack(data, 0x2C0, 1)
    data[0x280:0x288] = b"CSRACTOR"
    data[0x2D4:0x2D4 + 80] = b"\xff" * 80
    pack(data, 0x2D4 + 21 * 2, 0, "H")
    pack(data, 0x2D4 + 76, 1000, "H")  # Fists: metadata, not a 1000th item.
    pack(data, 0x2D4 + 78, 7, "H")
    data[-20:] = item_image()
    return data


def gam_image():
    cre = cre_image()
    data = bytearray(0xB4 + 0x160 + len(cre) + 84)
    data[:8] = b"GAMEV2.0"
    pack(data, 0x20, 0xB4)
    pack(data, 0x24, 1)
    pack(data, 0xB4 + 4, 0xB4 + 0x160)
    pack(data, 0xB4 + 8, len(cre))
    data[0xB4 + 0x18:0xB4 + 0x20] = b"BD4300\0\0"
    data[0x58:0x60] = b"AR0602\0\0"
    data[0xB4 + 0x160:0xB4 + 0x160 + len(cre)] = cre
    globals_offset = len(data) - 84
    pack(data, 0x38, globals_offset)
    pack(data, 0x3C, 1)
    data[globals_offset:globals_offset + 7] = b"BD_PLOT"
    pack(data, globals_offset + 0x28, -1, "i")
    pack(data, 0x18, 12345)
    pack(data, 0x74, 67890)
    return data


def archive_entry(name, data, declared_size=None):
    name = name.encode("ascii") + b"\0"
    compressed = zlib.compress(data)
    return (struct.pack("<I", len(name)) + name
            + struct.pack("<II", len(data) if declared_size is None else declared_size, len(compressed))
            + compressed)


def evidence(area="BD4300"):
    value = {"resref": "CSRMARK", "expiration": 0, "charges": [4, 3, 2],
             "flags": 1, "slots": ["backpack1"]}
    return {
        "effective_current_area": area,
        "party": [{"party_order": 0, "death_variable": "CSRACTOR", "name": "Hero",
                   "area": area, "items": [value]}],
        "globals": {"BD_PLOT": 590},
        "areas": {name: {"present": name == area, "containers": []} for name in AREAS},
        "saved_stores": {},
    }


class SaveEvidenceTests(unittest.TestCase):
    def test_selected_weapon_is_not_an_item_index_and_slots_are_not_instances(self):
        data = cre_image()
        pack(data, 0x2D4 + 18 * 2, 0, "H")  # Two references to one item row.
        result = parse_cre(bytes(data))
        self.assertEqual(result["selected_weapon"], 1000)
        self.assertEqual(result["items"][0]["slots"], ["quick1", "backpack1"])
        self.assertEqual(sum(multiset(result["items"], {"CSRMARK"}).values()), 1)

    def test_cre_invalid_inventory_index_fails(self):
        data = cre_image()
        pack(data, 0x2D4, 1, "H")
        with self.assertRaisesRegex(ValueError, "slot references item"):
            parse_cre(bytes(data))

    def test_gam_active_party_area_overrides_header_and_signed_global_survives(self):
        result = parse_gam(bytes(gam_image()))
        self.assertEqual(result["header_current_area"], "AR0602")
        self.assertEqual(result["effective_current_area"], "BD4300")
        self.assertEqual(result["globals"]["BD_PLOT"], -1)
        self.assertEqual(result["party_gold"], 12345)
        self.assertEqual(result["real_time_seconds"], 67890)

    def test_gam_no_active_party_uses_header(self):
        data = gam_image()
        pack(data, 0x1C, -1, "h")
        self.assertEqual(parse_gam(bytes(data))["effective_current_area"], "AR0602")

    def test_sav_duplicate_names_truncation_and_size_mismatch_fail(self):
        entry = archive_entry("BD4300.ARE", b"test")
        self.assertEqual(read_sav(b"SAV V1.0" + entry), {"BD4300.ARE": b"test"})
        for data in (b"SAV V1.0" + entry + entry, b"SAV V1.0" + entry[:-1],
                     b"SAV V1.0" + archive_entry("BD4300.ARE", b"test", 3)):
            with self.subTest(data=data[-8:]), self.assertRaises(ValueError):
                read_sav(data)

    def test_are_uses_container_run_and_preserves_charges(self):
        data = bytearray(0xF4 + 0xC0 + 40)
        data[:8] = b"AREAV1.0"
        pack(data, 0x70, 0xF4)
        pack(data, 0x74, 1, "H")
        pack(data, 0x76, 2, "H")
        pack(data, 0x78, 0xF4 + 0xC0)
        pack(data, 0xF4 + 0x40, 1)
        pack(data, 0xF4 + 0x44, 1)
        data[-40:-20] = item_image("OTHER")
        data[-20:] = item_image()
        result = parse_are(bytes(data))
        self.assertEqual([value["resref"] for value in result[0]["items"]], ["CSRMARK"])
        self.assertEqual(result[0]["items"][0]["charges"], [4, 3, 2])
        pack(data, 0xF4 + 0x44, 2)
        with self.assertRaisesRegex(ValueError, "run exceeds table"):
            parse_are(bytes(data))

    def test_saved_store_stock_and_charges_are_distinct(self):
        data = bytearray(0x9C + 28)
        data[:8] = b"STORV1.0"
        pack(data, 8, 5)
        pack(data, 0x34, 0x9C)
        pack(data, 0x38, 1)
        data[0x9C:0x9C + 20] = item_image()
        pack(data, 0x9C + 20, 6)
        result = parse_sto(bytes(data))
        self.assertEqual(result["type"], 5)
        self.assertEqual(result["items"][0]["stock"], 6)
        self.assertEqual(result["items"][0]["charges"], [4, 3, 2])

    def test_handoff_detects_loss_duplication_and_charges(self):
        before, after = evidence(), evidence("AR0602")
        after["globals"].update(CSR_ENDING_USED=1, BD_PLOT=700)
        self.assertTrue(compare(before, after, {"CSRMARK"}, "handoff")["passed"])
        for change in ("loss", "duplicate", "charge"):
            changed = deepcopy(after)
            if change == "loss":
                changed["party"][0]["items"].clear()
            elif change == "duplicate":
                changed["areas"]["AR0602"]["containers"].append({"items": changed["party"][0]["items"]})
            else:
                changed["party"][0]["items"][0]["charges"][0] = 0
            with self.subTest(change=change):
                self.assertFalse(compare(before, changed, {"CSRMARK"}, "handoff")["passed"])

    def test_guard_detects_loss_of_an_unmarked_item_and_slot_changes(self):
        before = evidence()
        other = deepcopy(before["party"][0]["items"][0])
        other["resref"] = "OTHER"
        before["party"][0]["items"].append(other)
        after = deepcopy(before)
        after["globals"].update(CSR_ENDING_USED=1, CSR_ENDING_FAILED=1)
        self.assertTrue(compare(before, after, {"CSRMARK"}, "guard")["passed"])
        after["party"][0]["items"].pop()
        self.assertFalse(compare(before, after, {"CSRMARK"}, "guard")["passed"])
        after = deepcopy(before)
        after["globals"].update(CSR_ENDING_USED=1, CSR_ENDING_FAILED=1)
        after["party"][0]["items"][0]["slots"] = ["quick1"]
        self.assertFalse(compare(before, after, {"CSRMARK"}, "guard")["passed"])

    def test_destination_bank_is_counted_but_preexisting_marker_is_not_delivery(self):
        before, after = evidence(), evidence("AR0602")
        after["globals"].update(CSR_ENDING_USED=1, BD_PLOT=700)
        bank = {"items": deepcopy(after["party"][0]["items"])}
        after["areas"]["AR0602"]["containers"].append(bank)
        after["party"][0]["items"].clear()
        self.assertTrue(compare(before, after, {"CSRMARK"}, "handoff")["passed"])
        before["areas"]["AR0602"]["containers"].append(deepcopy(bank))
        self.assertFalse(compare(before, after, {"CSRMARK"}, "handoff")["passed"])

    def test_empty_marker_set_and_missing_bag_do_not_vacuously_pass(self):
        before, after = evidence(), evidence("AR0602")
        after["globals"].update(CSR_ENDING_USED=1, BD_PLOT=700)
        self.assertFalse(compare(before, after, set(), "handoff")["passed"])
        self.assertFalse(compare(before, after, {"CSRMARK"}, "handoff", ("BAG01",))["passed"])


if __name__ == "__main__":
    unittest.main()
