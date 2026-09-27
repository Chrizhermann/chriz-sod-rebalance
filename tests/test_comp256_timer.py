"""Compile the bridge clock with WeiDU and replay its actual BAF decisions.

All resources are synthetic and disposable. The bounded interpreter verifies
saved timer state and branch priorities; it does not simulate engine frame
timing, rendering, sound playback, or the native Game Over screen.
"""
from __future__ import annotations

import copy
from pathlib import Path
import re
import shutil
import tempfile
import unittest

from test_comp256_ai import Actor, Decisions, ROOT, WEIDU, atom, call, tree, write_fake_game
from test_comp197_xp import decompile, run_weidu


DEMO = ('CSR256FM', 'CSR256CM', 'CSR256E1', 'CSR256E2', 'CSR256F1', 'CSR256F2')
BASE = '''IF
  Global("CSR256_STAGE","BD2000",1)
THEN
  RESPONSE #100
    SetGlobal("CSR256_STAGE","BD2000",2)
    DisplayStringNoName(Player1,123)
END

IF
  Global("CSR256_STAGE","BD2000",2)
  CombatCounter(0)
THEN
  RESPONSE #100
    SetGlobal("CSR256_STAGE","BD2000",3)
    CreateCreatureObject("bdbence",Player1,6,0,0)
END

IF
  True()
THEN
  RESPONSE #100
    NoAction()
END
'''


def write_timer_ids(game):
    """Use native EE signatures, including Wait=63 and SmallWait=83."""
    entries = {
        'action': '''0 NoAction()
26 PlaySound(S:Sound*)
30 SetGlobal(S:Name*,S:Area*,I:Value*)
36 Continue()
63 Wait(I:Time*)
83 SmallWait(I:Time*)
115 SetGlobalTimer(S:Name*,S:Area*,I:Time*GTimes)
120 StartCutScene(S:CutScene*)
120 StartCutSceneEx(S:CutScene*,I:evaluateConditions*BOOLEAN)
121 StartCutSceneMode()
122 EndCutSceneMode()
127 CutSceneId(O:Object*)
202 FadeToColor(P:Point*,I:Blue*)
254 ScreenShake(P:Point*,I:Duration*)
262 DisplayStringNoName(O:Object*,I:StrRef*)
269 DisplayStringHead(O:Object*,I:StrRef*)
346 DisplayStringNoNameHead(O:Object*,I:StrRef*)
366 GameOver(I:StrRef*)
387 SetCutSceneBreakable(I:BOOL*BOOLEAN)
388 DisplayStringHeadNoLog(O:Object*,I:StrRef*)
457 PlaySoundNotRanged(S:Sound*)
''',
        'trigger': '''0x400D Exists(O:Object*)
0x400F Global(S:Name*,S:Area*,I:Value*)
0x4011 HPGT(O:Object*,I:HitPoints*)
0x4023 True()
0x4034 GlobalGT(S:Name*,S:Area*,I:Value*)
0x4035 GlobalLT(S:Name*,S:Area*,I:Value*)
0x4037 StateCheck(O:Object*,I:State*STATE)
0x4040 GlobalTimerExpired(S:Name*,S:Area*)
0x4041 GlobalTimerNotExpired(S:Name*,S:Area*)
0x4051 Dead(S:Name*)
0x4083 CombatCounter(I:Number*)
0x4089 OR(I:OrCount*)
0x40CB InMyArea(O:Object*)
0x40D0 Difficulty(I:Amount*DIFFLEV)
0x40D1 DifficultyGT(I:Amount*DIFFLEV)
0x40D2 DifficultyLT(I:Amount*DIFFLEV)
0x40E9 NightmareModeOn()
0x40FA StoryModeOn()
''',
        'state': '128 STATE_STONE_DEATH\n',
        'difflev': '1 EASIEST\n2 EASY\n3 NORMAL\n4 HARD\n5 HARDEST\n',
        'gtimes': '',
    }
    for name, content in entries.items():
        path = game / 'override' / f'{name}.ids'
        current = path.read_text() if path.exists() else 'IDS V1.0\n'
        additions = content.splitlines()
        replaced = {int(line.split()[0], 0) for line in additions}
        lines = [line for line in current.splitlines()
                 if not line.strip() or line.startswith('IDS')
                 or int(line.split()[0], 0) not in replaced]
        path.write_text('\n'.join(lines + additions) + '\n', encoding='ascii')
    # Valid empty PCM WAVs stand in for native rockfall resources. This fixture
    # validates lookup and compilation, never actual audio delivery.
    wave = (b'RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00'
            b'\x01\x00\x01\x00\x44\xac\x00\x00\x88\x58\x01\x00'
            b'\x02\x00\x10\x00data\x00\x00\x00\x00')
    for name in ('amb_e17a.wav', 'amb_e17b.wav'):
        (game / 'override' / name).write_bytes(wave)


def write_timer_package(game):
    """Copy the real clock library into a synthetic game of either size."""
    mod = game / 'chriz-sod-remix'
    (mod / 'lib').mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / 'chriz-sod-remix/lib/comp256_timer.tpa', mod / 'lib')
    (mod / 'languages/english').mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / 'chriz-sod-remix/languages/english/setup.tra',
                 mod / 'languages/english')
    for name in ('timer', 'duplicate'):
        (game / f'{name}.tp2').write_text(f'''BACKUP ~{name}-backup~
AUTHOR ~test~
LANGUAGE ~English~ ~english~ ~chriz-sod-remix/languages/english/setup.tra~
BEGIN ~bridge clock~ DESIGNATED 258
INCLUDE ~chriz-sod-remix/lib/comp256_timer.tpa~
LAF csr256_timer_preflight INT_VAR check_world=1 RET already_installed END
ACTION_IF NOT already_installed BEGIN
  LAF csr256_timer_install END
END
''', encoding='ascii')


def write_timer_fixture(game, source=BASE):
    write_fake_game(game)
    write_timer_ids(game)
    write_timer_package(game)
    (game / 'fixture').mkdir()
    (game / 'fixture/bd2000.baf').write_text(source, encoding='ascii')
    (game / 'fixture/setup-fixture.tp2').write_text('''BACKUP ~fixture-backup~
AUTHOR ~test~ BEGIN ~legacy bridge clock seam~
COMPILE ~fixture/bd2000.baf~
''', encoding='ascii')
    result = run_weidu(game, 'fixture/setup-fixture.tp2', '--force-install-list', '0')
    if result.returncode:
        raise AssertionError(result.stdout + result.stderr)


class TimerDecisions(Decisions):
    """Only timer-related production blocks; reject unknown calls explicitly."""
    def __init__(self, baf):
        super().__init__(baf)
        self.variables = {('BD2000', 'CSR256_STAGE'): 2, ('GLOBAL', 'BD_PLOT'): 280}
        self.actors.update({name: Actor() for name in DEMO})
        self.actors.update({name: Actor() for name in ('CSR256G1', 'CSR256G2')})
        self.dead = set()
        self.story = False
        self.nightmare = False
        self.combat_counter = 10

    def condition(self, text, context=None):
        text = text.strip()
        if text.startswith('!'):
            return not self.condition(text[1:], context)
        fn, args = call(text)
        values = [atom(a) for a in args]
        if fn == 'True':
            return True
        if fn == 'StoryModeOn':
            return self.story
        if fn == 'NightmareModeOn':
            return self.nightmare
        if fn == 'Dead':
            return values[0] in self.dead
        if fn == 'CombatCounter':
            return self.combat_counter == values[0]
        if fn in ('GlobalGT', 'GlobalLT'):
            value = self.variables.get((values[1], values[0]), 0)
            return value > values[2] if fn.endswith('GT') else value < values[2]
        if fn == 'GlobalTimerExpired':
            key = (values[1], values[0])
            return key in self.timers and self.time >= self.timers[key]
        if fn in ('Difficulty', 'DifficultyGT', 'DifficultyLT'):
            level = {'EASIEST': 1, 'EASY': 2, 'NORMAL': 3,
                     'HARD': 4, 'HARDEST': 5}.get(values[0], values[0])
            return {'Difficulty': self.difficulty == level,
                    'DifficultyGT': self.difficulty > level,
                    'DifficultyLT': self.difficulty < level}[fn]
        if fn == 'StateCheck':
            actor = self.actor(args[0], context)
            state = 128 if values[1] == 'STATE_STONE_DEATH' else values[1]
            return actor is not None and bool(actor.state & state)
        if fn not in {'Global', 'GlobalTimerNotExpired', 'HPGT', 'Exists', 'InMyArea'}:
            raise AssertionError(f'Unsupported timer condition: {text}')
        return super().condition(text, context)

    def act(self, text):
        fn, args = call(text.strip())
        if fn in {'NoAction', 'DisplayStringNoName', 'DisplayStringHead',
                  'DisplayStringNoNameHead', 'DisplayStringHeadNoLog',
                  'PlaySound', 'PlaySoundNotRanged', 'ScreenShake',
                  'StartCutScene', 'StartCutSceneMode', 'EndCutSceneMode',
                  'StartCutSceneEx', 'SetCutSceneBreakable',
                  'CutSceneId', 'FadeToColor', 'Wait', 'GameOver'}:
            self.actions.append((fn, *(atom(a) for a in args)))
        else:
            super().act(text)

    def value(self, name):
        return self.variables.get(('BD2000', name), 0)

    def kill_demolition(self):
        self.dead.update(DEMO)
        for name in DEMO:
            self.actors[name].hp = 0

    def reload(self, baf):
        """Save inputs only; reconstruct script decisions from compiled source."""
        other = TimerDecisions(baf)
        for name in ('variables', 'timers', 'time', 'actors', 'dead', 'story',
                     'difficulty', 'nightmare', 'combat_counter'):
            setattr(other, name, copy.deepcopy(getattr(self, name)))
        return other


def messages(actions):
    return [a for a in actions if a[0].startswith('DisplayString')]


@unittest.skipUnless(WEIDU.is_file(), 'real WeiDU unavailable; set WEIDU_EXE')
class CompiledBridgeTimerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='csr256-clock-decisions-')
        cls.addClassCleanup(cls.temp.cleanup)
        cls.game = Path(cls.temp.name)
        write_timer_fixture(cls.game)
        result = run_weidu(cls.game, 'timer.tp2', '--force-install-list', '258')
        if result.returncode:
            raise AssertionError(result.stdout + result.stderr)
        cls.baf = decompile(cls.game, 'bd2000.bcs')
        cls.failure = decompile(cls.game, 'csr26end.bcs')

    def model(self, difficulty=3):
        model = TimerDecisions(self.baf)
        model.difficulty = difficulty
        return model

    def started(self, difficulty=3):
        model = self.model(difficulty)
        model.step()
        self.assertEqual(1, model.value('CSR256_CLOCK'))
        return model

    def test_all_difficulties_store_exact_initial_and_quarter_deadlines(self):
        for difficulty, seconds in ((1, 600), (2, 480), (3, 420), (4, 360), (5, 300)):
            with self.subTest(difficulty=difficulty):
                model = self.model(difficulty)
                model.time = 100
                actions = model.step()
                self.assertEqual(1, model.value('CSR256_CLOCK'))
                self.assertEqual(seconds, model.value('CSR256_LIMIT'))
                self.assertEqual({('BD2000', 'CSR256_DUE'): 100 + seconds,
                                  ('BD2000', 'CSR256_W25'): 100 + seconds // 4,
                                  ('BD2000', 'CSR256_W50'): 100 + seconds // 2,
                                  ('BD2000', 'CSR256_W75'): 100 + seconds * 3 // 4}, model.timers)
                self.assertTrue(messages(actions))
                self.assertTrue(all(a[1] == 'PLAYER1' for a in messages(actions)))

    def test_legacy_of_bhaal_flag_uses_five_minutes_independent_of_slider(self):
        for difficulty in range(1, 6):
            with self.subTest(difficulty=difficulty):
                model = self.model(difficulty)
                model.nightmare = True
                model.step()
                self.assertEqual(300, model.value('CSR256_LIMIT'))

    def test_ready_stage_advances_before_any_clock_starts(self):
        model = self.model()
        model.variables[('BD2000', 'CSR256_STAGE')] = 1
        model.step()
        self.assertEqual(2, model.value('CSR256_STAGE'))
        self.assertEqual(0, model.value('CSR256_CLOCK'))
        model.step()
        self.assertEqual(1, model.value('CSR256_CLOCK'))

    def test_unrelated_plot_does_not_start_timer(self):
        for plot in (293, 294):
            with self.subTest(plot=plot):
                model = self.model()
                model.variables[('GLOBAL', 'BD_PLOT')] = plot
                self.assertFalse(messages(model.step()))
                self.assertEqual({}, model.timers)

    def test_story_has_no_deadlines_or_milestones_and_cannot_be_reenabled(self):
        model = self.model()
        model.story = True
        model.step()
        self.assertEqual(3, model.value('CSR256_CLOCK'))
        self.assertEqual({}, model.timers)
        model.story = False
        model.time = 99999
        self.assertFalse(messages(model.step()))
        self.assertEqual(3, model.value('CSR256_CLOCK'))

    def test_story_still_confirms_when_demolition_is_stopped(self):
        model = self.model()
        model.story = True
        opening = messages(model.step())
        model.kill_demolition()
        confirmation = messages(model.step())
        self.assertEqual(2, model.value('CSR256_CLOCK'))
        self.assertTrue(confirmation)
        self.assertNotEqual(opening, confirmation)
        self.assertFalse(messages(model.step()))
        self.assertEqual({}, model.timers)

    def test_already_defeated_roster_does_not_start_a_spurious_countdown(self):
        model = self.model()
        model.kill_demolition()
        model.step()
        self.assertEqual(2, model.value('CSR256_CLOCK'))
        self.assertEqual({}, model.timers)

    def test_story_enabled_at_expiry_disables_failure_permanently(self):
        model = self.started()
        model.time = model.timers[('BD2000', 'CSR256_DUE')]
        model.story = True
        actions = model.step()
        self.assertEqual(3, model.value('CSR256_CLOCK'))
        self.assertFalse(any(a[0].startswith('StartCutScene') for a in actions))
        model.story = False
        model.time += 10000
        self.assertFalse(messages(model.step()))
        self.assertEqual(3, model.value('CSR256_CLOCK'))

    def test_difficulty_change_and_reload_do_not_reset_deadlines(self):
        model = self.started(5)
        original = model.timers.copy()
        for difficulty in (1, 4, 2, 5):
            model = model.reload(self.baf)
            model.time += 5
            model.difficulty = difficulty
            self.assertFalse(messages(model.step()))
            self.assertEqual(original, model.timers)
            self.assertEqual(300, model.value('CSR256_LIMIT'))

    def test_quarter_warnings_once_each_including_reload(self):
        model = self.started(5)
        observed = []
        for index, time in enumerate((75, 150, 225), 1):
            model.time = time - 1
            self.assertFalse(messages(model.step()))
            model.time = time
            actions = model.step()
            self.assertEqual(index, model.value('CSR256_WARN'))
            warning = messages(actions)
            self.assertTrue(warning)
            self.assertTrue(all(a[1] == 'PLAYER1' for a in warning))
            observed.append(tuple(a[-1] for a in warning))
            model = model.reload(self.baf)
            self.assertFalse(messages(model.step()))
        self.assertEqual(3, len(set(observed)))

    def test_delayed_processing_reports_only_most_urgent_warning(self):
        model = self.started(5)
        model.time = 230
        actions = model.step()
        self.assertEqual(3, model.value('CSR256_WARN'))
        # A paired overhead/log delivery is one warning, not three catch-up ones.
        self.assertEqual(1, len({a[-1] for a in messages(actions)}))
        self.assertFalse(messages(model.step()))

    def test_six_demolition_deaths_stop_clock_despite_living_guards_and_combat(self):
        model = self.started()
        model.kill_demolition()
        actions = model.step()
        self.assertEqual(2, model.value('CSR256_CLOCK'))
        self.assertEqual(2, model.value('CSR256_STAGE'))
        self.assertTrue(messages(actions))
        self.assertGreater(model.combat_counter, 0)
        self.assertGreater(model.actors['CSR256G1'].hp, 0)
        model.time = 99999
        self.assertFalse(messages(model.step()))
        self.assertFalse(any(a[0].startswith('StartCutScene') for a in model.actions))

    def test_each_demolition_survivor_keeps_clock_running(self):
        for survivor in DEMO:
            with self.subTest(survivor=survivor):
                model = self.started()
                model.kill_demolition()
                model.dead.remove(survivor)
                model.actors[survivor].hp = 1
                model.step()
                self.assertEqual(1, model.value('CSR256_CLOCK'))

    def test_death_wins_at_exact_expiry_and_suppresses_pending_warnings(self):
        model = self.started(5)
        model.time = 300
        model.kill_demolition()
        actions = model.step()
        self.assertEqual(2, model.value('CSR256_CLOCK'))
        self.assertEqual(0, model.value('CSR256_WARN'))
        self.assertFalse(any(a[0].startswith('StartCutScene') for a in actions))

    def test_removed_elemental_counts_as_defeated_for_banishment_counterplay(self):
        model = self.started()
        model.kill_demolition()
        model.dead.remove('CSR256E1')
        del model.actors['CSR256E1']
        model.step()
        self.assertEqual(2, model.value('CSR256_CLOCK'))
        # Native Exists cannot distinguish RemoveCreature from temporary Maze;
        # this test proves compatibility semantics, not Maze immunity.

    def test_invisible_or_offscreen_survivor_is_not_treated_as_removed(self):
        model = self.started()
        model.kill_demolition()
        model.dead.remove('CSR256FM')
        model.actors['CSR256FM'].hp = 52
        model.actors['CSR256FM'].visible = False
        model.actors['CSR256FM'].position = (9999, 9999)
        model.step()
        self.assertEqual(1, model.value('CSR256_CLOCK'))

    def test_petrified_demolition_actor_counts_as_defeated(self):
        model = self.started()
        model.kill_demolition()
        model.dead.remove('CSR256FM')
        model.actors['CSR256FM'].hp = 52
        model.actors['CSR256FM'].state = 128
        model.step()
        self.assertEqual(2, model.value('CSR256_CLOCK'))

    def test_expired_return_starts_failure_once_without_catching_up_warnings(self):
        model = self.started(5)
        # An inactive area receives no script steps while game time advances.
        model.time = 1000
        model = model.reload(self.baf)
        actions = model.step()
        self.assertEqual(4, model.value('CSR256_CLOCK'))
        self.assertEqual(4, model.value('CSR256_STAGE'))
        self.assertEqual(0, model.value('CSR256_WARN'))
        launches = [a for a in actions if a[0].startswith('StartCutScene')]
        self.assertEqual([('StartCutSceneEx', 'CSR26END', 0)], launches)
        launch_at = actions.index(launches[0])
        self.assertLess(actions.index(('SetGlobal', 'CSR256_CLOCK', 'BD2000', 4)), launch_at)
        self.assertLess(actions.index(('SetGlobal', 'CSR256_STAGE', 'BD2000', 4)), launch_at)
        model = model.reload(self.baf)
        self.assertFalse(any(a[0].startswith('StartCutScene') for a in model.step()))

    def test_failure_resource_uses_fade_and_native_gameover_without_explosion_or_party_kill(self):
        actions = TimerDecisions(self.failure).step()
        names = [a[0] for a in actions]
        self.assertEqual('CutSceneId', names[0])
        self.assertIn(('SetCutSceneBreakable', 0), actions)
        self.assertEqual('GameOver', names[-1])
        self.assertLess(names.index('FadeToColor'), names.index('GameOver'))
        self.assertEqual(3, sum(a[1] for a in actions if a[0] == 'Wait'))
        self.assertEqual({actions[-1][1]}, {a[-1] for a in messages(actions)})
        self.assertFalse({'Kill', 'ReallyForceSpell', 'ReallyForceSpellRES',
                          'CreateVisualEffect', 'CreateVisualEffectObject',
                          'CreateCreature'} & set(names))


@unittest.skipUnless(WEIDU.is_file(), 'real WeiDU unavailable; set WEIDU_EXE')
class TimerInstallerSafetyTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix='csr256-clock-install-')
        self.addCleanup(temp.cleanup)
        self.game = Path(temp.name)

    def test_unknown_ready_seam_is_rejected_without_resource_or_string_writes(self):
        write_timer_fixture(self.game, BASE.replace('DisplayStringNoName(Player1,123)', 'NoAction()'))
        before = tree(self.game / 'override')
        tlk = (self.game / 'lang/en_us/dialog.tlk').read_bytes()
        result = run_weidu(self.game, 'timer.tp2', '--force-install-list', '258')
        self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(before, tree(self.game / 'override'))
        self.assertEqual(tlk, (self.game / 'lang/en_us/dialog.tlk').read_bytes())

    def test_failure_helper_collision_is_rejected_before_writes(self):
        write_timer_fixture(self.game)
        (self.game / 'override/csr26end.bcs').write_bytes(b'FOREIGN HELPER')
        before = tree(self.game / 'override')
        tlk = (self.game / 'lang/en_us/dialog.tlk').read_bytes()
        result = run_weidu(self.game, 'timer.tp2', '--force-install-list', '258')
        self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(before, tree(self.game / 'override'))
        self.assertEqual(tlk, (self.game / 'lang/en_us/dialog.tlk').read_bytes())

    def test_second_application_is_byte_exact_noop_and_uninstall_restores_original(self):
        write_timer_fixture(self.game)
        original = tree(self.game / 'override')
        for name in ('timer', 'duplicate'):
            before = tree(self.game / 'override')
            result = run_weidu(self.game, f'{name}.tp2', '--force-install-list', '258')
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            if name == 'duplicate':
                self.assertEqual(before, tree(self.game / 'override'))
        for name in ('duplicate', 'timer'):
            result = run_weidu(self.game, f'{name}.tp2', '--force-uninstall-list', '258')
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(original, tree(self.game / 'override'))


@unittest.skipUnless(WEIDU.is_file(), 'real WeiDU unavailable; set WEIDU_EXE')
class TimerContinuityCompatibilityTests(unittest.TestCase):
    """Real 256/258/197 patches around the shared, independent 115 fork fixture."""
    def setUp(self):
        import test_comp256_world as world_fixture
        import test_comp115_comp256_order as continuity_fixture

        self.world_fixture = world_fixture
        self.continuity_fixture = continuity_fixture
        self.harness = world_fixture.BridgeWorldTests()
        self.harness.setUp()
        self.addCleanup(self.harness.doCleanups)
        self.game = self.harness.game
        write_timer_ids(self.game)
        write_timer_package(self.game)
        library = 'chriz-sod-remix/lib/comp197_bridge.tpa'
        shutil.copy2(ROOT / library, self.game / library)
        (self.game / 'skie.tp2').write_text('''BACKUP ~skie-backup~
AUTHOR ~test~
BEGIN ~production197 bridge spawn patch~ DESIGNATED 197
INCLUDE ~chriz-sod-remix/lib/comp197_bridge.tpa~
COPY_EXISTING ~bd2000.bcs~ ~override~
  DECOMPILE_AND_PATCH BEGIN
    LPF csr197_bridge_spawns END
  END
BUT_ONLY
''', encoding='ascii')
        self.spawn = '    CreateCreature("bdskie",[2485.2655],NW)'
        self.spawn_line = re.compile(
            r'(?mi)^[ \t]*CreateCreature\("bdskie",\[2485\.2655\],NW\)'
            r'[ \t]*(?://[^\n]*)?\n')

    def install(self, package, component):
        result = self.harness.weidu(package, '--force-install-list', str(component))
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn('SUCCESSFULLY INSTALLED', result.stdout)

    def world(self, *, fork):
        source = self.world_fixture.SCRIPT.replace(
            '    CreateCreature("bdbence",[2425.2660],NW)',
            '    CreateCreature("bdbence",[2425.2660],NW)\n' + self.spawn)
        if fork:
            source = self.continuity_fixture.continuity_script(source)
        self.harness.fixture(source)
        self.install('world.tp2', 256)

    def assert_timed_fork(self):
        source = self.harness.decompile()
        routes = self.continuity_fixture.assert_victory_routes(self, source)
        for guard, _ in routes:
            self.assertEqual(1, guard.count('global("csr256_clock","bd2000",2)'))
            # The 197 matcher consumes the eight actor guards as its prefix;
            # the additional clock check must follow that recognized prefix.
            self.assertGreater(guard.index('global("csr256_clock","bd2000",2)'),
                               guard.index('statecheck("csr256f2",state_stone_death)'))
        return source

    def remove_only_skie(self, expected_count):
        before_source = self.harness.decompile()
        before_files = tree(self.harness.override)
        expected, count = self.spawn_line.subn('', before_source)
        self.assertEqual(expected_count, count)
        self.install('skie.tp2', 197)
        self.assertEqual(self.world_fixture.compact(expected),
                         self.world_fixture.compact(self.harness.decompile()))
        after_files = tree(self.harness.override)
        self.assertEqual({'BD2000.BCS'}, {
            key for key in before_files.keys() | after_files.keys()
            if before_files.get(key) != after_files.get(key)})

    def test_115_fork_then_timer_then_197_preserves_clock_and_khalid_routes(self):
        self.world(fork=True)
        self.install('timer.tp2', 258)
        self.assert_timed_fork()
        self.remove_only_skie(2)
        self.assert_timed_fork()

    def test_115_fork_then_197_then_timer_preserves_both_guarded_routes(self):
        self.world(fork=True)
        self.remove_only_skie(2)
        self.install('timer.tp2', 258)
        source = self.assert_timed_fork()
        self.assertNotIn('CREATECREATURE("BDSKIE"', self.world_fixture.compact(source))

    def test_unforked_timer_then_197_removes_only_skie_preserving_safety_guards(self):
        self.world(fork=False)
        self.install('timer.tp2', 258)
        self.remove_only_skie(1)
        source = self.harness.decompile()
        routes = [(guard, actions) for guard, actions in
                  self.continuity_fixture.baf_blocks(source)
                  if 'createcreatureobject("bdbence",player1,6,0,0)' in actions]
        self.assertEqual(1, len(routes))
        guard, actions = routes[0]
        for condition in ('global("csr256_clock","bd2000",2)',
                          'global("csr256_stage","bd2000",2)',
                          'combatcounter(0)', 'inmyarea(player1)', 'hpgt(player1,0)'):
            self.assertIn(condition, guard)
        self.assertIn('actionoverride("khalid",savelocation(', actions)


if __name__ == '__main__':
    unittest.main()
