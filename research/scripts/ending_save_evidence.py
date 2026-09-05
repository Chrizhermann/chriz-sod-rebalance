#!/usr/bin/env python3
"""Read-only persisted evidence for the component-290 runtime matrix.

Examples (redirect stdout to preserve JSON outside the save directory):
  python ending_save_evidence.py snapshot SAVE_DIRECTORY
  python ending_save_evidence.py compare BEFORE AFTER --mode handoff --markers MISC01 MISC02
  python ending_save_evidence.py compare BEFORE AFTER --mode guard --markers MISC01

Only explicit ordinary marker resrefs are compared: this does not predict EET's
named-item sweeps or count every item as import-eligible. Handoff compares the
pre-handoff party with the destination-area party and containers. Guard compares
each party member's inventory including slots. --bag-stores names saved STO
resources to compare separately; a STO alone cannot prove which carried bag opens
it. Bag association and transient area/movie/control observations need runtime
evidence. A serialized BD6100 ARE does not prove the party visited it.

Format references: https://gibberlings3.github.io/iesdp/file_formats/ie_formats/
gam_v2.0.htm, cre_v1.htm, are_v1.htm, sto_v1.htm, sav_v1.htm.
Uses only the standard library; never writes game files, saves, or extracted data.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import struct
import sys
from typing import Any
import zlib


AREAS = ("BD4300", "BD6100", "AR0602")
WATCH_GLOBALS = (
    "BD_PLOT", "CSR_ENDING_USED", "CSR_ENDING_FAILED", "BD_CORWINROMANCE6",
    "BD_NEERAROMANCE6", "BD_NEERA_ROMANCEACTIVE", "BD_CORWIN_ROMANCEACTIVE",
    "ENDOFBG1", "K#IMPORTGOLD",
)
SLOT_NAMES = (
    "helmet", "armor", "shield", "gloves", "left_ring", "right_ring", "amulet",
    "belt", "boots", "weapon1", "weapon2", "weapon3", "weapon4", "quiver1",
    "quiver2", "quiver3", "quiver4", "cloak", "quick1", "quick2", "quick3",
    *(f"backpack{i}" for i in range(1, 17)), "magic_weapon",
)


def checked(data: bytes, offset: int, size: int) -> bytes:
    if offset < 0 or size < 0 or offset + size > len(data):
        raise ValueError(f"section {offset:#x}+{size:#x} exceeds resource size {len(data):#x}")
    return data[offset:offset + size]


def number(data: bytes, offset: int, kind: str = "I") -> int:
    return struct.unpack("<" + kind, checked(data, offset, struct.calcsize("<" + kind)))[0]


def text(data: bytes, offset: int, length: int) -> str:
    return checked(data, offset, length).split(b"\0", 1)[0].decode("latin-1")


def signature(data: bytes, expected: bytes) -> None:
    if checked(data, 0, 8) != expected:
        raise ValueError(f"expected {expected!r}, found {data[:8]!r}")


def item(data: bytes, offset: int) -> dict[str, Any]:
    checked(data, offset, 20)
    return {
        "resref": text(data, offset, 8).upper(),
        "expiration": number(data, offset + 8, "H"),
        "charges": [number(data, offset + x, "H") for x in (10, 12, 14)],
        "flags": number(data, offset + 16),
    }


def parse_cre(data: bytes) -> dict[str, Any]:
    signature(data, b"CRE V1.0")
    checked(data, 0, 0x2D4)
    offset, count = number(data, 0x2BC), number(data, 0x2C0)
    slots = number(data, 0x2B8)
    checked(data, offset, count * 20)
    checked(data, slots, 80)
    items = [dict(item(data, offset + i * 20), index=i, slots=[]) for i in range(count)]
    # Last two words are selected weapon and ability, not item-table indices.
    for slot, name in enumerate(SLOT_NAMES):
        index = number(data, slots + slot * 2, "H")
        if index == 0xFFFF:
            continue
        if index >= count:
            raise ValueError(f"CRE {name} slot references item {index}, table has {count}")
        items[index]["slots"].append(name)
    return {
        "death_variable": text(data, 0x280, 32),
        "state_flags": number(data, 0x20),
        "hp": number(data, 0x24, "h"),
        "max_hp": number(data, 0x26, "h"),
        "selected_weapon": number(data, slots + 76, "H"),
        "selected_weapon_ability": number(data, slots + 78, "H"),
        "items": items,
    }


def parse_gam(data: bytes) -> dict[str, Any]:
    if checked(data, 0, 8) not in (b"GAMEV2.0", b"GAMEV2.1"):
        raise ValueError(f"unsupported GAM signature {data[:8]!r}")
    checked(data, 0, 0xB4)
    party_offset, party_count = number(data, 0x20), number(data, 0x24)
    if not 1 <= party_count <= 6:
        raise ValueError(f"expected 1-6 saved party members, found {party_count}")
    checked(data, party_offset, party_count * 0x160)
    party = []
    for i in range(party_count):
        pos = party_offset + i * 0x160
        cre = checked(data, number(data, pos + 4), number(data, pos + 8))
        party.append({
            "record_index": i, "party_order": number(data, pos + 2, "H"),
            "selection_flags": number(data, pos, "H"),
            "name": text(data, pos + 0xC0, 32),
            "character_resref": text(data, pos + 0x0C, 8),
            "area": text(data, pos + 0x18, 8).upper(),
            "x": number(data, pos + 0x20, "H"), "y": number(data, pos + 0x22, "H"),
            **parse_cre(cre),
        })
    orders = [pc["party_order"] for pc in party]
    if len(set(orders)) != len(orders) or any(order > 5 for order in orders):
        raise ValueError(f"invalid/duplicate saved party orders {orders}")
    globals_offset, globals_count = number(data, 0x38), number(data, 0x3C)
    checked(data, globals_offset, globals_count * 84)
    variables = {}
    for i in range(globals_count):
        pos = globals_offset + i * 84
        name = text(data, pos, 32).upper()
        if name in variables:
            raise ValueError(f"duplicate GLOBAL variable {name}")
        variables[name] = number(data, pos + 0x28, "i")
    active = number(data, 0x1C, "h")
    current = text(data, 0x58, 8).upper()
    if active != -1:
        matches = [pc for pc in party if pc["party_order"] == active]
        if len(matches) != 1:
            raise ValueError(f"active-area player index {active} has no unique party record")
        effective = matches[0]["area"]
    else:
        effective = current
    return {
        "gam_signature": data[:8].decode("ascii"), "game_time_units": number(data, 8),
        "real_time_seconds": number(data, 0x74), "party_gold": number(data, 0x18),
        "campaign": text(data, 0x94, 8), "master_area": text(data, 0x40, 8).upper(),
        "header_current_area": current, "active_area_party_order": active,
        "effective_current_area": effective, "party": party, "globals": variables,
        "watch_globals": {name: variables.get(name, 0) for name in WATCH_GLOBALS},
    }


def read_sav(data: bytes) -> dict[str, bytes]:
    signature(data, b"SAV V1.0")
    pos, files = 8, {}
    while pos < len(data):
        length = number(data, pos)
        pos += 4
        if not 1 <= length <= 260:
            raise ValueError(f"invalid SAV filename length {length}")
        raw_name = checked(data, pos, length)
        pos += length
        if raw_name[-1:] != b"\0" or b"\0" in raw_name[:-1]:
            raise ValueError("invalid SAV filename terminator")
        name = raw_name[:-1].decode("ascii").upper()
        if name in files:
            raise ValueError(f"duplicate SAV resource {name}")
        raw_size, compressed_size = number(data, pos), number(data, pos + 4)
        pos += 8
        compressed = checked(data, pos, compressed_size)
        pos += compressed_size
        if raw_size > 256 * 1024 * 1024:
            raise ValueError(f"unreasonably large SAV resource {name}")
        decompressor = zlib.decompressobj()
        value = decompressor.decompress(compressed, raw_size + 1)
        if (len(value) != raw_size or not decompressor.eof
                or decompressor.unused_data or decompressor.unconsumed_tail):
            raise ValueError(f"SAV decompression/size mismatch for {name}")
        files[name] = value
    return files


def parse_are(data: bytes) -> list[dict[str, Any]]:
    signature(data, b"AREAV1.0")
    checked(data, 0, 0xF4)
    offset, count = number(data, 0x70), number(data, 0x74, "H")
    item_offset, item_count = number(data, 0x78), number(data, 0x76, "H")
    checked(data, offset, count * 0xC0)
    checked(data, item_offset, item_count * 20)
    containers = []
    for i in range(count):
        pos = offset + i * 0xC0
        first, length = number(data, pos + 0x40), number(data, pos + 0x44)
        if first + length > item_count:
            raise ValueError(f"ARE container {i} item run exceeds table")
        containers.append({
            "index": i, "name": text(data, pos, 32),
            "type": number(data, pos + 0x24, "H"),
            "x": number(data, pos + 0x20, "H"), "y": number(data, pos + 0x22, "H"),
            "items": [item(data, item_offset + j * 20) for j in range(first, first + length)],
        })
    return containers


def parse_sto(data: bytes) -> dict[str, Any]:
    signature(data, b"STORV1.0")
    checked(data, 0, 0x9C)
    offset, count = number(data, 0x34), number(data, 0x38)
    checked(data, offset, count * 28)
    return {"type": number(data, 8), "items": [
        dict(item(data, offset + i * 28), stock=number(data, offset + i * 28 + 20),
             infinite_supply=number(data, offset + i * 28 + 24)) for i in range(count)
    ]}


def snapshot(directory: Path, areas: tuple[str, ...] = AREAS) -> dict[str, Any]:
    paths = {path.name.upper(): path for path in directory.iterdir() if path.is_file()}
    stamp = lambda path: (path.stat().st_size, path.stat().st_mtime_ns)
    stamps = {name: stamp(paths[name]) for name in ("BALDUR.GAM", "BALDUR.SAV")}
    raw = {name: paths[name].read_bytes() for name in ("BALDUR.GAM", "BALDUR.SAV")}
    if any(stamp(paths[name]) != stamps[name] for name in raw):
        raise ValueError("save changed while reading; retry after the engine finishes saving")
    files = read_sav(raw["BALDUR.SAV"])
    result = parse_gam(raw["BALDUR.GAM"])
    result.update({
        "save_directory": str(directory.resolve()),
        "file_sha256": {name: hashlib.sha256(value).hexdigest() for name, value in raw.items()},
        "serialized_areas": sorted(name[:-4] for name in files if name.endswith(".ARE")),
        "areas": {area: {"present": f"{area}.ARE" in files,
                         "containers": parse_are(files[f"{area}.ARE"]) if f"{area}.ARE" in files else []}
                  for area in areas},
        "saved_stores": {name[:-4]: parse_sto(value) for name, value in files.items()
                         if name.endswith(".STO")},
    })
    return result


def item_key(value: dict[str, Any], with_slots: bool = False) -> tuple:
    key = (value["resref"], value["expiration"], *value["charges"], value["flags"])
    return (*key, tuple(value["slots"])) if with_slots else key


def multiset(items: list[dict[str, Any]], markers: set[str], with_slots: bool = False) -> Counter:
    return Counter(item_key(value, with_slots) for value in items if value["resref"] in markers)


def counter_json(counter: Counter) -> list[dict[str, Any]]:
    return [{"signature": list(key), "instances": count} for key, count in sorted(counter.items())]


def compare(before: dict, after: dict, markers: set[str], mode: str,
            bag_stores: tuple[str, ...] = ()) -> dict[str, Any]:
    checks = []

    def check(name: str, passed: bool, **details: Any) -> None:
        checks.append({"name": name, "passed": bool(passed), **details})

    source_items = [value for pc in before["party"] for value in pc["items"]]
    expected = multiset(source_items, markers)
    check("every explicit marker is present in the before party",
          bool(markers) and {key[0] for key in expected} == markers,
          missing=sorted(markers - {key[0] for key in expected}))
    check("before party is in BD4300", before["effective_current_area"] == "BD4300"
          and all(pc["area"] == "BD4300" for pc in before["party"]))
    if mode == "handoff":
        preexisting = multiset([value for c in before["areas"]["AR0602"]["containers"]
                                for value in c["items"]], markers)
        check("destination had no pre-existing marker copies", not preexisting,
              actual=counter_json(preexisting))
        check("after party is in AR0602", after["effective_current_area"] == "AR0602"
              and all(pc["area"] == "AR0602" for pc in after["party"]))
        check("destination area was serialized", after["areas"]["AR0602"]["present"])
        target_items = [value for pc in after["party"] if pc["area"] == "AR0602" for value in pc["items"]]
        target_items += [value for c in after["areas"]["AR0602"]["containers"] for value in c["items"]]
        actual = multiset(target_items, markers)
        check("ordinary marker multiset reached destination party/containers exactly", actual == expected,
              expected=counter_json(expected), actual=counter_json(actual),
              missing=counter_json(expected - actual), extra=counter_json(actual - expected))
        for area in ("BD4300", "BD6100"):
            remaining = multiset([value for c in after["areas"][area]["containers"] for value in c["items"]], markers)
            check(f"no marker remains in serialized {area} containers", not remaining,
                  area_serialized=after["areas"][area]["present"], actual=counter_json(remaining))
        check("handoff once flag was newly set", before["globals"].get("CSR_ENDING_USED", 0) == 0
              and after["globals"].get("CSR_ENDING_USED", 0) == 1)
        check("handoff failure flag is clear", after["globals"].get("CSR_ENDING_FAILED", 0) == 0)
        check("normal EET handoff reached plot 700", after["globals"].get("BD_PLOT", 0) == 700)
    elif mode == "guard":
        check("guard stayed in BD4300", after["effective_current_area"] == "BD4300"
              and all(pc["area"] == "BD4300" for pc in after["party"]))
        check("guard failure flag was newly set", before["globals"].get("CSR_ENDING_FAILED", 0) == 0
              and after["globals"].get("CSR_ENDING_FAILED", 0) == 1)
        check("once flag blocks a repeat attempt", after["globals"].get("CSR_ENDING_USED", 0) == 1)
        check("guard preserved plot", before["globals"].get("BD_PLOT", 0) == after["globals"].get("BD_PLOT", 0))
        identity = lambda pc: (pc["party_order"], pc["death_variable"].upper(), pc["name"])
        old = {identity(pc): pc for pc in before["party"]}
        new = {identity(pc): pc for pc in after["party"]}
        check("guard preserved party membership", old.keys() == new.keys())
        for key, pc in old.items():
            # Gear preservation checks all item rows, not just the marker subset.
            left = Counter(item_key(value, True) for value in pc["items"])
            right = Counter(item_key(value, True) for value in new.get(key, {}).get("items", []))
            check(f"guard preserved all gear and slots for {key}", left == right,
                  missing=counter_json(left - right), extra=counter_json(right - left))
    else:
        raise ValueError(f"unsupported comparison mode {mode}")
    for store in bag_stores:
        a, b = before["saved_stores"].get(store), after["saved_stores"].get(store)
        check(f"explicit bag store {store} exists as finite type-5 storage in both saves",
              bool(a and b and a["type"] == b["type"] == 5 and
                   all(not value["infinite_supply"] for value in a["items"] + b["items"])))
        key = lambda value: (*item_key(value), value["stock"], value["infinite_supply"])
        left = Counter(key(value) for value in (a or {}).get("items", []))
        right = Counter(key(value) for value in (b or {}).get("items", []))
        check(f"explicit bag store {store} retained exact contents", left == right,
              missing=counter_json(left - right), extra=counter_json(right - left))
    return {
        "mode": mode, "passed": all(row["passed"] for row in checks), "checks": checks,
        "before": before, "after": after,
        "limits": ["Persisted snapshots cannot prove movies, control recovery, or every transient party area.",
                   "Only supplied ordinary markers are asserted import-eligible; named-item EET sweeps are outside this comparison.",
                   "Explicit saved bag-store comparison does not establish the carried item's store association."],
    }


def resref(value: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9_#!+-]{1,8}", value):
        raise argparse.ArgumentTypeError(f"invalid resref {value!r}")
    return value.upper()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    snap = commands.add_parser("snapshot", help="read one save directory to JSON")
    snap.add_argument("save", type=Path)
    snap.add_argument("--areas", type=resref, nargs="+", default=AREAS)
    comparison = commands.add_parser("compare", help="assert persisted guard or handoff evidence")
    comparison.add_argument("before", type=Path)
    comparison.add_argument("after", type=Path)
    comparison.add_argument("--mode", choices=("guard", "handoff"), required=True)
    comparison.add_argument("--markers", type=resref, nargs="+", required=True)
    comparison.add_argument("--bag-stores", type=resref, nargs="*", default=[])
    args = parser.parse_args(argv)
    try:
        if args.command == "snapshot":
            result = snapshot(args.save, tuple(args.areas))
            result["parsed"] = True
        else:
            result = compare(snapshot(args.before), snapshot(args.after), set(args.markers),
                             args.mode, tuple(args.bag_stores))
    except (OSError, ValueError, KeyError, UnicodeError, zlib.error) as error:
        result = {"passed": False, "errors": [str(error)]}
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0 if result.get("passed", result.get("parsed", False)) else 1


if __name__ == "__main__":
    sys.exit(main())
