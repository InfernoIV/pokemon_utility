#imports
import csv, sys
from termcolor import colored, cprint
from type_fuctions import get_weakness


#https://pypi.org/project/termcolor/

#constants
___NUMBER_OF_POKEMON___ = 1010
___CSV_POKEMON____ = "pokemon.csv"



#Return data, according to input
#either number or name
def get_pokemon_data(input_raw):
    #sanatize
    input_sanatized = str(input_raw).lower()

    #set to number
    dict_keys = "name"
    #check if name input (if number or not)
    #check if it starts with a number (normal pokemon do not start with a number)
    if input_sanatized[0].isdigit():
        #remove the leading '0's
        input_sanatized = input_sanatized.lstrip("0")
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
    #TODO: WHY IS TYPE ABILITIES GROWING???
    #for every pokemon
    for index in range(1, ___NUMBER_OF_POKEMON___):
        #get 
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
    if pokemon_object.form_name != "":
        name += " " + pokemon_object.form_name
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
def get_base_pokemon(pokemon_id):
    #get data of the pokemon
    pokemon, error = get_pokemon_data(pokemon_id)
    #check for errors
    if error is not None:
        #return the error
        return None, f"get_base_pokemon: Pokemon not found! {error}"
    else:
        #get to the lowest evolution
        #if there is a predecessor
        while len(pokemon.predecessors) > 0:
            #get the (first) predecessor
            pokemon, error = get_pokemon_data(pokemon.predecessors[0])
            #if error
            if error is not None:
                #return the error
                return None, f"get_base_pokemon(inner): Pokemon not found! {error}" 
        #return this pokemon
        return pokemon, None
    
    

#function the print information to the console
def describe_pokemon(input):
    #get data of the pokemon
    pokemon, error = get_pokemon_data(input)    
    
    #print(f"pokemon: {str(pokemon)}")
    #check if success
    if error is not None:
        #print error
        #print(error)
        #stop
        return
    
    #print report
    #describe the name
    name = pokemon.name
    #if it is a specific form
    if pokemon.form_name != "":
        #add to name
        name += f" ({pokemon.form})"
    #print the number and name
    cprint(f"Pokemon #{pokemon.number}: {pokemon.name}", None, attrs=["bold", "underline"])
    #print types
    type_string = "Type: "
    #if there is only 1 ability
    if len(pokemon.type) == 1:
        #only print the first one
        type_string += f"{"".join(pokemon.type)}"
    else: 
        #print both abilities
        type_string += f"{", ".join(pokemon.type)}"
    #print the type
    print(f"{type_string}")

    #get the abilities
    ability_string = "Abilities: "
    #if there is only 1 ability
    if len(pokemon.abilities) == 1:
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

    #get the type match-up
    weaknesses = get_weakness(pokemon)
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
    evolution_tree, _ = get_evolution_line(pokemon.name)
    #print the evolution tree
    print(f"Evolutions: {", ".join(evolution_tree)}")

    #empty line
    print("")



#pokemon object, containing information of the pokemon
class pokemon(object):
    #properties
    number = -1
    name = ""
    form_name = ""
    form_type = ""
    type = []
    abilities = []
    hidden_ability = ""
    predecessors = []
    successors = []

    # The class "constructor" - It's actually an initializer 
    def __init__(self, dict):
        #print(f"dict: {dict}")
        self.number = -1
        self.name = ""
        self.form_name = ""
        self.form_type = ""
        self.type = []
        self.abilities = []
        self.hidden_ability = ""
        self.predecessors = []
        self.successors = []

        #description
        #add number
        self.number = dict["number"]
        #add name
        self.name = dict["name"]
        #add form name (for description)
        self.form_name = dict["form-name"]
        #TODO: add form type (to check)
        self.form_type = dict["form-type"]

        #typing
        #always add type 1
        self.type.append(dict["type-1"])        
        #if it has a secondary type
        if dict["type-2"] != "":
            #add it
            self.type.append(dict["type-2"])

        #ability-1,ability-2,ability-hidden,predecessors,successors
        #abilities
        #always add ability 1
        self.abilities.append(dict["ability-1"])
        #if it has a secondary ability
        if dict["ability-2"] != "":
            #add it
            self.abilities.append(dict["ability-2"])
        #if it has a hidden ability
        if dict["ability-hidden"] != "":
            self.hidden_ability = dict["ability-hidden"]

        #Evolutions
        #if it has previous evolutions
        if dict["predecessors"] != "": 
            #save them
            self.predecessors = dict["predecessors"].split(",")
        #if it has next evolutions
        if dict["successors"] != "": 
            #save them
            self.successors = dict["successors"].split(",")
    
    def __repr__(self):
        return f"number: '{self.number}', name: '{self.name}', form_name: '{self.form_name}', form_type: '{self.form_type}', type: '{self.type}', abilities: '{self.abilities}', hidden_ability: '{self.hidden_ability}', predecessors: '{self.predecessors}', successors: '{self.successors}'"