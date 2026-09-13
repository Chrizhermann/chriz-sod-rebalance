# Boareskyr Bridge barrel removal

These are small replacement tile packs for component 256. The source scenery is
Beamdog's Siege of Dragonspear Boareskyr Bridge artwork, obtained from the user's
installed game. The barrel removal was made with Codex's built-in ImageGen on
2026-09-08; both day and night edits were visually inspected before packaging.
The night edit used the original night scenery plus the cleaned day image as
references, keeping the replacement paving consistent.

The regeneration brief is: remove every barrel and its shadow from the supplied
bridge section, continue the existing stone paving naturally, and preserve the
bridge geometry, railings, lighting and unchanged scenery. ImageGen performs the
artistic edit. `research/scripts/pack_bridge_art.py` performs only fixed-size
normalization, tile slicing, palette/DXT1 encoding and retention of the original
binary transparency mask. The original water coverage is not regenerated.

The reference crop has world origin `(1088,1600)` and size `640x704`. Only the
rectangle `(1152,1728)` through `(1600,1984)` is packaged: columns 18–24 and rows
27–30 in the area's 80-column tile grid. The files contain 28 tiles in row order.
The same cleaned tiles also replace the four closed-door alternatives at TIS
indices 4882–4885 for DOOR07 cells 2261, 2262, 2341 and 2342.

- `CSR256D.PAL` and `CSR256N.PAL`: 28 palette-TIS tile records of 5,120 bytes each.
- `CSR256D.PVRZ` and `CSR256N.PVRZ`: one 512x256 DXT1 texture page each. The eighth
  tile column is transparent padding. On PVRZ-TIS installs these are installed as
  `B200090.PVRZ` and `B2000N90.PVRZ`, with conflicts rejected before any write.
- `manifest.json`: source/edit/output hashes and the exact edited rectangle.

The installer changes exactly 32 records in each existing day/night TIS. It
leaves the complete WEDs, water-overlay alternative tiles, door records and
navigation geometry unchanged. Removing the visible barrels therefore does not
open Bence's onward-passage gate early. Unexpected remapping or shared tile
references fail preflight rather than replacing unrelated scenery.

Validation includes real WeiDU fixtures for both TIS encodings, an installation
on copies of the effective day/night resources, and decoding the resulting
records back into comparison images. Both door states display the cleaned art;
the original transparency silhouette remains exact. These checks establish the
installed asset and geometry changes, not native in-game rendering acceptance.

Format references: [IESDP TIS](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/tis_v1.htm),
[WED](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/wed_v1.3.htm),
and [PVRZ](https://gibberlings3.github.io/iesdp/file_formats/ie_formats/pvrz.htm).
