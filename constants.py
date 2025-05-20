#constants to be imported by other scripts
___CONFIG_FILE___ = "config.ini"
___OPERATING_MODE_LOCAL___ = "local"
___OPERATING_MODE_ONLINE___ = "online"
___TOTAL_NUMBER_OF_POKEMON___ = 1025


#local (CSV) constants
___CSV_POKEMON____ = "Local/pokemon.csv"
___CSV_ABILITIES____ = "Local/abilities.csv"

#online (pokeapi) constants
___BASE_URL___ = "https://pokeapi.co/api/v2/"
___LOOKUP_LIMIT___ = 50

#pokemon object constants
___ALLOWED_TYPES___ = ["Normal","Fire","Water","Grass","Electric","Ice","Fighting","Poison","Ground","Flying","Psychic","Bug","Rock","Ghost","Dragon","Dark","Steel","Fairy"]
___CSV_TYPES___ = "Local/types.csv"
___CSV_TYPE_ABILITIES___ = "Local/type_ability.csv"
___GAME_LIST___ = [
    "Red","Green","Blue","Yellow",
    "Gold","Silver","Crystal",
    "Ruby","Sapphire","Fire Red","Leaf Green","Emerald","Colosseum","XD",
    "Diamond","Pearl","Platinum","Heart Gold","Soul Silver",
    "Black","White","Black 2","White 2",
    "X","Y","Omega Ruby","Alpha Sapphire",
    "Sun","Moon","Ultra Sun","Ultra Moon",
    "Let's Go Pikachu!","Let's Go Eevee!","Sword","Shield","Brilliant Diamond","Shining Pearl","Legends Arceus",
    "Scarlet","Violet"
]

___GAMES_WITH_HIDDEN_ABILITY___ = [
    "Black","White","Black 2","White 2",
    "X","Y","Omega Ruby","Alpha Sapphire",
    "Sun","Moon","Ultra Sun","Ultra Moon",
    "Sword","Shield","Brilliant Diamond","Shining Pearl",
    "Scarlet","Violet"
]

___GAMES_WITH_BEAST_BALL___ = [
    "Sun","Moon","Ultra Sun","Ultra Moon",
    "Sword","Shield",
    "Scarlet","Violet"
]

___CATCH_SYMBOLS___ = ["C", "S", "D", "E", "B", "CD", "DA", "CC", "FS", "EV"]

#Symbol	Meaning
"""Obtainable in-game	
C	The Pokémon can be caught in-game.
S	The Pokémon can be caught in-game, but is only available at certain non-fixed times (e.g. Pokémon found through swarms or changing Pokémon in the Trophy Garden and Great Marsh). In Pokémon Colosseum and Pokémon XD, this instead means Pokémon can be snagged. In Pokémon Sun, Moon, Ultra Sun and Ultra Moon, this instead means Pokémon can be caught through the Island Scan.
D	In Pokémon Diamond, Pearl, and Platinum, the Pokémon can be caught in-game via dual-slot mode. In Pokémon Sword and Shield, the Pokémon can be caught in-game via a Max Raid Battle at a Pokémon Den.
R	The Pokémon can be received from someone (such as first partner Pokémon, revived Fossil, in-game trade or gift).
E	The Pokémon cannot be caught in-game, but an earlier evolutionary stage can be obtained. It can be evolved into the Pokémon in this game.
	This may also be used as a suffix for other methods to indicate that the Pokémon must be evolved from a Pokémon caught using that method.
B	The Pokémon cannot be caught in-game, but a later evolutionary stage can be obtained. It can be bred to produce the Pokémon in this game; this may also involve evolving the hatched Pokémon.
	This may also be used as a suffix for other methods to indicate that the Pokémon must be bred from a Pokémon caught using that method.
CD	The Pokémon can be caught in-game, but is only accessible through paid DLC.
	"D" may also be used as a suffix for other methods to indicate that it can only be obtained through that method in paid DLC.
DA	In Pokémon Sword and Shield's The Crown Tundra DLC, the Pokémon can be caught in-game via a Max Raid Battle during a Dynamax Adventure in the Max Lair.
CC	The Pokémon is obtainable in-game but requires some form of communication with another core series game in order to obtain it.
	This may also be used as a prefix for other methods to indicate that the Pokémon requires a specific method after communicating with another game.
FS	In Pokémon X and Y, the Pokémon can only be caught through the Friend Safari.
EV	The Pokémon can be caught in-game, but only via event distribution (such as Poké Portal News) or using an item obtained exclusively via event distribution (such as the Eon Ticket).
Not obtainable in-game	
PW	The Pokémon is available via the Pokéwalker and can be transferred to Pokémon HeartGold and SoulSilver.
DR	The Pokémon is available via Dream Radar and can be transferred to Pokémon Black 2 and White 2.
DW	The Pokémon was available via Dream World and could be transferred to Pokémon Black, White, Black 2 and White 2 before it was shut down.
ET	The Pokémon cannot be caught in-game, but an earlier evolutionary stage can be obtained. It can be evolved into the Pokémon in this game by trading.
	"T" may also be used as a suffix for other methods to indicate that the Pokémon must be evolved through trading from a Pokémon caught using that method.
Ev	The Pokémon was available to this game at some point via distributions in real life such as ExtremeSpeed Pikachu. Additionally, all Global Link promotions and game-based Pokémon distributions fall under this category.
TE	This Pokémon cannot be caught in-game, but an earlier evolutionary stage can be obtained. It can be evolved into the Pokémon by transferring it to a game in a previous generation and evolving it there.
T	This Pokémon can be obtained only by trading it from another game or transferring it from a game in a previous generation.
—	This Pokémon is unobtainable in this game.
"""