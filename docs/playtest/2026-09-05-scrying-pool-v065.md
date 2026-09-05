# v0.6.5 scrying-pool acceptance — 2026-09-05

**Result:** Christopher accepted the focused in-game test and explicitly confirmed the
save/reload check. This closes the focused runtime gate for the no-Aura component-120/225
repair; it does not establish full-playthrough or standalone-game compatibility.

## Tested build and isolation

- Code commit: `3b21d6f0ed023551ceaa209479f31d8264b7ef3f`.
- Candidate: `chriz-sod-remix-v0.6.5.zip`, SHA-256
  `1113b9e6fd0f2929fce187a1a693b253b30b34da80c48850c9741333847d891e`.
- Game: `C:\Users\chris\Games\CEBG-SOD120-v065-test\game`.
- Separate profile: `CEBG SoD120 v065 Test`; no stream saves were imported for staging.
- Only missing components 120/225 were tail-installed onto a disposable copy of the
  frozen collection r3 game, retaining component 220 and all 344 previous WeiDU entries.
- This copy lacks the remaining collection tail. Component 290 is outside this test.
- The user performed gameplay. No agent launched a game for this acceptance check.

## Automated evidence already completed

WeiDU parsing passed for the TP2 and all 33 TPA files; all 11 tests passed. The fresh
120/225 installation completed with exit 0 and no warnings or errors. The semantic
verifier on the newly patched resources reported `SUMMARY: 0 failure(s)`.

The installed-resource checks cover the no-Aura four-state picker, three reachable
scepters, both container-held Essences, the still-cut wight, two-Essence payment,
once-first completion flag, six 1,000-XP slot actions, retained 3,000 party-total reward,
and no reachable old dialogue/cinematic/travel/spawn route.

## Runtime evidence

Christopher supplied two screenshots from the focused test. They show:

- the scepter insertion sequence and its 3,000 party-total XP award;
- a 1,000 quest-XP award to the tested character;
- the exact approved abstract Caelar omen, followed by the dormant-pool text;
- another dormant response after adding another Essence, without a repeated visible
  XP award.

Christopher also explicitly confirmed completing the save/reload check and accepted the
result. The screenshot sequence does not independently identify the reload boundary.

## Evidence limits and release handoff

Items were console-staged; natural acquisition of all five items remains for a later
playthrough. One-Essence refusal, exact inventory consumption, and every occupied party
slot's XP were not independently shown in the screenshots. These are covered by the
installed-resource checks, rather than a claim of separately observed runtime proof.

Aura compatibility is not required by the user. Standalone BG:EE+SoD and completion of
the entire curated collection were not tested here.

The acceptance record changes documentation only; the tested mod code is unchanged.
Publication and collection pinning remain separate from this gameplay approval. Keep the
tested RC intact as evidence; refresh the packaged feature inventory when preparing the
final release archive.
