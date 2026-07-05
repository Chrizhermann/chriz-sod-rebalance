# Chapter Pass — Prologue (Korlasz dungeon + Baldur's Gate city opening)

**Status: DRAFT for sparring (2026-07-05). Nothing here is signed off yet.**
Research basis: `docs/research/10a-10d` (item inventory, skip plumbing, staging map,
Korlasz/SCS pattern) — all verified against the live install. Builds on installed Wave-1
components 110 (keep companions) and 120 (hooded-man removal, which already touched BD0103).

Sections are tagged **DECIDED** (user's ask, feasibility confirmed), **PROPOSED** (my
suggestion, invited), **OPEN** (user decision needed).

---

## 1. Remove the Korlasz dungeon run — DECIDED (user), mechanism verified

**Spine = Beamdog's own debug skip** (`BDDEBUG.baf:151-160`): `bd_plot=50`,
`bd_npc_camp_chapter=1`, `StartCutSceneEx("bdcut00z",FALSE)` — everything downstream
self-assembles from BD0103's `BD_PLOT<51` blocks. We never reimplement `bdcut00z` (it owns
the gold impound `BD_TAKEN_GOLD`, `BD_SAFEHOUSE_DONE`, and the move to BD0103).

**Shape: "instant exit", not a start-area change.** Party still lands in BD0120 for 2-3
invisible script passes (no player control): all bootstrap runs for free — EET/fresh
new-game blocks (Bhaalspawn abilities, K#PLOT strip, 30k gold, gear script), the Key Ring
(`BDKEYR`, granted nowhere else), the Imoen import-strip, the BG1-journal cleanup, and
**BDINTRO's companion wiring blocks 1-539 kept intact** (SoD dialog/AI rewiring + the
C0Aura/L#BRIST mod hooks — free compatibility). We patch only BDINTRO's staging + walk-in
blocks (541-688): set `chapter=7`, `DREAM=7`, `bd_plot=50`, sprite flags, bdplayer AI, then
launch `bdcut00z`. One implementation covers EET import AND fresh SoD start.
**Never touch `SODSTRTA.2DA`** — a start-area change silently skips every mod-patched
bootstrap block.

**Korlasz default state:** `BD_KORLASZ_SURRENDER=1` + journal chain (256379 QUEST →
259573 QUEST_DONE → 269028 QUEST_DONE). Canon fiction, delivered by text/Liia: *the Flaming
Fist cleared the tomb; Korlasz surrendered and was taken to the palace* — which is exactly
what vanilla supports: `BD0116.baf:1-13` spawns her in the **palace-basement jail cell**
whenever she isn't dead, and her own line (strref 245646) says she was "taken to the palace
and not to the jail". Surrender-flag also keeps 12 companion banters + the BD7300 Ephrik
spawn coherent.

**Known losses to budget (XP ledger):** dungeon kill XP, the surrender cascade
(≈ kill-everything XP + 1000/member), and the 30,000 party XP from Imoen's wrap-up dialog
(BDIMOEN state 32). Re-attach: see §2 fight rewards + a completion award at the celebration
beat. Exact numbers in the ledger once the fight design is locked.

## 2. The Korlasz fight — PROPOSED (user asked for location/justification ideas)

**K1 (recommended): the jailbreak.** Vanilla already stages a Korlasz palace rematch in
**BD0116 (palace basement: treasury + wine cellar + jail cells)**: the proximity region
`TrapBDKorlasz` spans the whole cellar corridor → `BD_KORLAS_FREED=1` → she self-buffs,
kills a guard, opens her cell, forced dialog ("Now let us finish this!") → hostile; journals
261626/261627 wired. The player crosses that corridor anyway: **all party gold is impounded
at the dungeon exit** and Ophyllis/the treasury are down there — vanilla funnels you in.

So: *why is she in the prison?* Captured alive (canon). *Why do you fight her there?* She
breaks out as you come down for your gold — her surviving loyalists smuggled her gear in and
staged a rescue. The user's prison instinct is vanilla-canon; we upgrade the existing
rematch from "one under-equipped mage" to the real boss fight:

- **Her party (from the verified dungeon roster, all with real gear/roles):** BDKORME9
  (cleric of Bhaal, plate/shield, full priest book), BDSHIS08 (gnome illusionist F/M),
  BDKORME8 (wizard-slayer), 2× BDSHIS10 (elven archers), BDSHKFAM (her dust-mephit
  familiar). Difficulty-gated adds on HARD/HARDEST: elite undead (BDSKGR03/BDUNSLGU-tier)
  "raised from the tomb's dead". Reuse the `BDSHKFIN` sync-script pattern (neutral until she
  turns, then group-Enemy).
- **Korlasz herself:** restore her intended consumables (Minor Globe + Prot. Elemental
  scrolls, Vocalize, Potion of Clarity) — **revives four dead AI blocks in her vanilla
  brain** (on this install she has literally no items; SCS's DW#RND03 token is inert), works
  with or without SCS. Optionally, with-SCS: assign `dw#mg13` as her brain (verified: its
  prebuff set Shield/Mirror Image/Haste/Stoneskin is entirely inside her spellbook), guarded
  `FILE_EXISTS_IN_GAME ~dw#mg13.bcs~`, vanilla `BDSHKORL` as fallback. Non-casters get SCS
  generic brains (`dw1mel*/dw1ran*` + `dw#ptn*` potions) when present, `BDENSHTV` otherwise.
- **Scaling:** explicit `Difficulty()` composition branches (the SoD-native mechanism —
  BD0130's own guard waves do 12/9/8/3). The slider does NOT buff placed creatures; Insane
  only doubles enemy damage. LoB is a separate toggle we ignore.
- **Surrender option preserved:** keep her HP-threshold parley (maybe lower than vanilla's
  71%) → spare-or-kill choice as in the tomb, same globals (`BD_KORLASZ_SURRENDER` stays 1,
  `BD_SPAWN_KORLASZ=2` on kill) so zero downstream breakage either way.

**Alternative K2:** stage the fight as the palace night attack itself (merge with §4's
assassination). Rejected as primary because the night assassins are *crusade* plot (the
parchment BDMISC56, the sun-brand, Eltan's investigation) — mixing Korlasz in muddles the
new antagonist's introduction. Kept here as an option if the user prefers one big night.

**Fight staging alternatives surveyed** (10c §5): BD0118 (pristine unused palace-hall
clone — best free arena for any future set-piece), BD0100 upper hall, BD0102 great hall
(contested), BD0104 FF jail (contradicts her canon line). K1/BD0116 wins on plumbing + fiction.

## 3. Item re-homing — PROPOSED mechanics, item list verified (10a)

Two delivery channels:

1. **Fight loot (K1):** Korlasz's full kit — Cloak of Protection +1, Knave's Robe, Bracers
   AC6, Quarterstaff +1, Korlasz's Key — plus her lieutenants' gear. This is loot vanilla
   *denies* you on the surrender path; the jailbreak earns it.
2. **Evidence chest** ("recovered from the tomb by the Flaming Fist"), placed in the
   treasury room or the guest suite: **BDSHSARE Page from Sarevok's Notes (P1 — feeds the
   chapter-10 masks quest via `BD_SAREVOK_SECRET`; must survive)**, BDSHBHR Bhaal Research
   (its quest dies with the Imoen plot → keeps as lore paper), **BDSW2H03 Sword of Ruin +2**,
   **BDHELM10 Helm of Unwavering Purpose**, Korlasz's Journal + Orders (lore), BAG02I gem
   bag, the 3,000 gp jackpot + tomb cash (≈4,100 gp total, folded in as a Fist "recovered
   valuables" payout). Wands of Fire/Heavens: OPEN (both purchasable elsewhere; my lean:
   include one, not both).

Dies with the dungeon unless ported (OPEN, my lean in parens): Ammon's Cobalt-Moss quest
(cut — his wand is minor), Restless Spirit staff/headpiece quest + gem payout (cut), torch/
brazier puzzle (cut), Porios subplot (cut; his unique Cloak of Minor Arcana → evidence
chest?), BD_SAREVOK_SWORD rumor flavor (cut, dungeon-internal).

The `BD_SAREVOK_SECRET` flag: setting it belonged to looting the note in BD0130 — re-home
the *setter* onto the chest-loot or keep it on item-acquisition (verify at implementation).

## 4. Palace night: assassination without Imoen — DECIDED (user: no Imoen wake-up, no
attack on her, no poisoning), patch surface verified (10c §2)

The night attack itself is **load-bearing crusade plot** and stays (inciting incident:
parchment BDMISC56 on bdgass2, sun-brand, war council, Corwin intro). The complete
`Dead("bdgass1..4")` consumer list is known (6 sites) — the fight survives Imoen's removal:

- Remove the Imoen wake-up + dagger-practice scene: the trigger region at [666,587] launches
  the assassin spawn directly (or a wounded Fist guard bursts in) instead of BDCUT02's
  Imoen beats.
- Assassins target the party (BDGASS.baf's IMOEN2 priority becomes moot with no Imoen
  actor); no `BD_IMOEN_DOWN`, no `bdgassa1` poison, no bedside scene.
- `bd_001_plot` still marches 2→3→6→7→8→9: Corwin ally spawn, Liia arrival (now: summoned by
  the alarm, not healing anyone), war council in BD0102 as vanilla.
- The **morning MDD007 bedside block dies entirely** (component 120 already cut bdireni out
  of it; this pass removes the rest — sick Imoen, farewell).
- **Skie's 3 a.m. scene stays** (it's her SoD setup and the user wants her playable later)
  — re-gate its trigger off `BD_MDD007=2` onto plot-54 alone.
- Keep `BDMISC56` lootable on an assassin (Eltan's "I found one just like it" reply).

## 5. Imoen: keep / recruit — DECIDED goals (user), implementation PROPOSED

Verified constraint: three palace CREs share death variable `IMOEN2`, and BD0103's poison
plot damages/destroys/duplicates her — "never leaves the party" via brute force means
re-authoring every `IMOEN2` reference (against removal-over-rewriting). But **this pass
deletes most of those references anyway** (§4), which unlocks the clean version:

- **Was in party (EET import):** instead of the vanilla strip's `DestroySelf`
  (BD0120.baf:651-663), patch to `LeaveParty()` + `MoveGlobal` her **imported instance** to
  the BD0103 bedroom — she keeps her exact imported build, XP, and (skipping the
  `TakeCreatureItems`) her gear. The pre-placed scene-Imoen actor is removed/never fires.
  You wake up; she's standing in the room; one dialog line and she rejoins. Net effect =
  "you keep Imoen", without DV surgery.
- **Alive but not in party:** the pre-placed BD0103 actor (already at (221,459) — literally
  the first room, the bedroom you wake in) gets a new short join dialog instead of the
  sickness plot. Vanilla places her unconditionally (canon: she survived BG1), and BG1-death
  detection on EET is unreliable — **PROPOSED: unconditional presence** (matches canon and
  every vanilla assumption). OPEN if the user insists on death-tracking.
- Joinable CRE for the non-import case: BDIMOEN-based, leveled to the SoD baseline
  (fresh-start XP floor is 64,000 per SODSTRTA), BG1 gear tier; `Imoen_equipment` container
  default stock stays as her "room supplies".
- Component 110 note: Imoen was explicitly out of scope there; this is her component.

## 6. Celebration-first opening — DECIDED direction (user), staging PROPOSED

Vanilla's own TextScreen (DPALACE, strref 270019) already narrates: *"you are fêted by the
rulers of Baldur's Gate… A tenday after Korlasz's defeat…"* — the celebration exists in
prose; we put it on screen. Proposed flow after the invisible skip (§1):

1. **Arrival = celebration evening in the BD0102 great hall**: dukes assembled, short
   praise scene built from *existing* duke lines (Liia 234300 "The hero of Baldur's Gate…",
   Belt 264733/264741, the plot-56 blessing chain), crowd/ambience kit from BD0101/BD0021
   (412/385 placed crowd actors, cheer sound AMBDLCHE). No fireworks VFX exists in SoD —
   skip literal fireworks (OPEN: port one later).
2. **Free city roam before any obligation** — "run around and collect things": Three Old
   Kegs, Elfsong (Garrick performing; Coran+Safana upstairs), Sorcerous Sundries + auction,
   FF HQ (Tiax +1000 XP, refugee quests), palace basement (treasury/Ophyllis → **triggers
   the K1 Korlasz jailbreak**, evidence chest §3). Implementation must verify chapter-7 city
   content keys on `chapter`, not `bd_plot>=52` (spot-checks say chapter; one sweep needed).
3. **When the player goes to bed** in the guest suite → TextScreen tenday → night
   assassination (§4) → war council → goodnight → Skie scene → send-off parade → chapter 8.
   From the council on, vanilla runs untouched (bd_plot 52→65 chain, BDSCHAEL-driven).

This inverts vanilla's "dungeon→bed→attack→council→roam→parade" into
"celebrate→roam→attack→council→parade" — the attack lands mid-comfort, which is better
drama and exactly the relaxed on-ramp the user asked for.

## 7. XP ledger entry (prologue) — numbers TBD after fight design lock
Removed: dungeon kills/quests (incl. 30k party wrap-up, surrender cascade, Tiax-style side
XP stays since city content survives). Added: K1 fight (kills + quest award), celebration/
completion award, evidence-chest quest journal. Calibrate per 05-xp-ledger policy (user's
real endpoint 700-750k), after playtest.

## 8. Compatibility notes
- All changes are tail-mod patches on BD0120/BDINTRO/BD0103/BD0116 + new .d/.cre/.are
  containers; no engine 2DAs, no SODSTRTA/CAMPAIGN edits, K#/mod blocks preserved verbatim.
- Component 120 already edited BD0103 — this pass's patterns must match the *patched* text
  (or be robust to both orders); enforce install order 120 → prologue component.
- SCS integration is detect-and-adapt (FILE_EXISTS_IN_GAME guards + vanilla fallback);
  works on pure vanilla, SCS, SR, EET, standalone SoD.
- Everything ships as separate components: dungeon-skip, Korlasz fight, night-attack rework,
  Imoen, celebration — individually selectable, with the fight/celebration requiring the skip.

## OPEN decisions for the user
1. K1 jailbreak as THE Korlasz fight (vs K2 merge into the night attack)?
2. Night assassination beat: keep (Imoen-free, recommended) or remove wholesale?
3. Evidence-chest contents: the P1/P2 list as proposed? Wands in or out? Porios's cloak?
4. Ammon quest, Restless Spirit quest, torch puzzle: cut (my lean) or port?
5. Imoen unconditional in palace (recommended) vs BG1-death detection attempt?
6. Celebration scene: text-light (praise lines + crowd, ~1-2 min) or a bigger staged scene?
7. Surrender parley threshold for Korlasz round 2 (keep 71% / lower / none)?
