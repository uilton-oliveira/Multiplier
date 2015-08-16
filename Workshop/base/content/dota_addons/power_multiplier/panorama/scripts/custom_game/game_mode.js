"use strict";



function CheckForHostPrivileges(panel)
{
	var playerInfo = Game.GetLocalPlayerInfo();
	if ( !playerInfo )
		return undefined;

	// Set the "player_has_host_privileges" class on the panel, this can be used 
	// to have some sub-panels on display or be enabled for the host player.
	$.GetContextPanel().SetHasClass( "player_has_host_privileges", playerInfo.player_has_host_privileges );
	if (panel !== undefined) {
		panel.SetHasClass( "player_has_host_privileges", playerInfo.player_has_host_privileges );
	}
	return playerInfo.player_has_host_privileges;

}

function SelectDefaultGameMode(panel) {
	panel.FindChildTraverse('buffStats').SetSelected(true);
	panel.FindChildTraverse('buffTowers').SetSelected(true);

	var mapInfo = Game.GetMapInfo();


	if (mapInfo.map_display_name == 'curse_of_rivers_end') {
		var rndsk = panel.FindChildTraverse('randomSkills');
		var grndsk = panel.FindChildTraverse('GroupRdnSk');
		rndsk.enabled = true;
		grndsk.enabled = true;
	}
	else if (mapInfo.map_display_name == 'dota_random_skills') {
		var rndsk = panel.FindChildTraverse('randomSkills');
		rndsk.SetSelected(true);
		rndsk.enabled = false;
		var grndsk = panel.FindChildTraverse('GroupRdnSk');
		grndsk.enabled = true;
		grndsk.ToggleClass("disabled");
		panel.FindChildTraverse("PlayMode").SetSelected('ar')
		
	} else {
		panel.FindChildTraverse('randomSkills').enabled = false;
		panel.FindChildTraverse('changeSkillsOnDeath').enabled = false;
	}
}

function DrawGameModeUiSelected() {
	DrawGameModeUiNonHost($.GetContextPanel());
}

function DrawGameModeUiNonHost(panel)
{
	var gameModePanel = undefined;

	if (panel == undefined) {

		gameModePanel = $.CreatePanel( "Panel", $.GetContextPanel(), "" );
		gameModePanel.BLoadLayout( "file://{resources}/layout/custom_game/game_mode.xml", false, false );

	} else {

		gameModePanel = panel;

	}

	gameModePanel.style.x = '-250px';
	gameModePanel.style.opacity = 0;
	gameModePanel.enabled = false;
	gameModePanel.SetHasClass('not_host', true);

	SelectDefaultGameMode(gameModePanel);

	gameModePanel.FindChildTraverse('Group1').SetHasClass('not_host', true);
	gameModePanel.FindChildTraverse('GroupRdnSk').SetHasClass('not_host', true);

	AnimatePanel(gameModePanel, { "transform": "translateX(250px);", "opacity": "1;" }, 1.0, "ease-out"); 
}

function DrawGameModeUi()
{

	var isHost = CheckForHostPrivileges();
	if (isHost === undefined) {
		$.Schedule(1, DrawGameModeUi);
		return;
	}

	//isHost = false;

	if (!isHost) {
		return;
	}

	var gameModePanel = $.CreatePanel( "Panel", $.GetContextPanel(), "" );
	gameModePanel.BLoadLayout( "file://{resources}/layout/custom_game/game_mode.xml", false, false );

	// default values
	SelectDefaultGameMode(gameModePanel);

	// startup animation
	gameModePanel.style.x = '-250px';
	gameModePanel.style.opacity = 0;
	AnimatePanel(gameModePanel, { "transform": "translateX(250px);", "opacity": "1;" }, 1.0, "ease-out"); 

}


// function SetGameModeNonHost(event_data)
// {
// 	var isHost = CheckForHostPrivileges();
// 	if (!isHost) {
// 		return;
// 	}

// 	DrawGameModeUiNonHost();

// 	$.GetContextPanel().FindChildTraverse("PlayMode").SetSelected(event_data.gamemode);
// 	$.GetContextPanel().FindChildTraverse("easyMode").checked = event_data.em;
// 	$.GetContextPanel().FindChildTraverse("buffStats").checked = event_data.bs;
// 	$.GetContextPanel().FindChildTraverse("buffCreeps").checked = event_data.bc;
// 	$.GetContextPanel().FindChildTraverse("buffTowers").checked = event_data.bt;
// 	$.GetContextPanel().FindChildTraverse("randomSkills").checked = event_data.omg;
// 	$.GetContextPanel().FindChildTraverse("TotalSkills").SetSelected(event_data.tskills);
// 	$.GetContextPanel().FindChildTraverse("TotalUltis").SetSelected(event_data.tultis);

// }

function SetGameMode()
{
	GameEvents.SendCustomGameEventToServer( "set_game_mode", 
		{
			  
			"isHost": CheckForHostPrivileges(),
		 	"modes": {
				"gamemode": $.GetContextPanel().FindChildTraverse("PlayMode").GetSelected().id,
				"em": $.GetContextPanel().FindChildTraverse("easyMode").checked,
				"bs": $.GetContextPanel().FindChildTraverse("buffStats").checked,
				"bc": $.GetContextPanel().FindChildTraverse("buffCreeps").checked,
				"bt": $.GetContextPanel().FindChildTraverse("buffTowers").checked,
				"fr": $.GetContextPanel().FindChildTraverse("fastRespawn").checked,
				"omg": $.GetContextPanel().FindChildTraverse("randomSkills").checked,
				"tskills": $.GetContextPanel().FindChildTraverse("TotalSkills").GetSelected().id,
				"tultis": $.GetContextPanel().FindChildTraverse("TotalUltis").GetSelected().id,
				"omgdm": $.GetContextPanel().FindChildTraverse("changeSkillsOnDeath").checked
			}
			 
		} 
	);

	//AnimatePanel($.GetContextPanel(), { "transform": "translateY(10px) scaleY(2);", "opacity": "1;" }, 2, "ease-in", 1);
	AnimatePanel($.GetContextPanel(), { "transform": "translateX(-150px);", "opacity": "0;" }, 0.8); 
	// AnimatePanel($.GetContextPanel(), { "transform": "translateX(100px) translateY(50px) scaleX(1.5) scaleY(1.5);" }, 0.3);
	//AnimatePanel($.GetContextPanel(), { "transform": "scaleX(0.5) scaleY(0.5);", "opacity": "0.3;" });

	$.Schedule(1, DrawGameModeUiSelected);
}


function OnRandomSkillsClick()
{
	//$.Msg($.GetContextPanel());
	//$.GetContextPanel().SetHasClass('invisible', true);
	//GameEvents.SendCustomGameEventToServer( "set_game_mode", { "key1" : "value1", "key2" : "value2" } );
	// $.GetContextPanel().FindChildTraverse("GroupRdnSk").ToggleClass("invisible");
	var rndsk = $.GetContextPanel().FindChildTraverse("GroupRdnSk");
	rndsk.enabled = !rndsk.enabled;
	rndsk.ToggleClass("disabled");

}

(function()
{
	// We use a nettable to communicate victory conditions to make sure we get the value regardless of timing.
	// UpdateKillsToWin();
	// CustomNetTables.SubscribeNetTableListener( "game_state", OnGameStateChanged );

 //    GameEvents.Subscribe( "countdown", UpdateTimer );
 //    GameEvents.Subscribe( "show_timer", ShowTimer );
 //    GameEvents.Subscribe( "timer_alert", AlertTimer );
 //    GameEvents.Subscribe( "overtime_alert", HideTimer );
	//UpdateTimer();

	//GameEvents.Subscribe( "game_mode_was_set", SetGameModeNonHost);

})();

