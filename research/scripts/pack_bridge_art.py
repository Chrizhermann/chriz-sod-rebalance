"""Encode approved ImageGen bridge edits as bounded Infinity Engine tile assets.

This is format conversion, not an image editor. The edits must already have been
made and reviewed with ImageGen. Original source crops supply only the engine's
binary coverage mask, preserving the bridge silhouette above animated water.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import struct
import zlib

from PIL import Image


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encode(source_path: Path, edit_path: Path, output: Path, tag: str):
    source = Image.open(source_path).convert('RGBA')
    if source.size != (640, 704):
        raise ValueError('Expected the audited source crop at world (1088,1600), size 640x704')
    edited = Image.open(edit_path).convert('RGB')
    # ImageGen may upscale the reference. Return it to the game's fixed pixel
    # dimensions before slicing the exact 7x4 tile rectangle.
    edited = edited.resize(source.size, Image.Resampling.LANCZOS)
    patch = edited.crop((64, 128, 512, 384)).convert('RGBA')
    mask = source.getchannel('A').crop((64, 128, 512, 384))
    if any(value not in (0, 255) for value in set(mask.tobytes())):
        raise ValueError('The source silhouette must be the original binary TIS coverage mask')
    patch.putalpha(mask)
    page = Image.new('RGBA', (512, 256), (0, 0, 0, 0))
    page.paste(patch, (0, 0))
    dds = io.BytesIO()
    page.save(dds, format='DDS', pixel_format='DXT1')
    blocks = dds.getvalue()[128:]
    if len(blocks) != 65536:
        raise ValueError('Unexpected DXT1 payload size')
    decoded = Image.frombytes('RGBA', page.size, blocks, 'bcn', 1)
    if decoded.getchannel('A').tobytes() != page.getchannel('A').tobytes():
        raise ValueError('DXT1 conversion changed the engine coverage mask')
    pvr = struct.pack('<IIQ9I', 0x03525650, 0, 7, 0, 0, 256, 512, 1, 1, 1, 1, 0) + blocks
    (output/f'CSR256{tag}.PVRZ').write_bytes(struct.pack('<I', len(pvr)) + zlib.compress(pvr, 9))
    palette_tiles = bytearray()
    for y in range(4):
        for x in range(7):
            tile = patch.crop((x*64, y*64, (x+1)*64, (y+1)*64))
            indexed = tile.convert('RGB').quantize(colors=255, method=Image.Quantize.MEDIANCUT)
            rgb = indexed.getpalette()
            pal = bytearray(1024)  # Index zero is the engine's transparent color.
            for index in range(255):
                r, g, b = rgb[index*3:index*3+3]
                pal[(index+1)*4:(index+2)*4] = bytes((b, g, r, 0))
            pixels = bytes(value+1 if alpha else 0 for value, alpha in
                           zip(indexed.tobytes(), tile.getchannel('A').tobytes()))
            palette_tiles += pal + pixels
    if len(palette_tiles) != 143360:
        raise ValueError('Unexpected palette tile pack size')
    (output/f'CSR256{tag}.PAL').write_bytes(palette_tiles)
    return {'source_sha256': digest(source_path), 'edit_sha256': digest(edit_path),
            'pvrz_sha256': digest(output/f'CSR256{tag}.PVRZ'),
            'palette_sha256': digest(output/f'CSR256{tag}.PAL')}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('source-day', 'source-night', 'edit-day', 'edit-night', 'output'):
        parser.add_argument('--'+name, type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    result = {'world_rectangle': [1152, 1728, 1600, 1984],
              'tile_columns_inclusive': [18, 24], 'tile_rows_inclusive': [27, 30],
              'day': encode(args.source_day, args.edit_day, args.output, 'D'),
              'night': encode(args.source_night, args.edit_night, args.output, 'N')}
    (args.output/'manifest.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
