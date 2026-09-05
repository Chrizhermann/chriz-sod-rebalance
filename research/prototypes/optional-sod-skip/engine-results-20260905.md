# Native ground-pile probe: failed collection gate

Tested 2026-09-05 with user-authorized PC access. The proposed empty named
receptacle approach is **rejected on this tested build**. The optional SoD skip
remains unimplemented and must not be published or pinned in the collection.

## Observed result

`CopyGroundPilesTo("CSRGP002",[190.540])` copied A and B into a **new type-4
container named CSRSourceA**, at the requested coordinates. The preplaced empty
type-4 **CSRBG1PILE**, at those same coordinates, remained empty. Both source
ground piles retained their original tokens; source chest C was not copied and
destination chest D was unchanged. There were no extra target copies of A/B.

A full process restart, normal-menu Continue reload, and a second native
quicksave preserved that result. The read-only verifier rejected both saves
solely because CSRBG1PILE was empty. Container order changed on serialization;
name/type/item matching remained valid.

The banking command was deliberately **not run**, because its collection
precondition failed. Do not replace the expected name with CSRSourceA: that was
one observed source-derived name, not a proven stable identity for real BG1 loot.
No whole-bedroom sweep or low-level EEex container mutation is authorized by
this failed probe.

## Environment and evidence

- Game: `C:\Users\chris\Games\CEBG-SOD-ground-probe-20260905\game`
- Profile: `C:\Users\chris\OneDrive\Documents\CEBG SoD Ground Probe Offline 20260905`
- Source: a full copy of the accepted v0.6.5 EET test install; the copied
  single-character pool test save was used only as a disposable starting point.
- Actual executable: **BG2:EE 2.7.3.0**, with installed **EEex v1.2.0**.
  This is not a 2.6.6.0 or standalone-SoD validation claim.
- New tail entries: csr-ground-probe `ground-probe-1` component 0 and the
  existing EEex Remote Console v0.2.0 component 0, installed only in the copy.
- Probe resource provenance: CSRGP001/002 and CSRGPA-D are test-mod-owned new
  resources, created by csr-ground-probe component 0 from existing palace/potion
  resources. The copy/move primitives are native engine actions, not replacement
  EEex implementations. The bridge only submitted native action strings.
- Raw evidence stays outside Git under
  `C:\Users\chris\Games\CEBG-SOD-ground-probe-20260905\evidence`.

| Evidence | SHA-256 |
|---|---|
| Baldur.exe | `b51093a49140b2b8a7c046b4652bb8e535be24ebbc12b1d735e0b94217a14d57` |
| EEex.dll | `adc09b72951a28fed7b56ca1eba530f54c90505a495432f97401ea3c9b19a4c9` |
| copy-initial/BALDUR.SAV | `772bb01c852a93312de684da2d7a43222db31909220afdcd8cdcfbb60616bf9d` |
| copy-reloaded/BALDUR.SAV | `1bdced6b4106d032a0d5ee28b28590be31512230bc22f6c5b62959f5ad5791c9` |
| copy-initial/BALDUR.gam | `a883223602dacc69f455c1b7308cbca65180cec20555023bb519f9fec0ba80ab` |
| copy-reloaded/BALDUR.gam | `0f7673b200287d6e0e3112db5d1b6910c26f4816cd951a095639b5c425ba3a7f` |

The two GAM files have protagonist area CSRGP002 and game times 2517 and 2538.
The second save is `000000001-ff-Quick-Save-2`, not the original Quick-Save:
this install rotates names without changing the numeric prefix. An initial
stale-slot evidence selection was corrected; its files are explicitly marked
`copy-reloaded-stale-selection` and are not reload evidence.

## Test-harness caveats and isolation

- The first fresh profile downloaded existing Steam cloud saves before any
  save was loaded or written. Testing was moved to a second fresh profile;
  only the copied game's steam_appid.txt was disabled, its launcher received
  SteamAppId/SteamGameId=0, and the profile's legacy cloud-save setting was 0.
  The offline profile acquired no cloudsave directory before or after testing.
  No Steam account/global settings were changed. For 2.7, a legacy profile
  setting alone is not an isolation guarantee; see
  [Beamdog's cloud-save change](https://forums.beamdog.com/discussion/90560/new-infinity-engine-2-7-beta-release).
- Windows mouse input worked, but shortcut delivery did not. The existing
  local EEex bridge was therefore installed after closing the disposable game.
  Its ready handshake and a live ping succeeded.
- An initial space-separated multi-action bridge submission performed the copy
  but did not move the character onward. The destination move was submitted
  separately after confirming the character was idle. Future probe commands
  should remain separate as in the README; do not infer response-parser behavior
  from a successful bridge return.
- Calling `optionsScreen:LoadGame()` directly from a world-screen bridge poll
  crashed in `Infinity_PopMenu`. This was a test-harness UI-stack misuse, not a
  copy-action crash or a save-load failure. Its loader log is retained outside
  Git. The saved result subsequently loaded normally after restart; do not use
  that direct UI-engine call as a shortcut again.
- The disposable game and loader were closed after testing. The accepted
  source install's WeiDU.log and engine.lua, and the source test save's GAM/SAV,
  all retained their pre-test SHA-256 hashes. Live/stream installs and saves,
  component 290, released v0.6.5, and the collection pin were not modified.

Next source work: select a different provenance-safe ground-loot collection
mechanism, then implement the effective-EET-rule-aware stored-item adapter and
the actual bedroom/XP/handoff flow. This probe does not validate any of those.
