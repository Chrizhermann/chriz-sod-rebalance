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
        library = SCRY_COMPAT.read_text(encoding="utf-8")
        self.assertNotIn("REPLACE_TRIGGER_TEXT BDSCRY", source)
        self.assertNotIn("ADD_TRANS_TRIGGER BDSCRY", source)
        self.assertIn("ADD_TRANS_TRIGGER BDIMOEN 67 ~False()~ DO 1", source)
        self.assertRegex(
            tp2,
            r'ALWAYS\s+INCLUDE ~chriz-sod-remix/lib/bdscry_compat\.tpa~\s+END',
        )
        self.assertRegex(
            tp2,
            r'LAF csr_disable_bdscry_picker_route\s+STR_VAR\s+'
            r'csr_scry_flag = ~bd_sddd12_hood~\s+csr_scry_component = ~120~\s+END',
        )
        self.assertIn("DEFINE_ACTION_FUNCTION csr_disable_bdscry_picker_route", library)
        self.assertIn("csr_scry_state_count = 4", library)
        self.assertIn("csr_scry_route_count = 1", library)
        self.assertIn("csr_scry_reset_count != 0", library)
        self.assertIn("PATCH_FAIL", library)

    def test_component_150_classifies_eet_all_or_nothing(self) -> None:
        source = COMP150.read_text(encoding="utf-8")
        for anchor in ("K#TELBGT.BCS", "K#TELBGT.CRE", "AR0602.BCS"):
            self.assertIn(anchor, source)
        self.assertIn(
            "ACTION_IF ((csr150_eet_anchors = 1) OR (csr150_eet_anchors = 2))",
            source,
        )
        self.assertIn("partial EET", source)
        self.assertIn("OUTER_SET csr150_tlk_shift = 200000", source)

    def test_component_150_parameterizes_platform_values(self) -> None:
        source = COMP150.read_text(encoding="utf-8")
        expected_assignments = (
            "OUTER_SET csr150_treasury_journal = 67494 + csr150_tlk_shift",
            "OUTER_SET csr150_council_info = 56387 + csr150_tlk_shift",
            "OUTER_SET csr150_campaign_quest = 59617 + csr150_tlk_shift",
            "OUTER_SET csr150_quest_root = 66700 + csr150_tlk_shift",
            "OUTER_SET csr150_old_quest_done = 66701 + csr150_tlk_shift",
        )
        for assignment in expected_assignments:
            self.assertIn(assignment, source)

        self.assertIn("%csr150_treasury_journal%", source)
        self.assertIn("%csr150_imoen_outer%", source)
        self.assertIn("%csr150_imoen_inner%", source)
        self.assertIn("%csr150_quest_root%", source)
        self.assertIn("%csr150_old_quest_done%", source)
        self.assertIn("OUTER_SPRINT csr150_imoen_outer ~IMOEN~", source)
        self.assertIn("OUTER_SPRINT csr150_imoen_inner ~imoen~", source)
        self.assertEqual(source.count("OUTER_SPRINT csr150_imoen_outer ~IMOEN2~"), 1)
        self.assertEqual(source.count("OUTER_SPRINT csr150_imoen_inner ~IMOEN2~"), 1)

    def test_parameterized_sources_are_evaluated(self) -> None:
        comp150 = COMP150.read_text(encoding="utf-8")
        arrival = ARRIVAL.read_text(encoding="utf-8")
        council = COUNCIL.read_text(encoding="utf-8")

        self.assertIn("EXTEND_TOP ~bd0103.bcs~ ~chriz-sod-remix/baf/csrarr.baf~ EVALUATE_BUFFER", comp150)
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
