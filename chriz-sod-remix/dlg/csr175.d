// csr175.d — component 175: the prologue XP ledger. Liia's return-beat close
// (csrcele state 2 "korlret2", "Then the Fist will see to what remains...")
// pays 22,000 XP per character on every difficulty (user 2026-09-08;
// corrected basis: docs/research/23-prologue-xp-recount.md).
// Delivered as AddXPObject(Player1..6) — Beamdog's own
// chapter-award pattern, exact per character at any party size; the original
// single AddexperienceParty(24000) was WRONG (the engine DIVIDES that action
// among the party — user-verified in-game 2026-07-12 — so it paid ~4,000/char).
// Full ACTION replacement so the award runs BEFORE DestroySelf() (actions
// queued after DestroySelf on the speaker are dropped); the CSR_KORL_RET 1->2
// flip makes the state unrepeatable, so the award fires exactly once.
// comp175.tpa verifies state 2 is the expected line first.
ALTER_TRANS ~csrcele~ BEGIN 2 END BEGIN 0 END BEGIN
  ACTION ~SetGlobal("CSR_KORL_RET","GLOBAL",2) AddXPObject(Player1,22000) AddXPObject(Player2,22000) AddXPObject(Player3,22000) AddXPObject(Player4,22000) AddXPObject(Player5,22000) AddXPObject(Player6,22000) DestroySelf()~
END
