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

    @property
    def usable(self) -> bool:
        """Known quest-item sources must be ordinary, unlocked containers."""
        return self.lock_difficulty == 0 and self.flags == 0 and not self.key_resref


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
    containers, actors, live_scripts = parse_area(game_dir / "override" / "BD1200.ARE")
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
