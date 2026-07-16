#!/usr/bin/env python3
"""Verify the installed direct post-victory ending contract.

The verifier intentionally inspects compiled game resources.  It does not trust
the mod sources: ARE records are parsed directly and BCS/DLG resources are
decompiled with the target game's WeiDU binary from a temporary working
directory.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


EET_ANCHORS = ("K#TELBGT.BCS", "K#TELBGT.CRE", "AR0602.BCS")
COMMON_TEXT_RESOURCES = {
    "BD4300.BCS",
    "BDBENCE.DLG",
    "BDDAZZO.DLG",
    "BDDEBUG.BCS",
    "BDDEBUG.DLG",
    "BDDELANC.DLG",
    "BDPALACE.BCS",
    "BDRUMOR3.DLG",
}
EET_TEXT_RESOURCES = {"K#TELBGT.BCS", "CSRETBGT.BCS", "AR0602.BCS"}
STANDALONE_TEXT_RESOURCES = {"BD6100.BCS"}

# This is the frozen result of the 2026-07-16 installed-resource audit.  The
# authoritative dev EET override contained 1,232 BD*.BCS and 604 BD*.DLG
# resources.  Raw anchor screening selected 321 resources, all of which were
# decompiled before these counts were recorded.  The legacy sod_baf corpus was
# absent from the isolated worktree (it existed only as non-tracked data in the
# main checkout); its exhaustive anchor scan corroborated the base-game roots,
# but the installed inventory remains authoritative.  Counts describe the
# post-component-290 state; downstream scripts remain installed but have no
# live production root.
ROOT_PATTERNS = {
    "plot590": re.compile(
        r'(?:Global(?:LT|GT)?|SetGlobal)\s*\(\s*"bd_plot"\s*,\s*"global"\s*,\s*590\s*\)',
        re.IGNORECASE,
    ),
    "cut60": re.compile(
        r'StartCutScene(?:Ex)?\s*\(\s*"bdcut60[a-z]?"', re.IGNORECASE
    ),
    "cut61": re.compile(
        r'StartCutScene(?:Ex)?\s*\(\s*"bdcut61[a-z]?"', re.IGNORECASE
    ),
    "debugdream": re.compile(r"bd_debug_move_to_dream", re.IGNORECASE),
    "debugcell": re.compile(r"bd_debug_move_to_cell", re.IGNORECASE),
    "corwin6": re.compile(r"bd_CorwinRomance6", re.IGNORECASE),
    "neera6": re.compile(r"bd_NeeraRomance6", re.IGNORECASE),
}
KNOWN_ROOT_COUNTS: dict[str, dict[str, int]] = {
    "BD0112.BCS": {"cut61": 1},
    "BD4100.BCS": {"plot590": 3, "cut60": 2},
    "BD4300.BCS": {"plot590": 2, "corwin6": 3, "neera6": 3},
    "BDBENCE.DLG": {"plot590": 1},
    "BDCORWIJ.DLG": {"corwin6": 4},
    "BDCUT60.BCS": {"cut60": 1},
    "BDCUT60A.BCS": {"cut60": 3},
    "BDCUT61A.BCS": {"cut61": 1},
    "BDDAZZO.DLG": {"plot590": 1},
    "BDDEBUG.BCS": {
        "plot590": 1,
        "cut60": 1,
        "cut61": 1,
        "debugdream": 2,
        "debugcell": 2,
    },
    "BDDEBUG.DLG": {"plot590": 1, "debugdream": 4, "debugcell": 4},
    "BDDELANC.BCS": {"plot590": 1},
    "BDDELANC.DLG": {"plot590": 6},
    "BDIRENI.DLG": {"plot590": 1},
    "BDSKIE.DLG": {"cut60": 1},
    "BDVAULTD.BCS": {"plot590": 2},
    # Optional Aura interjection, present on the target EET install only.
    "C0AURA2J.DLG": {"plot590": 1},
    "CUTSKIP.BCS": {"cut61": 1},
    "NEERAJ.DLG": {"neera6": 2},
}

TARGET_CODA_STATES = {
    "BDBENCE": {6, 9, 10, 64, 65, 66, 67, 68, 70, 71, 73},
    "BDDELANC": {77, 78, 79, 80, 81, 82, 83, 95, 104},
    "BDDAZZO": {0, 2, 3},
    "BDRUMOR3": {7, 20, 37},
}
BENCE_TERMINAL_COUNTS = {9: 1, 10: 1, 70: 2, 71: 2, 73: 2}
EXPECTED_EXTERNAL_INBOUND = Counter(
    {
        ("BDCORWIN.DLG", "BDBENCE", 68): 4,
        ("BDCORWIJ.DLG", "BDBENCE", 68): 4,
        ("BDDELANC.DLG", "BDBENCE", 64): 1,
        ("BDVOGHIJ.DLG", "BDDELANC", 79): 1,
        ("BDVOGHIJ.DLG", "BDDELANC", 83): 1,
    }
)
EXPECTED_GOTO_INBOUND = Counter(
    {
        ("BDBENCE.DLG", 6, 9): 2,
        ("BDBENCE.DLG", 7, 10): 1,
        ("BDBENCE.DLG", 8, 10): 1,
        ("BDBENCE.DLG", 64, 65): 1,
        ("BDBENCE.DLG", 67, 68): 1,
        ("BDBENCE.DLG", 68, 70): 1,
        ("BDBENCE.DLG", 68, 71): 1,
        ("BDBENCE.DLG", 69, 70): 1,
        ("BDBENCE.DLG", 69, 71): 1,
        ("BDBENCE.DLG", 72, 73): 1,
        ("BDDELANC.DLG", 77, 78): 1,
        ("BDDELANC.DLG", 77, 80): 1,
        ("BDDELANC.DLG", 77, 82): 1,
        ("BDDELANC.DLG", 78, 79): 3,
        ("BDDELANC.DLG", 79, 83): 1,
        ("BDDELANC.DLG", 80, 79): 2,
        ("BDDELANC.DLG", 80, 81): 1,
        ("BDDELANC.DLG", 81, 79): 1,
        ("BDDELANC.DLG", 82, 79): 1,
        ("BDDAZZO.DLG", 0, 3): 2,
        ("BDDAZZO.DLG", 1, 2): 2,
        ("BDDAZZO.DLG", 1, 3): 1,
    }
)

ROOT_SCREEN_ANCHORS = (
    "bd_plot",
    "bdcut60",
    "bdcut61",
    "bd_debug_move_to_dream",
    "bd_debug_move_to_cell",
    "romance6",
    "bdbence",
    "bddelanc",
    "bddazzo",
    "bdrumor3",
)
ROOT_BINARY_NEEDLES = tuple(
    value.lower().encode("ascii") for value in ROOT_SCREEN_ANCHORS
)
# WeiDU's --biff-str uses \|, rather than a bare |, for alternation.
BIFF_ROOT_QUERY = r"\|".join(ROOT_SCREEN_ANCHORS)
OPTIONAL_ROOT_RESOURCES = {"C0AURA2J.DLG"}

HASH_REQUIRED_COMMON = {
    "BDCUT59.BCS",
    "BDCUT59A.BCS",
    "BDCUT59B.BCS",
    "CUTSKIP.BCS",
    "BD0104.BCS",
}
HASH_REQUIRED_EET = {
    "K#TELBGT.BCS",
    "K#TELBGT.CRE",
    "AR0602.BCS",
    "BD6100.BCS",
    "BD6100.ARE",
}
HASH_REQUIRED_STANDALONE = {"BD6100.BCS", "BD6100.ARE"}


class VerificationError(RuntimeError):
    """The installed resources could not be inspected safely."""


def cstring(data: bytes) -> str:
    return data.split(b"\0", 1)[0].decode("ascii", "replace")


def section(data: bytes, offset: int, count: int, size: int, label: str) -> None:
    if offset < 0 or count < 0 or offset + count * size > len(data):
        raise VerificationError(
            f"{label} is out of bounds (offset {offset:#x}, count {count}, size {size:#x})"
        )


def classify_platform(signatures: tuple[bool, bool, bool], requested: str) -> str:
    count = sum(signatures)
    if count not in (0, 3):
        detail = ", ".join(
            f"{name}={'present' if present else 'missing'}"
            for name, present in zip(EET_ANCHORS, signatures)
        )
        raise VerificationError(f"partial EET signature: {detail}")
    detected = "eet" if count == 3 else "standalone"
    if requested != "auto" and requested != detected:
        raise VerificationError(
            f"--platform {requested} contradicts complete {detected} signature"
        )
    return detected


def expected_timer_count(c0aura_barks: int) -> int:
    # Audited provenance: native merged SoD has 17 vanilla setters.  The
    # current target EET resolves to 18 only because C0Aura contributes one
    # exact plot-586 bark using the same timer; this is content-sensitive, not
    # intrinsically platform-sensitive.
    return 17 + c0aura_barks


def parse_biff_search_output(output: str) -> set[str]:
    """Parse the verified WeiDU 24600 ``--biff-str`` result-line format."""

    result: set[str] = set()
    result_shape = re.compile(
        r"^\s*(?P<resource>[^\s.\[\]]{1,8}\.(?:BCS|DLG))\s+"
        r"in\s+\[[^\]\r\n]+\]\s+matches\s*$",
        re.IGNORECASE,
    )
    possible_result = re.compile(
        r"\s+in\s+\[[^\]\r\n]+\]\s+matches\s*$", re.IGNORECASE
    )
    for line in output.splitlines():
        match = result_shape.fullmatch(line)
        if match:
            result.add(match.group("resource").upper())
        elif possible_result.search(line):
            raise VerificationError(
                f"unrecognized WeiDU --biff-str result line: {line.strip()}"
            )
    return result


def key_inventory(game_dir: Path) -> set[tuple[str, str]]:
    path = game_dir / "chitin.key"
    data = path.read_bytes()
    if len(data) < 0x18 or data[:8] != b"KEY V1  ":
        raise VerificationError(f"{path} is not a KEY V1 resource index")
    count = struct.unpack_from("<I", data, 0x0C)[0]
    offset = struct.unpack_from("<I", data, 0x14)[0]
    section(data, offset, count, 0x0E, "chitin.key resource table")
    extension_by_type = {1007: "BCS", 1009: "CRE", 1010: "ARE", 1011: "DLG"}
    result: set[tuple[str, str]] = set()
    for index in range(count):
        base = offset + index * 0x0E
        extension = extension_by_type.get(struct.unpack_from("<H", data, base + 8)[0])
        if extension:
            result.add((cstring(data[base : base + 8]).upper(), extension))
    return result


class ResourceStore:
    def __init__(self, game_dir: Path, work_dir: Path) -> None:
        self.game_dir = game_dir
        self.override = game_dir / "override"
        self.weidu = game_dir / "weidu.exe"
        if not self.weidu.is_file():
            raise VerificationError(f"target WeiDU is missing: {self.weidu}")
        self.inventory = key_inventory(game_dir)
        self.work_dir = work_dir
        self.extract_dir = work_dir / "extracted"
        self.extract_dir.mkdir()

    @staticmethod
    def split_name(resource: str) -> tuple[str, str]:
        path = Path(resource)
        if not path.suffix:
            raise VerificationError(f"resource has no extension: {resource}")
        return path.stem.upper(), path.suffix[1:].upper()

    def loose_path(self, resource: str) -> Path | None:
        direct = self.override / resource
        if direct.is_file():
            return direct
        wanted = resource.casefold()
        # Windows is case-insensitive, but this also keeps fixture behavior
        # deterministic under Python environments with different semantics.
        return next(
            (path for path in self.override.glob("*") if path.name.casefold() == wanted),
            None,
        )

    def exists(self, resource: str) -> bool:
        resref, extension = self.split_name(resource)
        return self.loose_path(resource) is not None or (resref, extension) in self.inventory

    def materialize(self, resource: str) -> Path:
        loose = self.loose_path(resource)
        if loose is not None:
            return loose
        if not self.exists(resource):
            raise VerificationError(f"resource is missing: {resource}")
        output = self.extract_dir / resource.upper()
        if output.is_file():
            return output
        result = subprocess.run(
            [
                str(self.weidu),
                "--game",
                str(self.game_dir),
                "--biff-get",
                resource,
                "--out",
                str(self.extract_dir),
                "--no-exit-pause",
            ],
            cwd=self.extract_dir,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=60,
            check=False,
        )
        found = next(
            (
                path
                for path in self.extract_dir.glob("*")
                if path.name.casefold() == resource.casefold()
            ),
            None,
        )
        if found is None:
            detail = (result.stderr or result.stdout).strip()
            raise VerificationError(f"WeiDU could not extract {resource}: {detail}")
        return found

    def read_bytes(self, resource: str) -> bytes:
        return self.materialize(resource).read_bytes()

    def loose_scan_candidates(self) -> set[str]:
        candidates: set[str] = set()
        for path in self.override.glob("*"):
            if not path.is_file() or path.suffix.upper() not in (".BCS", ".DLG"):
                continue
            raw = path.read_bytes().lower()
            if any(needle in raw for needle in ROOT_BINARY_NEEDLES):
                candidates.add(path.name.upper())
        return candidates

    def biff_scan_candidates(self) -> set[str]:
        """Content-screen only BIFFed BCS/DLG resources with the target WeiDU."""

        search_dir = self.work_dir / "biff-search"
        search_dir.mkdir()
        result = subprocess.run(
            [
                str(self.weidu),
                "--game",
                str(self.game_dir),
                "--biff-type",
                "BCS",
                "--biff-type",
                "DLG",
                "--biff-str",
                BIFF_ROOT_QUERY,
                "--no-exit-pause",
            ],
            cwd=search_dir,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=180,
            check=False,
        )
        if result.returncode:
            detail = (result.stderr or result.stdout).strip()
            raise VerificationError(f"WeiDU BIFF root screening failed: {detail}")
        output = "\n".join(part for part in (result.stdout, result.stderr) if part)
        candidates = parse_biff_search_output(output)
        impossible = sorted(
            resource
            for resource in candidates
            if self.split_name(resource) not in self.inventory
        )
        if impossible:
            raise VerificationError(
                "WeiDU BIFF screening returned resources absent from chitin.key: "
                + ", ".join(impossible)
            )
        return candidates


class DecompiledResources:
    def __init__(self, store: ResourceStore, work_dir: Path) -> None:
        self.store = store
        self.output_dir = work_dir / "decompiled"
        self.output_dir.mkdir()

    def decompile(self, resources: set[str]) -> dict[str, str]:
        existing = sorted(resource for resource in resources if self.store.exists(resource))
        paths = [self.store.materialize(resource) for resource in existing]
        for start in range(0, len(paths), 30):
            chunk = paths[start : start + 30]
            result = subprocess.run(
                [
                    str(self.store.weidu),
                    "--game",
                    str(self.store.game_dir),
                    *map(str, chunk),
                    "--no-exit-pause",
                ],
                cwd=self.output_dir,
                capture_output=True,
                text=True,
                errors="replace",
                timeout=120,
                check=False,
            )
            if result.returncode:
                detail = (result.stderr or result.stdout).strip()
                raise VerificationError(f"WeiDU decompilation failed: {detail}")

        texts: dict[str, str] = {}
        for resource in existing:
            resref, extension = self.store.split_name(resource)
            output_extension = ".baf" if extension == "BCS" else ".d"
            output = next(
                (
                    path
                    for path in self.output_dir.glob("*")
                    if path.stem.casefold() == resref.casefold()
                    and path.suffix.casefold() == output_extension
                ),
                None,
            )
            if output is None:
                raise VerificationError(f"WeiDU did not decompile {resource}")
            texts[resource] = output.read_text(encoding="utf-8", errors="replace")
        return texts


@dataclass(frozen=True)
class Container:
    name: str
    x: int
    y: int
    kind: int
    lock_difficulty: int
    trap_removal: int
    item_count: int
    bbox: tuple[int, int, int, int]
    trap_location: tuple[int, int]
    vertices: tuple[tuple[int, int], ...]


def bd4300_import_geometry_ok(container: Container) -> bool:
    """Match the audited local import container, including vertex order."""

    return (
        container.name.casefold() == "k#importcontainer"
        and container.item_count == 0
        and (container.x, container.y, container.kind) == (88, 76, 8)
        and (container.lock_difficulty, container.trap_removal) == (100, 100)
        and container.bbox == (72, 26, 120, 58)
        and container.trap_location == (80, 70)
        and container.vertices
        == ((111, 58), (72, 45), (82, 26), (120, 39))
    )


def parse_containers(data: bytes, label: str) -> list[Container]:
    if len(data) < 0x84 or data[:8] != b"AREAV1.0":
        raise VerificationError(f"{label} is not an ARE V1.0 resource")
    container_offset = struct.unpack_from("<I", data, 0x70)[0]
    container_count = struct.unpack_from("<H", data, 0x74)[0]
    item_count = struct.unpack_from("<H", data, 0x76)[0]
    item_offset = struct.unpack_from("<I", data, 0x78)[0]
    vertex_offset = struct.unpack_from("<I", data, 0x7C)[0]
    vertex_count = struct.unpack_from("<H", data, 0x80)[0]
    section(data, container_offset, container_count, 0xC0, f"{label} container table")
    section(data, item_offset, item_count, 0x14, f"{label} item table")
    section(data, vertex_offset, vertex_count, 4, f"{label} vertex table")
    result = []
    for index in range(container_count):
        base = container_offset + index * 0xC0
        first_item = struct.unpack_from("<I", data, base + 0x40)[0]
        live_items = struct.unpack_from("<I", data, base + 0x44)[0]
        first_vertex = struct.unpack_from("<I", data, base + 0x50)[0]
        live_vertices = struct.unpack_from("<H", data, base + 0x54)[0]
        if first_item + live_items > item_count:
            raise VerificationError(f"{label} container {index} has an invalid item run")
        if first_vertex + live_vertices > vertex_count:
            raise VerificationError(f"{label} container {index} has an invalid vertex run")
        vertices = tuple(
            struct.unpack_from("<HH", data, vertex_offset + (first_vertex + i) * 4)
            for i in range(live_vertices)
        )
        result.append(
            Container(
                cstring(data[base : base + 32]),
                *struct.unpack_from("<HH", data, base + 0x20),
                struct.unpack_from("<H", data, base + 0x24)[0],
                struct.unpack_from("<H", data, base + 0x26)[0],
                struct.unpack_from("<H", data, base + 0x2E)[0],
                live_items,
                struct.unpack_from("<HHHH", data, base + 0x38),
                struct.unpack_from("<HH", data, base + 0x34),
                vertices,
            )
        )
    return result


def baf_blocks(text: str) -> list[tuple[str, str]]:
    return [
        (match.group("triggers"), match.group("actions"))
        for match in re.finditer(
            r"(?ms)^IF\s*$\s*(?P<triggers>.*?)^THEN\s*$\s*(?P<actions>.*?)^END\s*$",
            text,
        )
    ]


@dataclass(frozen=True)
class DialogState:
    trigger: str
    body: str


def dialog_states(text: str, label: str) -> dict[int, DialogState]:
    header = re.compile(
        r"(?ms)^IF(?:\s+WEIGHT\s+#\d+)?\s+~(?P<trigger>.*?)~\s+THEN\s+BEGIN\s+"
        r"(?P<number>\d+)\b[^\n]*\n"
    )
    states: dict[int, DialogState] = {}
    for match in header.finditer(text):
        end = re.search(r"(?m)^END\s*$", text[match.end() :])
        if end is None:
            raise VerificationError(f"unterminated {label} state {match.group('number')}")
        number = int(match.group("number"))
        if number in states:
            raise VerificationError(f"duplicate {label} state {number}")
        body_end = match.end() + end.start()
        states[number] = DialogState(match.group("trigger"), text[match.end() : body_end])
    return states


def dialog_transitions(state: DialogState) -> list[tuple[str, str]]:
    return [
        (match.group("trigger"), match.group("route"))
        for match in re.finditer(
            r"(?ms)^\s*IF\s+~(?P<trigger>.*?)~\s+THEN\s+"
            r"(?P<route>.*?)(?=^\s*IF\s+~|\Z)",
            state.body,
        )
    ]


def trigger_atoms(trigger: str) -> list[str] | None:
    """Split a decompiled trigger expression into balanced function calls."""

    text = "\n".join(line.split("//", 1)[0] for line in trigger.splitlines())
    atoms = []
    index = 0
    while index < len(text):
        while index < len(text) and text[index].isspace():
            index += 1
        if index == len(text):
            break
        start = index
        if text[index] == "!":
            index += 1
            while index < len(text) and text[index].isspace():
                index += 1
        name = re.match(r"[A-Za-z_][A-Za-z0-9_]*", text[index:])
        if name is None:
            return None
        index += name.end()
        while index < len(text) and text[index].isspace():
            index += 1
        if index == len(text) or text[index] != "(":
            return None
        depth = 0
        quoted = False
        while index < len(text):
            character = text[index]
            if character == '"':
                quoted = not quoted
            elif not quoted:
                if character == "(":
                    depth += 1
                elif character == ")":
                    depth -= 1
                    if depth == 0:
                        index += 1
                        break
                    if depth < 0:
                        return None
            index += 1
        if depth != 0 or quoted:
            return None
        if index < len(text) and not text[index].isspace():
            return None
        atoms.append(re.sub(r"\s+", " ", text[start:index]).strip())
    return atoms


def false_gated(trigger: str) -> bool:
    """Return true only for an exact, top-level, non-negated False()."""

    atoms = trigger_atoms(trigger)
    if atoms is None:
        return False
    found_top_level_false = False
    index = 0
    while index < len(atoms):
        atom = atoms[index]
        or_group = re.fullmatch(r"OR\s*\(\s*(\d+)\s*\)", atom, re.IGNORECASE)
        if or_group:
            count = int(or_group.group(1))
            if count <= 0 or index + count >= len(atoms):
                return False
            members = atoms[index + 1 : index + count + 1]
            if any(re.match(r"!?\s*OR\b", member, re.IGNORECASE) for member in members):
                return False
            index += count + 1
            continue
        if re.match(r"!?\s*OR\b", atom, re.IGNORECASE):
            return False
        if re.fullmatch(r"False\s*\(\s*\)", atom, re.IGNORECASE):
            found_top_level_false = True
        index += 1
    return found_top_level_false


def canonical_code(text: str) -> str:
    lines = []
    for line in text.splitlines():
        code = line.split("//", 1)[0].strip()
        if code:
            lines.append(re.sub(r"\s+", " ", code))
    return "\n".join(lines)


def response_action_lines(actions: str) -> list[str]:
    """Return canonical BAF response actions without the RESPONSE weight line."""

    return [
        line
        for line in canonical_code(actions).splitlines()
        if not re.fullmatch(r"RESPONSE\s+#\d+", line, re.IGNORECASE)
    ]


def harmless_exit_route(route: str) -> bool:
    return bool(re.fullmatch(r"EXIT", canonical_code(route), re.IGNORECASE))


def guard_trigger_is_fail_closed(trigger: str) -> bool:
    """Accept only the exact two-way missing-local-container guard."""

    lines = canonical_code(trigger).splitlines()
    patterns = (
        re.compile(r"OR\s*\(\s*2\s*\)", re.IGNORECASE),
        re.compile(
            r'!\s*AreaCheck\s*\(\s*"BD4300"\s*\)', re.IGNORECASE
        ),
        re.compile(
            r'!\s*(?:Exists|ObjectExists)\s*\(\s*"K#ImportContainer"\s*\)',
            re.IGNORECASE,
        ),
    )
    return len(lines) == len(patterns) and all(
        pattern.fullmatch(line) for pattern, line in zip(patterns, lines)
    )


def guard_actions_are_fail_closed(actions: str) -> bool:
    """Accept only the five audited guard actions, once and in exact order."""

    canonical_lines = canonical_code(actions).splitlines()
    response_count = sum(
        bool(re.fullmatch(r"RESPONSE\s+#\d+", line, re.IGNORECASE))
        for line in canonical_lines
    )
    lines = response_action_lines(actions)
    patterns = (
        re.compile(r"DisplayString\s*\([^\r\n]*\)", re.IGNORECASE),
        re.compile(r"FadeFromColor\s*\([^\r\n]*\)", re.IGNORECASE),
        re.compile(r"EndCutSceneMode\s*\(\s*\)", re.IGNORECASE),
        re.compile(
            r'SetGlobal\s*\(\s*"CSR_ENDING_FAILED"\s*,\s*"GLOBAL"\s*,\s*1\s*\)',
            re.IGNORECASE,
        ),
        re.compile(r"DestroySelf\s*\(\s*\)", re.IGNORECASE),
    )
    return response_count == 1 and len(lines) == len(patterns) and all(
        pattern.fullmatch(line) for pattern, line in zip(patterns, lines)
    )


def dazzo_endpoint_is_ordered(
    route: str, platform: str, once_flag: str, journal: int
) -> bool:
    """Require exactly one whitelisted platform endpoint followed by EXIT."""

    if not once_flag:
        return False
    code = canonical_code(route)
    transition = re.fullmatch(
        r"DO\s+~(?P<actions>.*?)~\s+EXIT", code, re.IGNORECASE | re.DOTALL
    )
    if transition is None:
        return False
    actions = canonical_code(transition.group("actions")).splitlines()
    patterns = [
        re.compile(
            rf'SetGlobal\s*\(\s*"{re.escape(once_flag)}"\s*,\s*"GLOBAL"\s*,\s*1\s*\)',
            re.IGNORECASE,
        ),
        re.compile(rf"EraseJournalEntry\s*\(\s*{journal}\s*\)", re.IGNORECASE),
        re.compile(r"StartCutSceneMode\s*\(\s*\)", re.IGNORECASE),
        re.compile(r"FadeToColor\s*\([^\r\n]*\)", re.IGNORECASE),
    ]
    if platform == "eet":
        patterns.append(
            re.compile(
                r'CreateCreatureObject\s*\(\s*"CSRETBGT"\s*,\s*Player1\s*,'
                r"\s*0\s*,\s*0\s*,\s*0\s*\)",
                re.IGNORECASE,
            )
        )
    elif platform == "standalone":
        patterns.extend(
            (
                re.compile(r"EndCutSceneMode\s*\(\s*\)", re.IGNORECASE),
                re.compile(r"ContinueGame\s*\(\s*FALSE\s*\)", re.IGNORECASE),
                re.compile(r"EndCredits\s*\(\s*\)", re.IGNORECASE),
            )
        )
    else:
        raise ValueError(f"unknown endpoint platform {platform!r}")
    return len(actions) == len(patterns) and all(
        pattern.fullmatch(action)
        for pattern, action in zip(patterns, actions)
    )


def bence_terminal_problems(states: dict[int, DialogState]) -> list[str]:
    """Check every transition in each retired murder/arrest terminal state."""

    problems = []
    for number, expected_count in BENCE_TERMINAL_COUNTS.items():
        transitions = dialog_transitions(states.get(number, DialogState("", "")))
        if len(transitions) != expected_count:
            problems.append(
                f"state {number} has {len(transitions)} transition(s), expected {expected_count}"
            )
        for index, (_, route) in enumerate(transitions):
            if not harmless_exit_route(route):
                problems.append(
                    f"state {number} transition {index} is not a harmless EXIT: "
                    f"{canonical_code(route)}"
                )
    return problems


def root_fingerprints(texts: dict[str, str]) -> dict[str, dict[str, int]]:
    result = {}
    for resource, text in texts.items():
        counts = {
            name: len(pattern.findall(text)) for name, pattern in ROOT_PATTERNS.items()
        }
        counts = {name: count for name, count in counts.items() if count}
        if counts:
            result[resource] = counts
    return result


def root_inventory_problems(texts: dict[str, str]) -> list[str]:
    """Compare classified roots both ways; only C0Aura may be absent."""

    actual = root_fingerprints(texts)
    problems = []
    for resource, expected in sorted(KNOWN_ROOT_COUNTS.items()):
        if resource in OPTIONAL_ROOT_RESOURCES and resource not in texts:
            continue
        found = actual.get(resource)
        if found is None:
            problems.append(f"missing classified {resource}: expected {expected}")
        elif found != expected:
            problems.append(f"{resource}: expected {expected}, found {found}")
    for resource, counts in sorted(actual.items()):
        if resource not in KNOWN_ROOT_COUNTS:
            problems.append(f"unclassified {resource}={counts}")
    return problems


def same_dialog_goto_inbound(
    texts: dict[str, str],
) -> Counter[tuple[str, int, int]]:
    """Inventory direct GOTO edges into classified states of the same DLG."""

    result: Counter[tuple[str, int, int]] = Counter()
    for resource, text in texts.items():
        if not resource.upper().endswith(".DLG"):
            continue
        dialog = resource.rsplit(".", 1)[0].upper()
        targets = TARGET_CODA_STATES.get(dialog)
        if targets is None:
            continue
        for source, state in dialog_states(text, dialog).items():
            for _, route in dialog_transitions(state):
                route = re.sub(r"/\*.*?\*/", "", route, flags=re.DOTALL)
                direct = re.search(r"\bGOTO\s+(\d+)\s*$", route, re.IGNORECASE)
                if direct and int(direct.group(1)) in targets:
                    result[(resource.upper(), source, int(direct.group(1)))] += 1
    return result


def goto_inbound_problems(
    texts: dict[str, str],
    expected: Counter[tuple[str, int, int]] = EXPECTED_GOTO_INBOUND,
) -> list[str]:
    """Compare the frozen same-dialog GOTO graph in both directions."""

    actual = same_dialog_goto_inbound(texts)
    problems = []
    for resource, source, target in sorted(set(expected) | set(actual)):
        edge = (resource, source, target)
        if actual[edge] != expected[edge]:
            problems.append(
                f"{resource}:{source}->{target}: expected {expected[edge]}, "
                f"found {actual[edge]}"
            )
    return problems


def external_inbound(texts: dict[str, str]) -> Counter[tuple[str, str, int]]:
    result: Counter[tuple[str, str, int]] = Counter()
    pattern = re.compile(r"\bEXTERN\s+~([^~]+)~\s+(\d+)\b", re.IGNORECASE)
    for resource, text in texts.items():
        if not resource.endswith(".DLG"):
            continue
        for target, state_text in pattern.findall(text):
            target = target.upper()
            state = int(state_text)
            if state in TARGET_CODA_STATES.get(target, set()):
                result[(resource, target, state)] += 1
    return result


def load_manifest(path: Path) -> dict[str, str]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, dict) and isinstance(raw.get("resources"), dict):
        raw = raw["resources"]
    if not isinstance(raw, dict):
        raise VerificationError("baseline manifest must be a JSON object")
    result = {}
    for key, value in raw.items():
        if isinstance(value, dict):
            value = value.get("sha256")
        if not isinstance(value, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", value):
            raise VerificationError(f"invalid SHA-256 manifest entry for {key}")
        result[Path(key).name.upper()] = value.lower()
    return result


class Reporter:
    def __init__(self) -> None:
        self.failures = 0

    def check(self, label: str, passed: bool, detail: str = "") -> None:
        if not passed:
            self.failures += 1
        suffix = f" ({detail})" if detail else ""
        print(f"{'PASS' if passed else 'FAIL'}: {label}{suffix}")


def check_hashes(
    report: Reporter,
    store: ResourceStore,
    platform: str,
    manifest_path: Path | None,
) -> None:
    if manifest_path is None:
        report.check("optional pre-install SHA-256 manifest not requested", True)
        return
    manifest = load_manifest(manifest_path)
    required = set(HASH_REQUIRED_COMMON)
    required.update(HASH_REQUIRED_EET if platform == "eet" else HASH_REQUIRED_STANDALONE)
    missing = sorted(required.difference(manifest))
    report.check(
        "baseline manifest covers every immutable ending resource",
        not missing,
        ", ".join(missing),
    )
    for resource, expected in sorted(manifest.items()):
        if not store.exists(resource):
            report.check(f"{resource} matches its pre-install SHA-256", False, "missing")
            continue
        actual = hashlib.sha256(store.read_bytes(resource)).hexdigest()
        report.check(
            f"{resource} matches its pre-install SHA-256",
            actual == expected,
            f"expected {expected}, found {actual}",
        )


def check_root_classification(report: Reporter, texts: dict[str, str]) -> None:
    problems = root_inventory_problems(texts) + goto_inbound_problems(texts)
    report.check(
        "installed coda-root and same-dialog GOTO inventories match the frozen classification",
        not problems,
        "; ".join(problems[:8]),
    )

    inbound = external_inbound(texts)
    report.check(
        "all external inbound references to identified coda states are classified",
        inbound == EXPECTED_EXTERNAL_INBOUND,
        f"expected {dict(EXPECTED_EXTERNAL_INBOUND)}, found {dict(inbound)}",
    )


def check_bd4300(report: Reporter, text: str, platform: str) -> None:
    timers = re.findall(
        r'SetGlobalTimer\s*\(\s*"bd_mdd1341a_ot_timer"\s*,\s*"bd4300"\s*,\s*([^\)]+)\)',
        text,
        re.IGNORECASE,
    )
    blocks = baf_blocks(text)
    aura_blocks = [
        (trigger, actions)
        for trigger, actions in blocks
        if re.search(r'Global\s*\(\s*"bd_plot"\s*,\s*"global"\s*,\s*586\s*\)', trigger, re.I)
        and re.search(r'Global\s*\(\s*"bd_ot2_C0Aura"\s*,\s*"bd4300"\s*,\s*0\s*\)', trigger, re.I)
        and re.search(r'IsValidForPartyDialogue\s*\(\s*"C0Aura"\s*\)', trigger, re.I)
        and re.search(r'SetGlobalTimer\s*\(\s*"bd_mdd1341a_ot_timer"', actions, re.I)
        and re.search(r'SetGlobal\s*\(\s*"bd_ot2_C0Aura"\s*,\s*"bd4300"\s*,\s*1\s*\)', actions, re.I)
        and re.search(r'DisplayStringHead\s*\(\s*"C0Aura"', actions, re.I)
    ]
    expected = expected_timer_count(len(aura_blocks))
    report.check(
        "BD4300 has 17 vanilla victory timers plus zero or one exact C0Aura bark",
        len(aura_blocks) in (0, 1) and len(timers) == expected,
        f"platform {platform}, timers {len(timers)}, C0Aura anchors {len(aura_blocks)}",
    )
    report.check(
        "every BD4300 victory-bark timer is numeric 2",
        len(timers) == expected and all(value.strip() == "2" for value in timers),
        f"values {[value.strip() for value in timers]}",
    )

    convergence = [
        (trigger, actions)
        for trigger, actions in blocks
        if re.search(r'Global\s*\(\s*"bd_plot"\s*,\s*"global"\s*,\s*586\s*\)', trigger, re.I)
        and re.search(r'GlobalTimerExpired\s*\(\s*"bd_mdd1341a_ot_timer"', trigger, re.I)
        and re.search(r'SetGlobal\s*\(\s*"bd_plot"\s*,\s*"global"\s*,\s*587\s*\)', actions, re.I)
    ]
    report.check("BD4300 retains one 586-to-587 timer convergence", len(convergence) == 1)

    for companion in ("Corwin", "Neera"):
        global_name = f"bd_{companion}Romance6"
        relevant = [
            (trigger, actions)
            for trigger, actions in blocks
            if re.search(re.escape(global_name), trigger, re.IGNORECASE)
        ]
        setter = [
            pair
            for pair in relevant
            if re.search(
                rf'SetGlobal\s*\(\s*"{re.escape(global_name)}"\s*,\s*"GLOBAL"\s*,\s*1\s*\)',
                pair[1],
                re.IGNORECASE,
            )
        ]
        finale = [
            pair for pair in relevant if re.search(r"StartDialogNoSet", pair[1], re.I)
        ]
        report.check(
            f"{companion} Romance6 setter and forced finale are both False-gated",
            len(relevant) == 2
            and len(setter) == 1
            and len(finale) == 1
            and all(false_gated(trigger) for trigger, _ in relevant),
            f"blocks {len(relevant)}, setters {len(setter)}, finales {len(finale)}",
        )
        all_sets = re.findall(
            rf'SetGlobal\s*\(\s*"{re.escape(global_name)}"\s*,\s*"GLOBAL"\s*,\s*(-?\d+)\s*\)',
            text,
            re.IGNORECASE,
        )
        report.check(
            f"BD4300 does not fake {companion} Romance6 completion",
            all_sets == ["1"],
            f"writes {all_sets}",
        )


def check_dialog_cleanup(report: Reporter, texts: dict[str, str], platform: str) -> None:
    journal = 266908 if platform == "eet" else 66908
    delanc = dialog_states(texts.get("BDDELANC.DLG", ""), "BDDELANC")
    public_present = all(number in delanc for number in range(77, 84))
    state77 = delanc.get(77, DialogState("", ""))
    state79 = delanc.get(79, DialogState("", ""))
    state83 = delanc.get(83, DialogState("", ""))
    public_ok = (
        public_present
        and bool(re.search(r"GlobalLT\s*\([^\)]*590", state77.trigger, re.I))
        and len(re.findall(r'SetGlobal\s*\([^\)]*"bd_plot"[^\)]*590', state77.body, re.I)) == 3
        and len(re.findall(rf"AddJournalEntry\s*\(\s*{journal}", state79.body, re.I)) == 2
        and bool(re.search(r"EXTERN\s+~BDBENCE~\s+64", state83.body, re.I))
    )
    report.check(
        f"BDDELANC 77-83 public victory chain and journal {journal} survive",
        public_ok,
    )
    report.check(
        "BDDELANC private Waterdeep states 95 and 104 are False-gated",
        all(number in delanc and false_gated(delanc[number].trigger) for number in (95, 104)),
    )

    bence = dialog_states(texts.get("BDBENCE.DLG", ""), "BDBENCE")
    state64 = bence.get(64, DialogState("", ""))
    state65 = bence.get(65, DialogState("", ""))
    transitions65 = dialog_transitions(state65)
    route65 = transitions65[0][1] if len(transitions65) == 1 else ""
    report.check(
        "BDBENCE 64-65 public celebration exchange survives",
        bool(re.search(r"GOTO\s+65", state64.body, re.I))
        and bool(re.search(r"\bSAY\s+#\d+", state65.body, re.I)),
    )
    report.check(
        "BDBENCE 65 restores soldiers, exits Bence, and never enters 66",
        len(transitions65) == 1
        and bool(re.search(r'SoundActivate\s*\(\s*"SS_Soldier"\s*,\s*TRUE\s*\)', route65, re.I))
        and bool(re.search(r"\bEscapeArea\s*\(\s*\)", route65, re.I))
        and bool(re.search(r"\bEXIT\b", route65, re.I))
        and not re.search(r"GOTO\s+66\b", route65, re.I),
    )
    retired_bence = (6, 9, 10, 67, 68, 70, 71, 73)
    report.check(
        "all BDBENCE murder and arrest launch states are False-gated",
        all(number in bence and false_gated(bence[number].trigger) for number in retired_bence),
    )
    terminal_problems = bence_terminal_problems(bence)
    report.check(
        "BDBENCE murder and arrest terminal transitions are harmless EXITs",
        not terminal_problems,
        "; ".join(terminal_problems),
    )

    dazzo = dialog_states(texts.get("BDDAZZO.DLG", ""), "BDDAZZO")
    state0 = dazzo.get(0, DialogState("", ""))
    once_matches = re.findall(
        r'Global\s*\(\s*"([^"]*CSR[^"]*(?:END|ENDING)[^"]*)"\s*,\s*"GLOBAL"\s*,\s*0\s*\)',
        state0.trigger,
        re.IGNORECASE,
    )
    report.check(
        "BDDAZZO state 0 requires plot 590 and one component once flag",
        len(once_matches) == 1
        and bool(re.search(r'Global\s*\(\s*"bd_plot"\s*,\s*"GLOBAL"\s*,\s*590\s*\)', state0.trigger, re.I)),
        f"once flags {once_matches}",
    )
    endpoint_routes = []
    for number in (2, 3):
        transitions = dialog_transitions(dazzo.get(number, DialogState("", "")))
        endpoint_routes.append(transitions[0][1] if len(transitions) == 1 else "")
    same_endpoint = (
        all(endpoint_routes)
        and canonical_code(endpoint_routes[0]) == canonical_code(endpoint_routes[1])
    )
    report.check("BDDAZZO states 2 and 3 share one endpoint action contract", same_endpoint)
    for number, route in zip((2, 3), endpoint_routes):
        flag = once_matches[0] if len(once_matches) == 1 else ""
        ordered = dazzo_endpoint_is_ordered(route, platform, flag, journal)
        report.check(
            f"BDDAZZO state {number} has one exact ordered {platform} endpoint",
            ordered and not re.search(r"bdcut60", route, re.I),
        )
    endpoint = endpoint_routes[0] if same_endpoint else ""
    if platform == "eet":
        creates = re.findall(
            r'CreateCreatureObject\s*\(\s*"CSRETBGT"\s*,\s*Player1\s*,\s*0\s*,\s*0\s*,\s*0\s*\)',
            endpoint,
            re.I,
        )
        report.check(
            "EET Dazzo endpoint creates exactly one CSRETBGT carrier after the fade",
            len(creates) == 1
            and dazzo_endpoint_is_ordered(
                endpoint,
                platform,
                once_matches[0] if len(once_matches) == 1 else "",
                journal,
            ),
        )
        report.check("EET Dazzo endpoint does not run native credits", not re.search(r"EndCredits", endpoint, re.I))
    else:
        report.check(
            "standalone Dazzo endpoint uses one exact native terminal action order",
            dazzo_endpoint_is_ordered(
                endpoint,
                platform,
                once_matches[0] if len(once_matches) == 1 else "",
                journal,
            ),
        )
        report.check(
            "standalone Dazzo endpoint has no EET K# or carrier dependency",
            not re.search(r"K#|CSRETBGT|MoveToCampaign", endpoint, re.I),
        )

    rumor = dialog_states(texts.get("BDRUMOR3.DLG", ""), "BDRUMOR3")
    report.check(
        "BDRUMOR3 hooded-man rumors 7, 20, and 37 are False-gated",
        all(number in rumor and false_gated(rumor[number].trigger) for number in (7, 20, 37)),
    )
    report.check(
        "unrelated BDRUMOR3 chapter-8 and chapter-10 rumors remain live",
        0 in rumor
        and 36 in rumor
        and not false_gated(rumor[0].trigger)
        and not false_gated(rumor[36].trigger),
    )


def check_debug_and_palace(report: Reporter, texts: dict[str, str]) -> None:
    debug_baf = texts.get("BDDEBUG.BCS", "")
    blocks = baf_blocks(debug_baf)
    for suffix in ("dream", "cell"):
        name = f"bd_debug_move_to_{suffix}"
        matches = [
            (trigger, actions)
            for trigger, actions in blocks
            if re.search(
                rf'Global\s*\(\s*"{name}"\s*,\s*"global"\s*,\s*1\s*\)', trigger, re.I
            )
        ]
        report.check(
            f"BDDEBUG {suffix} launcher block is False-gated",
            len(matches) == 1 and false_gated(matches[0][0]),
            f"found {len(matches)}",
        )
    portal_live = [
        trigger
        for trigger, _ in blocks
        if re.search(r'Global\s*\(\s*"bd_debug_move_to_portal"[^\)]*,\s*1\s*\)', trigger, re.I)
        and not false_gated(trigger)
    ]
    report.check("unrelated BDDEBUG portal launcher remains live", len(portal_live) == 1)

    debug_dialog = dialog_states(texts.get("BDDEBUG.DLG", ""), "BDDEBUG")
    state10 = debug_dialog.get(10, DialogState("", ""))
    transitions = dialog_transitions(state10)
    for suffix in ("dream", "cell"):
        setters = [
            (trigger, route)
            for trigger, route in transitions
            if re.search(rf'SetGlobal\s*\(\s*"bd_debug_move_to_{suffix}"', route, re.I)
        ]
        report.check(
            f"all four BDDEBUG {suffix} dialogue setters are False-gated",
            len(setters) == 4 and all(false_gated(trigger) for trigger, _ in setters),
            f"found {len(setters)}",
        )

    palace_blocks = baf_blocks(texts.get("BDPALACE.BCS", ""))
    entar = [
        trigger
        for trigger, actions in palace_blocks
        if re.search(r'Range\s*\(\s*"BDENTAR"', trigger, re.I)
        and re.search(r'FaceObject\s*\(\s*"BDENTAR"', actions, re.I)
    ]
    report.check(
        "final BDPALACE Entar exit block is False-gated",
        len(entar) == 1 and false_gated(entar[0]),
        f"found {len(entar)}",
    )
    siblings = []
    for name in ("BDLIIA", "BDELTAN", "BDBELT"):
        siblings.extend(
            trigger
            for trigger, actions in palace_blocks
            if re.search(rf'Range\s*\(\s*"{name}"', trigger, re.I)
            and re.search(rf'FaceObject\s*\(\s*"{name}"', actions, re.I)
            and not false_gated(trigger)
        )
    report.check("unrelated BDPALACE duke exit blocks remain live", len(siblings) == 3)


def check_reachability(report: Reporter, texts: dict[str, str]) -> None:
    bence = dialog_states(texts.get("BDBENCE.DLG", ""), "BDBENCE")
    live_launches = []
    for number, state in bence.items():
        for transition_trigger, route in dialog_transitions(state):
            if re.search(r'StartCutSceneEx\s*\(\s*"bdcut(?:60b|61)"', route, re.I):
                live_launches.append(f"BDBENCE:{number}")
    corwin = dialog_states(texts.get("BDCORWIJ.DLG", ""), "BDCORWIJ")
    corwin203 = corwin.get(203, DialogState("", ""))
    corwin203_transitions = dialog_transitions(corwin203)
    corwin_launches = [
        transition_trigger
        for transition_trigger, route in corwin203_transitions
        if re.search(r'StartCutSceneEx\s*\(\s*"bdcut61"', route, re.I)
    ]
    if corwin_launches:
        live_launches.append("BDCORWIJ:203")
    for trigger, actions in baf_blocks(texts.get("BDDEBUG.BCS", "")):
        if re.search(r'StartCutSceneEx\s*\(\s*"bdcut(?:60|61)"', actions, re.I) and not false_gated(trigger):
            live_launches.append("BDDEBUG.BCS")
    dazzo = dialog_states(texts.get("BDDAZZO.DLG", ""), "BDDAZZO")
    if any(re.search(r"bdcut60", dazzo.get(number, DialogState("", "")).body, re.I) for number in (2, 3)):
        live_launches.append("BDDAZZO")
    delanc = dialog_states(texts.get("BDDELANC.DLG", ""), "BDDELANC")
    if any(number not in delanc or not false_gated(delanc[number].trigger) for number in (95, 104)):
        live_launches.append("BDDELANC-private")
    report.check(
        "no reachable production BDCUT60/60B/61 or private Waterdeep root remains",
        not live_launches,
        ", ".join(live_launches),
    )
    report.check(
        "BDCORWIJ state 203 is a harmless direct-entry EXIT",
        203 in corwin
        and len(corwin203_transitions) == 1
        and harmless_exit_route(corwin203_transitions[0][1]),
        f"transitions {len(corwin203_transitions)}, launch transitions {len(corwin_launches)}",
    )
    report.check(
        "unrelated Corwin victory and companion interjection states remain",
        196 in corwin
        and bool(re.search(r"\bSAY\s+#\d+", corwin[196].body, re.I))
        and bool(re.search(r"\bEXIT\b", corwin[196].body, re.I))
        and 204 in corwin,
    )


def check_eet(report: Reporter, store: ResourceStore, texts: dict[str, str]) -> None:
    bd4300 = parse_containers(store.read_bytes("BD4300.ARE"), "BD4300.ARE")
    local = [c for c in bd4300 if c.name.casefold() == "k#importcontainer"]
    geometry = len(local) == 1 and bd4300_import_geometry_ok(local[0])
    report.check(
        "BD4300 has exactly one empty K#ImportContainer with audited geometry",
        geometry,
        f"found {len(local)}",
    )
    bd6100 = parse_containers(store.read_bytes("BD6100.ARE"), "BD6100.ARE")
    destination = [c for c in bd6100 if c.name.casefold() == "k#importcontainer"]
    report.check(
        "BD6100 retains exactly one empty K#ImportContainer destination",
        len(destination) == 1 and destination[0].item_count == 0,
        f"found {len(destination)}",
    )

    original = texts.get("K#TELBGT.BCS", "")
    clone = texts.get("CSRETBGT.BCS", "")
    original_blocks = baf_blocks(original)
    clone_blocks = baf_blocks(clone)
    move_pattern = re.compile(
        r'^\s*MoveContainerContents\s*\(\s*"BD4300\*K#ImportContainer"\s*,\s*'
        r'"BD6100\*K#ImportContainer"\s*\)\s*(?://.*)?$',
        re.IGNORECASE | re.MULTILINE,
    )
    stripped_clone = move_pattern.sub("", clone)
    stripped_blocks = baf_blocks(stripped_clone)
    fidelity = (
        bool(original_blocks)
        and len(stripped_blocks) == len(original_blocks) + 1
        and [canonical_code(t + "\n" + a) for t, a in stripped_blocks[1:]]
        == [canonical_code(t + "\n" + a) for t, a in original_blocks]
    )
    report.check(
        "CSRETBGT clone normalizes only its prepended guard and cross-area move",
        fidelity,
        f"original blocks {len(original_blocks)}, clone blocks {len(clone_blocks)}",
    )
    guard_trigger, guard_actions = stripped_blocks[0] if stripped_blocks else ("", "")
    guard_ok = (
        guard_trigger_is_fail_closed(guard_trigger)
        and guard_actions_are_fail_closed(guard_actions)
    )
    report.check(
        "CSRETBGT begins with the exact fail-closed local-container guard order",
        guard_ok,
    )

    takes = re.findall(
        r'ActionOverride\s*\(\s*"K#ImportContainer"\s*,\s*TakeCreatureItems\s*\(\s*'
        r'(Player[1-6])\s*,\s*ALL\s*\)\s*\)',
        clone,
        re.I,
    )
    report.check(
        "CSRETBGT preserves one TakeCreatureItems action for Player1 through Player6",
        len(takes) == 6 and {name.upper() for name in takes} == {f"PLAYER{i}" for i in range(1, 7)},
        f"found {takes}",
    )
    moves = list(move_pattern.finditer(clone))
    code_lines = canonical_code(clone).splitlines()
    immediate = any(
        "MoveContainerContents(\"BD4300*K#ImportContainer\",\"BD6100*K#ImportContainer\")".casefold()
        in code_lines[index].replace(" ", "").casefold()
        and index + 1 < len(code_lines)
        and re.search(r'StartMovie\s*\(\s*"INTRO15F"', code_lines[index + 1], re.I)
        for index in range(len(code_lines))
    )
    report.check(
        "CSRETBGT has one BD4300-to-BD6100 move immediately before INTRO15F",
        len(moves) == 1
        and immediate
        and len(re.findall(r'StartMovie\s*\(\s*"INTRO15F"', clone, re.I)) == 1
        and len(re.findall(r'MoveToCampaign\s*\(\s*"SoA"', clone, re.I)) == 1,
        f"moves {len(moves)}",
    )

    if store.exists("CSRETBGT.CRE"):
        source_cre = store.read_bytes("K#TELBGT.CRE")
        clone_cre = store.read_bytes("CSRETBGT.CRE")
        shape_ok = len(source_cre) == len(clone_cre) and len(clone_cre) >= 0x2A0
        masked_source = bytearray(source_cre)
        masked_clone = bytearray(clone_cre)
        if shape_ok:
            for start, end in ((0x248, 0x250), (0x280, 0x2A0)):
                masked_source[start:end] = b"\0" * (end - start)
                masked_clone[start:end] = b"\0" * (end - start)
        script = cstring(clone_cre[0x248:0x250]).upper() if shape_ok else ""
        source_dv = cstring(source_cre[0x280:0x2A0]).upper() if shape_ok else ""
        clone_dv = cstring(clone_cre[0x280:0x2A0]).upper() if shape_ok else ""
        cre_ok = (
            shape_ok
            and masked_source == masked_clone
            and script == "CSRETBGT"
            and clone_dv in (source_dv, "CSRETBGT")
        )
    else:
        script = "missing"
        clone_dv = "missing"
        cre_ok = False
    report.check(
        "CSRETBGT.CRE differs only in override script and optional death variable",
        cre_ok,
        f"script {script}, dv {clone_dv}",
    )

    ar0602 = texts.get("AR0602.BCS", "")
    import_moves = re.findall(
        r'MoveContainerContents\s*\(\s*"BD6100\*K#ImportContainer"\s*,\s*'
        r'"AR0602\*K#ImportContainer"\s*\)',
        ar0602,
        re.I,
    )
    report.check("AR0602 retains exactly its BD6100-to-AR0602 import move", len(import_moves) == 1)


def check_standalone(report: Reporter, texts: dict[str, str]) -> None:
    native = texts.get("BD6100.BCS", "")
    triples = re.findall(
        r"EndCutSceneMode\s*\(\s*\)\s*ContinueGame\s*\(\s*FALSE\s*\)\s*EndCredits\s*\(\s*\)",
        canonical_code(native),
        re.I,
    )
    report.check("native standalone BD6100 retains both terminal action triples", len(triples) == 2)
    report.check(
        "native standalone BD6100 contains no EET campaign handoff",
        not re.search(r"K#TELBGT|MoveToCampaign", native, re.I),
    )


def verify(
    game_dir: Path, requested_platform: str, manifest_path: Path | None
) -> int:
    report = Reporter()
    if not game_dir.is_dir():
        raise VerificationError(f"game directory does not exist: {game_dir}")
    with tempfile.TemporaryDirectory(prefix="csr-ending-verifier-") as temporary:
        store = ResourceStore(game_dir, Path(temporary))
        signatures = tuple(store.exists(resource) for resource in EET_ANCHORS)
        platform = classify_platform(signatures, requested_platform)
        report.check(
            f"complete three-anchor platform signature resolves to {platform}",
            True,
            ", ".join(EET_ANCHORS),
        )

        candidates = store.loose_scan_candidates()
        candidates.update(store.biff_scan_candidates())
        candidates.update(COMMON_TEXT_RESOURCES)
        candidates.update(KNOWN_ROOT_COUNTS)
        candidates.update(source for source, _, _ in EXPECTED_EXTERNAL_INBOUND)
        candidates.update(EET_TEXT_RESOURCES if platform == "eet" else STANDALONE_TEXT_RESOURCES)
        texts = DecompiledResources(store, Path(temporary)).decompile(candidates)

        check_hashes(report, store, platform, manifest_path)
        check_root_classification(report, texts)
        check_bd4300(report, texts.get("BD4300.BCS", ""), platform)
        check_dialog_cleanup(report, texts, platform)
        check_debug_and_palace(report, texts)
        check_reachability(report, texts)
        if platform == "eet":
            check_eet(report, store, texts)
        else:
            check_standalone(report, texts)

    print(f"SUMMARY: {report.failures} failure(s)")
    return 1 if report.failures else 0


class ContractFixtureTests(unittest.TestCase):
    """Focused fixtures for the binary/text primitives used by the verifier."""

    def test_platform_signature_is_all_or_nothing(self) -> None:
        self.assertEqual(classify_platform((True, True, True), "auto"), "eet")
        self.assertEqual(classify_platform((False, False, False), "auto"), "standalone")
        with self.assertRaises(VerificationError):
            classify_platform((True, False, True), "auto")
        with self.assertRaises(VerificationError):
            classify_platform((True, True, True), "standalone")

    def test_timer_count_tracks_audited_content_provenance(self) -> None:
        self.assertEqual(expected_timer_count(1), 18)
        self.assertEqual(expected_timer_count(0), 17)

    def test_biff_search_parser_accepts_verified_weidu_24600_lines(self) -> None:
        fixture = """[C:\\game\\weidu.exe] WeiDU version 24600
  BDCUT60.BCS in [SOD-DLC/SCRIPTS.BIF] matches
BDDAZZO.DLG in [SOD-DLC/DIALOG.BIF] matches
"""
        self.assertEqual(
            parse_biff_search_output(fixture),
            {"BDCUT60.BCS", "BDDAZZO.DLG"},
        )
        with self.assertRaises(VerificationError):
            parse_biff_search_output("not-a-resource in [DATA/SCRIPTS.BIF] matches")

    def test_root_inventory_is_bidirectional_with_only_aura_optional(self) -> None:
        snippets = {
            "plot590": 'Global("bd_plot","global",590)',
            "cut60": 'StartCutSceneEx("bdcut60",TRUE)',
            "cut61": 'StartCutSceneEx("bdcut61",TRUE)',
            "debugdream": 'Global("bd_debug_move_to_dream","GLOBAL",1)',
            "debugcell": 'Global("bd_debug_move_to_cell","GLOBAL",1)',
            "corwin6": 'Global("bd_CorwinRomance6","GLOBAL",0)',
            "neera6": 'Global("bd_NeeraRomance6","GLOBAL",0)',
        }
        fixture = {
            resource: "\n".join(
                snippets[name]
                for name in ROOT_PATTERNS
                for _ in range(counts.get(name, 0))
            )
            for resource, counts in KNOWN_ROOT_COUNTS.items()
            if resource != "C0AURA2J.DLG"
        }
        problems = root_inventory_problems(fixture)
        self.assertEqual(problems, [])
        fixture.pop("BDCUT60.BCS")
        self.assertTrue(
            any(
                "missing classified BDCUT60.BCS" in problem
                for problem in root_inventory_problems(fixture)
            )
        )
        fixture["SURPRISE.BCS"] = snippets["cut61"]
        self.assertTrue(
            any(
                "unclassified SURPRISE.BCS" in problem
                for problem in root_inventory_problems(fixture)
            )
        )

    def test_same_dialog_goto_inventory_preserves_edges_and_rejects_new_retired_inbound(self) -> None:
        preserved = """BEGIN ~BDDELANC~

IF ~~ THEN BEGIN 77
  SAY #1
  IF ~~ THEN GOTO 78
END

IF ~~ THEN BEGIN 78
  SAY #2
  IF ~~ THEN EXIT
END
"""
        expected = Counter({("BDDELANC.DLG", 77, 78): 1})
        self.assertEqual(goto_inbound_problems({"BDDELANC.DLG": preserved}, expected), [])
        self.assertTrue(
            goto_inbound_problems(
                {"BDDELANC.DLG": preserved.replace("GOTO 78", "EXIT")},
                expected,
            )
        )
        malicious = preserved + """
IF ~~ THEN BEGIN 200
  SAY #3
  IF ~~ THEN GOTO 95
END
"""
        self.assertTrue(
            any(
                "BDDELANC.DLG:200->95" in problem
                for problem in goto_inbound_problems(
                    {"BDDELANC.DLG": malicious}, expected
                )
            )
        )

    def test_guard_actions_are_exact_unique_and_fail_closed(self) -> None:
        good = """RESPONSE #100
DisplayString(Player1,123)
FadeFromColor([1.0],0)
EndCutSceneMode()
SetGlobal("CSR_ENDING_FAILED","GLOBAL",1)
DestroySelf()
"""
        self.assertTrue(guard_actions_are_fail_closed(good))
        self.assertFalse(
            guard_actions_are_fail_closed(
                good.replace("FadeFromColor([1.0],0)\n", "")
            )
        )
        self.assertFalse(
            guard_actions_are_fail_closed(
                good.replace(
                    "DestroySelf()",
                    "Continue()\nDestroySelf()",
                )
            )
        )
        self.assertFalse(
            guard_actions_are_fail_closed(
                good.replace(
                    "DestroySelf()",
                    "TakeCreatureItems(Player1,ALL)\nDestroySelf()",
                )
            )
        )
        self.assertFalse(
            guard_actions_are_fail_closed(
                good.replace(
                    "DestroySelf()",
                    "SetGlobal(\"CSR_ENDING_FAILED\",\"GLOBAL\",1)\nDestroySelf()",
                )
            )
        )
        self.assertFalse(guard_actions_are_fail_closed(good + "RESPONSE #1\n"))

    def test_guard_trigger_is_exact_and_has_no_extra_predicates(self) -> None:
        good = """OR(2)
!AreaCheck("BD4300")
!Exists("K#ImportContainer")
"""
        self.assertTrue(guard_trigger_is_fail_closed(good))
        self.assertTrue(
            guard_trigger_is_fail_closed(
                good.replace("!Exists", "!ObjectExists")
            )
        )
        self.assertFalse(
            guard_trigger_is_fail_closed(
                good + 'Global("CSR_EXTRA","GLOBAL",1)\n'
            )
        )
        self.assertFalse(
            guard_trigger_is_fail_closed(
                good.replace('!AreaCheck("BD4300")', 'AreaCheck("BD4300")')
            )
        )

    def test_dazzo_endpoint_order_is_platform_exact_and_unique(self) -> None:
        common = """DO ~SetGlobal("CSR_ENDING_DONE","GLOBAL",1)
EraseJournalEntry(266908)
StartCutSceneMode()
FadeToColor([1.0],0)
"""
        eet = common + 'CreateCreatureObject("CSRETBGT",Player1,0,0,0)\n~ EXIT'
        standalone = (
            common
            + "EndCutSceneMode()\nContinueGame(FALSE)\nEndCredits()\n~ EXIT"
        )
        self.assertTrue(
            dazzo_endpoint_is_ordered(
                eet, "eet", "CSR_ENDING_DONE", 266908
            )
        )
        self.assertTrue(
            dazzo_endpoint_is_ordered(
                standalone, "standalone", "CSR_ENDING_DONE", 266908
            )
        )
        self.assertFalse(
            dazzo_endpoint_is_ordered(
                eet.replace(
                    'CreateCreatureObject("CSRETBGT",Player1,0,0,0)',
                    'CreateCreatureObject("CSRETBGT",Player1,0,0,0)\n'
                    'CreateCreatureObject("CSRETBGT",Player1,0,0,0)',
                ),
                "eet",
                "CSR_ENDING_DONE",
                266908,
            )
        )
        self.assertFalse(
            dazzo_endpoint_is_ordered(
                standalone.replace(
                    "FadeToColor([1.0],0)\n",
                    "EndCredits()\nFadeToColor([1.0],0)\n",
                ),
                "standalone",
                "CSR_ENDING_DONE",
                266908,
            )
        )
        self.assertFalse(
            dazzo_endpoint_is_ordered(
                eet.replace("DO ~", "DO ~TakePartyItemAll(Player1)\n"),
                "eet",
                "CSR_ENDING_DONE",
                266908,
            )
        )
        self.assertFalse(
            dazzo_endpoint_is_ordered(
                eet.replace("~ EXIT", "~ GOTO 66"),
                "eet",
                "CSR_ENDING_DONE",
                266908,
            )
        )

    def test_bence_terminal_routes_check_every_expected_transition(self) -> None:
        states = {
            number: DialogState(
                "False()",
                "SAY #1\n"
                + "\n".join("IF ~~ THEN EXIT" for _ in range(count)),
            )
            for number, count in BENCE_TERMINAL_COUNTS.items()
        }
        self.assertEqual(bence_terminal_problems(states), [])
        bad_count = dict(states)
        bad_count[70] = DialogState("False()", "SAY #1\nIF ~~ THEN EXIT")
        self.assertTrue(bence_terminal_problems(bad_count))
        bad_route = dict(states)
        bad_route[71] = DialogState(
            "False()",
            "SAY #1\nIF ~~ THEN EXIT\n"
            "IF ~~ THEN DO ~StartCutSceneEx(\"bdcut61\",TRUE)~ EXIT",
        )
        self.assertTrue(bence_terminal_problems(bad_route))

    def test_dialog_parser_keeps_state_trigger_and_transitions(self) -> None:
        fixture = """BEGIN ~TEST~

IF ~Global(\"X\",\"GLOBAL\",1) False()~ THEN BEGIN 7
  SAY #1
  IF ~~ THEN DO ~SetGlobal(\"Y\",\"GLOBAL\",1)~ EXIT
END
"""
        state = dialog_states(fixture, "TEST")[7]
        self.assertTrue(false_gated(state.trigger))
        self.assertEqual(len(dialog_transitions(state)), 1)

    def test_false_gate_must_be_a_top_level_conjunct(self) -> None:
        self.assertFalse(
            false_gated('OR(2)\nFalse()\nGlobal("LIVE","GLOBAL",1)')
        )
        self.assertTrue(
            false_gated('False()\nGlobal("LIVE","GLOBAL",1)')
        )
        self.assertTrue(
            false_gated(
                'OR(2)\nGlobal("A","GLOBAL",1)\nGlobal("B","GLOBAL",1)\nFalse()'
            )
        )
        self.assertTrue(
            false_gated(
                'False()\nOR(2)\nGlobal("A","GLOBAL",1)\nGlobal("B","GLOBAL",1)'
            )
        )
        self.assertFalse(false_gated('OR(2)\nFalse()'))
        self.assertFalse(
            false_gated('OR(2)\nOR(2)\nFalse()\nTrue()\nFalse()')
        )
        self.assertFalse(false_gated('!False()'))
        self.assertFalse(false_gated('TriggerOverride(Myself,False())'))
        self.assertFalse(false_gated('OR(x)\nFalse()'))

    def test_are_parser_reads_empty_container_and_vertices(self) -> None:
        data = bytearray(0x240)
        data[:8] = b"AREAV1.0"
        struct.pack_into("<I", data, 0x70, 0x100)
        struct.pack_into("<H", data, 0x74, 1)
        struct.pack_into("<H", data, 0x76, 0)
        struct.pack_into("<I", data, 0x78, 0x200)
        struct.pack_into("<I", data, 0x7C, 0x220)
        struct.pack_into("<H", data, 0x80, 4)
        base = 0x100
        data[base : base + 17] = b"K#ImportContainer"
        struct.pack_into("<HHH", data, base + 0x20, 88, 76, 8)
        struct.pack_into("<H", data, base + 0x26, 100)
        struct.pack_into("<H", data, base + 0x2E, 100)
        struct.pack_into("<HH", data, base + 0x34, 80, 70)
        struct.pack_into("<HHHH", data, base + 0x38, 72, 26, 120, 58)
        struct.pack_into("<I", data, base + 0x50, 0)
        struct.pack_into("<H", data, base + 0x54, 4)
        for index, vertex in enumerate(((111, 58), (72, 45), (82, 26), (120, 39))):
            struct.pack_into("<HH", data, 0x220 + index * 4, *vertex)
        container = parse_containers(bytes(data), "fixture")[0]
        self.assertEqual(container.item_count, 0)
        self.assertEqual((container.lock_difficulty, container.trap_removal), (100, 100))
        self.assertEqual(container.vertices[2], (82, 26))
        self.assertTrue(bd4300_import_geometry_ok(container))
        reordered = Container(
            container.name,
            container.x,
            container.y,
            container.kind,
            container.lock_difficulty,
            container.trap_removal,
            container.item_count,
            container.bbox,
            container.trap_location,
            tuple(reversed(container.vertices)),
        )
        self.assertFalse(bd4300_import_geometry_ok(reordered))


def _run_self_tests() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ContractFixtureTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game-dir", required=True, type=Path)
    parser.add_argument(
        "--platform", choices=("auto", "eet", "standalone"), default="auto"
    )
    parser.add_argument("--baseline-manifest", type=Path)
    parser.add_argument("--self-test", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.self_test:
        return _run_self_tests()
    try:
        return verify(
            args.game_dir.resolve(),
            args.platform,
            args.baseline_manifest.resolve() if args.baseline_manifest else None,
        )
    except (OSError, ValueError, json.JSONDecodeError, struct.error, subprocess.SubprocessError, VerificationError) as error:
        print(f"FAIL: verifier could not inspect the installed resources ({error})")
        return 1


if __name__ == "__main__":
    if "--self-test" in sys.argv and "--game-dir" not in sys.argv:
        sys.exit(_run_self_tests())
    sys.exit(main())
