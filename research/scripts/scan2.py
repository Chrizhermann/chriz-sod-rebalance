import struct, os, glob, re
GAME=r"C:\Games\Baldur's Gate II Enhanced Edition modded"
OVR=os.path.join(GAME,"override")

# friendly names from EET table
names={}
tbl=os.path.join(GAME,"EET","tbl","map_eet_areas.tbl")
for line in open(tbl,encoding="ascii",errors="replace"):
    m=re.match(r"\s*(BD\w+)\b.*?//\s*\[?([^\]]*?)\]?\s*$", line)
    if m: names[m.group(1).upper()]=m.group(2).strip()

def parse(p):
    d=open(p,"rb").read()
    if d[0:4]!=b"AREA" or len(d)<0xC4: return None
    ro,=struct.unpack_from("<I",d,0xC0)
    if ro==0 or ro+0xAC>len(d): 
        return dict(en=0,day=0,night=0,maxc=0,cnt=0,creats=[],ro=ro)
    creats=[d[ro+0x48+k*8:ro+0x48+(k+1)*8].split(b"\x00")[0].decode("ascii","replace") for k in range(10)]
    creats=[c for c in creats if c]
    cnt,=struct.unpack_from("<H",d,ro+0x98)
    diff,=struct.unpack_from("<H",d,ro+0x9a)
    maxc,=struct.unpack_from("<H",d,ro+0xa4)
    en,=struct.unpack_from("<H",d,ro+0xa6)
    day,=struct.unpack_from("<H",d,ro+0xa8)
    night,=struct.unpack_from("<H",d,ro+0xaa)
    # area flags & area type for context
    aflags,=struct.unpack_from("<I",d,0x14)
    return dict(en=en,day=day,night=night,maxc=maxc,cnt=cnt,diff=diff,creats=creats,ro=ro,aflags=aflags)

files=sorted({*glob.glob(os.path.join(OVR,"BD*.are")),*glob.glob(os.path.join(OVR,"bd*.are"))}, key=lambda x:os.path.basename(x).upper())
rows=[]
for f in files:
    nm=os.path.basename(f).upper().replace(".ARE","")
    info=parse(f)
    if info: rows.append((nm,info))

rows.sort(key=lambda x:(-(x[1]['day'] or 0),-(x[1]['night'] or 0),x[0]))
print(f"# {len(rows)} BD (SoD) areas in override\n")
print(f"{'AREA':8} {'EN':2} {'DAY':4} {'NGT':4} {'MAX':3} {'#':2} {'FRIENDLY':30} CREATURES")
for nm,i in rows:
    fn=names.get(nm,"")[:30]
    print(f"{nm:8} {i['en']:<2} {i['day']:<4} {i['night']:<4} {i['maxc']:<3} {i['cnt']:<2} {fn:30} {','.join(i['creats'][:4])}")

from collections import Counter
print("\n# DAY-probability distribution (rest-enabled areas only):")
c=Counter(i['day'] for _,i in rows if i['en'])
for v in sorted(c,reverse=True): print(f"  day={v:4}: {c[v]} areas")
en=sum(1 for _,i in rows if i['en']); dis=len(rows)-en
print(f"\n  rest-enabled: {en}   rest-disabled: {dis}")
