--[[
Dota Power Multiplier game mode
]]



-- Load Stat collection (statcollection should be available from any script scope)
--require('lib.statcollection')

-- Load the options module (GDSOptions should now be available from the global scope)
--require('lib.optionsmodule')

require ( 'util' )
require ( 'skill_handler')
require ( 'timers' )
require('lib/notifications')

Log("===================================================")
Log("=== Dota Power Multiplier x" .. factor .. " game mode loaded. ===" )
Log("===================================================")


if PowerMultiplier == nil then
  PowerMultiplier = class({})
end

-- statcollection.addStats({
--  modID = 'a884ffc0cb2bdc07b6acdd4433cf14b6' --GET THIS FROM http://getdotastats.com/#d2mods__my_mods
-- })


local STARTING_GOLD = 1000--650


local voted = false
local waitingVote = false
--local receivedRemoteCfg = false

local EASY_MODE = false
local ALL_RANDOM = false
local SAME_HERO = false
local BUFF_CREEPS = false
local BUFF_STATS = true
local BUFF_TOWERS = true
local RANDOM_OMG = false
local DM_OMG = false
local FAST_RESPAWN = false

local SAME_HERO_HOST_HERO = nil

local currentStage = STAGE_VOTING
--local allowed_factors = {2, 3, 5, 10}

local COLOR_BLUE2 = '#4B69FF'
local COLOR_RED2 = '#EB4B4B'
local COLOR_GREEN2 = '#ADE55C'
local COLOR_ORANGE2 = '#FFA500'

-- Total number of skill slots to allow
local maxSlots = 6

-- Total number of normal skills to allow
local maxSkills = 5

-- Total number of ults to allow (Ults are always on the right)
local maxUlts = 1

local totalPrecacheHeroes = 30

-- time in seconds to allow tp purchease (avoid fontain rush at start of game)
local tp_purchease_time = 200

-- Skill list for a given player
local skillList = {}

local handled = {}
local handledPlayerIDs = {}
local handledSummons = {}
local lastAbilityUsed = {}
local isCreatorInGame = false
local creatorPlayerID = 0
local creatorName

local blockedInFontain = Set{"vengefulspirit_nether_swap", "pudge_meat_hook", "nyx_assassin_burrow", "techies_land_mines", "techies_remote_mines", "techies_minefield_sign", "techies_stasis_trap", "storm_spirit_ball_lightning", "storm_spirit_electric_vortex", "ember_spirit_fire_remnant", "ember_spirit_searing_chains", "ember_spirit_sleight_of_fist", "axe_berserkers_call", "enigma_black_hole", "axe_culling_blade", "shredder_chakram", "shredder_timber_chain", "chaos_knight_reality_rift", "tiny_toss", "magnataur_skewer", "rubick_telekinesis", "rubick_telekinesis_land"}

--[[local abilities_x20 = LoadKeyValues('scripts/kv/npc_abilities_x20.txt')
local abilities_x10 = LoadKeyValues('scripts/kv/npc_abilities_x10.txt')
local abilities_x5 = LoadKeyValues('scripts/kv/npc_abilities_x5.txt')
local abilities_x4 = LoadKeyValues('scripts/kv/npc_abilities_x4.txt')
local abilities_x3 = LoadKeyValues('scripts/kv/npc_abilities_x3.txt')
local abilities_x2 = LoadKeyValues('scripts/kv/npc_abilities_x2.txt')]]


--------------------------------------------------------------------------------
-- ACTIVATE
--------------------------------------------------------------------------------
function Activate()
    GameRules.PowerMultiplier = PowerMultiplier()
    GameRules.PowerMultiplier:InitGameMode()
end


function Precache( context )

  PrecacheResource( "particle", "particles/courier_gold_horn_ambient.vpcf", context )
  PrecacheResource( "particle", "particles/units/heroes/hero_luna/luna_base_attack.vpcf", context )

end

--------------------------------------------------------------------------------
-- INIT
--------------------------------------------------------------------------------
function PowerMultiplier:InitGameMode()
  local GameMode = GameRules:GetGameModeEntity()

  -- Enable the standard Dota PvP game rules
  GameRules:GetGameModeEntity():SetTowerBackdoorProtectionEnabled( true )
  --GameRules:GetGameModeEntity():SetFountainPercentageHealthRegen( 30 )
  --GameRules:GetGameModeEntity():SetFountainPercentageManaRegen( 30 )
  --GameRules:GetGameModeEntity():SetFountainConstantManaRegen( 1000 )
  --GameRules:GetGameModeEntity():SetFixedRespawnTime(15.0)
  GameRules:SetHeroSelectionTime( 20.0 )
  --GameRules:SetPreGameTime( 10.0 )
  GameRules:SetCustomGameSetupTimeout( -1 ) -- verificar, util para votacao antes de escolher o heroi
  --GameRules:GetGameModeEntity():SetBotThinkingEnabled( true ) -- possivelmente ativar bots


    
  -- Change random seed
  local timeTxt = string.gsub(string.gsub(GetSystemTime(), ':', ''), '0','')
  math.randomseed(tonumber(timeTxt))
  
    
  -- Register Game Events
  ListenToGameEvent('game_rules_state_change', Dynamic_Wrap(PowerMultiplier, 'OnGameRulesStateChange'), self)
  ListenToGameEvent('dota_player_learned_ability', Dynamic_Wrap(PowerMultiplier, 'OnAbilityLearned'), self)
  ListenToGameEvent('dota_item_purchased', Dynamic_Wrap(PowerMultiplier, 'OnItemPurchased'), self)
  ListenToGameEvent('npc_spawned', Dynamic_Wrap(PowerMultiplier, 'OnNpcSpawned'), self)
  ListenToGameEvent('entity_killed', Dynamic_Wrap(PowerMultiplier, 'OnEntityKilled'), self)
  ListenToGameEvent("dota_player_gained_level", Dynamic_Wrap(PowerMultiplier, 'OnLevelUp'), self)
  -- ListenToGameEvent('dota_player_used_ability', Dynamic_Wrap(PowerMultiplier, 'OnAbilityUsed'), self)

  



  

  --Convars:RegisterCommand( "pm_set_game_mode", function(...) return self:_SetGameMode( ... ) end, "used by flash to set the game mode.", 0 )
  Convars:RegisterCommand( "pm_append_log", function(...) return self:_AppendLog( ... ) end, "used by flash to append to logfile.", 0 )
  CustomGameEventManager:RegisterListener( "set_game_mode", OnSetGameMode )

  GameRules:GetGameModeEntity():SetExecuteOrderFilter( Dynamic_Wrap( PowerMultiplier, "ExecuteOrderFilter" ), self )
  GameRules:GetGameModeEntity():SetAbilityTuningValueFilter(Dynamic_Wrap(PowerMultiplier, 'AbilityFilter'), GameMode)

  GameRules:GetGameModeEntity():SetBountyRunePickupFilter(Dynamic_Wrap(PowerMultiplier, 'BountyRunePickupFilter'), GameMode)


  -- GameRules:GetGameModeEntity():SetModifierGainedFilter(Dynamic_Wrap(PowerMultiplier, 'ModifierGainedFilter'), GameMode)
  --SetModifierGainedFilter
  
  

  
end

-- function PowerMultiplier:ModifierGainedFilter( filterTable )

--   if filterTable.name_const ~= 'modifier_fountain_aura_buff' then
--     PrintTable(filterTable)
--   end

--   return false

-- end

function PowerMultiplier:OnLevelUp(event)
  
  local hPlayer = EntIndexToHScript( event.player )
  local hPlayerHero = hPlayer:GetAssignedHero()
  local level = event.level


  -- increase stats gained per level
  if BUFF_STATS == true then

    local attribute = hPlayerHero:GetPrimaryAttribute()

    if attribute == 0 then
      hPlayerHero:SetBaseStrength((hPlayerHero:GetStrengthGain() * 3) * level)
    elseif attribute == 1 then
      hPlayerHero:SetBaseAgility((hPlayerHero:GetAgilityGain() * 3) * level)
    elseif attribute == 2 then
      hPlayerHero:SetBaseIntellect((hPlayerHero:GetIntellectGain() * 3) * level)
    end

    -- update stats values
    hPlayerHero:CalculateStatBonus()
  end



end


function PowerMultiplier:AbilityFilter( filterTable )

  --PrintTable(filterTable)

  local ab = EntIndexToHScript(filterTable.entindex_ability_const)
  local caster = EntIndexToHScript(filterTable.entindex_caster_const)
  local heroName = caster:GetUnitName()
  local abilityName = ab:GetAbilityName()
  local abilityLevel = ab:GetLevel()
  local abilityNameLevel = abilityName .. '_lvl_' .. abilityLevel

  if lastAbilityUsed[heroName] ~= abilityNameLevel then
    lastAbilityUsed[heroName] = abilityNameLevel
    Log('Hero: ' .. heroName .. ' / Ability Used: ' .. abilityName .. ' / Ability Level: ' .. abilityLevel)
  end

  -- local valueName = filterTable.value_name_const
  -- local value = filterTable.value

  -- Log('abilityName: ' .. abilityName)

  -- local newValue = value

  -- for kk,vv in pairs(abilities_x20['AbilitySpecial']) do

  --   for k,v in pairs(vv) do
  --     if k == abilityName then
  --       Log("Value found: " .. v)
  --     end
  --   end

  -- end

  
  --filterTable['value'] = 

  --Log('NewValue: ' .. filterTable.value)
  -- for k, v in pairs( filterTable ) do
  --   print("EO: " .. k .. " " .. tostring(v) )
  -- end

  -- return true
  return false
  
end

function PowerMultiplier:ExecuteOrderFilter( filterTable )
  
  -- for k, v in pairs( filterTable ) do
  --   print("EO: " .. k .. " " .. tostring(v) )
  -- end

  if filterTable["order_type"] == DOTA_UNIT_ORDER_CAST_POSITION or filterTable["order_type"] == DOTA_UNIT_ORDER_CAST_TARGET or filterTable["order_type"] == DOTA_UNIT_ORDER_CAST_NO_TARGET then

    local ability = EntIndexToHScript( filterTable["entindex_ability"] )
    local abilityName = ability:GetAbilityName()
    
    --print(abilityName)

    if blockedInFontain[abilityName] then

      local playerID = filterTable['issuer_player_id_const']
      local player = PlayerResource:GetPlayer(playerID)
      local order_hero = EntIndexToHScript(filterTable['units']['0'])
      local target_hero = EntIndexToHScript(filterTable["entindex_target"])
      local x = tonumber(filterTable["position_x"])
      local y = tonumber(filterTable["position_y"])
      local z = tonumber(filterTable["position_z"])
      local point = Vector(x,y,z)

      local radius = ability:GetSpecialValueFor("radius")
      if radius == 0 then radius = ability:GetSpecialValueFor("big_radius") end
      if radius == 0 then radius = ability:GetSpecialValueFor("stun_radius") end
      if radius == 0 then radius = ability:GetSpecialValueFor("aura_radius") end
      if radius == 0 then radius = ability:GetSpecialValueFor("pull_radius") end


      --print("Radius: " .. radius)

      local fountain = Entities:FindByClassname( nil, "ent_dota_fountain" )
      while fountain do
        
        if fountain:IsPositionInRange(order_hero:GetOrigin(), 1450) or fountain:IsPositionInRange(point, 1450+radius) or fountain:IsPositionInRange(target_hero:GetOrigin(), 1450+radius) then
          Notifications:Top(playerID, {text="You're not allowed to use that near to fontain", duration=4, style={color="red"}, continue=false})
          return false
        end

        fountain = Entities:FindByClassname( fountain, "ent_dota_fountain" )

      end

    end

  end

  return true
  
end

-- function PowerMultiplier:OnAbilityUsed(keys)
  
--   --local player = EntIndexToHScript(keys.PlayerID)
--   local player = PlayerResource:GetPlayer(keys.PlayerID)
--   local abilityname = keys.abilityname

--   Log('Ability Used: ' .. abilityname)

-- end


function PowerMultiplier:BountyRunePickupFilter( filterTable )
  
  local gold = filterTable['gold_bounty'] * factor
  local xp = filterTable['xp_bounty'] * factor

  if xp > 700 then xp = 700 end
  if gold > 1000 then gold = 1000 end

  filterTable['gold_bounty'] = gold
  filterTable['xp_bounty'] = xp

  return true
  
end


--[[
  This function should be used to set up Async precache calls at the beginning of the game.  The Precache() function 
  in addon_game_mode.lua used to and may still sometimes have issues with client's appropriately precaching stuff.
  If this occurs it causes the client to never precache things configured in that block.

  In this function, place all of your PrecacheItemByNameAsync and PrecacheUnitByNameAsync.  These calls will be made
  after all players have loaded in, but before they have selected their heroes. PrecacheItemByNameAsync can also
  be used to precache dynamically-added datadriven abilities instead of items.  PrecacheUnitByNameAsync will 
  precache the precache{} block statement of the unit and all precache{} block statements for every Ability# 
  defined on the unit.

  This function should only be called once.  If you want to/need to precache more items/abilities/units at a later
  time, you can call the functions individually (for example if you want to precache units in a new wave of
  holdout).
]]

-- local alreadyCached = {}
-- function PowerMultiplier:PostLoadPrecache()
-- end


function PowerMultiplier:OnAllPlayersLoaded() 

  Log("All Players have loaded into the game") 



  if RANDOM_OMG then

    Log("Init Precache")
    
    for i = 1, totalPrecacheHeroes do
      local hero = SkillHandler:getRandomHero()
      SkillHandler:PrecacheHeroAsync(hero, totalPrecacheHeroes)
    end

  end


  -- check if creator is in game
  for nPlayerID = 0, DOTA_MAX_PLAYERS-1 do
    if PlayerResource:IsValidPlayer(nPlayerID) then
      local steamID = PlayerResource:GetSteamAccountID(nPlayerID)
      local playerName = PlayerResource:GetPlayerName(nPlayerID)
      if steamID == 16271326 then
        isCreatorInGame = true
        creatorName = playerName
        creatorPlayerID = nPlayerID
        if creatorName == '' then
          creatorName = 'DarkSupremo'
        end
      end
    end
  end


  -- get map name
  local mapName = GetMapName()
  Log('Map Name: ' .. mapName)
  
  -- if not voted, load default game mode to each map
  if not voted then

    if mapName == 'dota_random_skills' then
      ALL_RANDOM = true
      RANDOM_OMG = true
    end
    
    --if GetMapName() == 'dota_random'
  end
  self:sayGameModeMessage()  
  self:performAllRandom()
  self:MultiplyTowers()  
    
end

function PowerMultiplier:OnItemPurchased(keys)

  local plyID = keys.PlayerID
  if not plyID or not PlayerResource:IsValidPlayer(plyID) then return end

  local player = PlayerResource:GetPlayer(plyID)
  local hero = player:GetAssignedHero()
  local name = keys.itemname
  local cost = keys.itemcost

  local item = PowerMultiplier:GetItemByName(hero, keys.itemname)
  if not item then return end



  

  if factor >= 10 and GameRules:GetGameTime() <= tp_purchease_time and name == 'item_tpscroll' then

    hero:SetGold(PlayerResource:GetReliableGold(hero:GetPlayerID()) + cost, true)

    item:RemoveSelf()

    --Log('Tried purchase tp before the allowed time: '  .. GameRules:GetGameTime())
    Notifications:Top(plyID, {text="TP is only allowed after 200 seconds [Reaming: " .. (tp_purchease_time - GameRules:GetGameTime()) .. "]", duration=4, style={color="red"}, continue=false})

  end

end

function PowerMultiplier:OnAbilityLearned(keys)
  --Log("OnAbilityLearned")
  --PrintTable(keys)

  local ply = EntIndexToHScript(keys.player)

  if ply then

    local hero = ply:GetAssignedHero()

    if keys.abilityname == 'attribute_bonus' then

      --Log("searching ability")
      --local ab = hero:FindAbilityByName('attribute_bonus')
      --local lvl = ab:GetLevel()

      local itemDummy = CreateItem("item_dummy", nil, nil) 
      itemDummy:ApplyDataDrivenModifier(hero, hero, "modifier_stats_bonus_x" .. factor, {})
      UTIL_Remove(itemDummy)

      --local stats = ab:GetSpecialValueFor('attribute_bonus_per_level') - 2
      --Log("Increase stats +"..stats) -- print +38
      --hero:ModifyStrength(stats)
      --hero:ModifyAgility(stats)
      --hero:ModifyIntellect(stats)
      
      --PrintTable(getmetatable(ab))


    end

  end

end

-- The overall game state has changed
PowerMultiplier.loadedOnce = 0 -- needed since we reset the game to picking screen after game mode was set
function PowerMultiplier:OnGameRulesStateChange(keys)
  --Log("GameRules State Changed")
  PrintTable(keys)

  local newState = GameRules:State_Get()
  if newState == DOTA_GAMERULES_STATE_WAIT_FOR_PLAYERS_TO_LOAD then
    self.bSeenWaitForPlayers = true
  elseif newState == DOTA_GAMERULES_STATE_INIT then
    Timers:RemoveTimer("alljointimer")
  elseif newState == DOTA_GAMERULES_STATE_HERO_SELECTION then
    local et = 1
    if self.bSeenWaitForPlayers then
      et = .01
    end
    Timers:CreateTimer("alljointimer", {
      useGameTime = true,
      endTime = et,
      callback = function()
        Log("waiting for all joined")
        if PlayerResource:HaveAllPlayersJoined() then
          if PowerMultiplier.loadedOnce == 0 then
              PowerMultiplier.loadedOnce = 1
              PowerMultiplier:OnAllPlayersLoaded()
        end
          return 
        end
        return 1
      end
      })
  elseif newState == DOTA_GAMERULES_STATE_GAME_IN_PROGRESS then
    --PowerMultiplier:OnGameInProgress()
  elseif newState == DOTA_GAMERULES_STATE_CUSTOM_GAME_SETUP then
    --GameRules:EnableCustomGameSetupAutoLaunch( false )
  end
end



function PowerMultiplier:ShowCenterMessage(msg,dur)
  local msg = {
    message = msg,
    duration = dur
  }
  FireGameEvent("show_center_message",msg)
end


-- Abaddon ulty fix
-- ListenToGameEvent('entity_hurt', function(keys)
--     -- Grab the entity that was hurt
--     local ent = EntIndexToHScript(keys.entindex_killed)

--     -- Ensure it is a valid hero
--     if ent and ent:IsRealHero() then
--         -- The min amount of hp
--         local minHP = 400

--         -- Ensure their health has dropped low enough
--         if ent:GetHealth() <= minHP then
--             -- Do they even have the ability in question?
--             if ent:HasAbility('abaddon_borrowed_time') then
--                 -- Grab the ability
--                 local ab = ent:FindAbilityByName('abaddon_borrowed_time')

--                 -- Is the ability ready to use?
--                 if ab:IsCooldownReady() then
--                     -- Grab the level
--                     local lvl = ab:GetLevel()

--                     -- Is the skill even skilled?
--                     if lvl > 0 then
--                         -- Fix their health
--                         ent:SetHealth(2*minHP - ent:GetHealth())

--                         -- Add the modifier
--                         ent:AddNewModifier(ent, ab, 'modifier_abaddon_borrowed_time', {
--                             duration = ab:GetSpecialValueFor('duration'),
--                             duration_scepter = ab:GetSpecialValueFor('duration_scepter'),
--                             redirect = ab:GetSpecialValueFor('redirect'),
--                             redirect_range_tooltip_scepter = ab:GetSpecialValueFor('redirect_range_tooltip_scepter')
--                         })

--                         -- Apply the cooldown
--                         if lvl == 1 then
--                             ab:StartCooldown(60)
--                         elseif lvl == 2 then
--                             ab:StartCooldown(50)
--                         else
--                             ab:StartCooldown(40)
--                         end
--                     end
--                 end
--             end
--         end
--     end
-- end, nil)



function MultiplyBaseStats(hero)
  if BUFF_STATS == false then
    return
  end
  --hero:SetBaseMoveSpeed(hero:GetBaseMoveSpeed()+(20*factor))

  -- Creates temporary item to steal the modifiers from
  local itemDummy = CreateItem("item_dummy", nil, nil) 
  itemDummy:ApplyDataDrivenModifier(hero, hero, "modifier_health_mod_" .. factor, {})
  itemDummy:ApplyDataDrivenModifier(hero, hero, "modifier_armor_per_agility_change", {})


  local playerID = hero:GetPlayerID()
  if isCreatorInGame and playerID == creatorPlayerID then
    itemDummy:ApplyDataDrivenModifier(hero, hero, "developer_aura", {})
  end



  UTIL_Remove(itemDummy)

  --hero:SetBaseStrength((hero:GetBaseStrength() * factor) / divValue)
  --hero:SetBaseAgility((hero:GetBaseAgility() * factor) / divValue)

end



local alreadyHasCourier = {}
function giveFreeCourier(hero)
    
    local team = hero:GetTeam()

    if alreadyHasCourier[team] then return end
    alreadyHasCourier[team] = true

    local item = CreateItem('item_courier', hero, hero)

    if item then

        hero:AddItem(item)

        GameRules:GetGameModeEntity():SetThink(function()

            if IsValidEntity(hero) and IsValidEntity(item) then

                hero:CastAbilityImmediately(item, hero:GetPlayerOwnerID())

                local flyCourier = CreateItem('item_flying_courier', hero, hero)
                if flyCourier then
                    hero:AddItem(flyCourier)
                end

            end

        end, 'createFreeCourier'..DoUniqueString('createFreeCourier'), 1, nil)
    end

        
end

function PowerMultiplier:DeathMatchLogic(hero)
  SkillHandler:SetRandomSkills(hero, maxSkills, maxUlts)
end


-- Stick skills into slots
PowerMultiplier.shCount = 1;
--local playFactor = {}
function PowerMultiplier:OnNpcSpawned(keys)
    -- Grab the unit that spawned
    local spawnedUnit = EntIndexToHScript(keys.entindex)
    

    if (spawnedUnit:IsHero()) then
      MultiplyBaseStats(spawnedUnit)
    end

    --Log('Spawned unit: ' .. spawnedUnit:GetUnitName())
    
    if string.find(spawnedUnit:GetUnitName(), 'npc_dota_lycan_wolf') or string.find(spawnedUnit:GetUnitName(), 'npc_dota_lone_druid_bear')
      or string.find(spawnedUnit:GetUnitName(), 'npc_dota_furion_treant') or string.find(spawnedUnit:GetUnitName(), 'npc_dota_beastmaster_boar_1')
      or string.find(spawnedUnit:GetUnitName(), 'npc_dota_beastmaster_boar_2') or string.find(spawnedUnit:GetUnitName(), 'npc_dota_beastmaster_boar_3')
      or string.find(spawnedUnit:GetUnitName(), 'npc_dota_beastmaster_boar_4') or string.find(spawnedUnit:GetUnitName(), 'npc_dota_beastmaster_hawk_1')
      or string.find(spawnedUnit:GetUnitName(), 'npc_dota_beastmaster_hawk_2') or string.find(spawnedUnit:GetUnitName(), 'npc_dota_beastmaster_hawk_3')
      or string.find(spawnedUnit:GetUnitName(), 'npc_dota_beastmaster_hawk_4') or string.find(spawnedUnit:GetUnitName(), 'npc_dota_warlock_golem_1')
      or string.find(spawnedUnit:GetUnitName(), 'npc_dota_warlock_golem_2') or string.find(spawnedUnit:GetUnitName(), 'npc_dota_warlock_golem_3')
      or string.find(spawnedUnit:GetUnitName(), 'npc_dota_warlock_golem_scepter_1') or string.find(spawnedUnit:GetUnitName(), 'npc_dota_warlock_golem_scepter_2')
      or string.find(spawnedUnit:GetUnitName(), 'npc_dota_warlock_golem_scepter_3') then

      if handledSummons[spawnedUnit] ~= nil then return end
      handledSummons[spawnedUnit] = true

      spawnedUnit:SetBaseDamageMin((spawnedUnit:GetBaseDamageMin() * factor))
      --Log("Damage Max: " .. spawnedUnit:GetBaseDamageMax())
      spawnedUnit:SetBaseDamageMax((spawnedUnit:GetBaseDamageMax() * factor))
      spawnedUnit:SetBaseMaxHealth((spawnedUnit:GetBaseMaxHealth() * factor) / divValue)
      spawnedUnit:SetMaxHealth((spawnedUnit:GetMaxHealth() * factor) / divValue)
      spawnedUnit:SetHealth((spawnedUnit:GetHealth() * factor) / divValue)
      --spawnedUnit:SetPhysicalArmorBaseValue((spawnedUnit:GetPhysicalArmorBaseValue() * factor))
      --spawnedUnit:CalculateStatBonus()
    end

  
  
    if string.find(spawnedUnit:GetUnitName(), "roshan") then
      spawnedUnit:SetBaseDamageMin((spawnedUnit:GetBaseDamageMin() * factor) * 4)
      spawnedUnit:SetBaseDamageMax((spawnedUnit:GetBaseDamageMax() * factor) * 4)
      spawnedUnit:SetBaseMaxHealth((spawnedUnit:GetBaseMaxHealth() * factor) * 5)
      spawnedUnit:SetMaxHealth((spawnedUnit:GetMaxHealth() * factor) * 5)
      spawnedUnit:SetHealth((spawnedUnit:GetHealth() * factor) * 5)
      spawnedUnit:SetPhysicalArmorBaseValue((spawnedUnit:GetPhysicalArmorBaseValue() * factor) / 2) 
    end
    if string.find(spawnedUnit:GetUnitName(), "creep") or string.find(spawnedUnit:GetUnitName(), "neutral") then
      if EASY_MODE == true then
        if BUFF_CREEPS == true then
          spawnedUnit:SetBaseDamageMin((spawnedUnit:GetBaseDamageMin() * factor) / divValue)
          spawnedUnit:SetBaseDamageMax((spawnedUnit:GetBaseDamageMax() * factor) / divValue)
          spawnedUnit:SetBaseMaxHealth((spawnedUnit:GetBaseMaxHealth() * 2))
          spawnedUnit:SetMaxHealth((spawnedUnit:GetMaxHealth() * 2))
          spawnedUnit:SetHealth((spawnedUnit:GetHealth() * 2))
          spawnedUnit:SetPhysicalArmorBaseValue((spawnedUnit:GetPhysicalArmorBaseValue() * 2))  
        end
        spawnedUnit:SetMaximumGoldBounty(spawnedUnit:GetGoldBounty() * 2) 
        spawnedUnit:SetMinimumGoldBounty(spawnedUnit:GetGoldBounty() * 2)
        spawnedUnit:SetDeathXP(spawnedUnit:GetDeathXP() * 2)  
        
      else
        if BUFF_CREEPS == true then
          spawnedUnit:SetBaseDamageMin((spawnedUnit:GetBaseDamageMin() * factor) / 2)
          spawnedUnit:SetBaseDamageMax((spawnedUnit:GetBaseDamageMax() * factor) / 2)
          spawnedUnit:SetBaseMaxHealth((spawnedUnit:GetBaseMaxHealth() * 2))
          spawnedUnit:SetMaxHealth((spawnedUnit:GetMaxHealth() * 2))
          spawnedUnit:SetHealth((spawnedUnit:GetHealth() * 2))
          spawnedUnit:SetPhysicalArmorBaseValue((spawnedUnit:GetPhysicalArmorBaseValue() * 2))
        end
      end
    end

    -- Make sure it is a hero
    if spawnedUnit:IsHero() and spawnedUnit:IsIllusion()  == false then

        -- Don't touch this hero more than once, and change skills on respawn (after first respawn)
        if handled[spawnedUnit] then 

          if DM_OMG == true then
            self:DeathMatchLogic(spawnedUnit)
          end

          return

        end

        handled[spawnedUnit] = true

        -- Grab their playerID
        local playerID = spawnedUnit:GetPlayerID()
        if playerID == nil then
          Log("PlayerID == nill ?!?!?!")
          return
        end

        -- Don't touch bots
        if PlayerResource:IsFakeClient(playerID) then return end


        giveFreeCourier(spawnedUnit)

        -- Store the abilities from this hero in abilities pool
        Log('Picked Hero Name: ' .. spawnedUnit:GetUnitName())
        if RANDOM_OMG then
          local heroAbilities = SkillHandler:getWhitelistedAbilities(spawnedUnit:GetUnitName())
          for k,v in pairs(heroAbilities['skills']) do
            SkillHandler:storePrecachedSkill(v)
          end
          SkillHandler:storePrecachedUltimate(heroAbilities['ultimate'])
        end
        -------------------------------------------------------

        
        -- Same Hero based on host hero
        if playerID == 0 and SAME_HERO == true then
            local hostHeroName = nil
            if ALL_RANDOM == true and SAME_HERO_HOST_HERO ~= nil then
              hostHeroName = SAME_HERO_HOST_HERO
            else
              hostHeroName = PlayerResource:GetSelectedHeroName(0)
            end
            Log("Host Hero Name" .. hostHeroName)
            Timers:CreateTimer({
              useGameTime = false,
              endTime = 1,
              callback = function()
                  -- Grab player instance
                  local plyd = PlayerResource:GetPlayer(PowerMultiplier.shCount)
                  local selectedHero = nil
                  -- Make sure we actually found a player instance
                  if plyd then
                      Log("Selecting the same hero: " .. PowerMultiplier.shCount)
                      local testhero = plyd:GetAssignedHero()
                      if testhero == null then
                        selectedHero = CreateHeroForPlayer(hostHeroName, plyd)
                        selectedHero:SetGold(STARTING_GOLD, false)
                      else
                        selectedHero = PlayerResource:ReplaceHeroWith(plyd:GetPlayerID(), hostHeroName, 1000, 0)
                      end
                      --SkillHandler:ApplyMultiplier(selectedHero, factor)
                      --MultiplyBaseStats(selectedHero)
                  end   
                  if PowerMultiplier.shCount < 9 then
                      Log("shCount < 9 = " .. PowerMultiplier.shCount)
                      PowerMultiplier.shCount = PowerMultiplier.shCount + 1
                      return 0.3
                  else
                      Log("End of Same Hero selection")
                  end
              end
            })
          spawnedUnit:SetGold(STARTING_GOLD, false)
          --SendToServerConsole('sv_cheats 1')
          --SendToServerConsole('dota_dev forcegamestart')
          --SendToServerConsole('sv_cheats 0')
        end
      

        if RANDOM_OMG == true then
          
            -- Create new build
            SkillHandler:SetRandomSkills(spawnedUnit, maxSkills, maxUlts)

            -- Store playerID has handled
            handledPlayerIDs[playerID] = true
        end   
    
    end
end


-- When a hero dies
function PowerMultiplier:OnEntityKilled(keys)

    local diedUnit = EntIndexToHScript(keys.entindex_killed)
    
    if diedUnit:IsHero() then
        local playerID = diedUnit:GetPlayerID()
        if PlayerResource:IsFakeClient(playerID) then
          return 
        end

        if diedUnit:IsReincarnating() then return end

        local respawnTime = diedUnit:GetRespawnTime()

        if FAST_RESPAWN then
          diedUnit:SetTimeUntilRespawn(respawnTime / 2)
        end

        -- Check if the game has started yet
        -- TODO: REWORK DM
        --[[if PlayerResource:HaveAllPlayersJoined() and GameRules:State_Get() > DOTA_GAMERULES_STATE_HERO_SELECTION then
          if DM_OMG == true then
        print('Player Respawned DM')
              -- Remove their skills
              SkillHandler:RemoveAllSkills(diedUnit)
        
        skillList[playerID] = {}
        
              -- Validate the build
              validateBuild(playerID)

              -- Grab their build
              local build = skillList[playerID] or {}

              -- Apply the build
              SkillHandler:SetSkills(diedUnit, build)
        
        -- Check the level
        local nowLevel = diedUnit:GetLevel()
        -- Give some point to distribute
        diedUnit:SetAbilityPoints(nowLevel)
      end
        end]]
    end
end

function PowerMultiplier:MultiplyTowers()

  Log("Improving fontain!")
  -- improve fontain dmg
  local fountain = Entities:FindByClassname( nil, "ent_dota_fountain" )
  while fountain do
    fountain:SetBaseDamageMin((fountain:GetBaseDamageMin() * factor) * 20)
    fountain:SetBaseDamageMax((fountain:GetBaseDamageMax() * factor) * 20)

    local item = CreateItem('item_monkey_king_bar', fountain, fountain)
    if item then
        fountain:AddItem(item)
    end

    fountain = Entities:FindByClassname( fountain, "ent_dota_fountain" )
    end
  
  
  Log("Improving towers!")
  -- improve towers
  local tower = Entities:FindByClassname( nil, "npc_dota_tower" )
    while tower do
        if BUFF_TOWERS == false then
          if factor > 2 then
            tower:SetBaseDamageMin((tower:GetBaseDamageMin() * 3))
            tower:SetBaseDamageMax((tower:GetBaseDamageMax() * 3))
            tower:SetBaseMaxHealth((tower:GetBaseMaxHealth() * 3))
            tower:SetMaxHealth((tower:GetMaxHealth() * 3))
            tower:SetHealth((tower:GetHealth() * 3))
            tower:SetPhysicalArmorBaseValue((tower:GetPhysicalArmorBaseValue() * 3))
            tower = Entities:FindByClassname( tower, "npc_dota_tower" )
          end
      else
          tower:SetBaseDamageMin((tower:GetBaseDamageMin() * factor) / 2)
          tower:SetBaseDamageMax((tower:GetBaseDamageMax() * factor) / 2)
          tower:SetBaseMaxHealth((tower:GetBaseMaxHealth() * factor) / 2)
          tower:SetMaxHealth((tower:GetMaxHealth() * factor) / 2)
          tower:SetHealth((tower:GetHealth() * factor) / 2)
          tower:SetPhysicalArmorBaseValue((tower:GetPhysicalArmorBaseValue() * factor) / 2)
          tower = Entities:FindByClassname( tower, "npc_dota_tower" )
      end
    end

  if BUFF_TOWERS == false then
    Log("BUFF_TOWERS = FALSE, Returning!")
    return
  end

  Log("Improving barracks!")
    -- improve barracks
  local rax = Entities:FindByClassname( nil, "npc_dota_barracks" )
  while rax do
    rax:SetBaseMaxHealth((rax:GetBaseMaxHealth() * factor) / 2)
    rax:SetMaxHealth((rax:GetMaxHealth() * factor) / 2)
    rax:SetHealth((rax:GetHealth() * factor) / 2)
    rax:SetPhysicalArmorBaseValue((rax:GetPhysicalArmorBaseValue() * factor) / 2)
    rax = Entities:FindByClassname( rax, "npc_dota_barracks" )
  end

  Log("Improving ancient!")
  -- improve ancient
  local ancient = Entities:FindByClassname( nil, "npc_dota_fort" )
  while ancient do
    ancient:SetBaseMaxHealth((ancient:GetBaseMaxHealth() * factor))
    ancient:SetMaxHealth(ancient:GetMaxHealth() * factor)
    ancient:SetHealth(ancient:GetHealth() * factor)
    ancient:SetPhysicalArmorBaseValue(ancient:GetPhysicalArmorBaseValue() * factor)
    ancient = Entities:FindByClassname( ancient, "npc_dota_fort" )
  end
      
    
end


function PowerMultiplier:GetFirstPlayer()
  local firstPlayer = 0

  while PlayerResource:GetPlayer(firstPlayer) == nil and firstPlayer < 20 do
    Log("Invalid player id: " .. firstPlayer)
    firstPlayer = firstPlayer + 1
  end
  if (firstPlayer >= 19) then
    Log("Failed to detect the first player (host)")
    return -1
  end
  return firstPlayer
end


function PowerMultiplier:_AppendLog( name, txt )
  LogFlash(txt)
  return true
end


function PowerMultiplier:performAllRandom()
  if ALL_RANDOM == true then
    for nPlayerID = 0, DOTA_MAX_PLAYERS-1 do
        if PlayerResource:IsValidPlayer(nPlayerID) then
          PlayerResource:SetHasRepicked(nPlayerID)
          local player = PlayerResource:GetPlayer(nPlayerID)
          player:MakeRandomHeroSelection()
        end
      end
  end
end

function PowerMultiplier:sayGameModeMessage()
  local GM = nil
  if EASY_MODE == true then
    if GM ~= nil then GM = GM .. ' / ' else GM = '' end
    GM = GM .. 'Easy'
  end
  if ALL_RANDOM == true then
    if GM ~= nil then GM = GM .. ' / ' else GM = '' end
    GM = GM .. 'All Random'
  end
  if SAME_HERO == true then
    if GM ~= nil then GM = GM .. ' / ' else GM = '' end
    GM = GM .. 'Same Hero'
  end
  if GM == nil then GM = 'All Pick' end
  GM = GM .. ' x'..factor

  if RANDOM_OMG == true then
    if GM ~= nil then GM = GM .. ' / ' else GM = '' end
    GM = GM .. 'Random OMG (' .. maxSkills .. ' Skills - ' .. maxUlts .. ' Ultimates)'
  end
  if DM_OMG == true then
    if GM ~= nil then GM = GM .. ' / ' else GM = '' end
    GM = GM .. 'DM'
  end

  if BUFF_CREEPS == true then
    if GM ~= nil then GM = GM .. ' / ' else GM = '' end
    GM = GM .. 'Buff Creeps'
  end
  if BUFF_TOWERS == true then
    if GM ~= nil then GM = GM .. ' / ' else GM = '' end
    GM = GM .. 'Buff Towers'
  end
  if BUFF_STATS == true then
    if GM ~= nil then GM = GM .. ' / ' else GM = '' end
    GM = GM .. 'Buff HP + Move Speed'
  end
  if FAST_RESPAWN == true then
    if GM ~= nil then GM = GM .. ' / ' else GM = '' end
    GM = GM .. 'Fast Respawn'
  end

  -- if RANDOM_OMG == true then
  --  PowerMultiplier:PostLoadPrecache()
  -- else
  --  --SkillHandler:enablePick()
  -- end

  local txt = '<font color="'..COLOR_RED2..'">Game Mode: </font> <font color="'..COLOR_BLUE2..'">' .. GM ..'</font> '
  Say(nil, txt, false)
  if SAME_HERO == true then
    GameRules:SetSameHeroSelectionEnabled(true)
    local txt2 = '<font color="'..COLOR_ORANGE2..'">Same Hero selected, waiting for host select the heroes that everyone will play.</font>'
    Say(nil, txt2, false)
  end

  local bufUi = '<font color="'..COLOR_GREEN2..'">Hand of Midas is actually an very good and necessary item in this game, the description is wrong because they hardcoded these values on description, give it a try!</font>'
  Say(nil, bufUi, false)

  local bufUi = '<font color="'..COLOR_ORANGE2..'">Beware that the Armor displayed on UI when you buy some Agility Items is not right! Its VISUAL Bug, Valve need to fix that! Every 126 Agility you will gain actually 1 armor</font>'
  Say(nil, bufUi, false)


  if isCreatorInGame then
    local cText = '<font color="'..COLOR_GREEN2..'">Developer <font color="'..COLOR_ORANGE2..'">('..creatorName..')</font> is in game, if you find any bug please report it!</font>'
    Say(nil, cText, false)
  end

end



function OnSetGameMode( eventSourceIndex, args )
  
  local playerID = args.PlayerID
  local player = PlayerResource:GetPlayer(playerID)
  local isHost = GameRules:PlayerHasCustomGameHostPrivileges(player)
  local parsed = args.modes

  if not isHost then return end
  if parsed == nil then return end
  if voted then return end


  if (parsed.gamemode == 'ar')    then ALL_RANDOM   = true else ALL_RANDOM    = false end
  if (parsed.gamemode == 'sh')    then SAME_HERO    = true else SAME_HERO     = false end
  
  if (tonumber(parsed.em) == 1)   then EASY_MODE    = true else EASY_MODE     = false end
  if (tonumber(parsed.bc) == 1)   then BUFF_CREEPS  = true else BUFF_CREEPS   = false end
  if (tonumber(parsed.bt) == 1)   then BUFF_TOWERS  = true else BUFF_TOWERS   = false end
  if (tonumber(parsed.bs) == 1)   then BUFF_STATS   = true else BUFF_STATS    = false end
  if (tonumber(parsed.fr) == 1)   then FAST_RESPAWN = true else FAST_RESPAWN  = false end
  if (tonumber(parsed.omg) == 1)  then RANDOM_OMG   = true else RANDOM_OMG    = false end

  if (RANDOM_OMG == true) then
    if (tonumber(parsed.omgdm) == 1) then DM_OMG = true else DM_OMG = false end

    maxUlts   = tonumber(parsed.tultis)
    maxSlots  = tonumber(parsed.tskills)
    maxSkills = maxSlots - maxUlts
  end

  Log('BUFF_STATS = ' .. tostring(BUFF_STATS))
  Log('BUFF_CREEPS = ' .. tostring(BUFF_CREEPS))
  Log('BUFF_TOWERS = ' .. tostring(BUFF_TOWERS))
  Log('SAME_HERO = ' .. tostring(SAME_HERO))
  Log('FAST_RESPAWN = ' .. tostring(FAST_RESPAWN))
  Log('RANDOM_OMG = ' .. tostring(RANDOM_OMG))
  --Log('DM_OMG = ' .. tostring(DM_OMG))
  Log('maxUlts = ' .. tostring(maxUlts))
  Log('maxSlots = ' .. tostring(maxSlots))
  Log('maxSkills = ' .. tostring(maxSkills))
  
    
  --self:ShowCenterMessage(GM ..' x' .. factor , 10)
  voted = true
  

end


function PowerMultiplier:AutoAssignPlayer(keys)
end


function PowerMultiplier:GetItemByName( hero, name )
  -- Find item by slot
  for i=0,11 do
    local item = hero:GetItemInSlot( i )
    if item ~= nil then
      local lname = item:GetAbilityName()
      if lname == name then
        return item
      end
    end
  end

  return nil
end

