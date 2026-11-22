# SoD Remix (`chriz-sod-rebalance`)

Streamlines *Siege of Dragonspear* between Baldur's Gate I and Shadows of Amn for
**BG2:EE + EET** and standalone **BG:EE + SoD** (**v0.6.17**). Part of
**[Chriz Easy BG](https://bg.chrizfader.org/collection)**.

**[Chriz Easy BG](https://bg.chrizfader.org/collection)** · **[Rules & Balance](https://bg.chrizfader.org/rules)** · **[Latest Release](https://github.com/Chrizhermann/chriz-sod-rebalance/releases/latest)**

---

## Part 1 — For Players

*SoD Remix* keeps the best moments of *Siege of Dragonspear* while cutting slow
filler, keeping your classic Baldur's Gate companions together, and cleaning up the
campaign transition into Baldur's Gate II.

### What It Changes

- **Cuts filler, keeps XP pacing:**
  Trims repetitive mob waves across Coast Way, the road north, the Coalition Camp
  scouting maps, and Kanaglym while re-injecting milestone XP onto key battles and
  chapter transitions so campaign progression stays balanced.
- **Classic BG1 companions stay & join early:**
  Your full BG1 party stays intact at the start of SoD (`110`), carried Khalid
  remains controllable at Bridgefort while Adirran handles the local briefing
  (`115`), Skie can join in the palace hall before the first rest (`197`/`198`),
  and classic BG1 companions become available early around Baldur's Gate and the
  Coast Way camp (`198`).
- **Streamlined prologue & optional Palace SoD Skip:**
  Instantly skips Korlasz's opening dungeon (`140`) with a reworked post-dungeon
  Korlasz jailbreak (`170`) and flat `22,000 XP` per character from Liia (`175`–`177`).
  Removes the forced assassination night and mid-campaign hooded-man/dream
  interruptions (`120`/`130`/`150`). On continuous EET runs, optional **component
  `910`** offers a full Palace SoD Skip on first palace arrival (`250,000 XP` +
  normal EET gear import).
- **Revamped Boareskyr Bridge finale (`256`, optional `257`):**
  Replaces the vanilla barrel/portal event with a focused two-mage, two-veteran,
  and four-elemental demolition fight backed by a difficulty-scaled collapse timer
  (10 / 8 / 7 / 6 / 5 minutes on Easy / Normal / Core / Hard / Insane; disabled on
  Story Mode).
- **Avernus portal & fairer Belhifet (`285`):**
  Converts the Avernus lift ride into a direct portal and tunes Belhifet (+1
  weapons, 60% MR, +25% movement, difficulty-scaled HP, targeted Breach instead of
  mass dispel, bounded devil reinforcements).
- **Clean Dragonspear ending & Imoen handoff:**
  Wraps up SoD after the Dragonspear victory celebration (`290`, dropping the arrest
  and trial chain) and hands Imoen cleanly into Shadows of Amn (`292`/`293`/`294`)
  with proper EET gear handling and tome boosts.

### Simple Install

1. Close the game and any mod manager using the game directory.
2. Download the [latest release ZIP](https://github.com/Chrizhermann/chriz-sod-rebalance/releases/latest)
   and extract it into your game folder containing `chitin.key`.
3. Run `setup-chriz-sod-remix.exe` and install as a **tail mod after `EET_end`**
   (standalone BG:EE + SoD automatically excludes EET-only `291`, `292`–`294`, and `910`).
4. For active campaigns, install before first entering modified areas (`BD2000`,
   `BD4700`, `BD5000`, `BD5110`). On EET, raise a dead Imoen before ending SoD.

---

## Part 2 — Component Groups, Technical Notes & License

### Install Groups Overview (7 groups, 49 declarations)

| Group | Components | What It Covers |
|---|---|---|
| **1. Wave 1 — Global levers** | `100`, `110`, `115`, `120`, `130`, `135` | 5× rest-ambush reduction (`100`), keep BG1 party (`110`), Khalid Bridgefort continuity (`115`), remove mid-campaign hooded man (`120`), skip 4 rest-dreams (`130`), keep assassin ambush without dead magic (`135`, default) |
| **2. Prologue** | `140`–`198`, `910` | Korlasz dungeon skip (`140`), no auto-start party (`145`), crusade council without assassination night (`150`/`187`/`190`/`195`), Imoen stays (`160`), jailbreak & flat 22,000 XP/char (`170`/`175`/`177`), proclamation (`180`), Entar stays dead (`185`), Skie talk-to-join (`197`), early BG1 recruits (`198`), optional Palace SoD Skip (`910`, EET) |
| **3. Coast Way** | `200`–`225`, `245`, `900`/`901` | Crossing spiders & skip-proof bridge (`200`/`245`), Coast Way Forest cut & Rasaad at camp (`210`/`215`), Dwarven Dig Site & text-only Caelar omen (`220`/`225`), Treasure from removed content (`900` collect / `901` remove) |
| **4. The Road North** | `230`–`258` | Cleaner road-north camps (`230`), Forest of Wyrms cave skip (`240`), Morentherene Hard/Insane tiers (`250`), Boareskyr Bridge elemental battle + timer (`256`, legacy `255`) |
| **5. Coalition Camp & Avernus** | `260`–`285` | Fewer scouting enemies & Mizhena amulet (`260`/`265`), finite Shadow Aspect Mislead on Insane (`266`, default), Kanaglym trim (`270`), no basement reveal dispel (`280`), Avernus portal & fairer Belhifet (`285`) |
| **6. Ending & EET Handoff** | `290`–`294` | Dragonspear victory celebration ending (`290`) and EET Imoen handoff into Shadows of Amn (`292`/`293`/`294`) |
| **7. Extra Challenge** | `257` | Optional Insane Boareskyr Bridge mage sequencers (Greater Malison/Slow and Dispel or Remove Magic/Flame Arrow; requires `256`) |

### Key Selection Options & Update Components

- **Treasure (`900` / `901`):** Mutually exclusive — collect removed Coast Way Forest
  treasure in the Coast Way camp chest (`900`), or remove it with the area (`901`).
- **Imoen in Shadows of Amn (`292` / `293` / `294`, EET):** Choose at most one after
  `160`, `290`, and `EET_end`:
  - `292`: BG2 dual-class Imoen plus her BG1/SoD tome boosts (Chriz Easy BG default).
  - `293`: Continue with Imoen exactly as taken along.
  - `294`: Dual-class Imoen to mage at her end-of-SoD thief level (requires EEex).
- **Palace SoD Skip (`910`, EET):** Optional choice on first palace bedroom arrival
  (`110`, `140`, `150`, `160`, `EET_end`); carries inventory through normal EET import
  and grants `250,000 XP` once in BG2.
- **Append-only updates (`176`, `235`, `258`, `291`):** Only needed when upgrading older
  installed versions; fresh `v0.6.17` installations already include every correction.

### Compatibility & We Overwrite Policy

- **We Overwrite:** As of `v0.6.17`, every component writes its decided result directly
  over edited values, missing dialogue states, or other mods' changes
  (`chriz-sod-remix/lib/overwrite.tpa`). Only the game type and declared prerequisite
  components remain required.
- **Mod interoperability:** Timer names resolve dynamically from `GTIMES.IDS` (e.g., Dark
  Tidings), Tweaks Anthology's ally fog clearing (`cdtweaks` `3500`) stays intact on
  bridge elementals, and `290` adapts victory remarks added by mods such as Sirene NPC.
- **Live-save boundaries & uninstall:** `.are`, `.bcs`, and `.dlg` edits apply when
  entering areas not yet saved in your campaign. Fully reversible via WeiDU backups in
  `weidu_external/backup/chriz-sod-remix`.

### Further Documentation & Verification

- [Component Notes](chriz-sod-remix/README.md) · [Complete 49-Component Inventory](docs/00-feature-inventory.md) · [Changelog](CHANGELOG.md)
- CI (`.github/workflows/ci.yml`) runs WeiDU 249 `--parse-check` across the TP2 and all
  `.tpa` libraries alongside Python unit and research-script suites
  (`python -m unittest discover -s tests`).

### Credits

- **[Sword Coast Stratagems](https://github.com/Gibberlings3/SwordCoastStratagems)**
  by DavidW — Boareskyr Bridge mage defensive priority and manual sequencer
  inspirations (`v35.21`).
- **Beamdog** — *Baldur's Gate: Siege of Dragonspear* base game and scenery assets.
- **[WeiDU](https://github.com/WeiDUorg/weidu/tree/v249.00)** (`v249.00`) — installer runtime.

## License

First-party code, WeiDU scripts, and documentation are licensed under the
**[MIT License](LICENSE)** (`Copyright (c) 2026 Christopher Hermann`).

Third-party notices and license boundaries are documented in
**[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)**, covering:
- The bundled **WeiDU 249.00** executable (GNU GPL v2, shipped as `WEIDU-COPYING.txt`).
- **Sword Coast Stratagems 35.21** defensive-priority inspirations (`chriz-sod-remix/lib/comp256_ai.tpa`).
- Edited **SoD bridge scenery tiles** (`chriz-sod-remix/art/bridge/README.md`).
