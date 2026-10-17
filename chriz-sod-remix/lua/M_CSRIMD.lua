-- chriz-sod-remix component 294: Imoen dual-classes at her SoD thief level.
-- Driven by BALDUR.BCS (EEex_LuaAction) after EET's carried-Imoen arrival in
-- AR0602. No script action or opcode can set the CRE original-class flag, so
-- the conversion writes it directly. Everything else stays native: ChangeClass
-- changes the class, SoA's join ladder (BD_JOINXP in IMOEN.BCS) raises the new
-- mage XP, and the spellbook is taught with the engine's learn-spell effect.
--
-- Progress in the GLOBAL CSR_IMSOA_DUAL (set here, read by BALDUR.BCS):
--   2 converted, 3 teaching spells (BALDUR.BCS retries), 4 finished,
--   5 finished but some spells could not be taught, 7 not applicable
--   (absent, or not a pure single-class thief), 8 error (logged).

local RESULT = "CSR_IMSOA_DUAL"
local TRIES = "CSR_IMSOA_TRIES"
local MAX_TRIES = 10
local THIEF, MAGE_THIEF = 4, 13
local ORIGINAL_CLASS_MASK = 0x1F8 -- CRE flags: original fighter ... ranger
local ORIGINAL_THIEF_BIT = 6      -- 0x40
local STAT_INT = 38               -- STATS.IDS
-- BG2 Imoen's known wizard spells; the installer fills this list from the
-- installed IMOEN10.CRE (only resources that exist in the game).
local SPELLS = { --[[CSR292_SPELLS]] }
local lastError

local function findImoen()
    local anchor = EEex_Sprite_GetInPortrait(0)
    assert(anchor, "no protagonist to resolve IMOEN2 from")
    local object = EEex_Object_EvalStringAsAIBase('"IMOEN2"', anchor)
    if EEex_GameObject_IsSprite(object, false) then return object end
    return nil
end

local function convert()
    local sprite = findImoen()
    if not sprite then return 7 end
    local base = sprite.m_baseStats
    -- IMOEN10 from EET's fresh path, an Imoen the player already dual-classed,
    -- and every multiclass are left exactly as they are.
    if sprite.m_typeAI.m_Class ~= THIEF or EEex_BAnd(base.m_flags, ORIGINAL_CLASS_MASK) ~= 0 then
        return 7
    end
    local thiefLevel = base.m_level1
    assert(thiefLevel >= 1 and thiefLevel <= 50, "unexpected thief level " .. tostring(thiefLevel))

    EEex_Action_ExecuteResponseStringOnAIBaseInstantly("ChangeClass(Myself,MAGE_THIEF)", sprite)
    assert(sprite.m_typeAI.m_Class == MAGE_THIEF, "ChangeClass did not apply")
    -- MAGE_THIEF keeps its class levels in CLASS.IDS name order: mage, thief.
    base.m_level1 = 1
    base.m_level2 = thiefLevel
    base.m_flags = EEex_SetBit(base.m_flags, ORIGINAL_THIEF_BIT)
    -- A dual-class's XP is its new class's XP: mage starts at 0, and SoA's join
    -- ladder raises it once she is in the party. Re-arm the ladder in case it
    -- already ran (or still holds a SoD value) before this conversion.
    base.m_xp = 0
    EEex_Sprite_SetLocalInt(sprite, "BD_JOINXP", 0)
    EEex_GameState_SetGlobalInt(TRIES, 0)
    return 2
end

local function missingSpells(sprite)
    local known = {}
    for _, _, resref in EEex_Sprite_GetKnownMageSpellsIterator(sprite, 1, 9) do
        known[string.upper(resref)] = true
    end
    local missing = {}
    for _, resref in ipairs(SPELLS) do
        if not known[resref] then table.insert(missing, resref) end
    end
    return missing
end

-- Learning rolls against Intelligence; at 25 it cannot fail. Raise it for a
-- few seconds, teach on a later pass, then verify. Returns nil to retry.
local function teach()
    local sprite = findImoen()
    assert(sprite, "IMOEN2 disappeared before her spells were taught")
    local missing = missingSpells(sprite)
    if #missing == 0 then return 4 end
    local tries = EEex_GameState_GetGlobalInt(TRIES) + 1
    EEex_GameState_SetGlobalInt(TRIES, tries)
    if tries > MAX_TRIES then
        print("[CSR Imoen SoA] could not teach: " .. table.concat(missing, ", "))
        return 5
    end
    if EEex_Sprite_GetStat(sprite, STAT_INT) < 25 then
        sprite:applyEffect({
            effectID = 19, effectAmount = 25, dwFlags = 1, -- Intelligence: set
            durationType = 0, duration = 12, sourceID = sprite.m_id,
        })
        return nil
    end
    for _, resref in ipairs(missing) do
        sprite:applyEffect({
            effectID = 147, res = resref, durationType = 1, sourceID = sprite.m_id,
        })
    end
    return nil
end

local function run(step)
    local ok, value = pcall(step)
    if not ok then
        local err = tostring(value)
        if err ~= lastError then print("[CSR Imoen SoA] " .. err) end
        lastError = err
        value = 8
    end
    if value then EEex_GameState_SetGlobalInt(RESULT, value) end
    -- No return value: EEex_LuaAction treats a returned value as the action status.
end

function CSR_ImoenSoA_Dual() run(convert) end
function CSR_ImoenSoA_Learn() run(teach) end
