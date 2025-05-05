#imports
import csv, sys
from termcolor import colored, cprint
from type_fuctions import get_weakness


#https://pypi.org/project/termcolor/

#constants
___NUMBER_OF_POKEMON___ = 151 #1010
___CSV_POKEMON____ = "pokemon.csv"



#Return data, according to input
#either number or name
def get_pokemon_data(input_raw):
    #sanatize
    input_sanatized = str(input_raw).lower()

    #set to number
    dict_keys = "name"
    #check if name input
    if input_sanatized.isdigit():
        #remove the first '0' by converting to int (and then back to str)
        input_sanatized = str(int(input_sanatized))
        dict_keys = "number"
    #debug
    #print(f"get_pokemon_data '{dict_keys}' '{input_sanatized}'")
    #used multiple times
    filename = ___CSV_POKEMON____
    #use the csv as data source
    with open(filename) as csvfile: 
        #use a dict
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                #if it matches what we are looking for
                if row[dict_keys].lower() == input_sanatized:
                    #convert the data to an object
                    pokemon_object = pokemon(row)
                    #debug
                    #print(f"Found pokemon for '{input_sanatized}': {pokemon_object.name}")
                    #return the object
                    return pokemon_object, None 
        #if exception
        except csv.Error as e:
            #print and exit
            sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))
    #default return value
    return None, f"Pokemon '{input_sanatized}' not found! ({input_raw})"



#function to get all pokemon families
def get_families():
    numbers_processed = []
    families = []
    print("Pokemon families:")
    for index in range(1, ___NUMBER_OF_POKEMON___):
        #convert to string for lookup
        index = str(index)
        #if not already processed
        if index not in numbers_processed:
            #get the evolution line
            evolution_tree, evolution_numbers = get_evolution_line(index)
            #print the evolution line
            print(f"{", ".join(evolution_tree)}")
            #families.append(evolution_tree)
            numbers_processed = numbers_processed + evolution_numbers

    

#describe all pokemon
def describe_pokemon_all():
    #for every pokemon
    for index in range(1, ___NUMBER_OF_POKEMON___):
        pokemon = str(index)
        #describe the pokemon
        describe_pokemon(pokemon)



#function to get the whole evolution line
def get_evolution_line(input):
    #print(f"get_evolutions: {input}")
    #variable to fill and return
    evolution_tree = []
    evolution_numbers = []
    #get the base pokemon
    base_pokemon, error = get_base_pokemon(input)
    #check for errors
    if error is not None:
        print(f"get_evolution_line: {error}")
    else:
        #print(f"Start get_evolutions: get_base_pokemon('{input}')")
        #get the evolution tree
        get_evolutions(base_pokemon, evolution_tree, evolution_numbers)
    #return data
    return evolution_tree, evolution_numbers



#[names, numbers], error
def get_evolutions(pokemon_object, evolution_tree, evolution_numbers):
    #guard clause, check object
    if not hasattr(pokemon_object, 'name'):
        print(f"Pokemon object")

    #determine the name of the pokemon
    name = pokemon_object.name
    #if it is a specific form:
    if pokemon_object.form != "":
        name += " " + pokemon_object.form
    #add information of the current pokemon
    evolution_tree.append(name)
    evolution_numbers.append(pokemon_object.number)
    #for each successor
    for evolution in pokemon_object.successors:
        #get object
        successor, error = get_pokemon_data(evolution)
        #if error occurred
        if error is not None:
            #print error
            print(f"get_evolutions: {error}")
        else:
            #go deeper
            get_evolutions(successor, evolution_tree, evolution_numbers)
    return



#get the lowest level pokemon
def get_base_pokemon(input):
    #get data of the pokemon
    pokemon, error = get_pokemon_data(input)
    #check for errors
    if error is not None:
        print(error)
    else:
        #get to the lowest evolution
        while len(pokemon.predecessors) > 0:
            pokemon, error = get_pokemon_data(pokemon.predecessors[0])
            if error is not None:
                print(f"get_base_pokemon: {error}")
        return pokemon, None
    return None, "get_base_pokemon: Pokemon not found!"






#function the print information to the console
def describe_pokemon(input):
    #get data of the pokemon
    pokemon, error = get_pokemon_data(input)
    #check if success
    if error is not None:
        #print error
        print(error)
        #stop
        return
    #print report
    #describe the name
    name = pokemon.name
    #if it is a specific form
    if pokemon.form != "":
        #add to name
        name += f" ({pokemon.form})"
    #print the number and name
    cprint(f"Pokemon #{pokemon.number}: {pokemon.name}", None, attrs=["bold", "underline"])
    #print types
    type_string = "Type: "
     #if there is only 1 ability
    if pokemon.type[1] == "":
        #only print the first one
        type_string += f"{"".join(pokemon.type)}"
    else: 
        #print both abilities
        type_string += f"{", ".join(pokemon.type)}"

    print(f"{type_string}")
    #get the abilities
    ability_string = "Abilities: "
    #if there is only 1 ability
    if pokemon.abilities[1] == "":
        #only print the first one
        ability_string += f"{"".join(pokemon.abilities)}"
    else: 
        #print both abilities
        ability_string += f"{", ".join(pokemon.abilities)}"
    #if there is a hidden abilty
    if pokemon.hidden_ability != "": 
        #add the hidden ability
        ability_string += f" ({pokemon.hidden_ability})"
    
    #print abilities
    print(ability_string)

    #print evolution tree
    evolution_tree, _ = get_evolution_line(pokemon.name)
    print(f"Evolutions: {", ".join(evolution_tree)}")

    #get the type match-up
    weaknesses = get_weakness(pokemon)
    
    #for each
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

    #empty line
    print("")



#pokemon object, containing information of the pokemon
class pokemon(object):
    number = -1
    name = ""
    form = ""
    type = []
    abilities = []
    hidden_ability = ""
    predecessors = []
    successors = []

    # The class "constructor" - It's actually an initializer 
    def __init__(self, dict):
        #print(f"dict: {dict}")
        
        self.number = dict["number"]
        self.name = dict["name"]
        self.form = dict["form"]
        self.type = dict["type"].split(",")

        abilities = dict["abilities"].split(",")
        self.abilities = [abilities[0], abilities[1]]
        self.hidden_ability = abilities[2]

        predecessors_list = dict["predecessors"].split(",")
        if predecessors_list[0] != '': 
            self.predecessors = predecessors_list

        successors_list = dict["successors"].split(",")
        if successors_list[0] != '': 
            self.successors = successors_list
