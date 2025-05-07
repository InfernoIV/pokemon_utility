#script functions that handles all pokemon specific comparisons and calculations


#imports
import sys
from termcolor import colored, cprint #https://pypi.org/project/termcolor/
from data_processing import get_pokemon
from type import get_weakness



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
    #print types
    type_string = "Type: "
    #if there is only 1 ability
    if len(pokemon_obj.type) == 1:
        #only print the first one
        type_string += f"{"".join(pokemon_obj.type)}"
    else: 
        #print both abilities
        type_string += f"{", ".join(pokemon_obj.type)}"
    #print the type
    print(f"{type_string}")

    #get the abilities
    ability_string = "Abilities: "
    #if there is only 1 ability
    if len(pokemon_obj.abilities) == 1:
        #only print the first one
        ability_string += f"{"".join(pokemon_obj.abilities)}"
    else: 
        #print both abilities
        ability_string += f"{", ".join(pokemon_obj.abilities)}"
    #if there is a hidden abilty
    if pokemon_obj.hidden_ability != "": 
        #add the hidden ability
        ability_string += f" ({pokemon_obj.hidden_ability})"
    #print abilities
    print(ability_string)

    #get the type match-up
    weaknesses = get_weakness(pokemon_obj)
    #for each weakness
    for weakness in weaknesses:
        modifier = weakness[0]
        types = ", ".join(weakness[1])
       
        #print(f"weakness key: {key} = {0 < value < 1}")
        if modifier > float(1): 
            cprint(f"Super Effective ({modifier}): {types}", "green")
        elif modifier <= float(0):
            cprint(f"Immune ({modifier}): {types}", "red", attrs=["bold","underline"])
        elif modifier != float(1):
            cprint(f"Not very effective ({modifier}): {types}", "red")   

    #get the evolution tree
    #evolution_tree, _ = get_evolution_line(pokemon.name)
    #print the evolution tree
    #print(f"Evolutions: {", ".join(evolution_tree)}")

    #empty line
    print("")



#function that creates a filter and then retrieves the matching pokemon
def get_pokemon_data(**kwargs): 
    #create the filter
    filter = create_filter(kwargs)
    #get the pokemon(s)
    pokemon_list = get_pokemon(filter)
    #return the pokemon
    return pokemon_list



#function that creates the filter
def create_filter(kwargs):
    #create local object to keep track of the filters
    filter = { 
        "number": "", #number of the pokemon (can be specfic but also be "generic" in case of regional forms) (number)
        "name": "", #name of the pokemon (name)
        "form": "", #searching for a specific form (form)
        "classification": "", #classification for legendary or mythical (classification)
        "type": "", #specific type (type-1 or type-2)
        "types": "", #specific type combination (type-1,type-2 or type-2,type-1)
        "ability": "", #specific ability (ability-1,ability-2,ability-hidden)
    }

    #for each key that we accept
    for key in filter:
        #if it is described
        if key in kwargs:
            #copy it
            filter[key] = kwargs[key]
    #remove empty keys
    empty_keys = []
    for key in filter:
        #if it is empty
        if filter[key] == "":
            #add it to the list
            empty_keys.append(key)
    #for each empty filter
    for key in empty_keys:
        #delete it
        del filter[key]
    #return the filter
    return filter
