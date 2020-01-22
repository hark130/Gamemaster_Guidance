# Gamemaster_Guidance
GM aid for Pathfinder 2nd Edition written in Python 3

## TO DO
1. Add names for all races

	[X] 1.1. Dwarf<br>
	[X] 1.2. Elf<br>	
	[X] 1.3. Gnome<br>	
	[X] 1.4. Goblin<br>	
	[X] 1.5. Halfling<br>	
	[X] 1.6. Human<br>
		* 1.6.1 Garundi<br>
		* 1.6.2 Keleshite<br>
		* 1.6.3 Kellid<br>
		* 1.6.4 Mwangi<br>
		* 1.6.5 Nidalese (not found)<br>
		* 1.6.6 Shoanti<br>
		* 1.6.7 Taldan<br>
		* 1.6.8 Tian<br>
		* 1.6.9 Ulfen<br>
		* 1.6.10 Varisian<br>
		* 1.6.11 Vudrani<br>
	[X] 1.7. Half-Elf<br>
	[X] 1.8. Half-Orc<br>

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
	[X] 4. Expand GG_city class to determine city attributes<br>
		- http://legacy.aonprd.com/gameMasteryGuide/settlements.html<br>
		- https://www.d20pfsrd.com/gamemastering/other-rules/kingdom-building/settlements/#Guards_Guards<br>
		- Use D&D 3.5 DM's Guide "Generating Towns" (P. 137) to randomize NPCs levels/classes<br>
	[X] 5. Finish the implementation of "parse_city" method in GG_City (finished? in 11-2)<br>
	[ ] 6. Update NPC generation of "NPC Classes" (e.g., Adept, Warrior) once Paizo releases them for 2nd edition
	[ ] 7. Add support for magic item generation.  While you're at it, add functionality to print the magic items in the Marketplace as well.<br>
	[ ] 8. Add support for user-driven "Notable NPCs".  Don't make it mandatory.  Print it if available under DEMOGRAPHICS.<br>

6. Add "quirks" to character creation

	[ ] 1. Use:<br>
		- https://nerdsonearth.com/2016/01/creating-memorable-npc-100-character-quirks/<br>
		- http://dndspeak.com/2017/12/100-personality-quirks/<br>
		- D&D 3.5 Dungeon Master's Guide P. 128<br>

7. Expand the Human ethnicity of Tian

	[ ] 1. Add all subgroups to the Human ethnicity of Tian<br>

8. Human ethnicity Nidalese

	[ ] 1. Find and implement character functionality for the Nidalese ethnicity (missing?!)<br>

9. Double back and implement the "validate defined" method for the "GG City" class

	[X] 1. Base Value (completed in 5-4)<br>
	[ ] 2. Magic Items (always recalculate?)<br>
	[X] 3. Modifiers (Accomplished(?) in 5-4)<br>
	[X] 4. NPCs (Accomplished in 5-4)<br>
	[X] 5. Purchase Limit (Accomplished(?) in 5-4)<br>
	[X] 6. Spellcasting (Accomplished(?) in 5-4)<br>
	[X] 7. Type (completed in 5-4)<br>

10. Update remaining settlement status

	[X] 1. Spellcasting (e.g., Magical government) (Accomplished in 5-4)<br>
	[X] 2. Base Value (e.g., Notorious quality) (Accomplished in 5-4)<br>
	[X] 3. Purchase Limit (e.g., Prosperous) (Accomplished in 5-4)<br>
	[ ] 4. Danger<br>

11. Support new city functionality

	[X] 1. Print city information in a standardized format (Implemented in 11-2)<br>
	[X] 2. Add a city section to the menu<br>

12. Miscellaneous

    [ ] 1. AESTHETIC: Don't print notes for characters if there are no notes<br>
    [ ] 2. BUG: REfactor GG_City DEMOGRAPHICS-Population string construction to use parsed attributes (raceLookup) instead of cityDict<br>
    [ ] 3. BUG: Verify there's no way for calculated NPC levels to go below 0.  (e.g., smallest city type + lowest roll)
    [ ] 4. AESTHETIC: Properly pluralize ancestries when calculating Demographic Populations in GG_City's "print city details" functionality
    [ ] 5. BUG?: Why am I printing things from the dictionary instead of parsing to class attributes and then printing?!
