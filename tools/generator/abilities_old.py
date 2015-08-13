from lib.keyvalues import KeyValues
from lib import clean
import os


force_divide = ['min_blink_range']

ignore_all_special = ['crit_chance', 'bonus_evasion', 'dodge_chance_pct', 'miss_chance', 'dodge_chance',
                    'illusion_damage_out_pct', 'illusion_damage_in_pct']

ignore_special = {'pudge_meat_hook':{'hook_width'}}

ignore_all_normal = ['ID', 'AbilityCastPoint', 'AbilityManaCost', 'AbilityCooldown']


dont_parse = ['Version', 'ability_base', 'default_attack',
             'abaddon_frostmourne', 'pudge_rot', 'alchemist_unstable_concoction'
             'alchemist_unstable_concoction_throw', 'drow_ranger_frost_arrows', 'axe_counter_helix',
             'beastmaster_call_of_the_wild', 'beastmaster_call_of_the_wild_boar']

factors = [2,3]




def str_to_type (s):
    try:                
        f = float(s)        
        if "." not in s:
            return int
        return float
    except ValueError:
        #print "EXCEPTION: %s" % s 
        value = s.upper()
        if value == "TRUE" or value == "FALSE":
            return bool
        return type(s)



def multiply(values, by, separator):
    aslist = values.strip().split(separator)
    tmplist = []
    newvalues = ''
    for value in aslist:
        try:
            newvalue = str(float(value.strip())*float(by))
            if newvalue[-2:] == '.0' and value[-2:] != '.0':
                newvalue = newvalue[:-2]
            tmplist.append(newvalue)
        except ValueError:
            print "EXCEPTION - ValueError multiply: %s | %s" % (value.strip(), values)
         
    return ' '.join(tmplist)

def divide(values, by, separator):
    aslist = values.strip().split(separator)
    tmplist = []
    newvalues = ''
    for value in aslist:
        try:
            newvalue = str(float(value.strip())/float(by))
            if newvalue[-2:] == '.0' and value[-2:] != '.0':
                newvalue = newvalue[:-2]
            tmplist.append(newvalue)
        except ValueError:
            print "EXCEPTION - ValueError divide: %s | %s" % (value.strip(), values)
        
    return ' '.join(tmplist)

def divide_or_multiply(key, values, by, separator):
    valueslist = values.strip().split(separator)
    if key in force_divide:
        return divide(values, by, " ")
    
    if len(valueslist) > 1:
        if float(valueslist[0]) < float(valueslist[len(valueslist)-1]):
            #last value is higher than first, then multiply
            return multiply(values, by, " ")
        elif float(valueslist[0]) == float(valueslist[len(valueslist)-1]):
            # same value, multiply
            return multiply(values, by, " ")
        else:
            #last value is lower than first, then divide
            return divide(values, by, " ")
    else:
        # only single element, then multiply (parse exceptions in dividelist...)
        return multiply(values, by, " ")
    return ' '.join(tmplist)

    
if __name__ == "__main__":

    # remove comments from file (there's bug in _custom that some comments have only an single slash instead of double slash...
    clean.remove_comments('npc_abilities.txt', 'npc_abilities_custom.tmp')

    kv = KeyValues()
    kv.load('npc_abilities_custom.tmp')

    root = KeyValues('DOTAAbilities')

    for factor in factors:
        for skill in kv:
            if skill in dont_parse:
                continue
            skillkv = KeyValues(skill)
            skillkv['BaseClass'] = skill

            for base in kv[skill]:
                base = str(base)
                if base != 'AbilitySpecial':
                    valueslist = kv[skill][base].strip().split(" ")
                    if base not in ignore_all_normal and str_to_type(valueslist[0]) in (int, long, float, complex):
                        skillkv[base] = divide_or_multiply(base, kv[skill][base], factor, " ")
                    else:
                        skillkv[base] = kv[skill][base]
                #print str(skillkv[base]) + ' = ' + str(kv[skill][base])
            
            if 'AbilitySpecial' in kv[skill]:
                abilityspecial = KeyValues('AbilitySpecial')
                for element in kv[skill]['AbilitySpecial']:
                    number = KeyValues(element)
                    for varElement in kv[skill]['AbilitySpecial'][element]:
                        numberValue = False
                        #print '%s -> %s' % (skill, varElement)
                       
                        testvalue = kv[skill]['AbilitySpecial'][element][varElement].split(" ")[0]
                        testinstance = str_to_type(testvalue)
                        if (skill in ignore_special and varElement in ignore_special[skill]) or (varElement in ignore_all_special):
                            print '###ignore: %s / %s [x%d]' % (skill, varElement, factor)
                        elif varElement != 'var_type' and testinstance in (int, long, float, complex):
                            varlist = kv[skill]['AbilitySpecial'][element][varElement]
                            numberValue = divide_or_multiply(varElement, varlist, factor, ' ')
                            """if '-' in varlist:
                                print 'negative: %s / %s -> %s' % (varlist, varElement, skill)
                                print 'negative2: %s / %s -> %s' % (numberValue, varElement, skill)      
                            """#print '%s old [x%d]: %s' % (varElement, factor, varlist) 
                            #print '%s new [x%d]: %s' % (varElement, factor, numberValue)
                        
                               
                        #check if variable number was defined
                        
                        if numberValue:
                            number[varElement] = numberValue
                        else:
                            number[varElement] = kv[skill]['AbilitySpecial'][element][varElement]
                            #print varElement
                            #print kv[skill]['AbilitySpecial'][element][varElement]
                    abilityspecial[element] = number
                #if usespec:
                skillkv['AbilitySpecial'] = abilityspecial
            root[skill + '_x'+str(factor)] = skillkv
    root.save('npc_abilities_custom.txt')
    os.remove('npc_abilities_custom.tmp')