"""Real WeiDU checks for the bridge's bounded day/night art-record replacement."""
from __future__ import annotations

from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib
import hashlib
import json

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'research/scripts'))
from test_comp291_installer import ROOT, WEIDU, tree, write_fake_game


CELLS = tuple(y * 80 + x for y in range(27, 31) for x in range(18, 25))
DOOR_CELLS = (2261, 2262, 2341, 2342)
ALTERNATES = dict(zip(DOOR_CELLS, range(4882, 4886)))


def wed(name='BD2000'):
    ov, door, doorcells, tilemap = 32, 80, 106, 114
    lookup = tilemap + 48000
    data = bytearray(lookup + 9600)
    data[:8] = b'WED V1.3'
    struct.pack_into('<6I', data, 8, 2, 1, ov, 0, door, doorcells)
    struct.pack_into('<HH8sHHII', data, ov, 80, 60, name.encode(), 4800, 0, tilemap, lookup)
    struct.pack_into('<HH8sHHII', data, ov+24, 80, 60, b'WATER', 0, 0, 0, 0)
    struct.pack_into('<8sHHHHHII', data, door, b'DOOR07', 1, 0, 4, 0, 0, 0, 0)
    struct.pack_into('<4H', data, doorcells, *DOOR_CELLS)
    for cell in range(4800):
        struct.pack_into('<HHHBBH', data, tilemap+10*cell,
                         cell, 1, ALTERNATES.get(cell, 65535), 0, 0, 0)
        struct.pack_into('<H', data, lookup+2*cell, cell)
    return bytes(data)


def tis(stride=12):
    count = 4890
    if stride == 12:
        tiles = b''.join(struct.pack('<III', 54, (i % 16)*64, (i // 16 % 16)*64)
                         for i in range(count))
    else:
        tiles = bytes(range(256)) * 20 * count
    return (struct.pack('<8s4I', b'TIS V1  ', count, stride, 24, 64) + tiles
            + b'FOREIGN_TRAILING_BYTES')


def palette(tag):
    # Includes NUL and percent bytes to catch accidental text interpretation.
    return b''.join(bytes((slot + n + ord(tag)) % 256 for n in range(5120))
                    for slot in range(28))


class PackagedBridgeArtTests(unittest.TestCase):
    def test_packaged_formats_match_hashes_dimensions_and_water_coverage(self):
        art = ROOT/'chriz-sod-remix/art/bridge'
        manifest = json.loads((art/'manifest.json').read_text())
        masks = []
        for tag, label in (('D', 'day'), ('N', 'night')):
            page = (art/f'CSR256{tag}.PVRZ').read_bytes()
            pal = (art/f'CSR256{tag}.PAL').read_bytes()
            self.assertEqual(hashlib.sha256(page).hexdigest(), manifest[label]['pvrz_sha256'])
            self.assertEqual(hashlib.sha256(pal).hexdigest(), manifest[label]['palette_sha256'])
            pvr = zlib.decompress(page[4:])
            self.assertEqual(struct.unpack_from('<I', page)[0], len(pvr))
            self.assertEqual(struct.unpack_from('<IIQ9I', pvr),
                             (0x03525650, 0, 7, 0, 0, 256, 512, 1, 1, 1, 1, 0))
            self.assertEqual(len(pvr), 65588)
            self.assertEqual(len(pal), 143360)
            # Decode BC1 transparency using only stdlib, so normal CI does not
            # need Pillow. A mismatched mask would cover the animated water.
            mask = bytearray(512*256)
            for block in range(128*64):
                c0, c1, indices = struct.unpack_from('<HHI', pvr, 52+block*8)
                bx, by = block % 128 * 4, block // 128 * 4
                for pixel in range(16):
                    invisible = c0 <= c1 and (indices >> (pixel*2)) & 3 == 3
                    mask[(by+pixel//4)*512+bx+pixel%4] = 0 if invisible else 255
            for slot in range(28):
                indices = pal[slot*5120+1024:(slot+1)*5120]
                for pixel, index in enumerate(indices):
                    x, y = slot % 7 * 64 + pixel % 64, slot // 7 * 64 + pixel // 64
                    self.assertEqual(mask[y*512+x], 255 if index else 0)
            self.assertTrue(all(mask[y*512+x] == 0 for y in range(256) for x in range(448, 512)))
            self.assertIn(0, mask)
            self.assertIn(255, mask)
            masks.append(mask)
        self.assertEqual(masks[0], masks[1], 'Day and night coverage must use the same bridge silhouette')


@unittest.skipUnless(WEIDU.is_file(), 'real WeiDU unavailable; set WEIDU_EXE')
class Component256VisualsTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix='csr256-art-')
        self.addCleanup(temp.cleanup)
        self.game = Path(temp.name)
        write_fake_game(self.game)
        (self.game/"weidu.log").write_text("")
        self.override = self.game/'override'
        (self.game/'chriz-sod-remix/lib').mkdir(parents=True)
        shutil.copy2(ROOT/'chriz-sod-remix/lib/comp256_visuals.tpa',
                     self.game/'chriz-sod-remix/lib/comp256_visuals.tpa')
        self.art = self.game/'chriz-sod-remix/art/bridge'
        self.art.mkdir(parents=True)
        for tag in ('D', 'N'):
            (self.art/f'csr256{tag.lower()}.pal').write_bytes(palette(tag))
            (self.art/f'csr256{tag.lower()}.pvrz').write_bytes(struct.pack('<I', 65588) + zlib.compress(b'fixture'*100))
        self.write('BD2000.WED', wed())
        self.write('BD2000N.WED', wed('BD2000N'))
        self.write('BD2000.TIS', tis())
        self.write('BD2000N.TIS', tis())
        self.write('BD2000.ARE', b'IMMUTABLE_DOOR_FLAGS_AND_SEARCH_GEOMETRY')
        self.write('OTHER.WED', b'IMMUTABLE_OTHER_AREA')
        (self.game/'repair.tp2').write_text('''BACKUP ~repair-backup~
AUTHOR ~fixture~
BEGIN ~production256 art harness~ DESIGNATED 256
INCLUDE ~chriz-sod-remix/lib/comp256_visuals.tpa~
LAF csr256_visuals_preflight END
LAF csr256_visuals_install END
''')

    def write(self, name, data):
        (self.override/name.lower()).write_bytes(data)

    def run_install(self):
        return subprocess.run([str(WEIDU), 'repair.tp2', '--force-install-list', '256',
                               '--game', str(self.game), '--language', '0',
                               '--use-lang', 'en_US', '--no-exit-pause'],
                              cwd=self.game, capture_output=True, text=True, timeout=90)

    def install_ok(self):
        result = self.run_install()
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertNotIn('WARNING', (result.stdout+result.stderr).upper())
        return result

    def primary(self, cell, name='bd2000'):
        data = (self.override/(name+'.wed')).read_bytes()
        ov = struct.unpack_from('<I', data, 16)[0]
        tm, lut = struct.unpack_from('<II', data, ov+16)
        first = struct.unpack_from('<H', data, tm+cell*10)[0]
        return struct.unpack_from('<H', data, lut+first*2)[0]

    def assert_tile(self, index, slot, name='bd2000'):
        data = (self.override/(name+'.tis')).read_bytes()
        self.assertEqual(struct.unpack_from('<III', data, 24+index*12),
                         (90, slot%7*64, slot//7*64))

    def check_replacement(self, stride):
        for name in ('BD2000.TIS', 'BD2000N.TIS'):
            self.write(name, tis(stride))
        before = {p.name.upper(): p.read_bytes() for p in self.override.iterdir()}
        tlk = (self.game/'lang/en_us/dialog.tlk').read_bytes()
        result = self.run_install()
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertIn('SUCCESSFULLY INSTALLED', result.stdout)
        self.assertFalse((self.game/'-').exists(), 'No temporary resource copy belongs in the game root')
        for name, tag in (('BD2000', 'D'), ('BD2000N', 'N')):
            expected = bytearray(before[name+'.TIS'])
            pal = palette(tag)
            for slot, cell in enumerate(CELLS):
                replacement = (struct.pack('<III', 90, slot % 7 * 64, slot // 7 * 64)
                               if stride == 12 else pal[slot*5120:(slot+1)*5120])
                targets = [cell] + ([ALTERNATES[cell]] if cell in ALTERNATES else [])
                for target in targets:
                    expected[24+target*stride:24+(target+1)*stride] = replacement
            self.assertEqual((self.override/(name+'.tis').lower()).read_bytes(), expected)
        for name, data in before.items():
            if not name.endswith('.TIS'):
                self.assertEqual((self.override/name.lower()).read_bytes(), data, name)
        self.assertEqual((self.game/'lang/en_us/dialog.tlk').read_bytes(), tlk)
        self.assertEqual(sorted(p.name.upper() for p in self.override.iterdir()
                                if p.suffix.lower() == '.pvrz'),
                         ['B200090.PVRZ', 'B2000N90.PVRZ'] if stride == 12 else [])
        if stride == 12:
            for page, tag in (('B200090', 'D'), ('B2000N90', 'N')):
                self.assertEqual((self.override/(page+'.pvrz').lower()).read_bytes(),
                                 (self.art/f'csr256{tag.lower()}.pvrz').read_bytes())

    def test_pvrz_tis_changes_only_32_records_and_leaves_door_and_water_geometry(self):
        self.check_replacement(12)

    def test_palette_tis_changes_only_32_binary_records_without_texture_pages(self):
        self.check_replacement(5120)

    def test_foreign_night_page_is_overwritten(self):
        self.write('B2000N90.PVRZ', b'FOREIGN_PAGE')
        self.install_ok()
        self.assertEqual((self.override/'b2000n90.pvrz').read_bytes(),
                         (self.art/'csr256n.pvrz').read_bytes())

    def test_existing_page_reference_does_not_gate_owned_art(self):
        data = bytearray(tis())
        struct.pack_into('<I', data, 24, 90)
        self.write('BD2000.TIS', data)
        self.install_ok()
        self.assertEqual((self.override/'bd2000.tis').read_bytes()[24:36], data[24:36])
        self.assert_tile(self.primary(CELLS[0]), 0)

    def test_remapped_closed_tile_is_written(self):
        data = bytearray(wed())
        struct.pack_into('<H', data, 114+2261*10+4, 4881)
        self.write('BD2000.WED', data)
        self.install_ok()
        self.assert_tile(4881, 10)

    def test_shared_tile_is_isolated_and_other_cell_preserved(self):
        data = bytearray(wed())
        struct.pack_into('<H', data, 114+48000, 2258)
        self.write('BD2000.WED', data)
        original = tis()[24+2258*12:24+2259*12]
        self.install_ok()
        self.assertEqual(self.primary(0), 2258)
        chosen = self.primary(2258)
        self.assertGreaterEqual(chosen, 4890)
        self.assert_tile(chosen, 7)
        self.assertEqual((self.override/'bd2000.tis').read_bytes()[24+2258*12:24+2259*12], original)

    def test_changed_door_cell_receives_owned_closed_art(self):
        data = bytearray(wed())
        struct.pack_into('<H', data, 106, 2260)
        self.write('BD2000.WED', data)
        self.install_ok()
        result = (self.override/'bd2000.wed').read_bytes()
        alternate = struct.unpack_from('<H', result, 114+2260*10+4)[0]
        self.assert_tile(alternate, 10)

    def test_absent_night_only_omits_night_art(self):
        (self.override/'bd2000n.wed').unlink()
        before = (self.override/'bd2000n.tis').read_bytes()
        self.install_ok()
        self.assert_tile(self.primary(CELLS[0]), 0)
        self.assertEqual((self.override/'bd2000n.tis').read_bytes(), before)

    def test_truncated_day_table_only_omits_day_art(self):
        self.write('BD2000.TIS', tis()[:30])
        before = (self.override/'bd2000.wed').read_bytes()
        self.install_ok()
        self.assertEqual((self.override/'bd2000.wed').read_bytes(), before)
        self.assertEqual((self.override/'bd2000.tis').read_bytes(), tis()[:30])
        self.assert_tile(self.primary(CELLS[0], 'bd2000n'), 0, 'bd2000n')

    def test_missing_and_extra_primary_frames_write_owned_static_art(self):
        data = bytearray(wed())
        struct.pack_into('<H', data, 114+CELLS[0]*10+2, 0)
        struct.pack_into('<H', data, 114+CELLS[1]*10+2, 2)
        self.write('BD2000.WED', data)
        self.install_ok()
        for slot in (0, 1): self.assert_tile(self.primary(CELLS[slot]), slot)

    def test_different_base_width_uses_coordinates(self):
        data = bytearray(wed())
        struct.pack_into('<H', data, 32, 79)
        self.write('BD2000.WED', data)
        self.install_ok()
        self.assert_tile(self.primary(27*79+18), 0)

    def test_small_base_grid_is_extended_for_the_owned_rectangle(self):
        data = bytearray(wed())
        struct.pack_into('<HH', data, 32, 20, 20)
        struct.pack_into('<I', data, 12, 0)
        self.write('BD2000.WED', data)
        self.install_ok()
        result = (self.override/'bd2000.wed').read_bytes()
        self.assertEqual(struct.unpack_from('<HH', result, 32), (25, 31))
        self.assert_tile(self.primary(27*25+18), 0)

    def test_other_overlay_sharing_the_tileset_keeps_its_records(self):
        data = bytearray(wed())
        data[56:80] = data[32:56]
        self.write('BD2000.WED', data)
        before = tis()[24+CELLS[0]*12:24+(CELLS[0]+1)*12]
        self.install_ok()
        self.assert_tile(self.primary(CELLS[0]), 0)
        result = (self.override/'bd2000.tis').read_bytes()
        self.assertEqual(result[24+CELLS[0]*12:24+(CELLS[0]+1)*12], before)

    def test_second_tail_execution_is_byte_identical(self):
        self.install_ok()
        before = tree(self.override)
        (self.game/'second.tp2').write_text((self.game/'repair.tp2').read_text().replace('repair-backup','second-backup'))
        result = subprocess.run([str(WEIDU), 'second.tp2', '--force-install-list', '256',
                                 '--game', str(self.game), '--use-lang', 'en_US', '--no-exit-pause'],
                                cwd=self.game, capture_output=True, text=True, timeout=90)
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertEqual(tree(self.override), before)


if __name__ == '__main__':
    unittest.main()
