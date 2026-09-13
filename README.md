# chriz-sod-rebalance

A Siege of Dragonspear remix and companion rebalance for BG2:EE + EET, with
standalone BG:EE + SoD also in scope. Current release: **v0.6.9**.

v0.6.9 adds **135** (default: keep the assassin ambush without
dead magic), **235** (preserve Ymori's staged quest after older cuts), and **265**
(Mizhena's amulet on the existing corpse and the missed creature-ban fixes).
See the [approved scope and save boundaries](docs/design/wave1/07-filler-triage.md).
Liia's prologue reward is a flat **22,000 XP per character** on every difficulty;
fresh 175 includes it, while **176** updates older 24,000 installations.

**256** replaces the Boareskyr barrel/portal finale with two wizards,
four fire/earth elementals and two veteran guards. It includes finite defensive
recasting, Haste on enemy sighting, coordinated engagement and cleaned day/night
bridge artwork. Mages are level 13 below Insane and level 14 on Insane. Bence
arrives beside the party after combat to open the passage through his dialogue.
Optional **257** adds only the two Insane mage sequencers: Greater Malison/Slow
and Dispel Magic with Spell Revisions (Remove Magic otherwise)/Flame Arrow.
It requires the current 256 resources and installation before the enemies spawn;
regular 256 retains the same stats and spellbooks without sequencer use. Install
256 before first entering BD2000; an installed 255 can stay in place.

Default-selected **266** limits Shadow Aspect's Insane Mislead to one use per
actor. Component **197** also gains Skie's normal, protagonist-dependent SoD XP
catch-up, corrected recruitment/rejoin dialogue, and movable SCS stock potions.
It does not grant a flat 250,000 XP regardless of the protagonist's XP.

Download the Windows installer ZIP from [Releases](https://github.com/Chrizhermann/chriz-sod-rebalance/releases/latest),
extract it into the game directory containing `chitin.key`, close the game, and run
`setup-chriz-sod-remix.exe`. Install as a tail mod after EET_end. Keep existing
WeiDU history: do not uninstall or reinstall earlier components to apply this repair.

v0.6.8 fixes component **900** rejecting camp chests modified by earlier mods.
It preserves all existing items and their charges/flags, then adds the eight
approved treasure records. Component 910 and the selection/order are unchanged.
For a mod-manager installation paused after 900 failed, use that manager's
recovery flow; replacing the archive alone does not reconcile its recorded step.

Component **290** ends SoD after the short victory celebration. Dazzo starts the
normal BG2 opening on EET, retaining existing import and item-placement rules.
There is no new equipment handout. Install it before first visiting BD4300.
For EET copies that already have an older 290, append **291**; fresh 290 already
includes the correction. Standalone players should not select the EET-only repair.

Optional EET component **910** offers a full SoD skip at the first palace-bedroom
arrival. Confirming Yes uses normal carried-inventory import rules and adds
250,000 XP to the protagonist once, on BG2 arrival. Ground-loot recovery is not
included. Requires EET_end and components 110, 140, 150, and 160; install before
the first palace arrival. It adds no EEex dependency.

The release has **41 component declarations in seven install groups**.
Selection depends on installed prerequisites and earlier versions: 176, 235 and
291 update older components; fresh versions already include those corrections.
Choose one of 900/901, add 257 only for Extra Challenge, and select 910 only on
supported EET setups.
See [component instructions](chriz-sod-remix/README.md), the
[feature inventory](docs/00-feature-inventory.md), and [changelog](CHANGELOG.md).

The EET safety guard, victory sequence, save/reload, and sampled import preservation
passed native testing. Standalone credits and broader party/multiplayer coverage
remain pending; see the [runtime record](docs/playtest/2026-09-06-ending-runtime.md).
The full-skip Yes route also passed a six-person native test with saved XP/import
evidence. Transition polish and additional native variants remain open; see its
[acceptance record](docs/design/wave1/06-optional-sod-skip-testing.md).
The harder bridge build, prompt Bence arrival, save/reload and onward crossing
passed the user's [combined playtest](docs/playtest/2026-09-08-bridge-finale.md).
The final 256/257 split and finite Mislead correction have not received new native
acceptance; Shadow Aspect testing is deferred. The companion appearance issue
after palace rest remains unresolved. The [release report](docs/releases/v0.6.9.md)
records 273 main tests, 41 research tests, 14 ending self-tests, and successful
WeiDU249 parsing of the TP2 and 56 libraries. These are offline checks and do
not extend the native observations above.
Research and approved designs remain in `docs/`; new encounter designs require
discussion before implementation.
