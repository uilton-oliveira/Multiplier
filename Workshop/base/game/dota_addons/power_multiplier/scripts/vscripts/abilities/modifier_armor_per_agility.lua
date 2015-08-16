require ( 'util' )

local baseArmorOriginal = {}
local lastArmorPerAgi = {}
local initialArmor = {}

-- function round(x)
--   return x>=0 and math.floor(x+0.5) or math.ceil(x-0.5)
-- end

-- function getExtraArmor(caster)
-- 	local extraArmor = math.abs(round((caster:GetAgility() * 0.14) - (caster:GetPhysicalArmorValue() - baseArmorOriginal[caster])))
-- end


function getArmorPerAgility(caster)

	return (((caster:GetAgility() * 0.14) + baseArmorOriginal[caster]))

end

function getArmorToReduce(caster)

	-- do not reduce the initial armor
	if caster:GetPhysicalArmorValue() == initialArmor[caster] then
		return 0 
	end	

	-- armor to be reduced
	--return ((getArmorPerAgility(caster) / factor) * (factor-1)) * -1
	local multiply = factor-3
	if multiply <= 0 then multiply = 1 end
	
	return ((getArmorPerAgility(caster) / factor) * multiply) * -1

end

function setup(caster)

	-- store base armor if its the first time
	if baseArmorOriginal[caster] == nil then
		baseArmorOriginal[caster] = caster:GetPhysicalArmorBaseValue()
	end


	-- abort if armor per agi is the same as the last time we checked
	if getArmorPerAgility(caster) == lastArmorPerAgi[caster] then
		return false
	end

	-- if its the first time, store the initial armor
	if initialArmor[caster] == nil then
		initialArmor[caster] = caster:GetPhysicalArmorValue()
	end

	-- reset the base armor
	if baseArmorOriginal[caster] ~= nil then
		caster:SetPhysicalArmorBaseValue(baseArmorOriginal[caster])
	else
		baseArmorOriginal[caster] = caster:GetPhysicalArmorBaseValue()
	end

	-- continue
	return true

end

function finish(caster)

	-- store the current armor, so we can check if the armor was changed or not between each execution
	lastArmorPerAgi[caster] = getArmorPerAgility(caster)

end

function ReduceArmorPerAgility( keys )

	local caster = keys.caster


	-- init required stuffs or return if no action is needed
	if setup(caster) == false then return end		
		
	--Log('armor_per_agi: ' .. getArmorPerAgility(caster))
	--Log('armor_to_reduce: ' .. getArmorToReduce(caster))		

	-- change armor base armor
	caster:SetPhysicalArmorBaseValue(getArmorToReduce(caster))

	finish(caster)


end