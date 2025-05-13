#script functions that handles all pokemon specific comparisons and calculations
#to be used:
# describe_pokemon (described the pokemon)

#imports
import operator
from termcolor import colored, cprint #https://pypi.org/project/termcolor/
from data_csv_functions import get_pokemon
from data_json_functions import get_pokemon_from_api, get_ability_data
#from type import determine_type_matchups



#function to determine the generation of the pokemon
def determine_generation(pokemon_obj):
    #check form first, since this can give away the generation
    #forms for region
    regional_forms = {
        "Alolan":7,
        "Galarian":8,
        "Hisuian":8,
        "Paldean":9,
    }
    #get the form to check for alternate forms
    form = pokemon_obj.form_name
    if form in regional_forms:
        #return the generation of this form
        return regional_forms[form]
    
    #otherwise normal processing
    #get the number of the pokemon
    number = pokemon_obj.number
    #if it is an alternate form
    while not number[len(number)-1].isdigit():
        #remove the last character
        number = number[:-1]
    #convert to number
    number = int(number)

    generation = [
        1,#-151
        152,#-251
        252,#-386
        387,#-493
        494,#-649
        650,#-721
        722,#-809
        810,#-905
        906,#-1010
    ]
    #for each generation
    for gen in range(len(generation)):
        start_value_of_generation = generation[gen]
        #if lower than the current generation
        if number < start_value_of_generation:
            #return the index (which is 1 lower than the current generation)
            return gen
    #return the highest generation
    return len(generation)    



#function to describe pokemon using the data from pokeapi
def describe_pokemon_from_api(pokemon_obj):
    #get the pokemon from pokemon api
    pokemon_api_obj = get_pokemon_from_api(pokemon_obj)
    #describe this
    describe_pokemon(pokemon_api_obj)



#function the print information to the console
#assuming pokemon object as input
def describe_pokemon(pokemon_obj): 
    #describe the name
    name = pokemon_obj.name
    #if it is a specific form
    if pokemon_obj.form_name != "":
        #add to name
        name += f" ({pokemon_obj.form_name})"
    #get the generation
    generation = determine_generation(pokemon_obj)
    #print the number and name
    cprint(f"Pokemon #{pokemon_obj.number} (gen {generation}): {name}", None, attrs=["bold", "underline"])

    #print abilities
    cprint(f"Abilities: ", None ,attrs=["underline"])#{", ".join(pokemon_obj.all_abilities)}")

    for ability in pokemon_obj.all_abilities:
        ability_data = get_ability_data(ability)
        print(f"{ability_data.name}: {ability_data.effect}")

    #print the type
    cprint(f"Type: {", ".join(pokemon_obj.type)}", None ,attrs=["underline"])

    #get the type match-up
    type_matchups = pokemon_obj.calculate_type_matchups()
    #convert for better reporting
    modifier_list = convert_type_matchups(type_matchups)
    #check if we need to create spacing
    if len(modifier_list) > 1:
        #empty line
        print("")

    #for each weakness
    for matchup in modifier_list:
        #if there are multiple configs
        if len(modifier_list) > 1:
            #print the ability for this config
            print(f"Modifiers with: {matchup}")
        #get the modifiers of this matchup
        modifiers = modifier_list[matchup]
        #for every modifier
        for entry in modifiers:
            #get the modifier
            modifier = entry[0]
            #get the types
            types = entry[1]
            
            if modifier > float(1): 
                cprint(f"Super Effective ({modifier}): {", ".join(types)}", "green")
            elif modifier == float(0):
                cprint(f"No effect ({modifier}): {", ".join(types)}", "red", attrs=["bold"])
            elif modifier < float(0):
                cprint(f"Absorb ({modifier}): {", ".join(types)}", "red", attrs=["bold","underline"])
            elif modifier != float(1):
                cprint(f"Not very effective ({modifier}): {", ".join(types)}", "red") 
            else:
                print(f"Effective: ({modifier}): {", ".join(types)}")
        #empty line
        print("")
    #spacer
    print("------------------------------------------------------------")



#function that converst type match to an list with scores which contains the typings instead of typings which contain their score 
def convert_type_matchups(type_matchups):
    #create list to print later
    type_matchups_modifiers = {}
    #group them, largest modifier first
    #for every possible ability which affects type
    for type_matchup in type_matchups:
        #create list
        modifiers = {}
        #get the types
        types = type_matchups[type_matchup]
        #for every type
        for type in types:
            #get the modifier
            modifier = types[type]
            #set to int if possible
            if modifier % 1 == 0:
                #convert to whole number (if a whole number)
                modifier = int(modifier)
            #check if entry exists
            if modifier not in modifiers:
                #create empty list
                modifiers[modifier] = []
            #add to list
            modifiers[modifier].append(type)
        #reverse sort (highest first)
        modifiers_sorted = sorted(modifiers.items(), key=operator.itemgetter(0), reverse=True)
        #add to total list
        type_matchups_modifiers[type_matchup] = modifiers_sorted    
    #return the modifiers
    return type_matchups_modifiers
