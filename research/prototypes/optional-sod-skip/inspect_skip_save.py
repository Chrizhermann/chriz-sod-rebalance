"""Read-only native skip evidence: party XP, globals, containers and bag stores."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import zlib

from verify_ground_probe import checked, number, containers


def string(data, offset, length=8):
    return checked(data, offset, length).split(b"\0")[0].decode("ascii").upper()


def inventory(cre):
    if checked(cre, 0, 8) != b"CRE V1.0":
        raise ValueError("unsupported creature format")
    offset, count = number(cre, 0x2BC), number(cre, 0x2C0)
    checked(cre, offset, count*20)
    return [{"resref": string(cre, offset + i*20),
             "charges": list(struct.unpack("<HHH", checked(cre, offset + i*20 + 10, 6)))}
            for i in range(count)]


def inspect(folder):
    gam = (folder / "BALDUR.gam").read_bytes()
    sav = (folder / "BALDUR.SAV").read_bytes()
    if checked(gam, 0, 8) != b"GAMEV2.0" or checked(sav, 0, 8) != b"SAV V1.0":
        raise ValueError("unsupported saved-game format")
    result = {"gam_sha256": hashlib.sha256(gam).hexdigest(),
              "sav_sha256": hashlib.sha256(sav).hexdigest(),
              "area": string(gam, 0x58), "globals": {}, "party": [], "areas": {}, "stores": {}}
    go, gn = number(gam, 0x38), number(gam, 0x3C)
    for offset in range(go, go + gn*84, 84):
        name = string(gam, offset, 32)
        if name.startswith(("CSR_", "CSR910_")) or name in ("ENDOFBG1", "BD_PLOT", "SOD_FROMIMPORT", "CHAPTER"):
            result["globals"][name] = number(gam, offset+40, "i")
    po, pn = number(gam, 0x20), number(gam, 0x24)
    for i in range(pn):
        row = po + i*0x160
        cre = checked(gam, number(gam, row+4), number(gam, row+8))
        result["party"].append({"slot": i, "dv": string(cre, 0x280, 32),
                                "area": string(gam, row+0x18), "xp": number(cre, 0x18),
                                "items": inventory(cre)})
    offset = 8
    names = set()
    while offset < len(sav):
        length = number(sav, offset)
        if not 1 <= length <= 260:
            raise ValueError("invalid archive filename length")
        name = string(sav, offset+4, length)
        if name in names:
            raise ValueError("duplicate archive resource")
        names.add(name)
        offset += 4+length
        size, compressed = number(sav, offset), number(sav, offset+4)
        offset += 8
        payload = checked(sav, offset, compressed)
        offset += compressed
        wanted_area = name in {"BG2300.ARE", "BD0120.ARE", "BD0103.ARE", "CSRS010.ARE", "BD6100.ARE", "AR0602.ARE"}
        if not wanted_area and not name.endswith(".STO"):
            continue
        if size > 32*1024*1024:
            raise ValueError("oversized evidence resource")
        decoder = zlib.decompressobj()
        data = decoder.decompress(payload, size+1)
        if len(data) != size or not decoder.eof or decoder.unused_data:
            raise ValueError("invalid compressed resource")
        if wanted_area:
            rows = containers(data)
            result["areas"][name] = rows
        else:
            if checked(data, 0, 8) != b"STORV1.0":
                raise ValueError("unsupported store format")
            so, sn = number(data, 0x34), number(data, 0x38)
            checked(data, so, sn*28)
            result["stores"][name] = [{"resref": string(data, so+i*28),
                                        "count": number(data, so+i*28+0x14),
                                        "charges": list(struct.unpack("<HHH", checked(data, so+i*28+0xA, 6)))}
                                       for i in range(sn)]
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("save_folder", type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.save_folder), indent=2))
