"""Real WeiDU Bence approach installation and bounded compiled decisions.

All writes use disposable synthetic games. These tests verify script priorities,
guards and retries, not engine pathfinding or successful native dialogue starts.
"""
from pathlib import Path
import shutil
import tempfile
import unittest

from test_comp256_ai import Decisions, ROOT, WEIDU, atom, at, call, tree, write_fake_game
from test_comp197_xp import decompile, run_weidu


# Keep a deliberately permissive old starter: the pending-wrap fallback must
# suppress it when combat or an unavailable protagonist blocks the new starter.
BASE = '''IF
  Global("bd_plot","GLOBAL",293)
THEN
  RESPONSE #100
    SetGlobal("LEGACY_STARTED","LOCALS",1)
END

IF
  True()
THEN
  RESPONSE #100
    SetGlobal("FOREIGN_TAIL","GLOBAL",7)
END
'''

ACTION_IDS = '''IDS V1.0
0 NoAction()
22 MoveToObject(O:Target*)
30 SetGlobal(S:Name*,S:Area*,I:Value*)
115 SetGlobalTimer(S:Name*,S:Area*,I:Time*GTimes)
198 StartDialogueNoSet(O:Object*)
'''
TRIGGER_IDS = '''IDS V1.0
0x400B Allegiance(O:Object*,I:Allegiance*EA)
0x400F Global(S:Name*,S:Area*,I:Value*)
0x4011 HPGT(O:Object*,I:HitPoints*)
0x4018 Range(O:Object*,I:Range*)
0x401C See(O:Object*)
0x4023 True()
0x4041 GlobalTimerNotExpired(S:Name*,S:Area*)
0x4043 IsValidForPartyDialogue(O:Object*)
0x407E AreaCheck(S:ResRef*)
0x4083 CombatCounter(I:Number*)
0x4089 OR(I:OrCount*)
0x40CB InMyArea(O:Object*)
'''


def write_aftermath_fixture(game):
    """Minimal Bence resources, independent of other component installers."""
    write_fake_game(game)
    for name, content in {
        'action': ACTION_IDS, 'trigger': TRIGGER_IDS,
        'ea': 'IDS V1.0\n0 ANYONE\n2 PC\n', 'gtimes': 'IDS V1.0\n',
    }.items():
        (game / 'override' / f'{name}.ids').write_text(content, encoding='ascii')
    lib = game / 'chriz-sod-remix' / 'lib'
    lib.mkdir(parents=True)
    shutil.copy2(ROOT / 'chriz-sod-remix/lib/comp256_aftermath.tpa', lib)
    fixture = game / 'fixture'
    fixture.mkdir()
    (fixture / 'bdbence.baf').write_text(BASE, encoding='ascii')
    (fixture / 'bdbence.d').write_text('''BEGIN ~BDBENCE~
IF ~Global("bd_plot","GLOBAL",293)~ THEN BEGIN wrap
  SAY ~Existing Bence wrap.~
  IF ~~ THEN DO ~SetGlobal("bd_plot","GLOBAL",294)~ EXIT
END
''', encoding='ascii')
    (fixture / 'setup-fixture.tp2').write_text('''BACKUP ~fixture-backup~
AUTHOR ~test~
BEGIN ~source resources~
COMPILE ~fixture/bdbence.baf~ ~fixture/bdbence.d~
''', encoding='ascii')
    for name in ('aftermath', 'duplicate'):
        (game / f'{name}.tp2').write_text(f'''BACKUP ~{name}-backup~
AUTHOR ~test~
BEGIN ~Bence approach~ DESIGNATED 256
INCLUDE ~chriz-sod-remix/lib/comp256_aftermath.tpa~
LAF csr256_aftermath_preflight END
LAF csr256_aftermath_install END
''', encoding='ascii')
    (game / 'override' / 'foreign.2da').write_bytes(
        b'2DA V1.0\r\n0\r\nVALUE\r\nFOREIGN 37\r\n')


class AftermathDecisions(Decisions):
    """Add only the aftermath's input predicates and observable actions."""
    def __init__(self, baf):
        super().__init__(baf)
        self.me.ea = 128
        self.variables = {('BD2000', 'CSR256_STAGE'): 3,
                          ('GLOBAL', 'BD_PLOT'): 293}
        self.combat_counter = 0
        self.dialogue_available = True

    def condition(self, text, context=None):
        fn, args = call(text.strip().lstrip('!'))
        if fn not in {
            'Global', 'GlobalTimerNotExpired', 'AreaCheck', 'HPGT',
            'Allegiance', 'See', 'Range', 'InMyArea', 'CombatCounter',
            'IsValidForPartyDialogue', 'True',
        }:
            raise AssertionError(f'Unsupported aftermath condition: {text}')
        if text.strip().startswith('!'):
            return not self.condition(text.strip()[1:], context)
        if fn == 'True':
            return True
        if fn == 'CombatCounter':
            return self.combat_counter == int(args[0])
        if fn == 'IsValidForPartyDialogue':
            return self.actor(args[0], context) is not None and self.dialogue_available
        return super().condition(text, context)

    def act(self, text):
        fn, args = call(text.strip())
        if fn in ('NoAction', 'MoveToObject', 'StartDialogueNoSet'):
            # Movement and dialogue are queued observables; neither teleports
            # an actor nor advances the story in this deliberately small model.
            self.actions.append((fn, *(atom(a) for a in args)))
        else:
            super().act(text)


@unittest.skipUnless(WEIDU.is_file(), 'real WeiDU unavailable; set WEIDU_EXE')
class CompiledAftermathDecisionsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='csr256-aftermath-decisions-')
        cls.addClassCleanup(cls.temp.cleanup)
        game = Path(cls.temp.name)
        write_aftermath_fixture(game)
        for package, component in [('fixture/setup-fixture.tp2', '0'),
                                   ('aftermath.tp2', '256')]:
            result = run_weidu(game, package, '--force-install-list', component)
            if result.returncode:
                raise AssertionError(result.stdout + result.stderr)
        cls.baf = decompile(game, 'BDBENCE.BCS')

    def model(self, distance=7):
        model = AftermathDecisions(self.baf)
        model.actors['PLAYER1'].position = at(distance)
        return model

    def assert_waits(self, model):
        self.assertEqual([('NoAction',)], model.step())
        self.assertEqual(0, model.variables.get(('LOCALS', 'LEGACY_STARTED'), 0))
        self.assertEqual(293, model.variables[('GLOBAL', 'BD_PLOT')])

    def test_far_player_is_approached_without_dialogue_or_story_changes(self):
        model = self.model(8)
        before = model.variables.copy()
        self.assertEqual([('MoveToObject', 'PLAYER1')], model.step())
        self.assertEqual(before, model.variables)
        self.assertEqual({}, model.timers)
        self.assertEqual(at(8), model.actors['PLAYER1'].position)

    def test_close_player_including_exact_seven_starts_existing_dialogue(self):
        for distance in (0, 6.99, 7):
            with self.subTest(distance=distance):
                model = self.model(distance)
                before = model.variables.copy()
                self.assertEqual([
                    ('SetGlobalTimer', 'CSR256_BENCE_TRY', 'LOCALS', 2),
                    ('StartDialogueNoSet', 'PLAYER1')], model.step())
                self.assertEqual(before, model.variables)
                self.assertEqual({('LOCALS', 'CSR256_BENCE_TRY'): 2}, model.timers)

    def test_approach_can_finish_then_dialogue_begins_on_next_evaluation(self):
        model = self.model(30)
        self.assertEqual([('MoveToObject', 'PLAYER1')], model.step())
        # The engine, not the decision runner, determines how quickly this occurs.
        model.actors['PLAYER1'].position = at(6)
        self.assertEqual('StartDialogueNoSet', model.step()[-1][0])

    def test_active_combat_suppresses_both_new_and_legacy_starters(self):
        for distance in (6, 30):
            for counter in (1, 6, 60):
                with self.subTest(distance=distance, counter=counter):
                    model = self.model(distance)
                    model.combat_counter = counter
                    self.assert_waits(model)
                    model.combat_counter = 0
                    self.assertNotEqual([('NoAction',)], model.step())

    def test_unavailable_close_player_waits_and_recovers_without_once_latch(self):
        model = self.model()
        model.dialogue_available = False
        self.assert_waits(model)
        self.assertEqual({}, model.timers)
        model.dialogue_available = True
        self.assertEqual('StartDialogueNoSet', model.step()[-1][0])

    def test_unavailable_far_player_may_be_approached_but_not_interrupted(self):
        model = self.model(12)
        model.dialogue_available = False
        self.assertEqual([('MoveToObject', 'PLAYER1')], model.step())
        model.actors['PLAYER1'].position = at(7)
        self.assert_waits(model)

    def test_absent_dead_nonparty_or_other_area_player_blocks_both_routes(self):
        for distance in (6, 30):
            for case in ('absent', 'dead', 'negative_hp', 'hostile', 'neutral', 'other_area'):
                with self.subTest(distance=distance, case=case):
                    model = self.model(distance)
                    player = model.actors['PLAYER1']
                    if case == 'absent':
                        del model.actors['PLAYER1']
                    elif case in ('dead', 'negative_hp'):
                        player.hp = 0 if case == 'dead' else -5
                    elif case in ('hostile', 'neutral'):
                        player.ea = 255 if case == 'hostile' else 128
                    else:
                        player.area = 'BD0102'
                    self.assert_waits(model)

    def test_unseen_close_player_waits_without_legacy_fallthrough(self):
        model = self.model()
        model.actors['PLAYER1'].visible = False
        self.assert_waits(model)
        model.actors['PLAYER1'].visible = True
        self.assertEqual('StartDialogueNoSet', model.step()[-1][0])

    def test_failed_or_interrupted_dialogue_retries_after_two_seconds(self):
        model = self.model()
        self.assertEqual('StartDialogueNoSet', model.step()[-1][0])
        for time in (0, 1, 1.99):
            model.time = time
            self.assert_waits(model)
        model.time = 2
        self.assertEqual('StartDialogueNoSet', model.step()[-1][0])
        self.assertEqual(4, model.timers[('LOCALS', 'CSR256_BENCE_TRY')])
        model.time = 4
        model.dialogue_available = False
        self.assert_waits(model)
        model.time = 9
        model.dialogue_available = True
        self.assertEqual('StartDialogueNoSet', model.step()[-1][0])
        self.assertEqual(293, model.variables[('GLOBAL', 'BD_PLOT')])

    def test_departing_player_can_be_followed_even_while_retry_timer_runs(self):
        model = self.model()
        model.step()
        model.time = 1
        model.actors['PLAYER1'].position = at(10)
        self.assertEqual([('MoveToObject', 'PLAYER1')], model.step())

    def test_other_stages_plots_and_areas_retain_original_script_behavior(self):
        cases = [('stage', stage) for stage in (0, 1, 2, 4)]
        cases += [('plot', plot) for plot in (292, 294, 295, 480)]
        cases += [('area', area) for area in ('BD0102', 'BD4300')]
        for field, value in cases:
            with self.subTest(field=field, value=value):
                model = self.model()
                if field == 'stage':
                    model.variables[('BD2000', 'CSR256_STAGE')] = value
                elif field == 'plot':
                    model.variables[('GLOBAL', 'BD_PLOT')] = value
                else:
                    model.me.area = value
                expected = ('SetGlobal', 'FOREIGN_TAIL', 'GLOBAL', 7) if field == 'plot' else (
                    'SetGlobal', 'LEGACY_STARTED', 'LOCALS', 1)
                self.assertEqual([expected], model.step())
                self.assertEqual({}, model.timers)

    def test_native_dialogue_plot_advance_immediately_releases_suppression(self):
        model = self.model()
        model.step()
        # Existing DLG owns the 293 -> 294 transition; this helper must not do it.
        model.variables[('GLOBAL', 'BD_PLOT')] = 294
        self.assertEqual([('SetGlobal', 'FOREIGN_TAIL', 'GLOBAL', 7)], model.step())


@unittest.skipUnless(WEIDU.is_file(), 'real WeiDU unavailable; set WEIDU_EXE')
class AftermathInstallerTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix='csr256-aftermath-install-')
        self.addCleanup(temp.cleanup)
        self.game = Path(temp.name)
        write_aftermath_fixture(self.game)
        result = run_weidu(self.game, 'fixture/setup-fixture.tp2', '--force-install-list', '0')
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def install(self, package='aftermath.tp2'):
        return run_weidu(self.game, package, '--force-install-list', '256')

    def protected(self):
        return {name: (self.game / name).read_bytes() for name in (
            'dialog.tlk', 'lang/en_us/dialog.tlk', 'chitin.key', 'data/csr291.bif')}

    def test_only_bence_script_changes_original_suffix_and_dialogue_survive(self):
        before = tree(self.game / 'override')
        protected = self.protected()
        original = decompile(self.game, 'BDBENCE.BCS')
        result = self.install()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        after = tree(self.game / 'override')
        self.assertEqual(set(before), set(after))
        self.assertEqual(['BDBENCE.BCS'], [name for name in before if before[name] != after[name]])
        self.assertEqual(protected, self.protected())
        installed = decompile(self.game, 'BDBENCE.BCS')
        self.assertTrue(installed.endswith(original), installed)
        self.assertEqual(3, len(AftermathDecisions(installed).blocks) - len(AftermathDecisions(original).blocks))

    def test_uninstall_restores_every_original_override_and_text_resource(self):
        before = tree(self.game / 'override')
        protected = self.protected()
        result = self.install()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        result = run_weidu(self.game, 'aftermath.tp2', '--force-uninstall-list', '256')
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(before, tree(self.game / 'override'))
        self.assertEqual(protected, self.protected())

    def test_native_initialization_is_preserved_before_pending_wrap_suppression(self):
        native = '''IF
  Global("bd_ai_controls","locals",0)
  OR(2)
    AreaCheck("bd2000")
    AreaCheck("bd4300")
THEN
  RESPONSE #100
    SetGlobal("bd_ai_controls","locals",1)
    SetGlobal("bd_no_assist","locals",2)
    SetGlobal("bd_no_combat","locals",1)
    SetGlobal("bd_no_search","locals",1)
END
'''
        (self.game/'fixture/bdbence.baf').write_text(BASE + native)
        result = run_weidu(self.game, 'fixture/setup-fixture.tp2', '--force-install-list', '0')
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        original = decompile(self.game, 'BDBENCE.BCS')
        result = self.install()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        installed = decompile(self.game, 'BDBENCE.BCS')
        self.assertTrue(installed.endswith(original))
        model = AftermathDecisions(installed)
        model.actors['PLAYER1'].position = at(30)
        self.assertEqual([
            ('SetGlobal', 'BD_AI_CONTROLS', 'LOCALS', 1),
            ('SetGlobal', 'BD_NO_ASSIST', 'LOCALS', 2),
            ('SetGlobal', 'BD_NO_COMBAT', 'LOCALS', 1),
            ('SetGlobal', 'BD_NO_SEARCH', 'LOCALS', 1)], model.step())
        self.assertEqual([('MoveToObject', 'PLAYER1')], model.step())

    def test_valid_empty_script_is_not_mistaken_for_an_existing_patch(self):
        # COUNT_REGEXP_INSTANCES returns -1 on this empty decompiled buffer in
        # WeiDU249. It is a valid unpatched BCS, not a positive marker count.
        (self.game / 'override' / 'bdbence.bcs').write_bytes(b'SC\nSC\n')
        before = tree(self.game / 'override')
        protected = self.protected()
        result = self.install()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(3, len(AftermathDecisions(decompile(self.game, 'BDBENCE.BCS')).blocks))
        self.assertEqual(protected, self.protected())
        result = run_weidu(self.game, 'aftermath.tp2', '--force-uninstall-list', '256')
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(before, tree(self.game / 'override'))

    def test_duplicate_preflight_fails_without_changing_installed_resources(self):
        result = self.install()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        before = tree(self.game / 'override')
        protected = self.protected()
        result = self.install('duplicate.tp2')
        self.assertNotEqual(0, result.returncode)
        self.assertIn('the owned Bence approach is already installed', result.stdout + result.stderr)
        self.assertEqual(before, tree(self.game / 'override'))
        self.assertEqual(protected, self.protected())


if __name__ == '__main__':
    unittest.main()
