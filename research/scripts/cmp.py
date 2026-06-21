import struct,os
def vals(p):
    if not os.path.exists(p): return None
    d=open(p,"rb").read()
    if d[0:4]!=b"AREA": return None
    ro,=struct.unpack_from("<I",d,0xC0)
    if ro==0 or ro+0xAC>len(d): return (0,0,0,0)
    en,=struct.unpack_from("<H",d,ro+0xa6); day,=struct.unpack_from("<H",d,ro+0xa8)
    ngt,=struct.unpack_from("<H",d,ro+0xaa); mx,=struct.unpack_from("<H",d,ro+0xa4)
    return (en,day,ngt,mx)
G=r"C:\Games\Baldur's Gate II Enhanced Edition modded"
for a in ["BD1000","BD3000","BD7100","BD7300","BD2000","BD5000"]:
    cur=vals(os.path.join(G,"override",a+".ARE"))
    scs=vals(os.path.join(G,"weidu_external","backup","stratagems","4218",a+".ARE"))
    cd33=vals(os.path.join(G,"weidu_external","cdtweaks","backup","3300",a+".ARE"))
    cd20=vals(os.path.join(G,"weidu_external","cdtweaks","backup","2020",a+".ARE"))
    print(f"{a}: current(en,day,ngt,max)={cur}  | pre-SCS4218={scs}  pre-CD3300={cd33}  pre-CD2020={cd20}")
