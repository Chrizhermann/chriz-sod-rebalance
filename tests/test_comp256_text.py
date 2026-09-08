"""Resource-local text edits preserve mod interjections and item mechanics."""
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'research/scripts'))
from test_comp291_installer import ROOT,WEIDU,write_fake_game,tree

def dialogue():
    # Five states, state 3's native transition to 4 plus a foreign interjection.
    data=bytearray(0x34+5*16+6*32)
    data[:8]=b'DLG V1.0'
    struct.pack_into('<IIII',data,8,5,0x34,6,0x84)
    for i,first in enumerate((0,1,2,3,5)):
        struct.pack_into('<IIII',data,0x34+i*16,0,first,2 if i==3 else 1,0xffffffff)
    for i in range(6):
        b=0x84+i*32
        struct.pack_into('<I',data,b,8)
    b=0x84+3*32
    struct.pack_into('<I',data,b,0)
    data[b+0x14:b+0x1c]=b'BDPHOSSE'
    struct.pack_into('<I',data,b+0x1c,4)
    b=0x84+4*32
    data[b+0x14:b+0x1c]=b'FOREIGN\0'
    struct.pack_into('<I',data,b+0x1c,77)
    return bytes(data)

def item():
    data=bytearray(0x72)
    data[:8]=b'ITM V1  '
    struct.pack_into('<I',data,0x4c,7) # Changed by a hypothetical weight mod.
    return bytes(data)+b'PRESERVE ITEM PAYLOAD'

@unittest.skipUnless(WEIDU.is_file(),'real WeiDU unavailable; set WEIDU_EXE')
class BridgeTextTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory(prefix='csr256-text-')
        self.addCleanup(tmp.cleanup)
        self.game=Path(tmp.name)
        write_fake_game(self.game)
        self.override=self.game/'override'
        (self.override/'bdphosse.dlg').write_bytes(dialogue())
        (self.override/'bdbwoosh.itm').write_bytes(item())
        shutil.copytree(ROOT/'chriz-sod-remix',self.game/'chriz-sod-remix')
        (self.game/'text.tp2').write_text('''BACKUP ~text-backup~
AUTHOR ~test~
BEGIN ~bridge text~ DESIGNATED 256
LOAD_TRA ~chriz-sod-remix/languages/english/setup.tra~
INCLUDE ~chriz-sod-remix/lib/comp256_text.tpa~
LAF csr256_text_preflight END
LAF csr256_text_install END
''')

    def install(self):
        return subprocess.run([str(WEIDU),'text.tp2','--force-install-list','256',
            '--game',str(self.game),'--use-lang','en_US','--language','0','--no-exit-pause'],
            cwd=self.game,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=60)

    def test_only_owned_string_references_change(self):
        result=self.install()
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        after=bytearray((self.override/'bdphosse.dlg').read_bytes())
        after[0x64:0x68]=b'\0'*4
        self.assertEqual(bytes(after),dialogue())
        after=bytearray((self.override/'bdbwoosh.itm').read_bytes())
        after[0x54:0x58]=b'\0'*4
        self.assertEqual(bytes(after),item())
        tlk=(self.game/'lang/en_us/dialog.tlk').read_bytes()
        self.assertIn(b'captured crusader supplies',tlk)
        self.assertIn(b'Weight: 7',tlk)
        self.assertNotIn(b'%csr256_bwoosh_weight%',tlk)

    def test_wrong_scene_is_rejected_without_resource_writes(self):
        data=bytearray(dialogue())
        struct.pack_into('<I',data,0x84+3*32+0x1c,2)
        (self.override/'bdphosse.dlg').write_bytes(data)
        before=tree(self.override)
        self.assertNotEqual(self.install().returncode,0)
        self.assertEqual(tree(self.override),before)

    def test_late_item_failure_precedes_dialogue_write(self):
        (self.override/'bdbwoosh.itm').write_bytes(b'truncated')
        before=tree(self.override)
        self.assertNotEqual(self.install().returncode,0)
        self.assertEqual(tree(self.override),before)

if __name__=='__main__': unittest.main()
