#imports
import csv, sys



#constants
___NUMBER_OF_POKEMON___ = 151 #1010
___CSV_POKEMON____ = "pokemon.csv"
___CSV_TYPES___ = "types.csv"

#Return data, according to input
#either number or name
def get_pokemon_data(input_raw):
    #sanatize
    input_sanatized = str(input_raw).lower()

    #set to number
    dict_keys = "name"
    #check if name input
    if input_sanatized.isdigit():
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
        index = str(index)
        #print(f"index not in numbers_processed: {index} = {index not in numbers_processed}")
        if index not in numbers_processed:
            evolution_tree, evolution_numbers = get_evolutions(index)
            print(f"{", ".join(evolution_tree)}")
            #families.append(evolution_tree)
            numbers_processed = numbers_processed + evolution_numbers
            #print(numbers_processed)
        #print(f"{'\r\n'.join(families)}")
    




#function to get the whole evolution line
def get_evolutions(input):
    #print(f"get_evolutions: {input}")
    #variable to fill and return
    evolution_tree = []
    evolution_numbers = []
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
                print(error)
                
        #add pokemon to the tree
        evolution_tree.append(pokemon.name)
        evolution_numbers.append(pokemon.number)
        #check evolutions
        while len(pokemon.successors) > 0:
            pokemon, error = get_pokemon_data(pokemon.successors[0])
            if error is not None:
                print(error)
            else:
                evolution_tree.append(pokemon.name)
                evolution_numbers.append(pokemon.number)

    return evolution_tree, evolution_numbers



#assuming object input
def get_weakness(input):
    #keep track of scores
    score = {
        4: [],
        2: [],
        1: [],
        0.5: [],
        0.25: [],
        0: [],
    }
 
    #used multiple times
    filename = ___CSV_TYPES___
    #use the csv as data source
    with open(filename) as csvfile: 
        #use a dict
        reader = csv.DictReader(csvfile)
        try:
            for row in reader:
                attack_type = row["Type"] 
                
                multiplier_1 = row[input.type[0]]
                if multiplier_1 == "":
                    multiplier_1 = float(1)
                else:
                    multiplier_1 = float(multiplier_1)
                damage_multiplier = multiplier_1
                
                if len(input.type) > 1 and input.type[1] != "":
                    multiplier_2 = row[input.type[1]]
                    if multiplier_2 == "":
                        multiplier_2 = float(1)
                    else:
                        multiplier_2 = float(multiplier_2)
                    damage_multiplier = damage_multiplier * multiplier_2
                
                #add to score list
                score[damage_multiplier].append(attack_type)
        
        #if exception
        except csv.Error as e:
            #print and exit
            sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))
    #default return value
    return score          




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
    print(f"Pokemon #{pokemon.number}: {pokemon.name}")
    
    evolution_tree, _ = get_evolutions(pokemon.name)
    print(f"Evolution tree: {", ".join(evolution_tree)}")

    print(f"Type: {", ".join(pokemon.type)}")
    ability_string = "Abilities: "
    if pokemon.abilities[1] == "":
        ability_string += f"{"".join(pokemon.abilities)}"
    else: 
        ability_string += f"{", ".join(pokemon.abilities)}"
    
    if pokemon.hidden_ability != "": 
        ability_string += f" ({pokemon.hidden_ability})"
    print(ability_string)

    weakness = get_weakness(pokemon)
    print(f"Weakness: {weakness}")



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