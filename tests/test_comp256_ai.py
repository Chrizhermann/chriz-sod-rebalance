"""Real WeiDU compilation and decisions from the resulting encounter scripts.

All writes go to disposable synthetic games. The decision runner interprets the
compiled/decompiled BAF conditions; it is not a second hand-written AI policy.
It models availability, priorities and spending, not engine spell effects/pathing.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
import math
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'research/scripts'))
from test_comp291_installer import WEIDU, ROOT, MOD, write_fake_game, tree

SPELLS = {
    'stoneskin': ('WIZARD_STONE_SKIN', 2408, 4),
    'mirrorimage': ('WIZARD_MIRROR_IMAGE', 2212, 2),
    'shield': ('WIZARD_SHIELD', 2114, 1),
    'fireshield': ('WIZARD_FIRE_SHIELD_RED', 2418, 4),
    'protfire': ('WIZARD_PROTECTION_FROM_FIRE', 2319, 4),
    'spiritarmor': ('WIZARD_SPIRIT_ARMOR', 2414, 4),
    'minordeflect': ('WIZARD_MINOR_SPELL_DEFLECTION', 2318, 3),
    'haste': ('WIZARD_HASTE', 2305, 3),
    'fireball': ('WIZARD_FIREBALL', 2304, 3),
    'flamearrow': ('WIZARD_FLAME_ARROW', 2303, 3),
    'slow': ('WIZARD_SLOW', 2312, 3),
    'glitterdust': ('WIZARD_GLITTERDUST', 2224, 2),
    'grease': ('WIZARD_GREASE', 2101, 1),
    'breach': ('WIZARD_BREACH', 2513, 5),
    'malison': ('WIZARD_GREATER_MALISON', 2412, 4),
    'magicmissile': ('WIZARD_MAGIC_MISSILE', 2112, 1),
}

ACTION_IDS = '''IDS V1.0
23 MoveToPoint(P:Point*)
30 SetGlobal(S:Name*,S:Area*,I:Value*)
31 SpellRES(S:RES*,O:Target*)
34 UseItem(S:Object*,O:Target*)
36 Continue()
86 SetInterrupt(I:State*Boolean)
115 SetGlobalTimer(S:Name*,S:Area*,I:Time*GTimes)
134 AttackReevaluate(O:Target*,I:ReevaluationPeriod*)
147 RemoveSpellRES(S:RES*)
181 ReallyForceSpellRES(S:RES*,O:Target*)
245 SaveObjectLocation(S:Area*,S:Global*,O:Object*)
297 MoveToSavedLocation(S:Global*,S:Area*)
'''
TRIGGER_IDS = '''IDS V1.0
0x400B Allegiance(O:Object*,I:Allegience*EA)
0x400E General(O:Object*,I:General*GENERAL)
0x400D Exists(O:Object*)
0x400F Global(S:Name*,S:Area*,I:Value*)
0x4011 HPGT(O:Object*,I:HitPoints*)
0x4018 Range(O:Object*,I:Range*)
0x401C See(O:Object*)
0x402D HPPercentLT(O:Object*,I:HitPoints*)
0x4031 HaveSpellRES(S:Spell*)
0x4037 StateCheck(O:Object*,I:State*STATE)
0x4041 GlobalTimerNotExpired(S:Name*,S:Area*)
0x4045 CheckStatGT(O:Object*,I:Value*,I:StatNum*STATS)
0x4046 CheckStatLT(O:Object*,I:Value*,I:StatNum*STATS)
0x4061 HasItem(S:ResRef*,O:Object*)
0x407E AreaCheck(S:ResRef*)
0x4089 OR(I:OrCount*)
0x40CB InMyArea(O:Object*)
0x40D1 DifficultyGT(I:Amount*DIFFLEV)
0x40E0 NextTriggerObject(O:Object*)
0x40E2 CheckSpellState(O:Object*,I:State*SPLSTATE)
0x40E3 NearLocation(O:Object*,I:PointX*,I:PointY*,I:Range*)
'''
STATE = {'STATE_SILENCED': 0x1000, 'STATE_SLOWED': 0x10000,
         'STATE_BLIND': 0x40000, 'STATE_MIRRORIMAGE': 0x40000000}
STATS = {'RESISTFIRE': 14, 'RESISTMAGIC': 18, 'SPELLFAILUREMAGE': 51,
         'SANCTUARY': 63, 'STONESKINS': 88, 'WIZARD_SPELL_DEFLECTION': 116,
         'WIZARD_PROTECTION_FROM_MAGIC_WEAPONS': 128}


def spell_bytes(level: int, cast_range: int = 30, projectile: int = 0) -> bytes:
    data = bytearray(0x72 + 0x28)
    data[:8] = b'SPL V1  '
    struct.pack_into('<H', data, 0x1c, 1)
    struct.pack_into('<I', data, 0x34, level)
    struct.pack_into('<IHIHH', data, 0x64, 0x72, 1, len(data), 0, 0)
    data[0x72 + 0xc] = 4
    struct.pack_into('<HH', data, 0x72 + 0xe, cast_range, 1)
    struct.pack_into('<H', data, 0x72 + 0x26, projectile)
    return bytes(data)


def write_ai_fixture(game: Path, *, vanilla: bool = False) -> None:
    write_fake_game(game)
    ids = {'action': ACTION_IDS, 'trigger': TRIGGER_IDS,
           'object': 'IDS V1.0\n1 Myself\n10 LastAttackerOf\n12 NearestEnemyOf\n' +
                     ''.join(f'{20+n} Player{n}\n' for n in range(1, 7)),
           'ea': 'IDS V1.0\n0 ANYONE\n2 PC\n255 ENEMY\n',
           'general': 'IDS V1.0\n0 ANYONE\n1 HUMANOID\n5 ELEMENTAL\n',
           'state': 'IDS V1.0\n' + ''.join(f'{v} {k}\n' for k, v in STATE.items()),
           'stats': 'IDS V1.0\n' + ''.join(f'{v} {k}\n' for k, v in STATS.items()),
           'difflev': 'IDS V1.0\n1 EASIEST\n2 EASY\n3 NORMAL\n4 HARD\n5 HARDEST\n',
           'projectl': 'IDS V1.0\n37 FIREBALL\n100 GREASE\n157 INAREAPA\n',
           'splstate': 'IDS V1.0\n71 GLITTERDUST\n',
           'gtimes': 'IDS V1.0\n6 ONE_ROUND\n', 'spell': 'IDS V1.0\n'}
    for short, (symbol, number, level) in SPELLS.items():
        if vanilla and short == 'stoneskin':
            number = 2415
        if vanilla and short == 'protfire':
            level = 3
        ids['spell'] += f'{number} {symbol}\n'
        (game / 'override' / f'spwi{number-2000}.spl').write_bytes(
            spell_bytes(level, 20 if short in ('grease', 'haste') else 30,
                        {'fireball': 38, 'grease': 101, 'haste': 158}.get(short, 0)))
    for name, radius in [('fireball', 256), ('grease', 110), ('inareapa', 256)]:
        pro = bytearray(0x300)
        pro[:8] = b'PRO V1.0'
        struct.pack_into('<H', pro, 8, 3)
        struct.pack_into('<H', pro, 0x206, radius)
        (game / 'override' / f'{name}.pro').write_bytes(pro)
    for name, contents in ids.items():
        (game / 'override' / f'{name}.ids').write_text(contents, encoding='ascii')
    shutil.copytree(MOD, game / 'chriz-sod-remix')
    (game / 'test.tp2').write_text('''BACKUP ~backup~ AUTHOR ~test~ BEGIN ~AI fixture~
INCLUDE ~chriz-sod-remix/lib/comp256_spells.tpa~
INCLUDE ~chriz-sod-remix/lib/comp256_ai.tpa~
LAM csr256_spells_preflight
OUTER_SET csr256_home_x=1500
OUTER_SET csr256_home_y=1950
OUTER_SET csr256_leash=18
LAF csr256_ai_install END
PRINT ~RESOLVED %csr256_stoneskin_res% %csr256_protfire_level%~
''', encoding='ascii')


def run_weidu(game: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([str(WEIDU), *args, '--game', str(game),
                           '--use-lang', 'en_US', '--no-exit-pause'], cwd=game,
                          capture_output=True, text=True, encoding='utf-8',
                          errors='replace', timeout=60)


@unittest.skipUnless(WEIDU.is_file(), 'real WeiDU unavailable; set WEIDU_EXE')
class SpellAndCompilationTests(unittest.TestCase):
    def test_installed_and_vanilla_spell_identities_compile_without_scs(self):
        for vanilla in (False, True):
            with self.subTest(vanilla=vanilla), tempfile.TemporaryDirectory() as d:
                game = Path(d)
                write_ai_fixture(game, vanilla=vanilla)
                original = tree(game / 'override')
                result = run_weidu(game, 'test.tp2', '--force-install-list', '0')
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                expected = 'SPWI415' if vanilla else 'SPWI408'
                self.assertIn(f'RESOLVED {expected} {3 if vanilla else 4}', result.stdout)
                for name in ('csr26fma', 'csr26cma', 'csr26mel'):
                    self.assertTrue((game / 'override' / f'{name}.bcs').is_file())
                current = tree(game / 'override')
                for path, digest in original.items():
                    self.assertEqual(digest, current[path], path)

    def test_missing_or_invalid_spell_fails_before_compilation(self):
        for fault in ('missing', 'level', 'effects', 'symbol', 'ability', 'projectile', 'collision'):
            with self.subTest(fault=fault), tempfile.TemporaryDirectory() as d:
                game = Path(d)
                write_ai_fixture(game)
                path = game / 'override/spwi408.spl'
                if fault == 'missing':
                    path.unlink()
                elif fault == 'collision':
                    (game / 'override/csr26fma.bcs').write_bytes(b'foreign sentinel')
                elif fault == 'projectile':
                    path = game / 'override/grease.pro'
                    data = bytearray(path.read_bytes())
                    struct.pack_into('<I', data, 0x2c, 0x8000)  # rectangular
                    path.write_bytes(data)
                elif fault == 'symbol':
                    path = game / 'override/spell.ids'
                    path.write_text(path.read_text().replace('WIZARD_STONE_SKIN', 'NO_STONESKIN'))
                else:
                    data = bytearray(path.read_bytes())
                    if fault == 'level':
                        struct.pack_into('<I', data, 0x34, 0)
                    elif fault == 'ability':
                        struct.pack_into('<H', data, 0x72 + 0x10, 14)
                    else:
                        struct.pack_into('<H', data, 0x72 + 0x1e, 1)
                    path.write_bytes(data)
                original = tree(game / 'override')
                result = run_weidu(game, 'test.tp2', '--force-install-list', '0')
                self.assertNotEqual(0, result.returncode)
                self.assertEqual(original, tree(game / 'override'))


def arguments(text: str) -> list[str]:
    """Split a BAF call without losing nested object selectors/overrides."""
    output, start, depth, quoted = [], 0, 0, False
    for i, char in enumerate(text):
        if char == '"':
            quoted = not quoted
        if not quoted:
            depth += (char == '(') - (char == ')')
            if char == ',' and depth == 0:
                output.append(text[start:i].strip())
                start = i + 1
    if text[start:].strip():
        output.append(text[start:].strip())
    return output


def call(text: str) -> tuple[str, list[str]]:
    match = re.fullmatch(r'(\w+)\((.*)\)', text.strip())
    if not match:
        raise AssertionError(f'Unsupported BAF call: {text}')
    return match[1], arguments(match[2])


def atom(text: str):
    text = text.strip()
    if text.startswith('"'):
        return text[1:-1].upper()
    constants = dict(STATE, **STATS, ENEMY=255, PC=2, HUMANOID=1,
                     NORMAL=3, TRUE=1, FALSE=0, ONE_ROUND=6, GLITTERDUST=71)
    if text in constants:
        return constants[text]
    try:
        return int(text, 0)
    except ValueError:
        return text.upper()


def at(x: float, y: float = 0) -> tuple[float, float]:
    return 1500 + 16*x, 1950 + 12*y


@dataclass
class Actor:
    position: tuple[float, float] = (1500, 1950)
    hp: int = 52
    hp_percent: int = 100
    ea: int = 255
    area: str = 'BD2000'
    visible: bool = True
    state: int = 0
    general: int = 1
    stats: Counter = field(default_factory=Counter)
    spell_states: set = field(default_factory=set)


class Decisions:
    """A bounded interpreter for the *decompiled production* script subset.

    Spell() consumption is modeled at cast start. Interrupted casts deliver no
    effects; exact engine interruption timing and moving targets need native QA.
    Unknown conditions/actions fail the test instead of silently succeeding.
    """
    def __init__(self, baf: str, role: str = 'fire', prepared: bool = True):
        source = re.sub(r'//[^\n]*', '', baf)
        self.blocks = [(c.strip().splitlines(), a.strip().splitlines())
                       for c, a in re.findall(
                           r'\bIF\s+(.*?)\bTHEN\s+RESPONSE\s+#100\s+(.*?)\bEND',
                           source, re.S)]
        self.actors = {'MYSELF': Actor(), 'PLAYER1': Actor(position=at(12), ea=2)}
        self.actors['CSR256FM' if role == 'fire' else 'CSR256CM'] = self.actors['MYSELF']
        self.variables = {('BD2000', 'CSR256_STAGE'): 2,
                          ('LOCALS', 'CSR256_PREP'): int(prepared)}
        self.timers = {}
        self.time = 0
        self.difficulty = 3
        self.book = Counter()
        self.items = Counter(POTN52=1)
        self.actions = []
        self.interrupted = False
        self.interruptible = True
        self.saved = {}

    @property
    def me(self):
        return self.actors['MYSELF']

    @staticmethod
    def distance(a: Actor, b: Actor) -> float:
        return math.hypot((a.position[0]-b.position[0])/16,
                          (a.position[1]-b.position[1])/12)

    def actor(self, name: str, context: Actor | None = None) -> Actor | None:
        if name.upper() == 'MYSELF':
            return context or self.me
        if name.startswith('NearestEnemyOf('):
            reference = self.actor(call(name)[1][0], context)
            enemies = [a for a in self.actors.values()
                       if a.hp > 0 and a.ea == 2 and a.area == reference.area]
            return min(enemies, key=lambda a: self.distance(reference, a), default=None)
        if name.startswith('LastAttackerOf('):
            return self.actors.get('LASTATTACKER')
        return self.actors.get(str(atom(name)).upper())

    def condition(self, text: str, context: Actor | None = None) -> bool:
        text = text.strip()
        if text.startswith('!'):
            return not self.condition(text[1:], context)
        fn, args = call(text)
        values = [atom(a) for a in args]
        actor = self.actor(args[0], context) if args else None
        source = context or self.me
        if fn == 'TriggerOverride':
            return actor is not None and self.condition(args[1], actor)
        if fn == 'Global':
            return self.variables.get((values[1], values[0]), 0) == values[2]
        if fn == 'GlobalTimerNotExpired':
            return self.timers.get((values[1], values[0]), 0) > self.time
        if fn == 'AreaCheck':
            return source.area == values[0]
        if fn == 'DifficultyGT':
            return self.difficulty > values[0]
        if fn == 'HaveSpellRES':
            return self.book[values[0]] > 0
        if fn == 'HasItem':
            return self.items[values[0]] > 0
        if fn == 'Exists':
            return actor is not None
        if actor is None:
            return False
        if fn == 'Allegiance':
            return actor.ea == values[1]
        if fn == 'General':
            return actor.general == values[1]
        if fn == 'HPGT':
            return actor.hp > values[1]
        if fn == 'HPPercentLT':
            return actor.hp_percent < values[1]
        if fn == 'See':
            return actor.visible and actor.hp > 0 and actor.area == source.area
        if fn == 'InMyArea':
            return actor.area == source.area
        if fn == 'Range':
            return actor.area == source.area and self.distance(source, actor) <= values[1]
        if fn == 'NearLocation':
            return self.distance(actor, Actor(position=(values[1], values[2]))) <= values[3]
        if fn == 'StateCheck':
            return bool(actor.state & values[1])
        if fn == 'CheckSpellState':
            return values[1] in actor.spell_states
        if fn in ('CheckStatGT', 'CheckStatLT'):
            stat = actor.stats[values[2]]
            return stat > values[1] if fn.endswith('GT') else stat < values[1]
        raise AssertionError(f'Unsupported condition: {text}')

    def conditions(self, lines: list[str]) -> bool:
        i = 0
        accepted = True
        while i < len(lines):
            fn, args = call(lines[i].strip().lstrip('!'))
            if fn == 'OR':
                count = int(args[0])
                accepted &= any(self.condition(s) for s in lines[i+1:i+1+count])
                i += count + 1
            else:
                accepted &= self.condition(lines[i])
                i += 1
        return accepted

    def effect(self, resource: str, target: Actor):
        # Minimal observable defense markers, independent of priority logic.
        if resource == 'SPWI408':
            target.stats[STATS['STONESKINS']] = 6
        if resource == 'SPWI212':
            target.state |= STATE['STATE_MIRRORIMAGE']
        if resource == 'SPWI318':
            target.stats[STATS['WIZARD_SPELL_DEFLECTION']] = 1
        if resource == 'SPWI312':
            target.state |= STATE['STATE_SLOWED']

    def act(self, text: str):
        fn, args = call(text.strip())
        values = [atom(a) for a in args]
        self.actions.append((fn, *values))
        if fn == 'SetGlobal':
            self.variables[(values[1], values[0])] = values[2]
        elif fn == 'SetGlobalTimer':
            self.timers[(values[1], values[0])] = self.time + values[2]
        elif fn == 'SetInterrupt':
            self.interruptible = bool(values[0])
        elif fn in ('RemoveSpellRES', 'SpellRES'):
            if self.book[values[0]] <= 0:
                raise AssertionError(f'Spell spent without a copy: {text}')
            self.book[values[0]] -= 1
            if fn == 'SpellRES' and not self.interrupted:
                self.effect(values[0], self.actor(args[1]))
        elif fn == 'ReallyForceSpellRES':
            self.effect(values[0], self.actor(args[1]))
        elif fn == 'SaveObjectLocation':
            self.saved[(values[0], values[1])] = self.actor(args[2]).position
        elif fn == 'UseItem':
            self.items[values[0]] -= 1
        elif fn not in ('Continue', 'AttackReevaluate', 'MoveToPoint', 'MoveToSavedLocation'):
            raise AssertionError(f'Unsupported action: {text}')

    def step(self) -> list[tuple]:
        start = len(self.actions)
        for conditions, actions in self.blocks:
            if self.conditions(conditions):
                for action in actions:
                    self.act(action)
                if not any(a.strip() == 'Continue()' for a in actions):
                    break
        return self.actions[start:]

    def casts(self):
        return [action[1:] for action in self.step() if action[0] == 'SpellRES']


@unittest.skipUnless(WEIDU.is_file(), 'real WeiDU unavailable; set WEIDU_EXE')
class CompiledDecisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='csr256-decisions-')
        cls.addClassCleanup(cls.temp.cleanup)
        game = Path(cls.temp.name)
        write_ai_fixture(game)
        result = run_weidu(game, 'test.tp2', '--force-install-list', '0')
        if result.returncode:
            raise AssertionError(result.stdout + result.stderr)
        cls.baf = {}
        for name in ('csr26fma', 'csr26cma', 'csr26mel'):
            result = run_weidu(game, str(game / 'override' / f'{name}.bcs'), '--out', str(game))
            if result.returncode:
                raise AssertionError(result.stdout + result.stderr)
            cls.baf[name] = (game / f'{name}.baf').read_text()

    def fire(self, **kwargs):
        return Decisions(self.baf['csr26fma'], **kwargs)

    def control(self, **kwargs):
        return Decisions(self.baf['csr26cma'], role='control', **kwargs)

    def test_preparation_is_once_only_and_spends_exact_reserved_allocation(self):
        for role, make, extras in [('fire', self.fire, ('SPWI418', 'SPWI319')),
                                   ('control', self.control, ('SPWI414', 'SPWI318'))]:
            with self.subTest(role=role):
                model = make(prepared=False)
                model.variables[('BD2000', 'CSR256_STAGE')] = 1
                model.book.update(SPWI408=2, SPWI212=3, SPWI114=1)
                model.book.update(extras)
                if role == 'control':
                    model.book['SPWI318'] += 1
                model.step()
                self.assertEqual(1, model.book['SPWI408'])
                self.assertEqual(2, model.book['SPWI212'])
                self.assertEqual(0, model.book['SPWI114'])
                self.assertEqual(int(role == 'control'), model.book['SPWI318'])
                self.assertTrue(model.interruptible)
                self.assertEqual(model.me.position, model.saved[('LOCALS', 'CSR256_HOME')])
                self.assertEqual(5, sum(a[0] == 'RemoveSpellRES' for a in model.actions))
                self.assertEqual([], model.step())

    def test_defense_beats_haste_both_recasts_share_timer_and_reserves_run_out(self):
        m = self.fire()
        m.book.update(SPWI408=1, SPWI212=2, SPWI305=1)
        m.actors['PLAYER1'].position = at(4)
        m.actors['CSR256G1'] = Actor(position=at(6))
        m.actors['CSR256G2'] = Actor(position=at(7))
        self.assertEqual([('SPWI408', 'MYSELF')], m.casts())
        m.time = 6
        m.me.stats[STATS['STONESKINS']] = 0
        self.assertNotIn(('SPWI212', 'MYSELF'), m.casts())
        # Haste may use the free cast interval at t=6; renewal stays on t=7.
        m.time = 13
        self.assertEqual([('SPWI212', 'MYSELF')], m.casts())
        m.time = 20
        self.assertNotIn(('SPWI212', 'MYSELF'), m.casts())  # intact images
        m.me.state = 0
        self.assertEqual([('SPWI212', 'MYSELF')], m.casts())
        m.time = 27
        m.me.state = 0
        self.assertEqual([], m.casts())
        self.assertEqual(0, m.book['SPWI408'])
        self.assertEqual(0, m.book['SPWI212'])

    def test_intact_skins_are_not_renewed_and_stage_is_required(self):
        m = self.fire()
        m.book.update(SPWI408=1, SPWI212=2)
        m.me.stats[STATS['STONESKINS']] = 5
        m.actors['PLAYER1'].position = at(4)
        self.assertEqual([], m.casts())
        m.me.stats.clear()
        for stage in (0, 1, 3):
            m.variables[('BD2000', 'CSR256_STAGE')] = stage
            self.assertEqual([], m.casts())
        self.assertEqual(1, m.book['SPWI408'])

    def test_ward_is_missing_only_finite_and_yields_to_melee_defense(self):
        m = self.control()
        m.book.update(SPWI408=1, SPWI318=1)
        m.actors['PLAYER1'].position = at(4)
        self.assertEqual([('SPWI408', 'MYSELF')], m.casts())
        m.time = 7
        self.assertEqual([('SPWI318', 'MYSELF')], m.casts())
        m.time = 14
        m.me.stats[STATS['WIZARD_SPELL_DEFLECTION']] = 0
        self.assertEqual([], m.casts())

    def test_haste_uses_two_owned_living_hostile_actors_and_late_candidates(self):
        m = self.fire()
        m.book['SPWI305'] = 1
        m.actors['CSR256G1'] = Actor(position=at(2), hp=0)
        m.actors['CSR256G2'] = Actor(position=at(2), ea=2)
        m.actors['CSR256E1'] = Actor(position=at(2), area='AR0602')
        m.actors['CSR256E2'] = Actor(position=at(100))
        m.actors['CSR256F1'] = Actor(position=at(7))
        m.actors['CSR256F2'] = Actor(position=at(8))
        self.assertEqual([('SPWI305', 'CSR256F1')], m.casts())
        self.assertEqual(0, m.book['SPWI305'])
        m.time = 10
        m.book['SPWI305'] = 1  # even an unintended extra copy cannot rebuff
        self.assertEqual([], m.casts())

    def test_previously_hasted_owned_group_is_not_cast_on_again(self):
        m = self.fire()
        m.book['SPWI305'] = 1
        m.variables[('LOCALS', 'CSR256_HASTE')] = 1
        m.actors['CSR256E1'] = Actor(position=at(6))
        m.actors['CSR256E2'] = Actor(position=at(7))
        # SR supplies no unique durable Haste marker; the fresh encounter group
        # is identified by its own successful/attempted cast contract instead.
        self.assertEqual([], m.casts())
        self.assertEqual(1, m.book['SPWI305'])

    def test_control_has_finite_magic_missile_fallback(self):
        m = self.control()
        m.book['SPWI112'] = 1
        self.assertEqual([('SPWI112', 'PLAYER1')], m.casts())
        m.time = 7
        self.assertEqual([], m.casts())

    def test_glitterdust_checks_installed_marker_and_does_not_repeat_same_pc(self):
        m = self.control()
        m.book['SPWI224'] = 2
        m.actors['PLAYER1'].spell_states.add(71)
        m.actors['PLAYER2'] = Actor(position=at(10), ea=2)
        self.assertEqual([('SPWI224', 'PLAYER2')], m.casts())
        m.time = 7
        self.assertEqual([], m.casts())
        self.assertEqual(1, m.book['SPWI224'])

    def test_haste_does_not_count_controller_random_army_or_single_owned_ally(self):
        m = self.fire()
        m.book['SPWI305'] = 1
        for name in ('CSR256CM', 'RANDOM_ARMY', 'BARREL_SPOT', 'CSR256E1'):
            m.actors[name] = Actor(position=at(4))
        self.assertEqual([], m.casts())
        self.assertEqual(1, m.book['SPWI305'])
        self.assertNotIn('STATE_HASTED', self.baf['csr26fma'])

    def test_interrupted_haste_spends_once_without_free_retry_or_double_remove(self):
        m = self.fire()
        m.book['SPWI305'] = 1
        m.actors['CSR256E1'] = Actor(position=at(6))
        m.actors['CSR256E2'] = Actor(position=at(7))
        m.interrupted = True
        self.assertEqual([('SPWI305', 'CSR256E1')], m.casts())
        m.time = 10
        self.assertEqual([], m.casts())
        self.assertEqual(0, m.book['SPWI305'])
        self.assertFalse(any(a[:2] == ('RemoveSpellRES', 'SPWI305') for a in m.actions))

    def test_fireball_skips_unsafe_pc_then_selects_safe_pc_ignoring_fire_elemental(self):
        m = self.fire()
        m.book['SPWI304'] = 1
        m.actors['PLAYER1'].position = at(24)
        m.actors['CSR256G1'] = Actor(position=at(24))
        m.actors['PLAYER2'] = Actor(position=at(0, 26), ea=2)
        m.actors['CSR256F1'] = Actor(position=at(0, 26), general=5)
        self.assertEqual([('SPWI304', 'PLAYER2')], m.casts())
        for friend in ('CSR256FM', 'CSR256CM', 'CSR256G1', 'CSR256G2', 'CSR256E1', 'CSR256E2'):
            with self.subTest(friend=friend):
                m = self.fire()
                m.book.update(SPWI304=1, SPWI303=1)
                m.actors['PLAYER1'].position = at(24)
                m.actors[friend] = Actor(position=at(24))
                self.assertEqual([('SPWI303', 'PLAYER1')], m.casts())
                self.assertEqual(1, m.book['SPWI304'])

    def test_grease_must_be_outside_pursuit_region_and_clear_of_all_eight(self):
        m = self.control()
        m.book['SPWI101'] = 1
        m.me.position = at(12)
        m.actors['PLAYER1'].position = at(24)
        self.assertEqual([], m.casts())  # free of allies but inside expanded leash
        m.actors['PLAYER1'].position = at(29)
        m.actors['CSR256F1'] = Actor(position=at(28), general=5)
        self.assertEqual([], m.casts())  # fire immunity does not imply Grease immunity
        del m.actors['CSR256F1']
        self.assertEqual([('SPWI101', 'PLAYER1')], m.casts())

    def test_breach_checks_protection_and_does_not_mistake_natural_mr_for_buff(self):
        m = self.fire()
        m.book['SPWI513'] = 1
        m.actors['PLAYER1'].stats[STATS['RESISTMAGIC']] = 50
        self.assertEqual([], m.casts())
        m.actors['PLAYER2'] = Actor(position=at(10), ea=2)
        m.actors['PLAYER2'].stats[STATS['STONESKINS']] = 4
        self.assertEqual([('SPWI513', 'PLAYER2')], m.casts())

    def test_malison_difficulty_and_already_slowed_target_selection(self):
        for difficulty, expected in ((3, 'SPWI312'), (4, 'SPWI412'), (5, 'SPWI412')):
            with self.subTest(difficulty=difficulty):
                m = self.control()
                m.difficulty = difficulty
                m.book.update(SPWI412=1, SPWI312=3)
                self.assertEqual([(expected, 'PLAYER1')], m.casts())
        m = self.control()
        m.book['SPWI312'] = 3
        m.actors['PLAYER1'].state = STATE['STATE_SLOWED']
        m.actors['PLAYER2'] = Actor(position=at(15), ea=2)
        self.assertEqual([('SPWI312', 'PLAYER2')], m.casts())

    def test_silence_and_spell_failure_do_not_spend_magic_and_potion_is_once_only(self):
        m = self.fire()
        m.book['SPWI303'] = 2
        m.me.state = STATE['STATE_SILENCED']
        self.assertEqual([], m.casts())
        m.me.hp_percent = 20
        self.assertTrue(any(a[0] == 'UseItem' for a in m.step()))
        m.time = 10
        m.items['POTN52'] = 1
        self.assertFalse(any(a[0] == 'UseItem' for a in m.step()))
        m.me.state = 0
        m.me.stats[STATS['SPELLFAILUREMAGE']] = 100
        self.assertEqual([], m.casts())
        self.assertEqual(2, m.book['SPWI303'])

    def test_displaced_wizard_returns_before_spending_offensive_spells(self):
        m = self.fire()
        m.me.position = at(25)
        m.actors['PLAYER1'].position = at(27)
        m.book['SPWI112'] = 1
        self.assertEqual([('MoveToSavedLocation', 'CSR256_HOME', 'LOCALS')], m.step())
        self.assertEqual(1, m.book['SPWI112'])

    def test_melee_leash_and_guard_interception(self):
        m = Decisions(self.baf['csr26mel'])
        m.actors['PLAYER1'].position = at(30)
        self.assertEqual([], m.step())
        m.me.position = at(20)
        self.assertEqual('MoveToPoint', m.step()[0][0])
        m.me.position = at(0)
        m.actors['CSR256CM'] = Actor(position=at(8))
        m.actors['LASTATTACKER'] = Actor(position=at(9), ea=2)
        self.assertEqual('AttackReevaluate', m.step()[0][0])


if __name__ == '__main__':
    unittest.main()
