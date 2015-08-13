from lib.keyvalues import KeyValues
from lib import clean
import abilities

import os
import codecs

tmpfix = ['DOTA_Tooltip_ability_item_boots_of_elves', 'DOTA_Tooltip_ability_item_belt_of_strength']
notname = ['_Lore', '_Description', '_Note0', '_radius', '_duration', '_bonus_armor'
                    '_bonus_movement_speed', '_bonus_damage', '_damage_pct', '_Note1']

# remove comments from file (there's bug in _custom that some comments have only an single slash instead of double slash...

if __name__ == "__main__":
    ff = codecs.open("addon_english.txt", "w", "utf16")
    ff.write('"lang"\r\n')
    ff.write('{\r\n')
    ff.write('   "Language"  "English"\r\n')
    ff.write('   "Tokens"\r\n')
    ff.write('   {\r\n')
    ff.write('      "game_mode_15"  "Custom Spell Power"\r\n')
    ff.write('      "addon_game_name"   "Custom Spell Power"\r\n')

    
    #strlist = []
    print 'Generating addon_english.txt'
    for factor in abilities.factors:
        #if factor == abilities.override_factor:
        #    print 'Ignoring override factor x%d...' % factor
        #    continue
        print 'Factor x%d...' % factor
        f = codecs.open("dota_english.txt", "r", "utf16")
        previous = ''
        lc = 0;
        for line in f:
            lc = lc + 1
            if line.strip().startswith('//'):
                continue
            var = line.split('"')
            if len(var) < 2:
                continue
            
            #change name of overwriten skills (comment, since it apparently still not work even with overwrite)
            #overwritten = var[1][len('DOTA_Tooltip_ability_'):]
            #if overwritten in abilities.override_instead and factor == abilities.override_factor:
                #ff.write('      "%s"    "%s [_x%d_]"\r\n' % (var[1], var[3], factor))
                #print overwritten
                    
            if 'DOTA_Tooltip_ability_' in line and '_item_' not in line:
                if previous != '' and previous in var[1]:
                    lg = len(previous)
                    name = '%s_x%d%s' % (previous, factor, var[1][lg:])
                    ff.write('      "%s"    "%s"\r\n' % (name, var[3]))
                else:
                    previous = var[1]
                    name = '%s_x%d' % (previous, factor)
                    chk =  var[1][var[1].rfind('_'):]
                    if chk not in notname:
                        ff.write('      "%s"    "%s [ x%d ]"\r\n' % (name, var[3], factor))
                    else:
                        ff.write('      "%s"    "%s"\r\n' % (name, var[3]))
                        
            elif 'DOTA_Tooltip_Ability_item_' in line:
                name = '%s_x%d' % (var[1], factor)
                ff.write('      "%s"    "%s"\r\n' % (name, var[3]))
            elif 'DOTA_Tooltip_ability_item_' in line:
                for fix in tmpfix:
                    if fix in var[1]:
                        previous = fix
                        if len(var[1]) > len(fix):
                            name = '%s_x%d%s' % (fix, factor, var[1][len(fix):])
                            ff.write('      "%s"    "%s"\r\n' % (name, var[3]))
                            break
                        else:
                            name = '%s_x%d%s' % (fix, factor, var[1])
                            ff.write('      "%s"    "%s"\r\n' % (name, var[3]))
                            break
                if '_Description' in var[1]:
                    previous = var[1][:-len('_Description')]
                    name = '%s_x%d_Description' % (previous, factor)
                    ff.write('      "%s"    "%s"\r\n' % (name, var[3]))
                elif '_Lore' in var[1]:
                    previous = var[1][:-len('_Lore')]
                    name = '%s_x%d_Lore' % (previous, factor)
                    ff.write('      "%s"    "%s"\r\n' % (name, var[3]))
                else:
                    lg = len(previous)
                    name = '%s_x%d%s' % (previous, factor, var[1][lg:])
                    ff.write('      "%s"    "%s"\r\n' % (name, var[3]))
        f.close()
    #print '\n'.join(strlist)
    ff.write('  }\r\n')
    ff.write('}\r\n')
    print 'ok'
    f.close()
    ff.close()

