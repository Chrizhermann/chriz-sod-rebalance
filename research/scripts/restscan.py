import struct, os, sys

GAME = r"C:\Games\Baldur's Gate II Enhanced Edition modded"
KEY  = os.path.join(GAME, "chitin.key")
OVR  = os.path.join(GAME, "override")

ARE_TYPE = 0x03F2

def read(path):
    with open(path, "rb") as f:
        return f.read()

key = read(KEY)
sig, ver = key[0:4], key[4:8]
bif_count, res_count, bif_off, res_off = struct.unpack_from("<IIII", key, 8)

# BIF entries
biffs = []   # index -> filename (lowercase)
for i in range(bif_count):
    base = bif_off + i*12
    flen, fnoff = struct.unpack_from("<II", key, base)
    fnlen, loc = struct.unpack_from("<HH", key, base+8)
    name = key[fnoff:fnoff+fnlen].split(b"\x00")[0].decode("ascii","replace")
    biffs.append(name.lower())

# Resource entries: resref(8), type(H), locator(I) => 14 bytes
# locator: bits 31-20 source biff index; 13-0 file index in biff
res = {}  # resref -> (type, biff_index, file_index)
for i in range(res_count):
    base = res_off + i*14
    resref = key[base:base+8].split(b"\x00")[0].decode("ascii","replace")
    rtype, = struct.unpack_from("<H", key, base+8)
    locator, = struct.unpack_from("<I", key, base+10)
    if rtype != ARE_TYPE:
        continue
    biff_idx = (locator >> 20) & 0xFFF
    file_idx = locator & 0x3FFF
    res[resref.upper()] = (biff_idx, file_idx)

def biff_of(resref):
    e = res.get(resref.upper())
    if not e: return None
    return biffs[e[0]]

def extract_from_biff(resref):
    e = res.get(resref.upper())
    if not e: return None
    biff_idx, file_idx = e
    biffpath = os.path.join(GAME, biffs[biff_idx].replace("/", os.sep))
    if not os.path.exists(biffpath):
        # try data/ lower
        return None
    data = read(biffpath)
    # BIF V1: sig+ver(8), fileCount(I 0x08), tilesetCount(I 0x0C), fileEntriesOff(I 0x10)
    fcount, tcount, foff = struct.unpack_from("<III", data, 8)
    for j in range(fcount):
        b = foff + j*16
        locator, off, size = struct.unpack_from("<III", data, b)
        ftype, = struct.unpack_from("<H", data, b+12)
        if (locator & 0x3FFF) == file_idx:
            return data[off:off+size]
    return None

def get_are_bytes(resref):
    p = os.path.join(OVR, resref + ".are")
    if os.path.exists(p):
        return read(p), "override"
    pl = os.path.join(OVR, resref.lower() + ".are")
    if os.path.exists(pl):
        return read(pl), "override"
    b = extract_from_biff(resref)
    if b is not None:
        return b, "biff"
    return None, None

def parse_rest(aredata):
    if len(aredata) < 0xC4: return None
    if aredata[0:4] != b"AREA": return None
    rest_off, = struct.unpack_from("<I", areadata if False else areata if False else aredata, 0xC0)
    s = rest_off
    if s == 0 or s+0xAC > len(areadata):
        return {"enabled":0,"day":0,"night":0,"max":0,"count":0,"creatures":[],"off":rest_off}
    name = aredata[s:s+32].split(b"\x00")[0].decode("ascii","replace")
    creatures = []
    for k in range(10):
        c = aredata[s+0x48+k*8 : s+0x48+(k+1)*8].split(b"\x00")[0].decode("ascii","replace")
        if c: creatures.append(c)
    count,  = struct.unpack_from("<H", aredata, s+0x98)
    diff,   = struct.unpack_from("<H", aredata, s+0x9a)
    maxc,   = struct.unpack_from("<H", aredata, s+0xa4)
    enabled,= struct.unpack_from("<H", aredata, s+0xa6)
    day,    = struct.unpack_from("<H", aredata, s+0xa8)
    night,  = struct.unpack_from("<H", aredata, s+0xaa)
    return {"name":name,"enabled":enabled,"day":day,"night":night,"max":maxc,
            "count":count,"diff":diff,"creatures":creatures,"off":rest_off}

# Identify SoD areas: ARE resource whose biff is an eetBD/BDTP/goBD biff
sod = []
for resref,(bidx,fidx) in res.items():
    bn = biffs[bidx]
    if "eetbd" in bn or "bdtp" in bn or bn.startswith("data/gobd") or "gobd" in bn:
        sod.append(resref)
sod.sort()

print(f"# SoD areas found in EET biffs: {len(sod)}\n")
print(f"{'AREA':8} {'SRC':9} {'EN':3} {'DAY':4} {'NIGHT':5} {'MAX':4} {'#':3} {'NAME':28} CREATURES")
rows = []
for r in sod:
    data, src = get_are_bytes(r)
    if data is None:
        print(f"{r:8} <no data>")
        continue
    info = parse_rest(data)
    if info is None:
        print(f"{r:8} <not ARE / {len(data)}b>")
        continue
    rows.append((r,src,info))

# sort by day prob desc
rows.sort(key=lambda x: (-(x[2]['day'] or 0), -(x[2]['night'] or 0)))
for r,src,info in rows:
    creats = ",".join(info['creatures'][:4])
    print(f"{r:8} {src:9} {info['enabled']:<3} {info['day']:<4} {info['night']:<5} {info['max']:<4} {info['count']:<3} {info.get('name','')[:28]:28} {creats}")

print("\n# Distribution of DAY probability among SoD areas with rest enabled:")
from collections import Counter
c = Counter(info['day'] for _,_,info in rows if info['enabled'])
for v in sorted(c, reverse=True):
    print(f"  day={v:4}: {c[v]} areas")
