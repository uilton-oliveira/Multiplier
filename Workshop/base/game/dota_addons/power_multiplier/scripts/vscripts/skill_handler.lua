--[[
    Skill Handler Library for Generating Random Skills and Replacing current Skills
]]

-- Current object to export
local skillHandler = {}

local skillsList = {}
local ultimatesList = {}
local unique = {}

local precachedSkills = {}
local precachedUltimates = {}

-- Contains all skills to be used by OMG
local skillsListKV = LoadKeyValues("scripts/kv/skillsList.kv")
local ultimatesListKV = LoadKeyValues("scripts/kv/ultimatesList.kv")
local subSkills = LoadKeyValues("scripts/kv/subSkills.kv")

local npcHeroesKV = LoadKeyValues("scripts/npc/npc_heroes.txt")


for k,v in pairs(skillsListKV) do
    table.insert(skillsList, v)
end

for k,v in pairs(ultimatesListKV) do
    table.insert(ultimatesList, v)
end


local heroIDToName = {}
local heroNameToID = {}
local simpleHeroList = {}
local skillOwnerID = {}
for k,v in pairs(npcHeroesKV) do
    if k ~= 'Version' and k ~= 'npc_dota_hero_base' then
        if v.HeroID then
            heroIDToName[v.HeroID] = k
            heroNameToID[k] = v.HeroID
            table.insert(simpleHeroList, k)
            for i=1,16 do
                local ab = v['Ability'..i]
                if ab then
                    skillOwnerID[ab] = v.HeroID
                end
            end
        end
    end
end

function skillHandler:storePrecachedSkill(skillName)
    if precachedSkills[skillName] == nil then
        table.insert(precachedSkills, skillName)
    end
end

function skillHandler:storePrecachedUltimate(skillName)
    if precachedUltimates[skillName] == nil then
        table.insert(precachedUltimates, skillName)
    end
end

function skillHandler:getRandomHero()

    rand = math.random(#simpleHeroList)
    while (unique[simpleHeroList[rand]] ~= nil) do
        rand = math.random(#simpleHeroList)
    end
    heroName = simpleHeroList[rand]
    unique[heroName] = true

    return heroName
end

function skillHandler:getWhitelistedAbilities(heroName)
    result = {}
    result['skills'] = {}

    local skills = self:GetSkills(heroName)

    for k,v in pairs(skills) do

        for kk,vv in pairs(skillsListKV) do
            if v == vv then
                table.insert(result['skills'], v)
            end
        end

        for kk,vv in pairs(ultimatesListKV) do
            if v == vv then
                result['ultimate'] = v
            end
        end
    end

    --LogTable(result)
    return result

end


function skillHandler:getRandomPrecachedSkill()
    rand = math.random(#precachedSkills)
    got = precachedSkills[rand]
    return got
end


function skillHandler:getRandomPrecachedUltimate()
    rand = math.random(#precachedUltimates)
    got = precachedUltimates[rand]
    return got
end


function skillHandler:getRandomPrecachedSkills(skills, ultimates)
    Log('Skills to generate: ' .. skills)
    Log('Ultimates to generate: ' .. ultimates) 
    local uniq = {}
    build = {}
    for i = 1, skills do
        local skill = self:getRandomPrecachedSkill()
        while (uniq[skill] ~= nil) do
            skill = self:getRandomPrecachedSkill()
        end
        uniq[skill] = true
        table.insert(build, skill)
    end
    for i = 1, ultimates do
        local skill = self:getRandomPrecachedUltimate()
        while (uniq[skill] ~= nil) do
            skill = self:getRandomPrecachedUltimate()
        end
        uniq[skill] = true
        table.insert(build, skill)
    end
    return build
end


function skillHandler:GetSkills(heroName)
    local foundSkills = {}

    for name, values in pairs(npcHeroesKV) do
        if name == heroName then
            for x = 1, 16 do
                local ability = values["Ability" .. x]
                if ability and ability ~= 'attribute_bonus' then
                    table.insert(foundSkills, ability)
                end
            end
        end
    end

    return foundSkills
end

local total_precached = 0
local PRECACHE_IN_PROGRESS = false
local PRECACHE_FINISHED = false
function skillHandler:PrecacheHeroAsync(heroName, total)

    Timers:CreateTimer(0, function()

        if PRECACHE_IN_PROGRESS then return 1 end
        
        UNIT_BEING_PRECACHED = true

        PrecacheUnitByNameAsync(heroName, function()

            local abilities = self:getWhitelistedAbilities(heroName)
            for k,v in pairs(abilities['skills']) do
              SkillHandler:storePrecachedSkill(v)
            end
            SkillHandler:storePrecachedUltimate(abilities['ultimate'])
            UNIT_BEING_PRECACHED = false

            total_precached = total_precached + 1

            Log("Total Precached Heroes: " .. total_precached .. ' / ' .. total)

            if total_precached == total then
                PRECACHE_FINISHED = true
                Log("END PRECACHE")
            end


        end)

    end)

end


function skillHandler:RemoveAllSkills(hero)
    for index = 0, 15 do
        if hero:GetAbilityByIndex(index) ~= nil then
            abilityName = hero:GetAbilityByIndex(index):GetAbilityName()
            hero:RemoveAbility(abilityName)
        end
    end
end



function skillHandler:setSubSkills(hero, skills, startingPos)
    local abilityCount = startingPos
    for i, abilityName in pairs(skills) do

        local subAbilityName = subSkills[abilityName]
        if subAbilityName then

            -- Check if the hero does not have this ability already
            if not hero:HasAbility(subAbilityName) then
                
                -- Set this skill to hero
                hero:AddAbility(subAbilityName)

                -- Remove possible auras
                hero:RemoveModifierByName('modifier_' .. subAbilityName .. '_aura')
                hero:RemoveModifierByName('modifier_' .. subAbilityName)

                abilityCount = abilityCount + 1

            end
        end
    end
    return abilityCount
end

function skillHandler:getSubSkill(skill)
    
    return subSkills[skill]
    
end

function skillHandler:setMainSkills(hero, skills, startingPos)
    local abilityCount = startingPos
    for k, abilityName in pairs(skills) do
        if abilityName then

            -- Set this skill to hero
            hero:AddAbility(abilityName)

            -- Remove possible auras
            hero:RemoveModifierByName('modifier_' .. abilityName .. '_aura')
            hero:RemoveModifierByName('modifier_' .. abilityName)

            abilityCount = abilityCount + 1
        end
    end
    return abilityCount
end

function skillHandler:SetRandomSkills(hero, skillsCount, ultisCount)

    Timers:CreateTimer(0, function()

        if PRECACHE_FINISHED == false then 
            Log("Precache not finished...")
            return 1
        end

        local build = self:getRandomPrecachedSkills(skillsCount, ultisCount)
        
        local plyd = hero:GetPlayerID()
        local level = hero:GetLevel()

        hero:SetAbilityPoints(level)

        -- Apply the build
        self:SetSkills(hero, build)

    end)

end

function skillHandler:SetSkills(hero, skills)
    
    if hero == nil then
        return
    end

    Log('SetSkills called')
    LogTable(skills)

    local totalSlots = #skills

    -- Store extra skills needed
    local addSubAbilities = {}

    -- Remove all current skills
    self:RemoveAllSkills(hero)


    -- Re-add attribute bonus
    hero:AddAbility('attribute_bonus')


    -- Set all skills received to this hero
    local abilityCount = 1
    abilityCount = self:setMainSkills(hero, skills, abilityCount)
    abilityCount = self:setSubSkills(hero, skills, abilityCount)

    -- Reconfigure Ability Layout
    local modifierLayout = 'ability_layout_4'
    if totalSlots == 5 then modifierLayout = 'ability_layout_5' end
    if totalSlots >= 6 then modifierLayout = 'ability_layout_6' end

    hero:AddAbility(modifierLayout)
    hero:FindAbilityByName(modifierLayout):SetLevel(1)

    -- Remove possible bugged modifiers at start
    hero:RemoveModifierByName('modifier_slark_shadow_dance')
    hero:RemoveModifierByName('modifier_slark_shadow_dance_passive')
    hero:RemoveModifierByName('modifier_slark_shadow_dance_passive_regen') 
    hero:RemoveModifierByName('modifier_riki_permanent_invisibility')   
    
end

SkillHandler = skillHandler
