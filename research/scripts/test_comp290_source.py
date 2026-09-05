#!/usr/bin/env python3
"""Source-level regression checks for component 290's WeiDU regexes."""

from pathlib import Path
import unittest


COMP290 = Path(__file__).resolve().parents[2] / "chriz-sod-remix" / "lib" / "comp290.tpa"


class Component290SourceTests(unittest.TestCase):
    def test_literal_call_parentheses_are_not_weidu_groups(self) -> None:
        source = COMP290.read_text(encoding="utf-8")
        bad_lines = [
            f"{line_no}: {line.strip()}"
            for line_no, line in enumerate(source.splitlines(), start=1)
            if r"\(" in line or r"\)" in line
        ]
        self.assertEqual(
            bad_lines,
            [],
            "WeiDU uses escaped parentheses for regex grouping; literal call "
            "parentheses must be unescaped:\n" + "\n".join(bad_lines),
        )


if __name__ == "__main__":
    unittest.main()
