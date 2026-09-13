# Shadow Aspect: deferred native check and Mislead correction

**Stopped by the user on September 13. The game is closed.** No further live
actions or tests are authorized by this record alone. The user subsequently
deprioritized the summon detail and native Shadow Aspect testing: this is **not
a release blocker or the mandatory next test**. Current priority is release
preparation and removing the repeated Mislead behavior. Keep the unfinished
evidence below for an optional future check.

## What this test was for

Component265 removes the two banned Shadowed Soul (`BDSHSOUL`) creations from
Shadow Aspect's Insane summon block. Its two ordinary Shadows (`BDSHAD04`) remain.
The unfinished native check was one completed summon cycle showing ordinary
Shadows without Shadowed Souls. The user no longer considers this detail worth
holding up the release. They want the entire encounter made trivial eventually;
that broader change is deferred, with its exact treatment still undecided.

## Accepted and outstanding results

- Bridge combat, prompt Bence arrival, save/reload and onward crossing passed.
- Assassin spellcasting/buff persistence passed with Edwin; the user accepted
  that limited sample and declined more assassin testing or transfer recovery.
- Guardian removal passed: fresh BD5110's BDUNSLGU sprite is inactive; ordinary
  shadows are active. Do not repeat this merely because its inactive sprite
  still appears in the engine's area object list.
- Shadow Aspect summon check is **unfinished**. The user described the fight as
  buggy and the unbuffed setup as capable of permanently killing someone within
  seconds. Do not claim its summons or balance passed.

## Mislead finding and current correction

Offline inspection of the current Combined `BDASHIRU.BCS` confirms that Insane
Mislead can recur whenever the actor is not invisible and `bd_invis` has expired.
It sets `bd_invis` to TWO_ROUNDS and uses `ApplySpell(Myself,WIZARD_MISLEAD)`.
There is no usage cap, memorized-copy requirement or enemy-sighting condition in
that block. The ordinary casting guard `bd_cast` does not govern this action.
Component265 only removes the two Shadowed Soul creation actions; it preserves
this Mislead behavior. Default-selected component266 is **implemented and
offline-verified** to allow Insane Mislead only once, removing the repeat chain.
All 13 focused tests passed, including public install and disposable restore;
see the [candidate report](../releases/v0.6.9.md). Native verification is
deferred; do not label the correction as a completed live pass or confuse it
with the eventual broader encounter simplification.

Installed script SHA256:
`462ca1008a0fca1176bd26ce01ca2558fdc1d7908c7502d7dcc0444a3edaae6c`.
Decompiled evidence is retained with the staging evidence below.

## Optional future restart

Use **CSR TEST 18 — Extra Challenge bridge won** (save949), whose complete folder
is under `C:/Users/chris/OneDrive/Documents/CEBG Combined Playtest 2026-09-08 - c2a832a75741/save/`.
No named Shadow Aspect checkpoint was saved. The game was closed after the
unsaved staged entry, so do not say the party is still paused in that room.
Save949 had neither BD5110 nor BD7230 cached and restores the full party.

Before any future engagement, provide a healed, rested, buffed party and a safe
preparation point outside immediate enemy reach. The previous inside-room
placement was too close for unbuffed preparation; do not repeat it. Native
`Rest()` restored spell availability but did not heal Khalid, who still had42HP.
Verify actual healing and protections rather than treating a rest command as
proof. A protected setup may be appropriate for this mechanical summon sample;
it would not establish encounter balance.

Use remote console only for necessary preparation. The user controls actual
combat and the game UI. Do not use Computer Use, replay the campaign, repair the
unrelated soundset text, or manipulate unrelated story/world-map progression.
The staged Chapter7 save's city world-map context prevented normal travel; direct
area staging leaves the travel launcher untested.

Staging helpers/evidence:
`C:/Users/chris/CEBG-Tests/Combined-20260908/filler-evidence-20260913/`.
Every BCS action in a remote response must be on its own line. Validate parsed
action IDs and verify all six arrivals before declaring a checkpoint ready.
Do not rerun guarded helpers blindly or reuse the abandoned split-party state.
