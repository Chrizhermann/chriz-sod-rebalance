"""Real public-installer checks in a synthetic EET; no native scheduling claim."""
import struct
import subprocess
import unittest
from pathlib import Path

from test_bdscry_compat import WEIDU, SyntheticDialogGame, _dialog_source
from test_optional_sod_skip import parse_containers
import test_optional_sod_skip as probe


ACTION_IDS = '''IDS V1.0
7 CreateCreature(S:NewObject*,P:Location*,I:Face*DIR)
8 Dialogue(O:Object*)
15 GiveItem(S:Object*,O:Target*)
30 SetGlobal(S:Name*,S:Area*,I:Value*)
36 Continue()
86 SetInterrupt(I:State*BOOLEAN)
109 IncrementGlobal(S:Name*,S:Area*,I:Value*)
110 LeaveAreaLUA(S:Area*,S:Parchment*,P:Point*,I:Face*DIR)
111 DestroySelf()
116 TakePartyItem(S:Item*)
120 StartCutSceneEx(S:CutScene*,I:evaluateConditions*BOOLEAN)
121 StartCutSceneMode()
122 EndCutSceneMode()
198 StartDialogueNoSet(O:Object*)
169 DestroyItem(S:ResRef*)
202 FadeToColor(P:Point*,I:Blue*)
203 FadeFromColor(P:Point*,I:Blue*)
224 GivePartyAllEquipment()
227 CreateCreatureObject(S:ResRef*,O:Object*,I:Usage1*,I:Usage2*,I:Usage3*)
257 PickUpItem(S:ResRef*)
259 AddXPObject(O:Object*,I:XP*)
264 CopyGroundPilesTo(S:Area*,P:Point*)
268 RealSetGlobalTimer(S:Name*,S:Area*,I:Time*)
338 SetCutSceneLite(I:BOOL*BOOLEAN)
363 AddStoreItem(S:Store*,S:Item*,I:Count*,I:Flags*)
379 TakeCreatureItems(O:Object*,I:Type*TAKEITM)
388 DisplayStringHeadNoLog(O:Object*,I:StrRef*)
394 MoveContainerContents(S:Container1*,S:Container2*)
'''
TRIGGER_IDS = '''IDS V1.0
0x400D Exists(O:Object*)
0x400F Global(S:Name*,S:Area*,I:Value*)
0x4023 True()
0x4030 False()
0x4034 GlobalGT(S:Name*,S:Area*,I:Value*)
0x4035 GlobalLT(S:Name*,S:Area*,I:Value*)
0x4042 PartyHasItem(S:Item*)
0x4061 HasItem(S:ResRef*,O:Object*)
0x407E AreaCheck(S:ResRef*)
0x4089 OR(I:OrCount*)
0x40A5 Name(S:Name*,O:Object*)
0x40B6 RealGlobalTimerExpired(S:Name*,S:Area*)
0x40CB InMyArea(O:Object*)
0x40D3 InPartyAllowDead(O:Object*)
'''


class SkipGame(SyntheticDialogGame):
    def __init__(self, *, extra_predicate=False, bedroom_ground=False,
                 missing_chest=False, chest_treasure=False, eet=True, missing_dependency=None):
        super().__init__(_dialog_source())
        override = self.root / "override"
        for name, text in {
            "action.ids": ACTION_IDS,
            "trigger.ids": TRIGGER_IDS,
            "object.ids": "IDS V1.0\n1 Myself\n" + "".join(
                f"{20+n} Player{n}\n" for n in range(1, 7)),
            "dir.ids": "IDS V1.0\n0 S\n2 SW\n",
            "takeitm.ids": "IDS V1.0\n0 ALL\n1 BACKPACK\n",
        }.items():
            (override / name).write_text(text, encoding="ascii")
        if eet:
            (override / "eet.flag").write_text("synthetic EET marker")
        room = [("PlayerChest00", 2, ["csrjunk"] if chest_treasure else []),
                ("Bookcase", 2, ["csrbook"])]
        if bedroom_ground:
            room.append(("UnrelatedLoot", 4, ["csrjunk"]))
        if missing_chest:
            room.pop(0)
        (override / "bd0103.are").write_bytes(probe.GroundProbeVerifierTests.area(room))
        (override / "bd6100.are").write_bytes(probe.GroundProbeVerifierTests.area(
            [("K#ImportContainer", 2, [])]))
        for name in ("campaign.2da", "startare.2da"):
            (override / name).write_text("2DA V1.0\n0\n COLUMN\nROW SoD\n")
        (override / "k#import.sto").write_bytes(b"STORV1.0" + bytes(0x94))
        creature = bytearray(0x338)
        creature[:8] = b"CRE V1.0"
        for pos in (0x2A0, 0x2A8, 0x2B0):
            struct.pack_into("<I", creature, pos, 0x2D4)
        struct.pack_into("<III", creature, 0x2B8, 0x2D4, 0x324, 1)
        struct.pack_into("<I", creature, 0x2C4, len(creature))
        for index in range(40):
            struct.pack_into("<H", creature, 0x2D4 + index*2, 0xFFFF)
        struct.pack_into("<H", creature, 0x2D4 + 21*2, 0)
        creature[0x324:0x32C] = b"csrjunk\0"
        # Real CUTSPY carries avatar removal: it prevents non-INSTANT actions.
        creature[0x33] = 1
        struct.pack_into("<I", creature, 0x20, 16)
        struct.pack_into("<I", creature, 0x2C8, 1)
        effect_start = len(creature)
        creature.extend(bytes(264))
        struct.pack_into("<I", creature, effect_start + 8, 271)
        for name in ("cutspy.cre", "k#telbgt.cre"):
            (override / name).write_bytes(creature)
        for name, category in (("misc47.itm", 0), ("csrbag.itm", 36), ("csrjunk.itm", 0)):
            item = bytearray(0x72)
            item[:8] = b"ITM V1  "
            struct.pack_into("<H", item, 0x1C, category)
            (override / name).write_bytes(item)
        fixture = self.root / "fixture"
        for name in ("bd0103", "bd6100", "baldur", "ar0602"):
            (fixture / f"{name}.baf").write_text(
                'IF True() THEN RESPONSE #100 Continue() END\n')
        (fixture / "bd0103.baf").write_text('''
IF Global("BD_PARTY_ITEMS","BD0103",0) GlobalLT("BD_PLOT","GLOBAL",51)
THEN RESPONSE #100
SetGlobal("BD_PARTY_ITEMS","BD0103",1)
''' + "\n".join(f'ActionOverride("PlayerChest00",TakeCreatureItems(Player{n},BACKPACK))'
                 for n in range(1, 7)) + '\nEND\n')
        (fixture / "bdsodtrn.baf").write_text(
            'IF True() THEN RESPONSE #100 CopyGroundPilesTo("BD0103",[190.540]) END\n')
        predicate = 'Global("OtherModRequirement","GLOBAL",1)' if extra_predicate else ""
        (fixture / "k#telbgt.baf").write_text(f'''
IF Global("K#FrameDelay","LOCALS",0) PartyHasItem("MISC47") {predicate}
THEN RESPONSE #100
TakePartyItem("MISC47") DestroyItem("MISC47")
AddStoreItem("K#IMPORT","MISC47",1,1) Continue()
END
''')
        setup = self.root / "setup-skip-bootstrap.tp2"
        setup.write_text('BACKUP ~weidu_external/backup/skip-bootstrap~\nAUTHOR ~test~\n'
                         'BEGIN ~fixture~\nCOMPILE ~fixture~\n')
        result = self._run(setup)
        if "SUCCESSFULLY INSTALLED" not in self.transcript(result):
            raise AssertionError(self.transcript(result))
        # Fixture-only install history: never edit a real install's WeiDU.log.
        log = self._find_output(self.root, "weidu.log")
        prerequisites = [
            ("EET_END/EET_END.TP2", 0),
            *(("CHRIZ-SOD-REMIX/SETUP-CHRIZ-SOD-REMIX.TP2", n) for n in (110, 140, 150, 160)),
        ]
        log.write_text(log.read_text() + "".join(
            f"~{path}~ #0 #{number} // synthetic prerequisite\n"
            for path, number in prerequisites if number != missing_dependency))
        self.before = self.tree()
        self.tlk_before = (self.root / "lang/en_us/dialog.tlk").read_bytes()

    def tree(self):
        return {f.name.lower(): f.read_bytes() for f in (self.root / "override").iterdir() if f.is_file()}

    def install(self):
        result = subprocess.run([
            str(WEIDU), "chriz-sod-remix/setup-chriz-sod-remix.tp2",
            "--force-install-list", "910", "--language", "0", "--use-lang", "en_us",
            "--no-exit-pause", "--noautoupdate", "--quick-log",
        ], cwd=self.root, capture_output=True, text=True, timeout=60)
        return result, self.transcript(result)

    def baf(self, name):
        output = Path(self.temporary.name) / (name + "-decompile")
        output.mkdir(exist_ok=True)
        result = subprocess.run([
            str(WEIDU), str(self._find_output(self.root / "override", name + ".bcs")),
            "--game", str(self.root), "--no-exit-pause",
        ], cwd=output, capture_output=True, text=True, timeout=60)
        if result.returncode:
            raise AssertionError(result.stdout + result.stderr)
        return self._find_output(output, name + ".baf").read_text()


@unittest.skipUnless(WEIDU.is_file(), f"WeiDU unavailable: {WEIDU}")
class OptionalSkipInstallerTests(unittest.TestCase):
    def game(self, **kwargs):
        game = SkipGame(**kwargs)
        self.addCleanup(game.cleanup)
        return game

    def test_public_install_changes_only_owned_resources_and_three_hooks(self):
        game = self.game()
        result, text = game.install()
        self.assertEqual(0, result.returncode, text)
        self.assertIn("SUCCESSFULLY INSTALLED", text)
        after = game.tree()
        changed = {name for name in after if after[name] != game.before.get(name)}
        self.assertEqual({"csrskask.cre", "csrskask.bcs", "csrskip.dlg",
                          "bd0103.bcs", "bd6100.bcs", "baldur.bcs"}, changed)
        cre = after["csrskask.cre"]
        for offset in (0x20, 0x2C8, 0x2C0):
            self.assertEqual(0, struct.unpack_from("<I", cre, offset)[0])
        self.assertEqual(b"csrskask", cre[0x248:0x250].rstrip(b"\0"))
        self.assertEqual(b"csrskask", cre[0x280:0x2A0].rstrip(b"\0"))
        helper = game.baf("csrskask")
        self.assertIn("StartDialogueNoSet(Player1)", helper)
        for forbidden in ("PickUpItem", "CSR_SKIP_SCAN", "csrs010", "TakePartyItem"):
            self.assertNotIn(forbidden, helper)
        self.assertNotIn("TakeCreatureItems(Player", helper)
        self.assertEqual(1, helper.count('AddStoreItem("K#IMPORT","MISC47",1,1)'))
        xp = game.baf("baldur")
        self.assertEqual(1, xp.count("AddXPObject(Player1,250000)"))
        self.assertIn('AreaCheck("AR0602")', xp)
        self.assertLess(xp.index('SetGlobal("CSR_SKIP_XP","GLOBAL",1)'), xp.index("AddXPObject"))

    def test_hold_backpacks_until_confirmed_no_and_leave_fresh_start_unchanged(self):
        game = self.game()
        _, text = game.install()
        self.assertIn("SUCCESSFULLY INSTALLED", text)
        blocks = probe._load_verifier().baf_blocks(game.baf("bd0103"))
        impounds = [(trigger, action) for trigger, action in blocks if "TakeCreatureItems" in action]
        self.assertEqual(1, len(impounds))
        trigger, action = impounds[0]
        self.assertIn('Global("BD_PARTY_ITEMS","BD0103",0)', trigger)
        self.assertRegex(trigger, r'(?s)OR\(2\)\s+!Global\("SOD_fromimport","GLOBAL",1\)\s+Global\("CSR_SKIP_CHOICE","GLOBAL",2\)')
        self.assertEqual(6, action.count("TakeCreatureItems("))
        offer = next(t for t, a in blocks if 'CreateCreatureObject("csrskask"' in a)
        self.assertIn('Global("BD_PARTY_ITEMS","BD0103",0)', offer)

    def test_ground_and_protected_eet_resources_are_byte_identical(self):
        game = self.game(bedroom_ground=True)
        _, text = game.install()
        self.assertIn("SUCCESSFULLY INSTALLED", text)
        after = game.tree()
        for name in ("bdsodtrn.bcs", "bd0103.are", "bd6100.are", "k#telbgt.bcs",
                     "k#telbgt.cre", "ar0602.bcs", "campaign.2da", "startare.2da"):
            self.assertEqual(game.before[name], after[name], name)
        self.assertEqual(["csrjunk"], parse_containers(after["bd0103.are"])["UnrelatedLoot"]["items"])

    def test_imported_imoen_selection_is_actual_present_only_and_avoids_party_duplicates(self):
        game = self.game()
        _, text = game.install()
        self.assertIn("SUCCESSFULLY INSTALLED", text)
        blocks = probe._load_verifier().baf_blocks(game.baf("csrskask"))
        requests = [(t, a) for t, a in blocks if "GiveItem(" in a]
        self.assertEqual(1, len(requests))
        trigger, action = requests[0]
        for guard in ('Global("CSR_IMOEN_IMPORT","GLOBAL",1)',
                      '!InPartyAllowDead("IMOEN2")', 'InMyArea("IMOEN2")',
                      '!PartyHasItem("MISC47")', 'HasItem("MISC47","IMOEN2")'):
            self.assertIn(guard, trigger)
        self.assertIn('ActionOverride("IMOEN2",GiveItem("MISC47","csrskask"))', action)
        received = next((t, a) for t, a in blocks if "AddStoreItem(" in a)
        self.assertIn('HasItem("MISC47",Myself)', received[0])
        self.assertLess(received[1].index('DestroyItem("MISC47")'), received[1].index("AddStoreItem"))
        bank = next((t, a) for t, a in blocks if 'TakeCreatureItems("IMOEN2",ALL)' in a)
        self.assertIn('Global("CSR_IMOEN_IMPORT","GLOBAL",1)', bank[0])
        self.assertNotIn("Imoen_equipment", game.baf("csrskask"))

    def test_missing_imoen_delivery_returns_control_without_xp_or_native_handoff(self):
        game = self.game()
        _, text = game.install()
        self.assertIn("SUCCESSFULLY INSTALLED", text)
        blocks = probe._load_verifier().baf_blocks(game.baf("csrskask"))
        guards = [(t, a) for t, a in blocks if "RealGlobalTimerExpired" in t]
        self.assertEqual(1, len(guards))
        self.assertIn('Global("CSR_SKIP_PHASE","GLOBAL",12)', guards[0][0])
        for statement in ('SetGlobal("CSR_SKIP_PHASE","GLOBAL",99)',
                          'SetGlobal("CSR_SKIP_FAILED","GLOBAL",1)',
                          "SetCutSceneLite(FALSE)", "EndCutSceneMode()",
                          "FadeFromColor([10.0],0)", "DisplayStringHeadNoLog(Player1,"):
            self.assertIn(statement, guards[0][1])
        self.assertNotIn("AddXPObject", guards[0][1])
        self.assertNotIn("K#TELBGT", guards[0][1])

    def test_rejects_changed_effective_eet_eligibility_instead_of_dropping_conditions(self):
        game = self.game(extra_predicate=True)
        _, text = game.install()
        self.assertIn("unsupported EET rule for MISC47", text)
        self.assertEqual(game.before, game.tree())
        self.assertEqual(game.tlk_before, (game.root / "lang/en_us/dialog.tlk").read_bytes())

    def test_rejects_missing_or_nonempty_staging_chest_without_mutations(self):
        for kwargs in ({"chest_treasure": True}, {"missing_chest": True}):
            with self.subTest(**kwargs):
                game = self.game(**kwargs)
                _, text = game.install()
                self.assertIn("NOT INSTALLED DUE TO ERRORS", text)
                self.assertEqual(game.before, game.tree())

    def test_public_platform_and_prerequisite_gates_do_not_mutate_resources(self):
        for kwargs in ({"eet": False}, {"missing_dependency": 160}, {"missing_dependency": 0}):
            with self.subTest(**kwargs):
                game = self.game(**kwargs)
                _, text = game.install()
                self.assertIn("SKIPPING:", text)
                self.assertNotIn("SUCCESSFULLY INSTALLED", text)
                self.assertEqual(game.before, game.tree())


if __name__ == "__main__":
    unittest.main()
