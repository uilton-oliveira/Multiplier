from lib.keyvalues import KeyValues
from lib import clean
from lib import update_addons
import os


force_divide = ['base_attack_time', 'transformation_time', 'attack_interval', 'structure_damage_mod', 'formation_time', 'transparency_fade', 'fixed_vision', 'slow_steps', 'visibility_radius']

specific_max_value = {'magic_resistance_pct':'35', 'magic_resistance':'75', 'bonus_magic_resistance':'45', 'bonus_magical_armor':'40', 'spell_resist_pct':'65', 'bonus_spell_resist':'60',
											'spell_resistance':'60', 'flesh_heap_magic_resist':'30',
											'kill_pct': '50', 'knockback_distance_max': '1000', 'knockback_max_distance': '1000', 'knockback_min': '500', 'knockback_max': '1000', 'knockback_distance': '1000',
											'trueshot_ranged_damage': '200 250 300 350', 'arrow_range': '10000', 'leap_distance': '1800', 'coil_radius': '900',
											'dragon_slave_distance': '2000', 'split_radius': '1000', 'ghostship_width': '850', 'ghostship_speed': '1300', 'structure_damage_mod': '0',
											'leap_speed': '2000', 'maim_chance': '50', 'health_regen_rate': '5', 'shadowraze_radius': '500', 'magic_resistance_aura': '50',
											'blink_range': '4500', 'modelscale': '100', 'model_scale': '100', 'str_scale_up': '10'}

more_specific_max_value = {'item_cloak':{'tooltip_resist':'40'},'item_hood_of_defiance':{'tooltip_resist':'60'},'item_pipe':{'tooltip_resist':'75', 'aura_radius': '1800'}, 'luna_eclipse': {'beams':'20 35 50', 'beams_scepter': '30 40 50', 'AbilityCastRange': '8000', 'beam_interval': '0.3 0.3 0.3'},
													 'jakiro_macropyre': {'cast_range': '1500', 'AbilityCastRange': '1500'}, 'jakiro_dual_breath': {'range': '1000', 'AbilityCastRange': '1000', 'speed': '1700'}, 'beastmaster_inner_beast': {'radius': '1500', 'bonus_attack_speed': '150'},
													 'tiny_toss': {'AbilityCastRange': '4500', 'tooltip_range': '4500', 'radius': '275 375 475 575'},
													 'morphling_waveform': {'AbilityCastRange': '4500', 'speed': '1800'}, 'phantom_lancer_doppelwalk': {'AbilityCastRange': '2500'},
													 'vengefulspirit_magic_missile': {'AbilityCastRange': '2000', 'magic_missile_speed': '1600'}, 'vengefulspirit_wave_of_terror': {'AbilityCastRange': '2000', 'wave_speed': '4000', 'armor_reduction': '-16 -17 -18 -19'},
													 'vengefulspirit_nether_swap': {'AbilityCastRange': '4500'}, 'beastmaster_wild_axes': {'range': '2000', 'AbilityCastRange': '2000'},
													 'crystal_maiden_crystal_nova': {'AbilityCastRange': '1500'}, 'puck_illusory_orb': {'max_distance': '4500'}, 'ember_spirit_searing_chains': {'radius': '1200', 'AbilityCastRange': '1200'},
													 'ember_spirit_sleight_of_fist': {'radius': '1100', 'AbilityCastRange': '900', 'bonus_hero_damage': '1000'}, 'lina_laguna_blade': {'AbilityCastRange': '1500'}, 'windrunner_powershot': {'arrow_range': '6500'},
													 'winter_wyvern_winters_curse': {'radius': '1000'}, 'tinker_laser': {'AbilityCastRange': '900', 'cast_range_tooltip': '900', 'cast_range_scepter': '900'}, 'tinker_heat_seeking_missile': {'radius': '3500', 'speed': '1800'},
													 'dark_seer_vacuum': {'AbilityCastRange': '1000'}, 'pudge_meat_hook': {'hook_distance': '8000', 'AbilityCastRange': '8000', 'hook_speed': '4000'},
													 'slark_pounce': {'pounce_distance': '1800', 'pounce_speed': '1500'}, 'lich_frost_nova': {'AbilityCastRange': '1500'}, 'lich_chain_frost': {'AbilityCastRange': '1500'},
													 'obsidian_destroyer_astral_imprisonment': {'steal_duration': '180'}, 'sven_storm_bolt': {'AbilityCastRange': '1500'}, 'tiny_avalanche': {'AbilityCastRange': '1500', 'radius': '475 575 675 775'},
													 'kunkka_torrent': {'AbilityCastRange': '1500'}, 'kunkka_ghostship': {'ghostship_distance': '1500', 'AbilityCastRange': '1500'},
													 'dragon_knight_breathe_fire': {'range': '1000', 'AbilityCastRange': '1000'}, 'necrolyte_heartstopper_aura': {'aura_radius': '2800'}, 'necrolyte_reapers_scythe': {'AbilityCastRange': '1500', 'damage_per_health': '0.6 0.9 1.2', 'damage_per_health_scepter': '0.8 1.0 1.4'},
													 'bounty_hunter_shuriken_toss': {'AbilityCastRange': '1500', 'speed': '2500'}, 'juggernaut_omni_slash': {'AbilityCastRange': '1000'}, 'phantom_lancer_spirit_lance': {'AbilityCastRange': '1500', 'lance_speed': '2800', 'fake_lance_distance': '1400'},
													 'drow_ranger_wave_of_silence': {'AbilityCastRange': '1500'}, 'antimage_mana_void': {'AbilityCastRange': '1500'}, 'morphling_adaptive_strike': {'AbilityCastRange': '1000'},
													 'crystal_maiden_frostbite': {'AbilityCastRange': '1500'}, 'zuus_arc_lightning': {'AbilityCastRange': '1200'}, 'zuus_lightning_bolt': {'AbilityCastRange': '1200'},
													 'puck_dream_coil': {'AbilityCastRange': '1500'}, 'lina_light_strike_array': {'AbilityCastRange': '1500'}, 'shadow_shaman_shackles': {'AbilityCastRange': '1200'},
													 'shadow_shaman_voodoo': {'AbilityCastRange': '1250', 'movespeed': '50'}, 'shadow_shaman_mass_serpent_ward': {'AbilityCastRange': '1000'},
													 'warlock_upheaval': {'AbilityCastRange': '1200'}, 'omniknight_purification': {'AbilityCastRange': '1500'}, 'omniknight_degen_aura': {'radius': '800', 'AbilityCastRange': '800', 'speed_bonus': '-35 -45 -55 -65', 'attack_bonus_tooltip': '-35 -45 -55 -65'},
													 'tidehunter_anchor_smash': {'radius': '900', 'AbilityCastRange': '900'}, 'tidehunter_gush': {'AbilityCastRange': '1500', 'projectile_speed': '5000', 'armor_bonus': '-7 -8 -9 -10'},
													 'tidehunter_ravage': {'radius': '3000', 'speed': '1400'}, 'treant_leech_seed': {'AbilityCastRange': '1500'},
													 'huskar_inner_vitality': {'AbilityCastRange': '2000', 'heal': '50', 'attrib_bonus': '0.2 0.3 0.4 0.5', 'tooltip_attrib_bonus': '20 30 40 50', 'hurt_attrib_bonus': '0.5 0.7 0.9 1.1', 'tooltip_hurt_attrib_bonus': '50 70 90 110'},
													 'legion_commander_duel': {'AbilityCastRange': '600'}, 'legion_commander_overwhelming_odds': {'AbilityCastRange': '600'},
													 'skywrath_mage_arcane_bolt': {'AbilityCastRange': '900', 'int_multiplier': '3.5', 'bolt_speed': '1000'}, 'skywrath_mage_concussive_shot': {'AbilityCastRange': '2000', 'launch_radius': '2000', 'speed': '1500'},
													 'skywrath_mage_ancient_seal': {'AbilityCastRange': '800'},
													 'disruptor_thunder_strike': {'AbilityCastRange': '1500'}, 'disruptor_kinetic_field': {'AbilityCastRange': '1500'}, 'disruptor_static_storm': {'AbilityCastRange': '1500'},
													 'disruptor_kinetic_field': {'formation_time': '0.1'}, 'axe_berserkers_call': {'radius': '1200'}, 'axe_battle_hunger': {'AbilityCastRange': '1500'},
													 'jakiro_ice_path': {'AbilityCastRange': '2000', 'path_delay': '0.1'}, 'leshrac_split_earth': {'AbilityCastRange': '1500', 'delay': '0.18'},
													 'ancient_apparition_cold_feet': {'AbilityCastRange': '1500'}, 'ancient_apparition_ice_vortex': {'AbilityCastRange': '2000', 'movement_speed_pct': ' -32 -43 -54 -65', 'spell_resist_pct': '-60 -90 -120 -150'},
													 'ancient_apparition_ice_blast': {'kill_pct': '40.0'}, 'enchantress_impetus': {'AbilityCastRange': '800', 'bonus_attack_range_scepter': '700', 'distance_damage_pct': '90.0 100.0 110.0'},
													 'invoker_chaos_meteor': {'travel_speed': '500', 'AbilityCastRange': '1400'}, 'invoker_tornado': {'travel_speed': '3000', 'AbilityCastRange': '6400'},
													 'invoker_cold_snap': {'AbilityCastRange': '2000'}, 'invoker_emp': {'AbilityCastRange': '1500'}, 'invoker_deafening_blast': {'travel_distance': '2000', 'travel_speed': '2200'},
													 'templar_assassin_psionic_trap': {'AbilityCastRange': '4000'}, 'venomancer_poison_nova': {'speed': '1400', 'radius': '1000'}, 'venomancer_venomous_gale': {'speed': '2000', 'AbilityCastRange': '1700'},
													 'dazzle_poison_touch': {'AbilityCastRange': '1500'}, 'dazzle_shadow_wave': {'AbilityCastRange': '2000'}, 'dazzle_weave': {'AbilityCastRange': '8000', 'radius': '800', 'radius_scepter': '1200', 'armor_per_second': '1.75 2 2.25', 'armor_per_second_scepter': '2.25 2.5 2.75'},
													 'phoenix_icarus_dive': {'dash_length': '3800'}, 'phoenix_fire_spirits': {'AbilityCastRange': '2500', 'spirit_count': '20'}, 'phoenix_sun_ray': {'AbilityCastRange': '2500', 'beam_range': '2500', 'ally_heal': '2'},
													 'phoenix_launch_fire_spirit': {'AbilityCastRange': '2500', 'spirit_count': '20'}, 'oracle_fortunes_end': {'AbilityCastRange': '1500', 'radius': '500'},
													 'oracle_fates_edict': {'AbilityCastRange': '1500', 'damage_amp': '500'}, 'oracle_purifying_flames': {'AbilityCastRange': '1600'}, 'witch_doctor_maledict': {'AbilityCastRange': '900'},
													 'witch_doctor_death_ward': {'AbilityCastRange': '1100'}, 'witch_doctor_paralyzing_cask': {'AbilityCastRange': '1400', 'speed': '1800'},
													 'lion_finger_of_death': {'AbilityCastRange': '1800', 'damage_delay': '0.1', 'splash_radius_scepter': '400'}, 'lion_voodoo': {'AbilityCastRange': '1000'},
													 'lion_impale': {'AbilityCastRange': '1200', 'length': '1200', 'speed': '2500'}, 'nyx_assassin_impale': {'AbilityCastRange': '1100', 'length': '1100', 'speed': '2500'},
													 'nyx_assassin_mana_burn': {'AbilityCastRange': '1200'}, 'nyx_assassin_spiked_carapace': {'burrow_aoe': '300'}, 'naga_siren_mirror_image': {'images_count': '7 8 9 10'},
													 'naga_siren_ensnare': {'net_speed': '2000', 'AbilityCastRange': '1500'}, 'keeper_of_the_light_illuminate': {'AbilityCastRange': '2200', 'range': '2200', 'speed': '1800.0'},
													 'keeper_of_the_light_mana_leak': {'AbilityCastRange': '1500', 'mana_leak_pct': '15'}, 'keeper_of_the_light_blinding_light': {'AbilityCastRange': '1800', 'radius': '1000'},
													 'lycan_shapeshift': {'speed': '1200', 'transformation_time': '0.5'}, 'lycan_summon_wolves_invisibility': {'fade_delay': '1.0'},
													 'warlock_fatal_bonds': {'AbilityCastRange': '2500', 'search_aoe': '1000', 'damage_share_percentage': '60'},
													 'warlock_shadow_word': {'AbilityCastRange': '1200'}, 'skeleton_king_reincarnation': {'scepter_duration': '10'},
													 'skeleton_king_hellfire_blast': {'blast_speed': '2500', 'AbilityCastRange': '1000' }, 'visage_grave_chill': {'AbilityCastRange': '1200'}, 'visage_soul_assumption': {'AbilityCastRange': '1800'},
													 'rubick_fade_bolt': {'AbilityCastRange': '1300'}, 'rubick_telekinesis': {'AbilityCastRange': '3000', 'cast_range_tooltip': '3000', 'max_land_distance': '3000', 'max_land_distance_allied': '3000'},
													 'rubick_null_field': {'radius': '1500'}, 'rubick_spell_steal': {'projectile_speed': '1800', 'AbilityCastRange': '4500', 'cast_range_scepter': '8500'},
													 'leshrac_lightning_storm': {'AbilityCastRange': '1500', 'jump_delay': '0.1'}, 'enigma_black_hole': {'AbilityCastRange': '800', 'far_radius': '1500', 'near_radius': '700', 'pull_radius': '1500'},
													 'enigma_midnight_pulse': {'radius': '1000', 'AbilityCastRange': '1200'}, 'enigma_demonic_conversion': {'AbilityCastRange': '1400'},
													 'enigma_malefice': {'AbilityCastRange': '1200'}, 'gyrocopter_homing_missile': {'AbilityCastRange': '2100', 'speed': '650'}, 'gyrocopter_call_down': {'AbilityCastRange': '2000'},
													 'lycan_feral_impulse': {'bonus_damage': '30 40 50 60', 'radius': '1800', 'bonus_attack_speed': '20 30 40 50'}, 'item_diffusal_blade': {'feedback_mana_burn': '300', 'damage_per_burn': '3.0'},
													 'item_diffusal_blade_2': {'feedback_mana_burn': '300', 'damage_per_burn': '3.0'}, 'antimage_mana_break': {'damage_per_burn': '2.0', 'mana_per_hit': '200 300 400 500'},
													 'sandking_burrowstrike': {'AbilityCastRange': '2500', 'tooltip_range': '2500'}, 'bounty_hunter_track': {'AbilityCastRange': '2500', 'aura_radius': '1800', 'bonus_gold_self': '500 750 1000', 'bonus_gold': '200 350 500'},
													 'chen_penitence': {'AbilityCastRange': '1500', 'bonus_damage_taken': '150', 'speed': '2800'}, 'chen_test_of_faith': {'AbilityCastRange': '1200'}, 'chen_holy_persuasion': {'max_units': '20'},
													 'bane_brain_sap': {'AbilityCastRange': '1800'}, 'bane_fiends_grip': {'AbilityCastRange': '1300'}, 'alchemist_acid_spray': {'AbilityCastRange': '1800', 'armor_reduction': '17 18 19 20', 'radius': '1000'},
													 'alchemist_unstable_concoction_throw': {'AbilityCastRange': '1500'},
													 'techies_land_mines': {'small_radius': '400', 'big_radius': '600', 'activation_time': '0.1', 'explode_delay': '0.1', 'fade_time': '0.5', 'damage': '3500 4500 5500 6500'},
													 'techies_stasis_trap': {'explode_delay': '0.5', 'activation_time': '0.5', 'fade_time': '0.5'}, 'techies_suicide': {'AbilityCastRange': '400', 'small_radius': '500', 'big_radius': '800', 'damage': '5000 6500 8500 11500', 'partial_damage': '2600 3000 3400 3800'},
													 'techies_remote_mines': {'AbilityCastRange': '1200', 'radius': '650', 'activation_time': '0.5', 'cast_range_tooltip': '1200', 'radius_scepter': '900', 'cast_range_scepter': '2200', 'damage': '2500 3500 4000'},
													 'item_veil_of_discord': {'AbilityCastRange': '2000', 'debuff_radius': '1500', 'resist_debuff': '-60'}, 'item_ethereal_blade': {'ethereal_damage_bonus': '-180'},
													 'doom_bringer_lvl_death': {'AbilityCastRange': '1200', 'lvl_bonus_damage': '50'}, 'doom_bringer_doom': {'AbilityCastRange': '1100'}, 'doom_bringer_devour': {'AbilityCastRange': '1000', 'bonus_gold': '300 400 500 600'},
													 'item_hand_of_midas': {'bonus_gold': '1000', 'xp_multiplier': '10', 'bonus_attack_speed': '100'}, 'ogre_magi_fireblast': {'AbilityCastRange': '900', 'multicast_delay': '1'},
													 'ogre_magi_unrefined_fireblast': {'AbilityCastRange': '900', 'multicast_delay': '1'},
													 'ogre_magi_ignite': {'AbilityCastRange': '1500', 'slow_movement_speed_pct': '-60', 'projectile_speed': '2500', 'multicast_delay': '0.2'},
													 'ogre_magi_bloodlust': {'AbilityCastRange': '6500', 'modelscale': '50'}, 'silencer_curse_of_the_silent': {'AbilityCastRange': '1600'}, 'silencer_glaives_of_wisdom': {'intellect_damage_pct': '60 80 100 120'},
													 'silencer_last_word': {'AbilityCastRange': '1600'}, 'magnataur_skewer': {'range': '3000', 'slow_pct': '60', 'skewer_radius': '500', 'skewer_speed': '2000'},
													 'nevermore_dark_lord': {'presence_radius': '1900', 'AbilityCastRange': '1900', 'presence_armor_reduction': '-11 -13 -15 -18'}, 'magnataur_shockwave': {'AbilityCastRange': '1700', 'shock_speed': '2000', 'shock_distance': '1700'},
													 'shredder_whirling_death': {'AbilityCastRange': '550', 'whirling_radius': '550'}, 'shredder_timber_chain': {'speed': '4000', 'range': '3100', 'AbilityCastRange': '3000'},
													 'razor_plasma_field': {'speed': '800'}, 'death_prophet_carrion_swarm': {'AbilityCastRange': '1000', 'range': '1200', 'speed': '1800'}, 'queenofpain_sonic_wave': {'AbilityCastRange': '1500', 'speed': '1100'},
													 'queenofpain_shadow_strike': {'AbilityCastRange': '1200', 'cast_range_tooltip': '1200', 'projectile_speed': '1700'}, 'queenofpain_scream_of_pain': {'area_of_effect': '850', 'projectile_speed': '1800'},
													 'venomancer_plague_ward': {'AbilityCastRange': '2000'}, 'faceless_void_time_walk': {'speed': '4500', 'AbilityCastRange': '4500', 'tooltip_range': '4500', 'radius': '650'},
													 'rattletrap_rocket_flare': {'speed': '3000'}, 'rattletrap_hookshot': {'speed': '4500'}, 'weaver_the_swarm': {'AbilityCastRange': '8000', 'speed': '1400', 'destroy_attacks': '20', 'armor_reduction': '1 1 2 3'},
													 'batrider_flamebreak': {'AbilityCastRange': '2500', 'speed': '1500'}, 'batrider_sticky_napalm': {'AbilityCastRange': '1400', 'radius': '600', 'turn_rate_pct': '-85', 'movement_speed_pct': '-19 -21 -23 -25'},
													 'batrider_flaming_lasso': {'drag_distance': '1500', 'AbilityCastRange': '1300', 'break_distance': '1700'}, 'spectre_spectral_dagger': {'AbilityCastRange': '4500', 'speed': '1500'},
													 'brewmaster_earth_hurl_boulder': {'AbilityCastRange': '1600', 'speed': '1500'}, 'shadow_demon_shadow_poison': {'speed': '1800', 'AbilityCastRange': '4000'},
													 'meepo_earthbind': {'AbilityCastRange': '2200', 'tooltip_range': '2200', 'speed': '1400'}, 'shredder_chakram': {'speed': '1300', 'AbilityCastRange': '1200', 'break_distance': '2000', 'radius': '200'},
													 'shredder_chakram_2': {'speed': '1300', 'AbilityCastRange': '1200', 'break_distance': '2000', 'radius': '200'}, 'elder_titan_ancestral_spirit': {'speed': '1200', 'AbilityCastRange': '2400', 'radius': '500'},
													 'elder_titan_earth_splitter': {'AbilityCastRange': '3000', 'crack_distance': '3000'}, 'ember_spirit_activate_fire_remnant': {'speed': '2000'}, 'earth_spirit_rolling_boulder': {'speed': '1500', 'rock_speed': '1900'},
													 'earth_spirit_geomagnetic_grip': {'speed': '1500'}, 'mud_golem_hurl_boulder': {'AbilityCastRange': '1600', 'speed': '1500'},
													 'satyr_hellcaller_shockwave': {'speed': '1800', 'distance': '1500', 'AbilityCastRange': '1200'}, 'techies_minefield_sign': {'AbilityCastRange': '500', 'aura_radius': '1000'},
													 'spirit_breaker_empowering_haste': {'aura_radius': '1800'}, 'item_ward_sentry': {'true_sight_range': '1500', 'AbilityCastRange': '2500'}, 'item_ward_observer': {'vision_range': '4000', 'AbilityCastRange': '2500'},
													 'item_ward_dispenser': {'true_sight_range': '1500'}, 'phantom_assassin_phantom_strike': {'AbilityCastRange': '4500', 'tooltip_range': '4500'}, 'phantom_assassin_stifling_dagger': {'AbilityCastRange': '2500'},
													 'phantom_lancer_phantom_edge': {'max_distance': '4500'}, 'item_blink': {'AbilityCastRange': '4500', 'blink_range_clamp': '6000'},
													 'templar_assassin_refraction': {'instances':'16'}, 'templar_assassin_meld': {'bonus_armor': '-30'}, 'ember_spirit_fire_remnant': {'speed_multiplier': '500'},
													 'medusa_mystic_snake': {'AbilityCastRange': '1300', 'snake_jumps': '10 15 20 25', 'initial_speed': '1600', 'return_speed': '1600', 'radius': '600 700 800 900'},
													 'pugna_life_drain': {'AbilityCastRange': '1600', 'cast_range_tooltip': '1600'},
													 'storm_spirit_ball_lightning': {'ball_lightning_travel_cost_base': '60', 'ball_lightning_travel_cost_percent': '3.0'},
													 'terrorblade_metamorphosis': {'bonus_range': '600'}, 'furion_sprout': {'AbilityCastRange': '1400', 'cast_range_tooltip': '1400'},
													 'item_glimmer_cape': {'active_magical_armor': '100'}, 'treant_natures_guise': {'radius': '700'}, 'abaddon_death_coil': {'self_damage': '450'},
													 'storm_spirit_electric_vortex': {'AbilityCastRange': '1000', 'electric_vortex_pull_tether_range': '2600', 'electric_vortex_pull_units_per_second': '300'},
													 'riki_smoke_screen': {'AbilityCastRange': '1800'}, 'riki_blink_strike': {'AbilityCastRange': '4500'}, 'item_vladmir': {'aura_radius': '5000', 'vampiric_aura': '70', 'vampiric_aura_ranged': '60', 'damage_aura': '35'},
													 'item_ancient_janggo': {'radius': '5000', 'bonus_movement_speed_pct': '40', 'bonus_attack_speed_pct': '300', 'bonus_aura_movement_speed_pct': '20', 'bonus_aura_attack_speed_pct': '150'},
													 'bloodseeker_bloodrage': {'damage_increase_pct': '60 90 120 150'}, 'tusk_ice_shards': {'AbilityCastRange': '5000'},
													 'night_stalker_void': {'AbilityCastRange': '1800'}, 'undying_decay': {'AbilityCastRange': '1500'},
													 'tusk_snowball': {'snowball_speed': '2000', 'AbilityCastRange': '4500', 'snowball_windup_radius': '200', 'snowball_radius': '600', 'snowball_grow_rate': '70'},
													 'spirit_breaker_nether_strike': {'AbilityCastRange': '2000', 'tooltip_range': '2000', 'cast_range_scepter': '4000'},
													 'item_power_treads': {'bonus_movement_speed': '100', 'bonus_attack_speed': '90'}, 'item_recipe_arcane_boots': {'bonus_movement': '110'},
													 'item_phase_boots': {'phase_movement_speed': '50', 'bonus_movement_speed': '100'},
													 'item_travel_boots': {'bonus_movement_speed': '200'}, 'item_travel_boots_2': {'bonus_movement_speed': '200'}, 'item_tranquil_boots': {'bonus_movement_speed': '150', 'broken_movement_speed': '100'},
													 'item_desolator': {'corruption_armor': '-20'}, 'item_satanic': {'lifesteal_percent': '100', 'unholy_lifesteal_percent': '400', 'unholy_lifesteal_total_tooltip': '500'},
													 'item_mask_of_madness': {'lifesteal_percent': '50', 'berserk_extra_damage': '60', 'berserk_bonus_attack_speed': '250', 'berserk_bonus_movement_speed': '30'},
													 'item_quelling_blade': {'damage_bonus': '400', 'damage_bonus_ranged': '350'}, 'item_bfury': {'quelling_bonus': '450', 'quelling_bonus_ranged': '400', 'cleave_damage_percent': '50', 'cleave_radius': '600'},
													 'item_orb_of_venom': {'poison_movement_speed_melee': '-30', 'poison_movement_speed_range': '-20'},
													 'item_lifesteal': {'lifesteal_percent': '40'}, 'skeleton_king_vampiric_aura': {'vampiric_aura': '40 50 60 70'},
													 'antimage_spell_shield': {'spell_shield_resistance': '40 50 60 70'}, 'chaos_knight_phantasm': {'images_count': '3 4 5'},
													 'rubick_null_field': {'magic_damage_reduction_pct':'20 23 25 30'}, 'sniper_take_aim': {'bonus_attack_range': '250 350 450 650'},
													 'templar_assassin_psi_blades': {'bonus_attack_range': '350 450 550 650'}, 'item_manta': {'images_count': '5'}, 'medusa_mana_shield': {'damage_per_mana': '3.2 3.8 4.4 5.0'},
													 'item_helm_of_the_dominator': {'lifesteal_percent': '70'}, 'treant_living_armor': {'damage_count': '10 17 25 35'},
													 'ursa_enrage': {'enrage_multiplier': '2 3 4', 'damage_reduction': '98'}, 'ursa_overpower': {'max_attacks': '5 10 15 20'},
													 'ursa_earthshock': {'movement_slow': '-40 -60 -80 -100'}, 'furion_wrath_of_nature': {'max_targets': '60', 'max_targets_scepter': '120'},
													 'item_force_staff': {'push_length': '1200', 'AbilityCastRange': '1400'}, 'shadow_demon_soul_catcher': {'AbilityCastRange': '1200', 'bonus_damage_taken': '100 110 120 130'},
													 'shadow_demon_disruption': {'AbilityCastRange': '1200'},
													 'shadow_demon_demonic_purge': {'AbilityCastRange': '1600'}, 'item_smoke_of_deceit': {'200'}, 'item_assault': {'aura_negative_armor': '-15'},
													 'item_medallion_of_courage': {'armor_reduction': '-20'}, 'item_solar_crest': {'armor_reduction': '-25', 'enemy_armor_reduction_tooltip': '-25', 'allied_evasion': '75'},
													 'item_orchid': {'bonus_damage': '90', 'silence_damage_percent': '50'}, 'viper_corrosive_skin': {'bonus_movement_speed': '-20 -25 -30 -35', 'bonus_attack_speed': '-30 -45 -50 -65'},
													 'item_octarine_core': {'hero_lifesteal': '50', 'creep_lifesteal': '10'}, 'axe_culling_blade': {'AbilityCastRange': '300'},
													 'bloodseeker_thirst': {'bonus_movement_speed': '100 150 200 250', 'bonus_damage': '60 80 100 120'},
													 'slardar_amplify_damage': {'armor_reduction': '-30 -35 -40'}, 'slark_essence_shift': {'agi_gain': '30'},
													 'sven_gods_strength': {'gods_strength_damage': '200 300 400', 'gods_strength_damage_scepter': '100 125 150'},
													 'item_sange_and_yasha': {'movement_speed_percent_bonus': '30'}, 'item_yasha': {'movement_speed_percent_bonus': '25'},
													 'obsidian_destroyer_sanity_eclipse': {'1000 1250 1500'}, 'naga_siren_rip_tide': {'armor_reduction': '-13 -14 -15 -16'},
													 'troll_warlord_whirling_axes_ranged': {'axe_range': '1500', 'axe_speed': '3000'}, 'troll_warlord_whirling_axes_melee': {'max_range': '950'},
													 'enchantress_untouchable': {'slow_attack_speed': '-70 -100 -130 -160'}, 'item_stout_shield': {'block_chance': '80'}, 'item_vanguard': {'block_chance': '90'},
													 'item_crimson_guard': {'block_chance': '100', 'block_chance_active': '100'}, 'lich_frost_armor': {'armor_bonus': '10 14 18 22'},
													 'troll_warlord_berserkers_rage': {'base_attack_time': '1.3'}, 'winter_wyvern_winters_curse': {'AbilityCastRange': '1800'},
													 'winter_wyvern_cold_embrace': {'AbilityCastRange': '3000'}, 'winter_wyvern_splinter_blast': {'AbilityCastRange': '2500', 'projectile_speed': '1500', 'secondary_projectile_speed': '1500'},
													 'chaos_knight_reality_rift': {'cast_range': '4500', 'AbilityCastRange': '4500'}, 'chaos_knight_chaos_bolt': {'AbilityCastRange': '1200', 'chaos_bolt_speed': '3000'},
													 'sven_great_cleave': {'great_cleave_damage': '50 55 60 65', 'great_cleave_radius': '600'}, 'magnataur_empower': {'cleave_damage_pct': '30 40 50 60', 'cleave_radius': '500'},
													 'magnataur_reverse_polarity': {'pull_radius': '1500'},
													 'bristleback_viscous_nasal_goo': {'base_move_slow': '30', 'move_slow_per_stack': '12 15 18 21', 'stack_limit': '6', 'AbilityCastRange': '2000'},
													 'bristleback_bristleback': {'back_damage_reduction': '30 40 50 60'}, 'bristleback_warpath': {'stack_duration': '20.0', 'damage_per_stack': '200 250 300'},
													 'luna_lucent_beam': {'AbilityCastRange': '1500'}, 'luna_moon_glaive': {'damage_reduction_percent': '15', 'bounces': '10 20 30 40'},
													 'luna_lunar_blessing': {'radius': '2500', 'bonus_night_vision': '3000'}, 'tiny_grow': {'bonus_cleave_radius_scepter': '600'},
													 'item_maelstrom': {'chain_radius': '1400', 'chain_strikes': '25', 'chain_delay': '0.05'},
													 'item_mjollnir': {'static_strikes': '25', 'static_primary_radius': '900', 'static_seconary_radius': '1400', 'static_radius': '1400', 'chain_radius': '1400', 'chain_strikes': '40', 'chain_delay': '0.05'},
													 'earthshaker_enchant_totem': {'totem_damage_percentage': '700 900 1200 1500'}, 'medusa_split_shot': {'arrow_count': '4 6 8 10'},
													 'phantom_lancer_juxtapose': {'proc_chance_pct': '45 55 65', 'illusion_proc_chance_pct': '20'}, 'drow_ranger_trueshot': {'trueshot_ranged_damage': '30 54 70 96'},
													 'nyx_assassin_burrow': {'damage_reduction': '90'}, 'life_stealer_infest': {'AbilityCastRange': '1500', 'radius': '1500'}, 'life_stealer_open_wounds': {'AbilityCastRange': '600 800 1000 1200'},
													 'life_stealer_feast': {'hp_leech_percent': '9 11 13 15'}, 'spirit_breaker_greater_bash': {'50 100 150 200'}}


multiply_all_by_fixed_factor = {'bonus_armor': 3, 'aura_armor_bonus': 3, 'aura_armor': 3, 'heal_bonus_armor': 3, 'armor_aura': 3, 'bonus_aoe_armor': 3, 'aura_bonus_armor': 3, 'aura_positive_armor': 3, 'allied_armor': 3,
	'warcry_armor': 3, 'spirit_armor': 3,	'bear_armor': 3, 'familiar_armor': 3}

ignore_all_special = [ 'enemy_armor_reduction_tooltip', 'armor_per_stack', 'crit_chance', 'duration', 'bonus_evasion', 'miss_chance', 'dodge_chance', 'evasion_chance_pct', 'miss_duration',
											'illusion_damage_out_pct', 'illusion_damage_in_pct', 'illusion_damage_incoming', 'illusion_damage_outgoing', 'incoming_damage', 'illusion_outgoing_damage', 'tooltip_illusion_total_damage_incoming',
											'illusion_incoming_damage', 'illusion_outgoing_tooltip', 'shadowraze_range', 'miss_rate', 'tick_rate', 'tick_interval', 'incoming_damage_tooltip',
											'delay', 'tooltip_delay', 'light_strike_array_delay_time', 'damage_delay', 'static_remnant_delay', 'sand_storm_invis_delay', 'jump_delay',
											'bounce_delay', 'idle_invis_delay', 'fire_delay', 'path_delay', 'hero_teleport_delay', 'attack_delay', 'multicast_delay', 'teleport_delay',
											'stun_delay', 'cast_delay', 'activation_delay', 'rock_explosion_delay', 'first_wave_delay', 'explode_delay', 'cooldown_scepter', 'tooltip_illusion_damage_out_pct',
											'omni_slash_cooldown_scepter', 'epicenter_cooldown_scepter', 'nether_swap_cooldown_scepter', 'scepter_cooldown', 'replica_damage_outgoing_scepter',
											'tooltip_outgoing_scepter', 'mana_cost_per_second', 'stun_duration', 'light_strike_array_stun_duration', 'arrow_min_stun', 'extra_phantasm_chance_pct_tooltip',
											'arrow_max_stun', 'stun_min', 'stun_max', 'coil_stun_duration', 'blast_stun_duration', 'bolt_stun_duration', 'stun_chance', 'magic_missile_stun',
											'fail_stun_duration', 'min_stun', 'max_stun', 'stun_delay', 'hero_stun_duration', 'creep_stun_duration', 'initial_stun_duration', 'sleep_duration',
											'non_hero_stun_duration', 'magic_missile_stun', 'cast_animation', 'stun_radius', 'lift_duration', 'silence_duration', 'knockback_duration', 'fade_time',
											'shock_radius', 'pre_flight_time', 'fiend_grip_tick_interval', 'fiend_grip_duration', 'fiend_grip_duration_scepter',
											'illusion_incoming_dmg_pct_tooltip', 'duration', 'tooltip_duration', 'duration_scepter', 'bash_chance', 'bonus_range', 'bonus_range_scepter', 'bonus_cleave_damage_scepter',
											'trance_duration', 'blind_duration', 'blind_pct', 'whirl_duration', 'projectile_duration', 'slow_duration', 'pause_duration', 'purge_frequency', 'strike_interval',
											'strike_interval_scepter', 'blast_dot_duration', 'tooltip_slow_duration', 'last_proc', 'crush_radius', 'crush_extra_slow_duration', 'charge_restore_time',
											'echo_slam_damage_range', 'echo_slam_echo_search_range', 'echo_slam_echo_range', 'blade_dance_crit_chance', 'blade_fury_radius', 'blade_fury_damage_tick',
											'healing_ward_aura_radius', 'omni_slash_radius', 'omni_slash_bounce_tick', 'illusion_duration', 'tooltip_attack_range', 'multicast_delay', 'scepter_mana',
											'multicast_2_times', 'multicast_3_times', 'multicast_4_times', 'fireblast_mana_cost', 'fireblast_cooldown', 'ignite_aoe', 'bloodlust_cooldown',
											'multicast_2_times_tooltip', 'multicast_3_times_tooltip', 'multicast_4_times_tooltip', 'outgoing_damage', 'incoming_damage', 'invuln_duration', 'outgoing_damage_tooltip',
											'burrow_duration', 'burrow_anim_time', 'burrow_width', 'sand_storm_radius', 'caustic_finale_radius', 'caustic_finale_duration', 'epicenter_radius',
											'necromastery_max_souls', 'necromastery_soul_release', 'requiem_radius', 'requiem_slow_duration', 'requiem_reduction_radius',
											'requiem_line_width_start', 'requiem_line_width_end', 'requiem_line_speed', 'soul_death_release', 'cast_time', 'duration_day', 'duration_night',
											'miss_rate_day', 'miss_rate_night', 'epicenter_slow_duration_tooltip', 'fade_delay', 'burn_duration', 'burn_tick_interval', 'hp_cost_perc',
											'hp_cost_perc_per_second', 'hp_perc_dmg', 'AbilityChannelTime', 'duration_tooltip', 'duration_hero', 'duration_unit', 'bash_chance_melee', 'bash_chance_ranged',
											'bash_duration', 'bash_cooldown',
											'cooldown_melee', 'cooldown_ranged', 'tooltip_outgoing_melee', 'tooltip_outgoing_range', 'travel_distance', 'end_vision_duration', 'push_length', 'reincarnate_time',
											'spiderling_duration', 'minimum_purge_duration', 'maximum_purge_duration', 'activation_time', 'ball_lightning_initial_mana_percentage', 'ball_lightning_initial_mana_base',
											'ball_lightning_aoe', 'ball_lightning_vision_radius', 'electric_vortex_self_slow_duration', 'soul_initial_charge', 'soul_additional_charges',
											'electric_vortex_self_slow', 'static_remnant_delay', 'trigger_chance', 'recovery_time', 'vision_radius', 'duration_ally', 'poison_duration', 'buff_duration',
											'heal_armor_duration', 'bonus_aoe_duration', 'bonus_aoe_duration_hero', 'barrier_duration', 'barrier_debuff_duration', 'soul_heal_duration', 'soul_heal_interval',
											'sheep_duration', 'summon_duration', 'blast_debuff_duration', 'windwalk_duration', 'maim_duration', 'unholy_duration', 'static_duration', 'cold_duration_melee',
											'cold_duration_ranged', 'dominate_duration', 'corruption_duration', 'resist_debuff_duration', 'heal_duration', 'vision_duration', '"transform_duration',
											'speed_duration', 'speed_duration_scepter', 'frost_arrows_creep_duration', 'allied_duration_tooltip', 'fow_duration', 'max_illusions', 'juxtapose_bonus',
											'rot_radius', 'ward_count', 'drain_duration', 'AbilityDuration', 'epicenter_slow', 'epicenter_slow_as', 'reduction_duration', 'creep_duration', 'hero_duration',
											'golem_duration', 'hawk_duration', 'boar_duration', 'push_duration', 'trap_duration', 'spiderite_duration', 'movespeed_duration', 'wolf_duration', 'howl_duration',
											'rabid_duration', 'rabid_duration_bonus', 'cry_duration', 'creep_root_duration', 'bonus_duration', 'reflect_duration', 'channel_vision_duration',
											'channel_vision_step', 'channel_vision_radius', 'chill_duration', 'tether_duration', 'revolution_time', 'leash_duration', 'leash_radius', 'pounce_radius', 'seal_duration',
											'damage_duration', 'wave_duration', 'pit_duration', 'ensnare_duration', 'bonus_damage_duration', 'slow_duration_unit', 'slow_duration_hero', 'non_hero_duration',
											'customval_duration', 'customval_duration_damage', 'base_attack_time', 'blast_agility_multiplier', 'duration_creep', 'chain_chance', 'entangle_chance', 'crit_multiplier', 'crit_bonus',
											'crit_damage', 'crit_mult', 'damage_interval', 'blade_dance_crit_mult', 'flesh_heap_range', 'animation_rate', 'cast_animation', 'percent_damage', 'min_distance', 'knockback_height',
											'target_sight_radius', 'bonus_cooldown', 'activation_radius', 'start_radius', 'end_radius', 'tooltip_illusion_damage', 'tooltip_total_illusion_damage_in_pct',
											'illusion_1_damage_out_pct', 'illusion_1_damage_in_pct', 'illusion_2_damage_out_pct', 'illusion_2_damage_in_pct', 'target_aoe', 'search_radius', 'bonus_damage_pct', 'projectile_speed_bonus',
											'tree_destruction_radius', 'attack_point', 'projectile_max_time', 'secondary_projectile_speed', 'width', 'damage_percent_loss', 'max_charges', 'soul_damage_duration',
											'spirit_duration', 'stat_loss', 'absorption_tooltip', 'leap_acceleration', 'caustic_finale_slow_duration', 'attack_spill_width', 'mana_cost_scepter', 'burrow_delay', 'crit_damage',
											'blink_damage_cooldown', 'windwalk_fade_time', 'backstab_duration', 'backstab_duration_range', 'ignite_cast_range', 'shadowraze_cooldown', 'mana_void_ministun', 'slow_second',
											'disarm_range', 'disarm_melee', 'disarm_cast_range_tooltip', 'min_blink_range', 'block_cooldown', 'vision_range', 'active_duration', 'debuff_duration', 'impale_burrow_cooldown_tooltip',
											'impale_burn_range_increase_pct_tooltip', 'mana_burn_burrow_range_tooltip', 'impale_burrow_range_tooltip', 'carapace_burrow_range_tooltip', 'cooldown_upgrade', 'slow_duration_first', 'slow_duration_second',
											'cooldown_ranged_tooltip', 'minimun_distance', 'epicenter_pulses', 'epicenter_pulses_scepter', 'illusion_from_illusion_duration']

ignore_special = {'pudge_meat_hook':{'hook_width'}, 'faceless_void_time_lock':{'duration'},
									'shadow_shaman_mass_serpent_ward': {'duration', 'full_splash_radius', 'mid_splash_radius', 'min_splash_radius', 'damage_min', 'damage_min_scepter'},
									'enigma_malefice': {'stun_duration', 'tick_rate', 'tooltip_stuns'}, 'enigma_black_hole': {'duration', 'pull_speed'},
									'enchantress_natures_attendants': {'radius','heal_interval'}, 'ember_spirit_sleight_of_fist': {'creep_damage_penalty', 'attack_interval'},
									'ember_spirit_flame_guard': {'radius', 'tick_interval'}, 'ember_spirit_fire_remnant': {'charge_restore_time', 'radius'},
									'ember_spirit_activate_fire_remnant': {'charge_restore_time', 'radius'}, 'earthshaker_fissure': {'fissure_range', 'fissure_duration', 'fissure_radius', 'stun_duration'},
									'crystal_maiden_freezing_field': {'explosion_interval', 'radius', 'explosion_radius', 'explosion_min_dist', 'explosion_max_dist'},
									'rattletrap_power_cogs': {'radius', 'spacing', 'duration'}, 'rattletrap_battery_assault': {'interval', 'radius', 'duration'},
									'dark_seer_ion_shell': {'radius', 'duration'}, 'necrolyte_heartstopper_aura': {'aura_damage'}, 'axe_battle_hunger': {'duration'},
									'doom_bringer_doom': {'duration', 'duration_scepter', 'deniable_pct'}, 'doom_bringer_lvl_death': {'lvl_bonus_multiple'},
									'doom_bringer_scorched_earth': {'radius', 'duration'}, 'dazzle_shallow_grave':{'duration_tooltip'}, 
									'dazzle_shadow_wave':{'damage_radius', 'bounce_radius'}, 'dazzle_weave':{'duration', 'duration_scepter', 'vision'},'sniper_assassinate': {'projectile_speed'},
									'dazzle_poison_touch': {'should_stun', 'duration_tooltip', 'set_time', 'stun_duration'}, 'batrider_sticky_napalm': {'duration', 'max_stacks'},
									'batrider_firefly': {'radius', 'tree_radius', 'duration'},
									'brewmaster_primal_split': {'split_duration'}, 'sniper_shrapnel': {'duration', 'damage_delay', 'slow_duration', 'radius'},
									'death_prophet_exorcism': {'radius', 'max_distance', 'give_up_distance', 'spirit_speed'}, 'death_prophet_silence': {'radius'},
									'alchemist_acid_spray': {'duration'}, 'alchemist_chemical_rage': {'duration', 'bonus_movespeed', 'transformation_time'}, 'spirit_breaker_greater_bash': {'chance_pct', 'duration', 'knockback_distance'},
									'alchemist_goblins_greed': {'bonus_gold', 'bonus_bonus_gold'}, 'weaver_shukuchi': {'radius', 'fade_time'}, 'sniper_headshot': {'stun_duration', 'proc_chance'},
									'viper_corrosive_skin': {'duration'}, 'windrunner_focusfire': {'focusfire_damage_reduction', 'focusfire_damage_reduction_scepter'},
									'windrunner_powershot': {'damage_reduction', 'speed_reduction', 'arrow_width', 'tree_width', 'vision_duration', 'arrow_speed'},
									'windrunner_shackleshot': {'shackle_count'}, 'viper_viper_strike': {'duration'},
									'spectre_spectral_dagger': {'dagger_path_duration', 'hero_path_duration', 'buff_persistence', 'dagger_radius', 'path_radius', 'vision_radius', 'dagger_grace_period'},
									'tinker_march_of_the_machines': {'radius', 'collision_radius', 'splash_radius', 'duration', 'speed', 'distance', 'distance_scepter', 'machines_per_sec'}, 'pugna_nether_blast': {'radius'},
									'lone_druid_spirit_bear_entangle': {'hero_duration', 'creep_duration'},
									'lone_druid_true_form': {'speed_loss'}, 'lone_druid_spirit_bear': {'bear_regen_tooltip', 'backlash_damage', 'bear_hp'},
									'shadow_shaman_shackles': {'channel_time'}, 'antimage_mana_break': {'damage_per_burn'}, 'antimage_mana_void': {'mana_void_aoe_radius'},
									'rubick_telekinesis': {'radius', 'lift_duration', 'stun_duration', 'fall_duration'}, 'rubick_fade_bolt': {'duration', 'slow_duration', 'jump_damage_reduction_pct', 'radius', 'jump_delay'},
									'leshrac_pulse_nova': {'radius', 'mana_cost_per_second'}, 'leshrac_lightning_storm': {'slow_duration', 'radius'}, 'leshrac_diabolic_edict': {'radius', 'num_explosions'},
									'leshrac_split_earth': {'duration', 'radius'}, 'rattletrap_hookshot': {'latch_radius', 'stun_radius', 'duration', 'tooltip_range'}, 'ursa_overpower': {'duration_tooltip'},
									'dragon_knight_frost_breath': {'duration'}, 'drow_ranger_silence': {'duration', 'silence_radius'}, 'drow_ranger_wave_of_silence': {'silence_duration', 'wave_width', 'wave_speed', 'wave_range_tooltip'},
									'dragon_knight_elder_dragon_form': {'duration', 'bonus_attack_range', 'corrosive_breath_duration', 'splash_radius', 'splash_damage_percent', 'frost_duration', 'frost_aoe'},
									'ursa_fury_swipes': {'bonus_reset_time', 'bonus_reset_time_roshan'},
									'gyrocopter_rocket_barrage': {'radius'}, 'gyrocopter_flak_cannon': {'radius', 'projectile_speed'}, 'gyrocopter_call_down': {'radius'}, 'tinker_laser': {'duration_hero', 'miss_rate', 'speed'},
									'bane_nightmare': {'duration', 'animation_rate', 'nightmare_dot_interval', 'nightmare_invuln_time'}, 'bloodseeker_bloodrage': {'duration'},
									'bloodseeker_thirst': {'visibility_threshold_pct', 'invis_threshold_pct', 'max_bonus_pct'}, 'wisp_tether': {'latch_distance'},
									'wisp_overcharge': {'drain_interval', 'drain_pct', 'drain_pct_tooltip', 'bonus_damage_pct'}, 'wisp_spirits': {'min_range', 'max_range', 'hero_hit_radius', 'explode_radius', 'hit_radius', 'default_radius', 'spirit_duration'},
									'lion_impale': {'duration', 'width'}, 'lion_voodoo': {'duration', 'movespeed'}, 'lion_mana_drain': {'duration', 'break_distance', 'illusion_kill_time', 'tick_interval'},
									'luna_moon_glaive': {'range'}, 'luna_eclipse': {'duration_tooltip', 'duration_tooltip_scepter'},
									'lina_light_strike_array': {'light_strike_array_aoe', 'light_strike_array_delay_time'}, 'magnataur_empower': {'empower_duration'},
									'magnataur_skewer': {'slow_duration', 'tree_radius'}, 'magnataur_reverse_polarity': {'pull_duration'},
									'medusa_stone_gaze': {'duration', 'stone_duration', 'face_duration', 'vision_cone'}, 'medusa_split_shot': {'range', 'projectile_speed'},
									'medusa_mystic_snake': {'snake_scale', 'jump_delay'}, 'morphling_waveform': {'width'}, 'morphling_replicate': {'duration'},
									'morphling_morph_agi': {'mana_cost', 'morph_cooldown'}, 'morphling_morph_str': {'mana_cost', 'morph_cooldown'},
									'omniknight_guardian_angel': {'duration', 'duration_scepter'}, 'omniknight_repel': {'duration'},
									'omniknight_purification': {'radius'}, 'clinkz_death_pact': {'damage_gain_pct', 'duration'}, 'clinkz_wind_walk': {'duration"'},
									'clinkz_strafe': {'duration'}, 'troll_warlord_whirling_axes_melee': {'hit_radius'}, 'warlock_upheaval': {'aoe', 'duration'},
									'troll_warlord_whirling_axes_ranged': {'axe_width', 'axe_spread', 'axe_count', 'axe_slow_duration'}, 'troll_warlord_berserkers_rage': {'bash_duration', 'bonus_range', 'bonus_move_speed', 'bonus_armor'},
									'tiny_avalanche': {'num_ticks'}, 'tiny_toss': {'duration', 'grab_radius', 'bonus_damage_pct', 'grow_bonus_damage_pct'}, 'spectre_dispersion': {'min_radius', 'max_radius'},
									'shredder_reactive_armor': {'stack_limit', 'stack_duration'}, 'shredder_whirling_death': {'duration', 'whirling_tick', 'stat_loss_pct', 'duration'},
									'earthshaker_aftershock': {'aftershock_range', 'tooltip_duration'}, 'razor_plasma_field': {'radius'},
									'razor_static_link': {'drain_duration', 'drain_range', 'radius', 'speed', 'vision_duration'}, 'razor_eye_of_the_storm': {'radius', 'duration', 'strike_interval'},
									'slardar_bash': {'chance', 'duration', 'duration_creep'}, 'warlock_fatal_bonds': {'duration'},
									'earth_spirit_geomagnetic_grip': {'radius', 'miss_rate', 'miss_duration', 'pull_units_per_second_heroes', 'pull_units_per_second', 'total_pull_distance'},
									'earth_spirit_rolling_boulder': {'distance', 'rock_distance', 'delay', 'slow_duration', 'radius'},
									'bristleback_viscous_nasal_goo': {'goo_duration', 'goo_duration_creep', 'armor_per_stack'},
									'bristleback_quill_spray': {'quill_stack_duration', 'radius'}, 'bristleback_bristleback': {'side_angle', 'back_angle', 'side_damage_reduction', 'quill_release_threshold'},
									'terrorblade_metamorphosis': {'speed_loss'}, 'treant_natures_guise': {'grace_time'},
									'undying_decay': {'radius', 'decay_duration'},
									'undying_soul_rip': {'radius'}, 'undying_tombstone': {'duration', 'radius', 'zombie_interval'}, 'undying_tombstone_zombie_aura': {'radius', 'zombie_interval'},
									'undying_tombstone_zombie_deathstrike': {'duration'}, 'undying_flesh_golem': {'duration', 'radius'}, 'disruptor_thunder_strike': {'radius', 'strike_interval', 'duration'},
									'disruptor_glimpse': {'backtrack_time'}, 'disruptor_kinetic_field': {'radius', 'duration'}, 'disruptor_static_storm': {'radius', 'duration', 'duration_scepter', 'pulses', 'pulses_scepter'},
									'nyx_assassin_impale': {'width', 'duration'}, 'nyx_assassin_vendetta': {'duration'}, 'naga_siren_ensnare': {'duration'},
									'naga_siren_rip_tide': {'radius'}, 'naga_siren_song_of_the_siren': {'duration', 'animation_rate'},
									'keeper_of_the_light_illuminate': {'radius', 'max_channel_time', 'channel_vision_interval'}, 'keeper_of_the_light_mana_leak': {'duration', 'cast_range_tooltip'},
									'keeper_of_the_light_spirit_form_illuminate': {'radius', 'range', 'speed', 'max_channel_time', 'channel_vision_interval'},
									'death_prophet_witchcraft': {'carrion_swarm_mana_cost_adjust', 'carrion_swarm_cooldown_adjust', 'silence_mana_cost_adjust', 'silence_cooldown_adjust'},
									'elder_titan_echo_stomp': {'radius'}, 'zuus_arc_lightning': {'radius', 'jump_delay', 'jump_count'}, 'zuus_lightning_bolt': {'sight_duration', 'spread_aoe', 'true_sight_radius', 'sight_radius_day', 'sight_radius_night'},
									'zuus_static_field': {'damage_health_pct', 'radius'}, 'puck_illusory_orb': {'radius', 'orb_speed', 'orb_vision', 'vision_duration'},
									'puck_waning_rift': {'puck_waning_rift', 'radius'}, 'puck_dream_coil': {'coil_duration', 'coil_break_radius', 'coil_stun_duration', 'coil_duration_scepter', 'coil_stun_duration_scepter'},
									'shredder_chakram': {'damage_interval', 'pass_slow_duration', 'mana_per_second', 'slow'}, 'shredder_chakram_2': {'damage_interval', 'pass_slow_duration', 'mana_per_second', 'slow'},
									'shredder_timber_chain': {'chain_radius', 'damage_radius'},
									'night_stalker_darkness': {'blind_percentage'}, 'riki_smoke_screen': {'radius', 'miss_rate'}, 'riki_backstab': {'backstab_angle', 'damage_multiplier'},
									'mirana_starfall': {'starfall_secondary_radius', 'starfall_radius'}, 'enigma_midnight_pulse': {'duration', 'damage_percent'},
									'nevermore_requiem': {'requiem_radius', 'requiem_reduction_ms', 'requiem_reduction_damage', 'requiem_reduction_tooltip', 'requiem_soul_conversion', 'requiem_line_width_start', 'requiem_line_width_end', 'requiem_line_speed', 'soul_death_release'},
									'phoenix_supernova': {'aura_radius', 'tooltip_duration', 'stun_duration'}, 'phoenix_fire_spirits': {'spirit_duration', 'spirit_speed', 'radius', 'duration', 'tick_interval'},
									'phoenix_icarus_dive': {'hp_cost_perc', 'dash_width', 'hit_radius', 'burn_duration', 'burn_tick_interval'},
									'phoenix_sun_ray': {'radius', 'forward_move_speed', 'turn_rate_initial', 'turn_rate', 'tooltip_duration', 'tick_interval'}, 'obsidian_destroyer_arcane_orb': {'mana_pool_damage_pct'},
									'obsidian_destroyer_astral_imprisonment': {'prison_duration', 'int_steal'}, 'obsidian_destroyer_essence_aura': {'restore_chance'},
									'obsidian_destroyer_sanity_eclipse': {'radius', 'cast_range', 'damage_multiplier', 'int_threshold', 'damage_multiplier_scepter'},
									'visage_summon_familiars': {'damage_charge_time', 'max_damage_charges', 'familiar_speed', 'familiar_hp', 'familiar_max_damage'},
									'visage_summon_familiars_stone_form': {'stun_radius', 'stun_delay', 'stun_duration', 'stone_duration', 'max_damage_charges', 'stun_delay'},
									'silencer_curse_of_the_silent': {'radius'}, 'silencer_glaives_of_wisdom': {'steal_range'}, 'silencer_last_word': {'duration', 'debuff_duration'},
									'necrolyte_death_pulse': {'area_of_effect'}, 'necrolyte_sadist': {'regen_duration'}, 'huskar_berserkers_blood': {'resistance_per_stack'},
									'huskar_life_break': {'health_cost_percent', 'health_damage', 'health_damage_scepter', 'tooltip_health_cost_percent', 'tooltip_health_damage', 'tooltip_health_damage_scepter', 'charge_speed'},
									'drow_ranger_marksmanship': {'radius'}, 'elder_titan_ancestral_spirit': {'spirit_duration', 'move_pct_cap'},
									'elder_titan_earth_splitter': {'crack_time', 'crack_width', 'vision_width', 'vision_interval', 'vision_duration', 'vision_step', 'total_steps', 'slow_duration_scepter'},
									'meepo_poof': {'radius'}, 'witch_doctor_paralyzing_cask': {'bounce_range', 'bounce_delay'},
									'witch_doctor_voodoo_restoration': {'mana_per_second', 'radius', 'heal_interval'}, 'witch_doctor_maledict': {'bonus_damage_threshold', 'duration_tooltip', 'bonus_damage', 'ticks'},
									'witch_doctor_death_ward': {'bounce_radius'}, 'pugna_nether_ward': {'radius', 'attacks_to_destroy_tooltip'}, 'shadow_demon_disruption': {'disruption_duration'},
									'shadow_demon_shadow_poison': {'radius', 'tooltip_duration'}, 'shadow_demon_soul_catcher': {'radius', 'tooltip_duration'},
									'shadow_demon_demonic_purge': {'tooltip_duration', 'charge_restore_time'}, 'tusk_ice_shards': {'shard_width', 'shard_count', 'shard_distance', 'shard_duration', 'shard_angle_step'},
									'tusk_snowball': {'snowball_windup', 'snowball_duration'}, 'enigma_demonic_conversion': {'eidolon_dmg_tooltip', 'eidolon_hp_tooltip'},
									'furion_force_of_nature': {'duration', 'max_treants', 'area_of_effect'}, 'furion_wrath_of_nature': {'damage_percent_add'},
									'invoker_ghost_walk': {'area_of_effect', 'duration', 'self_slow', 'aura_fade_time'},
									'invoker_cold_snap': {'duration', 'freeze_cooldown', 'damage_trigger'},
									'invoker_tornado': {'area_of_effect', 'vision_distance', 'end_vision_duration', 'lift_duration'}, 'invoker_emp': {'area_of_effect', 'delay', 'damage_per_mana_pct'},
									'invoker_chaos_meteor': {'land_time', 'area_of_effect', 'travel_distance', 'damage_interval', 'vision_distance', 'end_vision_duration', 'burn_duration'},
									'invoker_sun_strike': {'vision_distance', 'vision_duration', 'area_of_effect'}, 'invoker_forge_spirit': {'spirit_duration', 'spirit_attack_range', 'spirit_mana', 'spirit_hp'},
									'invoker_ice_wall': {'wall_element_spacing', 'duration', 'slow_duration', 'wall_place_distance', 'num_wall_elements', 'wall_element_radius'},
									'invoker_deafening_blast': {'disarm_duration', 'radius_start', 'radius_end', 'end_vision_duration'},
									'broodmother_spawn_spiderlings': {'count'}, 'broodmother_spin_web': {'radius', 'fade_delay', 'damage_time', 'charge_restore_time'}, 'weaver_the_swarm': {'attack_rate', 'count', 'radius', 'spawn_radius'},
									'ancient_apparition_chilling_touch': {'attack_speed_pct', 'max_attacks'},
									'ancient_apparition_ice_blast': {'frostbite_duration', 'frostbite_duration_scepter', 'radius_min', 'radius_max', 'path_radius', 'radius_grow', 'path_radius', 'speed'},
									'item_boots': {'bonus_movement_speed'},
									'item_cyclone': {'bonus_movement_speed', 'cyclone_duration'}, 'item_manta': {'bonus_movement_speed'}, 'item_mask_of_madness': {'berserk_duration'},
									'item_diffusal_blade': {'initial_charges', 'purge_root_duration', 'purge_slow_duration'}, 'item_diffusal_blade_2': {'initial_charges', 'purge_root_duration', 'purge_slow_duration'},
									'item_soul_ring': {'health_sacrifice'}, 'tiny_grow': {'bonus_movement_speed', 'bonus_attack_speed', 'bonus_range_scepter', 'bonus_building_damage_scepter', 'grow_bonus_damage_pct', 'grow_bonus_damage_pct_scepter'},
									'visage_soul_assumption': {'stack_limit', 'stack_duration', 'radius', 'bolt_speed'}, 'visage_gravekeepers_cloak': {'max_layers', 'recovery_time'},
									'slark_dark_pact': {'radius', 'pulse_duration', 'delay', 'total_pulses', 'pulse_interval'}, 'slark_shadow_dance': {'bonus_movement_speed', 'bonus_regen_pct', 'neutral_disable'},
									'tusk_frozen_sigil': {'sigil_radius', 'sigil_duration', 'move_slow', 'attack_slow'}, 'tusk_walrus_punch': {'hp_threshold', 'air_time', 'move_slow'},
									'abaddon_borrowed_time': {'hp_threshold'}, 'item_radiance': {'aura_radius'}, 'batrider_flamebreak': {'explosion_radius', 'collision_radius', 'knockback_height'},
									'item_gem': {'radius'}, 'item_shivas_guard': {'blast_radius', 'aura_radius'},
									'axe_counter_helix': {'radius', 'cooldown', 'trigger_chance'}, 'kunkka_torrent': {'radius'}, 'kunkka_tidebringer': {'radius', 'cleave_damage'},
									'sven_storm_bolt': {'bolt_aoe'}, 'storm_spirit_static_remnant': {'static_remnant_radius', 'static_remnant_damage_radius'},
									'tiny_craggy_exterior': {'radius'}, 'warlock_golem_permanent_immolation': {'aura_radius'}, 'beastmaster_wild_axes': {'radius', 'spread'},
									'rattletrap_rocket_flare': {'radius'}, 'jakiro_dual_breath': {'start_radius', 'end_radius'},
									'jakiro_macropyre': {'path_radius', 'cast_range_scepter', 'burn_interval'}, 'spectre_desolate': {'radius'}, 'ancient_apparition_ice_vortex': {'radius', 'vision_aoe'},
									'spirit_breaker_charge_of_darkness': {'bash_radius'},
									'alchemist_unstable_concoction': {'brew_time', 'radius', 'brew_explosion'}, 'alchemist_unstable_concoction_throw': {'brew_time', 'midair_explosion_radius'},
									'brewmaster_thunder_clap': {'radius'}, 'brewmaster_drunken_haze': {'radius'}, 'brewmaster_earth_pulverize': {'radius_inner', 'radius_outer'},
									'brewmaster_fire_permanent_immolation': {'radius'}, 'meepo_earthbind': {'radius'}, 'treant_leech_seed': {'radius'},
									'centaur_hoof_stomp': {'radius'}, 'centaur_double_edge': {'radius'}, 'centaur_stampede': {'radius', 'strength_damage'}, 'skywrath_mage_concussive_shot': {'slow_radius', 'shot_vision', 'vision_duration', 'movement_speed_pct', 'slow_duration'},
									'skywrath_mage_mystic_flare': {'radius', 'damage_interval', 'duration'}, 'abaddon_aphotic_shield': {'radius'}, 'elder_titan_echo_stomp_spirit': {'radius'}, 'legion_commander_overwhelming_odds': {'radius'},
									'earth_spirit_boulder_smash': {'radius', 'rock_search_aoe', 'unit_distance', 'rock_distance'},
									'earth_spirit_magnetize': {'cast_radius', 'rock_search_radius', 'rock_explosion_radius', 'damage_duration', 'rock_explosion_delay', 'silence_duration'},
									'abyssal_underlord_firestorm': {'radius', 'wave_interval', 'burn_interval', 'first_wave_delay'}, 'abyssal_underlord_pit_of_malice': {'radius', 'pit_interval', 'pit_duration'},
									'abyssal_underlord_atrophy_aura': {'radius', 'bonus_damage_duration'}, 'abyssal_underlord_dark_rift': {'radius', 'teleport_delay'},
									'oracle_fortunes_end': {'minimum_purge_duration', 'maximum_purge_duration', 'max_channel_time_tooltip', 'bolt_speed'}, 'backdoor_protection': {'radius', 'activation_time'}, 'backdoor_protection_in_base': {'activation_time'},
									'necronomicon_archer_aoe': {'radius'}, 'roshan_slam': {'radius'}, 'centaur_khan_war_stomp': {'radius'}, 'polar_furbolg_ursa_warrior_thunder_clap': {'radius'},
									'tornado_tempest': {'far_radius', 'near_radius'}, 'big_thunder_lizard_slam': {'radius'}, 'roshan_halloween_wave_of_force': {'radius', 'game_end_radius'},
									'techies_stasis_trap': {'stun_radius', 'duration'}, 'winter_wyvern_arctic_burn': {'attack_range_bonus': '475 575 675 775'},
									'techies_suicide': {'respawn_time_percentage', 'respawn_time_percentage_tooltip'},
									'techies_remote_mines': {'duration', 'cast_range_tooltip', 'model_scale'}, 'techies_focused_detonate': {'radius'},
									'techies_remote_mines_self_detonate': {'radius'}, 'storm_spirit_overload': {'overload_aoe'}, 'lich_frost_nova': {'radius'}, 'warlock_rain_of_chaos': {'aoe'},
									'queenofpain_sonic_wave': {'starting_aoe', 'final_aoe', 'distance'}, 'pudge_rot': {'rot_tick'}, 'pudge_dismember': {'strength_damage_scepter'},
									'magnataur_shockwave': {'shock_width'}, 'lich_chain_frost': {'jump_range', 'projectile_speed', 'vision_radius', 'cast_range_scepter'},
									'death_prophet_carrion_swarm': {'start_radius', 'end_radius'}, 'zuus_thundergods_wrath': {'true_sight_radius', 'true_sight_radius_tooltip', 'sight_radius_day', 'sight_radius_night', 'sight_duration'},
									'item_assault': {'aura_radius'}, 'vengefulspirit_wave_of_terror': {'wave_width', 'vision_aoe', 'vision_duration'},
									'dragon_knight_breathe_fire': {'speed'}, 'mirana_arrow': {'arrow_speed', 'arrow_width', 'arrow_max_stunrange', 'arrow_min_stun', 'arrow_max_stun', 'arrow_vision'},
									'vengefulspirit_command_aura': {'aura_radius'}, 'crystal_maiden_crystal_nova': {'radius'}, 'winter_wyvern_winters_curse': {'damage_reduction'},
									'lina_dragon_slave': {'dragon_slave_speed', 'dragon_slave_width_initial', 'dragon_slave_width_end'}, 'lina_fiery_soul': {'fiery_soul_attack_speed_bonus', 'fiery_soul_move_speed_bonus'},
									'lina_laguna_blade': {'cast_range_scepter'}, 'kobold_taskmaster_speed_aura': {'radius'}, 'centaur_khan_endurance_aura': {'radius'}, 'alpha_wolf_command_aura': {'radius'},
									'tornado_tempest': {'far_radius', 'near_radius'}, 'enraged_wildkin_tornado': {'duration'}, 'enraged_wildkin_toughness_aura': {'radius'}, 'granite_golem_hp_aura': {'radius'},
									'satyr_hellcaller_shockwave': {'radius_start', 'radius_end'}, 'satyr_hellcaller_unholy_aura': {'radius'}, 'harpy_storm_chain_lightning': {'jump_range', 'damage_percent_loss'},
									'black_dragon_splash_attack': {'range_close', 'damage_percent_close', 'range_mid', 'damage_percent_mid', 'range_far', 'damage_percent_far'}, 'blue_dragonspawn_overseer_devotion_aura': {'radius'},
									'bloodseeker_blood_bath': {'radius', 'delay_plus_castpoint_tooltip'}, 'bloodseeker_rupture': {'cast_range_tooltip'},
									'elder_titan_natural_order': {'radius', 'armor_reduction_pct'}, 'dark_seer_vacuum': {'radius', 'radius_tree'},
									'dark_seer_wall_of_replica': {'replica_damage_outgoing', 'tooltip_outgoing', 'replica_damage_incoming', 'tooltip_replica_total_damage_incoming', 'width', 'replica_scale', 'range_tooltip', 'replica_damage_outgoing_scepter', 'tooltip_outgoing_scepter'},
									'slark_pounce': {'pounce_radius', 'pounce_acceleration'}, 'item_gloves': {'bonus_attack_speed'}, 'beastmaster_primal_roar': {'damage_radius', 'push_distance', 'push_duration', 'slow_duration', 'cast_range_scepter', 'cooldown_scepter'},
									'necrolyte_reapers_scythe': {'respawn_constant', 'respawn'}, 'morphling_adaptive_strike': {'stun_min', 'stun_max', 'knockback_min', 'knockback_max', 'projectile_speed'},
									'warlock_golem_flaming_fists': {'radius', 'chance'}, 'skywrath_mage_arcane_bolt': {'bolt_vision'}, 'skywrath_mage_ancient_seal': {'resist_debuff'},
									'earth_spirit_petrify': {'aoe'}, 'earth_spirit_stone_caller': {'charge_restore_time', 'max_charges'}, 'axe_culling_blade': {'speed_duration'},
									'sandking_caustic_finale': {'caustic_finale_radius', 'caustic_finale_damage_reduced'}, 'jakiro_ice_path': {'path_radius'}, 'jakiro_liquid_fire': {'radius', 'tooltip_duration'},
									'ancient_apparition_cold_feet': {'break_distance', 'stun_duration'}, 'forged_spirit_melting_strike': {'duration'}, 'templar_assassin_self_trap': {'trap_radius', 'movement_speed_bonus_stage'},
									'venomancer_venomous_gale': {'duration', 'tick_interval', 'radius'}, 'venomancer_poison_sting': {'movement_speed'}, 'venomancer_plague_ward': {'ward_hp_tooltip', 'ward_damage_tooltip'},
									'venomancer_poison_nova': {'start_radius', 'duration', 'duration_scepter'}, 'phoenix_launch_fire_spirit': {'spirit_duration', 'spirit_speed', 'radius', 'duration', 'tick_interval'},
									'oracle_fates_edict': {'magic_damage_resistance_pct_tooltip'}, 'oracle_purifying_flames': {'tick_rate'}, 'lycan_shapeshift': {'bonus_night_vision'},
									'skeleton_king_reincarnation': {'aura_radius', 'aura_radius_tooltip_scepter'}, 'gyrocopter_homing_missile': {'max_distance'},
									'lycan_summon_wolves': {'wolf_index', 'wolf_duration', 'wolf_damage', 'wolf_hp', 'wolf_bat'}, 'sandking_burrowstrike': {'burrow_width'}, 'bounty_hunter_track': {'bonus_gold_radius', 'gold_steal'},
									'item_maelstrom': {'chain_chance'}, 'life_stealer_assimilate': {'order_lock_duration'},
									'item_mjollnir': {'static_duration', 'static_chance', 'static_cooldown', 'chain_chance'},
									'item_ghost': {'extra_spell_damage_percent'}, 'item_dagon': {'range_tooltip'}, 'item_dagon_2': {'range_tooltip'},
									'item_dagon_3': {'range_tooltip'}, 'item_dagon_4': {'range_tooltip'}, 'item_dagon_5': {'range_tooltip'}, 'templar_assassin_refraction': {'damage_threshold', 'duration'},
									'templar_assassin_psionic_trap': {'trap_fade_time'}, 'templar_assassin_trap': {'trap_radius', 'trap_duration', 'movement_speed_bonus_stage'},
									'templar_assassin_self_trap': {'trap_radius', 'trap_duration', 'movement_speed_bonus_stage'}, 'storm_spirit_ball_lightning': {'blocker_duration', 'ball_lightning_move_speed', 'AbilityDamage'},
									'spectre_haunt': {'attack_delay', 'tooltip_illusion_total_damage_incoming'}, 'item_bloodstone': {'charge_range', 'vision_on_death_radius', 'respawn_time_reduction'},
									'medusa_mana_shield': {'absorption_tooltip'}, 'huskar_inner_vitality': {'attrib_bonus', 'hurt_percent'},
									'spirit_breaker_nether_strike': {'bash_radius_scepter'}, 'item_tranquil_boots': {'heal_interval', 'break_time', 'break_count', 'break_threshold'},
									'treant_overgrowth': {'eyes_radius', 'radius'}, 'treant_eyes_in_the_forest': {'overgrowth_aoe', 'vision_aoe'}, 'lycan_howl': {'unit_bonus_damage'},
									'item_javelin': {'bonus_chance'}, 'troll_warlord_fervor': {'attack_speed'}, 'centaur_return': {'strength_pct'}}


ignore_normal = {'dazzle_shallow_grave':{'AbilityDuration'}, 'dazzle_poison_touch': {'AbilityDuration'},
								 'death_prophet_exorcism': {'AbilityDuration'}, 'leshrac_diabolic_edict': {'AbilityDuration'}, 'leshrac_split_earth': {'AbilityDuration'},
								 'ursa_overpower': {'AbilityDuration'}, 'gyrocopter_flak_cannon': {'AbilityDuration'}, 'wisp_tether': {'AbilityCastRange'},
								 'lion_mana_drain': {'AbilityCastRange', 'AbilityChannelTime'}, 'shredder_whirling_death': {'AbilityCastRange'},
								 'razor_static_link': {'AbilityCastRange'}, 'sandking_epicenter': {'AbilityDuration'},
								 'zuus_static_field': {'AbilityCastRange'},
								 'phoenix_supernova': {'AbilityDuration'}, 'obsidian_destroyer_arcane_orb': {'AbilityCastRange'}, 'obsidian_destroyer_astral_imprisonment': {'AbilityDuration'},
								 'meepo_geostrike': {'AbilityDuration'}, 'witch_doctor_maledict': {'AbilityDuration'},
								 'shadow_demon_disruption': {'AbilityDuration'}, 'vengefulspirit_command_aura': {'AbilityCastRange'}, 'lina_laguna_blade': {'AbilityCastRange'},
								 'shadow_shaman_ether_shock': {'AbilityCastRange'},
								 'sniper_shrapnel': {'AbilityCastRange'}, 'bloodseeker_rupture': {'AbilityCastRange'}, 'bloodseeker_blood_bath': {'AbilityCastRange'},
								 'huskar_burning_spear': {'AbilityCastRange'}, 'drow_ranger_frost_arrows': {'AbilityCastRange'},
								 'clinkz_searing_arrows': {'AbilityCastRange'}, 'viper_poison_attack': {'AbilityCastRange'}, 'jakiro_liquid_fire': {'AbilityCastRange'},
								 'silencer_glaives_of_wisdom': {'AbilityCastRange'}, 'pugna_nether_blast': {'AbilityCastRange'},
								 'earthshaker_fissure': {'AbilityCastRange'}, 'beastmaster_primal_roar': {'AbilityCastRange'}, 'huskar_life_break': {'AbilityCastRange'},
								 'earth_spirit_boulder_smash': {'AbilityCastRange'}, 'earth_spirit_rolling_boulder': {'AbilityCastRange'}, 'earth_spirit_geomagnetic_grip': {'AbilityCastRange'},
								 'earth_spirit_stone_caller': {'AbilityCastRange'}, 'earth_spirit_petrify': {'AbilityCastRange'}, 'earth_spirit_magnetize': {'AbilityCastRange'},
								 'tinker_march_of_the_machines': {'AbilityCastRange'}, 'item_dagon': {'AbilityCastRange'}, 'item_dagon_2': {'AbilityCastRange'},
								 'item_dagon_3': {'AbilityCastRange'}, 'item_dagon_4': {'AbilityCastRange'}, 'item_dagon_5': {'AbilityCastRange'}, 'skywrath_mage_mystic_flare': {'AbilityCastRange'},
								 'item_heavens_halberd': {'AbilityCastRange'}, 'item_ethereal_blade': {'AbilityCastRange'}}

ignore_all_normal = ['ID', 'AbilityCastPoint', 'AbilityManaCost', 'AbilityCooldown', 'AbilityModifierSupportValue', 'MaxLevel', 'RequiredLevel', 'LevelsBetweenUpgrades',
										 'DisplayAdditionalHeroes', 'AbilityDuration', 'AbilityChannelTime', 'FightRecapLevel', 'AbilityModifierSupportBonus', 'AbilityCastRangeBuffer', 'ItemCost',
										 'SideShop', 'ItemRecipe', 'MaxUpgradeLevel', 'ItemBaseLevel', 'ItemStackable', 'ItemPermanent', 'ItemInitialCharges', 'ItemSupport', 'ItemStockMax', 'ItemStockInitial',
										 'ItemStockTime', 'ItemDisplayCharges', 'ItemAlertable', 'ItemContributesToNetWorthWhenDropped', 'ItemRequiresCharges']

# removed 'AbilityCastRange' from ignore_all_normal


dont_parse = ['attribute_bonus', 'Version', 'ability_base', 'default_attack', 'invoker_invoke', 'invoker_empty1', 'invoker_empty2', 'ancient_apparition_ice_blast_release',
							'meepo_divided_we_stand', 'lone_druid_true_form_druid', 'lone_druid_spirit_bear_return', 'pugna_decrepify',
							'rubick_telekinesis_land', 'tinker_rearm', 'bane_nightmare_end', 'wisp_tether_break', 'wisp_spirits_in', 'wisp_spirits_out', 'wisp_empty1', 'wisp_empty2', 'wisp_relocate',
							'morphling_morph_replicate', 'naga_siren_song_of_the_siren_cancel', 'keeper_of_the_light_empty1', 'keeper_of_the_light_empty2', 'keeper_of_the_light_spirit_form',
							'keeper_of_the_light_illuminate_end', 'puck_ethereal_jaunt', 'shredder_return_chakram',
							'phoenix_icarus_dive_stop', 'phoenix_sun_ray_toggle_move_empty', 'phoenix_sun_ray_toggle_move', 'phoenix_sun_ray_stop',
							'riki_permanent_invisibility', 'silencer_global_silence', 'elder_titan_return_spirit', 'shadow_demon_shadow_poison_release', 'tusk_launch_snowball',
							'dark_seer_wall_of_replica', 'lone_druid_spirit_bear_entangle', 'ability_deward', 'item_recipe_ward_dispenser', 'rubick_hidden1', 'rubick_hidden2', 'rubick_hidden3',
							'rubick_empty1', 'rubick_empty2', 'doom_bringer_empty1', 'doom_bringer_empty2']


dont_parse_more_specific = {'luna_eclipse': {'duration_tooltip', 'radius'}, 'troll_warlord_berserkers_rage': {'bonus_hp', 'bonus_move_speed', 'bonus_armor', 'bonus_range', 'base_attack_time'}}

# luna_eclipse, furion_sprout, item_bloodstone, dark_seer_wall_of_replica multiplier disabled due crash issues


ignore_partial_names = {'cooldown'}

fixed_value = {'item_bloodstone': {'on_death_removal':'0.67', 'respawn_time_reduction': '4.0'},
							 'sniper_assassinate': {'AbilityUnitTargetFlags': 'DOTA_UNIT_TARGET_FLAG_MAGIC_IMMUNE_ENEMIES | DOTA_UNIT_TARGET_FLAG_INVULNERABLE | DOTA_UNIT_TARGET_FLAG_NOT_ANCIENTS'},
							 'spectre_dispersion': {'damage_reflection_pct':'14 18 22 26'}, 'gyrocopter_homing_missile': {'stun_duration':'2.0 2.5 3.0 3.5'}, 'item_lesser_crit': {'crit_chance': '30'},
							 'item_greater_crit': {'crit_chance': '45'}, 'juggernaut_blade_dance': {'blade_dance_crit_chance':'30 40 50 60'}, 'skeleton_king_mortal_strike': {'crit_chance':'30'},
							 'bounty_hunter_jinada': {'8.0 7.0 5.0 3.0'}, 'phantom_assassin_coup_de_grace': {'crit_chance':'15'}, 'lycan_shapeshift': {'crit_chance': '30 40 50'}, 'lycan_summon_wolves_critical_strike': {'crit_chance': '45'},
							 'brewmaster_drunken_brawler': {'crit_chance':'20 25 30 35'}, 'chaos_knight_chaos_strike': {'crit_chance': '10 14 18 20'}, 'witch_doctor_maledict': {'radius': '525'},
							 'leshrac_diabolic_edict': {'AbilityUnitTargetType': 'DOTA_UNIT_TARGET_HERO | DOTA_UNIT_TARGET_BASIC', 'tower_bonus': '-100'},
							 'jakiro_liquid_fire': {'AbilityUnitTargetType': 'DOTA_UNIT_TARGET_HERO | DOTA_UNIT_TARGET_BASIC' },
							 'ancient_apparition_ice_vortex': {'AbilityCooldown': '25.0 20.0 15.0 10.0'}, 'invoker_tornado': {'travel_distance': '1600 2400 3200 4000 4800 5600 6400'},
							 'invoker_ghost_walk': {'self_slow': '-5 -0 10 20 40 60 80'}, 'invoker_cold_snap': {'freeze_duration': '0.58'}, 'invoker_sun_strike': {'delay': '0.6'},
							 'templar_assassin_psi_blades': {'attack_spill_range': '900 1030 1270 1550'}, 'phoenix_sun_ray': {'hp_cost_perc_per_second': '10', 'hp_perc_dmg': '2 4 6 8'},
							 'keeper_of_the_light_recall': {'teleport_delay': '4.0 2.5 1.5'}, 'lone_druid_spirit_bear_demolish': {'bonus_building_damage': '-90'},
							 'rubick_spell_steal': {'duration': '300.0 400.0 500.0'}, 'enigma_demonic_conversion': {'split_attack_count': '5 4 3 2', 'spawn_count': '3 4 5 6'},
							 'techies_land_mines': {'SpellImmunityType': 'SPELL_IMMUNITY_ENEMIES_NO'},
							 'ogre_magi_multicast': {'multicast_2_times': '0.6 0.75 0.9', 'multicast_3_times': '0 0.40 0.50', 'multicast_4_times': '0 0 0.25', 'multicast_2_times_tooltip': '60 75 90', 'multicast_3_times_tooltip': '0 40 50', 'multicast_4_times_tooltip': '0 0 25'},
							 'skywrath_mage_mystic_flare': {'scepter_cooldown': '50 30 15'}, 'faceless_void_time_lock': {'chance_pct': '14 18 22 26'}, 'faceless_void_chronosphere': {'duration': '5.0 5.5 6.0', 'duration_scepter': '6.0 6.5 7.5'},
							 'faceless_void_backtrack': {'dodge_chance_pct': '15 20 25 30'}, 'oracle_false_promise': {'duration': '12 14 16'}, 'terrorblade_sunder': {'hit_point_minimum_pct': '10'},
							 'furion_teleportation': {'AbilityCastPoint': '1.5', 'AbilityCooldown': '30 20 10 5'}, 'furion_sprout': {'duration': '6 7 8 9'}, 'treant_natures_guise': {'fade_time': '1.0'},
							 'abaddon_borrowed_time': {'duration': '6.0 7.0 8.0', 'duration_scepter': '9.0 10.0 11.0'},
							 'morphling_adaptive_strike': {'damage_min': '0.50 0.50 0.50 0.50', 'damage_max': '1.0 2.0 3.0 4.0'}, 'courier_burst': {'AbilityCooldown': '15'},
							 'weaver_geminate_attack': {'AbilityCooldown': '3.0 2.0 1.0 0.5'}, 'weaver_shukuchi': {'duration': '4.0 4.4 4.8 5.2'}, 'weaver_time_lapse': {'AbilityCooldown': '30 25 20', 'cooldown_scepter': '10'},
							 'omniknight_purification': {'AbilityUnitDamageType': 'DAMAGE_TYPE_MAGICAL'},
							 'item_travel_boots': {'AbilityCooldown': '20'}, 'item_travel_boots_2': {'AbilityCooldown': '20'},
							 'item_sheepstick': {'sheep_duration': '5.0', 'sheep_movement_speed': '100'}, 'medusa_split_shot': {'damage_modifier': '-20 -16 -13 -10', 'damage_modifier_tooltip': '80 84 87 90'},
							 'item_force_staff': {'AbilityCooldown': '10.0'}, 'lone_druid_true_form': {'base_attack_time': '1.4 1.4 1.4'}, 'terrorblade_metamorphosis': {'base_attack_time': '1.5'},
							 'alchemist_chemical_rage': {'base_attack_time': '1.4 1.2 1.0'}, 'furion_wrath_of_nature': {'jump_delay': '0.01'}, 'item_monkey_king_bar': {'bash_stun': '0.0'},
							 'item_manta': {'images_do_damage_percent_melee': '-50', 'tooltip_damage_outgoing_melee': '50', 'images_take_damage_percent_melee': '150', 'tooltip_damage_incoming_melee_total_pct': '250',
											'images_do_damage_percent_ranged': '-60', 'tooltip_damage_outgoing_ranged': '40', 'images_take_damage_percent_ranged': '200', 'tooltip_damage_incoming_ranged_total_pct': '300'},
							 'item_solar_crest': {'AbilityCooldown': '14'}}


insert_custom_normal = {}

factors = [2,3,4,5,10,20]
divValue = {'20':'4'}
modID = {2:'c8f994a16d231168d00b98363e3913a8', 3:'23d7ecaf561aca2e5c65f987984b7f33', 4:'ac5882c70a73cd87a6020bb9e3255b76', 5:'a0a0aa957ab22d67b4e69d6b5b0d9f1d',
				10:'947f9940ae5d758373be75f2ea95a71e', 20:'a884ffc0cb2bdc07b6acdd4433cf14b6'}
#override_factor = [2,3,5,10]




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



def multiply(values, by, separator, forceMax):
	aslist = values.strip().split(separator)
	
	if forceMax != False:
		forceMaxList = forceMax.strip().split(separator)
	
	tmplist = []
	newvalues = ''
	
	level = -1
	
	for value in aslist:

		level += 1

		if forceMax != False and len(forceMaxList) >= (level+1):
			index = level
		else:
			index = 0
		
		try:
				
			newvalue = str(float(value.strip())*float(by))
			
			if forceMax != False and newvalue[0:1] == '-' and float(newvalue) < float(forceMaxList[index]):                
				newvalue = str(forceMaxList[index])                
					
			if forceMax != False and newvalue[0:1] != '-' and float(newvalue) > float(forceMaxList[index]):                
				newvalue = str(forceMaxList[index])
					
			if newvalue[-2:] == '.0' and value[-2:] != '.0':
				newvalue = newvalue[:-2]
					
			tmplist.append(newvalue)
				
				
		except ValueError:
			print "EXCEPTION - ValueError multiply: %s | %s > %s | %s [%d]" % (value.strip(), values, forceMax, forceMaxList[index], index)
			 
	return ' '.join(tmplist)

def divide(values, by, separator, forceMax):
	aslist = values.strip().split(separator)
	tmplist = []
	newvalues = ''

	if forceMax != False:
		forceMaxList = forceMax.strip().split(separator)

	level = -1
	
	for value in aslist:

		level += 1

		if forceMax != False and len(forceMaxList) >= (level+1):
			index = level
		else:
			index = 0
		
		try:
			newvalue = str(float(value.strip())/float(by))

			#print 'negative value: ' + values + ' / max: ' + str(forceMax)
			
			if forceMax != False and newvalue[0:1] == '-' and float(newvalue) < float(forceMax):
				newvalue = forceMax
			if forceMax != False and newvalue[0:1] != '-' and float(newvalue) > float(forceMax):
				newvalue = forceMax
			if newvalue[-2:] == '.0' and value[-2:] != '.0':
				newvalue = newvalue[:-2]
			tmplist.append(newvalue)
		except ValueError:
			print "EXCEPTION - ValueError divide: %s | %s" % (value.strip(), values)
			
	return ' '.join(tmplist)

def check_special_condition(name, key_type, key, values, separator):
	if key_type == "Normal" and key == "Modifiers":
		return values;
	
	for partial in ignore_partial_names:
		if partial in name:
				return values

	if name in fixed_value and key in fixed_value[name]:
		return fixed_value[name][key]


	if key in multiply_all_by_fixed_factor:
		return multiply(values, multiply_all_by_fixed_factor[key], separator, False)


	if key_type == "Normal":
		if key in ignore_all_normal:
			return values
		elif name in ignore_normal and key in ignore_normal[name]:
			#print key_type + " / " + name + " => " + key
			return values
	else:
		if key in ignore_all_special:
			return values
		elif name in ignore_special and key in ignore_special[name]:
			return values

	
	# multiply only numbers
	testinstance = str_to_type(values.split(" ")[0])
	if testinstance not in (int, long, float, complex):
		return values

	return False

def fix_requeriments(values, factor, separator):
	valueslist = values.strip().split(separator)
	tmplist = []
	for value in valueslist:
		tmplist.append(value+'_x'+str(factor))
	return separator.join(tmplist)


def divide_or_multiply(name, key_type, key, values, by, separator):
	 
	valueslist = values.strip().split(separator)

	maxValue = False
	if key in specific_max_value:
		maxValue = specific_max_value[key]
			
	if name in more_specific_max_value and key in more_specific_max_value[name]:
		#print 'foouuund'
		maxValue = more_specific_max_value[name][key]


	val = check_special_condition(name, key_type, key, values, separator)
	if val != False:
			return val;

	
	if key in force_divide:
		return divide(values, by, separator, maxValue)

	
					
	if len(valueslist) > 1:
		if float(valueslist[0]) < 0:
			#print '%s | %s | negative: %f' % (name, key, float(valueslist[0]));
			#negative, invert sign
			if float(valueslist[0]) > float(valueslist[len(valueslist)-1]):
				#last value is higher than first, then multiply
				return multiply(values, by, separator, maxValue)
			elif float(valueslist[0]) == float(valueslist[len(valueslist)-1]):
				# same value, multiply
				return multiply(values, by, separator, maxValue)
			else:
				#last value is lower than first, then divide
				return divide(values, by, separator, maxValue)
		else:
			if float(valueslist[0]) < float(valueslist[len(valueslist)-1]):
				#last value is higher than first, then multiply
				return multiply(values, by, separator, maxValue)
			elif float(valueslist[0]) == float(valueslist[len(valueslist)-1]):
				# same value, multiply
				return multiply(values, by, separator, maxValue)
			else:
				#last value is lower than first, then divide
				return divide(values, by, separator, maxValue)
	else:
		# only single element, then multiply (parse exceptions in dividelist...)
		return multiply(values, by, separator, maxValue)
	return ' '.join(tmplist)

def export():
	root = KeyValues('SpecificMaxValues')

	for key, value in more_specific_max_value.items():
	
		skillkv = KeyValues(key)

		for inKey, inValue in value.items():
			skillkv[inKey] = inValue

		root[key] = skillkv
			
	root.save('teste.txt')
	print 'fim'


def main():
		
	# remove comments from file (there's bug in _custom that some comments have only an single slash instead of double slash...
	clean.remove_comments('npc_abilities.txt', 'npc_abilities_custom.tmp')
	clean.remove_comments('items.txt', 'items.tmp')
	clean.remove_comments('abilities_custom.txt', 'abilities_custom.tmp')

	kv = KeyValues()
	kv.load('npc_abilities_custom.tmp')

	customkv = KeyValues()
	customkv.load('abilities_custom.tmp')

	itemkv = KeyValues()
	itemkv.load('items.tmp')

	root = KeyValues('DOTAAbilities')
	#rootov = KeyValues('DOTAAbilities')


	for factor in factors:
		print '==== Generating factor: x' +str(factor)+ ' ===='
		rootov = KeyValues('DOTAAbilities')
		print 'Factor x%d (_override.txt)...' % factor

		print 'Generating customs'
		for skill in customkv:
			if skill in dont_parse:
				continue
			skillkv = KeyValues(skill)
			skillkv['BaseClass'] = skill

			if skill in insert_custom_normal:
				for cust in insert_custom_normal[skill]:
					skillkv[cust] = insert_custom_normal[skill][cust]

			for base in customkv[skill]:
				base = str(base)
				if base != 'AbilitySpecial':
					skillkv[base] = divide_or_multiply(skill, 'Normal', base, customkv[skill][base], factor, " ")
			
			if 'AbilitySpecial' in customkv[skill]:
				abilityspecial = KeyValues('AbilitySpecial')
				for element in customkv[skill]['AbilitySpecial']:
					number = KeyValues(element)
					for varElement in customkv[skill]['AbilitySpecial'][element]:                       
						varlist = customkv[skill]['AbilitySpecial'][element][varElement]
						numberValue = divide_or_multiply(skill, 'AbilitySpecial', varElement, varlist, factor, ' ')
						number[varElement] = numberValue
							
					abilityspecial[element] = number
						
				skillkv['AbilitySpecial'] = abilityspecial
					
			rootov[skill] = skillkv
	
		print 'Generating items'
		for item in itemkv:
			if item in dont_parse or item in customkv:
				continue
			
			basekv = KeyValues(item)          
			basekv['BaseClass'] = item

			if item in insert_custom_normal:
				for cust in insert_custom_normal[item]:
					basekv[cust] = insert_custom_normal[item][cust]

			for base in itemkv[item]:
				base = str(base)
				if base != 'AbilitySpecial' and base != 'ItemRequirements':
					basekv[base] = divide_or_multiply(item, 'Normal', base, str(itemkv[item][base]), factor, " ")

			if 'AbilitySpecial' in itemkv[item]:
				basekv['AbilitySpecial'] = KeyValues(itemkv[item])
				for element in itemkv[item]['AbilitySpecial']:
					basekv['AbilitySpecial'][element] = KeyValues(element)
					for varElement in itemkv[item]['AbilitySpecial'][element]:
						values = itemkv[item]['AbilitySpecial'][element][varElement]
						value = divide_or_multiply(item, 'AbilitySpecial', varElement, values, factor, " ")
						basekv['AbilitySpecial'][element][varElement] = value
						#print varElement
			rootov[item] = basekv
				
					
		print 'Generating skills'
		for skill in kv:
			if skill in dont_parse or skill in customkv:
				continue

			skillkv = KeyValues(skill)
			skillkv['BaseClass'] = skill

			for base in kv[skill]:
				base = str(base)
				if base != 'AbilitySpecial':

					if base in dont_parse_more_specific and varElement in dont_parse_more_specific[base]:
						continue

					skillkv[base] = divide_or_multiply(skill, 'Normal', base, kv[skill][base], factor, " ")
			
			if 'AbilitySpecial' in kv[skill]:
				abilityspecial = KeyValues('AbilitySpecial')
				for element in kv[skill]['AbilitySpecial']:
					number = KeyValues(element)
					for varElement in kv[skill]['AbilitySpecial'][element]:

						if skill in dont_parse_more_specific and varElement in dont_parse_more_specific[skill]:
							number = False
							break

						varlist = kv[skill]['AbilitySpecial'][element][varElement]
						numberValue = divide_or_multiply(skill, 'AbilitySpecial', varElement, varlist, factor, ' ')
						number[varElement] = numberValue
							
					if number:
						abilityspecial[element] = number
						
				skillkv['AbilitySpecial'] = abilityspecial
					
			rootov[skill] = skillkv
			#root[skill + '_x'+str(factor)] = skillkv

		rootov.save('npc_abilities_override' + '_x'+str(factor)+'.txt')

		newDivValue = '2'
		if str(factor) in divValue:
			newDivValue = divValue[str(factor)]
		update_addons.updateAddons(factor, newDivValue, modID[factor])
		os.remove('npc_abilities_override' + '_x'+str(factor)+'.txt')
	os.remove('npc_abilities_custom.tmp')
	os.remove('abilities_custom.tmp')
	#update_addons.updateAddons()




def create_customs():
		
	# remove comments from file (there's bug in _custom that some comments have only an single slash instead of double slash...
	clean.remove_comments('npc_abilities.txt', 'npc_abilities_custom.tmp')
	clean.remove_comments('items.txt', 'items.tmp')
	clean.remove_comments('abilities_custom.txt', 'abilities_custom.tmp')
	clean.remove_comments('items_custom.txt', 'items_custom.tmp')

	kv = KeyValues()
	kv.load('npc_abilities_custom.tmp')

	customkv = KeyValues()
	customkv.load('abilities_custom.tmp')

	customitemskv = KeyValues()
	customitemskv.load('items_custom.tmp')

	itemkv = KeyValues()
	itemkv.load('items.tmp')

	#root = KeyValues('DOTAAbilities')
	rootov = KeyValues('DOTAAbilities')
	itemov = KeyValues('DOTAAbilities')

	for factor in factors:
		print '==== Generating factor: x' +str(factor)+ ' ===='
		#rootov = KeyValues('DOTAAbilities')
		print 'Factor x%d (_override.txt)...' % factor

		print 'Generating customs skills'
		for skill in customkv:
			if skill in dont_parse:
				continue
			skillkv = KeyValues(skill)
			skillkv['BaseClass'] = skill

			for base in customkv[skill]:
				base = str(base)
				if base != 'AbilitySpecial':
					skillkv[base] = divide_or_multiply(skill, 'Normal', base, customkv[skill][base], factor, " ")
			
			if 'AbilitySpecial' in customkv[skill]:
				abilityspecial = KeyValues('AbilitySpecial')
				for element in customkv[skill]['AbilitySpecial']:
					number = KeyValues(element)
					for varElement in customkv[skill]['AbilitySpecial'][element]:                       
						varlist = customkv[skill]['AbilitySpecial'][element][varElement]
						numberValue = divide_or_multiply(skill, 'AbilitySpecial', varElement, varlist, factor, ' ')
						number[varElement] = numberValue
							
					abilityspecial[element] = number
						
				skillkv['AbilitySpecial'] = abilityspecial
					
			rootov[skill] = skillkv

		print 'Generating customs items'
		for item in customitemskv:

			if item in dont_parse:
				continue

			basekv = KeyValues(item)

			for base in customitemskv[item]:
				base = str(base)
				basekv[base] = customitemskv[item][base]

			itemov[item] = basekv
		
		print 'Generating items'
		for item in itemkv:
			if item in dont_parse or item in customkv:
				continue

			basekv = KeyValues(item)   
			basekv['BaseClass'] = item
			basekv['ItemPurchasable'] = '0'

			for base in itemkv[item]:
				base = str(base)
				if base != 'AbilitySpecial' and base != 'ItemRequirements':
					if base == 'ItemResult':
						basekv[base] = str(itemkv[item][base]) + '_x' + str(factor)
					else:
						basekv[base] = divide_or_multiply(item, 'Normal', base, str(itemkv[item][base]), factor, " ")
							
			if 'ItemRequirements' in itemkv[item]:
				basekv['ItemRequirements'] = KeyValues(itemkv[item])
				for element in itemkv[item]['ItemRequirements']:
					values = itemkv[item]['ItemRequirements'][element]
					basekv['ItemRequirements'][element] = fix_requeriments(values, factor, ';')


			if 'AbilitySpecial' in itemkv[item]:
				basekv['AbilitySpecial'] = KeyValues(itemkv[item])
				for element in itemkv[item]['AbilitySpecial']:
					basekv['AbilitySpecial'][element] = KeyValues(element)
					for varElement in itemkv[item]['AbilitySpecial'][element]:
						values = itemkv[item]['AbilitySpecial'][element][varElement]
						value = divide_or_multiply(item, 'AbilitySpecial', varElement, values, factor, " ")
						basekv['AbilitySpecial'][element][varElement] = value
						#print varElement
			#rootov[item] = basekv
			itemov[item + '_x'+str(factor)] = basekv
				
					
		print 'Generating skills'
		for skill in kv:
			if skill in dont_parse or skill in customkv:
				continue
			skillkv = KeyValues(skill)
			skillkv['BaseClass'] = skill

			for base in kv[skill]:
				base = str(base)
				if base != 'AbilitySpecial':
					skillkv[base] = divide_or_multiply(skill, 'Normal', base, kv[skill][base], factor, " ")
			
			if 'AbilitySpecial' in kv[skill]:
				abilityspecial = KeyValues('AbilitySpecial')
				for element in kv[skill]['AbilitySpecial']:
					number = KeyValues(element)
					for varElement in kv[skill]['AbilitySpecial'][element]:                       
						varlist = kv[skill]['AbilitySpecial'][element][varElement]
						numberValue = divide_or_multiply(skill, 'AbilitySpecial', varElement, varlist, factor, ' ')
						number[varElement] = numberValue
							
					abilityspecial[element] = number
						
				skillkv['AbilitySpecial'] = abilityspecial
					
			#rootov[skill] = skillkv
			rootov[skill + '_x'+str(factor)] = skillkv
			#root[skill + '_x'+str(factor)] = skillkv

		#rootov.save('npc_abilities_override' + '_x'+str(factor)+'.txt')

		newDivValue = '2'
		if str(factor) in divValue:
			newDivValue = divValue[str(factor)]
		#update_addons.updateAddons(factor, newDivValue, modID[factor])
		#os.remove('npc_abilities_override' + '_x'+str(factor)+'.txt')

	rootov.save('npc_abilities_custom.txt')
	itemov.save('npc_items_custom.txt')
	os.remove('npc_abilities_custom.tmp')
	os.remove('abilities_custom.tmp')
	os.remove('items_custom.tmp')	
	#update_addons.updateAddons()
		

		
if __name__ == "__main__":

	#export()
	main()
	#create_customs()
