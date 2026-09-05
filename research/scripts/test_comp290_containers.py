#!/usr/bin/env python3
"""Exercise component 290's real container preflights in disposable fake games.

Set WEIDU_EXE to a WeiDU executable. These fixtures deliberately omit the carrier's
movie action: reaching that later guard proves the ARE preflights accepted the
fixture, while malformed bank names must fail at the earlier ARE guard instead.
No resource is read from or written to an installed game.
"""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
COMP290 = ROOT / "chriz-sod-remix" / "lib" / "comp290.tpa"
WEIDU = os.environ.get("WEIDU_EXE") or shutil.which("weidu")


def area(containers: list[tuple[str, int]]) -> bytes:
    """Minimal valid ARE tables, with independent container names and item runs."""
    item_count = sum(count for _, count in containers)
    item_offset = 0xF4 + len(containers) * 0xC0
    end = item_offset + item_count * 0x14
    data = bytearray(end)
    data[:8] = b"AREAV1.0"
    struct.pack_into("<IHHIIH", data, 0x70, 0xF4, len(containers), item_count,
                     item_offset, end, 0)
    first_item = 0
    for index, (name, count) in enumerate(containers):
        start = 0xF4 + index * 0xC0
        name_bytes = name.encode("ascii")
        if len(name_bytes) > 31:
            raise ValueError("fixture container name exceeds the ARE field")
        data[start:start + len(name_bytes)] = name_bytes
        struct.pack_into("<II", data, start + 0x40, first_item, count)
        first_item += count
    return bytes(data)


@unittest.skipUnless(WEIDU, "Set WEIDU_EXE to run actual WeiDU preflight fixtures")
class ContainerPreflightTests(unittest.TestCase):
    def run_preflight(
        self, local: list[tuple[str, int]], destination: list[tuple[str, int]],
        expected_guard: str,
    ) -> None:
        with tempfile.TemporaryDirectory(prefix="csr290-container-fixture-") as tmp:
            game = Path(tmp)
            override = game / "override"
            override.mkdir()
            # Every resource used by this early production preflight is in
            # override. A TLK default entry prevents WeiDU creating one itself.
            (game / "chitin.key").write_bytes(
                b"KEY V1  " + struct.pack("<4I", 0, 0, 24, 24)
            )
            (game / "dialog.tlk").write_bytes(
                b"TLK V1  " + struct.pack("<HII", 0, 1, 44) + bytes(26)
            )
            fixtures = {
                "BD4300.ARE": area(local),
                "BD6100.ARE": area(destination),
                "K#TELBGT.BCS": b"SC\nSC\n",
                "K#TELBGT.CRE": b"CRE V1.0",
                "AR0602.BCS": b"SC\nSC\n",
            }
            for name, data in fixtures.items():
                # Unix WeiDU normalizes resource paths to lowercase; mirror
                # that layout without changing the resource-name assertions.
                (override / name.lower()).write_bytes(data)
            harness = game / "container-fixture.tp2"
            harness.write_text(
                "BACKUP ~backup~\nAUTHOR ~CSR tests~\n"
                "BEGIN ~component 290 container preflight~ DESIGNATED 0\n"
                f"INCLUDE ~{COMP290.as_posix()}~\n",
                encoding="utf-8",
            )
            immutable = {
                path.relative_to(game): path.read_bytes()
                for path in (game / "chitin.key", game / "dialog.tlk", *override.iterdir())
            }
            result = subprocess.run(
                [str(WEIDU), str(harness), "--game", str(game),
                 "--force-install-list", "0", "--no-exit-pause"],
                cwd=game, capture_output=True, text=True, errors="replace", timeout=30,
            )
            output = result.stdout + result.stderr
            self.assertNotEqual(result.returncode, 0, output)
            self.assertIn(expected_guard, output)
            self.assertIn("NOT INSTALLED DUE TO ERRORS", output)
            self.assertEqual(
                {p.name.upper(): p.read_bytes() for p in override.iterdir()}, fixtures,
                "A rejected preflight must leave every resource unchanged",
            )
            for name, before in immutable.items():
                self.assertEqual((game / name).read_bytes(), before, str(name))

    def test_distinct_spaced_names_pass_both_area_preflights(self) -> None:
        self.run_preflight(
            [("Ordinary Treasure Chest", 0)], [("K#ImportContainer", 0)],
            "[K# carrier INTRO15F anchor]: expected 1 occurrence(s)",
        )

    def test_local_space_alias_conflicts_with_new_bank(self) -> None:
        self.run_preflight(
            [("K#Import Container", 0)], [("K#ImportContainer", 0)],
            "[BD4300 local bank]: expected zero K#ImportContainer records before installation, found 1",
        )

    def test_local_mixed_case_and_multiple_spaces_also_conflict(self) -> None:
        self.run_preflight(
            [(" k# import CONTAINER ", 0)], [("K#ImportContainer", 0)],
            "[BD4300 local bank]: expected zero K#ImportContainer records before installation, found 1",
        )

    def test_destination_space_alias_is_an_ambiguous_duplicate(self) -> None:
        self.run_preflight(
            [], [("K#ImportContainer", 0), ("K#Import Container", 0)],
            "[BD6100 destination]: expected exactly one empty K#ImportContainer, found 2 named container(s), 2 empty",
        )

    def test_single_destination_alias_remains_usable(self) -> None:
        self.run_preflight(
            [], [("K#Import Container", 0)],
            "[K# carrier INTRO15F anchor]: expected 1 occurrence(s)",
        )

    def test_single_nonempty_destination_alias_is_rejected(self) -> None:
        self.run_preflight(
            [], [("K#Import Container", 1)],
            "[BD6100 destination]: expected exactly one empty K#ImportContainer, found 1 named container(s), 0 empty",
        )


if __name__ == "__main__":
    unittest.main()
