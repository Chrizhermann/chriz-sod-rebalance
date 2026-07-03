# 09 — The SoD Chapter Rest-Dreams (full content documentation)

**Status:** research complete (verified against the live install, 2026-07-03).
**Purpose:** the remix **skips** these four dreams (user decision — "very very bad quality").
This doc preserves their complete content so a rewritten reintroduction stays possible later.
All quotes are exact `dialog.tlk` text; EET strrefs = vanilla + 200000; `[BD…]` = voiced line.

## System mechanics (verified)

- **Launcher:** `PLAYER1D.BCS` (the engine's on-rest dream script) carries four EET-appended
  SoD blocks (decompile lines 157–243; template `EET/lib/bg2_BCS.tph:1619–1696`). Block N
  fires on rest when `chapter ≥ 7+N && chapter < 13`, `bd_ddd == N−1`, and the 12h
  `bd_dream_timer` is expired. Action: `bd_ddd = N`, advance time 8h, apply `bdrejuve` to all
  six party slots, set the timer, launch cutscene `bddddNa`.
- **The dream replaces the rest** — and it's a *better* rest: `BDREJUVE.SPL` = 100% heal,
  full spell re-memorization (op316), restoration/cure-deafness/feeblemind/petrification,
  dispel. No rest-ambush roll can occur on a dream night. Closing message: *"You have rested
  for 8 hours."* (#270487).
- **Stage:** `BD0072`, a dedicated actor-less collage area with seven backdrop "doors"
  (Bhaal_Temple, Candlekeep, Tradeways, Lavish_Bedroom, Humble_Bedroom, City_Streets01/02).
  Dream 2's second half instead plays in the **real** `BD0103` (Imoen's palace sickroom).
- **Common skeleton:** party hidden (`bdhide`) and moved to the stage → scene dialogue →
  the dream figure `Polymorph(SLAYER)`, receives the glowing **"Ring"** (`bdskiedr.itm`,
  cosmetic glow — the visual thread pointing at the finale's Slayer-framed Skie murder) →
  staged 0-damage kill of the PC (`ApplyDamage(Player1,0)` + death animation) → wake, cleanup,
  rest message. Dreams are breakable cutscenes (`CUTSKIP.BCS` responses #46–49).
- **Player choices have zero consequences** — every reply branch converges within one node;
  no reply carries actions or variables. Pure flavor.
- **No persistent effects:** no XP, no items (the Ring dies with the dream actor), no global
  consumed outside the dream chain (verified exhaustively: `bd_ddd`/`bd_dream_timer` exist
  ONLY in `PLAYER1D.BCS`; the `bd_dddN_scene` locals only inside the chain).

## Dream 1 — chapter 8+, "Sarevok" (`BDDDD1A/1B/1C`)

Bhaal_Temple backdrop (Sarevok's death site). Sarevok's corpse is raised (`ICRAISEI` VFX),
he rises and approaches; the Hooded Man watches.

> #267200 *"You did not think me truly dead, did you?"* · #267201 *"We've a bond between us,
> you and I. A connection even the sharpest blade cannot sever. A bond forged in blood,
> hatred, death."* · #267202 *"I held the Sword Coast by its throat. It wriggled and squealed
> in my grip, and then... YOU."* · #267203 *"I should have killed you, as I had so many
> others. But something stayed my hand, a weakness I had never known before."*

Scene shift to a Baldur's Gate street (City_Streets01). Gender variant: #267204 *"Are we one
and the same, my brother? One soul in two bodies, born of the Lord of Murder?"* (male) /
#234895 (*"…my sister…"*, female). Then #267205 *"We will never end, you and I. Even in
death."* — three replies (fight him again / had my fill of vengeance / return whence you
came), answered by the Hooded Man (#267209 *"A cycle continued. Intriguing."* / #267210
*"Have you truly? In the end, vengeance is all you will have left."* / #267211 *"You
understood none of this, did you?"*), converging on #267212 *"Do you see now?"* →
Sarevok-Slayer kills the PC.

## Dream 2 — chapter 9+, "Imoen" (`BDDDD2A/2B/2C`)

Candlekeep backdrop. Child-Imoen (live Imoen polymorph-copied, then `Polymorph(GIRL)`),
Gorion standing by, and the PC's own child-double (`BDSERV`). Known vanilla bug (verified,
present in vanilla): for **female** PCs the script re-polymorphs Imoen instead of the double,
so the child-self appears as an adult clone.

> #267213 *"Books for bones, words for blood. Candlekeep. Our home. It wasn't your fault we
> had to leave."* · #267214 *"Only... it was. Wasn't it?"* · #267215 *"You were all I had
> left in the world. And you abandoned me. I've got nothing left now. Nothing."*

Scene shift to the **real** `BD0103` sickroom (dream-Imoen placed at the real bdimoen's spot;
dream theme `BDDRM1.mus`; the PC is slowed and trudges to her bed).

> #267216 *"I'm tired, <CHARNAME>. I'm so tired. Please."* · #267220 *"I need you to do it.
> For me."* — Hooded Man: #267221 *"Do as she asks. After everything you have done,
> everything you have put her through, you owe her this."* Three replies (I will, for you /
> Never! / *"I will do it, and happily. I never liked her, anyway."*), answered #267226 *"A
> wise choice."* / #267225 *"Her end may not come at your hand, but it will come."* / #267227
> *"Curious."* — converging on #267228 *"How do you feel?"*

→ Imoen-Slayer kills the PC. No alive/dead variant; she appears sick-but-alive regardless.

## Dream 3 — chapter 10+, "Corwin" (`BDDDD3A/3B/3C`)

Humble_Bedroom backdrop: Corwin tells her daughter Rohma a bedtime story.

> Corwin #267229 *"The queen does not relent. 'You must surrender the crown,' she says, 'or
> the worst will come.'"* · Rohma #267230 *"Does she have to give up the crown? Why can't she
> just stay a princess?"* · Corwin #267231 *"Duty. Duty compels us, above all else."*

Rohma vanishes in a burst of light (`SPFDAWN`); Corwin turns to the PC; Hooded Man: #267232
*"Do you see, <CHARNAME>? Do you understand now?"* Variant: if the real Corwin is **dead**,
dream-Corwin says #267233 *"It's your turn. Do your duty."* with three replies (refuse /
farewell / what is my duty?) answered #267238 *"You cannot refuse. It is far too late for
that."* / #267239 *"There is much that can yet be done."* / #267240 *"Understanding is not
required. You are compelled."*; if alive: #267237 *"My duty is done. The consequences are all
that remain."* (no choices). Converge on #267241 *"Let us try this one more time."* →
Corwin-Slayer kills the PC.

## Dream 4 — chapter 11+, "Caelar" (`BDDDD4A/4B/4C`)

Lavish_Bedroom backdrop: **young** Caelar (`Polymorph(GIRL)`) with her uncle **Aun Argent**.

> #267242 *"So much death. And to what end?"* · #267243 *"I had to make it right. I had to
> save them—save him. Whatever the cost."*

Scene shift to a Trade Way road; adult Caelar and the Hooded Man: #267244 *"There can be no
victory without sacrifice. What are you prepared to lose, <CHARNAME>? Have you anything left
to surrender?"* Three replies (whatever serves a righteous cause / there must be another way
/ I'll die before I lose more), answered #267248 *"…Only in the crucible can the truth be
known."* / #267250 *"You can walk but a single path. Dire consequences await those who try to
find another way. Believe me; I speak from experience."* / #267249 *"Then fight and claw your
way through life. Cling to the past, like a child does its mother's teat."* — converging on
#267251 *"You need not embrace your fate. But ultimately, you will accept it. You can do
nothing else."* → Caelar-Slayer kills the PC.

## Cut content: the orphaned alternate dream 1 (`BDDDD1AA/1AB/1AC`)

A "guilt ghosts" version of dream 1 exists fully compiled but is **unreachable on any
install** (nothing launches it — verified against live override AND vanilla BG:EE+SoD biffs):
City_Streets02, three unvoiced ghosts confront the PC — #267287 *"My son was a mercenary,
hired by the Iron Throne. You never knew his name, but you killed him all the same."* ·
#267288 *"You could have saved me. …My blood is on your hands."* · #267289 *"My momma's
gone."* — then Sarevok appears and the Slayer kill plays. Its dialogue states still live in
`BDCCIRE.dlg` states 4–10. Raw material for a possible rewrite.

## What skipping costs (mechanically)

Exactly four guaranteed, ambush-proof full restores (100% heal + full re-memorization +
cures) at those rests — nothing else. Those four rests become normal engine rests subject to
the (now 5×-reduced) ambush roll. No XP, items, abilities, or story flags are lost.

## Skip mechanism → design in `docs/design/wave1/03-hooded-man-removal.md`
`bd_ddd=4` pre-set via an EXTEND_TOP guard block on the master script; verified safe
(zero external consumers). The endgame celebration dream (`BDCUT60`, BD4100) is a separate,
dialog-launched system on its own locals — unaffected.
