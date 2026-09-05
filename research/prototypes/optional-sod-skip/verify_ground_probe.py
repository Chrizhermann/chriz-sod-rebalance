"""Read-only verification of the two native ground-pile probe saves.

This never opens the game, writes a save, or extracts files onto disk.
Format: https://gibberlings3.github.io/iesdp/file_formats/ie_formats/sav_v1.htm
"""

import argparse
from collections import Counter
import json
from pathlib import Path
import struct
import zlib


def checked(data, offset, size):
    if offset < 0 or size < 0 or offset + size > len(data):
        raise ValueError("truncated or out-of-bounds resource section")
    return data[offset:offset + size]


def number(data, offset, kind="I"):
    size = struct.calcsize("<" + kind)
    return struct.unpack("<" + kind, checked(data, offset, size))[0]


def read_probe_areas(data):
    if checked(data, 0, 8) != b"SAV V1.0":
        raise ValueError("not a SAV V1.0 archive")
    pos = 8
    found = {}
    while pos < len(data):
        length = number(data, pos)
        pos += 4
        if not 1 <= length <= 260:
            raise ValueError("invalid archive filename length")
        raw_name = checked(data, pos, length)
        if raw_name[-1:] != b"\0":
            raise ValueError("archive filename is not terminated")
        name = raw_name[:-1].decode("ascii").casefold()
        pos += length
        raw_length, compressed_length = number(data, pos), number(data, pos + 4)
        pos += 8
        payload = checked(data, pos, compressed_length)
        pos += compressed_length
        if name not in ("csrgp001.are", "csrgp002.are"):
            continue
        if name in found or raw_length > 16 * 1024 * 1024:
            raise ValueError("duplicate or oversized probe area")
        unpacker = zlib.decompressobj()
        area = unpacker.decompress(payload, raw_length + 1)
        if len(area) != raw_length or not unpacker.eof or unpacker.unused_data:
            raise ValueError("probe area compression/length mismatch")
        found[name] = area
    if set(found) != {"csrgp001.are", "csrgp002.are"}:
        raise ValueError("save must contain both visited probe rooms")
    return found


def containers(data):
    if checked(data, 0, 8) != b"AREAV1.0":
        raise ValueError("not an ARE V1.0 resource")
    offset, count = number(data, 0x70), number(data, 0x74, "H")
    items, item_count = number(data, 0x78), number(data, 0x76, "H")
    checked(data, offset, count * 0xC0)
    checked(data, items, item_count * 20)
    result = []
    for index in range(count):
        pos = offset + index * 0xC0
        first, length = number(data, pos + 0x40), number(data, pos + 0x44)
        if first + length > item_count:
            raise ValueError("container item range exceeds the item table")
        result.append({
            "name": checked(data, pos, 32).split(b"\0")[0].decode("ascii"),
            "type": number(data, pos + 0x24, "H"),
            "x": number(data, pos + 0x20, "H"),
            "y": number(data, pos + 0x22, "H"),
            "items": [checked(data, items + i * 20, 8).split(b"\0")[0].decode("ascii").lower()
                      for i in range(first, first + length)],
        })
    return result


def verify(data, stage):
    if stage not in ("copy", "bank"):
        raise ValueError("unknown verification stage")
    areas = read_probe_areas(data)
    source, target = (containers(areas[name]) for name in ("csrgp001.are", "csrgp002.are"))
    errors = []

    def expect(rows, name, items, kind=None, optional_empty=False):
        matches = [c for c in rows if c["name"].lower() == name.lower()]
        if not matches and optional_empty and not items:
            return
        if len(matches) != 1:
            errors.append(f"{name}: expected exactly one named container, found {len(matches)}")
            return
        container = matches[0]
        if Counter(container["items"]) != Counter(items):
            errors.append(f"{name}: expected {items}, found {container['items']}")
        if kind is not None and container["type"] != kind:
            errors.append(f"{name}: wrong container type {container['type']}")

    expect(source, "CSRSourceA", ["csrgpa"], 4)
    expect(source, "CSRSourceB", ["csrgpb"], 4)
    expect(source, "CSRSourceControl", ["csrgpc"], 2)
    expect(target, "CSRTargetControl", ["csrgpd"], 2)
    copied = ["csrgpa", "csrgpb"]
    expect(target, "CSRBG1PILE", copied if stage == "copy" else [], 4, stage == "bank")
    expect(target, "CSRProbeBank", [] if stage == "copy" else copied, 2)
    for name, rows, expected in (("source", source, ["csrgpa", "csrgpb", "csrgpc"]),
                                 ("target", target, ["csrgpa", "csrgpb", "csrgpd"])):
        actual = Counter(item for container in rows for item in container["items"])
        if actual != Counter(expected):
            errors.append(f"{name}: missing/duplicate/unrelated items: {dict(actual)}")
    return {"stage": stage, "passed": not errors, "errors": errors,
            "source": source, "target": target}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("save", type=Path, help="BALDUR.SAV from the disposable probe")
    parser.add_argument("--stage", choices=("copy", "bank"), required=True)
    args = parser.parse_args()
    try:
        report = verify(args.save.read_bytes(), args.stage)
    except (ValueError, OSError, UnicodeError, zlib.error) as error:
        report = {"passed": False, "errors": [str(error)]}
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
