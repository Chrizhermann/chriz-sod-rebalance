import struct, os
from collections import Counter
GAME = r"C:\Games\Baldur's Gate II Enhanced Edition modded"
key = open(os.path.join(GAME,"chitin.key"),"rb").read()
bif_count, res_count, bif_off, res_off = struct.unpack_from("<IIII", key, 8)
print("bifs",bif_count,"res",res_count)
biffs=[]
for i in range(bif_count):
    base=bif_off+i*12
    flen,fnoff=struct.unpack_from("<II",key,base)
    fnlen,loc=struct.unpack_from("<HH",key,base+8)
    name=key[fnoff:fnoff+fnlen].split(b"\x00")[0].decode("ascii","replace")
    biffs.append(name)
cnt=Counter()
examples={}
for i in range(res_count):
    base=res_off+i*14
    rtype,=struct.unpack_from("<H",key,base+8)
    if rtype!=0x03F2: continue
    loc,=struct.unpack_from("<I",key,base+10)
    bidx=(loc>>20)&0xFFF
    resref=key[base:base+8].split(b"\x00")[0].decode("ascii","replace")
    bn=biffs[bidx] if bidx<len(biffs) else f"<oob {bidx}>"
    cnt[bn]+=1
    examples.setdefault(bn,[]).append(resref)
for bn,c in cnt.most_common():
    print(f"{c:4}  {bn:30}  e.g. {','.join(examples[bn][:4])}")
