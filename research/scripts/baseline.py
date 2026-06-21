import struct,os,glob
from collections import Counter,defaultdict
GAME=r"C:\Games\Baldur's Gate II Enhanced Edition modded"
OVR=os.path.join(GAME,"override")
key=open(os.path.join(GAME,"chitin.key"),"rb").read()
bc,rc,bo,ro=struct.unpack_from("<IIII",key,8)
biffs=[]
for i in range(bc):
    b=bo+i*12; fl,fo=struct.unpack_from("<II",key,b); fnl,_=struct.unpack_from("<HH",key,b+8)
    biffs.append(key[fo:fo+fnl].split(b"\x00")[0].decode("ascii","replace"))
loc={}
for i in range(rc):
    b=ro+i*14; rt,=struct.unpack_from("<H",key,b+8)
    if rt!=0x03F2: continue
    rr=key[b:b+8].split(b"\x00")[0].decode("ascii","replace").upper()
    l,=struct.unpack_from("<I",key,b+10); loc[rr]=((l>>20)&0xFFF, l&0x3FFF)
def from_biff(rr):
    if rr not in loc: return None
    bi,fi=loc[rr]; bp=os.path.join(GAME,biffs[bi].replace("/",os.sep))
    if not os.path.exists(bp): return None
    d=open(bp,"rb").read(); fcount,tc,foff=struct.unpack_from("<III",d,8)
    for j in range(fcount):
        bb=foff+j*16; lcr,off,size=struct.unpack_from("<III",d,bb)
        if (lcr&0x3FFF)==fi: return d[off:off+size]
    return None
def getbytes(rr):
    for nm in (rr+".are", rr.lower()+".are", rr+".ARE"):
        p=os.path.join(OVR,nm)
        if os.path.exists(p): return open(p,"rb").read(),"ovr"
    b=from_biff(rr)
    return (b,"bif") if b else (None,None)
def rest(d):
    if not d or d[0:4]!=b"AREA" or len(d)<0xC4: return None
    r,=struct.unpack_from("<I",d,0xC0)
    if r==0 or r+0xAC>len(d): return (0,0,0,0,0)
    cnt,=struct.unpack_from("<H",d,r+0x98); mx,=struct.unpack_from("<H",d,r+0xa4)
    en,=struct.unpack_from("<H",d,r+0xa6); day,=struct.unpack_from("<H",d,r+0xa8); ngt,=struct.unpack_from("<H",d,r+0xaa)
    return (en,day,ngt,mx,cnt)

# gather all area resrefs: from chitin (AR/OH/BG/BD) + override loose
names=set(loc.keys())
for f in glob.glob(os.path.join(OVR,"*.are"))+glob.glob(os.path.join(OVR,"*.ARE")):
    names.add(os.path.basename(f).upper().replace(".ARE",""))

groups=defaultdict(list)
for rr in names:
    pre = "BG1(BG)" if rr.startswith("BG") else "SoD(BD)" if rr.startswith("BD") else "BG2(AR)" if rr.startswith("AR") else "EE(OH)" if rr.startswith("OH") else "other"
    d,src=getbytes(rr); info=rest(d)
    if info is None: continue
    groups[pre].append((rr,info,src))

print(f"{'GROUP':10} {'#areas':6} {'rest-ON':7} {'w/creatures':11}  day-prob histogram (enabled, creature-bearing)")
for g in ["BG1(BG)","SoD(BD)","BG2(AR)","EE(OH)"]:
    rows=groups.get(g,[])
    on=[x for x in rows if x[1][0]==1]
    wc=[x for x in on if x[1][4]>0]   # has creature table -> real ambush area
    hist=Counter(x[1][1] for x in wc)
    hs=" ".join(f"{k}:{hist[k]}" for k in sorted(hist,reverse=True))
    print(f"{g:10} {len(rows):<6} {len(on):<7} {len(wc):<11}  {hs}")

print("\n# SoD real-ambush areas (rest ON, has creature table), day/night:")
for rr,info,src in sorted([x for x in groups['SoD(BD)'] if x[1][0]==1 and x[1][4]>0], key=lambda x:-x[1][1]):
    print(f"  {rr}: day={info[1]:3} night={info[2]:3} max={info[3]} ncre={info[4]}")

print("\n# BG2 real-ambush areas day-prob (for scale):")
for rr,info,src in sorted([x for x in groups['BG2(AR)'] if x[1][0]==1 and x[1][4]>0], key=lambda x:-x[1][1])[:15]:
    print(f"  {rr}: day={info[1]:3} night={info[2]:3} max={info[3]} ncre={info[4]}")

print("\n# BG1 real-ambush areas day-prob (for scale):")
for rr,info,src in sorted([x for x in groups['BG1(BG)'] if x[1][0]==1 and x[1][4]>0], key=lambda x:-x[1][1])[:15]:
    print(f"  {rr}: day={info[1]:3} night={info[2]:3} max={info[3]} ncre={info[4]}")
