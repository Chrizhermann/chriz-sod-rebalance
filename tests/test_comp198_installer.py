"""Read-only EET inputs copied into disposable #198 installer fixtures."""
import os
from pathlib import Path
import shutil
import struct
import unittest
from test_comp285_installer import EffectiveResources, InstallerFixture, WEIDU

SOURCE = os.environ.get("CSR198_SOURCE_GAME")

@unittest.skipUnless(WEIDU.is_file() and SOURCE, "set CSR198_SOURCE_GAME for copied-resource fixtures")
class RecruitmentTests(InstallerFixture):
    def setUp(self):
        super().setUp()
        self.source = Path(SOURCE)
        source = EffectiveResources(self.source)
        source.copy_ids(self.override)
        shutil.copyfile(self.source / "lang/en_us/dialog.tlk", self.game / "lang/en_us/dialog.tlk")
        names = "bd0102.are bd0110.are bd0109.are bd0104.are bdsafana.dlg bdfritz.dlg bddialog.2da bdcut04.bcs bdfritz.bcs bdbaldur.bcs bd0010.bcs bd0101.bcs bd0110.bcs bd0109.bcs bd0020.bcs bd1000.bcs bd0104.bcs bd0102.bcs bd7100.bcs bd3000.bcs yeslic5.cre branwe5.cre ajanti6.cre coran5.cre garric6.cre kagain6.cre alora6.cre xan6.cre kivan6.cre sharte6.cre tiax6.cre skie6.cre bdcoran.cre bdgarric.cre bdtiax.cre bdskie.cre".split()
        for name in names:
            old = self.source / "weidu_external/backup/chriz-sod-remix/198" / name
            (self.override / name).write_bytes(old.read_bytes() if old.is_file() else source.read(name))
        (self.game / "test.tp2").write_text('BACKUP ~test-backup~ AUTHOR ~test~ BEGIN ~198 fixture~\nINCLUDE ~chriz-sod-remix/lib/comp198.tpa~\n')

    def apply(self):
        result = self.run_weidu("test.tp2", "--force-install-list", "0")
        self.assert_success(result)
        self.assertTrue((self.override / "c19812.cre").is_file())
        self.assertTrue((self.override / "csr198sk.dlg").is_file())
        self.assertIn('CSR198_12_PICK', self.decompile("bd0102.bcs"))
        self.assertIn('CSR198_TIAX_JOINED', self.decompile("bdfritz.bcs"))

    def test_normal_resources(self):
        self.apply()

    def test_missing_donor_and_recruitment_table(self):
        (self.override / "xan6.cre").unlink()
        (self.override / "bddialog.2da").unlink()
        self.apply()
        self.assertFalse((self.override / "c19808.cre").exists())
        self.assertIn("xan", (self.override / "bddialog.2da").read_text().lower())

    def test_missing_native_blocks_and_dialogue_states(self):
        for name in ("bd0102", "bd0110", "bd7100", "bdfritz"):
            (self.override / (name + ".bcs")).unlink()
        (self.override / "bdsafana.dlg").unlink()
        (self.override / "bdfritz.dlg").unlink()
        self.apply()
        self.assertIn('BD_FRITZ_GET_OUT', self.decompile("bdfritz.bcs"))
        from test_khalid_continuity_installer import dialog_states
        safana=dialog_states((self.override/'bdsafana.dlg').read_bytes())
        self.assertNotIn('false()', safana[60].trigger)
        self.assertEqual(len(safana[60].transitions),6)
        self.assertTrue(any('joinparty()' in t.action for st in safana for t in st.transitions))
        self.assertNotIn('false()',dialog_states((self.override/'bdfritz.dlg').read_bytes())[0].trigger)


    def test_cameo_schedules_ignore_creature_build_and_position(self):
        for area,label in [('bd0110','Coran'),('bd0109','Garrick'),('bd0104','Tiax')]:
            p=self.override/(area+'.are');raw=bytearray(p.read_bytes())
            off,n=struct.unpack_from('<IH',raw,0x54)
            for i in range(n):
                at=off+i*272
                if raw[at:at+32].split(b'\0')[0].decode()==label:
                    raw[at+128:at+136]=b'CHANGED\0'
                    struct.pack_into('<HH',raw,at+32,17,19)
                    struct.pack_into('<I',raw,at+64,123)
            p.write_bytes(raw)
        self.apply()
        for area,label in [('bd0110','Coran'),('bd0109','Garrick'),('bd0104','Tiax')]:
            raw=(self.override/(area+'.are')).read_bytes();off,n=struct.unpack_from('<IH',raw,0x54)
            for i in range(n):
                at=off+i*272
                if raw[at:at+32].split(b'\0')[0].decode()==label:
                    self.assertEqual(struct.unpack_from('<I',raw,at+64)[0],0)
                    self.assertEqual(raw[at+128:at+136],b'CHANGED\0')

    def test_second_tail_install(self):
        self.apply()
        names = ("bdfritz.bcs", "bd0102.bcs", "bd0110.bcs", "bd0109.bcs", "bd0104.bcs",
                 "bd7100.bcs", "bdsafana.dlg", "bdfritz.dlg")
        first = {name: (self.override/name).read_bytes() for name in names}
        (self.game / "second.tp2").write_text((self.game / "test.tp2").read_text().replace("test-backup", "second-backup"))
        self.assert_success(self.run_weidu("second.tp2", "--force-install-list", "0"))
        for name in names:
            with self.subTest(resource=name):
                self.assertEqual((self.override/name).read_bytes(), first[name])

    def test_damaged_donor_is_only_unavailable_clone(self):
        (self.override / "xan6.cre").write_bytes(b"CRE V1.0")
        broken = bytearray((self.override / "alora6.cre").read_bytes())
        struct.pack_into("<II", broken, 0x2c4, len(broken) + 100, 1)
        (self.override / "alora6.cre").write_bytes(broken)
        self.apply()
        self.assertFalse((self.override / "c19808.cre").exists())
        self.assertFalse((self.override / "c19807.cre").exists())
