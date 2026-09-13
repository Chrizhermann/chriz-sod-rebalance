# Third-party notices

The Windows release includes the official WeiDU 249.00 Windows AMD64
executable, renamed to `setup-chriz-sod-remix.exe`. WeiDU is distributed under
the GNU General Public License version 2; the release includes its license as
`WEIDU-COPYING.txt`.

- [WeiDU binary archive](https://github.com/WeiDUorg/weidu/releases/download/v249.00/WeiDU-Windows-249-amd64.zip)
- [WeiDU source](https://github.com/WeiDUorg/weidu/tree/v249.00)
- Archive SHA256: `b156910cbec69359fc2e42f6739aa959d49047d6fd3dc172f6bed88ffad8f927`
- Executable SHA256: `ad70f5897a6d0ba4b0d226f845a9b14cf345f56cc9697ca8d05cac9fe4932c1a`

Bridge mage defensive priorities and manual sequencer delivery draw on David
Wallace's Sword Coast Stratagems 35.21. Source paths and the changes made for
this encounter are recorded in `chriz-sod-remix/lib/comp256_ai.tpa` and
`docs/design/wave1/08-boareskyr-bridge.md`. This mod uses its own finite spell
budgets and installed spell identities; no generated SCS script is bundled.

The bridge tile patches derive from Beamdog's Siege of Dragonspear scenery,
with barrels removed using ImageGen. Only the replacement tiles are included.
Source provenance, the edited region and retained transparency are recorded in
`chriz-sod-remix/art/bridge/README.md` and its manifest. The mod requires an
installed copy of the game's SoD resources.
