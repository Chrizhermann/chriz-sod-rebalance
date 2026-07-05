"""Generate csrseq1.spl / csrseq1b.spl for chriz-sod-remix component 170.

Structure mirrors SCS's install-generated sequencer pair (verified by binary dump
of dw#ms3.SPL / dw#ms3B.SPL on the dev install, 2026-07-06; see docs/research/10d
and docs/design/chapters/01-prologue.md section 2a):

- csrseq1  = the HaveSpellRES marker ("Spell Sequencer"), innate, no-VFX. Its own
  ability carries the payload as 3x opcode 146 (cast instantly at caster level,
  preset target) + op172 self-removal, exactly like dw#ms3 carries 2x Color Spray.
  Unlike SCS we do NOT re-grant via delayed op171: a full 3-spell sequencer firing
  twice per fight would break the "above Semaj, below Sarevok" tier lock.
- csrseq1b = the combined-SPL the brain force-casts at the target: op172 removes
  the marker from the caster (once-per-fight semantics), 3x op101 immunity to
  opcodes 38/60/80 for 1 tick + op189 casting-time -10 guard the follow-up
  ReallyForceSpell burst against disruption - byte-for-byte the dw#ms3B pattern.

Payload (design 01-prologue.md sec 2a, option 1 "control bomb", user-locked):
  SPWI312 Slow + SPWI401 Confusion + SPWI224 Glitterdust
  (resrefs verified IN Korlasz's spellbook on the dev install; spell.ids maps
  WIZARD_SLOW=2312, WIZARD_CONFUSION=2401, WIZARD_GLITTERDUST=2224 - identical
  mapping on vanilla EE and Spell Revisions, so whatever SR made them is what
  fires; SPWI410 from an earlier draft was wrong on both counts.)

Name strrefs are left at -1; the tp2 SAYs them at install time.
"""
import struct, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "chriz-sod-remix", "spl"))
os.makedirs(OUT, exist_ok=True)


def effect(op, tgt, p1, p2, tim, dur, res=b"", prob1=100):
    e = bytearray(48)
    struct.pack_into("<H", e, 0x00, op)
    e[0x02] = tgt
    e[0x03] = 0                      # power
    struct.pack_into("<i", e, 0x04, p1)
    struct.pack_into("<i", e, 0x08, p2)
    e[0x0C] = tim                    # timing mode
    e[0x0D] = 0                      # dispel/resistance (0 = natural/nonmagical, as dumped)
    struct.pack_into("<I", e, 0x0E, dur)
    e[0x12] = prob1
    e[0x13] = 0
    e[0x14:0x14 + len(res)] = res
    # dice / save / savebonus / special all zero, as in dw#ms3/dw#ms3B
    return bytes(e)


def spl(effects):
    hdr = bytearray(0x72)
    hdr[0:8] = b"SPL V1  "
    struct.pack_into("<i", hdr, 0x08, -1)   # unidentified name (SAY'd at install)
    struct.pack_into("<i", hdr, 0x0C, -1)   # identified name
    struct.pack_into("<I", hdr, 0x18, 0)    # flags
    struct.pack_into("<H", hdr, 0x1C, 4)    # spell type 4 = innate (as dw#ms3)
    struct.pack_into("<I", hdr, 0x1E, 0)    # exclusion
    struct.pack_into("<H", hdr, 0x22, 0)    # casting graphics: none
    struct.pack_into("<I", hdr, 0x34, 1)    # level 1 (as dw#ms3)
    struct.pack_into("<i", hdr, 0x50, -1)   # unidentified desc
    struct.pack_into("<i", hdr, 0x54, -1)   # identified desc
    struct.pack_into("<I", hdr, 0x64, 0x72) # ability table offset
    struct.pack_into("<H", hdr, 0x68, 1)    # ability count
    struct.pack_into("<I", hdr, 0x6A, 0x9A) # effects table offset
    struct.pack_into("<H", hdr, 0x6E, 0)    # casting feature index
    struct.pack_into("<H", hdr, 0x70, 0)    # casting feature count

    ab = bytearray(40)
    ab[0x00] = 1                            # ability type (as dumped from dw#ms3)
    struct.pack_into("<H", ab, 0x02, 4)     # location 4 = innate
    ab[0x0C] = 1                            # target 1 = creature
    ab[0x0D] = 0
    struct.pack_into("<H", ab, 0x0E, 1)     # range 1
    struct.pack_into("<H", ab, 0x12, 0)     # casting speed 0
    struct.pack_into("<H", ab, 0x1E, len(effects))  # nFx (empirical offset, see gotchas.md)
    struct.pack_into("<H", ab, 0x20, 0)     # first fx index
    struct.pack_into("<H", ab, 0x26, 1)     # projectile 1 = instant/none

    return bytes(hdr) + bytes(ab) + b"".join(effects)


# csrseq1 - marker + self-contained payload (fires if ever cast directly)
seq1 = spl([
    effect(146, 2, 0, 1, 0, 0, b"SPWI312"),   # cast Slow instantly at preset target
    effect(146, 2, 0, 1, 0, 0, b"SPWI401"),   # cast Confusion
    effect(146, 2, 0, 1, 0, 0, b"SPWI224"),   # cast Glitterdust
    effect(172, 1, 0, 0, 0, 0, b"csrseq1"),   # remove own marker from caster
])

# csrseq1b - bookkeeping shell force-cast by the brain at the fight target
seq1b = spl([
    effect(172, 1, 0, 0, 0, 0, b"csrseq1"),   # burn the marker -> HaveSpellRES goes false
    effect(101, 1, 0, 38, 0, 1),               # 1-tick immunity: op38 (silence)
    effect(101, 1, 0, 60, 0, 1),               # 1-tick immunity: op60 (casting failure)
    effect(101, 1, 0, 80, 0, 1),               # 1-tick immunity: op80
    effect(189, 1, 10, 0, 0, 1),               # casting time -10 for the forced burst
])

for name, data in (("csrseq1.spl", seq1), ("csrseq1b.spl", seq1b)):
    with open(os.path.join(OUT, name), "wb") as f:
        f.write(data)
    print(f"wrote {name}: {len(data)} bytes")
