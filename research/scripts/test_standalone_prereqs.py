#!/usr/bin/env python3
"""Source regressions for standalone-SoD compatibility in components 120/150."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]
TP2 = ROOT / "chriz-sod-remix" / "setup-chriz-sod-remix.tp2"
HOOD = ROOT / "chriz-sod-remix" / "dlg" / "csrhood.d"
SCRY_COMPAT = ROOT / "chriz-sod-remix" / "lib" / "bdscry_compat.tpa"
COMP150 = ROOT / "chriz-sod-remix" / "lib" / "comp150.tpa"
ARRIVAL = ROOT / "chriz-sod-remix" / "baf" / "csrarr.baf"
COUNCIL = ROOT / "chriz-sod-remix" / "dlg" / "csrcncl.d"


class StandalonePrerequisiteSourceTests(unittest.TestCase):
    def test_component_120_disables_hood_picker_by_semantics(self) -> None:
        source = HOOD.read_text(encoding="utf-8")
        tp2 = TP2.read_text(encoding="utf-8")
        writer = (ROOT / "chriz-sod-remix/lib/comp120.tpa").read_text(encoding="utf-8")
        library = SCRY_COMPAT.read_text(encoding="utf-8")
        self.assertNotIn("REPLACE_TRIGGER_TEXT BDSCRY", source)
        self.assertNotIn("ADD_TRANS_TRIGGER BDSCRY", source)
        self.assertIn("REPLACE ~BDIMOEN~", source)
        self.assertIn("False()", source)
        self.assertRegex(
            tp2,
            r'ALWAYS\s+INCLUDE ~chriz-sod-remix/lib/bdscry_compat\.tpa~\s+'
            r'(?:INCLUDE ~chriz-sod-remix/lib/\w+\.tpa~\s+)*END',
        )
        self.assertRegex(
            writer,
            r'LAF csr_disable_bdscry_picker_route\s+STR_VAR\s+'
            r'csr_scry_flag = ~bd_sddd12_hood~\s+csr_scry_component = ~120~\s+END',
        )
        self.assertIn("DEFINE_ACTION_FUNCTION csr_disable_bdscry_picker_route", library)

    def test_component_150_uses_game_type_and_native_text_ids(self) -> None:
        source = COMP150.read_text(encoding="utf-8")
        self.assertIn('GAME_IS ~eet~', source)
        self.assertIn('OUTER_SET csr150_tlk_shift = 200000', source)
        for name, value in (('treasury_journal',67494),('council_info',56387),('campaign_quest',59617),('quest_root',66700)):
            self.assertIn(f'OUTER_SET csr150_{name} = {value} + csr150_tlk_shift', source)

    def test_parameterized_sources_are_evaluated(self) -> None:
        comp150 = COMP150.read_text(encoding="utf-8")
        arrival = ARRIVAL.read_text(encoding="utf-8")
        council = COUNCIL.read_text(encoding="utf-8")

        self.assertIn("~chriz-sod-remix/baf/csrarr.baf~", comp150)
        self.assertIn("COMPILE EVALUATE_BUFFER ~chriz-sod-remix/dlg/csrcncl.d~", comp150)
        self.assertIn("AddJournalEntry(%csr150_treasury_journal%,QUEST)", arrival)
        self.assertIn("AddJournalEntry(%csr150_council_info%,INFO)", council)
        self.assertIn("AddJournalEntry(%csr150_campaign_quest%,QUEST)", council)

        executable = "\n".join(
            line.split("//", 1)[0]
            for text in (comp150, arrival, council)
            for line in text.splitlines()
        )
        for eet_only_id in (267494, 256387, 259617, 266700, 266701):
            self.assertIsNone(
                re.search(rf"(?<!\d){eet_only_id}(?!\d)", executable),
                f"EET-only journal ID {eet_only_id} must be derived from the platform shift",
            )


if __name__ == "__main__":
    unittest.main()
