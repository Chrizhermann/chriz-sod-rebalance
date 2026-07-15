#!/usr/bin/env python3
"""Verify the installed BD1200 scrying-pool contract."""

from __future__ import annotations

import argparse
import re
import struct
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


class VerificationError(RuntimeError):
    """The installed resources could not be inspected safely."""


def cstring(data: bytes) -> str:
    return data.split(b"\0", 1)[0].decode("ascii", "replace")


def section(data: bytes, offset: int, count: int, size: int, name: str) -> None:
    if offset < 0 or count < 0 or offset + count * size > len(data):
        raise VerificationError(
            f"BD1200.ARE {name} table is out of bounds "
            f"(offset {offset:#x}, count {count}, size {size:#x})"
        )


@dataclass(frozen=True)
class Container:
    name: str
    x: int
    y: int
    items: tuple[str, ...]
    lock_difficulty: int
    flags: int
    trap_detection: int
    trap_removal: int
    trapped: int
    key_resref: str
    script_resref: str

    @property
    def usable(self) -> bool:
        """Known quest-item sources must be ordinary, unlocked containers."""
        return self.lock_difficulty == 0 and self.flags == 0 and not self.key_resref

    @property
    def unguarded_baseline(self) -> bool:
        """The rehome target must not gain an item behind a lock, trap, or script."""
        return (
            self.lock_difficulty == 0
            and self.flags == 0
            and self.trapped == 0
            and not self.key_resref
            and not self.script_resref
        )


@dataclass(frozen=True)
class Actor:
    resref: str
    x: int
    y: int
    schedule: int


def parse_area(path: Path) -> tuple[list[Container], list[Actor], set[str]]:
    data = path.read_bytes()
    if len(data) < 0x9C or data[:4] != b"AREA":
        raise VerificationError(f"{path} is not a valid ARE resource")

    actor_offset = struct.unpack_from("<I", data, 0x54)[0]
    actor_count = struct.unpack_from("<H", data, 0x58)[0]
    region_count = struct.unpack_from("<H", data, 0x5A)[0]
    region_offset = struct.unpack_from("<I", data, 0x5C)[0]
    container_offset = struct.unpack_from("<I", data, 0x70)[0]
    container_count = struct.unpack_from("<H", data, 0x74)[0]
    item_count = struct.unpack_from("<H", data, 0x76)[0]
    item_offset = struct.unpack_from("<I", data, 0x78)[0]
    section(data, actor_offset, actor_count, 0x110, "actor")
    section(data, region_offset, region_count, 0xC4, "info-region")
    section(data, container_offset, container_count, 0xC0, "container")
    section(data, item_offset, item_count, 0x14, "item")

    item_resrefs = [
        cstring(data[item_offset + i * 0x14 : item_offset + i * 0x14 + 8]).upper()
        for i in range(item_count)
    ]
    containers: list[Container] = []
    for i in range(container_count):
        base = container_offset + i * 0xC0
        first = struct.unpack_from("<I", data, base + 0x40)[0]
        count = struct.unpack_from("<I", data, base + 0x44)[0]
        if first + count > item_count:
            raise VerificationError(
                f"BD1200.ARE container {i} item run exceeds the live item table"
            )
        containers.append(
            Container(
                cstring(data[base : base + 32]),
                struct.unpack_from("<H", data, base + 0x20)[0],
                struct.unpack_from("<H", data, base + 0x22)[0],
                tuple(item_resrefs[first : first + count]),
                struct.unpack_from("<H", data, base + 0x26)[0],
                struct.unpack_from("<I", data, base + 0x28)[0],
                struct.unpack_from("<H", data, base + 0x2C)[0],
                struct.unpack_from("<H", data, base + 0x2E)[0],
                struct.unpack_from("<H", data, base + 0x30)[0],
                cstring(data[base + 0x78 : base + 0x80]).upper(),
                cstring(data[base + 0x48 : base + 0x50]).upper(),
            )
        )

    actors = []
    for i in range(actor_count):
        base = actor_offset + i * 0x110
        actors.append(
            Actor(
                cstring(data[base + 0x80 : base + 0x88]).upper(),
                struct.unpack_from("<H", data, base + 0x20)[0],
                struct.unpack_from("<H", data, base + 0x22)[0],
                struct.unpack_from("<I", data, base + 0x40)[0],
            )
        )
    live_scripts = {cstring(data[0x94:0x9C]).upper()}
    live_scripts.update(
        cstring(data[region_offset + i * 0xC4 + 0x7C : region_offset + i * 0xC4 + 0x84]).upper()
        for i in range(region_count)
    )
    live_scripts.update(
        cstring(data[container_offset + i * 0xC0 + 0x48 : container_offset + i * 0xC0 + 0x50]).upper()
        for i in range(container_count)
    )
    for i in range(actor_count):
        base = actor_offset + i * 0x110
        live_scripts.update(
            cstring(data[base + relative : base + relative + 8]).upper()
            for relative in (0x50, 0x58, 0x60, 0x68, 0x70, 0x78)
        )
    live_scripts.discard("")
    return containers, actors, live_scripts


def decompile(game_dir: Path) -> tuple[str, str]:
    weidu = game_dir / "weidu.exe"
    bcs = game_dir / "override" / "BDODSCRY.BCS"
    dlg = game_dir / "override" / "BDSCRY.DLG"
    for path in (weidu, bcs, dlg):
        if not path.is_file():
            raise VerificationError(f"required file is missing: {path}")
    with tempfile.TemporaryDirectory(prefix="csr-scrying-pool-") as output_dir:
        result = subprocess.run(
            [
                str(weidu),
                str(bcs),
                str(dlg),
                "--game",
                str(game_dir),
                "--out",
                output_dir,
                "--no-exit-pause",
            ],
            cwd=output_dir,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=60,
            check=False,
        )
        if result.returncode:
            detail = (result.stderr or result.stdout).strip()
            raise VerificationError(f"WeiDU decompilation failed: {detail}")
        baf_path = Path(output_dir) / "BDODSCRY.baf"
        d_path = Path(output_dir) / "BDSCRY.d"
        if not baf_path.is_file() or not d_path.is_file():
            raise VerificationError("WeiDU did not produce BDODSCRY.baf and BDSCRY.d")
        return (
            baf_path.read_text(encoding="utf-8", errors="replace"),
            d_path.read_text(encoding="utf-8", errors="replace"),
        )


def unique_container_offset(data: bytes, name: str, x: int, y: int) -> int:
    """Locate one container record in an ARE image or fail the binary audit."""
    if len(data) < 0x9C or data[:4] != b"AREA":
        raise VerificationError("component 225 backup is not a valid ARE resource")
    offset = struct.unpack_from("<I", data, 0x70)[0]
    count = struct.unpack_from("<H", data, 0x74)[0]
    section(data, offset, count, 0xC0, "backup container")
    matches = []
    for i in range(count):
        base = offset + i * 0xC0
        if (
            cstring(data[base : base + 32]).casefold() == name.casefold()
            and struct.unpack_from("<H", data, base + 0x20)[0] == x
            and struct.unpack_from("<H", data, base + 0x22)[0] == y
        ):
            matches.append(base)
    if len(matches) != 1:
        raise VerificationError(
            f"expected one {name}@{x},{y} in component 225 backup, found {len(matches)}"
        )
    return matches[0]


def baf_blocks(text: str) -> list[tuple[str, str]]:
    return [
        (match.group("triggers"), match.group("actions"))
        for match in re.finditer(
            r"(?ms)^IF\s*$\s*(?P<triggers>.*?)^THEN\s*$\s*(?P<actions>.*?)^END\s*$",
            text,
        )
    ]


def dialog_states(text: str) -> dict[int, str]:
    states: dict[int, str] = {}
    lines = text.splitlines()
    for i, line in enumerate(lines):
        match = re.search(r"\bTHEN\s+BEGIN\s+(\d+)\b", line, re.IGNORECASE)
        if not match:
            continue
        end = next(
            (j for j in range(i + 1, len(lines)) if lines[j].strip() == "END"),
            None,
        )
        if end is None:
            raise VerificationError(f"unterminated BDSCRY dialog state {match.group(1)}")
        states[int(match.group(1))] = "\n".join(lines[i + 1 : end])
    return states


def trigger_lines(text: str, pattern: str) -> list[str]:
    """Return uncommented trigger lines that match with the requested polarity."""
    compiled = re.compile(pattern, re.IGNORECASE)
    matches = []
    for line in text.splitlines():
        code = line.split("//", 1)[0].strip()
        if compiled.fullmatch(code):
            matches.append(code)
    return matches


def positive_two_copy_trigger_count(text: str) -> int:
    patterns = (
        r'NumItemsPartyGT\s*\(\s*"BDMISC59"\s*,\s*1\s*\)',
        r'NumItemsParty\s*\(\s*"BDMISC59"\s*,\s*2\s*\)',
        r'!\s*NumItemsPartyLT\s*\(\s*"BDMISC59"\s*,\s*2\s*\)',
    )
    return sum(len(trigger_lines(text, pattern)) for pattern in patterns)


def done_trigger_count(text: str, value: int) -> int:
    return len(
        trigger_lines(
            text,
            rf'Global\s*\(\s*"CSR_SCRY_(?:DONE|OMEN)"\s*,\s*"[^"]+"\s*,\s*{value}\s*\)',
        )
    )


def has_pool_click_gate(text: str) -> bool:
    return (
        len(trigger_lines(text, r"Clicked\s*\(\s*\[ANYONE\]\s*\)")) == 1
        and len(
            trigger_lines(
                text,
                r'Global\s*\(\s*"BD_SDDD12_COUNTER"\s*,\s*"MYAREA"\s*,\s*3\s*\)',
            )
        )
        == 1
    )


def dialog_transitions(state_body: str) -> list[tuple[str, str]]:
    return [
        (match.group("trigger"), match.group("route"))
        for match in re.finditer(
            r"(?ms)^\s*IF\s+~(?P<trigger>.*?)~\s+THEN\s+"
            r"(?P<route>.*?)(?=^\s*IF\s+~|\Z)",
            state_body,
        )
    ]


class Reporter:
    def __init__(self) -> None:
        self.failures = 0

    def check(self, label: str, passed: bool, detail: str = "") -> None:
        if not passed:
            self.failures += 1
        suffix = f" ({detail})" if detail else ""
        print(f"{'PASS' if passed else 'FAIL'}: {label}{suffix}")


def verify(game_dir: Path) -> int:
    report = Reporter()
    area_path = game_dir / "override" / "BD1200.ARE"
    containers, actors, live_scripts = parse_area(area_path)
    baf, dialog = decompile(game_dir)

    held = [
        (container, item)
        for container in containers
        if container.usable
        for item in container.items
    ]
    scepters = [entry for entry in held if entry[1] == "BDMISC55"]
    essences = [entry for entry in held if entry[1] == "BDMISC59"]
    report.check("three reachable container-held Silver Scepters", len(scepters) == 3, f"found {len(scepters)}")
    report.check("two reachable container-held Essences", len(essences) == 2, f"found {len(essences)}")

    expected_sources = (
        ("Silver Scepter", "Table01", (1859, 2408), "BDMISC55"),
        ("Silver Scepter", "Sarcophagus01", (2414, 1736), "BDMISC55"),
        ("Silver Scepter", "Table02", (2350, 805), "BDMISC55"),
        ("Essence", "Shelf", (1146, 1230), "BDMISC59"),
        ("Essence", "Sarcophagus01", (2414, 1736), "BDMISC59"),
    )
    for item_label, container_name, coordinates, resref in expected_sources:
        sources = [
            container
            for container in containers
            if container.name.casefold() == container_name.casefold()
            and (container.x, container.y) == coordinates
            and container.items.count(resref) == 1
        ]
        detail = f"found {len(sources)}"
        if len(sources) == 1:
            source = sources[0]
            detail += (
                f", lock {source.lock_difficulty}, flags {source.flags:#x}, "
                f"trap {source.trapped} ({source.trap_detection}/{source.trap_removal})"
            )
        report.check(
            f"{item_label} source {container_name}@{coordinates[0]},{coordinates[1]} is present and usable",
            len(sources) == 1 and sources[0].usable,
            detail,
        )

    targets = [
        container
        for container in containers
        if container.name.casefold() == "sarcophagus01" and (container.x, container.y) == (2414, 1736)
    ]
    report.check("unique Sarcophagus01 at (2414,1736)", len(targets) == 1, f"found {len(targets)}")
    target_items = targets[0].items if len(targets) == 1 else ()
    report.check("Sarcophagus01 retains BDMISC55", target_items.count("BDMISC55") == 1)
    report.check("Sarcophagus01 gains one BDMISC59", target_items.count("BDMISC59") == 1)
    target_baseline_ok = len(targets) == 1 and targets[0].unguarded_baseline
    target_baseline_detail = "target unavailable"
    if len(targets) == 1:
        target = targets[0]
        target_baseline_detail = (
            f"lock {target.lock_difficulty}, flags {target.flags:#x}, "
            f"trapped {target.trapped}, key {target.key_resref or '<blank>'}, "
            f"script {target.script_resref or '<blank>'}"
        )
    report.check(
        "Sarcophagus01 rehome target keeps its unlocked, untrapped, unscripted baseline",
        target_baseline_ok,
        target_baseline_detail,
    )

    backup_path = (
        game_dir
        / "weidu_external"
        / "backup"
        / "chriz-sod-remix"
        / "225"
        / "bd1200.are"
    )
    backup_available = backup_path.is_file()
    report.check(
        "component 225 BD1200 backup is available for byte-level audit",
        backup_available,
        str(backup_path),
    )
    if backup_available:
        installed_area = area_path.read_bytes()
        original_area = backup_path.read_bytes()
        original_target = unique_container_offset(
            original_area, "Sarcophagus01", 2414, 1736
        )
        installed_target = unique_container_offset(
            installed_area, "Sarcophagus01", 2414, 1736
        )
        report.check(
            "Sarcophagus01 container record stays at its original offset",
            installed_target == original_target,
            f"backup {original_target:#x}, installed {installed_target:#x}",
        )

        original_item_count = struct.unpack_from("<H", original_area, 0x76)[0]
        original_item_offset = struct.unpack_from("<I", original_area, 0x78)[0]
        installed_item_count = struct.unpack_from("<H", installed_area, 0x76)[0]
        installed_item_offset = struct.unpack_from("<I", installed_area, 0x78)[0]
        section(
            original_area,
            original_item_offset,
            original_item_count,
            0x14,
            "backup item",
        )
        section(
            installed_area,
            installed_item_offset,
            installed_item_count,
            0x14,
            "installed relocated item",
        )
        original_target_first = struct.unpack_from(
            "<I", original_area, original_target + 0x40
        )[0]
        original_target_count = struct.unpack_from(
            "<I", original_area, original_target + 0x44
        )[0]
        installed_target_first = struct.unpack_from(
            "<I", installed_area, installed_target + 0x40
        )[0]
        installed_target_count = struct.unpack_from(
            "<I", installed_area, installed_target + 0x44
        )[0]

        masked_original = bytearray(original_area)
        masked_installed = bytearray(installed_area[: len(original_area)])
        original_prefix_available = len(installed_area) >= len(original_area)
        if original_prefix_available and installed_target == original_target:
            for start, end in (
                (0x76, 0x7C),
                (original_target + 0x40, original_target + 0x48),
            ):
                masked_original[start:end] = b"\0" * (end - start)
                masked_installed[start:end] = b"\0" * (end - start)
        original_prefix_ok = (
            original_prefix_available
            and installed_target == original_target
            and masked_installed == masked_original
        )
        report.check(
            "original-length BD1200 bytes change only in the item header and target run",
            original_prefix_ok,
        )

        item_shape_ok = (
            installed_item_count == original_item_count + 2
            and installed_item_offset == len(original_area)
            and installed_target_first == original_item_count
            and installed_target_count == 2
            and len(installed_area)
            == len(original_area) + installed_item_count * 0x14
        )
        report.check(
            "relocated item table grows by two at EOF and only the target owns the new run",
            item_shape_ok,
            (
                f"count {original_item_count}->{installed_item_count}, "
                f"offset {installed_item_offset:#x}/{len(original_area):#x}, "
                f"target {installed_target_first}+{installed_target_count}"
            ),
        )

        original_items = original_area[
            original_item_offset : original_item_offset + original_item_count * 0x14
        ]
        relocated_original_items = installed_area[
            installed_item_offset : installed_item_offset + original_item_count * 0x14
        ]
        report.check(
            "original item array is copied byte-exact at the relocated offset",
            relocated_original_items == original_items,
        )

        original_scepter_start = (
            original_item_offset + original_target_first * 0x14
        )
        installed_scepter_start = (
            installed_item_offset + installed_target_first * 0x14
        )
        original_scepter = original_area[
            original_scepter_start : original_scepter_start + 0x14
        ]
        installed_scepter = installed_area[
            installed_scepter_start : installed_scepter_start + 0x14
        ]
        scepter_ok = (
            original_target_count == 1
            and len(original_scepter) == 0x14
            and installed_scepter == original_scepter
        )
        report.check(
            "target Silver Scepter record is copied byte-exact into the new run",
            scepter_ok,
        )

        essence_start = installed_scepter_start + 0x14
        essence = installed_area[essence_start : essence_start + 0x14]
        essence_ok = (
            len(essence) == 0x14
            and cstring(essence[:8]).upper() == "BDMISC59"
            and essence[8:] == b"\0" * 12
        )
        report.check(
            "new Essence record has BDMISC59 and zero expiration, charges, and flags",
            essence_ok,
        )

    wights = [actor for actor in actors if actor.resref == "BDWIGHDD" and (actor.x, actor.y) == (2474, 1951)]
    report.check(
        "BDWIGHDD at (2474,1951) remains schedule-zero",
        len(wights) == 1 and wights[0].schedule == 0,
        f"matches {len(wights)}" + (f", schedule {wights[0].schedule:#x}" if len(wights) == 1 else ""),
    )
    stale_scepter_refs = sorted(
        live_scripts.intersection({"BDSCEPT1", "BDSCEPT2", "BDSCEPT3"})
    )
    report.check(
        "no live BDSCEPT1/2/3 ARE script reference",
        not stale_scepter_refs,
        ", ".join(stale_scepter_refs),
    )

    success_trigger_count = positive_two_copy_trigger_count(baf)
    report.check("one two-Essence success trigger", success_trigger_count == 1, f"found {success_trigger_count}")

    take_matches = list(re.finditer(r'TakePartyItemNum\s*\(\s*"BDMISC59"\s*,\s*2\s*\)', baf, re.IGNORECASE))
    report.check("consume exactly two Essences once", len(take_matches) == 1, f"found {len(take_matches)}")

    legacy_one_vial = re.findall(
        r'TakePartyItem\s*\(\s*"BDMISC59"\s*\)', baf, re.IGNORECASE
    )
    report.check(
        "no active legacy one-Essence consumption path",
        not legacy_one_vial,
        f"found {len(legacy_one_vial)}",
    )

    blocks = baf_blocks(baf)
    no_consume_or_xp = re.compile(
        r"\b(?:TakePartyItem\w*|DestroyItem\w*|RemoveItem\w*|"
        r"AddXPObject|AddExperienceParty)\s*\(",
        re.IGNORECASE,
    )
    insufficient_blocks = [
        (trigger, actions)
        for trigger, actions in blocks
        if done_trigger_count(trigger, 0) == 1
        and has_pool_click_gate(trigger)
        and len(
            trigger_lines(
                trigger,
                r'NumItemsPartyLT\s*\(\s*"BDMISC59"\s*,\s*2\s*\)',
            )
        )
        == 1
    ]
    insufficient_ok = (
        len(insufficient_blocks) == 1
        and not no_consume_or_xp.search(insufficient_blocks[0][1])
    )
    report.check(
        "one done=0 insufficient-Essence block consumes and pays nothing",
        insufficient_ok,
        f"found {len(insufficient_blocks)}",
    )
    dormant_blocks = [
        (trigger, actions)
        for trigger, actions in blocks
        if done_trigger_count(trigger, 1) == 1
        and has_pool_click_gate(trigger)
    ]
    dormant_ok = (
        len(dormant_blocks) == 1
        and not no_consume_or_xp.search(dormant_blocks[0][1])
    )
    report.check(
        "one done=1 dormant click block consumes and pays nothing",
        dormant_ok,
        f"found {len(dormant_blocks)}",
    )

    success_blocks = [(trigger, actions) for trigger, actions in blocks if re.search(r'TakePartyItemNum\s*\(\s*"BDMISC59"', actions, re.IGNORECASE)]
    trigger_with_take = (
        len(success_blocks) == 1
        and positive_two_copy_trigger_count(success_blocks[0][0]) == 1
    )
    report.check("two-Essence trigger and consumption share one success block", trigger_with_take)
    success_click_gate = (
        len(success_blocks) == 1 and has_pool_click_gate(success_blocks[0][0])
    )
    report.check(
        "success block is one pool click after all three scepters",
        success_click_gate,
    )
    once_ok = False
    order_ok = False
    if len(success_blocks) == 1:
        trigger, actions = success_blocks[0]
        set_match = re.search(
            r'SetGlobal\s*\(\s*"(?P<flag>CSR_SCRY_(?:DONE|OMEN))"\s*,\s*"(?P<scope>[^"]+)"\s*,\s*1\s*\)',
            actions,
            re.IGNORECASE,
        )
        if set_match:
            flag = re.escape(set_match.group("flag"))
            scope = re.escape(set_match.group("scope"))
            once_ok = len(
                trigger_lines(
                    trigger,
                    rf'Global\s*\(\s*"{flag}"\s*,\s*"{scope}"\s*,\s*0\s*\)',
                )
            ) == 1
            take_pos = re.search(r'TakePartyItemNum\s*\(', actions, re.IGNORECASE)
            xp_pos = re.search(r'AddXPObject\s*\(', actions, re.IGNORECASE)
            order_ok = bool(take_pos and xp_pos and set_match.start() < take_pos.start() and set_match.start() < xp_pos.start())
    report.check("success path is gated by its CSR_SCRY_DONE/OMEN once flag", once_ok)
    report.check("once flag is set before Essence consumption and XP", order_ok)

    success_actions = success_blocks[0][1] if len(success_blocks) == 1 else ""
    terminal_cloudy = re.findall(
        r'SetGlobal\s*\(\s*"BD_SDDD12_CLOUDY"\s*,\s*"MYAREA"\s*,\s*2\s*\)',
        success_actions,
        re.IGNORECASE,
    )
    report.check(
        "success path sets BD_SDDD12_CLOUDY to terminal value 2",
        len(terminal_cloudy) == 1,
        f"found {len(terminal_cloudy)}",
    )
    omen_displays = re.findall(
        r"\bDisplayStringNoNameHead\s*\(", success_actions, re.IGNORECASE
    )
    report.check(
        "success path displays the text-only omen without dialog",
        len(omen_displays) == 1,
        f"found {len(omen_displays)}",
    )
    ambient_actions = [
        (name.casefold(), enabled.upper())
        for name, enabled in re.findall(
            r'AmbientActivate\s*\(\s*"([^"]+)"\s*,\s*(TRUE|FALSE)\s*\)',
            success_actions,
            re.IGNORECASE,
        )
    ]
    terminal_ambients = [
        ("scrying_pool", "FALSE"),
        ("scrying_pool_murky1", "TRUE"),
        ("scrying_pool_murky2", "TRUE"),
        ("scrying_pool_murky3", "TRUE"),
    ]
    report.check(
        "success path finishes with clear pool off and all murky ambients on",
        ambient_actions[-4:] == terminal_ambients,
        f"tail {ambient_actions[-4:]}",
    )

    xp_matches = re.findall(r'AddXPObject\s*\(\s*(Player[1-6])\s*,\s*(\d+)\s*\)', baf, re.IGNORECASE)
    xp_ok = len(xp_matches) == 6 and {name.upper() for name, amount in xp_matches if amount == "1000"} == {f"PLAYER{i}" for i in range(1, 7)}
    report.check("Player1..6 each receive exactly 1,000 XP", xp_ok, f"found {xp_matches}")
    ordered_xp = list(
        re.finditer(
            r'AddXPObject\s*\(\s*Player[1-6]\s*,\s*1000\s*\)',
            success_actions,
            re.IGNORECASE,
        )
    )
    take_before_xp = re.search(
        r'TakePartyItemNum\s*\(\s*"BDMISC59"\s*,\s*2\s*\)',
        success_actions,
        re.IGNORECASE,
    )
    first_cosmetic = re.search(
        r'\b(?:CreateVisualEffect|SmallWait|AmbientActivate|DisplayString\w*)\s*\(',
        success_actions,
        re.IGNORECASE,
    )
    xp_order_ok = (
        len(ordered_xp) == 6
        and take_before_xp is not None
        and first_cosmetic is not None
        and all(
            take_before_xp.end() < award.start() < first_cosmetic.start()
            for award in ordered_xp
        )
    )
    report.check(
        "all six XP awards follow Essence consumption before any cosmetic or wait",
        xp_order_ok,
    )

    launcher = re.search(r'ActionOverride\s*\(\s*"BDSCRY"\s*,\s*StartDialog', baf, re.IGNORECASE)
    report.check("no BDSCRY dialog launcher", launcher is None)
    forbidden = sorted(
        {
            match.group(1)
            for match in re.finditer(
                r'\b(StartCutScene\w*|LeaveArea\w*|MoveBetweenAreas\w*|MoveGlobal\w*|'
                r'EscapeArea\w*|Transfer\w*|TeleportParty\w*|JumpTo(?:Point|Object)\w*|'
                r'StorePartyLocations\w*|RestorePartyLocations\w*|CreateCreature\w*|CUTSKIP)\b',
                baf,
                re.IGNORECASE,
            )
        }
    )
    report.check("no cutscene, relocation, creature-spawn, or CUTSKIP action", not forbidden, ", ".join(forbidden))

    party_awards = re.findall(r'AddExperienceParty\s*\(\s*3000\s*\)', baf, re.IGNORECASE)
    report.check("one 3,000 party-total scepter award remains", len(party_awards) == 1, f"found {len(party_awards)}")

    states = dialog_states(dialog)
    for state_number in (0, 4):
        transitions = dialog_transitions(states.get(state_number, ""))
        for destination in (1, 2, 3):
            routes = [
                trigger
                for trigger, route in transitions
                if re.search(rf"\bGOTO\s+{destination}\b", route, re.IGNORECASE)
            ]
            report.check(
                f"BDSCRY state {state_number} has one GOTO {destination} picker route",
                len(routes) == 1,
                f"found {len(routes)}",
            )
            false_gated = len(routes) == 1 and bool(
                re.search(r"\bFalse\s*\(\s*\)", routes[0], re.IGNORECASE)
            )
            report.check(
                f"BDSCRY state {state_number} GOTO {destination} is False-gated",
                false_gated,
            )

    print(f"SUMMARY: {report.failures} failure(s)")
    return 1 if report.failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game-dir", required=True, type=Path)
    args = parser.parse_args()
    try:
        return verify(args.game_dir.resolve())
    except (OSError, subprocess.SubprocessError, struct.error, VerificationError) as error:
        print(f"FAIL: verifier could not inspect the installed resources ({error})")
        return 1


if __name__ == "__main__":
    sys.exit(main())
