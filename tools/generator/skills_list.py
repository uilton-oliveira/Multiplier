from lib.keyvalues import KeyValues
from lib import clean
import os

def inPartial(skillname, checkList):
    partial = False
    for check in checkList:
        if check in skillname:
            partial = True
            break
    return partial
   
if __name__ == "__main__":

    banSkills = ['ability_base', 'default_attack', 'attribute_bonus', 'courier_return_to_base', 'courier_go_to_secretshop', 'courier_transfer_items', 'courier_return_stash_items',
    'courier_take_stash_items', 'courier_morph', 'courier_shield', 'doom_bringer_empty1', 'doom_bringer_empty2', 'bane_nightmare_end', 'kunkka_return', 'morphling_morph',
    'morphling_morph_agi', 'morphling_morph_str', 'morphling_morph_replicate', 'beastmaster_call_of_the_wild_boar', 'beastmaster_boar_poison', 'beastmaster_greater_boar_poison',
    'templar_assassin_trap', 'templar_assassin_self_trap', 'life_stealer_consume', 'broodmother_spawn_spiderite', 'broodmother_poison_sting', 'chen_test_of_faith_teleport',
    'spectre_reality', 'ancient_apparition_ice_blast_release', 'alchemist_unstable_concoction_throw', 'forged_spirit_melting_strike', 'lone_druid_true_form_druid',
    'lone_druid_true_form_battle_cry', 'lone_druid_spirit_bear_return', 'brewmaster_storm_dispel_magic', 'brewmaster_earth_pulverize', 'shadow_demon_shadow_poison_release',
    'rubick_telekinesis_land', 'rubick_empty1', 'rubick_empty2', 'rubick_hidden1', 'rubick_hidden2', 'rubick_hidden3', 'naga_siren_song_of_the_siren_cancel', 'keeper_of_the_light_empty1',
    'keeper_of_the_light_empty2', 'keeper_of_the_light_blinding_light', 'keeper_of_the_light_illuminate_end', 'keeper_of_the_light_spirit_form_illuminate',
    'keeper_of_the_light_spirit_form_illuminate_end', 'keeper_of_the_light_spirit_form', 'visage_summon_familiars_stone_form', 'wisp_tether_break', 'wisp_spirits_in', 'wisp_spirits_out',
    'wisp_empty1', 'wisp_empty2', 'shredder_return_chakram', 'elder_titan_return_spirit', 'elder_titan_echo_stomp_spirit', 'abyssal_underlord_cancel_dark_rift',
    'phoenix_icarus_dive_stop', 'phoenix_sun_ray_stop', 'phoenix_sun_ray_toggle_move', 'phoenix_sun_ray_toggle_move_empty', 'phoenix_launch_fire_spirit', 'gnoll_assassin_envenomed_weapon',
    'ghost_frost_attack', 'neutral_spell_immunity', 'ogre_magi_frost_armor', 'dark_troll_warlord_raise_dead', 'satyr_hellcaller_shockwave', 'forest_troll_high_priest_heal',
    'harpy_storm_chain_lightning', 'blue_dragonspawn_sorcerer_evasion', 'blue_dragonspawn_overseer_evasion', 'blue_dragonspawn_overseer_devotion_aura', 'forest_troll_high_priest_mana_aura',
    'throw_snowball', 'luna_eclipse', 'throw_coal', 'healing_campfire', 'techies_focused_detonate', 'techies_remote_mines_self_detonate', 'techies_minefield_sign', 'ogre_magi_multicast',
    'morphling_replicate', 'ember_spirit_fire_remnant', 'ember_spirit_activate_fire_remnant', 'sandking_caustic_finale', 'tornado_tempest', 'granite_golem_hp_aura',
    'lone_druid_spirit_bear_demolish', 'lone_druid_true_form', 'beastmaster_hawk_invisibility', 'big_thunder_lizard_slam', 'big_thunder_lizard_frenzy', 'black_dragon_splash_attack',
    'satyr_hellcaller_unholy_aura', 'satyr_hellcaller_shockwave', 'satyr_soulstealer_mana_burn', 'satyr_trickster_purge', 'enraged_wildkin_toughness_aura', 'enraged_wildkin_tornado',
    'alpha_wolf_command_aura', 'alpha_wolf_critical_strike', 'giant_wolf_critical_strike', 'mud_golem_hurl_boulder', 'mud_golem_rock_destroy', 'dark_troll_warlord_ensnare',
    'ogre_magi_frost_armor', 'neutral_spell_immunity', 'polar_furbolg_ursa_warrior_thunder_clap', 'ghost_frost_attack', 'gnoll_assassin_envenomed_weapon', 'centaur_khan_war_stomp',
    'centaur_khan_endurance_aura', 'kobold_taskmaster_speed_aura', 'courier_burst', 'broodmother_spin_web_destroy', 'tusk_launch_snowball', 'shredder_return_chakram_2', 'troll_warlord_whirling_axes_ranged',
    'troll_warlord_whirling_axes_melee', 'troll_warlord_berserkers_rage', 'wisp_relocate', 'wisp_overcharge', 'wisp_spirits', 'keeper_of_the_light_recall', 'nyx_assassin_unburrow', 'nyx_assassin_burrow',
    'rubick_spell_steal', 'undying_tombstone_zombie_deathstrike', 'undying_tombstone_zombie_aura', 'ogre_magi_unrefined_fireblast', 'treant_eyes_in_the_forest', 'meepo_divided_we_stand', 'meepo_poof',
    'meepo_geostrike', 'brewmaster_fire_permanent_immolation', 'brewmaster_storm_wind_walk', 'brewmaster_storm_cyclone', 'brewmaster_earth_spell_immunity', 'brewmaster_earth_hurl_boulder',
    'lone_druid_spirit_bear_entangle', 'lone_druid_synergy', 'lycan_summon_wolves_invisibility', 'lycan_summon_wolves_critical_strike', 'doom_bringer_devour', 'broodmother_spawn_spiderlings',
    'night_stalker_darkness', 'night_stalker_hunter_in_the_night', 'enchantress_impetus', 'life_stealer_empty_4', 'life_stealer_empty_3', 'life_stealer_empty_2', 'life_stealer_empty_1', 'life_stealer_control',
    'life_stealer_consume', 'life_stealer_assimilate_eject', 'life_stealer_assimilate', 'dragon_knight_frost_breath', 'warlock_golem_permanent_immolation', 'warlock_golem_flaming_fists', 'sniper_take_aim',
    'riki_permanent_invisibility', 'puck_ethereal_jaunt', 'phantom_lancer_juxtapose', 'nevermore_shadowraze1', 'nevermore_shadowraze2', 'nevermore_shadowraze3', 'morphling_hybrid', 'drow_ranger_silence',
    'ability_deward', 'lone_druid_spirit_bear', 'shadow_demon_demonic_purge', 'tinker_rearm', 'lycan_summon_wolves', 'elder_titan_echo_stomp', 'shredder_chakram_2', 'tusk_ice_shards_stop', 'tusk_walrus_kick',
    'shoot_firework']

    banStartsWith = ['roshan_', 'greevil_', 'backdoor_', 'invoker_', 'earth_spirit_', 'cny', 'necronomicon_', 'abyssal_underlord_', 'earth_spirit_']

    #luna_eclipse disabled due crash issues
    #sandking_caustic_finale buggy with other skills
    #lycan_summon_wolves not working fine with other heroes

    # remove comments from file (there's bug in _custom that some comments have only an single slash instead of double slash...
    clean.remove_comments('npc_abilities.txt', 'skills_list.tmp')

    kv = KeyValues()
    kv.load('skills_list.tmp')

    root = KeyValues('DOTASkills')
    rootUlti = KeyValues('DOTAUltimates')

    for skill in kv:
        skillkv = KeyValues()
        if 'ID' in kv[skill]:
            if skill not in banSkills:
                if not inPartial(skill, banStartsWith):
                    if "AbilityType" in kv[skill] and kv[skill]["AbilityType"] == "DOTA_ABILITY_TYPE_ULTIMATE":
                        rootUlti[kv[skill]['ID']] = skill
                    else:
                        root[kv[skill]['ID']] = skill
    root.save('skillsList.kv')
    rootUlti.save('ultimatesList.kv')
    os.remove('skills_list.tmp')
    print 'finished'
