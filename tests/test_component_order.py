import re
import unittest
from pathlib import Path


TP2_PATH = (
    Path(__file__).resolve().parents[1]
    / "chriz-sod-remix"
    / "setup-chriz-sod-remix.tp2"
)

EXPECTED_COMPONENTS = {
    100,
    110,
    120,
    130,
    140,
    145,
    150,
    160,
    170,
    175,
    180,
    185,
    187,
    190,
    195,
    197,
    200,
    210,
    215,
    220,
    225,
    230,
    240,
    245,
    250,
    255,
    260,
    270,
    280,
    290,
    291,
    900,
    901,
    910,
}


def designated_components() -> list[int]:
    source = TP2_PATH.read_text(encoding="utf-8")
    return [
        int(match.group(1))
        for match in re.finditer(
            r"^BEGIN\s+@\d+\s+DESIGNATED\s+(\d+)\b", source, re.MULTILINE
        )
    ]


class ComponentOrderTests(unittest.TestCase):
    def test_patch_release_version_is_v0_6_7(self) -> None:
        source = TP2_PATH.read_text(encoding="utf-8")

        self.assertEqual(1, source.splitlines().count("VERSION ~v0.6.7~"))

    def test_component_210_is_declared_before_component_197(self) -> None:
        components = designated_components()

        self.assertLess(components.index(210), components.index(197))

    def test_ending_prerequisites_precede_290_and_repair_291(self) -> None:
        components = designated_components()

        for prerequisite in (120, 130, 185):
            self.assertLess(components.index(prerequisite), components.index(290))
        self.assertLess(components.index(290), components.index(291))

    def test_all_34_component_declarations_remain_unique(self) -> None:
        components = designated_components()

        self.assertEqual(34, len(components))
        self.assertEqual(EXPECTED_COMPONENTS, set(components))


if __name__ == "__main__":
    unittest.main()
