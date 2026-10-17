"""Public-installer checks for 292-294 (Imoen in Shadows of Amn) in a synthetic EET.

These prove install-time behaviour only: which resources change, the generated
script order and contents, adaptation to other mods' data, and refusals. The
in-game behaviour is verified separately in disposable lab installs.
"""
import re
import struct
import subprocess
import unittest

from test_bdscry_compat import WEIDU
from test_optional_sod_skip_installer import SkipGame
import test_optional_sod_skip as probe


TP2 = "chriz-sod-remix/setup-chriz-sod-remix.tp2"
ABILITY_OFFSETS = {"STR": 0x238, "INT": 0x23A, "WIS": 0x23B,
                   "DEX": 0x23C, "CON": 0x23D, "CHR": 0x23E}
BG1_SCORES = {"STR": 9, "INT": 17, "WIS": 11, "DEX": 18, "CON": 16, "CHR": 16}
PROTECTED = ("k#telbgt.bcs", "k#telbgt.cre", "ar0602.bcs", "bd4300.are",
             "bd6100.are", "bd0103.are", "campaign.2da", "startare.2da",
             "imoen2.cre", "imoen10.cre", "imoenhp1.itm", "k#import.sto")

EXTRA_ACTIONS = """0 NoAction()
1 ActionOverride(O:Actor*,A:Action*)
21 LeaveParty()
82 CreateItem(S:ResRef*,I:Usage1*,I:Usage2*,I:Usage3*)
139 JoinParty()
83 SmallWait(I:Time*)
133 ClearActions(O:Object*)
160 ApplySpellRES(S:RES*,O:Target)
197 MoveGlobal(S:Area*,O:Object*,P:Point*)
258 FillSlot(I:Slot*SLOTS)
262 DisplayStringNoName(O:Object*,I:StrRef*)
291 MoveGlobalObject(O:Object*,O:Target*)
370 ChangeStat(O:Object*,I:Stat*Stats,I:Value*,I:Modifier*StatMod)
383 MakeGlobalOverride()
"""
EXTRA_TRIGGERS = """0x4037 StateCheck(O:Object*,I:State*State)
0x4043 InParty(O:Object*)
0x4044 CheckStat(O:Object*,I:Value*,I:StatNum*Stats)
0x40DF BeenInParty(S:Name*)
"""
NEXT_TRIGGER_OBJECT = "0x40E0 NextTriggerObject(O:Object*)\n"
EXTRA_IDS = {
    "state.ids": "IDS V1.0\n0x00000FC0 STATE_REALLY_DEAD\n",
    "stats.ids": "IDS V1.0\n34 LEVEL\n36 STR\n38 INT\n39 WIS\n40 DEX\n41 CON\n42 CHR\n44 XP\n",
    "statmod.ids": "IDS V1.0\n1 ADD\n2 SET\n",
    "slots.ids": "IDS V1.0\n2 SLOT_BELT\n",
}

GUARD = """IF
  OR(2)
    !AreaCheck("BD4300")
    !Exists("K#ImportContainer")
THEN
  RESPONSE #100
    DisplayStringNoName(Player1,329569)
    FadeFromColor([1.0],0)
{lite}    EndCutSceneMode()
    SetGlobal("CSR_ENDING_FAILED","GLOBAL",1)
    DestroySelf()
END
"""


def import_rule(item, extra=""):
    return f"""IF
  Global("K#FrameDelay","LOCALS",0)
  PartyHasItem("{item}")
  {extra}
THEN
  RESPONSE #100
    TakePartyItem("{item}")
    DestroyItem("{item}")
    AddStoreItem("K#IMPORT","{item}",1,1)
    Continue()
END
"""


def creature(scores, spells=(), script_name="Imoen2", flags=0):
    """CRE V1.0 with the given ability scores, known wizard spells, script name
    (death variable) and creature flags."""
    known = 0x2D4
    tail = known + len(spells) * 12
    data = bytearray(tail)
    data[:8] = b"CRE V1.0"
    struct.pack_into("<i", data, 0x08, -1)
    struct.pack_into("<I", data, 0x10, flags)
    data[0x280:0x2A0] = script_name.encode().ljust(32, bytes(1))
    for name, value in scores.items():
        data[ABILITY_OFFSETS[name]] = value
    struct.pack_into("<II", data, 0x2A0, known, len(spells))
    for pos in (0x2A8, 0x2B0):
        struct.pack_into("<II", data, pos, tail, 0)
    struct.pack_into("<III", data, 0x2B8, tail, tail, 0)
    struct.pack_into("<II", data, 0x2C4, tail, 0)
    for index, (resref, level) in enumerate(spells):
        pos = known + index * 12
        data[pos:pos + 8] = resref.encode().ljust(8, b"\0")
        struct.pack_into("<HH", data, pos + 8, level - 1, 1)
    return bytes(data)


# Component 160's dialog for Imoen in SoD, as BDDIALOG.2DA's POST_DIALOG_FILE: one
# transition-only state (stay) between three triggered ones.
def post_dialog_source(name):
    return f"""BEGIN {name}
IF ~Global("CSR_IMOEN_JOINED","GLOBAL",0)~ THEN BEGIN greet
  SAY ~Heya!~
  IF ~~ THEN REPLY ~Together again.~ DO ~SetGlobal("CSR_IMOEN_JOINED","GLOBAL",1) JoinParty()~ EXIT
  IF ~~ THEN REPLY ~Not yet.~ GOTO stay
END
IF ~~ THEN BEGIN stay
  SAY ~Fiiine.~
  IF ~~ THEN EXIT
END
IF ~Global("CSR_IMOEN_JOINED","GLOBAL",1) !InParty(Myself)~ THEN BEGIN rejoin
  SAY ~Done leavin' me behind?~
  IF ~~ THEN REPLY ~Come on, then - rejoin the party.~ DO ~JoinParty()~ EXIT
  IF ~~ THEN REPLY ~Not just yet.~ EXIT
END
IF ~Global("CSR_IMOEN_JOINED","GLOBAL",1) InParty(Myself)~ THEN BEGIN chat
  SAY ~Quit pokin' me.~
  IF ~~ THEN EXIT
END
"""


def dlg_state_triggers(data):
    """{state number: whitespace-normalized trigger, or None} of a DLG V1.0 file."""
    count, table = struct.unpack_from("<II", data, 0x08)
    triggers = struct.unpack_from("<I", data, 0x18)[0]
    out = {}
    for state in range(count):
        index = struct.unpack_from("<i", data, table + state * 16 + 12)[0]
        if index < 0:
            out[state] = None
        else:
            offset, length = struct.unpack_from("<II", data, triggers + index * 8)
            out[state] = " ".join(data[offset:offset + length].decode("latin-1").split())
    return out


CLOSED = 'OR(2) GlobalLT("CSR_IMSOA_PREP","GLOBAL",1) GlobalGT("CSR_IMSOA_PREP","GLOBAL",8)'


# Real games have no TAKEITM.IDS (0 decompiles as 0); the 910 fixture maps 0 to ALL.
TAKE_ALL = r'TakeCreatureItems\("IMOEN2",(?:0|ALL)\)'


def baf_blocks(text):
    return [(m.group("t"), m.group("a")) for m in re.finditer(
        r"(?ms)^IF\s*$\s*(?P<t>.*?)^THEN\s*$\s*(?P<a>.*?)^END\s*$", text)]


class ImoenGame(SkipGame):
    def __init__(self, *, guard="current", ending_rules=("MISC47", "SW1H16"),
                 odd_ending_rule=False, bank=True, arrival_marker=True,
                 fresh_imoen10=True, imoen2=None, imoen10=None,
                 imoen10_spells=(("SPWI112", 1), ("SPWI203", 2), ("SPWI304", 3),
                                 ("CSRGONE1", 2)),
                 eeex=True, next_trigger_object=True, missing_remix=None,
                 post_dialog="CSRIMOEN", dialogs=("csrimoen",),
                 imoen10_script_name="Imoen2", imoen10_flags=0):
        super().__init__(missing_dependency=missing_remix if missing_remix in (110, 140, 150, 160) else None)
        override = self.root / "override"
        actions = (override / "action.ids").read_text()
        if eeex:
            actions += "472 EEex_LuaAction(S:Chunk*)\n"
            (override / "M___EEex.lua").write_text("-- synthetic EEex marker\n")
        (override / "action.ids").write_text(actions + EXTRA_ACTIONS, encoding="ascii")
        triggers = (override / "trigger.ids").read_text()
        if next_trigger_object:
            triggers += NEXT_TRIGGER_OBJECT
        (override / "trigger.ids").write_text(triggers + EXTRA_TRIGGERS, encoding="ascii")
        for name, text in EXTRA_IDS.items():
            (override / name).write_text(text, encoding="ascii")
        (override / "imoen2.cre").write_bytes(creature(imoen2 or BG1_SCORES))
        (override / "imoen10.cre").write_bytes(
            creature(imoen10 or BG1_SCORES, imoen10_spells, imoen10_script_name, imoen10_flags))
        for name in ("imoenhp1.itm", "spwi112.spl", "spwi203.spl", "spwi304.spl"):
            header = b"ITM V1  " if name.endswith(".itm") else b"SPL V1  "
            (override / name).write_bytes(header + bytes(0x6A))
        (override / "bd4300.are").write_bytes(probe.GroundProbeVerifierTests.area(
            [("K#ImportContainer", 2, [])] if bank else [("Unrelated", 2, [])]))

        fixture = self.root / "fixture292"
        fixture.mkdir()
        for name in dialogs:
            (fixture / f"{name}.d").write_text(post_dialog_source(name), encoding="ascii")
        if post_dialog is not None:
            (override / "bddialog.2da").write_text(
                "2DA V1.0\n*\n         POST_DIALOG_FILE JOIN_DIALOG_FILE DREAM_SCRIPT_FILE\n"
                "KHALID   BDKHALIP         BDKHALIJ         BDKHALID\n"
                f"IMOEN2   {post_dialog:<16} {post_dialog:<16} BDIMOEN\n", encoding="ascii")
        lite = "    SetCutSceneLite(FALSE)\n" if guard == "current" else ""
        rules = "".join(import_rule(item) for item in ending_rules)
        if odd_ending_rule:
            rules += import_rule("CSRODD", 'Global("OtherMod","GLOBAL",1)')
        tail = """IF
  Global("K#FrameDelay","LOCALS",0)
THEN
  RESPONSE #100
    SetGlobal("K#FrameDelay","LOCALS",1)
END
IF
  True()
THEN
  RESPONSE #100
    GivePartyAllEquipment()
    MoveContainerContents("BD4300*K#ImportContainer","BD6100*K#ImportContainer")
    DestroySelf()
END
"""
        body = GUARD.format(lite=lite) + rules + tail
        if guard == "late":
            body = rules + GUARD.format(lite=lite) + tail
        (fixture / "csretbgt.baf").write_text(body)
        marker = 'SetGlobal("K#ImoenImport","AR0602",1)' if arrival_marker else ""
        fresh = 'CreateCreature("Imoen10",[3198.2837],S)' if fresh_imoen10 else "NoAction()"
        (fixture / "ar0602.baf").write_text(f"""IF
  Global("K#ImoenImport","AR0602",0)
  BeenInParty("Imoen2")
  !StateCheck("Imoen2",STATE_REALLY_DEAD)
THEN
  RESPONSE #100
    MoveGlobal("AR0602","Imoen2",[3198.2837])
    ActionOverride("Imoen2",CreateItem("IMOENHP1",1,0,0))
    ActionOverride("Imoen2",FillSlot(SLOT_BELT))
    {marker}
    Continue()
END
IF
  Global("K#ImoenImport","AR0602",0)
  !BeenInParty("Imoen2")
THEN
  RESPONSE #100
    {fresh}
    {marker}
    Continue()
END
""")
        setup = self.root / "setup-imoen-bootstrap.tp2"
        setup.write_text("BACKUP ~weidu_external/backup/imoen-bootstrap~\nAUTHOR ~test~\n"
                         "BEGIN ~fixture292~\nCOMPILE ~fixture292~\n")
        result = self._run(setup)
        if "SUCCESSFULLY INSTALLED" not in self.transcript(result):
            raise AssertionError(self.transcript(result))
        log = self._find_output(self.root, "weidu.log")
        if missing_remix != 290:
            log.write_text(log.read_text() +
                           "~CHRIZ-SOD-REMIX/SETUP-CHRIZ-SOD-REMIX.TP2~ #0 #290 // synthetic prerequisite\n")
        self.before = self.tree()
        self.tlk_before = (self.root / "lang/en_us/dialog.tlk").read_bytes()

    def install_component(self, number):
        result = subprocess.run([
            str(WEIDU), TP2, "--force-install-list", str(number), "--language", "0",
            "--use-lang", "en_us", "--no-exit-pause", "--noautoupdate", "--quick-log",
        ], cwd=self.root, capture_output=True, text=True, timeout=120)
        return result, self.transcript(result)

    def changed(self):
        after = self.tree()
        return {name for name in after if after[name] != self.before.get(name)}


@unittest.skipUnless(WEIDU.is_file(), f"WeiDU unavailable: {WEIDU}")
class ImoenSoAInstallerTests(unittest.TestCase):
    def game(self, **kwargs):
        game = ImoenGame(**kwargs)
        self.addCleanup(game.cleanup)
        return game

    def installed(self, number, **kwargs):
        game = self.game(**kwargs)
        result, text = game.install_component(number)
        self.assertEqual(0, result.returncode, text)
        self.assertIn("SUCCESSFULLY INSTALLED", text)
        return game

    def prep_blocks(self, game, name="csretbgt"):
        return baf_blocks(game.baf(name))

    # ---- what each choice writes --------------------------------------------

    def test_each_choice_changes_only_its_owned_resources(self):
        expected = {
            292: {"csretbgt.bcs", "baldur.bcs", "csrimstr.spl", "csrimoen.dlg"},
            293: {"csretbgt.bcs", "baldur.bcs", "csrimoen.dlg"},
            294: {"csretbgt.bcs", "baldur.bcs", "m_csrimd.lua", "csrimoen.dlg"},
        }
        for number, owned in expected.items():
            with self.subTest(component=number):
                game = self.installed(number)
                self.assertEqual(owned, game.changed())
                after = game.tree()
                for name in PROTECTED:
                    self.assertEqual(game.before[name], after[name], name)

    def test_ending_preparation_follows_the_guard_and_holds_the_transition(self):
        game = self.installed(292)
        blocks = self.prep_blocks(game)
        self.assertIn('!AreaCheck("BD4300")', blocks[0][0])
        self.assertIn('Global("CSR_IMSOA_PREP","GLOBAL",0)', blocks[1][0])
        prep = [i for i, (t, _) in enumerate(blocks) if "CSR_IMSOA_PREP" in t]
        self.assertEqual(list(range(1, 1 + len(prep))), prep)
        for trigger, _ in blocks[1:1 + len(prep)]:
            self.assertIn('Global("K#FrameDelay","LOCALS",0)', trigger)
        wait_trigger, wait_action = blocks[prep[-1]]
        self.assertIn('!Global("CSR_IMSOA_PREP","GLOBAL",9)', wait_trigger)
        self.assertEqual("NoAction()", wait_action.split("RESPONSE #100", 1)[1].strip())
        first_rule = next(i for i, (_, a) in enumerate(blocks) if "TakePartyItem(" in a)
        self.assertGreater(first_rule, prep[-1])

    def test_old_guard_without_lite_release_is_supported(self):
        game = self.installed(293, guard="old")
        blocks = self.prep_blocks(game)
        self.assertIn('!AreaCheck("BD4300")', blocks[0][0])
        self.assertIn("CSR_IMSOA_PREP", blocks[1][0])

    def test_imoen_leaves_party_moves_here_and_is_banked_after_import_skims(self):
        game = self.installed(293)
        blocks = self.prep_blocks(game)
        leave_trigger, leave = next((t, a) for t, a in blocks if "LeaveParty()" in a)
        self.assertIn('InPartyAllowDead("IMOEN2")', leave_trigger)
        self.assertNotIn("!InPartyAllowDead", leave_trigger)
        self.assertEqual('ActionOverride("IMOEN2",LeaveParty())',
                         leave.split("RESPONSE #100", 1)[1].strip())
        move = next(a for t, a in blocks if "MoveGlobalObject" in a)
        self.assertIn('MoveGlobalObject("IMOEN2",Myself)', move)
        skims = [(t, a) for t, a in blocks if "AddStoreItem(" in a and "CSR_IMSOA_PREP" in t]
        self.assertEqual({"MISC47", "SW1H16"},
                         {re.search(r'HasItem\("([^"]+)","IMOEN2"\)', t).group(1) for t, _ in skims})
        for trigger, action in skims:
            item = re.search(r'HasItem\("([^"]+)"', trigger).group(1)
            self.assertIn(f'!PartyHasItem("{item}")', trigger)
            self.assertIn(f'AddStoreItem("K#IMPORT","{item}",1,1)', action)
            # Her copy is destroyed like the party's, so it is not banked too.
            destroy = f'ActionOverride("IMOEN2",DestroyItem("{item}"))'
            self.assertIn(destroy, action)
            self.assertLess(action.index("AddStoreItem("), action.index(destroy))
            self.assertNotIn("TakePartyItem", action)
        bank_index = next(i for i, (_, a) in enumerate(blocks) if re.search(TAKE_ALL, a))
        self.assertRegex(blocks[bank_index][1], r'ActionOverride\("K#ImportContainer",' + TAKE_ALL)
        # Then she removes herself (step 4), two seconds later.
        self.assertIn('RealSetGlobalTimer("CSR_IMSOA_TIMER","GLOBAL",2)', blocks[bank_index][1])
        self.assertIn('SetGlobal("CSR_IMSOA_PREP","GLOBAL",4)', blocks[bank_index][1])
        # The bank is a later pass, after her DestroyItem actions have run.
        self.assertIn('Global("CSR_IMSOA_PREP","GLOBAL",6)', blocks[bank_index][0])
        self.assertIn('RealGlobalTimerExpired("CSR_IMSOA_TIMER","GLOBAL")', blocks[bank_index][0])
        handoff = next(i for i, (t, a) in enumerate(blocks) if 'Global("CSR_IMSOA_PREP","GLOBAL",2)' in t
                       and 'SetGlobal("CSR_IMSOA_PREP","GLOBAL",6)' in a)
        self.assertIn('RealSetGlobalTimer("CSR_IMSOA_TIMER","GLOBAL",1)', blocks[handoff][1])
        self.assertLess(max(i for i, (t, a) in enumerate(blocks) if "AddStoreItem(" in a and "CSR_IMSOA_PREP" in t),
                        handoff)
        self.assertLess(handoff, bank_index)
        self.assertTrue(all(i < bank_index for i, (t, a) in enumerate(blocks)
                            if "AddStoreItem(" in a and "CSR_IMSOA_PREP" in t))
        self.assertNotIn("CSRIMSTR", game.baf("csretbgt"))

    def test_post_party_dialog_stays_closed_only_while_she_is_handed_over(self):
        # LeaveParty() opens her post-party dialog at once (lab, 2026-10-17); its
        # rejoin offer must not be available during the preparation.
        for number in (292, 293, 294):
            with self.subTest(component=number):
                game = self.installed(number)
                before = dlg_state_triggers(game.before["csrimoen.dlg"])
                after = dlg_state_triggers(game.tree()["csrimoen.dlg"])
                self.assertEqual(set(before), set(after))
                self.assertIsNone(after[1])  # transition-only "stay" is untouched
                for state in (0, 2, 3):
                    # WeiDU puts the added condition first; all lines must hold.
                    self.assertEqual(f"{CLOSED} {before[state]}", after[state])

    def test_post_party_dialog_comes_from_the_installed_campaign_table(self):
        game = self.installed(293, post_dialog="XXIMOENP", dialogs=("csrimoen", "xximoenp"))
        self.assertEqual(game.before["csrimoen.dlg"], game.tree()["csrimoen.dlg"])
        before = dlg_state_triggers(game.before["xximoenp.dlg"])
        after = dlg_state_triggers(game.tree()["xximoenp.dlg"])
        self.assertEqual(f"{CLOSED} {before[2]}", after[2])
        for kwargs in ({"post_dialog": None}, {"post_dialog": "*"}, {"post_dialog": "XXGONE"}):
            with self.subTest(**kwargs):
                game = self.installed(293, **kwargs)
                self.assertEqual({"csretbgt.bcs", "baldur.bcs"}, game.changed())

    def test_a_rejoined_imoen_is_never_removed_from_the_party(self):
        game = self.installed(292)
        blocks = self.prep_blocks(game)
        back = [i for i, (t, a) in enumerate(blocks) if 'InPartyAllowDead("IMOEN2")' in t
                and "!InPartyAllowDead" not in t and 'SetGlobal("CSR_IMSOA_PREP","GLOBAL",1)' in a]
        self.assertEqual(1, len(back), back)
        trigger = blocks[back[0]][0]
        for step in (2, 6):
            self.assertIn(f'Global("CSR_IMSOA_PREP","GLOBAL",{step})', trigger)
        self.assertIn("OR(2)", trigger)
        later = [i for i, (_, a) in enumerate(blocks) if "AddStoreItem(" in a or re.search(TAKE_ALL, a)]
        self.assertTrue(later and all(back[0] < i for i in later))
        # Her removal and the stand-in's both require "IMOEN2" out of the party.
        removals = [(t, a) for t, a in blocks if 'ActionOverride("IMOEN2",DestroySelf())' in a]
        self.assertEqual(2, len(removals))
        for trigger, _ in removals:
            self.assertIn('!InPartyAllowDead("IMOEN2")', trigger)
        # Back in the party after the read: the transition hands her over like any
        # companion, so EET carries her own Imoen over; no boosts are armed.
        kept = [a for t, a in blocks if 'Global("CSR_IMSOA_PREP","GLOBAL",4)' in t
                and re.search(r'(?m)^\s*InPartyAllowDead\("IMOEN2"\)', t)]
        self.assertEqual(1, len(kept))
        self.assertIn('SetGlobal("CSR_IMSOA_FAILED","GLOBAL",5)', kept[0])
        self.assertIn('SetGlobal("CSR_IMSOA_PREP","GLOBAL",9)', kept[0])
        self.assertIn("SetInterrupt(TRUE)", kept[0])
        self.assertNotIn("CSR_IMSOA_BOOST", kept[0])
        self.assertNotIn("DestroySelf", kept[0])
        for number in (293, 294):
            with self.subTest(component=number):
                # Choices 2/3 end the same way without a stand-in: she removes
                # herself once, out of the party, and EET's AR0602 brings her back
                # like any companion (an Imoen left alive in the area lost EET's
                # SoA dialog and scripts in the lab).
                blocks = self.prep_blocks(self.installed(number))
                removals = [t for t, a in blocks if 'ActionOverride("IMOEN2",DestroySelf())' in a]
                self.assertEqual(1, len(removals))
                self.assertIn('Global("CSR_IMSOA_PREP","GLOBAL",4)', removals[0])
                self.assertIn('!InPartyAllowDead("IMOEN2")', removals[0])
                kept = [a for t, a in blocks if 'Global("CSR_IMSOA_PREP","GLOBAL",4)' in t
                        and re.search(r'(?m)^\s*InPartyAllowDead\("IMOEN2"\)', t)]
                self.assertEqual(1, len(kept))
                self.assertIn('SetGlobal("CSR_IMSOA_FAILED","GLOBAL",5)', kept[0])
                left = [a for t, a in blocks if 'Global("CSR_IMSOA_PREP","GLOBAL",5)' in t
                        and '!InMyArea("IMOEN2")' in t]
                self.assertEqual(1, len(left))
                self.assertIn('SetGlobal("CSR_IMSOA_PREP","GLOBAL",9)', left[0])
                late = [a for t, a in blocks if 'Global("CSR_IMSOA_PREP","GLOBAL",5)' in t
                        and "RealGlobalTimerExpired" in t]
                self.assertEqual(1, len(late))
                self.assertIn('ClearActions("IMOEN2")', late[0])
                self.assertIn('SetGlobal("CSR_IMSOA_PREP","GLOBAL",9)', late[0])
                text = "\n".join(a for _, a in blocks)
                for absent in ("MakeGlobalOverride", 'CreateCreatureObject("IMOEN10"', "CSR_IMSOA_BOOST"):
                    self.assertNotIn(absent, text)

    def test_imoen_is_marked_as_a_sod_party_member_before_she_leaves(self):
        # EET's IMOEN_ removes an unmarked BG1 Imoen once she is out of the
        # party after BG1; EET's own SoD epilogue marks her (BD6200).
        mark_action = 'ActionOverride("IMOEN2",SetGlobal("K#PartySoD","LOCALS",1))'

        def on_her(negated):
            # NextTriggerObject + trigger; WeiDU decompiles the pair as TriggerOverride.
            neg = "!" if negated else ""
            return (rf'(?:NextTriggerObject\("IMOEN2"\)[^\n]*\n\s*{neg}Global\("K#PartySoD","LOCALS",1\)'
                    rf'|(?<![!\w]){neg}TriggerOverride\("IMOEN2",Global\("K#PartySoD","LOCALS",1\)\))')
        verified = on_her(False)
        for number in (292, 293, 294):
            with self.subTest(component=number):
                blocks = self.prep_blocks(self.installed(number))
                p1 = [(i, t, a) for i, (t, a) in enumerate(blocks)
                      if 'Global("CSR_IMSOA_PREP","GLOBAL",1)' in t]
                mark = next(i for i, t, a in p1 if 'InMyArea("IMOEN2")' in t
                            and "!InMyArea" not in t and mark_action in a)
                self.assertRegex(blocks[mark][0], on_her(True))
                ready = next(i for i, t, a in p1 if 'SetGlobal("CSR_IMSOA_PREP","GLOBAL",2)' in a)
                leave = next(i for i, t, a in p1 if "LeaveParty()" in a)
                for index in (ready, leave):
                    self.assertLess(mark, index)
                    self.assertRegex(blocks[index][0], verified)
                    self.assertIn('InMyArea("IMOEN2")', blocks[index][0])
                fetch = next(a for i, t, a in p1 if "MoveGlobalObject" in a)
                self.assertLess(fetch.index(mark_action), fetch.index("MoveGlobalObject("))

    def test_timeout_falls_back_only_while_she_still_exists(self):
        for number in (292, 293, 294):
            with self.subTest(component=number):
                game = self.installed(number)
                blocks = self.prep_blocks(game)
                timeouts = [(t, a) for t, a in blocks if 'Global("CSR_IMSOA_PREP","GLOBAL",1)' in t
                            and "RealGlobalTimerExpired" in t]

                def where(trigger):
                    if "!BeenInParty" in trigger:
                        return "gone"
                    if "!InPartyAllowDead" in trigger:
                        self.assertIn('BeenInParty("IMOEN2")', trigger)
                        return "elsewhere"
                    self.assertIn('InPartyAllowDead("IMOEN2")', trigger)
                    return "in party"
                outcomes = {where(t): re.search(
                    r'SetGlobal\("CSR_IMSOA_FAILED","GLOBAL",(\d)\)', a).group(1) for t, a in timeouts}
                # Only an Imoen who is still out there and keeps her gear gets the
                # SoA fallback (1); in the party, the transition hands her over (5)
                # without the preparation's own LeaveParty() still queued on her.
                self.assertEqual({"in party": "5", "elsewhere": "1", "gone": "4"}, outcomes)
                in_party = next(a for t, a in timeouts if where(t) == "in party")
                self.assertIn('ClearActions("IMOEN2")', in_party)
                for _, action in timeouts:
                    self.assertIn('SetGlobal("CSR_IMSOA_PREP","GLOBAL",9)', action)
                corpse = next(i for i, (t, _) in enumerate(blocks)
                              if 'Global("CSR_IMSOA_PREP","GLOBAL",1)' in t and "StateCheck" in t)
                self.assertLess(corpse, blocks.index(timeouts[0]))
                soa = baf_blocks(game.baf("baldur"))
                for code in ("4", "5"):
                    report = next((t, a) for t, a in soa
                                  if f'Global("CSR_IMSOA_FAILED","GLOBAL",{code})' in t)
                    self.assertIn('InParty("IMOEN2")', report[0])
                    self.assertIn('SetGlobal("CSR_IMSOA_FAILED","GLOBAL",3)', report[1])
                    self.assertNotIn("TakeCreatureItems", report[1])
                    self.assertIn("DisplayStringNoName(Player1,", report[1])
                starts = [t for t, a in soa if 'Global("CSR_IMSOA_FB","GLOBAL",0)' in t]
                self.assertEqual(1, len(starts))
                self.assertIn('Global("CSR_IMSOA_FAILED","GLOBAL",1)', starts[0])

    def test_dead_or_never_recruited_imoen_is_left_to_eet(self):
        game = self.installed(292)
        blocks = self.prep_blocks(game)
        skip = blocks[1]
        self.assertRegex(skip[0], r'OR\(2\)\s+!BeenInParty\("IMOEN2"\)[^\n]*\s+'
                                  r'StateCheck\("IMOEN2",STATE_REALLY_DEAD\)')
        self.assertIn('SetGlobal("CSR_IMSOA_PREP","GLOBAL",9)', skip[1])
        corpse = next((t, a) for t, a in blocks if 'Global("CSR_IMSOA_PREP","GLOBAL",1)' in t
                      and "StateCheck" in t)
        self.assertIn('SetGlobal("CSR_IMSOA_PREP","GLOBAL",9)', corpse[1])

    # ---- choice 1 -----------------------------------------------------------

    def test_choice1_reads_boosts_against_the_installed_chassis_and_caps_at_25(self):
        bg1 = dict(BG1_SCORES, DEX=17)
        bg2 = dict(BG1_SCORES, DEX=19, STR=25)
        game = self.installed(292, imoen2=bg1, imoen10=bg2)
        prep = game.baf("csretbgt")
        reads = re.findall(r'CheckStat\("IMOEN2",(\d+),(\w+)\)', prep)
        expected = {(str(v), name) for name, ref in bg1.items() for v in range(ref + 1, 26)}
        self.assertEqual(expected, set(reads))
        self.assertIn('SetGlobal("CSR_IMSOA_DDEX","GLOBAL",8)', prep)
        baldur = game.baf("baldur")
        boosts = dict()
        for d, add in re.findall(
                r'Global\("CSR_IMSOA_DDEX","GLOBAL",(\d+)\)\s+THEN\s+RESPONSE #100\s+'
                r'ChangeStat\("IMOEN2",DEX,(\d+),ADD\)', baldur):
            boosts[int(d)] = int(add)
        self.assertEqual({d: min(d, 6) for d in range(1, 9)}, boosts)
        self.assertNotIn("ChangeStat(\"IMOEN2\",STR", baldur)  # SoA Imoen is already at 25
        self.assertLess(baldur.index("ChangeStat("),
                        baldur.index('SetGlobal("CSR_IMSOA_BOOST","GLOBAL",2)'))
        # Only an Imoen without her SoD party mark gets them (Shadows of Amn's own);
        # her own Imoen, carried over after a failed swap, gets a report instead.
        # WeiDU decompiles NextTriggerObject + trigger as TriggerOverride.
        new = (r'(?:NextTriggerObject\("IMOEN2"\)\s+!Global\("K#PartySoD","LOCALS",1\)'
               r'|!TriggerOverride\("IMOEN2",Global\("K#PartySoD","LOCALS",1\)\))')
        soa = baf_blocks(baldur)
        for trigger, action in soa:
            if "ChangeStat(" in action or 'SetGlobal("CSR_IMSOA_BOOST","GLOBAL",2)' in action:
                self.assertIn('Global("CSR_IMSOA_BOOST","GLOBAL",1)', trigger)
                self.assertIn('InParty("IMOEN2")', trigger)
                self.assertRegex(trigger, new)
        hers = [(t, a) for t, a in soa if 'SetGlobal("CSR_IMSOA_BOOST","GLOBAL",3)' in a]
        self.assertEqual(1, len(hers))
        self.assertRegex(hers[0][0], r'(?:NextTriggerObject\("IMOEN2"\)\s+Global\("K#PartySoD","LOCALS",1\)'
                                     r'|(?<![!\w])TriggerOverride\("IMOEN2",Global\("K#PartySoD","LOCALS",1\)\))')
        self.assertIn("DisplayStringNoName(Player1,", hers[0][1])
        self.assertNotIn("ChangeStat(", hers[0][1])

    def test_choice1_swaps_her_for_an_imoen10_stand_in_after_strip_and_read(self):
        game = self.installed(292)
        blocks = self.prep_blocks(game)
        actions = [a for _, a in blocks]

        def step(n):
            return [(i, t, a) for i, (t, a) in enumerate(blocks)
                    if f'Global("CSR_IMSOA_PREP","GLOBAL",{n})' in t]
        strip = next(i for i, a in enumerate(actions) if 'ApplySpellRES("CSRIMSTR","IMOEN2")' in a)
        read = next(i for i, (t, _) in enumerate(blocks) if "CheckStat(" in t)
        remove = next(i for i, t, a in step(4) if 'ActionOverride("IMOEN2",DestroySelf())' in a)
        self.assertLess(strip, read)
        self.assertLess(read, remove)
        self.assertIn('SetGlobal("CSR_IMSOA_PREP","GLOBAL",5)', actions[remove])
        # Once she has left the area, a stand-in is made from IMOEN10.CRE; nothing
        # is queued on "IMOEN2" until it is seen here, so a failed creation leaves
        # nothing behind on her (EET's AR0602 would run it when it carries her over).
        create = [(i, t, a) for i, t, a in step(5) if 'CreateCreatureObject("IMOEN10",Myself,0,0,0)' in a]
        self.assertEqual(1, len(create))
        _, trigger, action = create[0]
        self.assertIn('!InMyArea("IMOEN2")', trigger)
        self.assertNotIn("ActionOverride", action)
        self.assertIn('SetGlobal("CSR_IMSOA_PREP","GLOBAL",7)', action)
        swap = [(t, a) for _, t, a in step(7) if "MakeGlobalOverride()" in a]
        self.assertEqual(1, len(swap))
        trigger, action = swap[0]
        for need in ('Global("CSR_IMSOA_STANDIN","GLOBAL",0)', 'InMyArea("IMOEN2")',
                     '!InPartyAllowDead("IMOEN2")'):
            self.assertIn(need, trigger)
        self.assertIn('SetGlobal("CSR_IMSOA_STANDIN","GLOBAL",1)', action)
        self.assertLess(action.index('ActionOverride("IMOEN2",MakeGlobalOverride())'),
                        action.index('ActionOverride("IMOEN2",DestroySelf())'))
        # Done once EET finds no Imoen who has been in the party: it creates IMOEN10.
        done = [t for _, t, a in step(7) if 'SetGlobal("CSR_IMSOA_BOOST","GLOBAL",1)' in a
                and "RealGlobalTimerExpired" not in t]
        self.assertEqual(1, len(done))
        for need in ('Global("CSR_IMSOA_STANDIN","GLOBAL",1)', '!InMyArea("IMOEN2")',
                     '!BeenInParty("IMOEN2")'):
            self.assertIn(need, done[0])
        # Each timeout drops whatever is still queued and ends with the boosts
        # pending; SoA decides by who arrives.
        for n in (5, 7):
            timeout = [a for _, t, a in step(n) if "RealGlobalTimerExpired" in t]
            self.assertEqual(1, len(timeout), n)
            for need in ('ClearActions("IMOEN2")', 'SetGlobal("CSR_IMSOA_BOOST","GLOBAL",1)',
                         'SetGlobal("CSR_IMSOA_PREP","GLOBAL",9)'):
                self.assertIn(need, timeout[0])
        # No destructive action is queued twice: each one leaves its state.
        end = next(i for i, (t, _) in enumerate(blocks) if '!Global("CSR_IMSOA_PREP","GLOBAL",9)' in t)
        self.assertEqual(2, sum(a.count("DestroySelf()") for a in actions[strip:end]))
        self.assertNotIn('CSR_IMSOA_FAILED","GLOBAL",2', game.baf("csretbgt") + game.baf("baldur"))

    def test_choice1_refuses_an_imoen10_that_cannot_stand_in_for_her(self):
        cases = (({"imoen10_script_name": "Imoen10"}, 'script name is "Imoen10"'),
                 ({"imoen10_flags": 0x8000}, "marked as having been in the party"))
        for kwargs, message in cases:
            with self.subTest(**kwargs):
                game = self.game(**kwargs)
                _, text = game.install_component(292)
                self.assertIn("NOT INSTALLED DUE TO ERRORS", text)
                self.assertIn(message, text)
                self.assertEqual(game.before, game.tree())
        for number in (293, 294):
            with self.subTest(component=number):
                self.installed(number, imoen10_script_name="Imoen10")

    def test_strip_spell_removes_every_ability_score_effect(self):
        game = self.installed(292)
        spl = game.tree()["csrimstr.spl"]
        self.assertEqual(b"SPL V1  ", spl[:8])
        effects_at, = struct.unpack_from("<I", spl, 0x6A)
        count, = struct.unpack_from("<H", spl, 0x72 + 0x1E)
        self.assertEqual(7, count)
        removed = set()
        for n in range(count):
            pos = effects_at + n * 0x30
            opcode, = struct.unpack_from("<H", spl, pos)
            param1, param2 = struct.unpack_from("<iI", spl, pos + 4)
            self.assertEqual((337, -1), (opcode, param1))
            removed.add(param2)
        self.assertEqual({6, 10, 15, 19, 44, 49, 97}, removed)

    # ---- choice 3 -----------------------------------------------------------

    def test_choice3_teaches_only_spells_present_in_this_game(self):
        game = self.installed(294)
        lua = game.tree()["m_csrimd.lua"].decode()
        self.assertNotIn("CSR292_SPELLS", lua)
        spells = re.search(r"local SPELLS = \{([^}]*)\}", lua).group(1)
        self.assertEqual(["SPWI112", "SPWI203", "SPWI304"], sorted(re.findall(r'"(\w+)"', spells)))
        baldur = game.baf("baldur")
        self.assertIn('EEex_LuaAction("CSR_ImoenSoA_Dual()")', baldur)
        self.assertIn('EEex_LuaAction("CSR_ImoenSoA_Learn()")', baldur)
        self.assertIn('Global("K#ImoenImport","AR0602",1)', baldur)

    def test_choices_1_and_2_need_no_eeex(self):
        for number in (292, 293):
            with self.subTest(component=number):
                game = self.installed(number, eeex=False)
                after = game.tree()
                for name in game.changed():
                    self.assertNotIn(b"EEex", after[name], name)
                self.assertNotIn("m_csrimd.lua", after)

    def test_choice3_requires_eeex_without_mutation(self):
        game = self.game(eeex=False)
        _, text = game.install_component(294)
        self.assertIn("SKIPPING", text)
        self.assertEqual(game.before, game.tree())

    # ---- gear fallback, every choice -----------------------------------------

    def test_unprepared_arrival_banks_gear_then_restores_the_belt(self):
        for number in (292, 293, 294):
            with self.subTest(component=number):
                game = self.installed(number)
                blocks = baf_blocks(game.baf("baldur"))
                # Three passes: drop EET's belt, bank the rest, re-equip a fresh belt,
                # so no second unique belt ends up in EET's bank.
                drop = next(i for i, (t, a) in enumerate(blocks) if 'DestroyItem("IMOENHP1")' in a)
                self.assertIn('Global("CSR_IMSOA_FAILED","GLOBAL",1)', blocks[drop][0])
                self.assertIn('Global("CSR_IMSOA_FB","GLOBAL",0)', blocks[drop][0])
                self.assertIn('AreaCheck("AR0602")', blocks[drop][0])
                self.assertIn('InParty("IMOEN2")', blocks[drop][0])
                self.assertIn('ActionOverride("IMOEN2",DestroyItem("IMOENHP1"))', blocks[drop][1])
                self.assertNotIn("TakeCreatureItems", blocks[drop][1])
                bank = next(i for i, (t, a) in enumerate(blocks) if "TakeCreatureItems" in a)
                self.assertIn('Global("CSR_IMSOA_FB","GLOBAL",1)', blocks[bank][0])
                self.assertIn("RealGlobalTimerExpired", blocks[bank][0])
                self.assertRegex(blocks[bank][1], r'ActionOverride\("K#ImportContainer",' + TAKE_ALL)
                belt = next(i for i, (t, a) in enumerate(blocks) if 'CreateItem("IMOENHP1"' in a)
                self.assertIn('Global("CSR_IMSOA_FB","GLOBAL",2)', blocks[belt][0])
                self.assertIn("RealGlobalTimerExpired", blocks[belt][0])
                action = blocks[belt][1]
                self.assertLess(action.index("CreateItem"), action.index("FillSlot(SLOT_BELT)"))
                self.assertIn('SetGlobal("CSR_IMSOA_FAILED","GLOBAL",3)', action)

    # ---- component 910 integration -------------------------------------------

    def test_skip_helper_gets_the_same_preparation_in_either_install_order(self):
        helpers = []
        for order in ((910, 292), (292, 910)):
            with self.subTest(order=order):
                game = self.game()
                for number in order:
                    result, text = game.install_component(number)
                    self.assertIn("SUCCESSFULLY INSTALLED", text)
                helper = game.baf("csrskask")
                blocks = baf_blocks(helper)
                prep = [i for i, (t, _) in enumerate(blocks) if "CSR_IMSOA_PREP" in t]
                self.assertEqual(0, prep[0])
                for trigger, _ in (blocks[i] for i in prep):
                    self.assertIn('Global("CSR_SKIP_PHASE","GLOBAL",1)', trigger)
                    self.assertIn('Global("CSR_SKIP_FAILED","GLOBAL",0)', trigger)
                self.assertRegex(helper, r'ActionOverride\("PlayerChest00",' + TAKE_ALL)
                own_phase1 = next(i for i, (t, _) in enumerate(blocks)
                                  if 'Global("CSR_SKIP_PHASE","GLOBAL",1)' in t
                                  and "CSR_IMSOA_PREP" not in t)
                self.assertGreater(own_phase1, prep[-1])
                self.assertIn("CSR_IMSOA_PREP", game.baf("csretbgt"))
                # TLK indices of 910's own messages depend on install order.
                helpers.append([blocks[i] for i in prep])
        self.assertEqual(helpers[0], helpers[1])

    # ---- refusals leave the game untouched ------------------------------------

    def test_refusals_do_not_mutate_the_game(self):
        cases = (
            ({"odd_ending_rule": True}, "refusing to guess"),
            ({"guard": "late"}, "safety guard is not the single first block"),
            ({"bank": False}, "K#ImportContainer in BD4300"),
            ({"arrival_marker": False}, "never marks Imoen's arrival"),
        )
        for kwargs, message in cases:
            with self.subTest(**kwargs):
                game = self.game(**kwargs)
                _, text = game.install_component(293)
                self.assertIn("NOT INSTALLED DUE TO ERRORS", text)
                self.assertIn(message, text)
                self.assertEqual(game.before, game.tree())

    def test_refuses_a_game_without_next_trigger_object(self):
        for number in (292, 293, 294):
            with self.subTest(component=number):
                game = self.game(next_trigger_object=False)
                _, text = game.install_component(number)
                self.assertIn("NOT INSTALLED DUE TO ERRORS", text)
                self.assertIn("NextTriggerObject", text)
                self.assertEqual(game.before, game.tree())

    def test_choice1_refuses_eet_without_its_fresh_imoen(self):
        game = self.game(fresh_imoen10=False)
        _, text = game.install_component(292)
        self.assertIn("does not create IMOEN10", text)
        self.assertEqual(game.before, game.tree())

    def test_prerequisites_gate_without_mutation(self):
        for missing in (160, 290):
            with self.subTest(missing=missing):
                game = self.game(missing_remix=missing)
                _, text = game.install_component(292)
                self.assertIn("SKIPPING", text)
                self.assertEqual(game.before, game.tree())


if __name__ == "__main__":
    unittest.main()
