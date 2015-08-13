from lib.keyvalues import KeyValues
from lib import clean
import abilities
import os
   
if __name__ == "__main__":

    # remove comments from file (there's bug in _custom that some comments have only an single slash instead of double slash...
    clean.remove_comments('item.txt', 'npc_abilities_override.tmp')

    kv = KeyValues()
    kv.load('npc_abilities_override.tmp')

    root = KeyValues('DOTAAbilities')

    for factor in abilitites.factors:
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
    root.save('npc_abilities_override.txt.txt')
    os.remove('npc_abilities_override.tmp')
