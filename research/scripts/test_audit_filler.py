"""Focused bounds and schedule/field regression checks for the census."""
import struct
import unittest

from audit_filler import VerificationError, area, creature, creation_calls, schedule


class CensusParsingTests(unittest.TestCase):
    def test_creation_at_location_uses_third_argument(self):
        calls = creation_calls('CreateCreatureAtLocation("location","GLOBAL","wolf")\n'
                               'ActionOverride("actor",CreateCreatureObject("ghoul",Myself,0,0,0))')
        self.assertEqual([c["cre_or_group"] for c in calls], ["WOLF", "GHOUL"])
        self.assertEqual([c["line"] for c in calls], [1, 2])
        group = creation_calls('CreateRandomCreature("PACK",[1.2],0)')[0]
        self.assertEqual((group["reference_kind"], group["cre_or_group"]), ("group", "PACK"))
        with self.assertRaisesRegex(VerificationError, "unhandled creation action"):
            creation_calls('CreateCreatureUnverified("CRE")')

    def fixture(self):
        raw = bytearray(0x200 + 0x110 + 0xC8 + 0xAC)
        raw[:8] = b"AREAV1.0"
        struct.pack_into("<I", raw, 0x54, 0x200)
        struct.pack_into("<H", raw, 0x58, 1)
        struct.pack_into("<I", raw, 0x60, 0x310)
        struct.pack_into("<I", raw, 0x64, 1)
        struct.pack_into("<I", raw, 0xC0, 0x3D8)
        return raw

    def test_actor_schedule_uses_only_24_hours(self):
        self.assertEqual(schedule(0)["scheduled_hours"], 0)
        self.assertEqual(schedule(0xFFFFFFFF)["scheduled_hours"], 24)
        self.assertEqual(schedule(0xFF000000)["schedule_active"], 0)
        self.assertEqual(schedule((1 << 6) | (1 << 23))["hours"], "6|23")
        raw = self.fixture()
        struct.pack_into("<I", raw, 0x240, 0xFF000000)
        self.assertEqual(area(raw, "TEST")["actors"][0]["schedule_active"], 0)

    def test_spawn_fields_use_primary_offsets_and_schedule(self):
        raw = self.fixture()
        raw[0x334:0x33C] = b"CREATURE"
        struct.pack_into("<H", raw, 0x310 + 0x74, 1)
        struct.pack_into("<H", raw, 0x310 + 0x84, 5)
        struct.pack_into("<H", raw, 0x310 + 0x86, 1)
        struct.pack_into("<I", raw, 0x310 + 0x88, 1 << 17)
        struct.pack_into("<H", raw, 0x310 + 0xAC, 99)
        struct.pack_into("<H", raw, 0x310 + 0xB4, 88)
        point = area(raw, "TEST")["spawn_points"][0]
        self.assertEqual((point["max_spawn"], point["enabled"], point["hours"]), (5, 1, "17"))
        self.assertEqual(point["configured_and_scheduled"], 1)
        struct.pack_into("<H", raw, 0x310 + 0x74, 0)
        self.assertEqual(area(raw, "TEST")["spawn_points"][0]["configured_and_scheduled"], 0)

    def test_rejects_truncated_tables_and_oversized_spawn_count(self):
        raw = self.fixture()
        with self.assertRaises(VerificationError):
            area(raw[:-1], "TEST")
        struct.pack_into("<I", raw, 0x64, 999)
        with self.assertRaises(VerificationError):
            area(raw, "TEST")
        raw = self.fixture()
        struct.pack_into("<H", raw, 0x310 + 0x74, 11)
        with self.assertRaises(VerificationError):
            area(raw, "TEST")

    def test_embedded_cre_bounds_and_xp_reward(self):
        raw = self.fixture()
        struct.pack_into("<II", raw, 0x200 + 0x88, len(raw) - 1, 2)
        with self.assertRaises(VerificationError):
            area(raw, "TEST")
        cre = bytearray(0x2D4)
        cre[:8] = b"CRE V1.0"
        struct.pack_into("<II", cre, 0x14, 1100, 999999)
        cre[0x270] = 255
        self.assertEqual(creature(cre)["kill_xp"], 1100)
        self.assertEqual(creature(cre)["ea"], 255)
        struct.pack_into("<II", cre, 0x2BC, len(cre) - 1, 1)
        with self.assertRaises(VerificationError):
            creature(cre)


if __name__ == "__main__":
    unittest.main()
