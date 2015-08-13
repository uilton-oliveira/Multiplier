#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
import os
import stat
import fileinput

addon_path_game = 'B:/Jogos/steam/steamapps/common/dota 2 beta/game/dota_addons/'
addon_path_content = 'B:/Jogos/steam/steamapps/common/dota 2 beta/content/dota_addons/'
addon_name = 'power_multiplier'
dev_path = u'D:/Programacao/Pessoal/LUA/dota2mods/Multiplier'
dev_path_game = u'D:/Programacao/Pessoal/LUA/dota2mods/Multiplier/Workshop/publish/game/dota_addons/'
dev_path_content = u'D:/Programacao/Pessoal/LUA/dota2mods/Multiplier/Workshop/publish/content/dota_addons/'

base_path_game = u'D:/Programacao/Pessoal/LUA/dota2mods/Multiplier/Workshop/base/game/dota_addons/'
base_path_content = u'D:/Programacao/Pessoal/LUA/dota2mods/Multiplier/Workshop/base/content/dota_addons/'


#npcs_to_copy = ['npc_abilities_custom.txt', 'npc_abilities_override.txt']
languages_to_copy = ['addon_english.txt']


def copyFile(src, dest):
    try:
        shutil.copy(src, dest)
    # eg. src and dest are the same file
    except shutil.Error as e:
        print('Error: %s' % e)
    # eg. source or destination doesn't exist
    except IOError as e:
        print('Error: %s' % e.strerror)

def copytree(src, dst, symlinks = False, ignore = None):
  if not os.path.exists(dst):
    os.makedirs(dst)
    shutil.copystat(src, dst)
  lst = os.listdir(src)
  if ignore:
    excl = ignore(src, lst)
    lst = [x for x in lst if x not in excl]
  for item in lst:
    s = os.path.join(src, item)
    d = os.path.join(dst, item)
    if symlinks and os.path.islink(s):
      if os.path.lexists(d):
        os.remove(d)
      os.symlink(os.readlink(s), d)
      try:
        st = os.lstat(s)
        mode = stat.S_IMODE(st.st_mode)
        os.lchmod(d, mode)
      except:
        pass # lchmod not available
    elif os.path.isdir(s):
      copytree(s, d, symlinks, ignore)
    else:
      shutil.copy2(s, d)

def updateAddons(fac, newDivValue, modID):
    fac_addon_name = addon_name + '_x' + str(fac)
    fac_override_file = "npc_abilities_override_x" + str(fac) + ".txt"    
    print '==== Updating Addon Folder ===='
    if os.path.exists(addon_path_game + fac_addon_name):
        print 'Removing dir: ' + addon_path_game + fac_addon_name
        shutil.rmtree(addon_path_game + fac_addon_name)
        os.makedirs(addon_path_game + fac_addon_name)
    if os.path.exists(addon_path_content + fac_addon_name):
        print 'Removing dir: ' + addon_path_content + fac_addon_name
        shutil.rmtree(addon_path_content + fac_addon_name)
        os.makedirs(addon_path_content + fac_addon_name)
    if os.path.exists(dev_path_game + fac_addon_name):
        print 'Removing dir: ' + dev_path_game + fac_addon_name
        shutil.rmtree(dev_path_game + fac_addon_name)
        os.makedirs(dev_path_game + fac_addon_name)
    if os.path.exists(dev_path_content + fac_addon_name):
        print 'Removing dir: ' + dev_path_content + fac_addon_name
        shutil.rmtree(dev_path_content + fac_addon_name)
        os.makedirs(dev_path_content + fac_addon_name)

    copytree(base_path_game + addon_name, dev_path_game + fac_addon_name)
    # replace variables
    # for line in fileinput.input(dev_path_game + fac_addon_name + '/scripts/vscripts/addon_game_mode.lua', inplace=True):
    #     newLine = line.replace('#FACTOR_HERE#', str(fac))
    #     newLine = newLine.replace('#DIV_VALUE_HERE#', newDivValue)
    #     #newLine = newLine.replace('#MOD_ID_HERE#', modID)
    #     print(newLine),

    for line in fileinput.input(dev_path_game + fac_addon_name + '/scripts/vscripts/util.lua', inplace=True):
        newLine = line.replace('#FACTOR_HERE#', str(fac))
        newLine = newLine.replace('#DIV_VALUE_HERE#', newDivValue)
        print(newLine),

        
    
    copytree(base_path_content + addon_name, dev_path_content + fac_addon_name)
    print 'Copying file: ' + fac_override_file
    copyFile(dev_path + '/tools/generator/' + fac_override_file, dev_path_game + fac_addon_name + '/scripts/npc/npc_abilities_override.txt')
    print 'Copying addon game to folder: ' + addon_path_game + fac_addon_name
    copytree(dev_path_game + fac_addon_name, addon_path_game + fac_addon_name)
    print 'Copying addon content to folder: ' +  addon_path_content + fac_addon_name
    copytree(dev_path_content + fac_addon_name, addon_path_content + fac_addon_name)
    
if __name__ == "__main__":
    updateAddons(2)
