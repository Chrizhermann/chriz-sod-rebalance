"""Bounds cases that must not silently produce an incomplete loot screen."""
import struct
import unittest

from audit_filler_loot import container_rows, placed_creatures


class LootBoundsTests(unittest.TestCase):
    def test_empty_inventory_and_truncated_header(self):
        raw = bytearray(0xC4)
        raw[:8] = b'AREAV1.0'
        self.assertEqual(container_rows(raw, 'TEST'), [])
        self.assertEqual(placed_creatures(raw), {})
        with self.assertRaises(ValueError):
            container_rows(raw[:-1], 'TEST')

    def test_container_run_cannot_escape_shared_item_table(self):
        raw = bytearray(0x200 + 0xC0 + 20)
        raw[:8] = b'AREAV1.0'
        struct.pack_into('<IHHI', raw, 0x70, 0x200, 1, 1, 0x2C0)
        struct.pack_into('<II', raw, 0x240, 1, 1)
        with self.assertRaisesRegex(ValueError, 'exceeds item table'):
            container_rows(raw, 'TEST')

    def test_embedded_cre_is_bounded_and_does_not_use_external_template(self):
        raw = bytearray(0x200 + 0x110 + 8)
        raw[:8] = b'AREAV1.0'
        struct.pack_into('<I', raw, 0x54, 0x200)
        struct.pack_into('<H', raw, 0x58, 1)
        struct.pack_into('<I', raw, 0x240, 0xFFFFFF)
        raw[0x280:0x288] = b'EXTERNAL'
        struct.pack_into('<II', raw, 0x288, 0x310, 8)
        raw[0x310:] = b'CRE V1.0'
        templates = placed_creatures(raw)
        self.assertEqual(templates['actor:0:EXTERNAL']['embedded'], b'CRE V1.0')
        struct.pack_into('<I', raw, 0x28C, 9)
        with self.assertRaises(ValueError):
            placed_creatures(raw)


if __name__ == '__main__':
    unittest.main()
