# chriz-sod-rebalance

A Siege of Dragonspear remix and companion rebalance for BG2:EE + EET, with
standalone BG:EE + SoD also in scope. Current release: **v0.6.7**.

Download the Windows installer ZIP from [Releases](https://github.com/Chrizhermann/chriz-sod-rebalance/releases/latest),
extract it into the game directory containing `chitin.key`, close the game, and run
`setup-chriz-sod-remix.exe`. Install as a tail mod after EET_end. Keep existing
WeiDU history: do not uninstall or reinstall earlier components to apply this repair.

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

The release has 34 component declarations. The previous 31-component fresh
selection remains available; add optional 910 on supported EET setups. Omit
repair-only 291 and choose one of the mutually exclusive 900/901 alternatives.
See [component instructions](chriz-sod-remix/README.md), the
[feature inventory](docs/00-feature-inventory.md), and [changelog](CHANGELOG.md).

The EET safety guard, victory sequence, save/reload, and sampled import preservation
passed native testing. Standalone credits and broader party/multiplayer coverage
remain pending; see the [runtime record](docs/playtest/2026-09-06-ending-runtime.md).
The full-skip Yes route also passed a six-person native test with saved XP/import
evidence. Transition polish and additional native variants remain open; see its
[acceptance record](docs/design/wave1/06-optional-sod-skip-testing.md).
Research and approved designs remain in `docs/`; new encounter designs require
discussion before implementation.
