# Gamemaster_Guidance
GM aid for Pathfinder 2nd Edition written in Python 3

## TO DO
1. Add names for all races

	[X] 1.1. Dwarf<br>
	[X] 1.2. Elf<br>	
	[X] 1.3. Gnome<br>	
	[X] 1.4. Goblin<br>	
	[X] 1.5. Halfling<br>	
	[/] 1.6. Human<br>
		[X] 1.6.1 Garundi
		[X] 1.6.2 Keleshite
		[ ] 1.6.3 Kellid
		[ ] 1.6.4 Mwangi
		[ ] 1.6.5 Nidalese
		[ ] 1.6.6 Shoanti
		[ ] 1.6.7 Taldan
		[ ] 1.6.8 Tian
		[ ] 1.6.9 Ulfen
		[ ] 1.6.10 Varisian
		[ ] 1.6.11 Vudrani
	[ ] 1.7. Half-Elf<br>	
	[ ] 1.8. Half-Orc<br>

2. Main CLI Menu

	[X] 1. Randomize a name<br>
	[X] 2. Randomize a character<br>
	[ ] 3. Randomize a bounty<br>

3. Custom Exceptions for new classes

	[ ] 1. GG_Ancestry Exception to indicate unsupported feature<br>
	[ ] 2. GG_Character(?) Exception<br>

4. Randomize Something

	[X] 1. Trait - Randomize one or more traits for a character<br>
	[ ] 2. REfactor GG_Menu's "randomize a name" entry into "randomize [something]" and create a sub-menu<br>

5. Read city-based yml file to calculate geographic bias

	[X] 1. Take an argument (setting configuration file)<br>
	[X] 2. Parse yaml configuration file<br>
	[X] 3. Create GG_city class to parse city input<br>
	[ ] 4. Expand GG_city class to determine city attributes<br>
		- http://legacy.aonprd.com/gameMasteryGuide/settlements.html<br>
		- https://www.d20pfsrd.com/gamemastering/other-rules/kingdom-building/settlements/#Guards_Guards<br>
		- Use D&D 3.5 DM's Guide "Generating Towns" (P. 137) to randomize NPCs levels/classes<br>

6. Add "quirks" to character creation

	[ ] 1. Use:<br>
		- https://nerdsonearth.com/2016/01/creating-memorable-npc-100-character-quirks/<br>
		- http://dndspeak.com/2017/12/100-personality-quirks/<br>
		- D&D 3.5 Dungeon Master's Guide P. 128<br>
