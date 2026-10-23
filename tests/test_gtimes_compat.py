#!/usr/bin/env python3
"""Real WeiDU fixtures for the shared GTIMES name helper (lib/gtimes_compat.tpa).

A decompiled timer argument is printed with a name from the game's GTIMES.IDS,
and mods append names: Dark Tidings v3.2 adds "60 ONE_TURN", after which 60
seconds decompile as ONE_TURN instead of TEN_ROUNDS. The helper must return the
token that a real DECOMPILE_AND_PATCH prints, for the BIFF layout, mod appends,
tab-separated files and other layouts WeiDU accepts. The component tests import
the GTIMES fixtures below. Only disposable synthetic games are written.
"""
from __future__ import annotations

from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'research/scripts'))
from test_comp291_installer import WEIDU, tree, write_fake_game

HELPER = ROOT / 'chriz-sod-remix/lib/gtimes_compat.tpa'
SET_GLOBAL_TIMER = '115 SetGlobalTimer(S:Name*,S:Area*,I:Time*GTimes)\n'

# Minimal synthetic GTIMES.IDS in the shape of the game's BIFF copy: a bare
# "IDS" header line, single spaces and CRLF. It carries the vanilla names of
# every timer a component matches (6, 10, 12, 18, 30 and 60 seconds) and their
# neighbours, including 61 ONE_TURN next to 60 TEN_ROUNDS.
VANILLA_NAMES = {5: 'ONE_MINUTE', 6: 'ONE_ROUND', 10: 'TWO_MINUTES', 12: 'TWO_ROUNDS',
                 18: 'THREE_ROUNDS', 24: 'FOUR_ROUNDS', 30: 'FIVE_ROUNDS',
                 60: 'TEN_ROUNDS', 61: 'ONE_TURN', 120: 'TWO_TURNS'}
VANILLA_GTIMES = 'IDS\r\n' + ''.join(f'{value} {name}\r\n' for value, name in VANILLA_NAMES.items())
# Setup-Tidings.tp2 v3.2: APPEND ~GTimes.IDS~ ~<line>~ UNLESS ~<line>~, in this order.
TIDINGS_LINES = ('6 ONE_ROUND', '12 TWO_ROUNDS', '18 THREE_ROUNDS', '24 FOUR_ROUNDS',
                 '30 FIVE_ROUNDS', '10 TWO_MINUTES', '60 ONE_TURN')
MATCHED_TIMERS = (6, 10, 12, 18, 30, 60)


def weidu_append(text: str, line: str) -> str:
    """WeiDU 249 APPEND without KEEP_CRLF: line breaks collapse to CRLF, then the line."""
    return re.sub(r'[\r\n]+', '\r\n', text + '\r\n') + line + '\r\n'


def tidings(text: str) -> str:
    for line in TIDINGS_LINES:
        if not re.search(line, text, re.I):
            text = weidu_append(text, line)
    return text


def tab_separated(text: str) -> str:
    return re.sub(r'^([0-9]+) ', '\\1\t', text, flags=re.M)


def gtimes_variants(value: int) -> dict[str, tuple[str, str]]:
    """GTIMES.IDS files a decompile contract for one timer value must accept.

    Maps a label to (file text, name WeiDU prints for value). Dark Tidings
    changes only 60; the last variant gives value a name of another mod.
    """
    vanilla = VANILLA_NAMES[value]
    after_tidings = 'ONE_TURN' if value == 60 else vanilla
    other = f'MOD_{vanilla}'
    return {
        'vanilla': (VANILLA_GTIMES, vanilla),
        'Dark Tidings': (tidings(VANILLA_GTIMES), after_tidings),
        'tab separated': (tab_separated(VANILLA_GTIMES), vanilla),
        'tab separated + Dark Tidings': (tidings(tab_separated(VANILLA_GTIMES)), after_tidings),
        'name from another mod': (weidu_append(VANILLA_GTIMES, f'{value} {other}'), other),
    }


def helper_variants() -> dict[str, tuple[str, dict[int, str]]]:
    """Wider WeiDU-valid layouts for the helper itself: label -> (text, printed names)."""
    without_60 = VANILLA_GTIMES.replace('60 TEN_ROUNDS\r\n', '')
    variants = {label: (text, {**VANILLA_NAMES, 60: name})
                for label, (text, name) in gtimes_variants(60).items()}
    variants.update({
        'IDS V1.0 header': ('IDS V1.0' + VANILLA_GTIMES[3:], dict(VANILLA_NAMES)),
        'hexadecimal value': (weidu_append(VANILLA_GTIMES, '0x3C SIXTY_SECONDS'),
                              {**VANILLA_NAMES, 60: 'SIXTY_SECONDS'}),
        'LF line breaks': (VANILLA_GTIMES.replace('\r\n', '\n') + '60 LF_TURN\n',
                           {**VANILLA_NAMES, 60: 'LF_TURN'}),
        'no name for 60': (without_60, {**VANILLA_NAMES, 60: '60'}),
        # WeiDU wraps a name with a dot in five quotes, and compiles that form back.
        'name with a dot': (weidu_append(VANILLA_GTIMES, '60 TEN.ROUNDS'),
                            {**VANILLA_NAMES, 60: '"""""TEN.ROUNDS"""""'}),
    })
    return variants


@unittest.skipUnless(WEIDU.is_file(), 'real WeiDU unavailable; set WEIDU_EXE')
class GtimesHelperTests(unittest.TestCase):
    def make_game(self, gtimes: str, action_extra: str = '') -> Path:
        temp = tempfile.TemporaryDirectory(prefix='csr-gtimes-helper-')
        self.addCleanup(temp.cleanup)
        game = Path(temp.name)
        write_fake_game(game)
        override = game / 'override'
        action = override / 'action.ids'
        action.write_bytes(action.read_bytes() + (SET_GLOBAL_TIMER + action_extra).encode('ascii'))
        (override / 'gtimes.ids').write_bytes(gtimes.encode('ascii'))
        (game / 'chriz-sod-remix/lib').mkdir(parents=True)
        shutil.copy2(HELPER, game / 'chriz-sod-remix/lib/gtimes_compat.tpa')
        # Numeric source: the compiled values must not depend on any name.
        (game / 'fixture').mkdir()
        timers = ''.join(f'    SetGlobalTimer("csrt{value}","LOCALS",{value})\n'
                         for value in MATCHED_TIMERS)
        (game / 'fixture/timers.baf').write_text(
            f'IF\n  True()\nTHEN\n  RESPONSE #100\n{timers}END\n', encoding='ascii')
        (game / 'fixture/setup-fixture.tp2').write_text('''BACKUP ~fixture/backup~
AUTHOR ~fixture~
BEGIN ~compile timer fixture~ DESIGNATED 0
COMPILE ~fixture/timers.baf~
''', encoding='ascii')
        self.assert_installed(self.run_weidu(game, 'fixture/setup-fixture.tp2'))
        (game / 'probe.tp2').write_text('''BACKUP ~probe-backup~
AUTHOR ~fixture~
BEGIN ~GTIMES helper harness~ DESIGNATED 0
INCLUDE ~chriz-sod-remix/lib/gtimes_compat.tpa~
ACTION_FOR_EACH csr_test_value IN %s BEGIN
  LAF csr_gtimes_regexp
    INT_VAR csr_gtimes_value = csr_test_value
    STR_VAR csr_gtimes_caller = ~fixture probe~
    RET csr_test_token = csr_gtimes_token csr_test_regexp = csr_gtimes_regexp
  END
  // The real decompile of a compiled timer, read the same way the probe is.
  COPY_EXISTING - ~timers.bcs~ ~override~
    DECOMPILE_AND_PATCH BEGIN
      SPRINT csr_test_real ~~
      REPLACE_EVALUATE CASE_SENSITIVE ~SetGlobalTimer("csrt%%csr_test_value%%","LOCALS",\\([^%%WNL%%]*\\))~ BEGIN
        SPRINT csr_test_real ~%%MATCH1%%~
      END ~%%MATCH0%%~
      COUNT_REGEXP_INSTANCES CASE_SENSITIVE ~SetGlobalTimer("csrt%%csr_test_value%%","LOCALS",%%csr_test_regexp%%)~ csr_test_exact
      COUNT_REGEXP_INSTANCES ~SetGlobalTimer("csrt%%csr_test_value%%","LOCALS",%%csr_test_regexp%%)~ csr_test_default
    END
  PRINT ~CSRTEST|%%csr_test_value%%|%%csr_test_token%%|%%csr_test_regexp%%|%%csr_test_real%%|%%csr_test_exact%%|%%csr_test_default%%~
END
''' % ' '.join(map(str, MATCHED_TIMERS)), encoding='ascii')
        return game

    @staticmethod
    def run_weidu(game: Path, tp2: str) -> subprocess.CompletedProcess:
        return subprocess.run([str(WEIDU), tp2, '--force-install-list', '0', '--game', str(game),
                               '--language', '0', '--use-lang', 'en_US', '--no-exit-pause'],
                              cwd=game, capture_output=True, text=True, encoding='utf-8',
                              errors='replace', timeout=60)

    def assert_installed(self, result: subprocess.CompletedProcess) -> None:
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('SUCCESSFULLY INSTALLED', result.stdout)

    def probe(self, game: Path) -> dict[int, tuple[str, str, str, int, int]]:
        before = tree(game / 'override')
        result = self.run_weidu(game, 'probe.tp2')
        self.assert_installed(result)
        self.assertEqual(tree(game / 'override'), before, 'the helper must not write game resources')
        rows = {}
        for line in result.stdout.splitlines():
            if line.startswith('CSRTEST|'):
                value, token, regexp, real, exact, default = line.rstrip().split('|')[1:]
                rows[int(value)] = token, regexp, real, int(exact), int(default)
        self.assertEqual(sorted(rows), list(MATCHED_TIMERS), result.stdout)
        return rows

    def test_token_is_what_a_real_decompile_prints(self):
        for label, (gtimes, names) in helper_variants().items():
            with self.subTest(gtimes=label):
                rows = self.probe(self.make_game(gtimes))
                for value, (token, regexp, real, exact, default) in rows.items():
                    self.assertEqual(token, names[value], value)
                    self.assertEqual(real, token, value)
                    self.assertEqual(regexp, token.replace('.', '[.]'), value)
                    self.assertEqual((exact, default), (1, 1), value)

    def test_dark_tidings_changes_only_the_sixty_second_name(self):
        rows = self.probe(self.make_game(tidings(VANILLA_GTIMES)))
        self.assertEqual({value: row[0] for value, row in rows.items()},
                         {**{value: VANILLA_NAMES[value] for value in MATCHED_TIMERS}, 60: 'ONE_TURN'})

    def test_unreadable_probe_fails_without_writes(self):
        # Another name for action 115 changes how every SetGlobalTimer prints.
        game = self.make_game(VANILLA_GTIMES, '115 SetTimerAlias(S:Name*,S:Area*,I:Time*GTimes)\n')
        before = tree(game / 'override')
        result = self.run_weidu(game, 'probe.tp2')
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('fixture probe: a probe timer of 6 seconds did not decompile to exactly one '
                      'SetGlobalTimer argument (found 0)', result.stdout + result.stderr)
        self.assertEqual(tree(game / 'override'), before)


class GtimesHelperSourceTests(unittest.TestCase):
    def test_public_installer_defines_the_helper_for_every_component(self):
        tp2 = (ROOT / 'chriz-sod-remix/setup-chriz-sod-remix.tp2').read_text(encoding='utf-8')
        always = re.search(r'^ALWAYS\s*$(.*?)^END\s*$', tp2, re.M | re.S)
        self.assertIsNotNone(always)
        self.assertIn('INCLUDE ~chriz-sod-remix/lib/gtimes_compat.tpa~', always.group(1))

    def test_fixture_follows_weidu_append_and_dark_tidings(self):
        self.assertEqual(tidings(VANILLA_GTIMES), VANILLA_GTIMES + '60 ONE_TURN\r\n')
        tabbed = tidings(tab_separated(VANILLA_GTIMES))
        self.assertTrue(tabbed.startswith(tab_separated(VANILLA_GTIMES)))
        self.assertEqual(tabbed[len(tab_separated(VANILLA_GTIMES)):],
                         ''.join(f'{line}\r\n' for line in TIDINGS_LINES))


if __name__ == '__main__':
    unittest.main(verbosity=2)
