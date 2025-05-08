#script functions that handles all pokemon specific comparisons and calculations
#to be used:
# describe_pokemon (described the pokemon)

#imports
import operator
from termcolor import colored, cprint #https://pypi.org/project/termcolor/
from data_conversion import get_pokemon
#from type import determine_type_matchups



#function the print information to the console
#assuming pokemon object as input
def describe_pokemon(pokemon_obj): 
    #describe the name
    name = pokemon_obj.name
    #if it is a specific form
    if pokemon_obj.form_name != "":
        #add to name
        name += f" ({pokemon_obj.form_name})"
    #print the number and name
    cprint(f"Pokemon #{pokemon_obj.number}: {name}", None, attrs=["bold", "underline"])
   
    #print the type
    print(f"Type: {", ".join(pokemon_obj.type)}")

    #print abilities
    print(f"Abilities: {", ".join(pokemon_obj.all_abilities)}")



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



