"""Public component 115 against copied effective EET resources.

Set CSR_DEV_GAME to a locally supplied EET fixture source, and WEIDU_EXE if WeiDU
249 is not on the normal test path. The local, ignored baseline at
.worktrees/csr115-fixture/game (captured 2026-09-10 before component 115) is preferred
over the documented dev copy, which is the last fallback. Game-owned
resources are read only and never committed; all installer writes and deliberate
negative-fixture mutations happen in a TemporaryDirectory. This is installer and
compiled-resource evidence, not live dialogue selection or engine acceptance.
"""

from __future__ import annotations

import os
import re
import shutil
import struct
import subprocess
import tempfile
import unittest
from dataclasses import dataclass, replace
from pathlib import Path

from test_bdscry_compat import ROOT, WEIDU, _write_key_and_bif


LOCAL_BASELINE = ROOT / ".worktrees/csr115-fixture/game"
DEV_GAME = Path(os.environ.get("CSR_DEV_GAME") or
                (LOCAL_BASELINE if LOCAL_BASELINE.is_dir() else
                 r"C:\Games\Baldur's Gate II Enhanced Edition modded - dev eet install"))
RESOURCE_NAMES = {
    "bd0103.bcs", "bd1000.bcs", "bd7100.bcs", "bd2000.bcs", "bd2100.bcs",
    "bdkhalid.bcs", "bdjaheir.bcs",
    "bdcut24.bcs", "bdc205ca.bcs", "bdc205cb.bcs", "bdc205cc.bcs", "cutskip.bcs",
    "bdc205aa.bcs", "bdc205ab.bcs", "bdc205ac.bcs", "bdc205ad.bcs", "bdc205ae.bcs",
    "bdban037.bcs", "bdban103.bcs",
    "bdkhalid.dlg", "khalij.dlg", "bdkhalij.dlg", "bdbfort.dlg", "bdjaheir.dlg",
    "jaheiraj.dlg", "bdjaheij.dlg", "bdneera.dlg", "bdbarghe.dlg", "bdjegg.dlg",
    "bdwynan.dlg", "bdvoghil.bcs", "bdvoghil.dlg", "bdbfort.cre", "bd2100.are", "bd2000.are",
    "bddialog.2da", "pdialog.2da",
    "k#telbgt.bcs", "ar0602.bcs", "campaign.2da", "startare.2da",
}


def normalized(script: str) -> str:
    """Ignore insignificant compiler formatting for trigger/action comparisons."""
    return re.sub(r"\s+", "", script).casefold()


def baf_blocks(source: str) -> list[tuple[str, str]]:
    source = re.sub(r"//[^\n]*", "", source)
    return [(normalized(match.group(1)), normalized(match.group(2))) for match in
            re.finditer(r"(?ms)^\s*IF\s*\n(.*?)^\s*THEN\s*\n(.*?)^\s*END\s*$", source)]


def entry_guard_holds(trigger: str, *, khalid_slot=0, arrived=range(1, 7), route=0,
                      named_lookup=False, been_in_party=True):
    """Evaluate the limited entry predicates after real WeiDU compilation.

    Lookup results are inputs so a failed named lookup can be tested separately
    from stable party slots and from an incomplete transfer.
    """
    tokens = re.findall(r'!?\w+\([^()]*\)', trigger)
    assert ''.join(tokens) == trigger, trigger
    variables = {'chapter': 7, 'bd_plot': 52, 'csr_kh_fort': route}

    def atom(token):
        negated = token.startswith('!')
        name, arguments = token.lstrip('!').split('(', 1)
        args = [value.strip('"') for value in arguments[:-1].split(',')]
        if name in ('global', 'globallt', 'globalgt'):
            value, expected = variables.get(args[0], 0), int(args[2])
            result = {'global': value == expected, 'globallt': value < expected,
                      'globalgt': value > expected}[name]
        elif name == 'inpartyallowdead':
            result = named_lookup
        elif name == 'name':
            result = args[0] == 'khalid' and int(args[1][6:]) == khalid_slot
        elif name == 'numinpartylt':
            result = 6 < int(args[0])
        elif name == 'inmyarea':
            result = int(args[0][6:]) in arrived
        elif name == 'statecheck':
            result = False
        elif name == 'beeninparty':
            result = been_in_party
        else:
            raise AssertionError(f'Unsupported entry predicate: {token}')
        return not result if negated else result

    results, index = [], 0
    while index < len(tokens):
        token = tokens[index]
        index += 1
        if token.startswith('or('):
            count = int(token[3:-1])
            results.append(any(atom(t) for t in tokens[index:index + count]))
            index += count
        else:
            results.append(atom(token))
    return all(results)


def biff_only_ids(game: Path, override_names: set[str]) -> dict[str, bytes]:
    """Read missing effective IDS by KEY ordinal; never run WeiDU on the source."""
    key = (game / "chitin.key").read_bytes()
    if key[:8] != b"KEY V1  ":
        raise AssertionError("fixture source does not contain a KEY V1 index")
    bif_count, resource_count, bif_table, resource_table = struct.unpack_from("<4I", key, 8)
    result = {}
    for index in range(resource_count):
        raw_name, resource_type, locator = struct.unpack_from(
            "<8sHI", key, resource_table + index * 14)
        name = raw_name.rstrip(b"\0").decode("ascii").casefold() + ".ids"
        if resource_type != 1008 or name in override_names:
            continue
        bif_index, ordinal = locator >> 20, locator & 0xFFFFF
        if bif_index >= bif_count:
            raise AssertionError(f"invalid fixture BIF index for {name}")
        _, offset, length, _ = struct.unpack_from("<IIHH", key, bif_table + bif_index * 12)
        relative = key[offset:offset + length].rstrip(b"\0").decode("ascii")
        path = game / relative.replace("\\", "/")
        with path.open("rb") as stream:
            header = stream.read(20)
            if header[:8] != b"BIFFV1  ":
                raise AssertionError(f"unsupported compressed fixture BIF: {path}")
            count, _, table = struct.unpack_from("<3I", header, 8)
            if ordinal >= count:
                raise AssertionError(f"invalid fixture BIF ordinal for {name}")
            stream.seek(table + ordinal * 16)
            _, payload_offset, payload_size, found_type, _ = struct.unpack("<3I2H", stream.read(16))
            if found_type != resource_type:
                raise AssertionError(f"fixture BIF type differs from KEY for {name}")
            stream.seek(payload_offset)
            result[name] = stream.read(payload_size)
            if len(result[name]) != payload_size:
                raise AssertionError(f"truncated fixture IDS payload: {name}")
    return result


@dataclass(frozen=True)
class Transition:
    flags: int
    text: int
    journal: int
    trigger: str
    action: str
    destination: str
    state: int


@dataclass(frozen=True)
class DialogState:
    text: int
    trigger: str
    transitions: tuple[Transition, ...]


def dialog_states(data: bytes) -> tuple[DialogState, ...]:
    """Read semantic DLG records without dependence on decompiler annotations."""
    if len(data) < 0x30 or data[:8] != b"DLG V1.0":
        raise AssertionError("not a DLG V1.0 resource")
    state_count, state_offset, transition_count, transition_offset = struct.unpack_from(
        "<4I", data, 0x08)

    def scripts(header_offset: int) -> list[str]:
        table, count = struct.unpack_from("<II", data, header_offset)
        if table + count * 8 > len(data):
            raise AssertionError("DLG script table outside resource")
        result = []
        for index in range(count):
            offset, length = struct.unpack_from("<II", data, table + index * 8)
            if offset + length > len(data):
                raise AssertionError("DLG script outside resource")
            result.append(normalized(data[offset:offset + length].decode("ascii")))
        return result

    state_triggers = scripts(0x18)
    transition_triggers = scripts(0x20)
    actions = scripts(0x28)
    if state_offset + state_count * 16 > len(data):
        raise AssertionError("DLG state table outside resource")
    if transition_offset + transition_count * 32 > len(data):
        raise AssertionError("DLG transition table outside resource")
    transitions = []
    for index in range(transition_count):
        flags, text, journal, trigger, action, destination, state = struct.unpack_from(
            "<5I8sI", data, transition_offset + index * 32)
        transitions.append(Transition(
            flags, text, journal,
            transition_triggers[trigger] if flags & 2 else "",
            actions[action] if flags & 4 else "",
            destination.rstrip(b"\0").decode("ascii").casefold(), state))
    states = []
    for index in range(state_count):
        text, first, count, trigger = struct.unpack_from(
            "<3Ii", data, state_offset + index * 16)
        if first + count > transition_count:
            raise AssertionError("DLG state transition run outside resource")
        states.append(DialogState(text, state_triggers[trigger] if trigger >= 0 else "",
                                  tuple(transitions[first:first + count])))
    return tuple(states)


def ordinary_transitions(state: DialogState) -> tuple[Transition, ...]:
    """Project mutually exclusive additions onto the preserved noncarry route."""
    result = []
    for transition in state.transitions:
        trigger = re.sub(r'!global\("csr_(?:kh_carry|kh_fort)","global",1\)',
                         "", transition.trigger)
        if re.search(r'global\("csr_(?:kh_carry|kh_fort)","global",1\)', trigger):
            continue
        flags = transition.flags if trigger else transition.flags & ~2
        result.append(replace(transition, trigger=trigger, flags=flags))
    return tuple(result)


def tlk_text(data: bytes, strref: int) -> str:
    count, text_offset = struct.unpack_from("<II", data, 10)
    if not 0 <= strref < count:
        raise AssertionError(f"string reference outside TLK: {strref}")
    offset, length = struct.unpack_from("<II", data, 18 + strref * 26 + 18)
    return data[text_offset + offset:text_offset + offset + length].decode("utf-8")


class EffectiveKhalidGame:
    """Minimal game shell with real inputs; source is never a WeiDU --game target."""

    def __init__(self, resources: dict[str, bytes], tlk: bytes, *, prerequisite=True):
        self.temporary = tempfile.TemporaryDirectory(prefix="csr-khalid-continuity-")
        self.root = Path(self.temporary.name) / "game"
        self.root.mkdir()
        override = self.root / "override"
        override.mkdir()
        _write_key_and_bif(self.root)
        for filename, payload in resources.items():
            (override / filename).write_bytes(payload)
        (override / "eet.flag").write_text("disposable EET fixture marker")
        for relative in ("dialog.tlk", "lang/en_us/dialog.tlk"):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(tlk)
        shutil.copytree(ROOT / "chriz-sod-remix", self.root / "chriz-sod-remix")
        # A fabricated prerequisite applies only to this disposable fake game.
        (self.root / "WeiDU.log").write_text(
            "~CHRIZ-SOD-REMIX/SETUP-CHRIZ-SOD-REMIX.TP2~ #0 #110 // fixture prerequisite\n"
            if prerequisite else "")
        self.before = self.tree()
        self.tlk_before = tlk
        self.protected_before = {
            name: (self.root / name).read_bytes()
            for name in ("chitin.key", "data/bdsctest.bif", "dialog.tlk")}

    def cleanup(self):
        self.temporary.cleanup()

    def tree(self):
        return {path.name.casefold(): path.read_bytes()
                for path in (self.root / "override").iterdir() if path.is_file()}

    def install(self):
        result = subprocess.run([
            str(WEIDU), "chriz-sod-remix/setup-chriz-sod-remix.tp2",
            "--force-install-list", "115", "--language", "0", "--use-lang", "en_us",
            "--no-exit-pause", "--noautoupdate", "--quick-log",
        ], cwd=self.root, capture_output=True, text=True, errors="replace", timeout=60)
        return result, result.stdout + "\n" + result.stderr

    def decompile(self, *resources: str) -> dict[str, str]:
        output = self.root.parent / "decompiled"
        output.mkdir(exist_ok=True)
        available = {path.name.casefold(): path for path in (self.root / "override").iterdir()
                     if path.is_file()}
        result = subprocess.run([
            str(WEIDU), *(str(available[resource.casefold()]) for resource in resources),
            "--game", str(self.root), "--out", str(output), "--no-exit-pause",
            "--noautoupdate", "--use-lang", "en_us",
        ], cwd=output, capture_output=True, text=True, errors="replace", timeout=60)
        if result.returncode or "FATAL ERROR" in result.stdout + result.stderr:
            raise AssertionError(result.stdout + result.stderr)
        paths = {path.name.casefold(): path for path in output.iterdir() if path.is_file()}
        return {resource: paths[Path(resource).stem.casefold() +
                               (".baf" if resource.endswith(".bcs") else ".d")].read_text(
                                   encoding="utf-8", errors="replace")
                for resource in resources}


@unittest.skipUnless(WEIDU.is_file(), f"WeiDU unavailable: {WEIDU}")
@unittest.skipUnless((DEV_GAME / "override").is_dir(),
                     "effective EET fixture unavailable; set CSR_DEV_GAME")
class KhalidContinuityInstallerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = {path.name.casefold(): path for path in (DEV_GAME / "override").iterdir()
                  if path.is_file()}
        missing = RESOURCE_NAMES - source.keys()
        if missing:
            raise AssertionError(f"effective EET fixture lacks {sorted(missing)}")
        cls.resources = {name: path.read_bytes() for name, path in source.items()
                         if name in RESOURCE_NAMES or
                         (path.suffix.casefold() == ".ids" and name != "add_spell.ids")}
        cls.resources.update(biff_only_ids(DEV_GAME, set(source)))
        cls.tlk = (DEV_GAME / "lang/en_us/dialog.tlk").read_bytes()
        cls._installed_game = None

    def game(self, **kwargs):
        game = EffectiveKhalidGame(self.resources, self.tlk, **kwargs)
        self.addCleanup(game.cleanup)
        return game

    def installed_game(self):
        # Positive checks inspect the same read-only result, so compiling this
        # effective 34 MB TLK fixture is done once rather than once per assertion.
        cls = type(self)
        if cls._installed_game is None:
            game = EffectiveKhalidGame(self.resources, self.tlk)
            cls.addClassCleanup(game.cleanup)
            result, transcript = game.install()
            self.assertEqual(0, result.returncode, transcript)
            self.assertIn("SUCCESSFULLY INSTALLED", transcript)
            self.assertNotIn("WARNING:", transcript)
            cls._installed_game = game
        return cls._installed_game

    def assert_untouched_failure(self, game, before, transcript):
        self.assertNotIn("SUCCESSFULLY INSTALLED", transcript)
        self.assertEqual(before, game.tree())
        self.assertEqual(game.tlk_before, (game.root / "lang/en_us/dialog.tlk").read_bytes())
        for name, payload in game.protected_before.items():
            self.assertEqual(payload, (game.root / name).read_bytes(), name)

    def test_component_requires_keep_companions_before_touching_resources(self):
        game = self.game(prerequisite=False)
        _, transcript = game.install()
        self.assertIn("SKIPPING:", transcript)
        self.assert_untouched_failure(game, game.before, transcript)

    def test_missing_required_dialog_fails_without_partial_resources_or_tlk(self):
        game = self.game()
        (game.root / "override/bdbfort.dlg").unlink()
        before = game.tree()
        _, transcript = game.install()
        self.assert_untouched_failure(game, before, transcript)
        self.assertRegex(transcript, r"SKIPPING:|NOT INSTALLED DUE TO ERRORS")

    def test_changed_original_fort_route_is_rejected_before_publishing(self):
        game = self.game()
        path = game.root / "override/bdbfort.dlg"
        data = bytearray(path.read_bytes())
        state_offset = struct.unpack_from("<I", data, 0x0C)[0]
        transition_offset = struct.unpack_from("<I", data, 0x14)[0]
        first_transition = struct.unpack_from("<I", data, state_offset + 2 * 16 + 4)[0]
        destination = transition_offset + first_transition * 32 + 20
        self.assertEqual(b"BDKHALID", data[destination:destination + 8].upper())
        # Fixture-only simulation of a prior mod replacing the initial handoff.
        data[destination:destination + 8] = b"CSRTEST0"
        path.write_bytes(data)
        before = game.tree()
        _, transcript = game.install()
        self.assertIn("NOT INSTALLED DUE TO ERRORS", transcript)
        self.assert_untouched_failure(game, before, transcript)

    def test_changed_arrival_staging_fails_before_any_patch_is_written(self):
        game = self.game()
        path = game.root / "override/bdcut24.bcs"
        original = path.read_bytes()
        self.assertIn(b"1460 1025", original)
        path.write_bytes(original.replace(b"1460 1025", b"1460 1024", 1))
        before = game.tree()
        _, transcript = game.install()
        self.assertIn("first-arrival Khalid staging actions", transcript)
        self.assertIn("NOT INSTALLED DUE TO ERRORS", transcript)
        self.assert_untouched_failure(game, before, transcript)

    def test_private_scene_actor_collision_is_not_overwritten(self):
        game = self.game()
        (game.root / "override/csr115ad.cre").write_bytes(b"another mod owns this name")
        before = game.tree()
        _, transcript = game.install()
        self.assertIn("private resource CSR115AD.CRE already exists", transcript)
        self.assert_untouched_failure(game, before, transcript)

    def test_personal_quest_progression_items_timers_and_rewards_remain_intact(self):
        game = self.installed_game()
        after = game.tree()
        for resource, indices in (
            ("khalij.dlg", range(233, 258)),
            ("bdjaheir.dlg", (48, 49)),
        ):
            before_states = dialog_states(game.before[resource])
            after_states = dialog_states(after[resource])
            for index in indices:
                with self.subTest(resource=resource, state=index):
                    self.assertEqual(before_states[index].trigger, after_states[index].trigger)
                    if resource == "khalij.dlg" and index == 234:
                        self.assertEqual(before_states[index].transitions,
                                         ordinary_transitions(after_states[index]))
                        self.assertEqual(6, len(after_states[index].transitions))
                    else:
                        self.assertEqual(before_states[index].transitions,
                                         after_states[index].transitions)
        # Positive anchors keep a shifted/irrelevant fixture from proving nothing.
        khalid = dialog_states(after["khalij.dlg"])
        self.assertIn('takepartyitem("bdsilk01")', khalid[242].transitions[0].action)
        self.assertIn('setglobaltimer("bd_sdd223_end_timer","global",six_hours)',
                      khalid[255].transitions[0].action)
        # EET merge offsets differ between the September 10 and Combined games.
        # This entire party dialogue is untouched; bind its reward by the native
        # SoD speech instead of accidentally inspecting an unrelated state.
        self.assertEqual(game.before["jaheiraj.dlg"], after["jaheiraj.dlg"])
        gift_text = dialog_states(game.before["bdjaheir.dlg"])[49].text
        rewards = [state for state in dialog_states(after["jaheiraj.dlg"])
                   if state.text == gift_text]
        self.assertEqual(1, len(rewards))
        reward = rewards[0].transitions[0].action
        self.assertIn('giveitemcreate("bdamul12",myself,1,0,0)', reward)
        self.assertIn("addexperienceparty(3000)", reward)

    def test_existing_fort_quest_actions_and_normal_branch_routes_are_preserved(self):
        game = self.installed_game()
        after = game.tree()
        for resource in ("bdkhalid.dlg", "bdbfort.dlg"):
            before_states = dialog_states(game.before[resource])
            after_states = dialog_states(after[resource])
            self.assertGreaterEqual(len(after_states), len(before_states))
            for index, original in enumerate(before_states):
                with self.subTest(resource=resource, state=index):
                    self.assertEqual(original.transitions, ordinary_transitions(after_states[index]))
                    self.assertEqual(original.text, after_states[index].text)
        khalid = dialog_states(after["bdkhalid.dlg"])
        self.assertEqual(9, len(khalid[70].transitions))
        self.assertIn('setglobal("bd_bridgefort_plot","global",30)',
                      khalid[57].transitions[0].action)
        self.assertIn('setglobal("bd_bridgefort_plot","global",6)',
                      khalid[65].transitions[0].action)

    def test_carried_route_cannot_spawn_escape_or_rewire_a_second_khalid_at_stakeout(self):
        game = self.installed_game()
        resources = ("cs115sca.bcs", "cs115scb.bcs", "cs115scc.bcs")
        decompiled = game.decompile(*resources)
        for name, source in decompiled.items():
            with self.subTest(resource=name):
                blocks = baf_blocks(source)
                carried = [(trigger, action) for trigger, action in blocks
                           if trigger.startswith('global("csr_kh_fort","global",1)')]
                self.assertEqual(1, len(carried), source)
                trigger, action = carried[0]
                self.assertIn('setglobal("bd_205_stakeout","global",4)', action)
                next_scene = "bdc205da" if name == "cs115sca.bcs" else "bdc205db"
                self.assertIn(f'startcutsceneex("{next_scene}",false)', action)
                for forbidden in ("createcreature(", "escapearea(", "setdialogue("):
                    self.assertNotIn(forbidden, action)
                original = [(t, a) for t, a in blocks if '"khalid"' in a]
                self.assertEqual(1, len(original), source)
                self.assertIn('!global("csr_kh_fort","global",1)', original[0][0])

    def test_arrival_preserves_party_transfer_and_award_without_moving_carried_khalid(self):
        game = self.installed_game()
        blocks = baf_blocks(game.decompile("bdcut24.bcs")["bdcut24.bcs"])
        carried = [(trigger, action) for trigger, action in blocks
                   if trigger.startswith('global("csr_kh_fort","global",1)')]
        self.assertEqual(1, len(carried))
        trigger, action = carried[0]
        self.assertIn('global("bd_bridgefort_plot","global",0)', trigger)
        self.assertNotIn('moveglobal("bd2100","khalid"', action)
        self.assertEqual(6, action.count("addxpobject("))
        self.assertEqual(6, action.count('leavearealua("bd2100","",'))
        self.assertIn('actionoverride("bdbfort",startdialognoset(player1))', action)
        original = [(t, a) for t, a in blocks if 'moveglobal("bd2100","khalid"' in a]
        self.assertEqual(1, len(original))
        self.assertIn('!global("csr_kh_fort","global",1)', original[0][0])

    def test_existing_soldier_remains_a_quest_contact_if_khalid_dies_or_is_dismissed(self):
        game = self.installed_game()
        states = dialog_states(game.tree()["bdbfort.dlg"])
        original_count = len(dialog_states(game.before["bdbfort.dlg"]))
        additions = states[original_count:]
        entries = [state for state in additions if state.trigger]
        self.assertEqual(3, len(entries))
        for state in entries:
            self.assertIn('global("csr_kh_fort","global",1)', state.trigger)
            self.assertNotIn("khalid", state.trigger)
            self.assertNotIn("inparty", state.trigger)
        # Intro, report and command menu stay independently selectable; replying
        # to the briefing optionally involves the actual party Khalid.
        self.assertTrue(any('globallt("bd_bridgefort_plot","global",5)' in s.trigger
                            for s in entries))
        self.assertTrue(any('global("bd_bf_action_plan","global",0)' in s.trigger
                            for s in entries))
        self.assertTrue(any('globalgt("bd_bf_action_plan","global",0)' in s.trigger
                            for s in entries))
        actions = [transition.action for state in additions for transition in state.transitions]
        self.assertTrue(any('setglobal("bd_bridgefort_plot","global",30)' in a for a in actions))
        self.assertTrue(any('setglobal("bd_bridgefort_plot","global",6)' in a for a in actions))
        self.assertFalse(any("joinparty(" in a or "leaveparty(" in a for a in actions))
        departure = next(a for a in actions if 'setglobal("csr115_briefed","global",1)' in a)
        self.assertIn("makeglobaloverride()", departure)
        self.assertIn('escapeareamove("bd2000",2900,1310,e)', departure)
        optional = [transition for state in additions for transition in state.transitions
                    if "isvalidforpartydialogue" in transition.trigger]
        self.assertEqual(2, len(optional))
        present = next(t for t in optional if not t.trigger.startswith("!"))
        absent = next(t for t in optional if t.trigger.startswith("!"))
        self.assertEqual("khalij", present.destination)
        self.assertEqual("bdbfort", absent.destination)
        interjection = dialog_states(game.tree()["khalij.dlg"])[present.state]
        self.assertEqual("bdbfort", interjection.transitions[0].destination)
        self.assertEqual(absent.state, interjection.transitions[0].state)

    def test_latched_route_and_reunion_guards_cover_dead_party_members(self):
        game = self.installed_game()
        sources = game.decompile("bd2000.bcs", "bd2100.bcs", "bdkhalid.bcs")
        for resource in ("bd2000.bcs", "bd2100.bcs"):
            blocks = baf_blocks(sources[resource])
            carried = [(t, a) for t, a in blocks
                       if 'setglobal("csr_kh_fort","global",1)' in a]
            ordinary = [(t, a) for t, a in blocks
                        if 'setglobal("csr_kh_fort","global",2)' in a]
            self.assertEqual(1, len(carried), resource)
            self.assertEqual(2, len(ordinary), resource)
            self.assertIn('global("csr_kh_fort","global",0)', carried[0][0])
            self.assertIn('inpartyallowdead("khalid")', carried[0][0])
            self.assertIn('globallt("bd_bridgefort_plot","global",5)', carried[0][0])
            self.assertIn('!inpartyallowdead("khalid")', ordinary[0][0])
            for slot in range(1, 7):
                self.assertIn(f'name("khalid",player{slot})', carried[0][0])
                self.assertIn(f'!name("khalid",player{slot})', ordinary[0][0])
                self.assertIn(f'or(2)numinpartylt({slot})inmyarea(player{slot})', ordinary[0][0])
            self.assertIn('globalgt("bd_bridgefort_plot","global",4)', ordinary[1][0])
            self.assertIn('setglobal("bd_khal_spawn","bd2000",1)', carried[0][1])
            self.assertLess(blocks.index(carried[0]), blocks.index(ordinary[0]))
        reunion = [(t, a) for t, a in baf_blocks(sources["bdkhalid.bcs"])
                   if re.search(r'global\("bd_mdd206","global",[01]\)', t)]
        self.assertEqual(2, len(reunion))
        for trigger, _ in reunion:
            self.assertIn('!global("csr_kh_carry","global",1)', trigger)
            self.assertIn('!global("csr_kh_fort","global",1)', trigger)

    def test_native_recruitment_cannot_reset_any_occupied_khalid_party_slot(self):
        """Evaluate compiled guards with the named lookup missing during arrival.

        This is a trigger-logic regression, not a claim about engine lookup timing.
        """
        game = self.installed_game()
        blocks = baf_blocks(game.decompile("bd2000.bcs")["bd2000.bcs"])
        recruiters = [(t, a) for t, a in blocks if
                      'moveglobal("bd2000","khalid",[2900.1310])' in a or
                      'createcreature("khalid7",[2900.1310],e)' in a]
        self.assertEqual(2, len(recruiters))
        for trigger, action in recruiters:
            self.assertIn('global("csr_kh_fort","global",2)', trigger)
            self.assertIn('!inpartyallowdead("khalid")', trigger)
            for slot in range(1, 7):
                self.assertIn(f'!name("khalid",player{slot})', trigger)
                self.assertIn(f'or(2)numinpartylt({slot})inmyarea(player{slot})', trigger)
            # The ordinary quest still has its original actions, behind the guards.
            self.assertIn('changeaiscript("bdfort",class)', action)

        fresh_fallback = next(t for t, a in blocks if
                              'setglobal("csr_kh_fort","global",2)' in a and
                              'globallt("bd_bridgefort_plot","global",5)' in t)
        # A missing actor cannot count as an empty party slot during transfer.
        self.assertNotIn('exists(', fresh_fallback)
        self.assertNotIn('csr_kh_carry', fresh_fallback)
        carried = next(t for t, a in blocks if 'setglobal("csr_kh_fort","global",1)' in a)
        for slot in range(1, 7):
            with self.subTest(khalid_party_slot=slot):
                self.assertTrue(entry_guard_holds(carried, khalid_slot=slot))
                self.assertFalse(entry_guard_holds(fresh_fallback, khalid_slot=slot))
                for trigger, _ in recruiters:
                    self.assertFalse(entry_guard_holds(trigger, khalid_slot=slot, route=2))
        # Even if both actor lookup paths miss, party size must keep the fresh
        # route unresolved until every occupied slot has completed the transfer.
        self.assertFalse(entry_guard_holds(fresh_fallback, arrived=range(1, 6)))
        self.assertTrue(entry_guard_holds(fresh_fallback))
        self.assertTrue(entry_guard_holds(recruiters[0][0], route=2))
        self.assertTrue(entry_guard_holds(recruiters[1][0], route=2, been_in_party=False))
        self.assertTrue(all(not entry_guard_holds(t) for t, _ in recruiters))

    def test_voghiln_does_not_start_hostile_jaheira_intro_for_a_carried_companion(self):
        game = self.installed_game()
        source = game.decompile("bdvoghil.bcs")["bdvoghil.bcs"]
        launchers = [(trigger, action) for trigger, action in baf_blocks(source)
                     if 'global("bd_jaheira_join","global",0)' in trigger and
                     'startdialognoset(player1)' in action]
        self.assertEqual(1, len(launchers))
        for guard in ('!inpartyallowdead("jaheira")', '!global("csr_jh_carry","global",1)'):
            self.assertIn(guard, launchers[0][0])
        original = dialog_states(game.before["bdvoghil.dlg"])
        installed = dialog_states(game.tree()["bdvoghil.dlg"])
        self.assertEqual(len(original), len(installed))
        for index, state in enumerate(original):
            if index != 9:
                self.assertEqual(state, installed[index], f"BDVOGHIL state {index}")
        self.assertEqual(original[9].transitions, installed[9].transitions)
        self.assertEqual(original[9].text, installed[9].text)
        for guard in ('!inpartyallowdead("jaheira")', '!global("csr_jh_carry","global",1)'):
            self.assertIn(guard, installed[9].trigger)
        # Independent recruitment remains usable; only the incompatible joint
        # introduction is gated. All recruitment dialogue mechanics above are exact.
        for index in (18, 35, 67, 68, 99):
            self.assertNotIn("csr_jh_carry", installed[index].trigger)
            self.assertNotIn("inpartyallowdead", installed[index].trigger)
        self.assertIn("joinparty()", installed[19].transitions[0].action)

    def test_jaheira_carried_reply_does_not_claim_she_arrived_without_khalid(self):
        game = self.installed_game()
        original = dialog_states(game.before["bdjaheir.dlg"])[25]
        installed = dialog_states(game.tree()["bdjaheir.dlg"])[25]
        self.assertEqual(original.transitions, ordinary_transitions(installed))
        self.assertEqual(4, len(installed.transitions))
        tlk = (game.root / "lang/en_us/dialog.tlk").read_bytes()
        changed = [t for t in installed.transitions if
                   tlk_text(tlk, t.text) == "What brings you this far north?"]
        self.assertEqual(1, len(changed))
        self.assertIn('global("csr_kh_carry","global",1)', changed[0].trigger)
        self.assertIn('global("csr_kh_fort","global",1)', changed[0].trigger)
        self.assertEqual(original.transitions[1].action, changed[0].action)
        self.assertEqual("How did you come to be here without Khalid?",
                         tlk_text(tlk, original.transitions[1].text))

    def test_smithy_cameo_uses_a_private_actor_and_preserves_its_original_scene(self):
        game = self.installed_game()
        names = tuple(f"cs115sa{letter}.bcs" for letter in "abcde")
        for resource, source in game.decompile(*names).items():
            blocks = baf_blocks(source)
            carried = [(t, a) for t, a in blocks
                       if t.startswith('global("csr_kh_fort","global",1)')]
            self.assertEqual(1, len(carried), resource)
            self.assertIn('"csr115ad"', carried[0][1])
            self.assertNotIn('"bdbfort"', carried[0][1])
            original = [(t, a) for t, a in blocks if '"bdbfort"' in a]
            self.assertEqual(1, len(original), resource)
            self.assertIn('!global("csr_kh_fort","global",1)', original[0][0])
        after = game.tree()
        old_cre = bytearray(game.before["bdbfort.cre"])
        new_cre = after["csr115ad.cre"]
        for offset, width in ((8, 8), (0x280, 32), (0x2CC, 8)):
            old_cre[offset:offset + width] = new_cre[offset:offset + width]
        self.assertEqual(bytes(old_cre), new_cre)
        self.assertEqual(b"csr115ad", new_cre[0x280:0x2A0].rstrip(b"\0").lower())
        cameo = dialog_states(after["csr115ad.dlg"])
        self.assertEqual(2, len(cameo))
        self.assertEqual(dialog_states(game.before["bdbfort.dlg"])[:2], cameo)

    def test_stakeout_wrappers_explicitly_evaluate_conditional_payloads(self):
        game = self.installed_game()
        names = tuple(f"bdc205{suffix}.bcs" for suffix in
                      ("aa", "ab", "ac", "ad", "ae", "ca", "cb", "cc"))
        for resource, source in game.decompile(*names).items():
            blocks = baf_blocks(source)
            self.assertEqual(1, len(blocks), resource)
            self.assertEqual("true()", blocks[0][0], resource)
            payload = "cs115s" + Path(resource).stem[-2:]
            self.assertIn(f'startcutsceneex("{payload}",true)', blocks[0][1])
            self.assertNotIn('"khalid"', blocks[0][1])
            self.assertNotIn('"bdbfort"', blocks[0][1])

    def test_public_install_writes_only_audited_resources_and_keeps_protected_game_data(self):
        game = self.installed_game()
        after = game.tree()
        expected = {
            "bd0103.bcs", "bd1000.bcs", "bd7100.bcs", "bd2000.bcs", "bd2100.bcs",
            "bdcut24.bcs", "bdkhalid.bcs", "bdban037.bcs", "bdban103.bcs",
            "bdbarghe.dlg", "bdbfort.dlg", "bdjaheir.dlg", "bdjegg.dlg", "bdkhalid.dlg",
            "bdneera.dlg", "bdwynan.dlg", "bdvoghil.dlg", "bdvoghil.bcs", "khalij.dlg",
            "csr115ad.cre", "csr115ad.dlg",
            *(f"bdc205{suffix}.bcs" for suffix in ("aa", "ab", "ac", "ad", "ae", "ca", "cb", "cc")),
            *(f"cs115s{suffix}.bcs" for suffix in ("aa", "ab", "ac", "ad", "ae", "ca", "cb", "cc")),
        }
        self.assertEqual(expected, {name for name, data in after.items()
                                    if data != game.before.get(name)})
        self.assertFalse(set(game.before) - set(after), "installer removed an original resource")
        for name, payload in game.protected_before.items():
            self.assertEqual(payload, (game.root / name).read_bytes(), name)
        for name in ("k#telbgt.bcs", "ar0602.bcs", "campaign.2da", "startare.2da",
                     "bd2100.are", "bd2000.are", "cutskip.bcs", "bdbfort.cre",
                     "bddialog.2da", "pdialog.2da"):
            self.assertEqual(game.before[name], after[name], name)

    def test_surrender_and_resolution_leave_party_khalid_control_unchanged(self):
        game = self.installed_game()
        blocks = baf_blocks(game.decompile("bd2000.bcs")["bd2000.bcs"])
        carried = [(t, a) for t, a in blocks
                   if t.startswith('global("csr_kh_fort","global",1)')]
        resolution = [(t, a) for t, a in carried if 'setglobal("bd_plot","global",293)' in a]
        installed_bridge = any('setglobal("csr256_stage","bd2000",3)' in a for _, a in blocks)
        self.assertEqual(1 if installed_bridge else 2, len(resolution))
        for _, action in resolution:
            self.assertNotIn('"khalid"', action)
            self.assertIn('createcreatureobject("bdbence",player1,6,0,0)' if installed_bridge else
                          'createcreature("bdbence",[2425.2660],nw)', action)
        surrender = [(t, a) for t, a in carried
                     if 'global("bd_bridgefort_plot","global",6)' in t]
        self.assertEqual(1, len(surrender))
        self.assertNotIn('"khalid"', surrender[0][1])
        self.assertIn('actionoverride("bdbarghe",startdialognoset(player1))', surrender[0][1])
        commands = [(t, a) for t, a in carried if 'displaystringhead("bdbfort",' in a]
        self.assertEqual(3, len(commands))
        self.assertTrue(all('"khalid"' not in a for _, a in commands))


if __name__ == "__main__":
    unittest.main()
